"""
Funções utilitárias relacionadas a nomes de pessoas.
"""

def quebrar_nome(nome_completo: str) -> tuple[str, str]:
    """
    Separa nome completo em (nome, sobrenome).

    Regras simples:
      - 0 palavras: ("", "")
      - 1 palavra: (p, p)
      - 2+ palavras: (tudo menos a última, última)

    Exemplos:
      "Ana"            -> ("Ana", "Ana")
      "Ana Maria"      -> ("Ana", "Maria")
      "Ana Maria Silva"-> ("Ana Maria", "Silva")
    """
    partes = nome_completo.split()
    if not partes:
        return "", ""
    if len(partes) == 1:
        return partes[0], partes[0]
    sobrenome = partes[-1]
    nome = " ".join(partes[:-1])
    return nome, sobrenome
