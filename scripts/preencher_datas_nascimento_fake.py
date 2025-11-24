from database import get_cursor

def main():
    print("Preenchendo datas de nascimento aleatórias para clientes sem data...")
    with get_cursor() as cur:
        # Gera datas entre 1950-01-01 e ~2010 (aprox. 60 anos de janela)
        cur.execute(
            """
            UPDATE clientes
               SET data_nascimento =
                     DATE '1950-01-01'
                     + (trunc(random() * 21900)::int)
             WHERE data_nascimento IS NULL
            """
        )
        print(f"Registros atualizados: {cur.rowcount}")

    print("Concluído.")

if __name__ == "__main__":
    main()
