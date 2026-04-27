import os
import sys
from datetime import datetime, timedelta
from supabase import create_client
from collections import defaultdict
import json
from dotenv import load_dotenv

load_dotenv()

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuração — credenciais via variáveis de ambiente (.env)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERRO: SUPABASE_URL e SUPABASE_KEY devem estar definidos no .env")
    sys.exit(1)

client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Buscar todos os trades de hoje
today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

response = client.table("signals_liquidez").select("*").gte("created_at", today_start).order("created_at").execute()

trades = response.data

# Estatísticas
total_trades = len(trades)
wins = [t for t in trades if t.get('pnl', 0) > 0]
losses = [t for t in trades if t.get('pnl', 0) < 0]
breakeven = [t for t in trades if t.get('pnl', 0) == 0]

total_pnl = sum(t.get('pnl', 0) for t in trades)
win_rate = (len(wins) / total_trades * 100) if total_trades > 0 else 0

# Por símbolo
by_symbol = defaultdict(lambda: {'trades': 0, 'wins': 0, 'losses': 0, 'pnl': 0, 'times': []})

for t in trades:
    symbol = t['symbol']
    pnl = t.get('pnl', 0)
    created_at = datetime.fromisoformat(t['created_at'].replace('Z', '+00:00'))

    by_symbol[symbol]['trades'] += 1
    by_symbol[symbol]['pnl'] += pnl
    by_symbol[symbol]['times'].append(created_at)

    if pnl > 0:
        by_symbol[symbol]['wins'] += 1
    elif pnl < 0:
        by_symbol[symbol]['losses'] += 1

# Detectar violações de Kill-Zone (< 4h entre trades)
killzone_violations = []
for symbol, data in by_symbol.items():
    times = sorted(data['times'])
    for i in range(len(times) - 1):
        diff = (times[i+1] - times[i]).total_seconds() / 3600  # horas
        if diff < 4:
            killzone_violations.append({
                'symbol': symbol,
                'time1': times[i].strftime('%H:%M:%S'),
                'time2': times[i+1].strftime('%H:%M:%S'),
                'interval_hours': round(diff, 2)
            })

# Output
print("=" * 80)
print("ANALISE COMPLETA DE TRADES - 20/04/2026")
print("=" * 80)
print(f"\nRESUMO GERAL:")
print(f"   Total de Trades: {total_trades}")
print(f"   Wins: {len(wins)} ({len(wins)/total_trades*100:.1f}%)")
print(f"   Losses: {len(losses)} ({len(losses)/total_trades*100:.1f}%)")
print(f"   Breakeven: {len(breakeven)}")
print(f"   Win Rate: {win_rate:.1f}%")
print(f"   P&L Total: ${total_pnl:.2f}")

print(f"\nPOR SIMBOLO:")
for symbol in sorted(by_symbol.keys()):
    data = by_symbol[symbol]
    wr = (data['wins'] / data['trades'] * 100) if data['trades'] > 0 else 0
    print(f"   {symbol:8s} | Trades: {data['trades']:3d} | Wins: {data['wins']:3d} | Losses: {data['losses']:3d} | WR: {wr:5.1f}% | P&L: ${data['pnl']:8.2f}")

print(f"\nVIOLACOES DE KILL-ZONE (< 4h entre trades):")
if killzone_violations:
    print(f"   Total: {len(killzone_violations)} violacoes detectadas")
    for v in killzone_violations[:10]:  # Mostrar primeiras 10
        print(f"   {v['symbol']:8s} | {v['time1']} -> {v['time2']} | Intervalo: {v['interval_hours']}h")
else:
    print("   OK: Nenhuma violacao detectada")

print(f"\nESTATISTICAS FINANCEIRAS:")
avg_win = sum(t['pnl'] for t in wins) / len(wins) if wins else 0
avg_loss = sum(t['pnl'] for t in losses) / len(losses) if losses else 0
risk_reward = abs(avg_win / avg_loss) if avg_loss != 0 else 0
print(f"   Media Win: ${avg_win:.2f}")
print(f"   Media Loss: ${avg_loss:.2f}")
print(f"   Risk/Reward: {risk_reward:.2f}x")

print(f"\nULTIMOS 10 TRADES:")
for t in trades[-10:]:
    created = datetime.fromisoformat(t['created_at'].replace('Z', '+00:00'))
    pnl = t.get('pnl', 0)
    status_icon = "WIN" if pnl > 0 else "LOSS" if pnl < 0 else "BE"
    print(f"   {status_icon:4s} {created.strftime('%H:%M:%S')} | {t['symbol']:8s} | {t['type']:4s} | ${pnl:7.2f}")

print("=" * 80)

# Salvar JSON para análise posterior
output = {
    'date': datetime.now().isoformat(),
    'summary': {
        'total_trades': total_trades,
        'wins': len(wins),
        'losses': len(losses),
        'win_rate': win_rate,
        'total_pnl': total_pnl,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'risk_reward': risk_reward
    },
    'by_symbol': {k: {**v, 'times': [t.isoformat() for t in v['times']]} for k, v in by_symbol.items()},
    'killzone_violations': killzone_violations
}

output_path = r"C:\Users\Pichau\Desktop\trade\assets\trade_analysis_20240420.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nOK: Analise salva em: {output_path}")
