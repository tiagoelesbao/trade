# Trade Analysis Kit — Pipeline LLM Pós-Trade

**Status:** Bootstrap operacional (Onda 5)
**Tipo:** Pipeline OFFLINE — não pertence ao runtime de trading

---

## 1. Propósito

Pipeline de análise multiagente que roda **após a sessão** sobre prints de trades + logs de bot/War Room para produzir relatório consolidado por trade e fechamento diário. Usa 9 agentes especializados (Huddleston ICT, Simons quant, Taleb risk, etc.) via OpenRouter LLM.

**Importante:** este pipeline **não modifica o bot, a estratégia ou config**. Toda recomendação fica em markdown — execução é decisão humana.

---

## 2. Componentes

```
squads/trade-liquidez-python/
├── scripts/
│   └── trade_analysis_engine.py            # Pipeline Python (offline, OpenRouter LLM)
├── scripts/runner_analisar_trades.bat      # Entrada CLI (orquestra workflow)
├── workflows/
│   └── trade_analysis_workflow.yaml        # Definição de etapas
├── tasks/                                  # Contratos por tipo de operação
├── templates/                              # Templates MD/JSON de saída
├── checklists/                             # Validações de qualidade
└── agents/                                 # Definições de cada agente (.md)
```

---

## 3. Como rodar

### Modo dry-run (validação sem chamar LLM)
```bat
scripts\runner_analisar_trades.bat ^
  --input "squads\trade-liquidez-python\data\trades\Abril\Semana 01\2026-04-24" ^
  --dry-run --verbose
```

### Modo full (com OpenRouter)
```bat
set OPENROUTER_API_KEY=sk-or-v1-...
scripts\runner_analisar_trades.bat ^
  --input "squads\trade-liquidez-python\data\trades\Abril\Semana 01\2026-04-24" ^
  --mode full --verbose
```

### Parâmetros
- `--input <path>` (obrigatório) — pasta do dia com prints e logs
- `--mode quick|full` (default `full`) — `quick`=5 agentes núcleo, `full`=9 agentes
- `--output <path>` (opcional) — destino dos artefatos consolidados
- `--date YYYY-MM-DD` (opcional) — override da data de referência
- `--dry-run` — valida contratos sem processar análises
- `--verbose` — detalha logs operacionais

### Modelo LLM
- Padrão: `google/gemini-2.0-flash-001` (definido em `trade_analysis_engine.call_llm_analysis`)
- Sem `OPENROUTER_API_KEY`: fallback simulado (`simulate_agent_analysis`)

---

## 4. Inputs esperados

Pasta do dia com:
- **Prints de trade** (`.png`, `.jpg`, `.jpeg`) — nomenclatura `[HH_MMh][SYMBOL][RESULTADO].png`
  - Exemplo: `[17_26h][EURGBP][-$102,76].png`
- **Logs de entrada/sessão** (`.md`, `.txt`, `.log`) — bot/lifecycle
- **Logs de War Room** (`.md`) — análise dos sinais (com "warroom" no nome)

Classificação automática em `classify_log()`:
- "warroom" → log de consenso
- "autoriz", "entrada", "signal", "bot" → log operacional/ciclo
- "session" → log de sessão completa

---

## 5. Outputs por execução

### Por trade (em pasta com mesma nomenclatura do print)
```
[17_26h][EURGBP][-$102,76]/
├── analysis_packet.json        # Pacote único entregue aos agentes
├── analise/
│   ├── huddleston_ict_parecer.json + .md
│   ├── simons_quant_parecer.json + .md
│   ├── taleb_risk_parecer.json + .md
│   ├── ... (1 par .json/.md por agente)
│   └── consenso_divergencia.json
├── evidencias/
│   └── [17_26h][EURGBP][-$102,76].png   # Print copiado
├── analise_consolidada.md
└── metadados_trade.json
```

### Por dia (raiz da pasta de saída)
```
output/
├── input_index.json
├── prints_index.json
├── logs_index.json
├── trade_catalog.json
├── trades/<trade_id_visual>/...   # como acima, por trade
├── fechamento_dia.md
├── resumo_quantitativo_dia.json
├── pendencias_dia.json
└── indice_trade_reports.json
```

---

## 6. Agentes

### Núcleo (modo `quick`, 5 agentes)
| Agente | Foco analítico |
|--------|----------------|
| `huddleston_ict` | Liquidez, sweep, displacement, contexto estrutural ICT/SMC |
| `simons_quant` | Coerência quantitativa do setup (RSI/wick/pin/session/history) |
| `taleb_risk` | Assimetria, risco de ruína, fragilidade operacional |
| `dalio_portfolio` | Conflito de exposição e correlação no dia |
| `kahneman_process` | Qualidade da decisão vs viés de resultado |

### Complementares (modo `full`, +4 agentes)
| Agente | Foco analítico |
|--------|----------------|
| `soros_regime` | Adequação ao regime de mercado no momento do trade |
| `chan_systems` | Robustez metodológica e consistência de sistema |
| `davey_validation` | Disciplina de validação e critérios de evolução |
| `lopezdeprado_research` | Risco de data snooping/leakage e rigor inferencial |

### Schema do parecer (`<agent_id>_parecer.json`)
```json
{
  "agent_id": "huddleston_ict",
  "analysis_status": "ok | partial | inconclusive | error",
  "confidence": 0..100,
  "thesis_assessment": "confirmada | parcial | refutada | inconclusiva",
  "primary_findings": [...],
  "risk_findings": [...],
  "data_gaps": [...],
  "counterfactual": "...",
  "recommended_actions": [...],
  "evidence_refs": [...],
  "summary_md": "..."
}
```

---

## 7. Quorum e validade

| Modo | Mínimo de pareceres válidos | Status final |
|------|------------------------------|--------------|
| `quick` | 4 de 5 com `analysis_status in (ok, partial)` | `valid` ou `valid_with_warnings` |
| `full` | 7 de 9 | idem |

Se agente crítico (`taleb_risk` ou `huddleston_ict`) falhar → flag de revisão obrigatória.

Status final de análise por trade:
- `valid` — quorum atingido sem lacunas críticas
- `valid_with_warnings` — quorum atingido com lacunas relevantes
- `incomplete` — quorum não atingido

---

## 8. Princípios inegociáveis

1. **Sem evidência, sem conclusão.**
2. **Divergência entre agentes deve ser explícita** — nunca apagada.
3. **Falta de dado vira flag de qualidade** — nunca ocultar.
4. **Não sobrescrever artefatos sem versionamento** — reprocessamento explícito.
5. **Nenhuma recomendação altera bot/config automaticamente.**

---

## 9. Política de fallback externo (OpenRouter)

- **Local-first por padrão.** Pipeline funciona sem LLM (modo simulado para testes).
- **OpenRouter apenas via flag explícita** (`--enable-openrouter-fallback` ou `OPENROUTER_API_KEY` set).
- **Credencial via env, nunca hardcoded.**
- **Telemetria mínima:** `fallback_used`, `fallback_reason`, `fallback_status` no run log.
- **Modo degradado** se LLM falhar: continua com simulação + flag de qualidade.

---

## 10. Status atual

| Componente | Status |
|------------|--------|
| `runner_analisar_trades.bat` | ✅ Bootstrap operacional |
| `trade_analysis_engine.py` | ✅ Funcional com OpenRouter + fallback simulado |
| `workflows/trade_analysis_workflow.yaml` | ✅ Definido |
| `agents/` (definições .md) | ✅ 9 agentes |
| `tasks/` | ✅ Definidos |
| `templates/` | ✅ Templates MD/JSON |
| `checklists/` | ✅ Gates de qualidade |

Para histórico completo das ondas de planejamento (1-5), checklists detalhados e contratos por etapa, consultar arquivos em `squads/trade-liquidez-python/{workflows,tasks,templates,checklists}/`.

---

## 11. Próximos passos

- Validar pipeline em volume de dias variados (atualmente bootstrap)
- Refinar prompts dos agentes para reduzir variância LLM
- Adicionar export para DB (atualmente só MD/JSON em disco)
- Integrar com Vercel/dashboard (apresentar consolidado diário no frontend)
