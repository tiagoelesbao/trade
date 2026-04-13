import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Caminho absoluto para evitar erros
env_path = r"C:\Users\Pichau\Desktop\trade\.env"
load_dotenv(env_path)

url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    print(f"Erro: NEXT_PUBLIC_SUPABASE_URL ou SUPABASE_SERVICE_ROLE_KEY não encontradas no .env")
    exit(1)

supabase: Client = create_client(url, key)

def clean_database():
    print("🧹 Iniciando limpeza de dados de teste...")
    
    # 1. Deletar sinais com o comentário "SIMULADO"
    # Fazemos um loop simples para garantir o delete e reportar dados
    try:
        res_signals = supabase.table("signals_liquidez").delete().ilike("comment", "%SIMULADO%").execute()
        count_signals = len(res_signals.data) if res_signals.data else 0
        print(f"✅ Sinais de teste removidos: {count_signals}")
        
        # 2. Deletar heartbeats
        res_hb = supabase.table("bot_heartbeats").delete().eq("symbol", "EURUSD").execute()
        count_hb = len(res_hb.data) if res_hb.data else 0
        print(f"✅ Heartbeats de teste removidos: {count_hb}")
        
    except Exception as e:
        print(f"❌ Erro durante a limpeza: {e}")

if __name__ == "__main__":
    clean_database()
