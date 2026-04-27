"""
Script de Correção: Sincronização MT5 → Supabase
==================================================
Problema: bot_liquidez.py cria registros duplicados/zerados no Supabase
Solução: Puxar dados REAIS do MT5 e substituir no Supabase

Uso:
    python fix_sync_duplicates.py --dry-run    # Ver o que seria corrigido
    python fix_sync_duplicates.py --fix        # Aplicar correções
"""

import MetaTrader5 as mt5
from datetime import datetime, timedelta
import os
import sys
from supabase import create_client
from dotenv import load_dotenv
import json

# Carrega configuração
# Navegar para o diretório raiz do projeto
script_dir = os.path.dirname(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
env_path = os.path.join(project_root, ".env")

print(f"[INFO] Carregando .env de: {env_path}")
load_dotenv(env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print(f"[ERRO] Credenciais Supabase nao encontradas")
    print(f"   SUPABASE_URL: {'OK' if SUPABASE_URL else 'FALTANDO'}")
    print(f"   SUPABASE_SERVICE_ROLE_KEY: {'OK' if SUPABASE_KEY else 'FALTANDO'}")
    print(f"\nVerifique o arquivo: {env_path}")
    sys.exit(1)

print(f"[OK] Credenciais Supabase carregadas")
MAGIC_NUMBER = 123456

def initialize_mt5():
    if not mt5.initialize():
        print("❌ Erro ao conectar ao MetaTrader 5")
        return False
    print("✅ Conectado ao MetaTrader 5")
    return True

def get_real_trades_from_mt5(start_date=None):
    """Puxar todos os trades REAIS do MT5 com P&L correto."""
    if start_date is None:
        start_date = datetime(2020, 1, 1)

    end_date = datetime.now() + timedelta(days=1)
    deals = mt5.history_deals_get(start_date, end_date)

    if not deals:
        print("⚠️ Nenhum trade encontrado no MT5")
        return []

    print(f"📊 {len(deals)} deals encontrados no MT5")

    # Agrupar por posição
    trades_by_position = {}
    for d in deals:
        if d.magic != MAGIC_NUMBER:
            continue

        pos_id = d.position_id
        if pos_id not in trades_by_position:
            trades_by_position[pos_id] = []
        trades_by_position[pos_id].append(d)

    # Montar trades completos
    real_trades = []
    for pos_id, deals_list in trades_by_position.items():
        if len(deals_list) < 2:
            continue  # Ignorar posições incompletas

        # Ordenar por tempo
        deals_list.sort(key=lambda x: x.time)

        entry = deals_list[0]
        exit_deal = deals_list[-1]

        # Calcular P&L real
        pnl_real = exit_deal.profit + exit_deal.commission + exit_deal.swap

        real_trades.append({
            'position_id': pos_id,
            'symbol': entry.symbol,
            'type': 'BUY' if entry.type == 0 else 'SELL',
            'entry_price': entry.price,
            'exit_price': exit_deal.price,
            'entry_time': datetime.fromtimestamp(entry.time).isoformat(),
            'exit_time': datetime.fromtimestamp(exit_deal.time).isoformat(),
            'pnl': pnl_real,
            'volume': entry.volume,
            'magic': MAGIC_NUMBER
        })

    print(f"✅ {len(real_trades)} trades completos identificados")
    return real_trades

def get_supabase_trades():
    """Puxar todos os trades do Supabase."""
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = client.table("signals_liquidez").select("*").execute()
    return response.data

def analyze_discrepancies(real_trades, supabase_trades):
    """Analisar diferenças entre MT5 e Supabase."""
    print("\n" + "="*80)
    print("ANÁLISE DE DISCREPÂNCIAS")
    print("="*80)

    # Agrupar Supabase por símbolo e tempo
    supabase_by_time = {}
    for st in supabase_trades:
        key = f"{st['symbol']}_{st['created_at']}"
        supabase_by_time[key] = st

    # Contar discrepâncias
    zeros_in_supabase = [st for st in supabase_trades if st.get('pnl', 0) == 0]
    duplicates = []
    missing_in_supabase = []

    for rt in real_trades:
        key = f"{rt['symbol']}_{rt['entry_time']}"
        if key not in supabase_by_time:
            missing_in_supabase.append(rt)

    print(f"\n📊 RESUMO:")
    print(f"   Trades no MT5 (REAL):      {len(real_trades)}")
    print(f"   Trades no Supabase:        {len(supabase_trades)}")
    print(f"   Trades com P&L = $0:       {len(zeros_in_supabase)} ⚠️")
    print(f"   Trades faltando:           {len(missing_in_supabase)}")

    if zeros_in_supabase:
        print(f"\n⚠️ TRADES ZERADOS NO SUPABASE (primeiros 10):")
        for st in zeros_in_supabase[:10]:
            print(f"   {st['symbol']:8s} | {st['type']:4s} | {st['created_at'][:19]} | Status: {st.get('status', 'N/A')}")

    return {
        'zeros': zeros_in_supabase,
        'missing': missing_in_supabase,
        'real_trades': real_trades
    }

def fix_supabase(real_trades, dry_run=True):
    """Corrigir Supabase com dados reais do MT5."""
    client = create_client(SUPABASE_URL, SUPABASE_KEY)

    if dry_run:
        print("\n" + "="*80)
        print("🔍 MODO DRY-RUN: Nenhuma alteração será feita")
        print("="*80)
    else:
        print("\n" + "="*80)
        print("🔧 APLICANDO CORREÇÕES")
        print("="*80)

        # Limpar tabela
        print("\n1. Limpando registros antigos...")
        client.table("signals_liquidez").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        print("   ✅ Tabela limpa")

    print(f"\n2. Inserindo {len(real_trades)} trades reais do MT5...")

    inserted = 0
    for rt in real_trades:
        new_trade = {
            "symbol": rt['symbol'],
            "type": rt['type'],
            "price": rt['entry_price'],
            "status": "closed",
            "pnl": rt['pnl'],
            "magic": rt['position_id'],  # Usar position_id como identificador único
            "wick_pct": 0.5,
            "agent_opinions": [{"agent": "MT5 Real", "comment": "Sincronizado via fix_sync_duplicates.py", "sentiment": "neutral"}],
            "created_at": rt['entry_time'],
            "closed_at": rt['exit_time']
        }

        if not dry_run:
            try:
                client.table("signals_liquidez").insert(new_trade).execute()
                inserted += 1
                if inserted % 10 == 0:
                    print(f"   ... {inserted}/{len(real_trades)}")
            except Exception as e:
                print(f"   ⚠️ Erro ao inserir {rt['symbol']}: {e}")
        else:
            print(f"   [DRY-RUN] {rt['symbol']:8s} | {rt['type']:4s} | P&L: ${rt['pnl']:8.2f}")

    if not dry_run:
        print(f"\n✅ {inserted} trades inseridos com sucesso")
    else:
        print(f"\n[DRY-RUN] {len(real_trades)} trades seriam inseridos")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Corrigir sincronização MT5 → Supabase")
    parser.add_argument('--dry-run', action='store_true', help='Ver o que seria corrigido sem aplicar')
    parser.add_argument('--fix', action='store_true', help='Aplicar correções')
    parser.add_argument('--analyze-only', action='store_true', help='Apenas analisar discrepâncias')
    args = parser.parse_args()

    if not args.dry_run and not args.fix and not args.analyze_only:
        print("❌ Use --dry-run, --fix ou --analyze-only")
        print("\nExemplos:")
        print("  python fix_sync_duplicates.py --dry-run       # Ver correções")
        print("  python fix_sync_duplicates.py --fix           # Aplicar correções")
        print("  python fix_sync_duplicates.py --analyze-only  # Apenas análise")
        return

    # Conectar ao MT5
    if not initialize_mt5():
        return

    # Puxar dados reais
    print("\n📊 Coletando dados do MetaTrader 5...")
    real_trades = get_real_trades_from_mt5()

    # Puxar dados do Supabase
    print("\n📊 Coletando dados do Supabase...")
    supabase_trades = get_supabase_trades()

    # Analisar discrepâncias
    analysis = analyze_discrepancies(real_trades, supabase_trades)

    if args.analyze_only:
        # Salvar análise em JSON
        output_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sync_analysis.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'mt5_trades': len(real_trades),
                'supabase_trades': len(supabase_trades),
                'zeros': len(analysis['zeros']),
                'missing': len(analysis['missing']),
                'real_trades_sample': real_trades[:5]
            }, f, indent=2, default=str)
        print(f"\n✅ Análise salva em: {output_file}")
        mt5.shutdown()
        return

    # Aplicar correções
    fix_supabase(real_trades, dry_run=args.dry_run)

    # Encerrar
    mt5.shutdown()
    print("\n" + "="*80)
    if args.dry_run:
        print("✅ DRY-RUN COMPLETO")
        print("\nPara aplicar as correções, execute:")
        print("  python fix_sync_duplicates.py --fix")
    else:
        print("✅ CORREÇÕES APLICADAS COM SUCESSO")
        print("\nRecarregue seu frontend (localhost:3000) para ver os dados corrigidos.")
    print("="*80)

if __name__ == "__main__":
    main()
