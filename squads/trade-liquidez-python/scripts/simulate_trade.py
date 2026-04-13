import time
import os
from datetime import datetime
import MetaTrader5 as mt5
from supabase_client import SupabaseManager

def export_to_mt5(indicator_file, zones, order_data):
    """Escreve no arquivo que o indicador MQL5 lê."""
    try:
        with open(indicator_file, "w", encoding="ansi") as f:
            f.write("HEADER\n") # Para o mq5 pular
            # Simula algumas zonas para o gráfico não ficar vazio
            for z in zones:
                f.write(f"ZONE_{z['type']},{z['price']},{datetime.now()}\n")
            
            # Escreve o sinal de entrada
            if order_data:
                type_str = "SIGNAL_BUY" if order_data['type'] == 2 else "SIGNAL_SELL"
                f.write(f"{type_str},{order_data['price']},{datetime.now()}\n")
        return True
    except Exception as e:
        print(f"[MT5 Sync Error] {e}")
        return False

def main():
    if not mt5.initialize():
        print("[ERRO] Não foi possível inicializar MetaTrader 5 para sincronia visual.")
        return

    data_path = mt5.terminal_info()._asdict().get('data_path')
    indicator_file = os.path.join(data_path, "MQL5", "Files", "liquidez_data.csv")
    
    db_manager = SupabaseManager()
    symbol = "EURUSD"
    
    print("\n" + "="*60)
    print(f" [SIMULADOR] SQUAD LIQUIDEZ: INICIANDO TESTE COM SYNC MT5 ")
    print(f" INDICADOR FILE: {indicator_file} ")
    print("="*60)

    # 1. Simula Heartbeat (Bot Online no Frontend)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Enviando Heartbeat (Status: SCANNING)...")
    db_manager.log_heartbeat(symbol, "scanning", 3)
    
    # Prepara zonas fakes para o gráfico
    fake_zones = [
        {'type': 'RESISTANCE', 'price': 1.08750},
        {'type': 'SUPPORT', 'price': 1.08500}
    ]
    export_to_mt5(indicator_file, fake_zones, None)

    time.sleep(2)

    # 2. Simula Entrada (Ordem de Compra)
    print("\n" + "-"*60)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] PADRÃO DE LIQUIDEZ DETECTADO EM {symbol}")
    
    order_data = {
        'symbol': symbol,
        'type': 2, # ORDER_TYPE_BUY_LIMIT
        'price': 1.08540,
        'sl': 1.08420,
        'tp': 1.08680,
        'comment': 'SIMULADO: Sync MT5'
    }
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Enviando sinal para Supabase e MT5...")
    db_manager.log_signal(order_data, 0.45)
    export_to_mt5(indicator_file, fake_zones, order_data)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Ordem enviada: {order_data['price']:.5f}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [SYNC SUCCESS] Verifique as setas no seu Gráfico MT5!")
    print("-"*60)
    
    # Aguarda para simulação de saída
    print("\nSimulação ativa. Aguardando 10 segundos para limpar o gráfico...")
    time.sleep(10)

    # 3. Limpa o arquivo (Simula fim de sinal)
    export_to_mt5(indicator_file, fake_zones, None)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Simulação de saída concluída.")
    
    mt5.shutdown()
    print("\n[SIMULAÇÃO CONCLUÍDA] Teste Visual MT5 e Nuvem Integrado.")

if __name__ == "__main__":
    main()
