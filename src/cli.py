import argparse
from importar_clientes_csv import importar as importar_csv
from buscar_por_sobrenome import buscar as buscar_sobrenome
from scripts.contar_clientes import main as contar_clientes

def cmd_import(args):
    """
    Importa clientes a partir de um arquivo CSV.
    Se o usuário não informar nada, usamos o arquivo padrão.
    """
    caminho = args.csv or "clientes_exemplo.csv"
    importar_csv(caminho)

def cmd_search(args):
    """
    Busca clientes pelo sobrenome.
    """
    sobrenome = args.sobrenome
    if not sobrenome:
        print("Você precisa informar um sobrenome (ex: --sobrenome Silva).")
        return
    buscar_sobrenome(sobrenome)

def cmd_count(args):
    """
    Mostra quantos clientes existem na tabela.
    """
    contar_clientes()

def build_parser():
    parser = argparse.ArgumentParser(
        prog="sistema-clientes",
        description="CLI oficial do sistema de clientes.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # subcomando: import
    p_import = sub.add_parser("import", help="Importar clientes de um CSV")
    p_import.add_argument(
        "--csv",
        help="Caminho do arquivo CSV (padrão: clientes_exemplo.csv)",
        default=None,
    )
    p_import.set_defaults(func=cmd_import)

    # subcomando: search
    p_search = sub.add_parser("search", help="Buscar clientes por sobrenome")
    p_search.add_argument(
        "--sobrenome",
        help="Sobrenome a ser buscado (ex: --sobrenome Silva)",
        required=True,
    )
    p_search.set_defaults(func=cmd_search)

    # subcomando: count
    p_count = sub.add_parser("count", help="Contar clientes na tabela")
    p_count.set_defaults(func=cmd_count)

    return parser

def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    main()
