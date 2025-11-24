import sys
import csv
from pathlib import Path

from database import get_cursor
from src.utils_nomes import quebrar_nome
from src.localidades import CIDADE_UF

ARQUIVO_PADRAO = "clientes_exemplo.csv"

def detectar_dialeto(caminho: Path) -> csv.Dialect:
    """
    Tenta descobrir automaticamente o separador do CSV (vírgula, ponto e vírgula, etc).
    """
    amostra = caminho.read_text(encoding="utf-8", errors="ignore")[:4096]
    return csv.Sniffer().sniff(amostra)

def normalizar_cabecalhos(fieldnames):
    """
    Recebe a lista de colunas do CSV (fieldnames) e devolve
    um dicionário que mapeia nomes normalizados -> nome original.
    Ex.: ["Nome ", "SOBRENOME"] vira {"nome": "Nome ", "sobrenome": "SOBRENOME"}
    """
    mapeado = {}
    for nome in fieldnames:
        if nome is None:
            continue
        chave = nome.strip().lower()
        mapeado[chave] = nome
    return mapeado

def importar(arquivo: str):
    caminho = Path(arquivo)
    if not caminho.exists():
        print(f"Arquivo não encontrado: {caminho}")
        sys.exit(1)

    print(f"Iniciando importação a partir de: {caminho}")

    dialeto = detectar_dialeto(caminho)

    ok, pulados = 0, 0

    with caminho.open(newline="", encoding="utf-8") as f, get_cursor() as cur:
        reader = csv.DictReader(f, dialect=dialeto)

        if not reader.fieldnames:
            print("Não foi possível detectar cabeçalhos no CSV.")
            sys.exit(1)

        cabecalhos = normalizar_cabecalhos(reader.fieldnames)
        print("Cabeçalhos detectados (normalizados -> original):")
        for k, v in cabecalhos.items():
            print(f"  {k} -> {v}")
        print()

        col_nome = cabecalhos.get("nome")
        col_sobrenome = cabecalhos.get("sobrenome")
        col_email = cabecalhos.get("email")
        col_telefone = cabecalhos.get("telefone")
        col_cidade = cabecalhos.get("cidade")
        col_uf = cabecalhos.get("uf")

        if not col_nome:
            print("ERRO: Não encontrei coluna de 'nome' no CSV.")
            sys.exit(1)

        if not col_sobrenome:
            print("AVISO: Não encontrei coluna de 'sobrenome'.")
            print("       Vou tentar derivar o sobrenome a partir do nome completo (última palavra).")
            print()

        for linha in reader:
            nome_completo = (linha.get(col_nome) or "").strip()

            # Decide como obter nome e sobrenome
            if col_sobrenome:
                sobrenome_csv = (linha.get(col_sobrenome) or "").strip()
                nome, sobrenome = nome_completo, sobrenome_csv
            else:
                nome, sobrenome = quebrar_nome(nome_completo)

            email = (linha.get(col_email) or "").strip() or None
            telefone = (linha.get(col_telefone) or "").strip() or None
            cidade = (linha.get(col_cidade) or "").strip() or None

            # UF: tenta pegar do CSV; se não tiver, tenta derivar pela cidade (CIDADE_UF)
            raw_uf = ""
            if col_uf:
                raw_uf = (linha.get(col_uf) or "").strip().upper()[:2]
            uf = raw_uf or (CIDADE_UF.get(cidade) if cidade else None)

            if not nome or not sobrenome:
                print(f"[LINHA {reader.line_num}] Nome ou sobrenome vazio após processamento. Pulando. Valor original: '{nome_completo}'")
                pulados += 1
                continue

            try:
                cur.execute(
                    """
                    INSERT INTO clientes (nome, sobrenome, email, telefone, cidade, uf)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (email) DO NOTHING
                    """,
                    (nome, sobrenome, email, telefone, cidade, uf),
                )
                ok += 1
            except Exception as e:
                pulados += 1
                print(f"[LINHA {reader.line_num}] Erro ao inserir: {e}")

    print(f"Importação concluída. Sucesso: {ok} | Pulados: {pulados}")

def main():
    arquivo = sys.argv[1] if len(sys.argv) > 1 else ARQUIVO_PADRAO
    importar(arquivo)

if __name__ == "__main__":
    main()
