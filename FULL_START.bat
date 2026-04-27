@echo off
title [AIOX] Orquestrador -- Trade Liquidez v6.0
color 0B
chcp 65001 > nul

set PYTHONPATH=%PYTHONPATH%;%CD%

echo.
echo ===================================================================
echo   TRADE LIQUIDEZ v6.0  --  LIFECYCLE ARCHITECTURE
echo   Orquestrador de Sessao  --  %DATE%  %TIME:~0,8%
echo ===================================================================
echo.
echo   Componentes que serao iniciados:
echo     [0] MetaTrader 5 -- Plataforma de execucao
echo     [1] Dashboard    -- Next.js  localhost:3000
echo     [2] War Room     -- Analise e aprovacao de sinais
echo     [3] Bot          -- Deteccao, execucao e sync MT5
echo.
echo ===================================================================
echo.

timeout /t 2 /nobreak > nul

echo [0/3] Iniciando MetaTrader 5...
set MT5_EXE=C:\Program Files\MetaTrader 5\terminal64.exe
if not exist "%MT5_EXE%" set MT5_EXE=C:\Program Files (x86)\MetaTrader 5\terminal64.exe
if exist "%MT5_EXE%" (
    start "" "%MT5_EXE%"
    echo         MetaTrader 5 iniciado.
) else (
    echo         [AVISO] MetaTrader 5 nao encontrado em path padrao.
    echo         Abra manualmente se necessario.
)
timeout /t 4 /nobreak > nul

echo [1/3] Iniciando Dashboard Next.js...
start "Dashboard  (Next.js)" cmd /c "cd app && npm run dev"
timeout /t 2 /nobreak > nul

echo [2/3] Iniciando War Room...
start "War Room   (Python)" cmd /k "python squads/trade-liquidez-python/scripts/auto_war_room.py"
timeout /t 1 /nobreak > nul

echo [3/3] Iniciando Bot de Liquidez...
start "Bot Liquidez (Python)" cmd /k "python squads/trade-liquidez-python/scripts/bot_liquidez.py"

echo.
echo ===================================================================
echo   SISTEMA ONLINE  --  4 processos iniciados
echo.
echo   Dashboard : http://localhost:3000
echo   Logs      : http://localhost:3000/logs
echo   Status    : heartbeat a cada 20s
echo ===================================================================
echo.
echo   Pressione qualquer tecla para fechar este orquestrador.
echo   (Os processos continuam rodando em suas proprias janelas)
echo.
pause > nul
