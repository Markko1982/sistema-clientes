#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de gerenciamento de produtos
Implementa operações CRUD (Create, Read, Update, Delete)
"""

from database import Database
from datetime import datetime


# ============================================================================
# FUNÇÃO 1: CADASTRAR PRODUTO
# ============================================================================

def cadastrar_produto(nome, preco, estoque, categoria, descricao=None):
    """Cadastra um novo produto no banco de dados"""
    db = Database()
    
    try:
        db.conectar()
        
        query = """
            INSERT INTO produtos (nome, descricao, preco, estoque, categoria)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        
        resultado = db.executar(query, (nome, descricao, preco, estoque, categoria))
        
        if resultado:
            produto_id = resultado[0][0]
            print(f"✅ Produto cadastrado com sucesso! ID: {produto_id}")
            return produto_id
        else:
            print("❌ Erro ao cadastrar produto")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao cadastrar produto: {e}")
        return None
    finally:
        db.desconectar()


# ============================================================================
# FUNÇÃO 2: LISTAR PRODUTOS
# ============================================================================

def listar_produtos(limite=20, offset=0, categoria=None):
    """Lista produtos com paginação e filtro opcional"""
    db = Database()
    
    try:
        db.conectar()
        
        if categoria:
            query = """
                SELECT id, nome, preco, estoque, categoria, data_cadastro
                FROM produtos
                WHERE categoria = %s
                ORDER BY nome
                LIMIT %s OFFSET %s
            """
            produtos = db.buscar_todos(query, (categoria, limite, offset))
        else:
            query = """
                SELECT id, nome, preco, estoque, categoria, data_cadastro
                FROM produtos
                ORDER BY nome
                LIMIT %s OFFSET %s
            """
            produtos = db.buscar_todos(query, (limite, offset))
        
        return produtos
        
    except Exception as e:
        print(f"❌ Erro ao listar produtos: {e}")
        return []
    finally:
        db.desconectar()


# ============================================================================
# FUNÇÃO 3: BUSCAR PRODUTO POR ID
# ============================================================================

def buscar_produto(produto_id):
    """Busca um produto específico por ID"""
    db = Database()
    
    try:
        db.conectar()
        
        query = """
            SELECT id, nome, descricao, preco, estoque, categoria, data_cadastro
            FROM produtos
            WHERE id = %s
        """
        
        produto = db.buscar_um(query, (produto_id,))
        return produto
        
    except Exception as e:
        print(f"❌ Erro ao buscar produto: {e}")
        return None
    finally:
        db.desconectar()


# ============================================================================
# FUNÇÃO 4: ATUALIZAR PRODUTO
# ============================================================================

def atualizar_produto(produto_id, nome=None, preco=None, estoque=None, categoria=None, descricao=None):
    """Atualiza dados de um produto"""
    db = Database()
    
    try:
        db.conectar()
        
        campos = []
        valores = []
        
        if nome:
            campos.append("nome = %s")
            valores.append(nome)
        if preco is not None:
            campos.append("preco = %s")
            valores.append(preco)
        if estoque is not None:
            campos.append("estoque = %s")
            valores.append(estoque)
        if categoria:
            campos.append("categoria = %s")
            valores.append(categoria)
        if descricao:
            campos.append("descricao = %s")
            valores.append(descricao)
        
        if not campos:
            print("⚠️  Nenhum campo para atualizar")
            return False
        
        valores.append(produto_id)
        query = f"UPDATE produtos SET {', '.join(campos)} WHERE id = %s"
        
        db.executar(query, tuple(valores))
        print(f"✅ Produto ID {produto_id} atualizado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar produto: {e}")
        return False
    finally:
        db.desconectar()


# ============================================================================
# FUNÇÃO 5: DELETAR PRODUTO
# ============================================================================

def deletar_produto(produto_id):
    """Deleta um produto do banco de dados"""
    db = Database()
    
    try:
        db.conectar()
        
        query = "DELETE FROM produtos WHERE id = %s"
        db.executar(query, (produto_id,))
        
        print(f"✅ Produto ID {produto_id} deletado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao deletar produto: {e}")
        return False
    finally:
        db.desconectar()


# ============================================================================
# FUNÇÃO 6: CONTAR PRODUTOS
# ============================================================================

def contar_produtos(categoria=None):
    """Conta total de produtos"""
    db = Database()
    
    try:
        db.conectar()
        
        if categoria:
            query = "SELECT COUNT(*) FROM produtos WHERE categoria = %s"
            resultado = db.buscar_um(query, (categoria,))
        else:
            query = "SELECT COUNT(*) FROM produtos"
            resultado = db.buscar_um(query)
        
        return resultado[0] if resultado else 0
        
    except Exception as e:
        print(f"❌ Erro ao contar produtos: {e}")
        return 0
    finally:
        db.desconectar()


# ============================================================================
# FUNÇÃO 7: ESTATÍSTICAS
# ============================================================================

def estatisticas_produtos():
    """Retorna estatísticas sobre produtos"""
    db = Database()
    
    try:
        db.conectar()
        
        # Total
        total = contar_produtos()
        
        # Por categoria
        query = """
            SELECT categoria, COUNT(*) as total
            FROM produtos
            GROUP BY categoria
            ORDER BY total DESC
        """
        por_categoria = db.buscar_todos(query)
        
        # Produto mais caro
        query = "SELECT nome, preco FROM produtos ORDER BY preco DESC LIMIT 1"
        mais_caro = db.buscar_um(query)
        
        # Produto mais barato
        query = "SELECT nome, preco FROM produtos ORDER BY preco ASC LIMIT 1"
        mais_barato = db.buscar_um(query)
        
        # Estoque total
        query = "SELECT SUM(estoque) FROM produtos"
        estoque_total = db.buscar_um(query)
        
        return {
            'total': total,
            'por_categoria': por_categoria,
            'mais_caro': mais_caro,
            'mais_barato': mais_barato,
            'estoque_total': estoque_total[0] if estoque_total else 0
        }
        
    except Exception as e:
        print(f"❌ Erro ao gerar estatísticas: {e}")
        return None
    finally:
        db.desconectar()


# ============================================================================
# TESTES
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DO MÓDULO PRODUTOS")
    print("=" * 60)
    
    # Teste 1: Listar produtos
    print("\n1️⃣ LISTANDO PRODUTOS:")
    produtos = listar_produtos(limite=5)
    for p in produtos:
        print(f"   {p[0]:3d}. {p[1]:30s} R$ {p[2]:8.2f} | Estoque: {p[3]:3d} | {p[4]}")
    
    # Teste 2: Estatísticas
    print("\n2️⃣ ESTATÍSTICAS:")
    stats = estatisticas_produtos()
    if stats:
        print(f"   Total de produtos: {stats['total']}")
        print(f"   Estoque total: {stats['estoque_total']} unidades")
        if stats['mais_caro']:
            print(f"   Mais caro: {stats['mais_caro'][0]} - R$ {stats['mais_caro'][1]:.2f}")
        if stats['mais_barato']:
            print(f"   Mais barato: {stats['mais_barato'][0]} - R$ {stats['mais_barato'][1]:.2f}")
        print("\n   Por categoria:")
        for cat, total in stats['por_categoria']:
            print(f"      {cat:20s}: {total:3d} produtos")
    
    print("\n" + "=" * 60)
    print("✅ TESTES CONCLUÍDOS!")
    print("=" * 60)
