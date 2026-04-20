@echo off
title [AIOX] Orquestrador de Sessão: Trade-Liquidez v5.6 (Source of Truth)
color 0B

:: Define o caminho raiz para os scripts localizarem os módulos
set PYTHONPATH=%PYTHONPATH%;%CD%

echo ==================================================
echo   ECOSSISTEMA TRADE-LIQUIDEZ: MODO SNIPER v5.6
echo ==================================================
echo.

:: FASE 0: Sanidade do Ambiente (DESATIVADO PARA MODO 24/5)
:: echo [0/4] @qa limpando dados residuais de teste...
:: python squads/trade-liquidez-python/scripts/clean_db.py
echo [SISTEMA] Modo 24/5 Ativo: Preservando histórico semanal.

echo.
:: FASE 1: Inteligencia de Abertura (@analyst)
echo [1/4] @analyst iniciando analise de pre-sessao...
echo Diagnóstico do dia e ajuste de filtros no config.yaml...
python squads/trade-liquidez-python/scripts/diagnose_today.py
echo ✅ Configuracao Sniper Carregada.

echo.
:: FASE 2: Interface de Comando (Frontend)
echo [2/4] Iniciando Dashboard Next.js (Porta 3000)...
start "Dashboard" cmd /c "cd app && npm run dev"

echo.
:: FASE 3: Sala de Guerra (General de Guerra Agêntico)
echo [3/4] Iniciando General de Guerra (Aprovação Automática)...
start "General de Guerra" cmd /k "python squads/trade-liquidez-python/scripts/auto_war_room.py"

echo.
:: FASE 4: Motor de Execucao (Python)
echo [4/4] Iniciando Robo de Liquidez (Python)...
start "Robo de Liquidez" cmd /k "python squads/trade-liquidez-python/scripts/bot_liquidez.py"

echo.
echo ==================================================
echo   SISTEMA ONLINE E EM MODO SNIPER v5.6!
echo   Sincronia Total MetaTrader-Dashboard Ativa.
echo   P^&L calculado diretamente pelo Terminal Broker.
echo ==================================================
echo.
echo Pressione qualquer tecla para finalizar este orquestrador...
pause > nul
