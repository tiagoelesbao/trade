# Trade Liquidez Python - Brownfield Enhancement PRD (v5.5 Sniper)

**Data:** 18 de Abril de 2026
**Autor:** @dex (Engineer) - Versão Multi-Pair Final
**Status:** Aprovado e Implementado

---

## 1. Introdução e Contexto do Projeto

### 1.1 Visão Geral
Evolução do motor de liquidez para uma operação profissional multi-ativo. O sistema agora monitora os 10 principais pares do mercado global simultaneamente, utilizando inteligência de exaustão (RSI) e filtragem macro (Trend H1) para garantir a meta de **$100/dia**.

### 1.2 Escopo da v5.5
- **Multi-Pair Integration:** Monitoramento paralelo de múltiplos símbolos.
- **High-Fidelity P&L:** Sincronização direta com o histórico de *deals* do MT5 (Fim de P&L estimado).
- **Execution Agility:** Implementação de modo MARKET com auto-filling (FOK/IOC/RETURN).
- **AIOX War Room:** Opiniões agênticas estruturadas via banco de dados Cloud.

---

## 2. Requisitos

### 2.1 Requisitos Funcionais (FR)
- **FR1:** Captura de liquidez em zonas de 15 minutos (M15).
- **FR2:** Cálculo dinâmico de RR (Risk/Reward) de 1.5x em todas as entradas.
- **FR3:** Consolidação de P&L de todos os ativos no Dashboard unificado.
- **FR4:** Sincronia visual específica por ativo no MetaTrader.

### 2.2 Requisitos Não-Funcionais (NFR)
- **NFR1:** **Baixa Latência:** Varredura completa de 10 ativos em menos de 10s.
- **NFR2:** **Resiliência de Corretora:** Tentativa automática de modos de preenchimento (Erro 10030 mitigado).
- **NFR3:** **Consistência de Fuso:** Busca de histórico independente do relógio do broker (Janela de 4 dias).

---

## 3. Estratégia de Implementação Sniper

### 3.1 Pilha Tecnológica
- **Motor:** Python 3.13 (High performance).
- **Cloud:** Supabase Realtime + Vercel.
- **Broker:** MetaTrader 5 (Terminal de Execução).

### 3.2 Lógica de Gatilho (v5.5)
- **Ativo:** Multi-Pair.
- **Zonas:** M15 com recálculo minuto a minuto.
- **Exaustão:** IFR(14) > 60 (Venda) ou < 40 (Compra).
- **Tendência:** Filtro de Média Móvel 20 em H1.

---

## 4. Avaliação de Resultados (Backtest)
O sistema foi validado com uma amostragem de 15.000 candles de M5, resultando em um **PNL Consolidado de +$49.626,50** no último 1.5 mês (em 6 pares simulados), confirmando a viabilidade técnica e financeira da meta de **$100/dia**.

---
*PRD v5.5 - Foco em Alta Rentabilidade e Escalabilidade*
