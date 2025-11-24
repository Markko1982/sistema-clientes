import sys
import random
import uuid
from datetime import date, timedelta

from database import get_cursor
from src.localidades import CIDADE_UF, CIDADES

# Alguns nomes e sobrenomes para combinar
PRIMEIROS_NOMES = [
    "Ana", "Bruno", "Carlos", "Daniela", "Eduardo",
    "Fernanda", "Gabriel", "Helena", "Igor", "João",
    "Juliana", "Lucas", "Mariana", "Nicolas", "Patrícia",
    "Rafael", "Renata", "Samuel", "Tatiana", "Vinícius",
]

SOBRENOMES = [
    "Silva", "Souza", "Almeida", "Lima", "Oliveira",
    "Rodrigues", "Pereira", "Costa", "Santos", "Gomes",
]

def data_nascimento_aleatoria(
    ano_inicio: int = 1950,
    ano_fim: int = 2010,
) -> date:
    """
    Gera uma data de nascimento aleatória entre ano_inicio e ano_fim.
    """
    inicio = date(ano_inicio, 1, 1)
    fim = date(ano_fim, 12, 31)
    delta_dias = (fim - inicio).days
    return inicio + timedelta(days=random.randint(0, delta_dias))

def gerar_telefone() -> str:
    """
    Gera um telefone simples no formato 11 dígitos.
    (Não é real, é só pra teste.)
    """
    ddds = ["11", "12", "13", "19", "21", "24", "27", "31", "41", "47", "51", "61", "62", "71", "79", "81", "82", "85", "91", "95", "98"]
    ddd = random.choice(ddds)
    numero = random.randint(900000000, 999999999)
    return f"{ddd}{numero}"

def salvar_batch(batch):
    """
    Recebe uma lista de tuplas com dados dos clientes e salva tudo de uma vez.
    """
    if not batch:
        return
    with get_cursor() as cur:
        cur.executemany(
            """
            INSERT INTO clientes (
                nome, sobrenome, email, telefone,
                cidade, uf, status_cliente, vip, data_nascimento
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING
            """,
            batch,
        )

def gerar_clientes(qtd: int):
    """
    Gera 'qtd' clientes fake e insere no banco em lotes.

    Estratégia:
      - Se qtd >= número de cidades, garante pelo menos 1 cliente em cada cidade.
      - O restante é distribuído de forma aleatória.
    """
    if qtd <= 0:
        print("Quantidade deve ser maior que zero.")
        return

    print(f"Iniciando geração de {qtd} clientes fake...")
    BATCH_SIZE = 5000
    batch = []
    gerados = 0

    # Garante pelo menos 1 cliente em cada cidade, se possível
    cidades = list(CIDADES)
    random.shuffle(cidades)

    usados = 0
    if qtd >= len(cidades):
        for cidade in cidades:
            uf = CIDADE_UF[cidade]
            primeiro = random.choice(PRIMEIROS_NOMES)
            sobrenome = random.choice(SOBRENOMES)
            sufixo = uuid.uuid4().hex[:8]
            email = f"{primeiro.lower()}.{sobrenome.lower()}.{sufixo}@fake.com"
            telefone = gerar_telefone()
            status_cliente = "ativo" if random.random() < 0.8 else "inativo"
            vip = random.random() < 0.05
            data_nasc = data_nascimento_aleatoria()

            batch.append(
                (
                    primeiro,
                    sobrenome,
                    email,
                    telefone,
                    cidade,
                    uf,
                    status_cliente,
                    vip,
                    data_nasc,
                )
            )
            usados += 1

            if len(batch) >= BATCH_SIZE:
                salvar_batch(batch)
                gerados += len(batch)
                print(f"... {gerados} clientes preparados (lote salvo).")
                batch.clear()

    restante = qtd - usados

    # Gera o restante aleatório
    for _ in range(restante):
        cidade = random.choice(CIDADES)
        uf = CIDADE_UF[cidade]
        primeiro = random.choice(PRIMEIROS_NOMES)
        sobrenome = random.choice(SOBRENOMES)
        sufixo = uuid.uuid4().hex[:8]
        email = f"{primeiro.lower()}.{sobrenome.lower()}.{sufixo}@fake.com"
        telefone = gerar_telefone()
        status_cliente = "ativo" if random.random() < 0.8 else "inativo"
        vip = random.random() < 0.05
        data_nasc = data_nascimento_aleatoria()

        batch.append(
            (
                primeiro,
                sobrenome,
                email,
                telefone,
                cidade,
                uf,
                status_cliente,
                vip,
                data_nasc,
            )
        )

        if len(batch) >= BATCH_SIZE:
            salvar_batch(batch)
            gerados += len(batch)
            print(f"... {gerados} clientes preparados (lote salvo).")
            batch.clear()

    # salva o último lote
    if batch:
        salvar_batch(batch)
        gerados += len(batch)
        print(f"... {gerados} clientes preparados (último lote salvo).")

    print("Geração concluída.")

def main():
    if len(sys.argv) > 1:
        try:
            qtd = int(sys.argv[1])
        except ValueError:
            print("Uso: python -m scripts.gerar_clientes_fake <quantidade>")
            sys.exit(1)
    else:
        txt = input("Quantos clientes fake deseja gerar? ").strip()
        try:
            qtd = int(txt)
        except ValueError:
            print("Valor inválido.")
            sys.exit(1)

    gerar_clientes(qtd)

if __name__ == "__main__":
    main()
