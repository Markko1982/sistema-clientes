#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de gerenciamento de vendas
CRUD completo para vendas
"""

import psycopg2
from datetime import datetime
from database import Database

# Instância do banco
db = Database()

def registrar_venda(cliente_id, produto_id, quantidade, observacao=None):
    """
    Registra uma nova venda
    
    Args:
        cliente_id: ID do cliente
        produto_id: ID do produto
        quantidade: Quantidade vendida
        observacao: Observação opcional
    
    Returns:
        ID da venda criada ou None em caso de erro
    """
    conn = db.conectar()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Buscar preço atual do produto
        cursor.execute("SELECT preco, estoque FROM produtos WHERE id = %s", (produto_id,))
        resultado = cursor.fetchone()
        
        if not resultado:
            print(f"❌ Produto ID {produto_id} não encontrado!")
            return None
        
        preco, estoque = resultado
        
        # Verificar estoque
        if estoque < quantidade:
            print(f"❌ Estoque insuficiente! Disponível: {estoque}, Solicitado: {quantidade}")
            return None
        
        valor_unitario = preco
        valor_total = quantidade * valor_unitario
        
        # Inserir venda
        query = """
            INSERT INTO vendas (cliente_id, produto_id, quantidade, valor_unitario, valor_total, observacao)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        
        cursor.execute(query, (cliente_id, produto_id, quantidade, valor_unitario, valor_total, observacao))
        venda_id = cursor.fetchone()[0]
        
        # Atualizar estoque do produto
        cursor.execute(
            "UPDATE produtos SET estoque = estoque - %s WHERE id = %s",
            (quantidade, produto_id)
        )
        
        conn.commit()
        
        print("\n" + "=" * 80)
        print("✅ VENDA REGISTRADA COM SUCESSO!")
        print("=" * 80)
        print(f"\n📋 ID da Venda: {venda_id}")
        print(f"💰 Valor Total: R$ {valor_total:.2f}")
        print(f"📦 Estoque Atualizado: {estoque - quantidade} unidades")
        print("\n" + "=" * 80)
        
        cursor.close()
        conn.close()
        
        return venda_id
        
    except Exception as e:
        print(f"\n❌ Erro ao registrar venda: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return None

def listar_vendas(limite=50):
    """
    Lista todas as vendas com informações de cliente e produto
    
    Args:
        limite: Número máximo de vendas a retornar
    
    Returns:
        Lista de tuplas com dados das vendas
    """
    conn = db.conectar()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        
        query = """
            SELECT 
                v.id,
                c.nome as cliente,
                p.nome as produto,
                v.quantidade,
                v.valor_unitario,
                v.valor_total,
                v.data_venda,
                v.observacao
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN produtos p ON v.produto_id = p.id
            ORDER BY v.data_venda DESC
            LIMIT %s
        """
        
        cursor.execute(query, (limite,))
        vendas = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return vendas
        
    except Exception as e:
        print(f"\n❌ Erro ao listar vendas: {e}")
        if conn:
            conn.close()
        return []

def buscar_venda(venda_id):
    """
    Busca uma venda específica por ID
    
    Args:
        venda_id: ID da venda
    
    Returns:
        Tupla com dados da venda ou None
    """
    conn = db.conectar()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        query = """
            SELECT 
                v.id,
                v.cliente_id,
                c.nome as cliente,
                v.produto_id,
                p.nome as produto,
                v.quantidade,
                v.valor_unitario,
                v.valor_total,
                v.data_venda,
                v.observacao
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN produtos p ON v.produto_id = p.id
            WHERE v.id = %s
        """
        
        cursor.execute(query, (venda_id,))
        venda = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return venda
        
    except Exception as e:
        print(f"\n❌ Erro ao buscar venda: {e}")
        if conn:
            conn.close()
        return None

def vendas_por_cliente(cliente_id):
    """
    Lista todas as vendas de um cliente específico
    
    Args:
        cliente_id: ID do cliente
    
    Returns:
        Lista de tuplas com vendas do cliente
    """
    conn = db.conectar()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        
        query = """
            SELECT 
                v.id,
                p.nome as produto,
                v.quantidade,
                v.valor_total,
                v.data_venda
            FROM vendas v
            JOIN produtos p ON v.produto_id = p.id
            WHERE v.cliente_id = %s
            ORDER BY v.data_venda DESC
        """
        
        cursor.execute(query, (cliente_id,))
        vendas = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return vendas
        
    except Exception as e:
        print(f"\n❌ Erro ao buscar vendas do cliente: {e}")
        if conn:
            conn.close()
        return []

def vendas_por_produto(produto_id):
    """
    Lista todas as vendas de um produto específico
    
    Args:
        produto_id: ID do produto
    
    Returns:
        Lista de tuplas com vendas do produto
    """
    conn = db.conectar()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        
        query = """
            SELECT 
                v.id,
                c.nome as cliente,
                v.quantidade,
                v.valor_total,
                v.data_venda
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            WHERE v.produto_id = %s
            ORDER BY v.data_venda DESC
        """
        
        cursor.execute(query, (produto_id,))
        vendas = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return vendas
        
    except Exception as e:
        print(f"\n❌ Erro ao buscar vendas do produto: {e}")
        if conn:
            conn.close()
        return []

def cancelar_venda(venda_id):
    """
    Cancela uma venda e devolve o estoque
    
    Args:
        venda_id: ID da venda a ser cancelada
    
    Returns:
        True se cancelada com sucesso, False caso contrário
    """
    conn = db.conectar()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Buscar dados da venda
        cursor.execute(
            "SELECT produto_id, quantidade FROM vendas WHERE id = %s",
            (venda_id,)
        )
        resultado = cursor.fetchone()
        
        if not resultado:
            print(f"❌ Venda ID {venda_id} não encontrada!")
            return False
        
        produto_id, quantidade = resultado
        
        # Deletar venda
        cursor.execute("DELETE FROM vendas WHERE id = %s", (venda_id,))
        
        # Devolver estoque
        cursor.execute(
            "UPDATE produtos SET estoque = estoque + %s WHERE id = %s",
            (quantidade, produto_id)
        )
        
        conn.commit()
        
        print(f"\n✅ Venda ID {venda_id} cancelada com sucesso!")
        print(f"📦 Estoque devolvido: {quantidade} unidades")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao cancelar venda: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def estatisticas_vendas():
    """
    Retorna estatísticas gerais de vendas
    
    Returns:
        Dicionário com estatísticas
    """
    conn = db.conectar()
    if not conn:
        return {}
    
    try:
        cursor = conn.cursor()
        
        stats = {}
        
        # Total de vendas e faturamento
        cursor.execute("""
            SELECT 
                COUNT(*) as total_vendas,
                COALESCE(SUM(valor_total), 0) as total_faturado,
                COALESCE(AVG(valor_total), 0) as ticket_medio
            FROM vendas
        """)
        
        resultado = cursor.fetchone()
        stats['total_vendas'] = resultado[0]
        stats['total_faturado'] = float(resultado[1])
        stats['ticket_medio'] = float(resultado[2])
        
        # Top 5 produtos mais vendidos
        cursor.execute("""
            SELECT 
                p.nome,
                SUM(v.quantidade) as total_vendido
            FROM vendas v
            JOIN produtos p ON v.produto_id = p.id
            GROUP BY p.nome
            ORDER BY total_vendido DESC
            LIMIT 5
        """)
        stats['top_produtos'] = cursor.fetchall()
        
        # Top 5 clientes que mais compraram
        cursor.execute("""
            SELECT 
                c.nome,
                SUM(v.valor_total) as total_gasto
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            GROUP BY c.nome
            ORDER BY total_gasto DESC
            LIMIT 5
        """)
        stats['top_clientes'] = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return stats
        
    except Exception as e:
        print(f"\n❌ Erro ao buscar estatísticas: {e}")
        if conn:
            conn.close()
        return {}

# Teste do módulo
if __name__ == "__main__":
    print("🧪 Testando módulo de vendas...\n")
    
    # Listar vendas
    vendas = listar_vendas(10)
    print(f"✅ Total de vendas: {len(vendas)}")
    
    # Estatísticas
    stats = estatisticas_vendas()
    print(f"✅ Faturamento total: R$ {stats.get('total_faturado', 0):.2f}")
