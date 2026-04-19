# Trade Liquidez Python - Documento de Arquitetura Brownfield (v5.6 Auditor)

**Data:** 18 de Abril de 2026
**Autor:** @dex (Engineer)
**Status:** Consolidado (Versão Final de Auditoria)

---

## 1. Introdução

Este documento detalha a infraestrutura técnica da v5.6 Sniper, focada em precisão matemática e transparência visual para auditoria de alto nível.

---

## 2. Referência de Arquivos (Fluxo v5.6)

### Componentes de Auditoria
- **Auditor Visual:** `squads/trade-liquidez-python/scripts/AuditorBacktest.mq5` (Script de traçado de trajetórias).
- **Faxina Gráfica:** `squads/trade-liquidez-python/scripts/LimparGrafico.mq5` (Script de limpeza de objetos).
- **Motor Realista:** `squads/trade-liquidez-python/scripts/market_replay.py` (Simulador com custos operacionais).

---

## 3. Lógica de P&L Absoluto (v5.6.1)

Diferente das versões anteriores que usavam o horário do broker para filtrar o lucro de "hoje", a arquitetura v5.6.1 utiliza:
1.  **Fixed Timestamp:** O robô grava o segundo exato do boot em `SESSION_START`.
2.  **Cumulative Scan:** A busca de histórico (`history_deals_get`) é feita do boot até agora + 2h de margem.
3.  **Result:** Terminal e Dashboard ficam 100% sincronizados, ignorando viradas de meia-noite ou desencontros de fuso horário.

---

## 4. Auditoria de Trajetória (Visual Path)

A integração MT5-Python agora suporta o traçado do ciclo de vida do trade:
- **Camada 1 (Preço):** Preço de Entrada (Seta) e Preço de Saída (Pin).
- **Camada 2 (Vetor):** Trendline conectando ambos os pontos, colorida por PNL.
- **Camada 3 (Contexto):** Retângulo de zona e texto com valor de RSI e Trend no momento do gatilho.

---

## 5. Resiliência e Segurança

- **Auto-Filling:** Implementada a tentativa automática FOK -> IOC -> RETURN para furar bloqueios de preenchimento da corretora.
- **Error Protection:** O status no Dashboard só transiciona para ACTIVE se o terminal confirmar o `retcode` 10009 (Done).
- **Multi-Pair Dictionary:** O motor gerencia estados de sinais ativos por chave de símbolo, evitando colisões de dados em operações paralelas.

---
*Documentação técnica consolidada v5.6.*
