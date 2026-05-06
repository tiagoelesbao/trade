"""
Cooldown Manager — Bloqueio direcional pós-loss.
=======================================================================
Sprint 6.1 (v6.2.0-ict).

Após loss confirmado em (symbol, direction), bloqueia novas entradas na MESMA
combinação por `cooldown_hours_after_loss` horas (default 4h). Resolve cluster
de losses consecutivos no mesmo par/direção (visto em 30/04: 3 USDCHF BUY
losses seguidos em 2h, todos seguindo a estratégia mas mercado não respeitou).

Estado persistido em data/cooldowns.json para sobreviver reinício do bot.
Compatível com bot e war room (cache compartilhado de leitura).

API:
  manager = CooldownManager()
  is_blocked, until = manager.check(symbol, trade_type)  # consulta
  manager.register_loss(symbol, trade_type)              # registra após loss
  manager.cleanup_expired()                              # poda entries velhas

Persistência:
  data/cooldowns.json — { "USDCHF:BUY": "2026-04-30T13:42:00+00:00", ... }
"""

import os
import json
import yaml
from datetime import datetime, timezone, timedelta
from typing import Tuple, Optional


def _resolve_state_path() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    squad_root = os.path.dirname(here)
    data_dir = os.path.join(squad_root, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "cooldowns.json")


def _resolve_config() -> dict:
    here = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(os.path.dirname(here), "config.yaml")
    try:
        with open(cfg_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


class CooldownManager:
    """
    Gerencia cooldowns direcionais por (symbol, direction).
    Singleton-friendly: cada processo tem sua própria instância, mas todos
    leem/escrevem o mesmo arquivo JSON. Race condition é tolerável aqui
    porque a perda é só um warning duplo, não uma execução errada.
    """

    def __init__(self):
        cfg = _resolve_config()
        self.enabled       = bool(cfg.get('cooldown_after_loss_enabled', True))
        self.cooldown_h    = float(cfg.get('cooldown_hours_after_loss', 4.0))
        self.state_path    = _resolve_state_path()
        # Cache em memória — recarregado a cada operação (TTL implícito de poucos ms)
        self._cache: dict = {}
        self._cache_mtime: float = 0.0

    # ── Persistência ─────────────────────────────────────────────────────

    def _load(self) -> dict:
        """Carrega estado do disco. Cache via mtime."""
        try:
            mtime = os.path.getmtime(self.state_path)
        except Exception:
            return {}
        if mtime != self._cache_mtime:
            try:
                with open(self.state_path, 'r', encoding='utf-8') as f:
                    self._cache = json.load(f) or {}
                self._cache_mtime = mtime
            except Exception:
                self._cache = {}
        return self._cache

    def _save(self, data: dict):
        try:
            with open(self.state_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            self._cache = data
            self._cache_mtime = os.path.getmtime(self.state_path)
        except Exception:
            pass

    @staticmethod
    def _key(symbol: str, trade_type: str) -> str:
        return f"{symbol.upper()}:{trade_type.upper()}"

    # ── API pública ──────────────────────────────────────────────────────

    def check(self, symbol: str, trade_type: str) -> Tuple[bool, Optional[datetime]]:
        """
        Retorna (blocked: bool, until_utc: datetime|None).

        blocked=True quando há cooldown ativo para (symbol, trade_type).
        """
        if not self.enabled:
            return False, None

        data = self._load()
        key = self._key(symbol, trade_type)
        until_iso = data.get(key)
        if not until_iso:
            return False, None

        try:
            until_dt = datetime.fromisoformat(until_iso.replace('Z', '+00:00'))
        except Exception:
            return False, None

        now = datetime.now(timezone.utc)
        if now >= until_dt:
            # Expirou — remove e libera
            data.pop(key, None)
            self._save(data)
            return False, None

        return True, until_dt

    def register_loss(self, symbol: str, trade_type: str,
                      cooldown_hours: Optional[float] = None) -> datetime:
        """
        Registra um loss em (symbol, trade_type) e ativa cooldown.
        Retorna timestamp UTC de quando expira.
        """
        if not self.enabled:
            return datetime.now(timezone.utc)

        h = cooldown_hours if cooldown_hours is not None else self.cooldown_h
        until = datetime.now(timezone.utc) + timedelta(hours=h)
        data = self._load()
        data[self._key(symbol, trade_type)] = until.isoformat()
        self._save(data)
        return until

    def cleanup_expired(self) -> int:
        """Remove entries expirados. Retorna quantos foram removidos."""
        if not self.enabled:
            return 0
        data = self._load()
        now = datetime.now(timezone.utc)
        removed = 0
        for key in list(data.keys()):
            try:
                until_dt = datetime.fromisoformat(data[key].replace('Z', '+00:00'))
                if now >= until_dt:
                    data.pop(key)
                    removed += 1
            except Exception:
                data.pop(key, None)
                removed += 1
        if removed > 0:
            self._save(data)
        return removed

    def list_active(self) -> list:
        """Lista cooldowns ativos: [(symbol, type, until_utc, remaining_minutes), ...]"""
        if not self.enabled:
            return []
        data = self._load()
        now = datetime.now(timezone.utc)
        out = []
        for key, until_iso in data.items():
            try:
                until_dt = datetime.fromisoformat(until_iso.replace('Z', '+00:00'))
                if now < until_dt:
                    sym, typ = key.split(":")
                    remaining = int((until_dt - now).total_seconds() / 60)
                    out.append((sym, typ, until_dt, remaining))
            except Exception:
                continue
        return out
