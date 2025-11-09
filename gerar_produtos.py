#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera produtos realistas para o banco de dados
"""

import psycopg2
import random

def conectar():
    """Conecta ao banco"""
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

def gerar_produtos():
    """Gera produtos realistas"""
    
    # Categorias e produtos
    produtos_por_categoria = {
        "Informática": [
            ("Notebook Dell Inspiron 15", 3500.00, random.randint(5, 20)),
            ("Notebook Lenovo IdeaPad", 2800.00, random.randint(5, 20)),
            ("Notebook HP Pavilion", 3200.00, random.randint(5, 20)),
            ("Notebook Acer Aspire", 2500.00, random.randint(5, 20)),
            ("Notebook Asus VivoBook", 2900.00, random.randint(5, 20)),
            ("MacBook Air M2", 8500.00, random.randint(3, 10)),
            ("MacBook Pro 14\"", 12000.00, random.randint(2, 8)),
            ("PC Gamer Completo", 4500.00, random.randint(5, 15)),
            ("PC Desktop i5", 2800.00, random.randint(10, 25)),
            ("PC Desktop i7", 3800.00, random.randint(10, 25)),
            ("Tablet Samsung Galaxy Tab", 1200.00, random.randint(15, 30)),
            ("Tablet iPad 10ª Geração", 3500.00, random.randint(10, 20)),
            ("Tablet Positivo", 600.00, random.randint(20, 40)),
        ],
        
        "Monitores": [
            ("Monitor LG 24\" Full HD", 899.00, random.randint(15, 40)),
            ("Monitor Samsung 27\" 4K", 1899.00, random.randint(10, 25)),
            ("Monitor Dell 24\" IPS", 1099.00, random.randint(12, 30)),
            ("Monitor AOC 27\" Gamer", 1499.00, random.randint(8, 20)),
            ("Monitor LG 29\" Ultrawide", 1799.00, random.randint(5, 15)),
            ("Monitor Samsung 32\" Curvo", 2299.00, random.randint(5, 12)),
            ("Monitor Philips 24\"", 799.00, random.randint(20, 45)),
        ],
        
        "Periféricos": [
            ("Mouse Logitech MX Master", 450.00, random.randint(30, 80)),
            ("Mouse Logitech G502", 350.00, random.randint(25, 60)),
            ("Mouse Razer DeathAdder", 380.00, random.randint(20, 50)),
            ("Mouse Gamer RGB", 120.00, random.randint(50, 100)),
            ("Teclado Mecânico Logitech", 599.00, random.randint(20, 50)),
            ("Teclado Mecânico Razer", 799.00, random.randint(15, 40)),
            ("Teclado Gamer RGB", 250.00, random.randint(30, 70)),
            ("Teclado e Mouse Sem Fio", 180.00, random.randint(40, 90)),
            ("Webcam Logitech C920", 450.00, random.randint(25, 60)),
            ("Webcam Full HD", 200.00, random.randint(35, 80)),
            ("Headset Gamer HyperX", 380.00, random.randint(30, 70)),
            ("Headset Logitech G733", 850.00, random.randint(15, 35)),
            ("Fone de Ouvido Bluetooth", 150.00, random.randint(50, 120)),
            ("Mousepad Gamer Grande", 80.00, random.randint(60, 150)),
            ("Suporte para Notebook", 120.00, random.randint(40, 100)),
        ],
        
        "Armazenamento": [
            ("SSD 480GB Kingston", 280.00, random.randint(30, 80)),
            ("SSD 1TB Samsung", 550.00, random.randint(25, 60)),
            ("SSD 2TB WD Blue", 980.00, random.randint(15, 40)),
            ("HD Externo 1TB", 350.00, random.randint(35, 90)),
            ("HD Externo 2TB", 480.00, random.randint(30, 75)),
            ("Pen Drive 64GB", 35.00, random.randint(100, 250)),
            ("Pen Drive 128GB", 55.00, random.randint(80, 200)),
            ("Cartão de Memória 64GB", 45.00, random.randint(90, 220)),
            ("Cartão de Memória 128GB", 75.00, random.randint(70, 180)),
        ],
        
        "Redes": [
            ("Roteador TP-Link AC1200", 180.00, random.randint(40, 100)),
            ("Roteador Intelbras", 120.00, random.randint(50, 120)),
            ("Roteador Mesh 3 Pack", 850.00, random.randint(10, 30)),
            ("Repetidor Wi-Fi", 80.00, random.randint(60, 150)),
            ("Switch 8 Portas", 150.00, random.randint(25, 70)),
            ("Cabo de Rede Cat6 5m", 25.00, random.randint(100, 300)),
        ],
        
        "Smartphones": [
            ("iPhone 14 128GB", 5500.00, random.randint(8, 25)),
            ("iPhone 13 128GB", 4200.00, random.randint(10, 30)),
            ("Samsung Galaxy S23", 4800.00, random.randint(12, 35)),
            ("Samsung Galaxy A54", 2200.00, random.randint(20, 60)),
            ("Xiaomi Redmi Note 12", 1400.00, random.randint(25, 70)),
            ("Motorola Edge 40", 2800.00, random.randint(15, 45)),
            ("Motorola Moto G73", 1600.00, random.randint(30, 80)),
        ],
        
        "Acessórios": [
            ("Carregador Rápido 65W", 120.00, random.randint(50, 150)),
            ("Cabo USB-C 2m", 35.00, random.randint(100, 300)),
            ("Cabo HDMI 2.0 3m", 45.00, random.randint(80, 250)),
            ("Hub USB 4 Portas", 65.00, random.randint(60, 180)),
            ("Adaptador USB-C para HDMI", 85.00, random.randint(40, 120)),
            ("Suporte para Monitor", 150.00, random.randint(30, 90)),
            ("Organizador de Cabos", 25.00, random.randint(80, 250)),
            ("Filtro de Linha 6 Tomadas", 45.00, random.randint(70, 200)),
            ("Nobreak 600VA", 350.00, random.randint(20, 60)),
        ],
        
        "Impressoras": [
            ("Impressora HP DeskJet", 450.00, random.randint(15, 40)),
            ("Impressora Epson EcoTank", 1200.00, random.randint(10, 30)),
            ("Impressora Brother Laser", 850.00, random.randint(12, 35)),
            ("Multifuncional HP", 680.00, random.randint(18, 50)),
            ("Scanner de Mesa", 380.00, random.randint(15, 45)),
        ],
        
        "Gaming": [
            ("Controle Xbox Wireless", 450.00, random.randint(25, 70)),
            ("Controle PS5 DualSense", 480.00, random.randint(20, 60)),
            ("Volante Logitech G29", 1800.00, random.randint(5, 15)),
            ("Cadeira Gamer", 950.00, random.randint(10, 30)),
            ("Mesa Gamer RGB", 650.00, random.randint(8, 25)),
        ],
        
        "Componentes": [
            ("Placa de Vídeo RTX 3060", 2800.00, random.randint(5, 15)),
            ("Placa de Vídeo GTX 1660", 1800.00, random.randint(8, 20)),
            ("Memória RAM 16GB DDR4", 350.00, random.randint(30, 80)),
            ("Memória RAM 32GB DDR4", 650.00, random.randint(20, 50)),
            ("Processador Intel i5", 1200.00, random.randint(15, 40)),
            ("Processador AMD Ryzen 5", 1100.00, random.randint(18, 45)),
            ("Placa Mãe Asus", 850.00, random.randint(12, 35)),
            ("Fonte 600W 80 Plus", 380.00, random.randint(25, 70)),
            ("Cooler CPU RGB", 180.00, random.randint(35, 90)),
            ("Gabinete Gamer RGB", 450.00, random.randint(20, 60)),
        ],
    }
    
    conn = conectar()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        total_inseridos = 0
        
        for categoria, produtos in produtos_por_categoria.items():
            for nome, preco, estoque in produtos:
                try:
                    # Gerar descrição
                    descricao = f"{nome} - Categoria: {categoria}"
                    
                    # Inserir produto
                    query = """
                        INSERT INTO produtos (nome, descricao, preco, estoque, categoria)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    
                    cursor.execute(query, (nome, descricao, preco, estoque, categoria))
                    total_inseridos += 1
                    
                except Exception as e:
                    # Produto já existe, ignorar
                    pass
        
        conn.commit()
        
        print("\n" + "=" * 80)
        print("✅ PRODUTOS GERADOS COM SUCESSO!")
        print("=" * 80)
        print(f"\n📦 Total de produtos inseridos: {total_inseridos}")
        print(f"📊 Categorias: {len(produtos_por_categoria)}")
        print("\n" + "=" * 80)
        
        # Mostrar estatísticas
        cursor.execute("SELECT COUNT(*) FROM produtos")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT categoria, COUNT(*) FROM produtos GROUP BY categoria ORDER BY COUNT(*) DESC")
        por_categoria = cursor.fetchall()
        
        print("\n📊 ESTATÍSTICAS:")
        print(f"\n   Total de produtos no banco: {total}")
        print(f"\n   Por categoria:")
        for cat, qtd in por_categoria:
            print(f"      {cat}: {qtd} produtos")
        
        print("\n" + "=" * 80)
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        if conn:
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    print("\n🚀 Gerando produtos realistas...\n")
    gerar_produtos()
