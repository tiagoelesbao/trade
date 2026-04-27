"""
ETL DB Audit — Auditoria de integridade do banco de dados
==========================================================
Uso:
  python etl_db_audit.py              # audit somente (dry-run)
  python etl_db_audit.py --fix        # corrigir problemas identificados
  python etl_db_audit.py --output json
  python etl_db_audit.py --verbose    # mostrar cada registro problemático

Verifica:
  1. Trades 'closed' com pnl=NULL ou pnl=0 (sync bug)
  2. Trades 'open' há mais de 24h (stuck trades)
  3. Duplicatas por position_id
  4. Registros sem symbol ou sem type
  5. Sinais com status inválido
  6. Trades com preço de entrada = 0
  7. Registros antigos com dados corrompidos (pre-v5)
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

VALID_STATUSES = {"signal_detected", "awaiting_consensus", "approved", "rejected",
                  "filled", "open", "closed", "error", "cancelled"}

issues = []  # lista global de problemas encontrados

def add_issue(check, severity, count, description, ids=None, fix_fn=None):
    issues.append({
        "check": check,
        "severity": severity,  # CRITICAL / WARNING / INFO
        "count": count,
        "description": description,
        "ids": ids or [],
        "fix_fn": fix_fn
    })

def fmt_dt(iso):
    if not iso: return "—"
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%d/%m %H:%M")
    except:
        return iso[:16]

# ─── Checks ───────────────────────────────────────────────────────────────────

def check_closed_null_pnl(verbose):
    res = client.table("signals_liquidez")\
        .select("id,symbol,closed_at,created_at")\
        .eq("status", "closed")\
        .is_("pnl", "null")\
        .execute()
    data = res.data or []
    if data:
        if verbose:
            for r in data[:20]:
                print(f"    [{r['id'][:8]}] {r['symbol']} closed_at={fmt_dt(r.get('closed_at'))}")
        add_issue("closed_null_pnl", "CRITICAL", len(data),
                  "Trades 'closed' com pnl=NULL — não atualizados no fechamento",
                  [r["id"] for r in data])
    return data

def check_closed_zero_pnl(verbose):
    res = client.table("signals_liquidez")\
        .select("id,symbol,closed_at,created_at,price,exit_price")\
        .eq("status", "closed")\
        .eq("pnl", 0)\
        .execute()
    data = res.data or []
    # Exclui breakeven legítimos onde entry != exit
    suspect = [r for r in data if r.get("price") and r.get("exit_price") and
               abs(r["price"] - r["exit_price"]) > 0.00001]
    if suspect:
        if verbose:
            for r in suspect[:20]:
                print(f"    [{r['id'][:8]}] {r['symbol']} entry={r.get('price','?'):.5f} exit={r.get('exit_price','?'):.5f}")
        add_issue("closed_zero_pnl", "WARNING", len(suspect),
                  "Trades 'closed' com pnl=0 mas entry≠exit (sync bug provável)",
                  [r["id"] for r in suspect])
    return suspect

def check_stuck_open(verbose):
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
    res = client.table("signals_liquidez")\
        .select("id,symbol,type,created_at,position_id")\
        .eq("status", "open")\
        .lte("created_at", cutoff)\
        .execute()
    data = res.data or []
    if data:
        if verbose:
            for r in data[:20]:
                print(f"    [{r['id'][:8]}] {r['symbol']} {r['type']} desde {fmt_dt(r['created_at'])}")

        def fix_stuck():
            for r in data:
                client.table("signals_liquidez")\
                    .update({"status": "error", "reject_reason": "audit: stuck open >24h"})\
                    .eq("id", r["id"])\
                    .execute()
            return len(data)

        add_issue("stuck_open", "CRITICAL", len(data),
                  "Trades 'open' há mais de 24h (possível falha no fechamento)",
                  [r["id"] for r in data], fix_fn=fix_stuck)
    return data

def check_duplicate_position_id(verbose):
    res = client.table("signals_liquidez")\
        .select("id,symbol,status,position_id,created_at")\
        .neq("status", "rejected")\
        .not_.is_("position_id", "null")\
        .execute()
    data = res.data or []
    by_pos = defaultdict(list)
    for r in data:
        if r.get("position_id"):
            by_pos[r["position_id"]].append(r)
    dupes = {k: v for k, v in by_pos.items() if len(v) > 1}
    if dupes:
        ids = [r["id"] for v in dupes.values() for r in v]
        if verbose:
            for pos_id, recs in list(dupes.items())[:10]:
                syms = [f"{r['symbol']}({r['status']})" for r in recs]
                print(f"    pos_id={pos_id}: {', '.join(syms)}")
        add_issue("duplicate_position_id", "WARNING", len(dupes),
                  f"position_id duplicado em {len(dupes)} grupos ({len(ids)} registros)",
                  ids)
    return dupes

def check_invalid_status(verbose):
    res = client.table("signals_liquidez")\
        .select("id,symbol,status,created_at")\
        .execute()
    data = res.data or []
    invalid = [r for r in data if r.get("status") not in VALID_STATUSES]
    if invalid:
        if verbose:
            for r in invalid[:20]:
                print(f"    [{r['id'][:8]}] {r['symbol']} status='{r['status']}'")
        add_issue("invalid_status", "WARNING", len(invalid),
                  f"Registros com status inválido: {set(r['status'] for r in invalid)}",
                  [r["id"] for r in invalid])
    return invalid

def check_missing_fields(verbose):
    res = client.table("signals_liquidez")\
        .select("id,symbol,type,status,created_at")\
        .execute()
    data = res.data or []
    bad = [r for r in data if not r.get("symbol") or not r.get("type")]
    if bad:
        if verbose:
            for r in bad[:20]:
                print(f"    [{r['id'][:8]}] symbol='{r.get('symbol')}' type='{r.get('type')}'")
        add_issue("missing_fields", "WARNING", len(bad),
                  "Registros sem symbol ou type",
                  [r["id"] for r in bad])
    return bad

def check_zero_entry_price(verbose):
    res = client.table("signals_liquidez")\
        .select("id,symbol,status,price,created_at")\
        .eq("price", 0)\
        .execute()
    data = res.data or []
    # Só preocupa para trades que chegaram a fill
    active = [r for r in data if r.get("status") in ("open", "closed", "filled")]
    if active:
        if verbose:
            for r in active[:20]:
                print(f"    [{r['id'][:8]}] {r['symbol']} status={r['status']}")
        add_issue("zero_entry_price", "WARNING", len(active),
                  "Trades com price=0 e status ativo/fechado",
                  [r["id"] for r in active])
    return active

def check_old_orphans(verbose):
    cutoff = "2026-01-01T00:00:00"
    res = client.table("signals_liquidez")\
        .select("id,symbol,status,created_at,pnl")\
        .lte("created_at", cutoff)\
        .execute()
    data = res.data or []
    if data:
        if verbose:
            for r in data[:20]:
                print(f"    [{r['id'][:8]}] {r['symbol']} {r['status']} {fmt_dt(r['created_at'])}")
        add_issue("old_orphans", "INFO", len(data),
                  f"Registros anteriores a 2026-01-01 ({len(data)} total) — dados pré-v5",
                  [r["id"] for r in data])
    return data

# ─── Apply fixes ──────────────────────────────────────────────────────────────

def apply_fixes():
    fixed = 0
    for issue in issues:
        if issue.get("fix_fn") and issue["severity"] in ("CRITICAL", "WARNING"):
            print(f"\n  Corrigindo: {issue['check']} ({issue['count']} registros)...")
            try:
                n = issue["fix_fn"]()
                print(f"    ✓ {n} registros corrigidos")
                fixed += n
            except Exception as e:
                print(f"    ✗ Erro: {e}")
    return fixed

# ─── Report ───────────────────────────────────────────────────────────────────

def print_report(args):
    sev_icon = {"CRITICAL": "🔴", "WARNING": "🟡", "INFO": "🔵"}
    criticals = [i for i in issues if i["severity"] == "CRITICAL"]
    warnings  = [i for i in issues if i["severity"] == "WARNING"]
    infos     = [i for i in issues if i["severity"] == "INFO"]

    print(DASH)
    total_issues = len(criticals) + len(warnings)
    if total_issues == 0:
        print("  ✅ Banco de dados íntegro — nenhum problema encontrado.")
    else:
        print(f"  Resultado: {len(criticals)} CRITICAL  {len(warnings)} WARNING  {len(infos)} INFO")

    print(DASH)
    for issue in issues:
        icon = sev_icon.get(issue["severity"], "  ")
        fix_hint = "  [corrigível com --fix]" if issue.get("fix_fn") else ""
        print(f"  {icon} [{issue['severity']:<8}] {issue['check']:<28} {issue['count']:>4} registros{fix_hint}")
        print(f"       {issue['description']}")

    if args.fix and total_issues > 0:
        print(DASH)
        print("  Aplicando correções automáticas...")
        n = apply_fixes()
        print(f"\n  Total corrigido: {n} registros")

    print(f"\n  Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(SEP)

def export_json(args):
    output = {
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "critical": len([i for i in issues if i["severity"] == "CRITICAL"]),
            "warning":  len([i for i in issues if i["severity"] == "WARNING"]),
            "info":     len([i for i in issues if i["severity"] == "INFO"]),
        },
        "issues": [{k: v for k, v in i.items() if k != "fix_fn"} for i in issues]
    }
    path = os.path.join(os.path.dirname(__file__), f"etl_db_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)
    print(f"  JSON exportado: {path}")

def main():
    p = argparse.ArgumentParser(description="ETL DB Audit — auditoria de integridade do Supabase")
    p.add_argument("--fix",     action="store_true", help="corrigir problemas automáticos identificados")
    p.add_argument("--verbose", action="store_true", help="mostrar registros problemáticos individualmente")
    p.add_argument("--output",  choices=["table", "json"], default="table")
    args = p.parse_args()

    print(SEP)
    print("  ETL DB AUDIT — Trade Liquidez v6.0")
    if args.fix:
        print("  MODO: FIX (correções serão aplicadas)")
    else:
        print("  MODO: DRY-RUN (use --fix para corrigir)")
    print(DASH)

    checks = [
        ("1. closed pnl=NULL",      lambda: check_closed_null_pnl(args.verbose)),
        ("2. closed pnl=0 suspect",  lambda: check_closed_zero_pnl(args.verbose)),
        ("3. stuck open >24h",        lambda: check_stuck_open(args.verbose)),
        ("4. duplicate position_id",  lambda: check_duplicate_position_id(args.verbose)),
        ("5. invalid status",         lambda: check_invalid_status(args.verbose)),
        ("6. missing fields",         lambda: check_missing_fields(args.verbose)),
        ("7. zero entry price",       lambda: check_zero_entry_price(args.verbose)),
        ("8. old records pre-2026",   lambda: check_old_orphans(args.verbose)),
    ]

    for label, fn in checks:
        print(f"  Verificando {label}...", end=" ", flush=True)
        result = fn()
        count = len(result) if isinstance(result, (list, dict)) else 0
        print(f"{'OK' if count == 0 else f'{count} problema(s)'}")
        if args.verbose and count > 0:
            pass  # verbose output already printed inside check fn

    if args.output == "json":
        export_json(args)
    else:
        print_report(args)

if __name__ == "__main__":
    main()
