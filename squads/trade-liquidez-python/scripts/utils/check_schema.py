"""
Verificar Schema do Supabase - signals_liquidez
================================================
Identifica quais colunas existem e quais precisam ser criadas.
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

# Colunas necessárias para v6.0
REQUIRED_COLUMNS = {
    # Existentes (v5.9.6)
    'id': 'uuid PRIMARY KEY DEFAULT uuid_generate_v4()',
    'symbol': 'text NOT NULL',
    'type': 'text NOT NULL',
    'price': 'numeric NOT NULL',
    'sl': 'numeric',
    'tp': 'numeric',
    'status': 'text NOT NULL',
    'pnl': 'numeric',
    'magic': 'bigint',
    'wick_pct': 'numeric',
    'created_at': 'timestamptz DEFAULT now()',
    'agent_opinions': 'jsonb DEFAULT \'[]\'::jsonb',

    # Novas (v6.0)
    'position_id': 'bigint UNIQUE',  # ID único do MT5
    'exit_price': 'numeric',          # Preço de saída
    'approved_at': 'timestamptz',     # Quando foi aprovado
    'filled_at': 'timestamptz',       # Quando foi executado
    'closed_at': 'timestamptz',       # Quando foi fechado
    'updated_at': 'timestamptz',      # Última atualização
    'reject_reason': 'text',          # Motivo da rejeição
    'error_message': 'text'           # Mensagem de erro
}

def check_schema():
    """Verificar colunas existentes."""
    client = create_client(SUPABASE_URL, SUPABASE_KEY)

    print("="*80)
    print("VERIFICACAO DE SCHEMA: signals_liquidez")
    print("="*80)

    try:
        # Buscar um registro qualquer para ver as colunas
        result = client.table("signals_liquidez").select("*").limit(1).execute()

        if result.data:
            existing_columns = set(result.data[0].keys())
            print(f"\n[OK] {len(existing_columns)} colunas encontradas no schema atual:")
            for col in sorted(existing_columns):
                print(f"   - {col}")
        else:
            # Tabela vazia, tentar inserir registro vazio para ver erro
            print("\n[INFO] Tabela vazia, tentando detectar colunas...")
            existing_columns = set()

    except Exception as e:
        print(f"[ERROR] Falha ao buscar schema: {e}")
        existing_columns = set()

    # Identificar colunas faltantes
    required_columns = set(REQUIRED_COLUMNS.keys())
    missing_columns = required_columns - existing_columns

    if missing_columns:
        print(f"\n[WARNING] {len(missing_columns)} colunas FALTANDO:")
        for col in sorted(missing_columns):
            print(f"   - {col} ({REQUIRED_COLUMNS[col]})")

        # Gerar SQL ALTER TABLE
        print("\n" + "="*80)
        print("SQL PARA CRIAR COLUNAS FALTANTES")
        print("="*80)
        print("\n-- Execute este SQL no Supabase SQL Editor:\n")

        for col in sorted(missing_columns):
            print(f"ALTER TABLE signals_liquidez ADD COLUMN IF NOT EXISTS {col} {REQUIRED_COLUMNS[col]};")

        print("\n-- Criar índice para position_id (importante para performance):")
        print("CREATE UNIQUE INDEX IF NOT EXISTS idx_signals_position_id ON signals_liquidez(position_id) WHERE position_id IS NOT NULL;")

    else:
        print("\n[OK] Todas as colunas necessarias estao presentes!")

    # Colunas extras (que existem mas não são necessárias)
    extra_columns = existing_columns - required_columns
    if extra_columns:
        print(f"\n[INFO] {len(extra_columns)} colunas EXTRAS (podem ser mantidas):")
        for col in sorted(extra_columns):
            print(f"   - {col}")

    return existing_columns, missing_columns

if __name__ == "__main__":
    existing, missing = check_schema()

    print("\n" + "="*80)
    print("RESUMO")
    print("="*80)
    print(f"Colunas existentes: {len(existing)}")
    print(f"Colunas faltando:   {len(missing)}")

    if missing:
        print("\n[ACTION REQUIRED] Execute o SQL acima no Supabase antes da migracao!")
    else:
        print("\n[OK] Schema pronto para migracao v6.0!")
