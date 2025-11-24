#!/usr/bin/env bash
set -e

echo "=== Setup do ambiente de desenvolvimento do Sistema de Clientes ==="

# Diretório da venv fora do disco montado (no HOME)
VENV_DIR="$HOME/.venvs/novo-projeto"

# 1) Criar venv se não existir
if [ ! -d "$VENV_DIR" ] || [ ! -f "$VENV_DIR/bin/activate" ]; then
  echo "[1/5] Criando ambiente virtual em: $VENV_DIR"
  mkdir -p "$(dirname "$VENV_DIR")"
  python3 -m venv "$VENV_DIR"
else
  echo "[1/5] Ambiente virtual ($VENV_DIR) já existe e parece OK. Pulando criação."
fi

# 2) Ativar venv
echo "[2/5] Ativando ambiente virtual..."
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# 3) Instalar dependências
if [ -f "requirements.txt" ]; then
  echo "[3/5] Instalando dependências do requirements.txt..."
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "[3/5] Arquivo requirements.txt não encontrado. Pulando instalação."
fi

# 4) Subir banco PostgreSQL com docker compose
if [ -f "docker-compose.yml" ]; then
  echo "[4/5] Subindo PostgreSQL com docker compose..."
  docker compose up -d
else
  echo "[4/5] Arquivo docker-compose.yml não encontrado. Pulando Docker."
fi

# 5) Testar conexão com o banco
echo "[5/5] Testando conexão com o banco..."
set -a
if [ -f ".env" ]; then
  # shellcheck disable=SC1091
  source .env
else
  echo "AVISO: Arquivo .env não encontrado. Usando variáveis atuais do ambiente."
fi
set +a

python -m scripts.teste_db || {
  echo "ERRO: falha ao conectar no banco. Verifique .env e docker compose."
  exit 1
}

echo "=== Setup concluído com sucesso! ==="
echo "Ambiente virtual usado: $VENV_DIR"
echo "Para usar o projeto depois:"
echo "  1) Ative a venv:  source \"$VENV_DIR/bin/activate\""
echo "  2) Carregue o .env: set -a; source .env; set +a"
echo "  3) Rode o menu:    python menu.py   (ou alias menucli, se configurado)"
