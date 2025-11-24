import sys
from database import get_cursor

def buscar(sobrenome: str):
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT id, nome, sobrenome, email, telefone, cidade, uf, criado_em
            FROM clientes
            WHERE sobrenome ILIKE %s
            ORDER BY nome
            """,
            (sobrenome,),
        )
        resultados = cur.fetchall()

    if not resultados:
        print(f"Nenhum cliente encontrado com sobrenome parecido com: {sobrenome}")
        return

    print(f"Clientes encontrados para sobrenome ~ {sobrenome}:")
    for r in resultados:
        id_, nome, sob, email, telefone, cidade, uf, criado_em = r
        print(f"- [{id_}] {nome} {sob} | email={email} | tel={telefone} | {cidade}-{uf} | criado_em={criado_em}")

def main():
    if len(sys.argv) > 1:
        sobrenome = sys.argv[1]
    else:
        sobrenome = input("Digite o sobrenome para busca: ").strip()

    if not sobrenome:
        print("Sobrenome não pode ser vazio.")
        sys.exit(1)

    buscar(sobrenome)

if __name__ == "__main__":
    main()
