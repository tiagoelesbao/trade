@echo off
title [AIOX] Watchdog: Liquidez Bot
echo ==================================================
echo   Iniciando Watchdog do Trade Liquidez
echo   O bot sera religado automaticamente em caso de crash
echo ==================================================

:loop
echo [%time%] Iniciando bot_liquidez.py...
python scripts\bot_liquidez.py
echo [%time%] O bot encontrou um erro ou foi fechado!
echo Reiniciando em 15 segundos para proteger conexao com MetaTrader...
timeout /t 15 /nobreak
goto loop
