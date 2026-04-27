"""
Setup Schema v6.0 - Adicionar Colunas Necessárias
==================================================
Adiciona as 7 colunas novas necessárias para arquitetura de estados.
"""

import os
from supabase import create_client
from dotenv import load_dotenv

# Carregar credenciais
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# SQL para criar colunas
SETUP_SQL = """
-- Colunas para arquitetura de estados v6.0
ALTER TABLE signals_liquidez ADD COLUMN IF NOT EXISTS position_id bigint;
ALTER TABLE signals_liquidez ADD COLUMN IF NOT EXISTS exit_price numeric;
ALTER TABLE signals_liquidez ADD COLUMN IF NOT EXISTS approved_at timestamptz;
ALTER TABLE signals_liquidez ADD COLUMN IF NOT EXISTS filled_at timestamptz;
ALTER TABLE signals_liquidez ADD COLUMN IF NOT EXISTS updated_at timestamptz;
ALTER TABLE signals_liquidez ADD COLUMN IF NOT EXISTS reject_reason text;
ALTER TABLE signals_liquidez ADD COLUMN IF NOT EXISTS error_message text;

-- Índice único para position_id (previne duplicatas)
CREATE UNIQUE INDEX IF NOT EXISTS idx_signals_position_id
ON signals_liquidez(position_id)
WHERE position_id IS NOT NULL;

-- Índice para status (para queries por estado)
CREATE INDEX IF NOT EXISTS idx_signals_status
ON signals_liquidez(status);

-- Índice para created_at (para ordenação temporal)
CREATE INDEX IF NOT EXISTS idx_signals_created_at
ON signals_liquidez(created_at DESC);
"""

def setup_schema():
    """Adicionar colunas necessárias ao schema."""
    client = create_client(SUPABASE_URL, SUPABASE_KEY)

    print("="*80)
    print("SETUP SCHEMA v6.0")
    print("="*80)

    print("\n[INFO] Executando SQL para adicionar colunas...")

    try:
        # Executar SQL usando RPC (função SQL customizada) ou via REST
        # Como não temos acesso direto ao SQL, vamos usar uma abordagem alternativa:
        # Tentar inserir um registro com as novas colunas e ver se funciona

        print("\n[INFO] Verificando se as colunas ja existem...")

        # Tentar fazer um SELECT com as novas colunas
        try:
            result = client.table("signals_liquidez").select(
                "id, position_id, exit_price, approved_at, filled_at, updated_at, reject_reason, error_message"
            ).limit(1).execute()
            print("[OK] Todas as colunas necessarias ja existem!")
            return True
        except Exception as e:
            if "could not find" in str(e).lower() or "column" in str(e).lower():
                print(f"[ERROR] Colunas faltando. Erro: {e}")
                print("\n" + "="*80)
                print("ACESSO SQL NECESSARIO")
                print("="*80)
                print("\nO Supabase nao permite ALTER TABLE via Python API.")
                print("Voce precisa executar o SQL manualmente no Supabase Dashboard.")
                print("\n1. Abra: https://supabase.com/dashboard")
                print(f"2. Selecione seu projeto")
                print("3. Va em 'SQL Editor' no menu lateral")
                print("4. Cole e execute este SQL:\n")
                print(SETUP_SQL)
                print("\n5. Depois execute este script novamente para validar")
                return False
            else:
                raise

    except Exception as e:
        print(f"[ERROR] Falha ao verificar schema: {e}")
        print("\n[INFO] Execute o SQL manualmente no Supabase Dashboard:")
        print(SETUP_SQL)
        return False

if __name__ == "__main__":
    success = setup_schema()

    print("\n" + "="*80)
    if success:
        print("[OK] Schema v6.0 pronto!")
        print("\nProximo passo:")
        print("  python migrate_to_v6_lifecycle.py --migrate")
    else:
        print("[ACTION REQUIRED] Execute o SQL no Supabase Dashboard primeiro!")
        print("\nDepois execute este script novamente para validar:")
        print("  python setup_schema_v6.py")
    print("="*80)
