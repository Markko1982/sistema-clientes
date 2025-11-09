#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar novos clientes ao banco de dados
Versão interativa com validação
"""

import psycopg2
import re
from datetime import datetime

def validar_email(email):
    """Valida formato de email"""
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

def validar_telefone(telefone):
    """Valida formato de telefone"""
    numeros = re.sub(r'\D', '', telefone)
    return len(numeros) in [10, 11]

def formatar_telefone(telefone):
    """Formata telefone para padrão (XX) XXXXX-XXXX"""
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

def adicionar_cliente(nome, email, telefone, cidade):
    """Adiciona um novo cliente ao banco"""
    conn = conectar()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        query = """
            INSERT INTO clientes (nome, email, telefone, cidade)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """
        
        cursor.execute(query, (nome, email, telefone, cidade))
        cliente_id = cursor.fetchone()[0]
        
        conn.commit()
        
        print("\n" + "=" * 70)
        print("✅ CLIENTE CADASTRADO COM SUCESSO!")
        print("=" * 70)
        print(f"\n📋 ID: {cliente_id}")
        print(f"👤 Nome: {nome}")
        print(f"📧 Email: {email}")
        print(f"📱 Telefone: {telefone}")
        print(f"🏙️  Cidade: {cidade}")
        print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("\n" + "=" * 70)
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao adicionar cliente: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def menu_interativo():
    """Menu interativo para adicionar cliente"""
    print("\n" + "=" * 70)
    print("➕ ADICIONAR NOVO CLIENTE")
    print("=" * 70)
    
    while True:
        nome = input("\n👤 Nome completo: ").strip()
        if nome and len(nome) >= 3:
            break
        print("⚠️  Nome deve ter pelo menos 3 caracteres!")
    
    while True:
        email = input("📧 Email: ").strip()
        if email and validar_email(email):
            break
        print("⚠️  Email inválido! Use o formato: exemplo@dominio.com")
    
    while True:
        telefone = input("📱 Telefone (com DDD): ").strip()
        if telefone and validar_telefone(telefone):
            telefone = formatar_telefone(telefone)
            break
        print("⚠️  Telefone inválido! Use o formato: (11) 98765-4321")
    
    while True:
        cidade = input("��️  Cidade: ").strip()
        if cidade and len(cidade) >= 3:
            break
        print("⚠️  Cidade deve ter pelo menos 3 caracteres!")
    
    print("\n" + "-" * 70)
    print("📋 CONFIRME OS DADOS:")
    print("-" * 70)
    print(f"👤 Nome: {nome}")
    print(f"📧 Email: {email}")
    print(f"📱 Telefone: {telefone}")
    print(f"🏙️  Cidade: {cidade}")
    print("-" * 70)
    
    confirma = input("\n✅ Confirma o cadastro? (s/n): ").strip().lower()
    
    if confirma == 's':
        adicionar_cliente(nome, email, telefone, cidade)
    else:
        print("\n❌ Cadastro cancelado!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 5:
        nome = sys.argv[1]
        email = sys.argv[2]
        telefone = sys.argv[3]
        cidade = sys.argv[4]
        adicionar_cliente(nome, email, telefone, cidade)
    else:
        menu_interativo()
