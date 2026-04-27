"""
ETL Report — Relatório completo para análise IA
================================================
Gera um relatório estruturado (JSON + Markdown) combinando:
  - Trades fechados (stats, por símbolo, curva de equity)
  - Sinais rejeitados (breakdown por motivo e símbolo)
  - Saúde do banco de dados (issues encontrados)
  - Logs de sessão (bot_logs)

Uso:
  python etl_report.py                          # relatório da sessão atual
  python etl_report.py --from 2026-04-20        # período específico
  python etl_report.py --from 2026-04-20 --to 2026-04-21
  python etl_report.py --full                   # sem filtro de data (tudo)
  python etl_report.py --format markdown        # só markdown
  python etl_report.py --format json            # só JSON (para IA)
  python etl_report.py --format both            # JSON + Markdown (padrão)
"""

import sys, os, argparse, json
from datetime import datetime, timezone, timedelta
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

# ─── Helpers ──────────────────────────────────────────────────────────────────

def fmt_dt(iso):
    if not iso: return "—"
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%d/%m %H:%M")
    except:
        return iso[:16]

def fmt_pnl(v):
    if v is None: return "—"
    return f"+${v:.2f}" if v >= 0 else f"-${abs(v):.2f}"

def get_session_start():
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
    return (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat()

def categorize_reason(reason):
    if not reason: return "unknown"
    r = reason.lower()
    if "trend" in r or "slope" in r:         return "trend_filter"
    if "rsi" in r:                            return "rsi_filter"
    if "wick" in r:                           return "wick_filter"
    if "cool" in r or "kill" in r:            return "cooldown"
    if "proxim" in r or "near" in r:          return "proximity"
    if "reversal" in r or "color" in r:       return "reversal_filter"
    if "daily" in r or "target" in r:         return "daily_limit"
    if "zone" in r:                           return "zone_filter"
    return "other"

# ─── Data collectors ──────────────────────────────────────────────────────────

def collect_trades(date_from, date_to):
    query = client.table("signals_liquidez")\
        .select("id,symbol,type,status,pnl,price,exit_price,sl,tp,wick_pct,created_at,closed_at,position_id")\
        .eq("status", "closed")\
        .order("created_at", desc=False)
    if date_from: query = query.gte("created_at", date_from + "T00:00:00")
    if date_to:   query = query.lte("created_at", date_to + "T23:59:59")
    return query.execute().data or []

def collect_rejections(date_from, date_to):
    query = client.table("signals_liquidez")\
        .select("id,symbol,type,reject_reason,price,wick_pct,created_at")\
        .eq("status", "rejected")\
        .order("created_at", desc=False)
    if date_from: query = query.gte("created_at", date_from + "T00:00:00")
    if date_to:   query = query.lte("created_at", date_to + "T23:59:59")
    return query.execute().data or []

def collect_bot_logs(date_from, date_to):
    try:
        query = client.table("bot_logs")\
            .select("event,message,symbol,created_at")\
            .order("created_at", desc=False)
        if date_from: query = query.gte("created_at", date_from + "T00:00:00")
        if date_to:   query = query.lte("created_at", date_to + "T23:59:59")
        return query.execute().data or []
    except:
        return []

def collect_all_open():
    return client.table("signals_liquidez")\
        .select("id,symbol,type,price,created_at,position_id")\
        .eq("status", "open")\
        .execute().data or []

# ─── Analyzers ────────────────────────────────────────────────────────────────

def analyze_trades(trades):
    closed = [t for t in trades if t.get("pnl") is not None]
    if not closed:
        return {"total": 0}

    wins   = [t for t in closed if t["pnl"] > 0]
    losses = [t for t in closed if t["pnl"] < 0]
    be     = [t for t in closed if t["pnl"] == 0]

    total_pnl  = sum(t["pnl"] for t in closed)
    avg_win    = sum(t["pnl"] for t in wins) / len(wins) if wins else 0
    avg_loss   = sum(t["pnl"] for t in losses) / len(losses) if losses else 0
    rr         = abs(avg_win / avg_loss) if avg_loss else 0
    wr         = len(wins) / len(closed) * 100

    # Equity curve + max drawdown
    peak = 0; curve = 0; max_dd = 0
    equity = []
    for t in closed:
        curve += t["pnl"]
        equity.append(round(curve, 2))
        if curve > peak: peak = curve
        dd = peak - curve
        if dd > max_dd: max_dd = dd

    # Por símbolo
    by_sym = defaultdict(lambda: {"trades":0,"wins":0,"losses":0,"pnl":0.0,"buy":0,"sell":0})
    for t in closed:
        s = t["symbol"]
        by_sym[s]["trades"] += 1
        by_sym[s]["pnl"]    += t["pnl"]
        if t["pnl"] > 0: by_sym[s]["wins"] += 1
        elif t["pnl"] < 0: by_sym[s]["losses"] += 1
        if t["type"] == "BUY": by_sym[s]["buy"] += 1
        else:                  by_sym[s]["sell"] += 1

    sym_stats = []
    for sym, d in sorted(by_sym.items(), key=lambda x: x[1]["pnl"], reverse=True):
        wr_s = d["wins"] / d["trades"] * 100 if d["trades"] else 0
        sym_stats.append({
            "symbol": sym, "trades": d["trades"], "wins": d["wins"],
            "losses": d["losses"], "wr_pct": round(wr_s, 1),
            "pnl": round(d["pnl"], 2), "avg_pnl": round(d["pnl"]/d["trades"], 2),
            "buy": d["buy"], "sell": d["sell"]
        })

    return {
        "total": len(closed), "wins": len(wins), "losses": len(losses), "breakeven": len(be),
        "wr_pct": round(wr, 1), "total_pnl": round(total_pnl, 2),
        "avg_win": round(avg_win, 2), "avg_loss": round(avg_loss, 2),
        "rr_ratio": round(rr, 2), "expectancy": round((wr/100 * avg_win) + ((1 - wr/100) * avg_loss), 2),
        "max_win": round(max((t["pnl"] for t in closed), default=0), 2),
        "max_loss": round(min((t["pnl"] for t in closed), default=0), 2),
        "max_drawdown": round(max_dd, 2),
        "equity_curve": equity,
        "by_symbol": sym_stats
    }

def analyze_rejections(rejections):
    if not rejections:
        return {"total": 0}

    by_cat  = defaultdict(int)
    by_sym  = defaultdict(int)
    by_raw  = defaultdict(int)

    for r in rejections:
        by_cat[categorize_reason(r.get("reject_reason"))] += 1
        by_sym[r["symbol"]] += 1
        by_raw[r.get("reject_reason") or "—"] += 1

    top_reasons = sorted(by_raw.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "total": len(rejections),
        "by_category": dict(sorted(by_cat.items(), key=lambda x: x[1], reverse=True)),
        "by_symbol":   dict(sorted(by_sym.items(), key=lambda x: x[1], reverse=True)),
        "top_reasons": [{"reason": r, "count": c} for r, c in top_reasons]
    }

def analyze_logs(logs):
    if not logs:
        return {"total": 0, "events": {}}
    by_event = defaultdict(int)
    errors = []
    for l in logs:
        by_event[l.get("event", "unknown")] += 1
        if l.get("event") in ("error", "trade_error", "connection_lost"):
            errors.append({"event": l["event"], "message": l.get("message",""), "time": fmt_dt(l.get("created_at"))})
    return {"total": len(logs), "events": dict(by_event), "errors": errors[:20]}

# ─── Formatters ───────────────────────────────────────────────────────────────

def to_markdown(report):
    t   = report["trades"]
    rej = report["rejections"]
    logs = report["bot_logs"]
    meta = report["meta"]
    open_trades = report["open_trades"]

    lines = [
        f"# Relatório Trade Liquidez v6.0",
        f"",
        f"**Gerado em:** {meta['generated_at']}  ",
        f"**Período:** {meta['period']}  ",
        f"**Sessão desde:** {meta.get('session_start','—')}  ",
        f"",
        f"---",
        f"",
        f"## 1. Sumário de Performance",
        f"",
    ]

    if t.get("total", 0) == 0:
        lines.append("Nenhum trade fechado no período.")
    else:
        lines += [
            f"| Métrica | Valor |",
            f"|---------|-------|",
            f"| Total trades | {t['total']} |",
            f"| Win Rate | {t['wr_pct']}% |",
            f"| P&L Total | {fmt_pnl(t['total_pnl'])} |",
            f"| Avg Win | {fmt_pnl(t['avg_win'])} |",
            f"| Avg Loss | {fmt_pnl(t['avg_loss'])} |",
            f"| R/R Ratio | {t['rr_ratio']}x |",
            f"| Expectancy/trade | {fmt_pnl(t['expectancy'])} |",
            f"| Max Win | {fmt_pnl(t['max_win'])} |",
            f"| Max Loss | {fmt_pnl(t['max_loss'])} |",
            f"| Max Drawdown | ${t['max_drawdown']:.2f} |",
            f"",
            f"## 2. Performance por Símbolo",
            f"",
            f"| Símbolo | Trades | WR% | P&L | Avg | B/S |",
            f"|---------|--------|-----|-----|-----|-----|",
        ]
        for s in t.get("by_symbol", []):
            lines.append(f"| {s['symbol']} | {s['trades']} | {s['wr_pct']}% | {fmt_pnl(s['pnl'])} | {fmt_pnl(s['avg_pnl'])} | {s['buy']}B/{s['sell']}S |")

    lines += [
        f"",
        f"## 3. Sinais Rejeitados",
        f"",
        f"**Total rejeitado:** {rej.get('total', 0)}",
        f"",
    ]
    if rej.get("by_category"):
        lines.append("| Categoria | Qtd | % |")
        lines.append("|-----------|-----|---|")
        total_rej = rej["total"]
        for cat, cnt in rej["by_category"].items():
            lines.append(f"| {cat} | {cnt} | {cnt/total_rej*100:.1f}% |")

    if rej.get("top_reasons"):
        lines += [f"", f"**Top motivos:**", f""]
        for item in rej["top_reasons"][:5]:
            lines.append(f"- `{item['reason']}` — {item['count']}x")

    lines += [
        f"",
        f"## 4. Trades Abertos Atualmente",
        f"",
    ]
    if open_trades:
        lines.append(f"**{len(open_trades)} trade(s) aberto(s):**")
        lines.append("")
        for o in open_trades:
            lines.append(f"- {o['symbol']} {o['type']} @ {o.get('price','?')} desde {fmt_dt(o['created_at'])}")
    else:
        lines.append("Nenhum trade aberto no momento.")

    lines += [
        f"",
        f"## 5. Logs de Sessão",
        f"",
        f"**Total de eventos:** {logs.get('total', 0)}",
        f"",
    ]
    if logs.get("events"):
        for ev, cnt in logs["events"].items():
            lines.append(f"- `{ev}`: {cnt}x")
    if logs.get("errors"):
        lines += [f"", f"**Erros registrados:**", f""]
        for e in logs["errors"]:
            lines.append(f"- [{e['time']}] `{e['event']}`: {e['message']}")

    lines += [
        f"",
        f"---",
        f"*Relatório gerado automaticamente pelo ETL Report — Trade Liquidez v6.0*",
    ]

    return "\n".join(lines)

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="ETL Report — relatório completo para análise IA")
    p.add_argument("--from",    dest="date_from", help="data início YYYY-MM-DD")
    p.add_argument("--to",      dest="date_to",   help="data fim YYYY-MM-DD")
    p.add_argument("--full",    action="store_true", help="sem filtro de data (tudo)")
    p.add_argument("--session", action="store_true", help="usar sessão atual como início")
    p.add_argument("--format",  choices=["json", "markdown", "both"], default="both")
    args = p.parse_args()

    print(SEP)
    print("  ETL REPORT — Trade Liquidez v6.0")
    print(DASH)

    # Determinar período
    date_from = args.date_from
    date_to   = args.date_to
    session_start = None

    if args.session:
        session_start = get_session_start()
        print(f"  Sessão desde: {fmt_dt(session_start)}")
        # Para session: sem filtro de data (usar session_start direto na query)
        date_from = session_start[:10]
    elif args.full:
        date_from = None
        date_to   = None
        print("  Modo: FULL (sem filtro de data)")
    elif not date_from:
        # Padrão: hoje
        date_from = datetime.now().strftime("%Y-%m-%d")
        print(f"  Padrão: hoje ({date_from})")

    period_str = f"{date_from or 'início'} → {date_to or 'agora'}"
    print(f"  Período: {period_str}")
    print(DASH)

    print("  Coletando trades...", end=" ", flush=True)
    trades = collect_trades(date_from, date_to)
    print(f"{len(trades)} fechados")

    print("  Coletando rejeições...", end=" ", flush=True)
    rejections = collect_rejections(date_from, date_to)
    print(f"{len(rejections)} sinais")

    print("  Coletando logs...", end=" ", flush=True)
    logs = collect_bot_logs(date_from, date_to)
    print(f"{len(logs)} eventos")

    print("  Coletando trades abertos...", end=" ", flush=True)
    open_trades = collect_all_open()
    print(f"{len(open_trades)} abertos")

    print(DASH)
    print("  Analisando dados...")

    report = {
        "meta": {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "period": period_str,
            "session_start": fmt_dt(session_start) if session_start else None,
            "version": "6.0"
        },
        "trades":      analyze_trades(trades),
        "rejections":  analyze_rejections(rejections),
        "bot_logs":    analyze_logs(logs),
        "open_trades": open_trades
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = os.path.join(os.path.dirname(__file__), f"etl_report_{ts}")

    if args.format in ("json", "both"):
        json_path = base_path + ".json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        print(f"  JSON exportado: {json_path}")

    if args.format in ("markdown", "both"):
        md_path = base_path + ".md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(to_markdown(report))
        print(f"  Markdown exportado: {md_path}")

    # Console summary
    t = report["trades"]
    if t.get("total", 0) > 0:
        print(DASH)
        print(f"  Trades: {t['total']}  |  WR: {t['wr_pct']}%  |  P&L: {fmt_pnl(t['total_pnl'])}")
        print(f"  R/R: {t['rr_ratio']}x  |  Expectancy: {fmt_pnl(t['expectancy'])}  |  Max DD: ${t['max_drawdown']:.2f}")
        print(f"  Rejeitados: {report['rejections'].get('total',0)}")

    print(f"\n  Relatório gerado com sucesso.")
    print(SEP)

if __name__ == "__main__":
    main()
