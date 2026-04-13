# Trade Liquidez Python - Documento de Arquitetura Brownfield

**Data:** 11 de Abril de 2026
**Autor:** @architect (Aria)
**Status:** Atualizado via PRD de Integração

---

## 1. Introdução

Este documento captura o estado ATUAL (Realidade) do projeto `trade-liquidez-python` e define como a nova arquitetura de integração orquestrada por agentes AIOX será implementada sobre a base de código existente.

### Escopo do Documento
Focado na integração entre o framework AIOX (Node.js/TS) e o motor de execução de trading em Python localizado em `squads/trade-liquidez-python/scripts/`.

---

## 2. Referência Rápida - Arquivos e Pontos de Entrada

### Arquivos Críticos para Entendimento do Sistema
- **Motor de Execução Principal:** `squads/trade-liquidez-python/scripts/bot_liquidez.py` (Lógica de bot real-time).
- **Backtesting & Análise:** `squads/trade-liquidez-python/scripts/backtest_liquidez.py`.
- **Configuração do Squad:** `squads/trade-liquidez-python/squad.yaml`.
- **Configurações Gerais:** `squads/trade-liquidez-python/config.yaml`.
- **Pintor Gráfico (MT5/MQL5):** `squads/trade-liquidez-python/scripts/PintorLiquidez.mq5`.

### Áreas de Impacto do Novo PRD
- `squads/trade-liquidez-python/scripts/`: Adição de logging JSONL e Sanity Checks.
- `.aiox-core/development/tasks/`: Criação de novas tarefas para orquestração dos agentes.

---

## 3. Arquitetura de Alto Nível (Estado Atual)

### Resumo Técnico
O sistema utiliza uma abordagem de **Trading Algorítmico Candle a Candle** focado no ativo `WIN$` (Mini Índice B3), operando via integração MetaTrader 5 (MT5).

### Pilha Tecnológica Real
| Categoria | Tecnologia | Versão | Notas |
|----------|------------|---------|--------|
| Runtime | Python | 3.x | Dependência de `MetaTrader5`, `pandas`, `numpy`. |
| Orquestrador | AIOX Framework | 1.x | Gerencia os agentes e fluxos de trabalho. |
| Plataforma | MetaTrader 5 | Atual | Broker-interface obrigatória para execução. |

### Estrutura do Repositório (Realidade)
```text
C:\Users\Pichau\Desktop\trade\
├── squads/trade-liquidez-python/
│   ├── agents/          # Configurações específicas dos agentes do squad
│   ├── scripts/         # O "Motor": bots, backtests e ferramentas Python
│   ├── tasks/           # Definições de tarefas locais do squad
│   ├── squad.yaml       # Definição dos papéis (Simons, Druckenmiller, etc.)
│   └── run_watchdog.bat # Utilitário de monitoramento local
├── .aiox-core/          # O Core do framework (Orquestração)
└── docs/prd.md          # Documento de requisitos para a integração
```

---

## 4. O Squad de Liquidez

O projeto possui um squad especializado baseado em figuras lendárias do mercado:

1. **Stanley Druckenmiller (Macro Agent):** Valida contexto H1 (tendência institucional).
2. **Jim Simons (Quant Agent):** Analisa gatilhos estatísticos em M5 (geometria de pavios/volatilidade).
3. **Paul Tudor Jones (Execution Agent):** Gerencia o envio de ordens `LIMIT` a 50% do pavio.
4. **Nassim Taleb (Risk Agent):** Aplica a regra estrita de saída em 6 candles para evitar "caudas longas" perdedoras.

---

## 5. Dívida Técnica e Pontos de Atenção

1. **Comunicação Acoplada:** Atualmente, os scripts Python e os agentes AIOX operam de forma independente (via shell direto). Falta uma ponte de estado compartilhada.
2. **Logs Textuais:** Os scripts geram logs para visualização humana, dificultando a automação de auditoria pelos agentes QA.
3. **Gerenciamento de Erros:** Se o MT5 desconectar, o script Python falha, mas o agente AIOX pode não detectar a falha imediatamente.

---

## 6. Padrões de Integração (Propostos no PRD)

Com a nova integração (PRD Melhorado pela Aria):

- **Bridge de Logs:** Mudança para **JSONL** em todos os scripts Python em `scripts/`.
- **Sanity Checks:** Cada script verificará chaves de API e conexão MT5 antes do loop principal.
- **Daemon Mode:** Suporte para que `bot_liquidez.py` rode continuamente, reportando status via pulso (heartbeat).

---

## 7. Comandos Úteis

```bash
# Executar backtest de liquidez
python squads/trade-liquidez-python/scripts/backtest_liquidez.py

# Iniciar o bot de produção
python squads/trade-liquidez-python/scripts/bot_liquidez.py
```

---
*Documento gerado automaticamente pela @architect baseando-se no PRD de 11/04/2026.*
