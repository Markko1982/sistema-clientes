#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de gerenciamento de vendas
CRUD completo de vendas
"""

import psycopg2
from datetime import datetime

# ============================================================================
# CONEXÃO
# ============================================================================

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
        print(f"\n❌ Erro ao conectar: {e}")
        return None

# ============================================================================
# CRUD DE VENDAS
# ============================================================================

def adicionar_venda(cliente_id, produto_id, quantidade, observacao=""):
    """
    Adiciona uma nova venda
    
    Args:
        cliente_id: ID do cliente
        produto_id: ID do produto
        quantidade: Quantidade vendida
        observacao: Observação opcional
        
    Returns:
        ID da venda ou None em caso de erro
    """
    conn = conectar()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Buscar preço do produto
        cursor.execute("SELECT preco, estoque FROM produtos WHERE id = %s", (produto_id,))
        resultado = cursor.fetchone()
        
        if not resultado:
            print(f"\n❌ Produto ID {produto_id} não encontrado!")
            cursor.close()
            conn.close()
            return None
        
        preco, estoque = resultado
        
        # Verificar estoque
        if estoque < quantidade:
            print(f"\n❌ Estoque insuficiente! Disponível: {estoque}, Solicitado: {quantidade}")
            cursor.close()
            conn.close()
            return None
        
        # Calcular valor total
        valor_unitario = float(preco)
        valor_total = valor_unitario * quantidade
        
        # Inserir venda
        query = """
            INSERT INTO vendas (cliente_id, produto_id, quantidade, valor_unitario, valor_total, observacao)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        
        cursor.execute(query, (cliente_id, produto_id, quantidade, valor_unitario, valor_total, observacao))
        venda_id = cursor.fetchone()[0]
        
        # Atualizar estoque
        cursor.execute("""
            UPDATE produtos 
            SET estoque = estoque - %s 
            WHERE id = %s
        """, (quantidade, produto_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n✅ Venda registrada com sucesso! ID: {venda_id}")
        print(f"💰 Valor total: R$ {valor_total:.2f}")
        print(f"📦 Estoque atualizado: {estoque} → {estoque - quantidade}")
        
        return venda_id
        
    except Exception as e:
        print(f"\n❌ Erro ao adicionar venda: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return None

def listar_vendas(limite=50):
    """
    Lista vendas com informações de cliente e produto
    
    Args:
        limite: Número máximo de vendas a retornar
        
    Returns:
        Lista de tuplas com dados das vendas
    """
    conn = conectar()
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
                v.data_venda
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
    Busca uma venda por ID
    
    Args:
        venda_id: ID da venda
        
    Returns:
        Tupla com dados da venda ou None
    """
    conn = conectar()
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
    Lista vendas de um cliente específico
    
    Args:
        cliente_id: ID do cliente
        
    Returns:
        Lista de tuplas com vendas do cliente
    """
    conn = conectar()
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
    Lista vendas de um produto específico
    
    Args:
        produto_id: ID do produto
        
    Returns:
        Lista de tuplas com vendas do produto
    """
    conn = conectar()
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
        venda_id: ID da venda
        
    Returns:
        True se cancelada com sucesso, False caso contrário
    """
    conn = conectar()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Buscar dados da venda
        cursor.execute("""
            SELECT produto_id, quantidade 
            FROM vendas 
            WHERE id = %s
        """, (venda_id,))
        
        resultado = cursor.fetchone()
        
        if not resultado:
            print(f"\n❌ Venda ID {venda_id} não encontrada!")
            cursor.close()
            conn.close()
            return False
        
        produto_id, quantidade = resultado
        
        # Devolver ao estoque
        cursor.execute("""
            UPDATE produtos 
            SET estoque = estoque + %s 
            WHERE id = %s
        """, (quantidade, produto_id))
        
        # Deletar venda
        cursor.execute("DELETE FROM vendas WHERE id = %s", (venda_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n✅ Venda cancelada com sucesso!")
        print(f"📦 Estoque devolvido: +{quantidade} unidades")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao cancelar venda: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

# ============================================================================
# ESTATÍSTICAS
# ============================================================================

def estatisticas_vendas():
    """
    Retorna estatísticas gerais de vendas
    
    Returns:
        Dicionário com estatísticas
    """
    conn = conectar()
    if not conn:
        return {
            'total_vendas': 0,
            'total_faturado': 0.0,
            'ticket_medio': 0.0,
            'top_produtos': [],
            'top_clientes': []
        }
    
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
        stats['total_vendas'] = resultado[0] if resultado else 0
        stats['total_faturado'] = float(resultado[1]) if resultado else 0.0
        stats['ticket_medio'] = float(resultado[2]) if resultado else 0.0
        
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
        return {
            'total_vendas': 0,
            'total_faturado': 0.0,
            'ticket_medio': 0.0,
            'top_produtos': [],
            'top_clientes': []
        }

# Alias para compatibilidade
estatisticas_vendas_v2 = estatisticas_vendas

def contar_vendas():
    """
    Conta o total de vendas
    
    Returns:
        Número total de vendas
    """
    conn = conectar()
    if not conn:
        return 0
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vendas")
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total
    except Exception as e:
        print(f"\n❌ Erro ao contar vendas: {e}")
        if conn:
            conn.close()
        return 0

# ============================================================================
# TESTE DO MÓDULO
# ============================================================================

if __name__ == "__main__":
    print("🧪 Testando módulo de vendas...\n")
    
    # Listar vendas
    print("📋 Listando vendas...")
    vendas = listar_vendas(10)
    print(f"✅ Total de vendas: {len(vendas)}\n")
    
    # Estatísticas
    print("📊 Estatísticas...")
    stats = estatisticas_vendas()
    print(f"✅ Total de vendas: {stats['total_vendas']}")
    print(f"💰 Faturamento total: R$ {stats['total_faturado']:.2f}")
    print(f"🎯 Ticket médio: R$ {stats['ticket_medio']:.2f}")
    
    if stats['top_produtos']:
        print(f"\n🏆 Top produtos:")
        for produto, qtd in stats['top_produtos']:
            print(f"   {produto}: {qtd} unidades")
    
    if stats['top_clientes']:
        print(f"\n👥 Top clientes:")
        for cliente, total in stats['top_clientes']:
            print(f"   {cliente}: R$ {total:.2f}")
    
    print("\n✅ Módulo de vendas funcionando corretamente!")

# Alias para compatibilidade com main.py
registrar_venda = adicionar_venda

# Alias para compatibilidade com main.py
registrar_venda = adicionar_venda

# Alias para compatibilidade
registrar_venda = adicionar_venda
