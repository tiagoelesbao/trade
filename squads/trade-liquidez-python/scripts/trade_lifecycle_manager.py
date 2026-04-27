"""
Trade Lifecycle Manager - Gerenciamento de Estados de Trade
=============================================================
Gerencia o ciclo de vida completo de um trade com estados claros.
Falhas são logadas via SystemLogger — não silenciadas.
"""

import os
from datetime import datetime, timezone
from supabase import create_client
from dotenv import load_dotenv

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")


def _utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


class TradeLifecycleManager:
    """Gerenciador de ciclo de vida de trades. Falhas são logadas via SystemLogger."""

    STATES = {
        'signal_detected':    'Sinal técnico detectado',
        'awaiting_consensus': 'Aguardando aprovação da sala de guerra',
        'approved':           'Aprovado para execução',
        'rejected':           'Rejeitado pela sala de guerra',
        'filled':             'Ordem executada no MT5',
        'open':               'Trade ativo (posição aberta)',
        'closed':             'Trade finalizado',
        'error':              'Erro na execução'
    }

    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise Exception("Credenciais Supabase não encontradas")
        self.client = create_client(SUPABASE_URL, SUPABASE_KEY)
        # Logger é lazy — import circular evitado
        self._logger = None

    @property
    def logger(self):
        if self._logger is None:
            from system_logger import SystemLogger
            self._logger = SystemLogger("LIFECYCLE")
        return self._logger

    def _log_failure(self, op: str, signal_id=None, position_id=None, error: Exception = None):
        self.logger.error(
            f"lifecycle_{op}_failed",
            f"{op}: {error}",
            data={
                "signal_id": str(signal_id) if signal_id else None,
                "position_id": position_id,
                "error": str(error),
            }
        )

    def create_signal(self, symbol, trade_type, price, sl, tp, wick_pct, magic_number):
        signal = {
            "symbol": symbol,
            "type": trade_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "status": "signal_detected",
            "wick_pct": wick_pct,
            "magic": magic_number,
            "pnl": None,
            "position_id": None,
            "created_at": _utc_now_iso(),
            "agent_opinions": []
        }
        try:
            result = self.client.table("signals_liquidez").insert(signal).execute()
            return result.data[0]
        except Exception as e:
            self._log_failure("create_signal", error=e)
            return None

    def transition_to_awaiting_consensus(self, signal_id):
        try:
            self.client.table("signals_liquidez").update({
                "status": "awaiting_consensus",
                "updated_at": _utc_now_iso()
            }).eq("id", signal_id).execute()
            return True
        except Exception as e:
            self._log_failure("transition_awaiting_consensus", signal_id=signal_id, error=e)
            return False

    def approve_signal(self, signal_id, agent_opinions):
        try:
            self.client.table("signals_liquidez").update({
                "status": "approved",
                "agent_opinions": agent_opinions,
                "approved_at": _utc_now_iso()
            }).eq("id", signal_id).execute()
            return True
        except Exception as e:
            self._log_failure("approve_signal", signal_id=signal_id, error=e)
            return False

    def reject_signal(self, signal_id, reason):
        try:
            self.client.table("signals_liquidez").update({
                "status": "rejected",
                "reject_reason": reason,
                "updated_at": _utc_now_iso()
            }).eq("id", signal_id).execute()
            return True
        except Exception as e:
            self._log_failure("reject_signal", signal_id=signal_id, error=e)
            return False

    def mark_as_filled(self, signal_id, position_id):
        try:
            self.client.table("signals_liquidez").update({
                "status": "filled",
                "position_id": position_id,
                "filled_at": _utc_now_iso()
            }).eq("id", signal_id).execute()
            return True
        except Exception as e:
            self._log_failure("mark_as_filled", signal_id=signal_id, position_id=position_id, error=e)
            return False

    def mark_as_open(self, signal_id):
        try:
            self.client.table("signals_liquidez").update({
                "status": "open",
                "updated_at": _utc_now_iso()
            }).eq("id", signal_id).execute()
            return True
        except Exception as e:
            self._log_failure("mark_as_open", signal_id=signal_id, error=e)
            return False

    def close_trade(self, position_id, pnl, exit_price):
        try:
            result = self.client.table("signals_liquidez").select("*").eq("position_id", position_id).execute()
            if not result.data:
                self.logger.warning(
                    "close_trade_no_match",
                    f"Nenhum trade encontrado para position_id={position_id}",
                    data={"position_id": position_id, "pnl": pnl}
                )
                return False
            trade = result.data[0]
            self.client.table("signals_liquidez").update({
                "status": "closed",
                "pnl": pnl,
                "exit_price": exit_price,
                "closed_at": _utc_now_iso()
            }).eq("id", trade['id']).execute()
            return True
        except Exception as e:
            self._log_failure("close_trade", position_id=position_id, error=e)
            return False

    def mark_as_error(self, signal_id, error_message):
        try:
            self.client.table("signals_liquidez").update({
                "status": "error",
                "error_message": error_message,
                "updated_at": _utc_now_iso()
            }).eq("id", signal_id).execute()
            return True
        except Exception as e:
            self._log_failure("mark_as_error", signal_id=signal_id, error=e)
            return False

    def get_signal_by_id(self, signal_id):
        try:
            result = self.client.table("signals_liquidez").select("*").eq("id", signal_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            self._log_failure("get_signal_by_id", signal_id=signal_id, error=e)
            return None

    def get_signal_by_position_id(self, position_id):
        try:
            result = self.client.table("signals_liquidez").select("*").eq("position_id", position_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            self._log_failure("get_signal_by_position_id", position_id=position_id, error=e)
            return None

    def get_pending_signals(self, status='signal_detected'):
        try:
            result = self.client.table("signals_liquidez").select("*").eq("status", status).execute()
            return result.data
        except Exception as e:
            self._log_failure(f"get_pending_signals({status})", error=e)
            return []

    def cleanup_duplicates(self):
        try:
            all_trades = self.client.table("signals_liquidez").select("*").execute().data
            by_position = {}
            for trade in all_trades:
                pos_id = trade.get('position_id')
                if pos_id and pos_id != 0:
                    by_position.setdefault(pos_id, []).append(trade)
            to_delete = []
            for trades in by_position.values():
                if len(trades) > 1:
                    trades.sort(key=lambda x: x.get('created_at', ''), reverse=True)
                    to_delete.extend(t['id'] for t in trades[1:])
            for trade_id in to_delete:
                self.client.table("signals_liquidez").delete().eq("id", trade_id).execute()
            return len(to_delete)
        except Exception as e:
            self._log_failure("cleanup_duplicates", error=e)
            return 0
