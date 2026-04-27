import MetaTrader5 as mt5
import pandas as pd
import os
from datetime import datetime, timedelta
import pytz

# Configurações
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "ml_dataset.csv")

def get_session_report():
    if not mt5.initialize():
        print("Erro ao conectar ao MT5")
        return

    print("="*60)
    print("SQUAD LIQUIDEZ: AUDITORIA DE SESSAO")
    print("="*60)

    # 1. Carregar Sinais de ML
    if not os.path.exists(CSV_PATH):
        print("Nenhum dado de ML encontrado ainda.")
        mt5.shutdown()
        return

    df_ml = pd.read_csv(CSV_PATH)
    df_ml['time'] = pd.to_datetime(df_ml['time'])
    
    # Pegar apenas o dia de hoje (Segunda 13/04)
    today = datetime.now(pytz.utc).date()
    # today_signals = df_ml[df_ml['time'].dt.date == today] # Para uso real
    today_signals = df_ml # Mostra tudo para demonstração agora
    
    if today_signals.empty:
        print("Nenhum sinal detectado hoje até agora.")
        mt5.shutdown()
        return

    print(f"Sinais detectados hoje: {len(today_signals)}")
    
    # 2. Buscar Trades no MT5
    from_date = datetime.now() - timedelta(days=1)
    deals = mt5.history_deals_get(from_date, datetime.now(), group="*")
    
    trades = []
    if deals:
        df_deals = pd.DataFrame(list(deals), columns=deals[0]._as_dict().keys())
        # Filtrar pelo Magic Number (caso o bot tenha magic cadastrado)
        # Note: bot_liquidez usa 123456 por padrão
        df_deals = df_deals[df_deals['magic'] == 123456]
        
        # Agrupar entradas e saídas por ticket de posição
        for pos_id in df_deals['position_id'].unique():
            pos_deals = df_deals[df_deals['position_id'] == pos_id]
            if len(pos_deals) >= 2:
                # Simplificação: assume primeira entrada e última saída
                entry = pos_deals.iloc[0]
                exit = pos_deals.iloc[-1]
                pnl = pos_deals['profit'].sum() + pos_deals['commission'].sum() + pos_deals['swap'].sum()
                trades.append({
                    'time': datetime.fromtimestamp(entry['time'], tz=pytz.utc),
                    'pnl': pnl,
                    'type': 'BUY' if entry['type'] == mt5.ORDER_TYPE_BUY else 'SELL'
                })

    # 3. Cruzamento e Insights
    report_md = f"# Auditoria de Sessão: {today}\n\n"
    report_md += f"- **Sinais Capturados:** {len(today_signals)}\n"
    report_md += f"- **Ordens Executadas:** {len(trades)}\n\n"
    
    print(f"Ordens executadas (MT5): {len(trades)}")
    
    if len(today_signals) > 0:
        avg_wick = today_signals['top_wick_pct'].mean() if not today_signals['top_wick_pct'].isnull().all() else 0
        print(f"Média de Pavio (Superior): {avg_wick*100:.1f}%")
        
        report_md += "## Métricas Quantitativas (ML)\n"
        report_md += f"| Métrica | Valor Médio |\n|---|---|\n"
        report_md += f"| Top Wick % | {avg_wick*100:.1f}% |\n"
        report_md += f"| Bottom Wick % | {today_signals['bottom_wick_pct'].mean()*100:.1f}% |\n"
        report_md += f"| Volume Momentum | {today_signals['volume_momentum'].mean():.0f} |\n\n"

    if trades:
        win_rate = len([t for t in trades if t['pnl'] > 0]) / len(trades) * 100
        print(f"Taxa de Acerto Real: {win_rate:.1f}%")
        report_md += f"## Performance Financeira\n- **Win Rate:** {win_rate:.1f}%\n"
        report_md += f"- **PNL Total:** ${sum(t['pnl'] for t in trades):.2f}\n"

    # Salvar Relatório
    report_path = os.path.join(BASE_DIR, "docs", f"audit_{today}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)
        
    print(f"\n[SUCESSO] Relatório detalhado salvo em: docs/audit_{today}.md")
    mt5.shutdown()

if __name__ == "__main__":
    get_session_report()
