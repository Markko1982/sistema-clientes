import os
import psycopg2
from contextlib import contextmanager

def get_connection():
    """
    Abre uma conexão com o PostgreSQL usando as variáveis de ambiente.
    Isso evita deixar usuário/senha fixos no código.
    """
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5433"),
        dbname=os.getenv("PGDATABASE", "clientes"),
        user=os.getenv("PGUSER", "app"),
        password=os.getenv("PGPASSWORD", "app"),
    )

@contextmanager
def get_cursor():
    """
    Entrega um cursor já dentro de uma transação.
    No final, faz commit automático.
    Se der erro, dá rollback.

    Uso típico:
        from database import get_cursor

        with get_cursor() as cur:
            cur.execute("SELECT 1")
            print(cur.fetchone())
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
