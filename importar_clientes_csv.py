#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Importador de clientes a partir de arquivo CSV
Suporta grandes volumes (milhares de registros)
"""

import psycopg2
import csv
import sys
import re
from datetime import datetime

def validar_email(email):
    """Valida formato de email"""
    if not email:
        return False
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

def formatar_telefone(telefone):
    """Formata telefone para padrão (XX) XXXXX-XXXX"""
    if not telefone:
        return None
    
    numeros = re.sub(r'\D', '', telefone)
    
    if len(numeros) == 11:
        return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
    elif len(numeros) == 10:
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
    else:
        return telefone

def conectar():
    """Conecta ao banco de dados"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="sistema_clientes",
            user="postgres",
            password="postgres"
        )
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return None

def importar_csv(arquivo_csv, pular_duplicados=True):
    """Importa clientes de arquivo CSV"""
    
    print("\n" + "=" * 80)
    print("📥 IMPORTAÇÃO DE CLIENTES - CSV")
    print("=" * 80)
    print(f"\n📂 Arquivo: {arquivo_csv}")
    print(f"📅 Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    conn = conectar()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Ler CSV
        with open(arquivo_csv, 'r', encoding='utf-8') as file:
            # Detectar delimitador
            sample = file.read(1024)
            file.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            
            reader = csv.DictReader(file, delimiter=delimiter)
            
            # Estatísticas
            total_linhas = 0
            importados = 0
            erros = 0
            duplicados = 0
            erros_lista = []
            
            print("🔄 Processando...")
            print("-" * 80)
            
            for linha_num, row in enumerate(reader, start=2):  # Linha 2 porque linha 1 é cabeçalho
                total_linhas += 1
                
                try:
                    # Extrair dados (adaptar conforme colunas do CSV)
                    nome = row.get('nome', '').strip()
                    email = row.get('email', '').strip()
                    telefone = row.get('telefone', '').strip()
                    cidade = row.get('cidade', '').strip()
                    
                    # Validações básicas
                    if not nome or len(nome) < 3:
                        raise ValueError("Nome inválido ou muito curto")
                    
                    if not email or not validar_email(email):
                        raise ValueError("Email inválido")
                    
                    # Formatar telefone
                    telefone = formatar_telefone(telefone)
                    
                    # Verificar duplicado (por email)
                    if pular_duplicados:
                        cursor.execute("SELECT id FROM clientes WHERE email = %s", (email,))
                        if cursor.fetchone():
                            duplicados += 1
                            print(f"⚠️  Linha {linha_num}: Email duplicado - {email}")
                            continue
                    
                    # Inserir
                    query = """
                        INSERT INTO clientes (nome, email, telefone, cidade)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query, (nome, email, telefone, cidade))
                    
                    importados += 1
                    
                    # Mostrar progresso a cada 100 registros
                    if importados % 100 == 0:
                        print(f"✅ {importados} clientes importados...")
                
                except Exception as e:
                    erros += 1
                    erro_msg = f"Linha {linha_num}: {str(e)}"
                    erros_lista.append(erro_msg)
                    if erros <= 10:  # Mostrar apenas os primeiros 10 erros
                        print(f"❌ {erro_msg}")
            
            # Commit
            conn.commit()
            
            # Relatório final
            print("\n" + "=" * 80)
            print("📊 RELATÓRIO DE IMPORTAÇÃO")
            print("=" * 80)
            print(f"\n📄 Total de linhas processadas: {total_linhas}")
            print(f"✅ Clientes importados: {importados}")
            print(f"⚠️  Duplicados ignorados: {duplicados}")
            print(f"❌ Erros: {erros}")
            print(f"\n📅 Término: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            
            if erros > 10:
                print(f"\n⚠️  Foram encontrados {erros} erros. Mostrando apenas os 10 primeiros.")
            
            print("\n" + "=" * 80)
            
            # Salvar log de erros
            if erros_lista:
                log_file = f"log_importacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(log_file, 'w', encoding='utf-8') as log:
                    log.write("LOG DE ERROS - IMPORTAÇÃO DE CLIENTES\n")
                    log.write("=" * 80 + "\n\n")
                    for erro in erros_lista:
                        log.write(erro + "\n")
                print(f"\n📝 Log de erros salvo em: {log_file}")
        
        cursor.close()
        conn.close()
        
    except FileNotFoundError:
        print(f"\n❌ Arquivo não encontrado: {arquivo_csv}")
    except Exception as e:
        print(f"\n❌ Erro durante importação: {e}")
        if conn:
            conn.rollback()
            conn.close()

def criar_csv_exemplo():
    """Cria um arquivo CSV de exemplo"""
    arquivo = "clientes_exemplo.csv"
    
    with open(arquivo, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        
        # Cabeçalho
        writer.writerow(['nome', 'email', 'telefone', 'cidade'])
        
        # Dados de exemplo
        writer.writerow(['João Silva', 'joao.silva@email.com', '11987654321', 'São Paulo'])
        writer.writerow(['Maria Santos', 'maria.santos@email.com', '21987654321', 'Rio de Janeiro'])
        writer.writerow(['Pedro Oliveira', 'pedro.oliveira@email.com', '31987654321', 'Belo Horizonte'])
        writer.writerow(['Ana Costa', 'ana.costa@email.com', '41987654321', 'Curitiba'])
        writer.writerow(['Carlos Souza', 'carlos.souza@email.com', '51987654321', 'Porto Alegre'])
    
    print(f"\n✅ Arquivo de exemplo criado: {arquivo}")
    print("\n📋 Formato do CSV:")
    print("-" * 80)
    print("nome,email,telefone,cidade")
    print("João Silva,joao.silva@email.com,11987654321,São Paulo")
    print("Maria Santos,maria.santos@email.com,21987654321,Rio de Janeiro")
    print("-" * 80)
    print("\n💡 Edite este arquivo ou crie um novo seguindo este formato!")

def menu():
    """Menu principal"""
    print("\n" + "=" * 80)
    print("📥 IMPORTADOR DE CLIENTES CSV")
    print("=" * 80)
    print("\n1. Importar arquivo CSV")
    print("2. Criar arquivo CSV de exemplo")
    print("3. Ver formato esperado do CSV")
    print("4. Sair")
    print("\n" + "-" * 80)
    
    opcao = input("\n👉 Escolha uma opção: ").strip()
    
    if opcao == "1":
        arquivo = input("\n📂 Caminho do arquivo CSV: ").strip()
        if arquivo:
            pular = input("⚠️  Pular emails duplicados? (s/n) [s]: ").strip().lower()
            pular_duplicados = pular != 'n'
            importar_csv(arquivo, pular_duplicados)
    
    elif opcao == "2":
        criar_csv_exemplo()
    
    elif opcao == "3":
        print("\n" + "=" * 80)
        print("📋 FORMATO ESPERADO DO CSV")
        print("=" * 80)
        print("\n✅ Colunas obrigatórias:")
        print("   - nome      (mínimo 3 caracteres)")
        print("   - email     (formato válido)")
        print("   - telefone  (com DDD)")
        print("   - cidade    (nome da cidade)")
        print("\n💡 Exemplo:")
        print("-" * 80)
        print("nome,email,telefone,cidade")
        print("João Silva,joao@email.com,11987654321,São Paulo")
        print("-" * 80)
        print("\n⚠️  Importante:")
        print("   - Primeira linha deve ser o cabeçalho")
        print("   - Separador pode ser vírgula (,) ou ponto-e-vírgula (;)")
        print("   - Arquivo deve estar em UTF-8")
        print("=" * 80)
    
    elif opcao == "4":
        print("\n👋 Até logo!\n")
        return False
    
    else:
        print("\n❌ Opção inválida!")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Modo linha de comando
        arquivo = sys.argv[1]
        importar_csv(arquivo)
    else:
        # Menu interativo
        while menu():
            pass
