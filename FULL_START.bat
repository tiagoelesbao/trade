@echo off
title [AIOX] Orquestrador de Sessão: Trade-Liquidez v3.0
color 0B

echo ==================================================
echo   ECOSSISTEMA TRADE-LIQUIDEZ: CICLO AUTONOMO
echo ==================================================
echo.

:: FASE 1: Inteligencia de Abertura (@analyst)
echo [1/3] @analyst iniciando analise de pre-sessao...
:: Nota: Chamar via CLI AIOX (ajustar conforme ambiente)
echo Analisando mercado e ajustando config.yaml...
python squads/trade-liquidez-python/scripts/diagnose_today.py
echo ✅ Configuracao Otimizada Salva em config.yaml

echo.
:: FASE 2: Interface de Comando (Frontend)
echo [2/3] Iniciando Dashboard Next.js (Porta 3000)...
start "Dashboard" cmd /c "cd app && npm run dev"

echo.
:: FASE 3: Motor de Execucao (Python)
echo [3/3] Iniciando Robo de Liquidez (Python)...
:: O robo agora vai rodar e se auto-encerrar ao bater a meta
start "Robo de Liquidez" cmd /c "cd squads\trade-liquidez-python && run_watchdog.bat"

echo.
echo ==================================================
echo   SISTEMA ONLINE E OPERANDO AUTONOMAMENTE!
echo   O robo encerrara automaticamente ao bater a meta.
echo ==================================================
echo.
echo Pressione qualquer tecla para ver as janelas de log...
pause
