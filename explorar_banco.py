#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para explorar o banco de dados
Mostra todas as tabelas e suas estruturas
"""

import psycopg2
from psycopg2 import sql

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
        return
    
    try:
        cursor = conn.cursor()
        
        # Buscar tabelas
        query = """
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename
        """
        cursor.execute(query)
        tabelas = cursor.fetchall()
        
        print("=" * 70)
        print("📊 TABELAS NO BANCO 'sistema_clientes'")
        print("=" * 70)
        print(f"\n✅ Total de tabelas: {len(tabelas)}\n")
        
        for i, (tabela,) in enumerate(tabelas, 1):
            print(f"{i}. {tabela}")
        
        print("\n" + "=" * 70)
        
        cursor.close()
        return [t[0] for t in tabelas]
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return []
    finally:
        conn.close()

def descrever_tabela(nome_tabela):
    """Mostra estrutura de uma tabela"""
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
        
        print("\n" + "=" * 70)
        print(f"📋 ESTRUTURA DA TABELA: {nome_tabela}")
        print("=" * 70)
        print(f"📊 Total de registros: {total}")
        print("\n" + "-" * 70)
        print(f"{'COLUNA':<25} {'TIPO':<20} {'NULO?':<8} {'PADRÃO':<15}")
        print("-" * 70)
        
        for col in colunas:
            nome = col[0]
            tipo = col[1]
            tamanho = col[2]
            nulo = "SIM" if col[3] == "YES" else "NÃO"
            padrao = str(col[4])[:15] if col[4] else "-"
            
            if tamanho:
                tipo = f"{tipo}({tamanho})"
            
            print(f"{nome:<25} {tipo:<20} {nulo:<8} {padrao:<15}")
        
        print("-" * 70)
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        conn.close()

def explorar_tudo():
    """Explora o banco completo"""
    tabelas = listar_tabelas()
    
    if tabelas:
        print("\n" + "=" * 70)
        print("🔍 DETALHES DE CADA TABELA")
        print("=" * 70)
        
        for tabela in tabelas:
            descrever_tabela(tabela)
        
        print("\n" + "=" * 70)
        print("✅ EXPLORAÇÃO CONCLUÍDA!")
        print("=" * 70)

if __name__ == "__main__":
    explorar_tudo()
