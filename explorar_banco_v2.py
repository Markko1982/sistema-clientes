#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script AVANÇADO para explorar banco de dados
Versão 2.0 - Com mais recursos!
"""

import psycopg2
from datetime import datetime

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

def listar_tabelas():
    """Lista todas as tabelas do banco"""
    conn = conectar()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        
        query = """
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename
        """
        cursor.execute(query)
        tabelas = cursor.fetchall()
        
        print("=" * 80)
        print("📊 BANCO DE DADOS: sistema_clientes")
        print("=" * 80)
        print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"✅ Total de tabelas: {len(tabelas)}\n")
        
        for i, (tabela,) in enumerate(tabelas, 1):
            print(f"   {i}. {tabela}")
        
        print("=" * 80)
        
        cursor.close()
        return [t[0] for t in tabelas]
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return []
    finally:
        conn.close()

def descrever_tabela(nome_tabela):
    """Mostra estrutura completa de uma tabela"""
    conn = conectar()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Buscar colunas
        query = """
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' 
            AND table_name = %s
            ORDER BY ordinal_position
        """
        cursor.execute(query, (nome_tabela,))
        colunas = cursor.fetchall()
        
        # Contar registros
        cursor.execute(f"SELECT COUNT(*) FROM {nome_tabela}")
        total = cursor.fetchone()[0]
        
        # Buscar chaves primárias
        query_pk = """
            SELECT a.attname
            FROM pg_index i
            JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
            WHERE i.indrelid = %s::regclass AND i.indisprimary
        """
        cursor.execute(query_pk, (nome_tabela,))
        pks = [row[0] for row in cursor.fetchall()]
        
        # Buscar índices
        query_idx = """
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE tablename = %s AND schemaname = 'public'
        """
        cursor.execute(query_idx, (nome_tabela,))
        indices = cursor.fetchall()
        
        print("\n" + "=" * 80)
        print(f"📋 TABELA: {nome_tabela}")
        print("=" * 80)
        print(f"📊 Total de registros: {total:,}".replace(',', '.'))
        print(f"🔑 Chave primária: {', '.join(pks) if pks else 'Nenhuma'}")
        print(f"📇 Índices: {len(indices)}")
        
        print("\n" + "-" * 80)
        print(f"{'COLUNA':<25} {'TIPO':<25} {'NULO?':<8} {'PADRÃO':<20}")
        print("-" * 80)
        
        for col in colunas:
            nome = col[0]
            tipo = col[1]
            tamanho = col[2]
            nulo = "SIM" if col[3] == "YES" else "NÃO"
            padrao = str(col[4])[:20] if col[4] else "-"
            
            if tamanho:
                tipo = f"{tipo}({tamanho})"
            
            # Destacar chave primária
            if nome in pks:
                nome = f"🔑 {nome}"
            
            print(f"{nome:<25} {tipo:<25} {nulo:<8} {padrao:<20}")
        
        print("-" * 80)
        
        # Mostrar primeiros registros
        cursor.execute(f"SELECT * FROM {nome_tabela} LIMIT 3")
        registros = cursor.fetchall()
        
        if registros:
            print(f"\n📄 Primeiros {len(registros)} registros:")
            print("-" * 80)
            for i, reg in enumerate(registros, 1):
                print(f"\n   Registro {i}:")
                for j, col in enumerate(colunas):
                    nome_col = col[0]
                    valor = reg[j]
                    if isinstance(valor, str) and len(valor) > 50:
                        valor = valor[:50] + "..."
                    print(f"      {nome_col}: {valor}")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        conn.close()

def estatisticas_banco():
    """Mostra estatísticas gerais do banco"""
    conn = conectar()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        print("\n" + "=" * 80)
        print("📈 ESTATÍSTICAS DO BANCO")
        print("=" * 80)
        
        # Total de registros por tabela
        query = """
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public'
        """
        cursor.execute(query)
        tabelas = cursor.fetchall()
        
        total_geral = 0
        print("\n📊 Registros por tabela:\n")
        
        for (tabela,) in tabelas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
            count = cursor.fetchone()[0]
            total_geral += count
            print(f"   {tabela:<20} {count:>10,} registros".replace(',', '.'))
        
        print(f"\n   {'TOTAL':<20} {total_geral:>10,} registros".replace(',', '.'))
        
        # Tamanho do banco
        query = """
            SELECT pg_size_pretty(pg_database_size('sistema_clientes'))
        """
        cursor.execute(query)
        tamanho = cursor.fetchone()[0]
        print(f"\n💾 Tamanho do banco: {tamanho}")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        conn.close()

def menu():
    """Menu interativo"""
    while True:
        print("\n" + "=" * 80)
        print("🔍 EXPLORADOR DE BANCO DE DADOS")
        print("=" * 80)
        print("\n1. Listar todas as tabelas")
        print("2. Descrever tabela específica")
        print("3. Explorar tudo (completo)")
        print("4. Ver estatísticas")
        print("5. Sair")
        print("\n" + "-" * 80)
        
        opcao = input("\n👉 Escolha uma opção: ").strip()
        
        if opcao == "1":
            listar_tabelas()
        
        elif opcao == "2":
            tabela = input("\n📋 Nome da tabela: ").strip()
            if tabela:
                descrever_tabela(tabela)
        
        elif opcao == "3":
            tabelas = listar_tabelas()
            for tabela in tabelas:
                descrever_tabela(tabela)
            estatisticas_banco()
        
        elif opcao == "4":
            estatisticas_banco()
        
        elif opcao == "5":
            print("\n👋 Até logo!\n")
            break
        
        else:
            print("\n❌ Opção inválida!")

if __name__ == "__main__":
    menu()
