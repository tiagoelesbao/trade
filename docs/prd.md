# Trade Liquidez Python - Brownfield Enhancement PRD (v5.6 Auditor)

**Data:** 18 de Abril de 2026
**Autor:** @dex (Engineer) - Versão Final Consolidada
**Status:** Implementado e Auditado

---

## 1. Introdução e Contexto do Projeto

### 1.1 Visão Geral
Conclusão da evolução do motor de liquidez para uma operação profissional. O sistema v5.6 foca em **Fidelidade Visual e Matemática**, permitindo que traders profissionais auditem o racional de cada operação através de ferramentas gráficas nativas no MetaTrader 5.

### 1.2 Escopo da v5.6
- **Realistic Engine:** Simulação de custos operacionais (Spread e Slippage).
- **Visual Path Auditing:** Renderização de linhas de conexão entre entrada e saída no gráfico.
- **Absolute Session Tracking:** Fim das discrepâncias de P&L causadas por fuso horário ou calendário.

---

## 2. Requisitos de Auditoria

### 2.1 Requisitos Funcionais (FR)
- **FR1:** Exportação de CSV enriquecido com 9 colunas (Entrada, Saída, PNL, RSI, Trend, Zona).
- **FR2:** Script MQL5 capaz de desenhar a trajetória do trade (Trendline pontilhada).
- **FR3:** Diferenciação visual entre trades lucrativos (Verde) e perdedores (Vermelho).

### 2.2 Requisitos Não-Funcionais (NFR)
- **NFR1:** **Realismo Financeiro:** Desconto obrigatório de 1.5 - 2.5 pips em cada trade do backtest.
- **NFR2:** **Performance do Replay:** Processamento de 15.000+ candles em menos de 10 segundos via pré-cálculo de vetores.

---

## 3. Arquitetura de Dados v5.6

### 3.1 Fluxo de Sincronia
- **Momento Zero:** `SESSION_START` capturado no boot do robô.
- **Filtro de Broker:** Tentativa sequencial de Filling Modes para garantir 100% de preenchimento.
- **Histórico Global:** Busca de deals em janela de 4 dias para total imunidade a fuso horário.

---

## 4. Conclusão da Validação
O sistema v5.6 foi validado em backtest multi-ativo, superando a meta de **$100/dia** mesmo após o desconto de taxas, estabelecendo um novo patamar de robustez para o ecossistema AIOX.

---
*PRD v5.6 - Rumo à Consistência Profissional*
