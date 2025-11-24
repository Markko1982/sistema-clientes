CREATE TABLE IF NOT EXISTS clientes (
  id SERIAL PRIMARY KEY,
  nome TEXT NOT NULL,
  sobrenome TEXT NOT NULL,
  email TEXT UNIQUE,
  telefone TEXT,
  cidade TEXT,
  uf CHAR(2),
  status_cliente VARCHAR(20) NOT NULL DEFAULT 'ativo',
  vip BOOLEAN NOT NULL DEFAULT FALSE,
  data_nascimento DATE,
  criado_em TIMESTAMP DEFAULT NOW()
);

-- Garante colunas novas mesmo se a tabela já existia antes
ALTER TABLE clientes
  ADD COLUMN IF NOT EXISTS status_cliente VARCHAR(20) NOT NULL DEFAULT 'ativo';

ALTER TABLE clientes
  ADD COLUMN IF NOT EXISTS vip BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE clientes
  ADD COLUMN IF NOT EXISTS data_nascimento DATE;

-- Índices para buscas rápidas
CREATE INDEX IF NOT EXISTS idx_clientes_sobrenome ON clientes (sobrenome);
CREATE INDEX IF NOT EXISTS idx_clientes_uf ON clientes (uf);
CREATE INDEX IF NOT EXISTS idx_clientes_cidade ON clientes (cidade);
CREATE INDEX IF NOT EXISTS idx_clientes_status ON clientes (status_cliente);
CREATE INDEX IF NOT EXISTS idx_clientes_vip ON clientes (vip);
CREATE INDEX IF NOT EXISTS idx_clientes_data_nascimento ON clientes (data_nascimento);
