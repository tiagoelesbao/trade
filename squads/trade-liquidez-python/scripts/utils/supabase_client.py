import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
import yaml

load_dotenv()

class SupabaseManager:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not key:
            print("❌ Erro: SUPABASE_URL ou KEY não encontradas no .env")
            self.client = None
        else:
            self.client = create_client(url, key)
            print(f"[Supabase] Conectado. Chave: {key[:10]}...{key[-4:]} (Service Role)")

    def log_signal(self, order_data, wick_pct, status="approved"):
        if not self.client: return None
        symbol = order_data.get('symbol', 'EURUSD')
        data = {
            "symbol": symbol,
            "type": "SELL" if "SELL" in str(order_data['type']) else "BUY",
            "price": order_data['price'],
            "status": status,
            "wick_pct": wick_pct,
            "magic": 123456,
            "agent_opinions": []
        }
        try:
            return self.client.table("signals_liquidez").insert(data).execute()
        except Exception as e:
            print(f"Erro ao logar sinal: {e}")
            return None

    def update_signal_pnl(self, signal_id, pnl):
        if not self.client: return
        try:
            self.client.table("signals_liquidez").update({
                "status": "closed",
                "pnl": pnl,
                "closed_at": datetime.now().isoformat()
            }).eq("id", signal_id).execute()
        except: pass

    def log_heartbeat(self, symbol, status, active_zones, pnl_today=0.0, pnl_total=0.0):
        """
        Heartbeat v5.6.4: Otimizado com UPSERT (Restrição Única validada).
        """
        if not self.client: return
        data = {
            "symbol": symbol,
            "status": status,
            "active_zones": active_zones,
            "pnl_today": pnl_today,
            "pnl_total": pnl_total,
            "created_at": datetime.now().isoformat()
        }
        try:
            # Sobrescreve o registro anterior do mesmo símbolo
            self.client.table("bot_heartbeats").upsert(data, on_conflict="symbol").execute()
        except Exception as e:
            print(f"Erro no heartbeat: {e}")
