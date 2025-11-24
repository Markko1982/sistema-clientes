from typing import Optional, List, Tuple, Dict
from src.database import get_cursor

Linha = Tuple[
    int,              # id
    str,              # nome
    str,              # sobrenome
    Optional[str],    # email
    Optional[str],    # telefone
    Optional[str],    # cidade
    Optional[str],    # uf
    str,              # status_cliente
    bool,             # vip
    object,           # criado_em (datetime)
    Optional[object], # data_nascimento (date)
]

def criar_cliente(
    nome: str,
    sobrenome: str,
    email: Optional[str] = None,
    telefone: Optional[str] = None,
    cidade: Optional[str] = None,
    uf: Optional[str] = None,
    status_cliente: str = "ativo",
    vip: bool = False,
) -> int:
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO clientes (nome, sobrenome, email, telefone, cidade, uf, status_cliente, vip)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (nome, sobrenome, email, telefone, cidade, uf, status_cliente, vip),
        )
        new_id = cur.fetchone()[0]
        return new_id

def _select_base(
    where: str = "",
    params: tuple = (),
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Linha]:
    sql = """
        SELECT id, nome, sobrenome, email, telefone, cidade, uf,
               status_cliente, vip, criado_em, data_nascimento
        FROM clientes
    """
    if where:
        sql += " WHERE " + where
    sql += " ORDER BY nome"

    param_list = list(params)

    if limit is not None:
        sql += " LIMIT %s"
        param_list.append(limit)

    if offset is not None:
        sql += " OFFSET %s"
        param_list.append(offset)

    with get_cursor() as cur:
        cur.execute(sql, tuple(param_list))
        return cur.fetchall()

def buscar_por_sobrenome(
    sobrenome: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Linha]:
    return _select_base("sobrenome ILIKE %s", (sobrenome,), limit, offset)

def buscar_por_uf(
    uf: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Linha]:
    return _select_base("uf = %s", (uf.upper(),), limit, offset)

def buscar_por_cidade(
    cidade: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Linha]:
    like = f"%{cidade}%"
    return _select_base("cidade ILIKE %s", (like,), limit, offset)

def buscar_por_status(
    status_cliente: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Linha]:
    return _select_base("status_cliente = %s", (status_cliente,), limit, offset)

def buscar_vips(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Linha]:
    return _select_base("vip = TRUE", (), limit, offset)

def buscar_aniversariantes_mes(
    mes: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Linha]:
    return _select_base(
        "data_nascimento IS NOT NULL AND EXTRACT(MONTH FROM data_nascimento) = %s",
        (mes,),
        limit,
        offset,
    )

def buscar_aniversariantes_hoje(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Linha]:
    where = (
        "data_nascimento IS NOT NULL "
        "AND EXTRACT(MONTH FROM data_nascimento) = EXTRACT(MONTH FROM CURRENT_DATE) "
        "AND EXTRACT(DAY   FROM data_nascimento) = EXTRACT(DAY   FROM CURRENT_DATE)"
    )
    return _select_base(where, (), limit, offset)

def contar_clientes() -> int:
    with get_cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM clientes")
        total = cur.fetchone()[0]
        return total

def estatisticas_clientes() -> Dict[str, int]:
    stats: Dict[str, int] = {}
    with get_cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM clientes")
        stats["total"] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM clientes WHERE status_cliente = 'ativo'")
        stats["ativos"] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM clientes WHERE status_cliente = 'inativo'")
        stats["inativos"] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM clientes WHERE vip = TRUE")
        stats["vips"] = cur.fetchone()[0]

    return stats

def ranking_ufs(limit: Optional[int] = None) -> List[Tuple[str, int]]:
    """
    Retorna lista (uf, quantidade) ordenada da maior para a menor quantidade de clientes.
    """
    sql = """
        SELECT uf, COUNT(*) AS qtde
        FROM clientes
        WHERE uf IS NOT NULL
        GROUP BY uf
        ORDER BY qtde DESC
    """
    params: tuple = ()
    if limit is not None:
        sql += " LIMIT %s"
        params = (limit,)

    with get_cursor() as cur:
        cur.execute(sql, params)
        return [(uf, qtde) for (uf, qtde) in cur.fetchall()]

def ranking_cidades_por_uf(uf: str, limit: Optional[int] = None) -> List[Tuple[str, int]]:
    """
    Retorna lista (cidade, quantidade) para uma UF específica.
    """
    sql = """
        SELECT cidade, COUNT(*) AS qtde
        FROM clientes
        WHERE uf = %s
          AND cidade IS NOT NULL
        GROUP BY cidade
        ORDER BY qtde DESC, cidade ASC
    """
    params: tuple = (uf.upper(),)
    if limit is not None:
        sql += " LIMIT %s"
        params = params + (limit,)

    with get_cursor() as cur:
        cur.execute(sql, params)
        return [(cidade, qtde) for (cidade, qtde) in cur.fetchall()]
