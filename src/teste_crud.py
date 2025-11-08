#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do módulo CRUD
"""

from cliente import cadastrar_cliente, listar_clientes, contar_clientes, buscar_cliente

print("=" * 60)
print("TESTE DO MÓDULO CRUD")
print("=" * 60)

# Teste 1: Cadastrar cliente
print("\n1️⃣ CADASTRANDO CLIENTE DE TESTE...")
id_cliente = cadastrar_cliente(
    nome="Maria Santos",
    email="maria.santos@techdata.com.br",
    telefone="(11) 98765-4321",
    cidade="São Paulo"
)

if id_cliente:
    print(f"   ✅ Cliente cadastrado com ID: {id_cliente}")
else:
    print("   ❌ Erro ao cadastrar")

# Teste 2: Contar clientes
print("\n2️⃣ CONTANDO CLIENTES...")
total = contar_clientes()
print(f"   📊 Total de clientes no banco: {total}")

# Teste 3: Buscar o cliente cadastrado
if id_cliente:
    print(f"\n3️⃣ BUSCANDO CLIENTE ID {id_cliente}...")
    cliente = buscar_cliente(id_cliente)
    if cliente:
        print(f"   ✅ Cliente encontrado:")
        print(f"      Nome: {cliente[1]}")
        print(f"      Email: {cliente[2]}")
        print(f"      Telefone: {cliente[3]}")
        print(f"      Cidade: {cliente[4]}")

# Teste 4: Listar todos os clientes
print("\n4️⃣ LISTANDO TODOS OS CLIENTES...")
clientes = listar_clientes(limite=10)
print(f"   📋 Mostrando {len(clientes)} cliente(s):")
for c in clientes:
    print(f"      • ID: {c[0]:3d} | {c[1]:30s} | {c[4]}")

print("\n" + "=" * 60)
print("✅ TESTES CONCLUÍDOS!")
print("=" * 60)
