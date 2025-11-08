-- Script para criar tabela de produtos
-- Autor: Markko1982
-- Data: 2025-11-08

-- Criar tabela produtos
CREATE TABLE IF NOT EXISTS produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    estoque INTEGER DEFAULT 0,
    categoria VARCHAR(50),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índice para busca por categoria
CREATE INDEX idx_produtos_categoria ON produtos(categoria);

-- Inserir alguns produtos de teste
INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES
('Notebook Dell', 'Notebook Dell Inspiron 15, 8GB RAM, 256GB SSD', 3500.00, 10, 'Informática'),
('Mouse Logitech', 'Mouse sem fio Logitech M170', 45.90, 50, 'Periféricos'),
('Teclado Mecânico', 'Teclado mecânico RGB', 299.00, 25, 'Periféricos'),
('Monitor LG 24"', 'Monitor LG 24 polegadas Full HD', 899.00, 15, 'Monitores'),
('Webcam Logitech', 'Webcam Full HD 1080p', 350.00, 30, 'Periféricos');

-- Ver resultado
SELECT * FROM produtos;
