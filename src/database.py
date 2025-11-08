#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de conexão com PostgreSQL
"""

import psycopg2
from psycopg2 import sql


class Database:
    """
    Classe para gerenciar conexão com PostgreSQL
    """
    
    def __init__(self):
        """Inicializa configurações do banco"""
        self.host = "localhost"
        self.database = "sistema_clientes"
        self.user = "postgres"
        self.password = ""  # Sem senha (configurado com trust)
        self.conexao = None
        self.cursor = None
    
    def conectar(self):
        """
        Estabelece conexão com o banco de dados
        """
        try:
            self.conexao = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conexao.cursor()
            return True
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return False
    
    def desconectar(self):
        """
        Fecha conexão com o banco de dados
        """
        if self.cursor:
            self.cursor.close()
        if self.conexao:
            self.conexao.close()
    
    def executar(self, query, parametros=None):
        """
        Executa query que modifica dados (INSERT, UPDATE, DELETE)
        
        Parâmetros:
            query (str): Query SQL a executar
            parametros (tuple): Parâmetros da query
        
        Retorna:
            list: Resultados se houver RETURNING, None caso contrário
        """
        try:
            if parametros:
                self.cursor.execute(query, parametros)
            else:
                self.cursor.execute(query)
            
            self.conexao.commit()
            
            # Se a query tem RETURNING, retornar os resultados
            if query.strip().upper().find('RETURNING') != -1:
                return self.cursor.fetchall()
            
            return None
            
        except Exception as e:
            self.conexao.rollback()
            raise e
    
    def buscar_um(self, query, parametros=None):
        """
        Executa query e retorna um único resultado
        
        Parâmetros:
            query (str): Query SQL a executar
            parametros (tuple): Parâmetros da query
        
        Retorna:
            tuple: Uma linha de resultado ou None
        """
        try:
            if parametros:
                self.cursor.execute(query, parametros)
            else:
                self.cursor.execute(query)
            
            return self.cursor.fetchone()
            
        except Exception as e:
            raise e
    
    def buscar_todos(self, query, parametros=None):
        """
        Executa query e retorna todos os resultados
        
        Parâmetros:
            query (str): Query SQL a executar
            parametros (tuple): Parâmetros da query
        
        Retorna:
            list: Lista de tuplas com os resultados
        """
        try:
            if parametros:
                self.cursor.execute(query, parametros)
            else:
                self.cursor.execute(query)
            
            return self.cursor.fetchall()
            
        except Exception as e:
            raise e


# Teste do módulo
if __name__ == "__main__":
    print("=== TESTE DE CONEXÃO ===\n")
    
    db = Database()
    
    print("1. Conectando ao banco...")
    if db.conectar():
        print("   ✅ Conexão estabelecida!")
        
        print("\n2. Testando consulta...")
        resultado = db.buscar_todos("SELECT COUNT(*) FROM clientes")
        print(f"   📊 Total de clientes: {resultado[0][0]}")
        
        print("\n3. Desconectando...")
        db.desconectar()
        print("   ✅ Desconectado!")
    else:
        print("   ❌ Falha na conexão!")
    
    print("\n=== TESTE CONCLUÍDO ===")
