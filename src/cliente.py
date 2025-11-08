#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de gerenciamento de clientes
Implementa operações CRUD (Create, Read, Update, Delete)
"""

from database import Database
from datetime import datetime


# ============================================================================
# FUNÇÃO 1: CADASTRAR CLIENTE
# ============================================================================
def cadastrar_cliente(nome, email, telefone, cidade):
    """
    Cadastra um novo cliente no banco de dados
    
    Parâmetros:
        nome (str): Nome completo do cliente
        email (str): Email do cliente (deve ser único)
        telefone (str): Telefone do cliente
        cidade (str): Cidade do cliente
    
    Retorna:
        int: ID do cliente cadastrado ou None se houver erro
    """
    db = Database()
    
    try:
        db.conectar()
        
        # Query SQL para inserir novo cliente
        # RETURNING id retorna o ID do cliente inserido
        query = """
            INSERT INTO clientes (nome, email, telefone, cidade)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """
        
        # Executar query com os dados
        resultado = db.executar(query, (nome, email, telefone, cidade))
        
        # Pegar o ID retornado
        if resultado:
            cliente_id = resultado[0][0]
            print(f"✅ Cliente cadastrado com sucesso! ID: {cliente_id}")
            return cliente_id
        
    except Exception as e:
        print(f"❌ Erro ao cadastrar cliente: {e}")
        return None
    
    finally:
        db.desconectar()


# ============================================================================
# FUNÇÃO 2: LISTAR CLIENTES
# ============================================================================
def listar_clientes(limite=None, offset=0, cidade=None):
    """
    Lista clientes do banco de dados
    
    Parâmetros:
        limite (int): Número máximo de clientes a retornar (para paginação)
        offset (int): Número de registros a pular (para paginação)
        cidade (str): Filtrar por cidade (opcional)
    
    Retorna:
        list: Lista de tuplas com dados dos clientes
    """
    db = Database()
    
    try:
        db.conectar()
        
        # Construir query base
        query = "SELECT id, nome, email, telefone, cidade, data_cadastro FROM clientes"
        parametros = []
        
        # Adicionar filtro de cidade se fornecido
        if cidade:
            query += " WHERE cidade = %s"
            parametros.append(cidade)
        
        # Ordenar por data de cadastro (mais recentes primeiro)
        query += " ORDER BY data_cadastro DESC"
        
        # Adicionar paginação se fornecido
        if limite:
            query += " LIMIT %s OFFSET %s"
            parametros.extend([limite, offset])
        
        # Executar query
        clientes = db.buscar_todos(query, tuple(parametros) if parametros else None)
        
        return clientes
    
    except Exception as e:
        print(f"❌ Erro ao listar clientes: {e}")
        return []
    
    finally:
        db.desconectar()


# ============================================================================
# FUNÇÃO 3: BUSCAR CLIENTE POR ID
# ============================================================================
def buscar_cliente(cliente_id):
    """
    Busca um cliente específico por ID
    
    Parâmetros:
        cliente_id (int): ID do cliente
    
    Retorna:
        tuple: Dados do cliente ou None se não encontrado
    """
    db = Database()
    
    try:
        db.conectar()
        
        query = """
            SELECT id, nome, email, telefone, cidade, data_cadastro
            FROM clientes
            WHERE id = %s
        """
        
        cliente = db.buscar_um(query, (cliente_id,))
        
        return cliente
    
    except Exception as e:
        print(f"❌ Erro ao buscar cliente: {e}")
        return None
    
    finally:
        db.desconectar()


# ============================================================================
# FUNÇÃO 4: BUSCAR CLIENTES POR NOME (BUSCA PARCIAL)
# ============================================================================
def buscar_por_nome(nome):
    """
    Busca clientes por nome (busca parcial com LIKE)
    
    Parâmetros:
        nome (str): Nome ou parte do nome a buscar
    
    Retorna:
        list: Lista de clientes encontrados
    """
    db = Database()
    
    try:
        db.conectar()
        
        # ILIKE é case-insensitive (não diferencia maiúsculas/minúsculas)
        # %nome% busca em qualquer parte do nome
        query = """
            SELECT id, nome, email, telefone, cidade, data_cadastro
            FROM clientes
            WHERE nome ILIKE %s
            ORDER BY nome
        """
        
        # Adicionar % para busca parcial
        padrao = f"%{nome}%"
        
        clientes = db.buscar_todos(query, (padrao,))
        
        return clientes
    
    except Exception as e:
        print(f"❌ Erro ao buscar por nome: {e}")
        return []
    
    finally:
        db.desconectar()


# ============================================================================
# FUNÇÃO 5: ATUALIZAR CLIENTE
# ============================================================================
def atualizar_cliente(cliente_id, nome=None, email=None, telefone=None, cidade=None):
    """
    Atualiza dados de um cliente existente
    
    Parâmetros:
        cliente_id (int): ID do cliente a atualizar
        nome (str): Novo nome (opcional)
        email (str): Novo email (opcional)
        telefone (str): Novo telefone (opcional)
        cidade (str): Nova cidade (opcional)
    
    Retorna:
        bool: True se atualizado com sucesso, False caso contrário
    """
    db = Database()
    
    try:
        db.conectar()
        
        # Construir query dinamicamente baseado nos campos fornecidos
        campos = []
        valores = []
        
        if nome:
            campos.append("nome = %s")
            valores.append(nome)
        
        if email:
            campos.append("email = %s")
            valores.append(email)
        
        if telefone:
            campos.append("telefone = %s")
            valores.append(telefone)
        
        if cidade:
            campos.append("cidade = %s")
            valores.append(cidade)
        
        # Se nenhum campo foi fornecido, não há nada para atualizar
        if not campos:
            print("⚠️ Nenhum campo fornecido para atualização")
            return False
        
        # Adicionar ID no final dos valores
        valores.append(cliente_id)
        
        # Construir query
        query = f"UPDATE clientes SET {', '.join(campos)} WHERE id = %s"
        
        # Executar atualização
        db.executar(query, tuple(valores))
        
        print(f"✅ Cliente {cliente_id} atualizado com sucesso!")
        return True
    
    except Exception as e:
        print(f"❌ Erro ao atualizar cliente: {e}")
        return False
    
    finally:
        db.desconectar()


# ============================================================================
# FUNÇÃO 6: DELETAR CLIENTE
# ============================================================================
def deletar_cliente(cliente_id):
    """
    Remove um cliente do banco de dados
    
    Parâmetros:
        cliente_id (int): ID do cliente a deletar
    
    Retorna:
        bool: True se deletado com sucesso, False caso contrário
    """
    db = Database()
    
    try:
        db.conectar()
        
        # Primeiro verificar se o cliente existe
        cliente = buscar_cliente(cliente_id)
        
        if not cliente:
            print(f"⚠️ Cliente {cliente_id} não encontrado")
            return False
        
        # Deletar cliente
        query = "DELETE FROM clientes WHERE id = %s"
        db.executar(query, (cliente_id,))
        
        print(f"✅ Cliente {cliente_id} deletado com sucesso!")
        return True
    
    except Exception as e:
        print(f"❌ Erro ao deletar cliente: {e}")
        return False
    
    finally:
        db.desconectar()


# ============================================================================
# FUNÇÃO 7: CONTAR CLIENTES
# ============================================================================
def contar_clientes(cidade=None):
    """
    Conta o número total de clientes
    
    Parâmetros:
        cidade (str): Filtrar por cidade (opcional)
    
    Retorna:
        int: Número de clientes
    """
    db = Database()
    
    try:
        db.conectar()
        
        if cidade:
            query = "SELECT COUNT(*) FROM clientes WHERE cidade = %s"
            resultado = db.buscar_um(query, (cidade,))
        else:
            query = "SELECT COUNT(*) FROM clientes"
            resultado = db.buscar_um(query)
        
        return resultado[0] if resultado else 0
    
    except Exception as e:
        print(f"❌ Erro ao contar clientes: {e}")
        return 0
    
    finally:
        db.desconectar()


# ============================================================================
# FUNÇÃO 8: ESTATÍSTICAS
# ============================================================================
def estatisticas():
    """
    Retorna estatísticas gerais sobre os clientes
    
    Retorna:
        dict: Dicionário com estatísticas
    """
    db = Database()
    
    try:
        db.conectar()
        
        # Total de clientes
        total = contar_clientes()
        
        # Clientes por cidade (top 10)
        query_cidades = """
            SELECT cidade, COUNT(*) as total
            FROM clientes
            GROUP BY cidade
            ORDER BY total DESC
            LIMIT 10
        """
        cidades = db.buscar_todos(query_cidades)
        
        # Cliente mais recente
        query_recente = """
            SELECT nome, data_cadastro
            FROM clientes
            ORDER BY data_cadastro DESC
            LIMIT 1
        """
        recente = db.buscar_um(query_recente)
        
        return {
            'total': total,
            'cidades': cidades,
            'mais_recente': recente
        }
    
    except Exception as e:
        print(f"❌ Erro ao gerar estatísticas: {e}")
        return None
    
    finally:
        db.desconectar()


# ============================================================================
# TESTE DO MÓDULO (executado apenas se rodar este arquivo diretamente)
# ============================================================================
if __name__ == "__main__":
    print("=== TESTE DO MÓDULO CLIENTE ===\n")
    
    # Teste 1: Cadastrar cliente
    print("1. Testando cadastro...")
    cliente_id = cadastrar_cliente(
        nome="João da Silva",
        email="joao.silva@teste.com",
        telefone="(11) 98765-4321",
        cidade="São Paulo"
    )
    
    # Teste 2: Listar clientes
    print("\n2. Testando listagem...")
    clientes = listar_clientes(limite=5)
    print(f"Encontrados {len(clientes)} clientes")
    
    # Teste 3: Buscar por ID
    if cliente_id:
        print(f"\n3. Testando busca por ID ({cliente_id})...")
        cliente = buscar_cliente(cliente_id)
        if cliente:
            print(f"Cliente encontrado: {cliente[1]}")
    
    # Teste 4: Estatísticas
    print("\n4. Testando estatísticas...")
    stats = estatisticas()
    if stats:
        print(f"Total de clientes: {stats['total']}")
    
    print("\n=== TESTES CONCLUÍDOS ===")
