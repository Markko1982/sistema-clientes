import pytest
from src.utils_nomes import quebrar_nome

@pytest.mark.parametrize(
    "entrada,esperado_nome,esperado_sobrenome",
    [
        ("", "", ""),
        ("Ana", "Ana", "Ana"),
        ("Ana Maria", "Ana", "Maria"),
        ("Ana Maria Silva", "Ana Maria", "Silva"),
        (" João  Souza  ", "João", "Souza"),
        ("JOSE", "JOSE", "JOSE"),
    ],
)
def test_quebrar_nome_casos_basicos(entrada, esperado_nome, esperado_sobrenome):
    nome, sobrenome = quebrar_nome(entrada)
    assert nome == esperado_nome
    assert sobrenome == esperado_sobrenome
