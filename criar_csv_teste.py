#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera CSV de teste com muitos clientes
"""

import csv
import random

# Listas para gerar nomes aleatórios
nomes = ['João', 'Maria', 'Pedro', 'Ana', 'Carlos', 'Julia', 'Lucas', 'Fernanda', 'Rafael', 'Camila']
sobrenomes = ['Silva', 'Santos', 'Oliveira', 'Souza', 'Lima', 'Costa', 'Pereira', 'Rodrigues', 'Almeida', 'Nascimento']
cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Porto Alegre', 'Salvador', 'Brasília', 'Fortaleza', 'Recife', 'Manaus']

quantidade = int(input("\n📊 Quantos clientes deseja gerar? [100]: ").strip() or "100")

arquivo = f"clientes_teste_{quantidade}.csv"

with open(arquivo, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    
    # Cabeçalho
    writer.writerow(['nome', 'email', 'telefone', 'cidade'])
    
    # Gerar clientes
    for i in range(1, quantidade + 1):
        nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
        email = f"{nome.lower().replace(' ', '.')}.{i}@email.com"
        ddd = random.choice(['11', '21', '31', '41', '51', '71', '61', '85', '81', '92'])
        telefone = f"{ddd}9{random.randint(10000000, 99999999)}"
        cidade = random.choice(cidades)
        
        writer.writerow([nome, email, telefone, cidade])

print(f"\n✅ Arquivo criado: {arquivo}")
print(f"📊 Total de clientes: {quantidade}")
print(f"\n🚀 Para importar, use:")
print(f"   importar-csv")
print(f"   Opção 1")
print(f"   Arquivo: {arquivo}")
