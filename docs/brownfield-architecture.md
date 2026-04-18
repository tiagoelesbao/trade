# Trade Liquidez Python - Documento de Arquitetura Brownfield (v5.5 Sniper)

**Data:** 18 de Abril de 2026
**Autor:** @dex (Engineer)
**Status:** Consolidado (Versão Multi-Pair Profissional)

---

## 1. Introdução

Este documento captura a arquitetura final da v5.5 do projeto `trade-liquidez-python`, detalhando a integração entre o motor Python de alta performance e a camada agêntica AIOX.

### Evolução da Realidade
O sistema migrou de um protótipo de ativo único (WIN$) para uma **Central de Trading Global** capaz de monitorar e executar operações em 10+ mercados simultaneamente com paridade total de dados.

---

## 2. Referência de Arquivos (Fluxo v5.5)

### Componentes Críticos
- **Orquestrador:** `FULL_START.bat` (Gerencia o ciclo de vida do ambiente).
- **Motor Multi-Pair:** `squads/trade-liquidez-python/scripts/bot_liquidez.py`.
- **Integrador Cloud:** `squads/trade-liquidez-python/scripts/supabase_client.py`.
- **General de Guerra:** `squads/trade-liquidez-python/scripts/auto_war_room.py`.
- **Backtesting:** `squads/trade-liquidez-python/scripts/market_replay.py` (Engine Ultra-Veloz).

---

## 3. Arquitetura de Dados e Sincronia

### O Fluxo "High-Fidelity"
O sistema garante 100% de paridade entre Broker e Dashboard:
1.  **Sinal:** Python detecta pavio M15 em zona consolidada.
2.  **Aprovação:** Sala de Guerra AIOX valida via Supabase (JSONB Opinions).
3.  **Execução:** Ordem MARKET enviada ao MT5 com auto-filling (FOK/IOC).
4.  **Fechamento:** Python monitora o histórico de *deals* do MT5 e envia o P&L real ao fechar.

### Pilha Tecnológica v5.5
| Categoria | Tecnologia | Notas |
|----------|------------|-------|
| Runtime | Python 3.13 | Processamento paralelo de múltiplos ativos. |
| DB Cloud | Supabase | Barramento de eventos em tempo real. |
| Interface | Next.js 14 | Visualização consolidada de P&L Global. |
| Broker | MT5 | Terminal de execução com ponte CSV específica por par. |

---

## 4. O Squad de Liquidez v5.5

A estratégia Sniper é governada pela confluência de 3 pilares:
1.  **Zonas Micro (M15):** Inteligência de pontos de entrada frequentes.
2.  **Filtro Macro (SMA 20 H1):** Proteção contra tendências explosivas (faca caindo).
3.  **Oscilador (RSI 14):** Identificação de exaustão técnica e reversão de preço.

---

## 5. Resiliência Operacional

- **Erro 10030 (Filling Mode):** Mitigado via tentativa sequencial automática.
- **Fuso Horário:** Sincronizado via busca agressiva de histórico (Janela Broker vs Local).
- **Ambiente:** Sanitização automática via `clean_db.py` a cada novo boot.

---
*Documento consolidado após a grande atualização Multi-Pair Sniper v5.5.*
