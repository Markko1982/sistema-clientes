# Sistema de Clientes (CLI + PostgreSQL)

Projeto de estudo para simular um mini-CRM de clientes em ambiente de linha de comando,
usando **Python 3.12**, **PostgreSQL** e **Docker**.

O sistema suporta milhões de clientes com dados realistas (Brasil inteiro, vários estados e cidades,
clientes VIP, ativos/inativos, datas de nascimento etc.).

---

## Visão Geral

Funcionalidades principais:

- Importar clientes a partir de arquivos CSV.
- Gerar massas grandes de dados fake (milhares ou milhões de clientes).
- Buscar clientes por:
    - sobrenome
    - estado (UF)
    - cidade
    - status (ativo / inativo)
    - VIP
- Listar aniversariantes:
    - do mês
    - do dia atual
- Estatísticas gerais:
    - total de clientes
    - ativos / inativos
    - VIPs
    - porcentagens por tipo
- Relatórios de ranking:
    - ranking de estados (clientes por UF)
    - ranking de cidades por UF
- Paginação nas listagens:
    - próxima página (N)
    - página anterior (P)
    - ir direto para página X (digitando o número)
    - sair com ENTER
    - exibição do tempo da consulta (ms), para ter noção de performance.

---

## Estrutura do Projeto

    .
    ├── docker-compose.yml           # Banco PostgreSQL via Docker
    ├── .env.example                 # Exemplo de configuração de ambiente
    ├── .env                         # Configurações locais (não versionar em produção)
    ├── requirements.txt             # Dependências Python
    ├── ALIASES.md                   # Documentação dos aliases de terminal
    ├── README.md                    # Este arquivo :)
    ├── menu.py                      # Menu principal (CLI interativa)
    ├── src/
    │   ├── __init__.py
    │   ├── cli.py                   # CLI simples para contagem de clientes etc.
    │   ├── clientes.py              # Funções de negócio (buscas, estatísticas, rankings)
    │   ├── database.py              # Conexão com PostgreSQL
    │   ├── localidades.py           # Mapa de cidades/UF do Brasil
    │   └── utils_nomes.py           # Funções auxiliares para tratar nomes
    ├── scripts/
    │   ├── gerar_clientes_fake.py   # Gera clientes fake em massa
    │   ├── importar_clientes_csv.py # Importa clientes a partir de CSV
    │   ├── preencher_uf_por_cidade.py
    │   ├── teste_db.py              # Teste rápido de conexão com banco
    │   └── setup_dev.sh             # Script de setup do ambiente (opcional)
    └── tests/
        └── test_utils_nomes.py      # Testes de unidade (pytest)

---

## Pré-requisitos

- **Python 3.12+**
- **Docker** e **docker compose**
- Git (para clonar o repositório)
- Sistema testado principalmente em **Linux** (Ubuntu/Debian-like)

---

## 1. Clonar o Repositório

    git clone https://github.com/SEU_USUARIO/sistema-clientes.git
    cd sistema-clientes

(Altere `SEU_USUARIO` para o usuário correto do GitHub.)

---

## 2. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo:

    cp .env.example .env

Edite o `.env` se necessário (nome do banco, usuário, senha, host, porta etc.).

Para carregar as variáveis no shell atual:

    set -a; source .env; set +a

> Em desenvolvimento isso é suficiente.  
> Em produção, o ideal é configurar variáveis de ambiente direto no sistema/servidor.

---

## 3. Subir o PostgreSQL com Docker

    docker compose up -d

Isso cria:

- um container com PostgreSQL;
- um volume para persistir os dados do banco.

Verifique se o container está no ar:

    docker ps

---

## 4. Criar Ambiente Virtual e Instalar Dependências

### Opção A – Manual

    python3 -m venv .venv
    source .venv/bin/activate

    pip install --upgrade pip
    pip install -r requirements.txt

### Opção B – Script de Setup (conveniência)

Você pode usar o script opcional `scripts/setup_dev.sh`:

    bash scripts/setup_dev.sh

Ele faz:

1. Cria a venv `.venv` (se não existir).
2. Ativa a venv.
3. Instala dependências do `requirements.txt`.
4. Sobe o Postgres com `docker compose up -d`.
5. Testa a conexão com o banco (`python -m scripts.teste_db`).

---

## 5. Testar Conexão com o Banco

Com a venv ativa e o `.env` carregado:

    source .venv/bin/activate
    set -a; source .env; set +a
    python -m scripts.teste_db

Saída esperada (exemplo):

    Testando conexão com o banco...
    Conexão OK!
    Versão do PostgreSQL: PostgreSQL 16.x (...)

Se der erro, verifique:

- se o container do Postgres está rodando (`docker ps`);
- se as configurações do `.env` (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME etc.) estão corretas.

---

## 6. Rodar o Menu Interativo

Com venv ativa e `.env` carregado:

    python menu.py

Se você configurou aliases (ver seção mais abaixo), também pode usar:

    menucli

Exemplo de menu:

    === MENU SISTEMA CLIENTES ===
    (Clientes cadastrados: 123456)
    1) Importar clientes de CSV
    2) Buscar clientes por sobrenome
    3) Buscar clientes por estado (UF)
    4) Buscar clientes por cidade
    5) Listar clientes VIP
    6) Listar clientes inativos
    7) Listar clientes ativos
    8) Ver estatísticas
    9) Listar aniversariantes de um mês
    10) Listar aniversariantes de hoje
    11) Gerar clientes FAKE de teste
    12) Ver ranking de estados (clientes por UF)
    13) Ver ranking de cidades de uma UF
    0) Sair

---

## 7. Gerar Massa de Dados Fake

Para popular o banco com muitos clientes (por exemplo, 100.000):

    source .venv/bin/activate
    set -a; source .env; set +a
    python -m scripts.gerar_clientes_fake 100000

O gerador:

- usa uma lista de cidades/UF do Brasil (capitais + cidades grandes e médias/menores);
- garante pelo menos 1 cliente por cidade (quando a quantidade pedida é maior que o número de cidades);
- distribui status (ativo/inativo) e flag VIP com probabilidades configuradas.

Depois disso, as opções de:

- estatísticas,
- buscas por UF/cidade,
- ranking de estados/cidades,

passam a refletir um cenário bem mais realista.

---

## 8. Paginação e Navegação

Nas listagens (busca por sobrenome, UF, cidade, VIP, ativos, inativos, aniversariantes etc.):

- o sistema pergunta quantos registros por página (default = 20);
- mostra qual página você está;
- exibe o tempo da consulta em milissegundos.

Comandos aceitos na paginação:

- `N` ou `n` – próxima página
- `P` ou `p` – página anterior
- um número (ex.: `3`) – ir direto para a página 3
- `ENTER` – sair da listagem e voltar ao menu

---

## 9. Relatórios de Ranking

O sistema possui relatórios simples de “BI”:

- **Ranking de estados (clientes por UF)**  
  Opção 12 do menu.

- **Ranking de cidades de uma UF**  
  Opção 13 do menu.

Em ambos os casos o sistema pergunta quantos itens você quer ver (ex.: top 10).

---

## 10. Aliases de Terminal (Atalhos)

Para facilitar o dia a dia, podem ser criados aliases no shell (por exemplo,
em `~/.bashrc` ou `~/.zshrc`).  
A documentação dos aliases utilizados neste projeto está em:

- `ALIASES.md`

Exemplos de aliases comuns (podem variar conforme sua configuração local):

- `vproj` – entrar rapidamente no diretório do projeto e ativar a venv.
- `menucli` – executar o menu `menu.py`.
- outros aliases para comandos frequentes podem ser adicionados conforme necessidade.

> Os aliases são uma conveniência local de desenvolvimento, não fazem parte da
> implantação em produção.

---

## 11. Rodar Testes

O projeto usa **pytest** para testes unitários.

Com a venv ativa:

    pytest

Saída esperada (exemplo):

    collected 6 items
    tests/test_utils_nomes.py ......   [100%]

---

## 12. Roadmap / Próximos Passos

Este projeto atualmente é a **versão CLI (v1.0)** do Sistema de Clientes.

Possíveis evoluções:

- **v2.0 – API Web (FastAPI)**  
    - Expor operações de busca, estatísticas e rankings via HTTP.
    - Criar endpoints como `/clientes`, `/estatisticas`, `/ranking/ufs`, etc.

- **v3.0 – Interface Web**  
    - Criar uma interface web (front-end) que consuma a API.
    - Telas para listagem de clientes, filtros, estatísticas, dashboards simples.

Enquanto isso, a versão CLI já serve como:

- laboratório de SQL com PostgreSQL;
- exemplo de organização de projeto Python (src/scripts/tests);
- ferramenta de linha de comando para brincar com milhões de registros.

---
