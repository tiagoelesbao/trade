import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Localiza o .env na raiz do projeto usando caminho absoluto resolvido
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print(f"[ERRO CRÍTICO] Arquivo .env não encontrado em: {env_path}")

class SupabaseManager:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") # Bypasses RLS for backend bot
        if not url or not key:
            self.client = None
            print(f"[AVISO] Supabase desativado. Chaves ausentes no .env.")
        else:
            self.client = create_client(url, key)
            # Log de depuração mascarado para segurança
            masked_key = f"{key[:10]}...{key[-4:]}" if len(key) > 14 else "***"
            print(f"[Supabase] Conectado. Chave: {masked_key} (Service Role)")

    def log_heartbeat(self, symbol, status, active_zones):
        """Envia batimento cardíaco para o dashboard."""
        if not self.client: return
        try:
            data = {
                "symbol": symbol,
                "status": status,
                "active_zones": active_zones
            }
            # Upsert para manter apenas um registro por símbolo se quiser apenas o status atual
            # Ou insert para histórico. Vamos usar upsert no ID fixo ou apenas insert para simplicidade.
            self.client.table("bot_heartbeats").insert(data).execute()
        except Exception as e:
            if "PGRST205" in str(e) or "not find the table" in str(e).lower():
                print("[Supabase ALERT] Tabela 'bot_heartbeats' ausente. Rode o SQL Editor no painel Supabase.")
            else:
                print(f"[Supabase] Erro ao enviar heartbeat: {e}")

    def log_signal(self, order_data, wick_pct):
        """Registra um novo sinal de liquidez."""
        if not self.client: return
        try:
            data = {
                "symbol": order_data.get('symbol', 'EURUSD'),
                "type": "SELL" if "SELL" in order_data.get('comment', '') else "BUY",
                "price": order_data['price'],
                "sl": order_data['sl'],
                "tp": order_data['tp'],
                "magic": 123456,
                "wick_pct": wick_pct,
                "status": "pending"
            }
            self.client.table("signals_liquidez").insert(data).execute()
        except Exception as e:
            if "PGRST205" in str(e) or "not find the table" in str(e).lower():
                print("[Supabase ALERT] Tabela 'signals_liquidez' ausente. Rode o SQL Editor no painel Supabase.")
            else:
                print(f"[Supabase] Erro ao registrar sinal: {e}")
