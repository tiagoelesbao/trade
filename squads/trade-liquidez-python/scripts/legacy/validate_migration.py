"""
Validar Migração v6.0
Verifica se os dados foram migrados corretamente sem zeros/duplicatas
"""

import os
from supabase import create_client
from dotenv import load_dotenv

# Carregar credenciais
script_dir = os.path.dirname(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Buscar todos os trades
result = client.table('signals_liquidez').select('*').order('created_at', desc=True).execute()

trades = result.data
print('=' * 80)
print('VALIDACAO POS-MIGRACAO v6.0')
print('=' * 80)
print(f'\nTotal de trades: {len(trades)}')

# Verificar zeros
zeros = [t for t in trades if t.get('pnl') == 0 or t.get('pnl') is None]
status = 'OK' if len(zeros) == 0 else 'ATENCAO'
print(f'Trades com PNL = 0 ou NULL: {len(zeros)} [{status}]')

# Verificar position_id
with_position_id = [t for t in trades if t.get('position_id') is not None]
status = 'OK' if len(with_position_id) == len(trades) else 'ATENCAO'
print(f'Trades com position_id: {len(with_position_id)}/{len(trades)} [{status}]')

# Verificar status
status_counts = {}
for t in trades:
    st = t.get('status', 'unknown')
    status_counts[st] = status_counts.get(st, 0) + 1

print('\nDistribuicao por status:')
for st, count in sorted(status_counts.items()):
    print(f'   {st}: {count}')

# Verificar duplicatas por position_id
position_ids = [t['position_id'] for t in trades if t.get('position_id')]
duplicates = len(position_ids) - len(set(position_ids))
status = 'OK' if duplicates == 0 else 'ATENCAO'
print(f'\nDuplicatas (mesmo position_id): {duplicates} [{status}]')

# Estatisticas de P&L
pnls = [t['pnl'] for t in trades if t.get('pnl') is not None and t['pnl'] != 0]
if pnls:
    total_pnl = sum(pnls)
    wins = len([p for p in pnls if p > 0])
    losses = len([p for p in pnls if p < 0])
    wr = (wins / len(pnls) * 100) if pnls else 0

    print(f'\nEstatisticas de P&L:')
    print(f'   Total P&L: ${total_pnl:.2f}')
    print(f'   Win Rate: {wr:.1f}% ({wins}W / {losses}L)')
    print(f'   Media por trade: ${total_pnl/len(pnls):.2f}')

# Verificar colunas novas
print(f'\nColunas v6.0:')
sample = trades[0] if trades else {}
for col in ['position_id', 'exit_price', 'approved_at', 'filled_at', 'updated_at', 'reject_reason', 'error_message']:
    exists = col in sample
    print(f'   {col}: {"[OK]" if exists else "[FALTANDO]"}')

print('\n' + '=' * 80)
result_msg = 'MIGRACAO VALIDADA' if len(zeros) == 0 and duplicates == 0 else 'REVISAR DADOS'
print(f'[{result_msg}]')
print('=' * 80)
