"""
Migração para v6.0 - Lifecycle Architecture
==========================================
Limpa dados antigos e reconstrói com arquitetura de estados.

Uso:
    python migrate_to_v6_lifecycle.py --dry-run   # Ver o que seria feito
    python migrate_to_v6_lifecycle.py --migrate   # Aplicar migração
"""

import MetaTrader5 as mt5
from datetime import datetime, timedelta
import os
import sys
from trade_lifecycle_manager import TradeLifecycleManager

# Configuração
MAGIC_NUMBER = 123456

def initialize_mt5():
    if not mt5.initialize():
        print("[ERROR] Falha ao conectar ao MetaTrader 5")
        return False
    print("[OK] Conectado ao MetaTrader 5")
    return True

def get_real_trades_from_mt5():
    """Puxar todos os trades REAIS do MT5."""
    start_date = datetime(2020, 1, 1)
    end_date = datetime.now() + timedelta(days=1)

    deals = mt5.history_deals_get(start_date, end_date)

    if not deals:
        print("[WARNING] Nenhum trade encontrado no MT5")
        return []

    print(f"[INFO] {len(deals)} deals encontrados no MT5")

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
            'entry_time': datetime.fromtimestamp(entry.time),
            'exit_time': datetime.fromtimestamp(exit_deal.time),
            'pnl': pnl_real,
            'volume': entry.volume,
            'magic': MAGIC_NUMBER
        })

    print(f"[OK] {len(real_trades)} trades completos identificados")
    return real_trades

def migrate_trades(lifecycle, trades, dry_run=True):
    """Migrar trades para nova arquitetura."""

    if dry_run:
        print("\n" + "="*80)
        print("[DRY-RUN] Nenhuma alteracao sera feita")
        print("="*80)
    else:
        print("\n" + "="*80)
        print("[MIGRATION] Aplicando migracao")
        print("="*80)

        # Limpar tabela
        print("\n[STEP 1] Limpando registros antigos...")
        try:
            lifecycle.client.table("signals_liquidez").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print("[OK] Tabela limpa")
        except Exception as e:
            print(f"[ERROR] Falha ao limpar tabela: {e}")
            return 0

    print(f"\n[STEP 2] Inserindo {len(trades)} trades com nova arquitetura...")

    inserted = 0
    for trade in trades:
        # Calcular SL e TP fictícios (pois não temos histórico)
        # Usar a diferença entre entrada e saída como base
        price_diff = abs(trade['exit_price'] - trade['entry_price'])

        if trade['type'] == 'BUY':
            sl = trade['entry_price'] - price_diff
            tp = trade['entry_price'] + (price_diff * 1.5)
        else:
            sl = trade['entry_price'] + price_diff
            tp = trade['entry_price'] - (price_diff * 1.5)

        if not dry_run:
            try:
                # Criar registro diretamente no estado 'closed'
                # (pois esses trades já foram finalizados)
                new_trade = {
                    "symbol": trade['symbol'],
                    "type": trade['type'],
                    "price": trade['entry_price'],
                    "sl": sl,
                    "tp": tp,
                    "exit_price": trade['exit_price'],
                    "status": "closed",  # Estado final
                    "pnl": trade['pnl'],
                    "position_id": trade['position_id'],  # ID único
                    "magic": trade['magic'],
                    "wick_pct": 0.5,
                    "agent_opinions": [{
                        "agent": "Migration Script",
                        "comment": "Migrado do historico do MT5",
                        "sentiment": "neutral"
                    }],
                    "created_at": trade['entry_time'].isoformat(),
                    "approved_at": trade['entry_time'].isoformat(),
                    "filled_at": trade['entry_time'].isoformat(),
                    "closed_at": trade['exit_time'].isoformat()
                }

                lifecycle.client.table("signals_liquidez").insert(new_trade).execute()
                inserted += 1

                if inserted % 10 == 0:
                    print(f"   ... {inserted}/{len(trades)}")

            except Exception as e:
                print(f"   [ERROR] Falha ao inserir {trade['symbol']}: {e}")
        else:
            print(f"   [DRY-RUN] {trade['symbol']:8s} | {trade['type']:4s} | PNL: ${trade['pnl']:8.2f} | Position: {trade['position_id']}")

    if not dry_run:
        print(f"\n[OK] {inserted} trades inseridos")
    else:
        print(f"\n[DRY-RUN] {len(trades)} trades seriam inseridos")

    return inserted

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Migrar para v6.0 Lifecycle Architecture")
    parser.add_argument('--dry-run', action='store_true', help='Ver o que seria feito sem aplicar')
    parser.add_argument('--migrate', action='store_true', help='Aplicar migracao')
    args = parser.parse_args()

    if not args.dry_run and not args.migrate:
        print("[ERROR] Use --dry-run ou --migrate")
        print("\nExemplos:")
        print("  python migrate_to_v6_lifecycle.py --dry-run    # Ver mudancas")
        print("  python migrate_to_v6_lifecycle.py --migrate    # Aplicar migracao")
        return

    # Conectar ao MT5
    if not initialize_mt5():
        return

    # Puxar dados reais
    print("\n[INFO] Coletando dados do MetaTrader 5...")
    real_trades = get_real_trades_from_mt5()

    if not real_trades:
        print("[ERROR] Nenhum trade encontrado para migrar")
        mt5.shutdown()
        return

    # Inicializar lifecycle manager
    try:
        lifecycle = TradeLifecycleManager()
    except Exception as e:
        print(f"[ERROR] Falha ao inicializar lifecycle manager: {e}")
        mt5.shutdown()
        return

    # Migrar trades
    migrated = migrate_trades(lifecycle, real_trades, dry_run=args.dry_run)

    # Encerrar
    mt5.shutdown()

    print("\n" + "="*80)
    if args.dry_run:
        print("[DRY-RUN] COMPLETO")
        print("\nPara aplicar a migracao, execute:")
        print("  python migrate_to_v6_lifecycle.py --migrate")
    else:
        print("[MIGRATION] COMPLETO")
        print(f"\n{migrated} trades migrados com sucesso")
        print("\nProximos passos:")
        print("1. Recarregue o frontend (localhost:3000)")
        print("2. Valide que nao ha trades com PNL = $0")
        print("3. Inicie o bot v6.0 para novos trades")
    print("="*80)

if __name__ == "__main__":
    main()
