"""
ETL Rejections — Análise de sinais rejeitados
==============================================
Uso:
  python etl_rejections.py                        # todos os sinais rejeitados
  python etl_rejections.py --from 2026-04-20      # a partir de uma data
  python etl_rejections.py --from 2026-04-20 --to 2026-04-21
  python etl_rejections.py --symbol EURUSD
  python etl_rejections.py --reason trend         # filtrar por motivo (substring)
  python etl_rejections.py --detail               # listar cada sinal individualmente
  python etl_rejections.py --output json          # exportar JSON
  python etl_rejections.py --output csv           # exportar CSV
"""

import sys, os, argparse, json, csv
from datetime import datetime, timezone
from collections import defaultdict

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

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
    if not iso: return "—"
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%d/%m %H:%M")
    except:
        return iso[:16]

def fetch_rejections(args):
    query = client.table("signals_liquidez")\
        .select("id,symbol,type,status,reject_reason,wick_pct,price,created_at,position_id")\
        .eq("status", "rejected")\
        .order("created_at", desc=False)

    if args.date_from:
        query = query.gte("created_at", args.date_from + "T00:00:00")
    if args.date_to:
        query = query.lte("created_at", args.date_to + "T23:59:59")
    if args.symbol:
        query = query.eq("symbol", args.symbol.upper())

    res = query.execute()
    data = res.data or []

    if args.reason:
        kw = args.reason.lower()
        data = [r for r in data if r.get("reject_reason") and kw in r["reject_reason"].lower()]

    return data

def categorize_reason(reason):
    if not reason:
        return "unknown"
    r = reason.lower()
    if "trend" in r or "slope" in r:        return "trend_filter"
    if "rsi" in r:                           return "rsi_filter"
    if "wick" in r:                          return "wick_filter"
    if "cool" in r or "kill" in r:           return "cooldown"
    if "proxim" in r or "near" in r:         return "proximity"
    if "reversal" in r or "color" in r:      return "reversal_filter"
    if "daily" in r or "target" in r or "loss" in r: return "daily_limit"
    if "zone" in r:                          return "zone_filter"
    if "spread" in r:                        return "spread"
    return "other"

def print_report(rejections, args):
    total = len(rejections)
    print(SEP)
    title = f"SINAIS REJEITADOS {args.date_from or 'TODOS'}"
    if args.date_to:    title += f" → {args.date_to}"
    if args.symbol:     title += f"  [{args.symbol.upper()}]"
    if args.reason:     title += f"  [motivo~'{args.reason}']"
    print(f"  {title}")
    print(f"  Total rejeitados: {total}")
    print(DASH)

    if total == 0:
        print("  Nenhum sinal rejeitado encontrado.")
        print(SEP)
        return

    # Por motivo (categoria)
    by_cat  = defaultdict(int)
    by_raw  = defaultdict(int)
    by_sym  = defaultdict(lambda: {"total": 0, "buy": 0, "sell": 0, "cats": defaultdict(int)})

    for r in rejections:
        cat = categorize_reason(r.get("reject_reason"))
        raw = r.get("reject_reason") or "—"
        by_cat[cat]  += 1
        by_raw[raw]  += 1
        sym = r["symbol"]
        by_sym[sym]["total"] += 1
        by_sym[sym]["cats"][cat] += 1
        if r["type"] == "BUY":  by_sym[sym]["buy"]  += 1
        else:                   by_sym[sym]["sell"] += 1

    # Tabela por categoria
    print(f"  {'CATEGORIA':<22} {'QTD':>5} {'%':>7}")
    print(DASH)
    for cat, cnt in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
        pct = cnt / total * 100
        bar = "█" * int(pct / 5)
        print(f"  {cat:<22} {cnt:>5} {pct:>6.1f}%  {bar}")
    print(DASH)

    # Motivos textuais únicos (top 10)
    print(f"\n  TOP MOTIVOS EXATOS (raw):")
    print(DASH)
    for raw, cnt in sorted(by_raw.items(), key=lambda x: x[1], reverse=True)[:10]:
        pct = cnt / total * 100
        print(f"  {cnt:>4}x ({pct:>5.1f}%)  {raw[:55]}")
    print(DASH)

    # Por símbolo
    print(f"\n  {'SYM':<10} {'TOTAL':>6} {'BUY':>5} {'SELL':>5}  TOP MOTIVO")
    print(DASH)
    for sym, d in sorted(by_sym.items(), key=lambda x: x[1]["total"], reverse=True):
        top_cat = max(d["cats"], key=d["cats"].get) if d["cats"] else "—"
        print(f"  {sym:<10} {d['total']:>6} {d['buy']:>5} {d['sell']:>5}  {top_cat}")
    print(DASH)

    # Detalhe linha a linha
    if args.detail:
        print(f"\n  {'DATA':>11} {'SYM':<10} {'DIR':<5} {'PREÇO':>10}  MOTIVO")
        print(DASH)
        for r in rejections:
            price = f"{r['price']:.5f}" if r.get("price") else "     —    "
            reason_txt = (r.get("reject_reason") or "—")[:45]
            print(f"  {fmt_dt(r['created_at']):>11} {r['symbol']:<10} {r['type']:<5} {price:>10}  {reason_txt}")
        print(DASH)

    print(f"\n  {total} registros  |  Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(SEP)

def export_json(rejections, args):
    by_cat  = defaultdict(int)
    by_sym  = defaultdict(int)
    for r in rejections:
        by_cat[categorize_reason(r.get("reject_reason"))] += 1
        by_sym[r["symbol"]] += 1

    output = {
        "generated_at": datetime.now().isoformat(),
        "filters": {"date_from": args.date_from, "date_to": args.date_to,
                    "symbol": args.symbol, "reason_keyword": args.reason},
        "summary": {"total": len(rejections), "by_category": dict(by_cat), "by_symbol": dict(by_sym)},
        "rejections": rejections
    }
    path = os.path.join(os.path.dirname(__file__), f"etl_rejections_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)
    print(f"  JSON exportado: {path}")

def export_csv(rejections):
    path = os.path.join(os.path.dirname(__file__), f"etl_rejections_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    fields = ["id", "symbol", "type", "price", "wick_pct", "reject_reason", "created_at", "position_id"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rejections)
    print(f"  CSV exportado: {path}")

def main():
    p = argparse.ArgumentParser(description="ETL Rejections — analisa sinais rejeitados no Supabase")
    p.add_argument("--from",    dest="date_from", help="data início YYYY-MM-DD")
    p.add_argument("--to",      dest="date_to",   help="data fim YYYY-MM-DD")
    p.add_argument("--symbol",  help="filtrar por símbolo (ex: EURUSD)")
    p.add_argument("--reason",  help="filtrar por substring no motivo (ex: trend, rsi, wick)")
    p.add_argument("--output",  choices=["table", "json", "csv"], default="table")
    p.add_argument("--detail",  action="store_true", help="listar cada sinal individualmente")
    args = p.parse_args()

    print(SEP)
    print("  ETL REJECTIONS — Trade Liquidez v6.0")
    print(DASH)

    rejections = fetch_rejections(args)

    if not rejections:
        print("  Nenhum sinal rejeitado encontrado com os filtros informados.")
        print(SEP)
        return

    if args.output == "json":
        export_json(rejections, args)
    elif args.output == "csv":
        export_csv(rejections)
    else:
        print_report(rejections, args)

if __name__ == "__main__":
    main()
