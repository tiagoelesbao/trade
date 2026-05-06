"""
Terminal Log Writer — Persistência local de rolling logs.

Cada terminal (BOT, EXIT_WR) tem um deque em memória para exibição visual e
um writer em arquivo (data/terminal_logs/{source}_{YYYYMMDD}.log) para
auditoria persistente sem depender do Supabase.

API:
  writer = TerminalLogWriter(source="BOT")
  writer.append("18:51:35  SINAL  USDCHF SELL @ 0.79116  -> War Room")

Comportamento:
  - Rotação diária automática (data muda no nome do arquivo)
  - Append-only com flush imediato (não perde se processo cair)
  - Cria diretório data/terminal_logs/ se não existir
"""

import os
from datetime import datetime, timezone


def _resolve_log_dir() -> str:
    """data/terminal_logs/ na raiz do squad."""
    here = os.path.dirname(os.path.abspath(__file__))
    squad_root = os.path.dirname(here)   # scripts/ -> ../
    log_dir = os.path.join(squad_root, "data", "terminal_logs")
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


class TerminalLogWriter:
    """Append rolling log a arquivo por dia. Thread-safe para escritas simples."""

    def __init__(self, source: str):
        self.source = source
        self.log_dir = _resolve_log_dir()
        self._current_date: str = ""
        self._fh = None
        self._open_today()

    def _open_today(self):
        """(Re)abre arquivo do dia atual em append. Fecha o anterior se existir."""
        today = datetime.now().strftime("%Y%m%d")
        if today == self._current_date and self._fh is not None:
            return
        if self._fh is not None:
            try:
                self._fh.close()
            except Exception:
                pass
        path = os.path.join(self.log_dir, f"{self.source}_{today}.log")
        self._fh = open(path, "a", encoding="utf-8", buffering=1)  # line-buffered
        self._current_date = today
        # Marca abertura
        self._fh.write(f"\n=== Sessao iniciada {datetime.now().isoformat()} ({self.source}) ===\n")
        self._fh.flush()

    def append(self, line: str):
        """Escreve uma linha. Garante \\n no final. Auto-rotaciona se mudou o dia."""
        try:
            self._open_today()
            if not line.endswith("\n"):
                line = line + "\n"
            self._fh.write(line)
            self._fh.flush()
        except Exception:
            # Silenciar — terminal log é suporte, não pode derrubar o bot
            pass

    def close(self):
        if self._fh is not None:
            try:
                self._fh.close()
            except Exception:
                pass
            self._fh = None
