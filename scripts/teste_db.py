from database import get_cursor

def main():
    print("Testando conexão com o banco...")
    with get_cursor() as cur:
        cur.execute("SELECT version()")
        versao = cur.fetchone()[0]
        print("Conexão OK!")
        print("Versão do PostgreSQL:", versao)

if __name__ == "__main__":
    main()
