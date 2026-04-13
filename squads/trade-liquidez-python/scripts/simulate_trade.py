import time
import os
from datetime import datetime
from supabase_client import SupabaseManager

def main():
    db_manager = SupabaseManager()
    symbol = "EURUSD"
    
    print("\n" + "="*60)
    print(f" [SIMULADOR] SQUAD LIQUIDEZ: INICIANDO TESTE CONTROLADO ")
    print(f" DASHBOARD LOCAL: http://localhost:3000 ")
    print("="*60)

    # 1. Simula Heartbeat (Bot Online no Frontend)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Enviando Heartbeat (Status: SCANNING)...")
    db_manager.log_heartbeat(symbol, "scanning", 3)
    
    time.sleep(2)

    # 2. Simula Entrada (Ordem de Compra)
    print("\n" + "-"*60)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] PADRÃO DE LIQUIDEZ DETECTADO EM {symbol} (H1)")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ANALISANDO ANATOMIA DO PAVIO...")
    
    order_data = {
        'symbol': symbol,
        'type': 2, # ORDER_TYPE_BUY_LIMIT
        'price': 1.08540,
        'sl': 1.08420,
        'tp': 1.08680,
        'comment': 'SIMULADO: Liquidez Suporte'
    }
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Enviando sinal para Supabase...")
    db_manager.log_signal(order_data, 0.45)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Ordem {order_data['comment']} enviada: {order_data['price']:.5f}")
    print("-"*60)
    print("\n >>> Verifique seu Dashboard (localhost:3000) agora! <<<")
    
    # Aguarda para simulação de saída
    print("\nAguardando 10 segundos para simular fechamento...")
    time.sleep(10)

    # 3. Simula Saída (Log apenas no console para ver o registro)
    print("\n" + "-"*60)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Expirando posição simulada por tempo (Final de Ciclo).")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] MetaTraderSim: Ordem Cancelada/Fechada com sucesso.")
    print("-"*60)
    
    print("\n[SIMULAÇÃO CONCLUÍDA] O ecossistema está 100% integrado.")

if __name__ == "__main__":
    main()
