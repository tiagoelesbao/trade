@echo off
title [AIOX] Lançador Unificado: Trade-Liquidez v2.0
color 0B

echo ==================================================
echo   INICIANDO ECOSSISTEMA TRADE-LIQUIDEZ v2.0
echo ==================================================
echo.
echo [1/2] Iniciando Dashboard Next.js (Porta 3000)...
start "Dashboard Frontend" cmd /c "cd app && npm run dev"

echo [2/2] Iniciando Robô de Liquidez (Python)...
start "Robo de Liquidez" cmd /c "cd squads\trade-liquidez-python && run_watchdog.bat"

echo.
echo ==================================================
echo   SISTEMA ONLINE!
echo   Dashboard: http://localhost:3000
echo   Robo:      Ver Janela Separada
echo ==================================================
pause
