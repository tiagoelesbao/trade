import os
import sys
import yaml
import random
import time

# Permite acesso à mesma pasta
sys.path.append(os.path.dirname(__file__))
from market_replay import run_replay

CFG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")

def load_base_cfg():
    with open(CFG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_optimizer(iterations=20):
    print("="*50)
    print("INICIANDO JIM SIMONS (Quant Optimizer Agent)")
    print(f"Executando {iterations} permutações aleatórias cegas...")
    print("Isso pode levar alguns minutos (Walk-Forward pesado em background)")
    print("="*50)

    base_cfg = load_base_cfg()
    
    # Ranges de otimização (Search Space)
    cooldown_range = [6, 8, 12, 18, 24]
    retracement_range = [0.40, 0.50, 0.60, 0.70]
    breakeven_range = [2, 3, 4]
    exit_range = [5, 6, 8]
    
    best_pnl = -9999
    best_cfg = None

    start_time = time.time()

    for i in range(iterations):
        # Gera mutação
        test_cfg = base_cfg.copy()
        test_cfg['cooldown_candles'] = random.choice(cooldown_range)
        test_cfg['entry_retracement_pct'] = random.choice(retracement_range)
        test_cfg['breakeven_candles'] = random.choice(breakeven_range)
        test_cfg['exit_candles_max'] = random.choice(exit_range)
        
        print(f"[{i+1}/{iterations}] Testando [Cool:{test_cfg['cooldown_candles']} Retr:{test_cfg['entry_retracement_pct']} Bk:{test_cfg['breakeven_candles']} Exit:{test_cfg['exit_candles_max']}]...")
        
        # Roda o motor cego
        pnl, win_rate, _ = run_replay(custom_cfg=test_cfg, silent=True)
        
        if pnl > best_pnl:
            best_pnl = pnl
            best_cfg = test_cfg.copy()
            print(f"   [NOVO LIDER] PNL Maximo Encontrado: ${pnl:.2f} (WR: {win_rate:.2f}%)")

    elapsed = time.time() - start_time
    print("="*50)
    print(f"OTIMIZACAO CONCLUIDA em {elapsed:.1f} segundos!")
    print(f"Melhor Resultado Financeiro: ${best_pnl:.2f}")
    
    if best_cfg:
        with open(CFG_PATH, "w", encoding="utf-8") as f:
            yaml.dump(best_cfg, f, default_flow_style=False)
        print("[SUCESSO] config.yaml foi atualizado automaticamente com a melhor configuracao!")

if __name__ == "__main__":
    run_optimizer(iterations=2) # 2 para rodar rápido se bater na mao
