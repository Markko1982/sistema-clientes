import math
from database import get_cursor

def main():
    print("Marcando status e VIP aleatoriamente...")
    with get_cursor() as cur:
        # Zera todo mundo para um estado conhecido
        cur.execute("UPDATE clientes SET status_cliente = 'ativo', vip = FALSE")

        # Quantidade total
        cur.execute("SELECT COUNT(*) FROM clientes")
        total = cur.fetchone()[0] or 0
        print(f"Total de clientes atuais: {total}")

        if total == 0:
            print("Não há clientes para atualizar.")
            return

        qtd_inativos = math.ceil(total * 0.10)  # 10% inativos
        qtd_vips = math.ceil(total * 0.05)      # 5% VIP

        print(f"Marcando ~{qtd_inativos} como inativos e ~{qtd_vips} como VIP...")

        # Escolhe alguns aleatoriamente para inativo
        cur.execute(
            """
            UPDATE clientes
               SET status_cliente = 'inativo'
             WHERE id IN (
                SELECT id FROM clientes ORDER BY random() LIMIT %s
             )
            """,
            (qtd_inativos,),
        )

        # Escolhe alguns como VIP (podem ser ativos ou inativos)
        cur.execute(
            """
            UPDATE clientes
               SET vip = TRUE
             WHERE id IN (
                SELECT id FROM clientes ORDER BY random() LIMIT %s
             )
            """,
            (qtd_vips,),
        )

    print("Atualização concluída.")

if __name__ == "__main__":
    main()
