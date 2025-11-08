#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar clientes fictícios realistas
Simula ambiente empresarial com ~1500 clientes
"""

import sys
import os
import random
from datetime import datetime, timedelta

# Adicionar src ao path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cliente import cadastrar_cliente, contar_clientes


# ============================================================================
# DADOS PARA GERAÇÃO REALISTA
# ============================================================================

NOMES = [
    "João", "Maria", "José", "Ana", "Pedro", "Carla", "Paulo", "Juliana",
    "Carlos", "Fernanda", "Ricardo", "Patricia", "Fernando", "Mariana",
    "Roberto", "Camila", "Marcos", "Beatriz", "Antonio", "Luciana",
    "Rafael", "Amanda", "Daniel", "Gabriela", "Rodrigo", "Renata",
    "Bruno", "Tatiana", "Felipe", "Vanessa", "Lucas", "Cristina",
    "Gustavo", "Adriana", "Eduardo", "Sandra", "Marcelo", "Daniela",
    "Thiago", "Aline", "Diego", "Claudia", "Leonardo", "Simone",
    "Vinicius", "Monica", "Fabio", "Elaine", "Alexandre", "Priscila"
]

SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira",
    "Alves", "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins",
    "Carvalho", "Rocha", "Almeida", "Nascimento", "Araujo", "Melo",
    "Barbosa", "Cardoso", "Correia", "Dias", "Fernandes", "Garcia",
    "Mendes", "Moreira", "Nunes", "Ramos", "Reis", "Teixeira", "Vieira",
    "Castro", "Campos", "Freitas", "Pinto", "Monteiro", "Lopes", "Barros"
]

CIDADES = {
    "São Paulo": {"ddd": "11", "peso": 30},
    "Rio de Janeiro": {"ddd": "21", "peso": 18},
    "Belo Horizonte": {"ddd": "31", "peso": 10},
    "Curitiba": {"ddd": "41", "peso": 8},
    "Porto Alegre": {"ddd": "51", "peso": 7},
    "Salvador": {"ddd": "71", "peso": 6},
    "Brasília": {"ddd": "61", "peso": 5},
    "Fortaleza": {"ddd": "85", "peso": 4},
    "Recife": {"ddd": "81", "peso": 4},
    "Manaus": {"ddd": "92", "peso": 3},
    "Campinas": {"ddd": "19", "peso": 2},
    "Goiânia": {"ddd": "62", "peso": 2},
    "Florianópolis": {"ddd": "48", "peso": 1}
}

DOMINIOS_EMAIL = [
    "gmail.com", "hotmail.com", "outlook.com", "yahoo.com.br",
    "empresa.com.br", "techdata.com.br", "solutions.com.br",
    "consulting.com.br", "corp.com.br", "business.com.br"
]


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def gerar_nome_completo():
    """Gera um nome completo realista"""
    nome = random.choice(NOMES)
    sobrenome1 = random.choice(SOBRENOMES)
    sobrenome2 = random.choice(SOBRENOMES)
    
    # 70% chance de ter dois sobrenomes
    if random.random() < 0.7:
        return f"{nome} {sobrenome1} {sobrenome2}"
    else:
        return f"{nome} {sobrenome1}"


def gerar_email(nome):
    """Gera um email baseado no nome"""
    # Remover acentos e converter para minúsculas
    nome_limpo = nome.lower()
    nome_limpo = nome_limpo.replace(" ", ".")
    
    # Remover acentos manualmente
    acentos = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e',
        'í': 'i',
        'ó': 'o', 'õ': 'o', 'ô': 'o',
        'ú': 'u', 'ü': 'u',
        'ç': 'c'
    }
    for acento, letra in acentos.items():
        nome_limpo = nome_limpo.replace(acento, letra)
    
    dominio = random.choice(DOMINIOS_EMAIL)
    
    # 20% chance de adicionar número
    if random.random() < 0.2:
        numero = random.randint(1, 999)
        return f"{nome_limpo}{numero}@{dominio}"
    else:
        return f"{nome_limpo}@{dominio}"


def gerar_telefone(ddd):
    """Gera um telefone celular realista"""
    # Celular começa com 9
    numero = f"9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    return f"({ddd}) {numero}"


def escolher_cidade():
    """Escolhe uma cidade baseado na distribuição de peso"""
    cidades = list(CIDADES.keys())
    pesos = [CIDADES[c]["peso"] for c in cidades]
    return random.choices(cidades, weights=pesos, k=1)[0]


def gerar_data_cadastro():
    """Gera uma data de cadastro nos últimos 2 anos"""
    hoje = datetime.now()
    dias_atras = random.randint(0, 730)  # 2 anos = 730 dias
    data = hoje - timedelta(days=dias_atras)
    return data


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def gerar_clientes(quantidade=1500):
    """
    Gera quantidade especificada de clientes fictícios
    
    Parâmetros:
        quantidade (int): Número de clientes a gerar
    """
    print("=" * 70)
    print(f"GERADOR DE CLIENTES FICTÍCIOS")
    print("=" * 70)
    print(f"\n🎯 Meta: Gerar {quantidade} clientes realistas")
    print(f"📊 Distribuição geográfica: {len(CIDADES)} cidades brasileiras")
    print(f"📅 Período: Últimos 2 anos\n")
    
    # Verificar quantos clientes já existem
    total_atual = contar_clientes()
    print(f"📋 Clientes atuais no banco: {total_atual}\n")
    
    if total_atual > 0:
        resposta = input("⚠️  Já existem clientes no banco. Continuar? (s/n): ")
        if resposta.lower() != 's':
            print("❌ Operação cancelada!")
            return
    
    print("\n🚀 Iniciando geração...\n")
    
    sucesso = 0
    erro = 0
    emails_usados = set()
    
    for i in range(quantidade):
        try:
            # Gerar dados
            nome = gerar_nome_completo()
            cidade = escolher_cidade()
            ddd = CIDADES[cidade]["ddd"]
            telefone = gerar_telefone(ddd)
            
            # Gerar email único
            tentativas = 0
            while tentativas < 10:
                email = gerar_email(nome)
                if email not in emails_usados:
                    emails_usados.add(email)
                    break
                tentativas += 1
            
            # Cadastrar cliente
            id_cliente = cadastrar_cliente(nome, email, telefone, cidade)
            
            if id_cliente:
                sucesso += 1
                
                # Mostrar progresso a cada 100 clientes
                if (sucesso % 100) == 0:
                    print(f"   ✅ {sucesso} clientes cadastrados...")
            else:
                erro += 1
        
        except Exception as e:
            erro += 1
            if erro <= 5:  # Mostrar só os primeiros 5 erros
                print(f"   ❌ Erro ao cadastrar: {e}")
    
    # Resumo final
    print("\n" + "=" * 70)
    print("RESUMO DA GERAÇÃO")
    print("=" * 70)
    print(f"✅ Clientes cadastrados com sucesso: {sucesso}")
    print(f"❌ Erros: {erro}")
    print(f"📊 Total no banco: {contar_clientes()}")
    print("=" * 70)
    
    # Estatísticas por cidade
    print("\n📍 DISTRIBUIÇÃO POR CIDADE:")
    print("-" * 70)
    from cliente import estatisticas
    stats = estatisticas()
    if stats and stats['cidades']:
        for cidade, total in stats['cidades']:
            percentual = (total / sucesso) * 100
            print(f"   {cidade:20s}: {total:4d} clientes ({percentual:5.1f}%)")
    
    print("\n✅ Geração concluída!")


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    # Verificar se foi passado argumento
    if len(sys.argv) > 1:
        try:
            quantidade = int(sys.argv[1])
        except:
            print("❌ Quantidade inválida! Use: python gerar_clientes.py 1500")
            sys.exit(1)
    else:
        quantidade = 1500
    
    gerar_clientes(quantidade)
