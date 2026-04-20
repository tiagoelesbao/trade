import MetaTrader5 as mt5
from datetime import datetime, timedelta
import os
import yaml
import sys

# Carrega Config
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
with open(config_path, "r", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

sys.path.append(os.path.dirname(__file__))
from supabase_client import SupabaseManager
db = SupabaseManager()

def sync():
    if not mt5.initialize(): return
    print("🚀 INICIANDO SINCRONIA DE LIMPEZA...")

    # 1. Pega histórico real total (desde o início da conta)
    from_date = datetime(2020, 1, 1)
    deals = mt5.history_deals_get(from_date, datetime.now() + timedelta(days=1))
    
    if not deals:
        print("Nenhum trade encontrado no MT5.")
        return

    # 2. Limpa o banco de dados de sinais duplicados/errados para recomeçar limpo
    # (Apenas para sinais desse robô)
    print("🧹 Limpando registros antigos para re-sincronização...")
    db.client.table("signals_liquidez").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()

    # 3. Insere cada trade do histórico real uma única vez
    inserted = 0
    for d in deals:
        if d.magic != CFG['magic_number'] or d.entry != 1: continue
        
        in_deals = mt5.history_deals_get(position=d.position_id)
        if not in_deals: continue
        
        pnl = d.profit + d.commission + d.swap
        entry_time = datetime.fromtimestamp(in_deals[0].time).isoformat()
        
        new_trade = {
            "symbol": d.symbol,
            "type": "BUY" if in_deals[0].type == 0 else "SELL",
            "price": in_deals[0].price,
            "status": "closed",
            "pnl": pnl,
            "magic": d.position_id, # Usamos o campo magic para guardar o ID da POSIÇÃO e evitar duplicidade
            "wick_pct": 0.5,
            "agent_opinions": [{"agent": "Auditor", "comment": "Sincronizado via Relatório Real", "sentiment": "neutral"}],
            "created_at": entry_time,
            "closed_at": datetime.fromtimestamp(d.time).isoformat()
        }
        
        db.client.table("signals_liquidez").insert(new_trade).execute()
        inserted += 1
        print(f"✅ Sincronizado: {d.symbol} | PNL: {pnl:.2f}")

    print(f"\n✨ Sincronia concluída! {inserted} trades reais restaurados.")
    mt5.shutdown()

if __name__ == "__main__":
    sync()
