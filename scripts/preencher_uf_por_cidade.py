from database import get_cursor
from src.localidades import CIDADE_UF

def main():
    print("Preenchendo UF com base na cidade (usando mapa CIDADE_UF)...")
    with get_cursor() as cur:
        total_atualizados = 0
        for cidade, uf in CIDADE_UF.items():
            print(f"- Atualizando cidade='{cidade}' para uf='{uf}'...")
            cur.execute(
                """
                UPDATE clientes
                   SET uf = %s
                 WHERE cidade = %s
                   AND (uf IS NULL OR uf = '')
                """,
                (uf, cidade),
            )
            print(f"  -> {cur.rowcount} registros atualizados.")
            total_atualizados += cur.rowcount

    print(f"Concluído. Total de registros atualizados: {total_atualizados}.")

if __name__ == "__main__":
    main()
