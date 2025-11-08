#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de teste de conexão com o banco de dados
"""

from database import Database

def main():
    print("=" * 60)
    print("🧪 TESTE DE CONEXÃO COM POSTGRESQL")
    print("=" * 60)
    print()
    
    # Criar instância do banco
    db = Database()
    
    # Testar conexão
    print("🔌 Tentando conectar ao banco de dados...")
    if db.conectar():
        print()
        
        # Verificar se a tabela existe
        print("🔍 Verificando tabela 'clientes'...")
        resultado = db.buscar_um("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_name = 'clientes'
        """)
        
        if resultado and resultado[0] == 1:
            print("✅ Tabela 'clientes' encontrada!")
            print()
            
            # Contar registros
            print("📊 Contando registros...")
            resultado = db.buscar_um("SELECT COUNT(*) FROM clientes")
            total = resultado[0] if resultado else 0
            print(f"📈 Total de clientes cadastrados: {total}")
        else:
            print("❌ Tabela 'clientes' não encontrada!")
        
        print()
        # Desconectar
        db.desconectar()
    else:
        print("❌ Falha na conexão!")
    
    print()
    print("=" * 60)
    print("✅ Teste concluído!")
    print("=" * 60)

if __name__ == "__main__":
    main()
