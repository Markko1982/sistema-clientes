import time

from importar_clientes_csv import importar
from src.clientes import (
    buscar_por_sobrenome,
    buscar_por_uf,
    buscar_por_cidade,
    buscar_vips,
    buscar_por_status,
    buscar_aniversariantes_mes,
    buscar_aniversariantes_hoje,
    estatisticas_clientes,
    contar_clientes,
    ranking_ufs,
    ranking_cidades_por_uf,
)
from scripts.gerar_clientes_fake import gerar_clientes as gerar_clientes_fake
from src.localidades import UFS, CIDADES

def imprimir_clientes(linhas):
    if not linhas:
        print("Nenhum cliente encontrado.")
        return
    for r in linhas:
        (id_, nome, sobrenome, email, telefone, cidade, uf,
         status_cliente, vip, criado_em, data_nascimento) = r
        flag_vip = " [VIP]" if vip else ""
        nasc_str = data_nascimento.isoformat() if data_nascimento else "?"
        print(
            f"- [{id_}] {nome} {sobrenome}{flag_vip} | "
            f"email={email} | tel={telefone} | {cidade}-{uf} | "
            f"status={status_cliente} | nasc={nasc_str} | criado_em={criado_em}"
        )

def perguntar_por_pagina(mensagem: str, default: int = 20) -> int:
    texto = input(mensagem).strip()
    if not texto:
        return default
    try:
        valor = int(texto)
        if valor <= 0:
            print(f"Valor deve ser maior que zero. Usando {default}.")
            return default
        return valor
    except ValueError:
        print(f"Valor inválido. Usando {default}.")
        return default

def listar_paginado(descricao: str, func_busca, *args):
    """
    Paginação para qualquer função de busca que aceite limit e offset.

    Comandos:
      - N ou n  -> próxima página
      - P ou p  -> página anterior
      - número  -> ir direto para a página X (ex: 3)
      - ENTER   -> sair da paginação
    """
    por_pagina = perguntar_por_pagina("Quantos registros por página? (ENTER = 20): ", default=20)
    pagina = 0  # índice interno (0 = primeira página)

    while True:
        offset = pagina * por_pagina

        inicio = time.perf_counter()
        linhas = func_busca(*args, limit=por_pagina, offset=offset)
        fim = time.perf_counter()
        duracao = (fim - inicio) * 1000  # ms

        if not linhas:
            if pagina == 0:
                print("Nenhum resultado encontrado.")
                break
            else:
                print("Não há registros nessa página. Voltando para a última página disponível.")
                pagina -= 1
                if pagina < 0:
                    pagina = 0
                continue

        numero_pagina = pagina + 1
        print(f"\n--- {descricao} | página {numero_pagina} ---")
        imprimir_clientes(linhas)
        print(f"\nConsulta retornou {len(linhas)} registros em {duracao:.1f} ms.")

        comando = input(
            f"\n[Você está na página {numero_pagina}] "
            "Digite N=próxima, P=anterior, número da página ou ENTER para voltar ao menu: "
        ).strip()

        if not comando:
            break

        if comando.isdigit():
            alvo = int(comando)
            if alvo <= 0:
                print("Número de página deve ser >= 1.")
            else:
                pagina = alvo - 1
            continue

        primeira_letra = comando[0].lower()
        if primeira_letra == "n":
            pagina += 1
            continue
        elif primeira_letra == "p":
            if pagina == 0:
                print("Você já está na primeira página.")
            else:
                pagina -= 1
            continue
        else:
            break

def opcao_importar():
    caminho = input("Informe o caminho do arquivo CSV (ENTER para usar clientes_exemplo.csv): ").strip()
    if not caminho:
        caminho = "clientes_exemplo.csv"
    importar(caminho)

def opcao_buscar_sobrenome():
    sobrenome = input("Digite o sobrenome para busca: ").strip()
    if not sobrenome:
        print("Sobrenome não pode ser vazio.")
        return
    listar_paginado(f"Clientes com sobrenome '{sobrenome}'", buscar_por_sobrenome, sobrenome)

def opcao_buscar_estado():
    print("\nUFs disponíveis:", ", ".join(UFS))
    uf = input("Digite a UF (ex: SP): ").strip().upper()
    if len(uf) != 2:
        print("UF deve ter 2 letras.")
        return
    if uf not in UFS:
        print("UF não está na lista de UFs conhecidas.")
        return
    listar_paginado(f"Clientes da UF {uf}", buscar_por_uf, uf)

def opcao_buscar_cidade():
    print("\nAlgumas cidades conhecidas (exemplos):")
    # mostra as cidades em ordem alfabética, mas limita a, digamos, 40 para não virar um livro
    for cidade in sorted(CIDADES)[:40]:
        print(" -", cidade)
    texto = input("\nDigite a cidade (ou parte do nome): ").strip()
    if not texto:
        print("Cidade não pode ser vazia.")
        return
    listar_paginado(f"Clientes da cidade contendo '{texto}'", buscar_por_cidade, texto)

def opcao_buscar_vips():
    listar_paginado("Clientes VIP", buscar_vips)

def opcao_buscar_inativos():
    listar_paginado("Clientes INATIVOS", buscar_por_status, "inativo")

def opcao_buscar_ativos():
    listar_paginado("Clientes ATIVOS", buscar_por_status, "ativo")

def opcao_estatisticas():
    stats = estatisticas_clientes()
    total = stats.get("total", 0)
    ativos = stats.get("ativos", 0)
    inativos = stats.get("inativos", 0)
    vips = stats.get("vips", 0)

    def pct(valor: int) -> float:
        return (valor * 100.0 / total) if total > 0 else 0.0

    print("\n=== ESTATÍSTICAS DE CLIENTES ===")
    print(f"Total:     {total}")
    print(f"Ativos:    {ativos:7d}  ({pct(ativos):6.2f} %)")
    print(f"Inativos:  {inativos:7d}  ({pct(inativos):6.2f} %)")
    print(f"VIPs:      {vips:7d}  ({pct(vips):6.2f} %)")
    print()

def opcao_aniversariantes_mes():
    mes_txt = input("Digite o mês (1-12): ").strip()
    if not mes_txt:
        print("Mês não pode ser vazio.")
        return
    try:
        mes = int(mes_txt)
    except ValueError:
        print("Mês inválido.")
        return
    if not 1 <= mes <= 12:
        print("Mês deve estar entre 1 e 12.")
        return
    listar_paginado(f"Aniversariantes do mês {mes}", buscar_aniversariantes_mes, mes)

def opcao_aniversariantes_hoje():
    listar_paginado("Aniversariantes de hoje", buscar_aniversariantes_hoje)

def opcao_gerar_clientes_fake():
    txt = input("Quantos clientes FAKE deseja gerar? (ex: 10000) ").strip()
    if not txt:
        print("Quantidade não pode ser vazia.")
        return
    try:
        qtd = int(txt)
    except ValueError:
        print("Valor inválido.")
        return
    gerar_clientes_fake(qtd)

def opcao_ranking_ufs():
    limite = perguntar_por_pagina("Quantos estados no ranking? (ENTER = 10): ", default=10)
    dados = ranking_ufs(limit=limite)
    if not dados:
        print("Nenhum dado para exibir.")
        return
    print("\n=== RANKING DE ESTADOS POR QUANTIDADE DE CLIENTES ===")
    print("Pos | UF | Qtde Clientes")
    print("---------------------------")
    for i, (uf, qtd) in enumerate(dados, start=1):
        print(f"{i:3d} | {uf:2s} | {qtd:10d}")

def opcao_ranking_cidades_por_uf():
    print("\nUFs disponíveis:", ", ".join(UFS))
    uf = input("Digite a UF para ver o ranking de cidades (ex: RS): ").strip().upper()
    if len(uf) != 2 or uf not in UFS:
        print("UF inválida ou desconhecida.")
        return
    limite = perguntar_por_pagina("Quantas cidades no ranking? (ENTER = 10): ", default=10)
    dados = ranking_cidades_por_uf(uf, limit=limite)
    if not dados:
        print("Nenhuma cidade com clientes para essa UF.")
        return
    print(f"\n=== RANKING DE CIDADES DA UF {uf} ===")
    print("Pos | Cidade                 | Qtde Clientes")
    print("-------------------------------------------")
    for i, (cidade, qtd) in enumerate(dados, start=1):
        print(f"{i:3d} | {cidade:21s} | {qtd:10d}")

def main():
    while True:
        total = contar_clientes()
        print("\n=== MENU SISTEMA CLIENTES ===")
        print(f"(Clientes cadastrados: {total})")
        print("1) Importar clientes de CSV")
        print("2) Buscar clientes por sobrenome")
        print("3) Buscar clientes por estado (UF)")
        print("4) Buscar clientes por cidade")
        print("5) Listar clientes VIP")
        print("6) Listar clientes inativos")
        print("7) Listar clientes ativos")
        print("8) Ver estatísticas")
        print("9) Listar aniversariantes de um mês")
        print("10) Listar aniversariantes de hoje")
        print("11) Gerar clientes FAKE de teste")
        print("12) Ver ranking de estados (clientes por UF)")
        print("13) Ver ranking de cidades de uma UF")
        print("0) Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            opcao_importar()
        elif escolha == "2":
            opcao_buscar_sobrenome()
        elif escolha == "3":
            opcao_buscar_estado()
        elif escolha == "4":
            opcao_buscar_cidade()
        elif escolha == "5":
            opcao_buscar_vips()
        elif escolha == "6":
            opcao_buscar_inativos()
        elif escolha == "7":
            opcao_buscar_ativos()
        elif escolha == "8":
            opcao_estatisticas()
        elif escolha == "9":
            opcao_aniversariantes_mes()
        elif escolha == "10":
            opcao_aniversariantes_hoje()
        elif escolha == "11":
            opcao_gerar_clientes_fake()
        elif escolha == "12":
            opcao_ranking_ufs()
        elif escolha == "13":
            opcao_ranking_cidades_por_uf()
        elif escolha == "0":
            print("Saindo do menu.")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
