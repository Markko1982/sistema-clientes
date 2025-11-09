#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Gerenciamento de Clientes, Produtos e Vendas
Menu principal integrado
"""

import cliente
import produto
import vendas
import sys

def limpar_tela():
    """Limpa a tela do terminal"""
    import os
    os.system('clear' if os.name != 'nt' else 'cls')

def pausar():
    """Pausa e aguarda Enter"""
    input("\n⏸️  Pressione ENTER para continuar...")

def menu_principal():
    """Menu principal do sistema"""
    while True:
        limpar_tela()
        print("=" * 80)
        print(" " * 20 + "🏢 SISTEMA DE GERENCIAMENTO")
        print("=" * 80)
        print("\n📋 MENU PRINCIPAL:\n")
        print("   1. 👥 Gerenciar Clientes")
        print("   2. 📦 Gerenciar Produtos")
        print("   3. 💰 Gerenciar Vendas")
        print("   4. 📊 Relatórios")
        print("   5. ℹ️  Sobre o Sistema")
        print("   6. 🚪 Sair")
        print("\n" + "-" * 80)
        
        opcao = input("\n👉 Escolha uma opção: ").strip()
        
        if opcao == "1":
            menu_clientes()
        elif opcao == "2":
            menu_produtos()
        elif opcao == "3":
            menu_vendas()
        elif opcao == "4":
            menu_relatorios()
        elif opcao == "5":
            sobre_sistema()
        elif opcao == "6":
            limpar_tela()
            print("\n" + "=" * 80)
            print(" " * 25 + "👋 ATÉ LOGO!")
            print("=" * 80)
            print("\n   Obrigado por usar o Sistema de Gerenciamento!")
            print("\n" + "=" * 80 + "\n")
            sys.exit(0)
        else:
            print("\n❌ Opção inválida! Tente novamente.")
            pausar()

def menu_clientes():
    """Menu de gerenciamento de clientes"""
    while True:
        limpar_tela()
        print("=" * 80)
        print(" " * 25 + "👥 GERENCIAR CLIENTES")
        print("=" * 80)
        print("\n📋 OPÇÕES:\n")
        print("   1. ➕ Cadastrar novo cliente")
        print("   2. 📋 Listar todos os clientes")
        print("   3. 🔍 Buscar cliente por ID")
        print("   4. 📊 Ver histórico de compras")
        print("   5. ⬅️  Voltar ao menu principal")
        print("\n" + "-" * 80)
        
        opcao = input("\n👉 Escolha uma opção: ").strip()
        
        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            listar_clientes()
        elif opcao == "3":
            buscar_cliente()
        elif opcao == "4":
            historico_cliente()
        elif opcao == "5":
            break
        else:
            print("\n❌ Opção inválida!")
            pausar()

def menu_produtos():
    """Menu de gerenciamento de produtos"""
    while True:
        limpar_tela()
        print("=" * 80)
        print(" " * 25 + "📦 GERENCIAR PRODUTOS")
        print("=" * 80)
        print("\n📋 OPÇÕES:\n")
        print("   1. ➕ Cadastrar novo produto")
        print("   2. 📋 Listar todos os produtos")
        print("   3. 🔍 Buscar produto por ID")
        print("   4. 📊 Ver histórico de vendas")
        print("   5. ⬅️  Voltar ao menu principal")
        print("\n" + "-" * 80)
        
        opcao = input("\n👉 Escolha uma opção: ").strip()
        
        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            buscar_produto()
        elif opcao == "4":
            historico_produto()
        elif opcao == "5":
            break
        else:
            print("\n❌ Opção inválida!")
            pausar()

def menu_vendas():
    """Menu de gerenciamento de vendas"""
    while True:
        limpar_tela()
        print("=" * 80)
        print(" " * 25 + "💰 GERENCIAR VENDAS")
        print("=" * 80)
        print("\n📋 OPÇÕES:\n")
        print("   1. ➕ Registrar nova venda")
        print("   2. 📋 Listar todas as vendas")
        print("   3. 🔍 Buscar venda por ID")
        print("   4. ❌ Cancelar venda")
        print("   5. 📊 Estatísticas de vendas")
        print("   6. ⬅️  Voltar ao menu principal")
        print("\n" + "-" * 80)
        
        opcao = input("\n👉 Escolha uma opção: ").strip()
        
        if opcao == "1":
            registrar_venda()
        elif opcao == "2":
            listar_vendas_menu()
        elif opcao == "3":
            buscar_venda()
        elif opcao == "4":
            cancelar_venda_menu()
        elif opcao == "5":
            estatisticas_vendas_menu()
        elif opcao == "6":
            break
        else:
            print("\n❌ Opção inválida!")
            pausar()

def menu_relatorios():
    """Menu de relatórios"""
    while True:
        limpar_tela()
        print("=" * 80)
        print(" " * 28 + "📊 RELATÓRIOS")
        print("=" * 80)
        print("\n📋 OPÇÕES:\n")
        print("   1. 👥 Top 10 clientes")
        print("   2. 📦 Top 10 produtos mais vendidos")
        print("   3. 💰 Faturamento total")
        print("   4. 📊 Resumo geral")
        print("   5. ⬅️  Voltar ao menu principal")
        print("\n" + "-" * 80)
        
        opcao = input("\n👉 Escolha uma opção: ").strip()
        
        if opcao == "1":
            relatorio_top_clientes()
        elif opcao == "2":
            relatorio_top_produtos()
        elif opcao == "3":
            relatorio_faturamento()
        elif opcao == "4":
            relatorio_geral()
        elif opcao == "5":
            break
        else:
            print("\n❌ Opção inválida!")
            pausar()

def sobre_sistema():
    """Informações sobre o sistema"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "ℹ️  SOBRE O SISTEMA")
    print("=" * 80)
    print("\n📋 Sistema de Gerenciamento Completo")
    print("\n📅 Versão: 2.0.0")
    print("👤 Desenvolvedor: Markko")
    print("🗄️  Banco de Dados: PostgreSQL")
    print("🐍 Linguagem: Python 3")
    print("📝 Git: https://github.com/Markko1982/sistema-clientes" )
    print("\n💡 Funcionalidades:")
    print("   ✅ Gerenciamento de clientes")
    print("   ✅ Gerenciamento de produtos")
    print("   ✅ Sistema de vendas")
    print("   ✅ Relatórios gerenciais")
    print("   ✅ Importação de CSV")
    print("   ✅ Busca avançada")
    print("   ✅ Controle de estoque")
    print("\n" + "=" * 80)
    pausar()

# ============================================================================
# FUNÇÕES DE CLIENTES
# ============================================================================

def cadastrar_cliente():
    """Cadastra novo cliente"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "➕ CADASTRAR CLIENTE")
    print("=" * 80)
    
    try:
        nome = input("\n👤 Nome: ").strip()
        email = input("📧 Email: ").strip()
        telefone = input("📱 Telefone: ").strip()
        cidade = input("🏙️  Cidade: ").strip()
        
        if nome and email:
            cliente.cadastrar_cliente(nome, email, telefone, cidade)
        else:
            print("\n❌ Nome e email são obrigatórios!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

def listar_clientes():
    """Lista todos os clientes"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "📋 LISTA DE CLIENTES")
    print("=" * 80)
    
    try:
        clientes = cliente.listar_clientes(limite=20)
        
        if clientes:
            print(f"\n✅ Total: {len(clientes)} clientes\n")
            print("-" * 80)
            print(f"{'ID':<5} {'NOME':<30} {'EMAIL':<30} {'CIDADE':<15}")
            print("-" * 80)
            
            for c in clientes:
                print(f"{c[0]:<5} {c[1][:30]:<30} {c[2][:30]:<30} {c[4][:15] if c[4] else '-':<15}")
            
            print("-" * 80)
        else:
            print("\n⚠️  Nenhum cliente cadastrado.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

def buscar_cliente():
    """Busca cliente por ID"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "🔍 BUSCAR CLIENTE")
    print("=" * 80)
    
    try:
        cliente_id = int(input("\n🔢 ID do cliente: ").strip())
        c = cliente.buscar_cliente(cliente_id)
        
        if c:
            print("\n✅ Cliente encontrado:\n")
            print(f"   ID: {c[0]}")
            print(f"   Nome: {c[1]}")
            print(f"   Email: {c[2]}")
            print(f"   Telefone: {c[3] if c[3] else '-'}")
            print(f"   Cidade: {c[4] if c[4] else '-'}")
        else:
            print(f"\n❌ Cliente ID {cliente_id} não encontrado.")
    except ValueError:
        print("\n❌ ID inválido!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

def historico_cliente():
    """Mostra histórico de compras de um cliente"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "📊 HISTÓRICO DE COMPRAS")
    print("=" * 80)
    
    try:
        cliente_id = int(input("\n🔢 ID do cliente: ").strip())
        
        # Buscar cliente
        c = cliente.buscar_cliente(cliente_id)
        if not c:
            print(f"\n❌ Cliente ID {cliente_id} não encontrado.")
            pausar()
            return
        
        print(f"\n👤 Cliente: {c[1]}")
        print("\n📋 Histórico de compras:\n")
        
        # Buscar vendas do cliente
        vendas_cliente = vendas.vendas_por_cliente(cliente_id)
        
        if vendas_cliente:
            print("-" * 80)
            print(f"{'ID':<5} {'PRODUTO':<30} {'QTD':<5} {'VALOR':<15} {'DATA':<20}")
            print("-" * 80)
            
            total = 0
            for v in vendas_cliente:
                print(f"{v[0]:<5} {v[1][:30]:<30} {v[2]:<5} R$ {v[3]:<12.2f} {v[4]}")
                total += v[3]
            
            print("-" * 80)
            print(f"{'TOTAL GASTO:':<42} R$ {total:.2f}")
            print("-" * 80)
        else:
            print("⚠️  Nenhuma compra realizada ainda.")
    
    except ValueError:
        print("\n❌ ID inválido!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

# ============================================================================
# FUNÇÕES DE PRODUTOS
# ============================================================================

def cadastrar_produto():
    """Cadastra novo produto"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "➕ CADASTRAR PRODUTO")
    print("=" * 80)
    
    try:
        nome = input("\n📦 Nome: ").strip()
        preco = float(input("💰 Preço: R$ ").strip())
        estoque = int(input("📊 Estoque: ").strip())
        categoria = input("🏷️  Categoria: ").strip()
        descricao = input("📝 Descrição (opcional): ").strip() or None
        
        if nome and preco >= 0 and estoque >= 0:
            produto.cadastrar_produto(nome, preco, estoque, categoria, descricao)
        else:
            print("\n❌ Dados inválidos!")
    except ValueError:
        print("\n❌ Preço e estoque devem ser números!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

def listar_produtos():
    """Lista todos os produtos"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "📋 LISTA DE PRODUTOS")
    print("=" * 80)
    
    try:
        produtos = produto.listar_produtos(limite=20)
        
        if produtos:
            print(f"\n✅ Total: {len(produtos)} produtos\n")
            print("-" * 80)
            print(f"{'ID':<5} {'NOME':<30} {'PREÇO':<12} {'ESTOQUE':<10} {'CATEGORIA':<15}")
            print("-" * 80)
            
            for p in produtos:
                print(f"{p[0]:<5} {p[1][:30]:<30} R$ {p[2]:<9.2f} {p[3]:<10} {p[4][:15]:<15}")
            
            print("-" * 80)
        else:
            print("\n⚠️  Nenhum produto cadastrado.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

def buscar_produto():
    """Busca produto por ID"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "🔍 BUSCAR PRODUTO")
    print("=" * 80)
    
    try:
        produto_id = int(input("\n🔢 ID do produto: ").strip())
        p = produto.buscar_produto(produto_id)
        
        if p:
            print("\n✅ Produto encontrado:\n")
            print(f"   ID: {p[0]}")
            print(f"   Nome: {p[1]}")
            print(f"   Descrição: {p[2] if p[2] else '-'}")
            print(f"   Preço: R$ {p[3]:.2f}")
            print(f"   Estoque: {p[4]}")
            print(f"   Categoria: {p[5]}")
        else:
            print(f"\n❌ Produto ID {produto_id} não encontrado.")
    except ValueError:
        print("\n❌ ID inválido!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

def historico_produto():
    """Mostra histórico de vendas de um produto"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "📊 HISTÓRICO DE VENDAS")
    print("=" * 80)
    
    try:
        produto_id = int(input("\n🔢 ID do produto: ").strip())
        
        # Buscar produto
        p = produto.buscar_produto(produto_id)
        if not p:
            print(f"\n❌ Produto ID {produto_id} não encontrado.")
            pausar()
            return
        
        print(f"\n📦 Produto: {p[1]}")
        print(f"💰 Preço: R$ {p[3]:.2f}")
        print(f"📊 Estoque atual: {p[4]}")
        print("\n📋 Histórico de vendas:\n")
        
        # Buscar vendas do produto
        vendas_produto = vendas.vendas_por_produto(produto_id)
        
        if vendas_produto:
            print("-" * 80)
            print(f"{'ID':<5} {'CLIENTE':<30} {'QTD':<5} {'VALOR':<15} {'DATA':<20}")
            print("-" * 80)
            
            total_vendido = 0
            total_faturado = 0
            for v in vendas_produto:
                print(f"{v[0]:<5} {v[1][:30]:<30} {v[2]:<5} R$ {v[3]:<12.2f} {v[4]}")
                total_vendido += v[2]
                total_faturado += v[3]
            
            print("-" * 80)
            print(f"{'TOTAL VENDIDO:':<42} {total_vendido} unidades")
            print(f"{'TOTAL FATURADO:':<42} R$ {total_faturado:.2f}")
            print("-" * 80)
        else:
            print("⚠️  Nenhuma venda realizada ainda.")
    
    except ValueError:
        print("\n❌ ID inválido!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

# ============================================================================
# FUNÇÕES DE VENDAS
# ============================================================================

def registrar_venda():
    """Registra uma nova venda"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "➕ REGISTRAR VENDA")
    print("=" * 80)
    
    try:
        cliente_id = int(input("\n🔢 ID do cliente: ").strip())
        produto_id = int(input("🔢 ID do produto: ").strip())
        quantidade = int(input("📊 Quantidade: ").strip())
        observacao = input("📝 Observação (opcional): ").strip() or None
        
        if quantidade > 0:
            vendas.registrar_venda(cliente_id, produto_id, quantidade, observacao)
        else:
            print("\n❌ Quantidade deve ser maior que zero!")
    except ValueError:
        print("\n❌ IDs e quantidade devem ser números!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

def listar_vendas_menu():
    """Lista todas as vendas"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "📋 LISTA DE VENDAS")
    print("=" * 80)
    
    try:
        vendas_lista = vendas.listar_vendas(limite=20)
        
        if vendas_lista:
            print(f"\n✅ Total: {len(vendas_lista)} vendas\n")
            print("-" * 100)
            print(f"{'ID':<5} {'CLIENTE':<20} {'PRODUTO':<20} {'QTD':<5} {'VALOR':<12} {'DATA':<20}")
            print("-" * 100)
            
            for v in vendas_lista:
                print(f"{v[0]:<5} {v[1][:20]:<20} {v[2][:20]:<20} {v[3]:<5} R$ {v[5]:<9.2f} {v[6]}")
            
            print("-" * 100)
        else:
            print("\n⚠️  Nenhuma venda registrada.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

def buscar_venda():
    """Busca venda por ID"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "🔍 BUSCAR VENDA")
    print("=" * 80)
    
    try:
        venda_id = int(input("\n🔢 ID da venda: ").strip())
        v = vendas.buscar_venda(venda_id)
        
        if v:
            print("\n✅ Venda encontrada:\n")
            print(f"   ID: {v[0]}")
            print(f"   Cliente: {v[2]} (ID: {v[1]})")
            print(f"   Produto: {v[4]} (ID: {v[3]})")
            print(f"   Quantidade: {v[5]}")
            print(f"   Valor Unitário: R$ {v[6]:.2f}")
            print(f"   Valor Total: R$ {v[7]:.2f}")
            print(f"   Data: {v[8]}")
            if v[9]:
                print(f"   Observação: {v[9]}")
        else:
            print(f"\n❌ Venda ID {venda_id} não encontrada.")
    except ValueError:
        print("\n❌ ID inválido!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

def cancelar_venda_menu():
    """Cancela uma venda"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "❌ CANCELAR VENDA")
    print("=" * 80)
    
    try:
        venda_id = int(input("\n🔢 ID da venda: ").strip())
        
        confirma = input(f"\n⚠️  Tem certeza que deseja cancelar a venda ID {venda_id}? (s/n): ").strip().lower()
        
        if confirma == 's':
            vendas.cancelar_venda(venda_id)
        else:
            print("\n❌ Operação cancelada.")
    except ValueError:
        print("\n❌ ID inválido!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

def estatisticas_vendas_menu():
    """Mostra estatísticas de vendas"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "📊 ESTATÍSTICAS DE VENDAS")
    print("=" * 80)
    
    try:
        stats = vendas.estatisticas_vendas()
        
        if stats:
            print(f"\n💰 FATURAMENTO:")
            print(f"   Total de vendas: {stats['total_vendas']}")
            print(f"   Total faturado: R$ {stats['total_faturado']:.2f}")
            print(f"   Ticket médio: R$ {stats['ticket_medio']:.2f}")
            
            if stats.get('top_produtos'):
                print(f"\n📦 TOP 5 PRODUTOS MAIS VENDIDOS:")
                for i, (nome, qtd) in enumerate(stats['top_produtos'], 1):
                    print(f"   {i}. {nome}: {qtd} unidades")
            
            if stats.get('top_clientes'):
                print(f"\n👥 TOP 5 CLIENTES:")
                for i, (nome, total) in enumerate(stats['top_clientes'], 1):
                    print(f"   {i}. {nome}: R$ {total:.2f}")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

# ============================================================================
# FUNÇÕES DE RELATÓRIOS
# ============================================================================

def relatorio_top_clientes():
    """Relatório de top clientes"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "👥 TOP 10 CLIENTES")
    print("=" * 80)
    
    try:
        stats = vendas.estatisticas_vendas()
        
        if stats.get('top_clientes'):
            print("\n📊 Clientes que mais compraram:\n")
            print("-" * 60)
            print(f"{'#':<5} {'CLIENTE':<35} {'TOTAL GASTO':<20}")
            print("-" * 60)
            
            for i, (nome, total) in enumerate(stats['top_clientes'], 1):
                print(f"{i:<5} {nome[:35]:<35} R$ {total:<17.2f}")
            
            print("-" * 60)
        else:
            print("\n⚠️  Nenhum dado disponível.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

def relatorio_top_produtos():
    """Relatório de top produtos"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "📦 TOP 10 PRODUTOS")
    print("=" * 80)
    
    try:
        stats = vendas.estatisticas_vendas()
        
        if stats.get('top_produtos'):
            print("\n📊 Produtos mais vendidos:\n")
            print("-" * 60)
            print(f"{'#':<5} {'PRODUTO':<35} {'QUANTIDADE':<20}")
            print("-" * 60)
            
            for i, (nome, qtd) in enumerate(stats['top_produtos'], 1):
                print(f"{i:<5} {nome[:35]:<35} {qtd:<20}")
            
            print("-" * 60)
        else:
            print("\n⚠️  Nenhum dado disponível.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

def relatorio_faturamento():
    """Relatório de faturamento"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "💰 FATURAMENTO")
    print("=" * 80)
    
    try:
        stats = vendas.estatisticas_vendas()
        
        if stats:
            print("\n📊 Resumo financeiro:\n")
            print(f"   Total de vendas realizadas: {stats['total_vendas']}")
            print(f"   Faturamento total: R$ {stats['total_faturado']:.2f}")
            print(f"   Ticket médio: R$ {stats['ticket_medio']:.2f}")
        else:
            print("\n⚠️  Nenhum dado disponível.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

def relatorio_geral():
    """Relatório geral do sistema"""
    limpar_tela()
    print("=" * 80)
    print(" " * 25 + "📊 RESUMO GERAL")
    print("=" * 80)
    
    try:
        # Estatísticas de vendas
        stats = vendas.estatisticas_vendas()
        
        print("\n💰 VENDAS:")
        print(f"   Total de vendas: {stats.get('total_vendas', 0)}")
        print(f"   Faturamento: R$ {stats.get('total_faturado', 0):.2f}")
        print(f"   Ticket médio: R$ {stats.get('ticket_medio', 0):.2f}")
        
        # Total de clientes
        total_clientes = cliente.contar_clientes()
        print(f"\n👥 CLIENTES:")
        print(f"   Total cadastrados: {total_clientes}")
        
        # Total de produtos
        total_produtos = produto.contar_produtos()
        print(f"\n📦 PRODUTOS:")
        print(f"   Total cadastrados: {total_produtos}")
        
        print("\n" + "=" * 80)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    pausar()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        limpar_tela()
        print("\n\n" + "=" * 80)
        print(" " * 25 + "👋 SISTEMA ENCERRADO")
        print("=" * 80 + "\n")
        sys.exit(0)
