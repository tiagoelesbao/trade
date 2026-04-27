"""
System Logger - Logs centralizados para todas as pontas do sistema
==================================================================
Escreve no Supabase (bot_logs) + console em tempo real.
"""

import os
from datetime import datetime, timezone, timedelta
import yaml
from supabase import create_client
from dotenv import load_dotenv

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# v6.1.3: timestamps do logger em timezone do servidor MT5
# (alinhado com bot_liquidez.py e auto_war_room.py — mt5_server_utc_offset do config)
_config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
try:
    with open(_config_path, 'r', encoding='utf-8') as _f:
        _CFG = yaml.safe_load(_f) or {}
    _MT5_UTC_OFFSET = int(_CFG.get('mt5_server_utc_offset', 3))
except Exception:
    _MT5_UTC_OFFSET = 3
MT5_TZ = timezone(timedelta(hours=_MT5_UTC_OFFSET))


def _now_mt5_ts() -> str:
    """Timestamp HH:MM:SS no timezone do servidor MT5 (alinha logs com chart)."""
    return datetime.now(MT5_TZ).strftime("%H:%M:%S")

LEVEL_PREFIX = {
    "INFO":    "  ",
    "WARNING": "⚠ ",
    "ERROR":   "✗ ",
    "TRADE":   "$ ",
    "SIGNAL":  "◈ ",
}

# Pesos máximos por critério (v6.1.2 — RSI alpha, Slope/Volume removidos)
SCORE_MAX = {
    'rsi': 35, 'wick': 25, 'pin_bar': 20,
    'session': 15, 'history': 5,
}
SCORE_LABELS = {
    'rsi':     'RSI    ', 'wick':    'Wick   ',
    'pin_bar': 'PinBar ', 'session': 'Sessao ',
    'history': 'Hist   ',
}
SCORE_KEYS_ORDER = ['rsi', 'wick', 'pin_bar', 'session', 'history']

def _mini_bar(pts, max_pts, width=14):
    filled = round((pts / max_pts) * width) if max_pts else 0
    return "#" * filled + "-" * (width - filled)


class SystemLogger:
    """Logger centralizado. Fallback para console se Supabase indisponível."""

    def __init__(self, source: str):
        self.source = source
        self._enabled = False
        try:
            self.client = create_client(SUPABASE_URL, SUPABASE_KEY)
            self._enabled = True
        except Exception as e:
            print(f"[LOGGER] Supabase indisponível, apenas console: {e}")

    def _log(self, level: str, event: str, message: str,
             data: dict = None, symbol: str = None, trade_id: str = None):
        ts     = _now_mt5_ts()
        prefix = LEVEL_PREFIX.get(level, "  ")
        sym_part = f" [{symbol}]" if symbol else ""
        print(f"[{ts}][{self.source}]{sym_part} {prefix}{event}: {message}")

        if not self._enabled:
            return
        try:
            self.client.table("bot_logs").insert({
                "source":   self.source,
                "level":    level,
                "event":    event,
                "message":  message,
                "data":     data or {},
                "symbol":   symbol,
                "trade_id": str(trade_id) if trade_id else None,
            }).execute()
        except Exception as e:
            print(f"[LOGGER] Falha ao gravar log: {e}")

    # ── Métodos públicos básicos ───────────────────────────────────────────────

    def info(self, event: str, message: str, **kwargs):
        self._log("INFO", event, message, **kwargs)

    def warning(self, event: str, message: str, **kwargs):
        self._log("WARNING", event, message, **kwargs)

    def error(self, event: str, message: str, **kwargs):
        self._log("ERROR", event, message, **kwargs)

    def trade(self, event: str, message: str, **kwargs):
        self._log("TRADE", event, message, **kwargs)

    def signal(self, event: str, message: str, **kwargs):
        self._log("SIGNAL", event, message, **kwargs)

    # ── Método especializado: análise completa de sinal ───────────────────────

    def signal_analysis(self, signal_info: dict, scores: dict, raw: dict,
                        opinions: list, verdict: str, reason: str = ""):
        """
        Imprime breakdown completo de análise de sinal no console
        e grava registro estruturado no Supabase (bot_logs).

        Parâmetros:
          signal_info  — dict com symbol, type, price, wick_pct, sl, tp
          scores       — dict com pts por critério (wick, pin_bar, rsi, ...)
          raw          — dict com valores brutos (rsi, body_ratio, slope_pips, ...)
          opinions     — lista de opiniões dos agentes
          verdict      — "APROVADO" | "REJEITADO" | "PRETERIDO"
          reason       — motivo textual (ex: "Score 47.3 < 55")
        """
        sym        = signal_info.get('symbol', '?')
        typ        = signal_info.get('type', '?')
        wick_pct   = signal_info.get('wick_pct', 0) * 100
        price      = signal_info.get('price', 0)
        sl         = signal_info.get('sl', 0)
        tp         = signal_info.get('tp', 0)
        total      = round(sum(scores.values()), 1)
        min_score  = 55  # importar do war room seria circular; mantemos aqui

        ts = _now_mt5_ts()

        # ── Console: cabeçalho ────────────────────────────────────────────────
        icon   = "✓" if verdict == "APROVADO" else ("✗" if verdict == "REJEITADO" else "○")
        v_mark = f"\033[92m{verdict}\033[0m" if verdict == "APROVADO" else \
                 (f"\033[91m{verdict}\033[0m" if verdict == "REJEITADO" else verdict)

        diff   = total - min_score
        diff_s = f"+{diff:.1f}" if diff >= 0 else f"{diff:.1f}"

        print(f"\n[{ts}][{self.source}] [{sym}] ◈ signal_analysis:")
        print(f"   {icon} {sym} {typ}  @{price:.5f}  "
              f"SL:{sl:.5f}  TP:{tp:.5f}  pavio:{wick_pct:.0f}%")
        print(f"   {'─'*60}")

        # ── Console: breakdown por critério (v6.1.2 — 5 critérios) ───────────
        for key in SCORE_KEYS_ORDER:
            if key not in scores:
                continue
            pts   = scores[key]
            mx    = SCORE_MAX.get(key, 10)
            label = SCORE_LABELS.get(key, key)
            bar   = _mini_bar(pts, mx)

            # Detalhe contextual
            if key == 'rsi':
                detail = f"RSI {raw.get('rsi', 0):.1f}"
            elif key == 'wick':
                detail = f"pavio {wick_pct:.0f}%"
            elif key == 'pin_bar':
                br = raw.get('body_ratio', 0)
                q  = ("perfeito" if pts >= 17 else "bom" if pts >= 10
                      else "aceitável" if pts >= 5 else "suja")
                detail = f"corpo {br:.0f}% range  [{q}]"
            elif key == 'session':
                detail = raw.get('session', '?')
            elif key == 'history':
                wr = raw.get('symbol_wr', 0)
                ht = raw.get('hist_trades', 0)
                detail = f"WR {wr:.0f}%  ({ht}T / 30d)"
            else:
                detail = ''

            pct_fill = (pts / mx * 100) if mx else 0
            print(f"   {label}  [{bar}]  {pts:>4}/{mx}  ({pct_fill:>5.1f}%)  {detail}")

        # ── Console: total + veredito ─────────────────────────────────────────
        total_bar = _mini_bar(total, 100, width=20)
        print(f"   {'─'*60}")
        print(f"   TOTAL   [{total_bar}]  {total:>5}/100  ({diff_s} pts vs mínimo {min_score})")

        # Critério mais fraco
        if scores:
            weakest_k = min(scores, key=lambda k: scores[k] / SCORE_MAX.get(k, 1))
            weakest_v = scores[weakest_k]
            weakest_m = SCORE_MAX.get(weakest_k, 10)
            print(f"   Pior critério: {SCORE_LABELS.get(weakest_k, weakest_k).strip()} "
                  f"{weakest_v}/{weakest_m}  "
                  f"({weakest_v/weakest_m*100:.0f}% do máximo)")

        if reason:
            print(f"   → {verdict}  —  {reason}")
        else:
            print(f"   → {verdict}")

        # ── Console: opiniões dos agentes ─────────────────────────────────────
        if opinions:
            print(f"   {'─'*60}")
            for op in opinions:
                conf = op.get('confidence', 0)
                av   = op.get('avatar', '??')
                name = op.get('agent', '?')
                comm = op.get('comment', '')
                print(f"   [{av}] {name:<15}  {conf:>3}%  \"{comm}\"")

        # ── Supabase: registro estruturado ────────────────────────────────────
        # Gera texto multi-linha para o campo 'message' (visível na página /logs)
        lines = [
            f"{icon} {sym} {typ}  Score {total}/100  {verdict}  ({diff_s} pts)",
        ]
        for key in SCORE_KEYS_ORDER:
            if key not in scores:
                continue
            pts = scores[key]
            mx  = SCORE_MAX.get(key, 10)
            lines.append(f"  {SCORE_LABELS.get(key, key)} {pts}/{mx}")
        if reason:
            lines.append(f"  Motivo: {reason}")
        for op in (opinions or []):
            lines.append(f"  [{op.get('avatar','?')}] {op.get('comment','')}")
        message_text = "\n".join(lines)

        # Payload estruturado para o campo 'data' (JSON)
        analysis_payload = {
            "verdict":      verdict,
            "total_score":  total,
            "min_score":    min_score,
            "diff":         round(diff, 1),
            "reason":       reason,
            "signal": {
                "symbol":   sym,
                "type":     typ,
                "price":    price,
                "sl":       sl,
                "tp":       tp,
                "wick_pct": round(wick_pct, 1),
            },
            "scores":   scores,
            "raw":      raw,
            "opinions": [
                {
                    "agent":      op.get("agent"),
                    "confidence": op.get("confidence"),
                    "comment":    op.get("comment"),
                }
                for op in (opinions or [])
            ],
        }

        if not self._enabled:
            return
        try:
            level = "INFO" if verdict == "APROVADO" else "WARNING"
            self.client.table("bot_logs").insert({
                "source":  self.source,
                "level":   level,
                "event":   f"signal_{verdict.lower()}",
                "message": message_text,
                "data":    analysis_payload,
                "symbol":  sym,
            }).execute()
        except Exception as e:
            print(f"[LOGGER] Falha ao gravar signal_analysis: {e}")
