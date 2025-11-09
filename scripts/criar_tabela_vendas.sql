-- ============================================================================
-- Script para criar tabela de vendas
-- Relaciona clientes com produtos
-- ============================================================================

-- Criar tabela vendas
CREATE TABLE IF NOT EXISTS vendas (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    produto_id INTEGER NOT NULL REFERENCES produtos(id) ON DELETE CASCADE,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    valor_unitario DECIMAL(10, 2) NOT NULL CHECK (valor_unitario >= 0),
    valor_total DECIMAL(10, 2) NOT NULL CHECK (valor_total >= 0),
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observacao TEXT,
    CONSTRAINT vendas_valores_check CHECK (valor_total = quantidade * valor_unitario)
);

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_vendas_cliente ON vendas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_vendas_produto ON vendas(produto_id);
CREATE INDEX IF NOT EXISTS idx_vendas_data ON vendas(data_venda);

-- Comentários
COMMENT ON TABLE vendas IS 'Tabela de vendas - relaciona clientes com produtos';
COMMENT ON COLUMN vendas.cliente_id IS 'ID do cliente que comprou';
COMMENT ON COLUMN vendas.produto_id IS 'ID do produto vendido';
COMMENT ON COLUMN vendas.quantidade IS 'Quantidade vendida';
COMMENT ON COLUMN vendas.valor_unitario IS 'Valor unitário no momento da venda';
COMMENT ON COLUMN vendas.valor_total IS 'Valor total da venda (quantidade * valor_unitario)';
COMMENT ON COLUMN vendas.data_venda IS 'Data e hora da venda';
COMMENT ON COLUMN vendas.observacao IS 'Observações sobre a venda';

-- Inserir algumas vendas de exemplo
INSERT INTO vendas (cliente_id, produto_id, quantidade, valor_unitario, valor_total, observacao)
SELECT 
    (SELECT id FROM clientes ORDER BY RANDOM() LIMIT 1),
    (SELECT id FROM produtos ORDER BY RANDOM() LIMIT 1),
    (RANDOM() * 5 + 1)::INTEGER,
    (SELECT preco FROM produtos WHERE id = (SELECT id FROM produtos ORDER BY RANDOM() LIMIT 1)),
    ((RANDOM() * 5 + 1)::INTEGER * (SELECT preco FROM produtos WHERE id = (SELECT id FROM produtos ORDER BY RANDOM() LIMIT 1))),
    'Venda de teste'
FROM generate_series(1, 10);

-- Mostrar resultado
SELECT 
    v.id,
    c.nome as cliente,
    p.nome as produto,
    v.quantidade,
    v.valor_unitario,
    v.valor_total,
    v.data_venda
FROM vendas v
JOIN clientes c ON v.cliente_id = c.id
JOIN produtos p ON v.produto_id = p.id
ORDER BY v.data_venda DESC
LIMIT 10;

-- Estatísticas
SELECT 
    COUNT(*) as total_vendas,
    SUM(valor_total) as total_faturado,
    AVG(valor_total) as ticket_medio
FROM vendas;

