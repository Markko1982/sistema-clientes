from database import get_cursor

def main():
    with get_cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM clientes")
        total = cur.fetchone()[0]
        print(f"Total de clientes na tabela: {total}")

if __name__ == "__main__":
    main()
