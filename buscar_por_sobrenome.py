#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buscar clientes por sobrenome
"""

import psycopg2
import sys

def buscar_por_sobrenome(sobrenome):
    try:
        # Conectar
        conn = psycopg2.connect(
            host="localhost",
            database="sistema_clientes",
            user="postgres",
            password="postgres"
        )
        cursor = conn.cursor()
        
        # Buscar (SEM a coluna estado que não existe)
        query = """
            SELECT id, nome, email, telefone, cidade
            FROM clientes
            WHERE nome ILIKE %s
            ORDER BY nome
        """
        
        padrao = f'%{sobrenome}%'
        cursor.execute(query, (padrao,))
        resultados = cursor.fetchall()
        
        print("=" * 90)
        print(f"🔍 CLIENTES COM SOBRENOME '{sobrenome.upper()}'")
        print("=" * 90)
        print(f"\n✅ Total encontrado: {len(resultados)}\n")
        
        if resultados:
            print("-" * 90)
            print(f"{'ID':<5} {'NOME':<35} {'EMAIL':<30} {'CIDADE':<15}")
            print("-" * 90)
            
            for cliente in resultados:
                id_cliente = cliente[0]
                nome = cliente[1][:35]
                email = cliente[2][:30] if cliente[2] else "-"
                cidade = cliente[4][:15] if cliente[4] else "-"
                
                print(f"{id_cliente:<5} {nome:<35} {email:<30} {cidade:<15}")
            
            print("-" * 90)
            print(f"\n📊 Total: {len(resultados)} cliente(s) encontrado(s)")
            print("=" * 90)
        else:
            print(f"❌ Nenhum cliente encontrado com sobrenome '{sobrenome}'")
            print("=" * 90)
        
        cursor.close()
        conn.close()
        
        return resultados
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return []

def menu():
    """Menu interativo"""
    while True:
        print("\n" + "=" * 90)
        print("🔍 BUSCAR CLIENTES POR SOBRENOME")
        print("=" * 90)
        
        sobrenome = input("\n👉 Digite o sobrenome (ou 'sair' para sair): ").strip()
        
        if sobrenome.lower() == 'sair':
            print("\n👋 Até logo!\n")
            break
        
        if sobrenome:
            buscar_por_sobrenome(sobrenome)
        else:
            print("\n⚠️  Digite um sobrenome válido!")

if __name__ == "__main__":
    # Se passou argumento na linha de comando
    if len(sys.argv) > 1:
        sobrenome = sys.argv[1]
        buscar_por_sobrenome(sobrenome)
    else:
        # Menu interativo
        menu()
