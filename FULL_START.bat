@echo off
title [AIOX] Orquestrador de Sessão: Trade-Liquidez v3.5 (Guerra)
color 0B

echo ==================================================
echo   ECOSSISTEMA TRADE-LIQUIDEZ: MODO OFENSIVO
echo ==================================================
echo.

:: FASE 1: Inteligencia de Abertura (@analyst)
echo [1/4] @analyst iniciando analise de pre-sessao...
echo Analisando mercado e ajustando config.yaml...
python squads/trade-liquidez-python/scripts/diagnose_today.py
echo ✅ Configuracao Otimizada Salva em config.yaml

echo.
:: FASE 2: Interface de Comando (Frontend)
echo [2/4] Iniciando Dashboard Next.js (Porta 3000)...
start "Dashboard" cmd /c "cd app && npm run dev"

echo.
:: FASE 3: General de Guerra (Aprovação Automática)
echo [3/4] Iniciando General de Guerra (Auto-Approve)...
start "General de Guerra" cmd /c "python squads/trade-liquidez-python/scripts/auto_war_room.py"

echo.
:: FASE 4: Motor de Execucao (Python)
echo [4/4] Iniciando Robo de Liquidez (Python)...
:: O robo agora vai rodar e se auto-encerrar ao bater a meta
start "Robo de Liquidez" cmd /c "cd squads\trade-liquidez-python && run_watchdog.bat"

echo.
echo ==================================================
echo   SISTEMA ONLINE E EM MODO OFENSIVO!
echo   Aprovação Automática Ativa (General de Guerra).
echo   O robo encerrara automaticamente ao bater a meta.
echo ==================================================
echo.
echo Pressione qualquer tecla para ver as janelas de log...
pause
