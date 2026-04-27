-- ============================================================================
-- Trade Liquidez - Schema Migration v6.0
-- ============================================================================
-- Adiciona colunas necessárias para arquitetura de estados
-- Execute este SQL no Supabase SQL Editor
-- ============================================================================

-- 1. Adicionar colunas novas
ALTER TABLE signals_liquidez ADD COLUMN IF NOT EXISTS position_id bigint;
ALTER TABLE signals_liquidez ADD COLUMN IF NOT EXISTS exit_price numeric;
ALTER TABLE signals_liquidez ADD COLUMN IF NOT EXISTS approved_at timestamptz;
ALTER TABLE signals_liquidez ADD COLUMN IF NOT EXISTS filled_at timestamptz;
ALTER TABLE signals_liquidez ADD COLUMN IF NOT EXISTS updated_at timestamptz;
ALTER TABLE signals_liquidez ADD COLUMN IF NOT EXISTS reject_reason text;
ALTER TABLE signals_liquidez ADD COLUMN IF NOT EXISTS error_message text;

-- 2. Criar índices para performance e integridade
-- Índice único para position_id (previne duplicatas)
CREATE UNIQUE INDEX IF NOT EXISTS idx_signals_position_id
ON signals_liquidez(position_id)
WHERE position_id IS NOT NULL;

-- Índice para status (queries por estado serão comuns)
CREATE INDEX IF NOT EXISTS idx_signals_status
ON signals_liquidez(status);

-- Índice para created_at (ordenação temporal)
CREATE INDEX IF NOT EXISTS idx_signals_created_at
ON signals_liquidez(created_at DESC);

-- Índice composto para symbol + status (queries frequentes)
CREATE INDEX IF NOT EXISTS idx_signals_symbol_status
ON signals_liquidez(symbol, status);

-- 3. Comentários nas colunas (documentação)
COMMENT ON COLUMN signals_liquidez.position_id IS 'ID único da posição no MT5 (chave para evitar duplicatas)';
COMMENT ON COLUMN signals_liquidez.exit_price IS 'Preço de saída do trade (apenas quando status=closed)';
COMMENT ON COLUMN signals_liquidez.approved_at IS 'Timestamp de quando foi aprovado pela sala de guerra';
COMMENT ON COLUMN signals_liquidez.filled_at IS 'Timestamp de quando a ordem foi executada no MT5';
COMMENT ON COLUMN signals_liquidez.updated_at IS 'Timestamp da última atualização do registro';
COMMENT ON COLUMN signals_liquidez.reject_reason IS 'Motivo da rejeição (se status=rejected)';
COMMENT ON COLUMN signals_liquidez.error_message IS 'Mensagem de erro (se status=error)';

-- 4. Validações (constraints)
-- Garantir que position_id é positivo
ALTER TABLE signals_liquidez
ADD CONSTRAINT check_position_id_positive
CHECK (position_id IS NULL OR position_id > 0);

-- Garantir que pnl só existe quando status=closed
-- (removido pois pode causar problemas em updates parciais)

-- 5. Atualizar registros existentes (se houver)
-- Adicionar updated_at para registros antigos
UPDATE signals_liquidez
SET updated_at = created_at
WHERE updated_at IS NULL;

-- ============================================================================
-- Verificação Final
-- ============================================================================
-- Execute esta query para validar as colunas:
SELECT
  column_name,
  data_type,
  is_nullable
FROM information_schema.columns
WHERE table_name = 'signals_liquidez'
ORDER BY ordinal_position;

-- Deve mostrar:
-- id, symbol, type, price, sl, tp, status, pnl, magic, wick_pct,
-- created_at, closed_at, agent_opinions, position_id, exit_price,
-- approved_at, filled_at, updated_at, reject_reason, error_message

-- ============================================================================
-- Sucesso!
-- ============================================================================
-- Se nao houver erros acima, execute:
--   python setup_schema_v6.py (para validar)
--   python migrate_to_v6_lifecycle.py --migrate (para migrar dados)
-- ============================================================================
