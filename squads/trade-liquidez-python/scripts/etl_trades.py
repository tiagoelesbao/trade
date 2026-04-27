"""
ETL Trades — Consulta e análise de trades fechados
===================================================
Uso:
  python etl_trades.py                          # todos os trades fechados
  python etl_trades.py --session                # trades da sessão atual (bot_logs)
  python etl_trades.py --from 2026-04-20        # a partir de uma data
  python etl_trades.py --from 2026-04-20 --to 2026-04-21
  python etl_trades.py --symbol EURUSD
  python etl_trades.py --symbol EURUSD --from 2026-04-20
  python etl_trades.py --output json            # exportar JSON
  python etl_trades.py --output csv             # exportar CSV
  python etl_trades.py --detail                 # listar cada trade individualmente
"""

import sys, os, argparse, json, csv
from datetime import datetime, timezone
from collections import defaultdict

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Credenciais
sys.path.insert(0, os.path.dirname(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, ".env"))

from supabase import create_client
client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

W = 72
SEP  = "=" * W
DASH = "-" * W

def fmt_dt(iso):
    if not iso:
        return "—"
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%d/%m %H:%M")
    except:
        return iso[:16]

def fmt_pnl(v):
    if v is None:
        return "  —   "
    return f"+${v:.2f}" if v >= 0 else f"-${abs(v):.2f}"

def get_session_start():
    """Detecta início da sessão via bot_logs (evento bot_started mais recente)."""
    try:
        res = client.table("bot_logs")\
            .select("created_at")\
            .eq("event", "bot_started")\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()
        if res.data:
            return res.data[0]["created_at"]
    except:
        pass
    # Fallback: últimas 12h
    from datetime import timedelta
    return (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat()

def fetch_trades(args):
    query = client.table("signals_liquidez")\
        .select("id,symbol,type,status,pnl,price,sl,tp,exit_price,wick_pct,created_at,closed_at,position_id,reject_reason")\
        .eq("status", "closed")\
        .order("created_at", desc=False)

    if args.session:
        session_start = get_session_start()
        print(f"  Sessão desde: {fmt_dt(session_start)}")
        query = query.gte("created_at", session_start)
    elif args.date_from:
        query = query.gte("created_at", args.date_from + "T00:00:00")
    if args.date_to:
        query = query.lte("created_at", args.date_to + "T23:59:59")
    if args.symbol:
        query = query.eq("symbol", args.symbol.upper())

    res = query.execute()
    return res.data or []

def compute_stats(trades):
    closed = [t for t in trades if t.get("pnl") is not None]
    wins   = [t for t in closed if t["pnl"] > 0]
    losses = [t for t in closed if t["pnl"] < 0]
    be     = [t for t in closed if t["pnl"] == 0]

    total_pnl   = sum(t["pnl"] for t in closed)
    avg_win     = sum(t["pnl"] for t in wins) / len(wins) if wins else 0
    avg_loss    = sum(t["pnl"] for t in losses) / len(losses) if losses else 0
    rr          = abs(avg_win / avg_loss) if avg_loss else 0
    wr          = len(wins) / len(closed) * 100 if closed else 0
    max_win     = max((t["pnl"] for t in closed), default=0)
    max_loss    = min((t["pnl"] for t in closed), default=0)
    expectancy  = (wr/100 * avg_win) + ((1 - wr/100) * avg_loss)

    # Drawdown sequencial
    peak = 0; curve = 0; max_dd = 0
    for t in closed:
        curve += t["pnl"]
        if curve > peak:
            peak = curve
        dd = peak - curve
        if dd > max_dd:
            max_dd = dd

    return {
        "total": len(closed), "wins": len(wins), "losses": len(losses),
        "breakeven": len(be), "wr": wr, "total_pnl": total_pnl,
        "avg_win": avg_win, "avg_loss": avg_loss, "rr": rr,
        "max_win": max_win, "max_loss": max_loss,
        "expectancy": expectancy, "max_drawdown": max_dd
    }

def print_report(trades, args):
    s = compute_stats(trades)

    print(SEP)
    title = "TRADES DA SESSÃO" if args.session else \
            f"TRADES {args.date_from or 'TODOS'}" + (f" → {args.date_to}" if args.date_to else "")
    if args.symbol:
        title += f"  [{args.symbol.upper()}]"
    print(f"  {title}")
    print(DASH)

    # Resumo financeiro
    print(f"  Total: {s['total']} trades  |  WR: {s['wr']:.1f}%  |  P&L: {fmt_pnl(s['total_pnl'])}")
    print(f"  Wins:  {s['wins']}  |  Losses: {s['losses']}  |  Breakeven: {s['breakeven']}")
    print(f"  Avg Win: {fmt_pnl(s['avg_win'])}  |  Avg Loss: {fmt_pnl(s['avg_loss'])}  |  R/R: {s['rr']:.2f}x")
    print(f"  Melhor: {fmt_pnl(s['max_win'])}  |  Pior: {fmt_pnl(s['max_loss'])}  |  Max DD: ${s['max_drawdown']:.2f}")
    print(f"  Expectancy/trade: {fmt_pnl(s['expectancy'])}")
    print(DASH)

    # Por símbolo
    by_sym = defaultdict(lambda: {"trades":0,"wins":0,"losses":0,"pnl":0.0,"buy":0,"sell":0})
    for t in [x for x in trades if x.get("pnl") is not None]:
        sym = t["symbol"]
        by_sym[sym]["trades"] += 1
        by_sym[sym]["pnl"]    += t["pnl"]
        if t["pnl"] > 0: by_sym[sym]["wins"] += 1
        else:            by_sym[sym]["losses"] += 1
        if t["type"] == "BUY": by_sym[sym]["buy"] += 1
        else:                  by_sym[sym]["sell"] += 1

    print(f"  {'SYM':<10} {'TRD':>4} {'W':>3} {'L':>3} {'WR%':>6} {'P&L':>10} {'AVG':>8} {'BUY':>4} {'SELL':>5}")
    print(DASH)
    for sym, d in sorted(by_sym.items(), key=lambda x: x[1]["pnl"], reverse=True):
        wr  = d["wins"]/d["trades"]*100 if d["trades"] else 0
        avg = d["pnl"]/d["trades"] if d["trades"] else 0
        flag = " ✓" if d["pnl"] > 0 else " ✗"
        print(f"  {sym:<10} {d['trades']:>4} {d['wins']:>3} {d['losses']:>3} {wr:>5.1f}% {fmt_pnl(d['pnl']):>10} {fmt_pnl(avg):>8} {d['buy']:>4} {d['sell']:>5}{flag}")
    print(DASH)

    # Detalhe linha a linha
    if args.detail:
        print(f"\n  {'DATA':>11} {'SYM':<10} {'DIR':<5} {'ENTRADA':>9} {'SAÍDA':>9} {'PNL':>9} {'WICK':>6}")
        print(DASH)
        for t in trades:
            if t.get("pnl") is None:
                continue
            wick = f"{t['wick_pct']*100:.0f}%" if t.get("wick_pct") else "  —  "
            ep   = f"{t.get('exit_price', 0):.5f}" if t.get("exit_price") else "   —   "
            print(f"  {fmt_dt(t['created_at']):>11} {t['symbol']:<10} {t['type']:<5} {t['price']:>9.5f} {ep:>9} {fmt_pnl(t['pnl']):>9} {wick:>6}")
        print(DASH)

    print(f"\n  {len(trades)} registros  |  Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(SEP)

def export_json(trades, args):
    stats  = compute_stats(trades)
    output = {
        "generated_at": datetime.now().isoformat(),
        "filters": {"session": args.session, "date_from": args.date_from,
                    "date_to": args.date_to, "symbol": args.symbol},
        "summary": stats,
        "trades": trades
    }
    path = os.path.join(os.path.dirname(__file__), f"etl_trades_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)
    print(f"  JSON exportado: {path}")

def export_csv(trades):
    path = os.path.join(os.path.dirname(__file__), f"etl_trades_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    fields = ["id","symbol","type","pnl","price","exit_price","sl","tp","wick_pct","created_at","closed_at","position_id"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(trades)
    print(f"  CSV exportado: {path}")

def main():
    p = argparse.ArgumentParser(description="ETL Trades — consulta trades fechados no Supabase")
    p.add_argument("--session",    action="store_true", help="trades da sessão atual")
    p.add_argument("--from",       dest="date_from",    help="data início YYYY-MM-DD")
    p.add_argument("--to",         dest="date_to",      help="data fim YYYY-MM-DD")
    p.add_argument("--symbol",     help="filtrar por símbolo (ex: EURUSD)")
    p.add_argument("--output",     choices=["table","json","csv"], default="table")
    p.add_argument("--detail",     action="store_true", help="listar cada trade individualmente")
    args = p.parse_args()

    print(SEP)
    print("  ETL TRADES — Trade Liquidez v6.0")
    print(DASH)

    trades = fetch_trades(args)

    if not trades:
        print("  Nenhum trade encontrado com os filtros informados.")
        print(SEP)
        return

    if args.output == "json":
        export_json(trades, args)
    elif args.output == "csv":
        export_csv(trades)
    else:
        print_report(trades, args)

if __name__ == "__main__":
    main()
