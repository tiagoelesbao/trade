@echo off
title [AIOX] Orquestrador -- Trade Liquidez v6.2.0-ict
color 0B
chcp 65001 > nul

set PYTHONPATH=%PYTHONPATH%;%CD%

echo.
echo ===================================================================
echo   TRADE LIQUIDEZ v6.2.0-ict  --  ICT CONTEXT + POOL + EXIT WR
echo   Orquestrador de Sessao  --  %DATE%  %TIME:~0,8%
echo ===================================================================
echo.
echo   Componentes que serao iniciados:
echo     [0] MetaTrader 5  -- Plataforma de execucao
echo     [1] Dashboard     -- Next.js  localhost:3000
echo     [2] War Room      -- Pool-then-Pick + ICT score 25pts
echo     [3] Bot           -- Deteccao + gates ICT/horario
echo     [4] Exit War Room -- BE/Exit dinamico ICT-aware (Sprint 4)
echo.
echo ===================================================================
echo.

timeout /t 2 /nobreak > nul

echo [0/4] Iniciando MetaTrader 5...
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

echo [1/4] Iniciando Dashboard Next.js...
start "Dashboard  (Next.js)" cmd /c "cd app && npm run dev"
timeout /t 2 /nobreak > nul

echo [2/4] Iniciando War Room v2 (Pool-then-Pick + ICT)...
start "War Room   (Python)" cmd /k "python squads/trade-liquidez-python/scripts/auto_war_room.py"
timeout /t 1 /nobreak > nul

echo [3/4] Iniciando Bot de Liquidez...
start "Bot Liquidez (Python)" cmd /k "python squads/trade-liquidez-python/scripts/bot_liquidez.py"
timeout /t 1 /nobreak > nul

echo [4/4] Iniciando Exit War Room (gestao de saida)...
start "Exit War Room (Python)" cmd /k "python squads/trade-liquidez-python/scripts/exit_war_room.py"

echo.
echo ===================================================================
echo   SISTEMA ONLINE  --  5 processos iniciados (MT5 + 4 servicos)
echo.
echo   Dashboard : http://localhost:3000
echo   Logs      : http://localhost:3000/logs
echo   Status    : heartbeat a cada 20s (bot)  10s (exit_wr)
echo.
echo   Pipeline:
echo     Bot detecta -> War Room scoring (pool 30s) -> aprovacao -> MT5
echo     Exit War Room monitora posicoes abertas em tempo real
echo ===================================================================
echo.
echo   Pressione qualquer tecla para fechar este orquestrador.
echo   (Os processos continuam rodando em suas proprias janelas)
echo.
pause > nul
