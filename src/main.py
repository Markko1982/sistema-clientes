#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Gerenciamento de Clientes - Interface CLI
Menu interativo para gerenciar clientes
"""

import os
from cliente import (
    cadastrar_cliente, listar_clientes, buscar_cliente,
    buscar_por_nome, atualizar_cliente, deletar_cliente,
    contar_clientes, estatisticas
)


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('clear' if os.name != 'nt' else 'cls')


def pausar():
    """Pausa e aguarda Enter"""
    input("\n⏸️  Pressione ENTER para continuar...")


def exibir_cabecalho():
    """Exibe cabeçalho do sistema"""
    limpar_tela()
    print("╔" + "═" * 60 + "╗")
    print("║" + " " * 10 + "SISTEMA DE GERENCIAMENTO DE CLIENTES" + " " * 14 + "║")
    print("╚" + "═" * 60 + "╝")
    print()
    
    # Mostrar total de clientes
    total = contar_clientes()
    print(f"📊 Total de clientes no sistema: {total}")
    print()


# ============================================================================
# OPÇÃO 1: CADASTRAR CLIENTE
# ============================================================================

def menu_cadastrar():
    """Menu para cadastrar novo cliente"""
    exibir_cabecalho()
    print("📝 CADASTRAR NOVO CLIENTE")
    print("-" * 60)
    print()
    
    try:
        nome = input("Nome completo: ").strip()
        if not nome:
            print("❌ Nome não pode ser vazio!")
            pausar()
            return
        
        email = input("Email: ").strip()
        if not email:
            print("❌ Email não pode ser vazio!")
            pausar()
            return
        
        telefone = input("Telefone (ex: (11) 98765-4321): ").strip()
        cidade = input("Cidade: ").strip()
        
        print("\n🔄 Cadastrando...")
        id_cliente = cadastrar_cliente(nome, email, telefone, cidade)
        
        if id_cliente:
            print(f"\n✅ Cliente cadastrado com sucesso! ID: {id_cliente}")
        else:
            print("\n❌ Erro ao cadastrar cliente!")
    
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()


# ============================================================================
# OPÇÃO 2: LISTAR CLIENTES
# ============================================================================

def menu_listar():
    """Menu para listar clientes com paginação"""
    pagina = 1
    por_pagina = 20
    
    while True:
        exibir_cabecalho()
        print("📋 LISTA DE CLIENTES")
        print("-" * 60)
        
        # Calcular offset
        offset = (pagina - 1) * por_pagina
        
        # Buscar clientes
        clientes = listar_clientes(limite=por_pagina, offset=offset)
        total = contar_clientes()
        total_paginas = (total + por_pagina - 1) // por_pagina
        
        if not clientes:
            print("\n📭 Nenhum cliente encontrado nesta página!")
        else:
            print(f"\n📄 Página {pagina}/{total_paginas} (Total: {total} clientes)")
            print()
            print(f"{'ID':>5} | {'Nome':<30} | {'Cidade':<20}")
            print("-" * 60)
            
            for c in clientes:
                id_cliente, nome, email, telefone, cidade, data = c
                print(f"{id_cliente:>5} | {nome:<30} | {cidade:<20}")
        
        # Menu de navegação
        print("\n" + "-" * 60)
        print("Navegação:")
        if pagina > 1:
            print("  [A] Página anterior")
        if pagina < total_paginas:
            print("  [P] Próxima página")
        print("  [N] Ir para página específica")
        print("  [V] Voltar ao menu principal")
        
        opcao = input("\nEscolha: ").strip().upper()
        
        if opcao == 'A' and pagina > 1:
            pagina -= 1
        elif opcao == 'P' and pagina < total_paginas:
            pagina += 1
        elif opcao == 'N':
            try:
                nova_pagina = int(input(f"Número da página (1-{total_paginas}): "))
                if 1 <= nova_pagina <= total_paginas:
                    pagina = nova_pagina
                else:
                    print("❌ Página inválida!")
                    pausar()
            except:
                print("❌ Número inválido!")
                pausar()
        elif opcao == 'V':
            break
        else:
            print("❌ Opção inválida!")
            pausar()


# ============================================================================
# OPÇÃO 3: BUSCAR CLIENTE
# ============================================================================

def menu_buscar():
    """Menu para buscar clientes"""
    exibir_cabecalho()
    print("🔍 BUSCAR CLIENTE")
    print("-" * 60)
    print()
    print("Buscar por:")
    print("  1. ID")
    print("  2. Nome")
    print("  3. Cidade")
    print("  0. Voltar")
    print()
    
    opcao = input("Escolha: ").strip()
    
    if opcao == '1':
        buscar_por_id()
    elif opcao == '2':
        buscar_por_nome_menu()
    elif opcao == '3':
        buscar_por_cidade()
    elif opcao == '0':
        return
    else:
        print("❌ Opção inválida!")
        pausar()


def buscar_por_id():
    """Busca cliente por ID"""
    try:
        id_cliente = int(input("\nID do cliente: "))
        
        print("\n🔄 Buscando...")
        cliente = buscar_cliente(id_cliente)
        
        if cliente:
            print("\n✅ Cliente encontrado:")
            print("-" * 60)
            print(f"ID:       {cliente[0]}")
            print(f"Nome:     {cliente[1]}")
            print(f"Email:    {cliente[2]}")
            print(f"Telefone: {cliente[3]}")
            print(f"Cidade:   {cliente[4]}")
            print(f"Cadastro: {cliente[5]}")
        else:
            print(f"\n❌ Cliente com ID {id_cliente} não encontrado!")
    
    except ValueError:
        print("\n❌ ID inválido!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()


def buscar_por_nome_menu():
    """Busca clientes por nome"""
    nome = input("\nNome (ou parte do nome): ").strip()
    
    if not nome:
        print("❌ Nome não pode ser vazio!")
        pausar()
        return
    
    print("\n🔄 Buscando...")
    clientes = buscar_por_nome(nome)
    
    if clientes:
        print(f"\n✅ Encontrados {len(clientes)} cliente(s):")
        print("-" * 60)
        print(f"{'ID':>5} | {'Nome':<30} | {'Cidade':<20}")
        print("-" * 60)
        
        for c in clientes[:50]:  # Limitar a 50 resultados
            print(f"{c[0]:>5} | {c[1]:<30} | {c[4]:<20}")
        
        if len(clientes) > 50:
            print(f"\n⚠️  Mostrando apenas os primeiros 50 de {len(clientes)} resultados")
    else:
        print(f"\n❌ Nenhum cliente encontrado com '{nome}'")
    
    pausar()


def buscar_por_cidade():
    """Busca clientes por cidade"""
    cidade = input("\nCidade: ").strip()
    
    if not cidade:
        print("❌ Cidade não pode ser vazia!")
        pausar()
        return
    
    print("\n🔄 Buscando...")
    clientes = listar_clientes(cidade=cidade, limite=50)
    total = contar_clientes(cidade=cidade)
    
    if clientes:
        print(f"\n✅ Encontrados {total} cliente(s) em {cidade}:")
        print("-" * 60)
        print(f"{'ID':>5} | {'Nome':<30} | {'Telefone':<15}")
        print("-" * 60)
        
        for c in clientes:
            print(f"{c[0]:>5} | {c[1]:<30} | {c[3]:<15}")
        
        if total > 50:
            print(f"\n⚠️  Mostrando apenas os primeiros 50 de {total} resultados")
    else:
        print(f"\n❌ Nenhum cliente encontrado em {cidade}")
    
    pausar()


# ============================================================================
# OPÇÃO 4: ATUALIZAR CLIENTE
# ============================================================================

def menu_atualizar():
    """Menu para atualizar cliente"""
    exibir_cabecalho()
    print("✏️  ATUALIZAR CLIENTE")
    print("-" * 60)
    print()
    
    try:
        id_cliente = int(input("ID do cliente: "))
        
        # Buscar cliente
        cliente = buscar_cliente(id_cliente)
        
        if not cliente:
            print(f"\n❌ Cliente com ID {id_cliente} não encontrado!")
            pausar()
            return
        
        # Mostrar dados atuais
        print("\n📋 Dados atuais:")
        print(f"  Nome:     {cliente[1]}")
        print(f"  Email:    {cliente[2]}")
        print(f"  Telefone: {cliente[3]}")
        print(f"  Cidade:   {cliente[4]}")
        print()
        
        # Menu de atualização
        print("O que deseja atualizar?")
        print("  1. Nome")
        print("  2. Email")
        print("  3. Telefone")
        print("  4. Cidade")
        print("  5. Tudo")
        print("  0. Cancelar")
        print()
        
        opcao = input("Escolha: ").strip()
        
        nome = email = telefone = cidade = None
        
        if opcao == '1':
            nome = input("\nNovo nome: ").strip()
        elif opcao == '2':
            email = input("\nNovo email: ").strip()
        elif opcao == '3':
            telefone = input("\nNovo telefone: ").strip()
        elif opcao == '4':
            cidade = input("\nNova cidade: ").strip()
        elif opcao == '5':
            nome = input("\nNovo nome: ").strip()
            email = input("Novo email: ").strip()
            telefone = input("Novo telefone: ").strip()
            cidade = input("Nova cidade: ").strip()
        elif opcao == '0':
            print("\n❌ Operação cancelada!")
            pausar()
            return
        else:
            print("\n❌ Opção inválida!")
            pausar()
            return
        
        # Atualizar
        print("\n🔄 Atualizando...")
        sucesso = atualizar_cliente(id_cliente, nome, email, telefone, cidade)
        
        if sucesso:
            print("\n✅ Cliente atualizado com sucesso!")
        else:
            print("\n❌ Erro ao atualizar cliente!")
    
    except ValueError:
        print("\n❌ ID inválido!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()


# ============================================================================
# OPÇÃO 5: DELETAR CLIENTE
# ============================================================================

def menu_deletar():
    """Menu para deletar cliente"""
    exibir_cabecalho()
    print("❌ DELETAR CLIENTE")
    print("-" * 60)
    print()
    
    try:
        id_cliente = int(input("ID do cliente: "))
        
        # Buscar cliente
        cliente = buscar_cliente(id_cliente)
        
        if not cliente:
            print(f"\n❌ Cliente com ID {id_cliente} não encontrado!")
            pausar()
            return
        
        # Mostrar dados e confirmar
        print("\n⚠️  ATENÇÃO! Você está prestes a deletar:")
        print("-" * 60)
        print(f"ID:    {cliente[0]}")
        print(f"Nome:  {cliente[1]}")
        print(f"Email: {cliente[2]}")
        print("-" * 60)
        print()
        
        confirmacao = input("⚠️  Tem certeza? Digite 'SIM' para confirmar: ").strip().upper()
        
        if confirmacao == 'SIM':
            print("\n🔄 Deletando...")
            sucesso = deletar_cliente(id_cliente)
            
            if sucesso:
                print("\n✅ Cliente deletado com sucesso!")
            else:
                print("\n❌ Erro ao deletar cliente!")
        else:
            print("\n❌ Operação cancelada!")
    
    except ValueError:
        print("\n❌ ID inválido!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()


# ============================================================================
# OPÇÃO 6: ESTATÍSTICAS
# ============================================================================

def menu_estatisticas():
    """Menu de estatísticas"""
    exibir_cabecalho()
    print("📊 ESTATÍSTICAS DO SISTEMA")
    print("-" * 60)
    print()
    
    print("🔄 Gerando estatísticas...")
    stats = estatisticas()
    
    if stats:
        print(f"\n📈 RESUMO GERAL:")
        print(f"   Total de clientes: {stats['total']}")
        
        if stats['mais_recente']:
            print(f"   Cadastro mais recente: {stats['mais_recente'][0]}")
        
        print(f"\n📍 DISTRIBUIÇÃO POR CIDADE (Top 10):")
        print("-" * 60)
        print(f"{'Cidade':<25} | {'Clientes':>10} | {'Percentual':>10}")
        print("-" * 60)
        
        for cidade, total in stats['cidades']:
            percentual = (total / stats['total']) * 100
            print(f"{cidade:<25} | {total:>10} | {percentual:>9.1f}%")
    else:
        print("\n❌ Erro ao gerar estatísticas!")
    
    pausar()


# ============================================================================
# MENU PRINCIPAL
# ============================================================================

def menu_principal():
    """Menu principal do sistema"""
    while True:
        exibir_cabecalho()
        print("MENU PRINCIPAL:")
        print("  1. 📝 Cadastrar novo cliente")
        print("  2. 📋 Listar clientes")
        print("  3. 🔍 Buscar cliente")
        print("  4. ✏️  Atualizar cliente")
        print("  5. ❌ Deletar cliente")
        print("  6. 📊 Estatísticas")
        print("  0. 🚪 Sair")
        print()
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == '1':
            menu_cadastrar()
        elif opcao == '2':
            menu_listar()
        elif opcao == '3':
            menu_buscar()
        elif opcao == '4':
            menu_atualizar()
        elif opcao == '5':
            menu_deletar()
        elif opcao == '6':
            menu_estatisticas()
        elif opcao == '0':
            limpar_tela()
            print("👋 Obrigado por usar o Sistema de Gerenciamento de Clientes!")
            print("✅ Até logo!\n")
            break
        else:
            print("\n❌ Opção inválida! Tente novamente.")
            pausar()


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        limpar_tela()
        print("\n\n⚠️  Programa interrompido pelo usuário!")
        print("👋 Até logo!\n")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
