#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de conexão com o banco de dados PostgreSQL
Autor: Markko1982
Data: 07/11/2025
"""

import psycopg2
from psycopg2 import Error

class Database:
    """Classe para gerenciar conexão com PostgreSQL"""
    
    def __init__(self):
        """Inicializa a classe"""
        self.connection = None
        self.cursor = None
    
    def conectar(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                database="sistema_clientes",
                user="postgres",
                password=""
            )
            self.cursor = self.connection.cursor()
            print("✅ Conexão estabelecida com sucesso!")
            return True
        except Error as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def desconectar(self):
        """Fecha conexão com o banco de dados"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("✅ Conexão fechada!")
    
    def executar_query(self, query, params=None):
        """Executa uma query SQL"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            print(f"❌ Erro ao executar query: {e}")
            self.connection.rollback()
            return False
    
    def buscar_todos(self, query, params=None):
        """Busca todos os resultados de uma query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"❌ Erro ao buscar dados: {e}")
            return []
    
    def buscar_um(self, query, params=None):
        """Busca um único resultado"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except Error as e:
            print(f"❌ Erro ao buscar dados: {e}")
            return None
