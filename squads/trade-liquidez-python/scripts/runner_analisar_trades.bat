@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM Runner de analise de trades - v1 (bootstrap operacional)
REM Uso:
REM   runner_analisar_trades.bat --input "C:\caminho\da\pasta" [--mode quick|full] [--output "C:\saida"] [--date YYYY-MM-DD] [--dry-run] [--verbose] [--enable-openrouter-fallback]

set "INPUT_DIR="
set "MODE=full"
set "OUTPUT_DIR="
set "RUN_DATE="
set "DRY_RUN=false"
set "VERBOSE=false"
set "ENABLE_OPENROUTER_FALLBACK=false"
set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "SQUAD_DIR=%%~fI"

:parse_args
if "%~1"=="" goto args_done

if /I "%~1"=="--input" (
  set "INPUT_DIR=%~2"
  shift & shift
  goto parse_args
)
if /I "%~1"=="--mode" (
  set "MODE=%~2"
  shift & shift
  goto parse_args
)
if /I "%~1"=="--output" (
  set "OUTPUT_DIR=%~2"
  shift & shift
  goto parse_args
)
if /I "%~1"=="--date" (
  set "RUN_DATE=%~2"
  shift & shift
  goto parse_args
)
if /I "%~1"=="--dry-run" (
  set "DRY_RUN=true"
  shift
  goto parse_args
)
if /I "%~1"=="--verbose" (
  set "VERBOSE=true"
  shift
  goto parse_args
)
if /I "%~1"=="--enable-openrouter-fallback" (
  set "ENABLE_OPENROUTER_FALLBACK=true"
  shift
  goto parse_args
)

echo [ERROR] Parametro invalido: %~1
goto usage_error

:args_done
if "%INPUT_DIR%"=="" (
  echo [ERROR] --input eh obrigatorio.
  goto usage_error
)

if /I not "%MODE%"=="quick" if /I not "%MODE%"=="full" (
  echo [ERROR] --mode invalido. Use quick ou full.
  exit /b 1
)

if not exist "%INPUT_DIR%" (
  echo [ERROR] Pasta de input nao existe: "%INPUT_DIR%"
  exit /b 2
)

if "%OUTPUT_DIR%"=="" (
  set "OUTPUT_DIR=%INPUT_DIR%\_analysis_output"
)

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%" >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Nao foi possivel criar pasta de output: "%OUTPUT_DIR%"
  exit /b 2
)

set "RUN_ID=%DATE:~-4%%DATE:~3,2%%DATE:~0,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%"
set "RUN_ID=%RUN_ID: =0%"
set "RUN_DIR=%OUTPUT_DIR%\run_%RUN_ID%"
mkdir "%RUN_DIR%" >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Nao foi possivel criar pasta do run: "%RUN_DIR%"
  exit /b 2
)

set "RUN_LOG=%RUN_DIR%\runner.log"
call :log INFO RUN_START "input=%INPUT_DIR%;mode=%MODE%;dry_run=%DRY_RUN%"

if /I "%ENABLE_OPENROUTER_FALLBACK%"=="true" (
  if "%OPENROUTER_API_KEY%"=="" (
    call :log WARN FALLBACK_DISABLED "OPENROUTER_API_KEY ausente. Fallback externo sera ignorado."
    set "ENABLE_OPENROUTER_FALLBACK=false"
  ) else (
    call :log INFO FALLBACK_ENABLED "openrouter=true"
  )
)

for %%F in ("%INPUT_DIR%\*.png" "%INPUT_DIR%\*.jpg" "%INPUT_DIR%\*.jpeg") do (
  set "HAS_PRINT=true"
)
if not defined HAS_PRINT (
  call :log ERROR PRECHECK_FAIL "Nenhum print de trade encontrado no input."
  echo [ERROR] Nenhum print encontrado em "%INPUT_DIR%"
  exit /b 2
)

if /I "%DRY_RUN%"=="true" (
  call :log INFO DRY_RUN_OK "Prechecks concluidos sem execucao de workflow."
  echo [OK] Dry-run concluido com sucesso.
  exit /b 0
)

set "WORKFLOW_FILE=%SQUAD_DIR%\workflows\trade_analysis_workflow.yaml"
if not exist "%WORKFLOW_FILE%" (
  call :log ERROR WORKFLOW_MISSING "Arquivo nao encontrado: %WORKFLOW_FILE%"
  echo [ERROR] Workflow ausente: "%WORKFLOW_FILE%"
  exit /b 4
)

call :log INFO WORKFLOW_START "workflow=%WORKFLOW_FILE%"
echo [INFO] Workflow planejado localizado: "%WORKFLOW_FILE%"
set "ENGINE_FILE=%SQUAD_DIR%\scripts\trade_analysis_engine.py"
if not exist "%ENGINE_FILE%" (
  call :log ERROR ENGINE_MISSING "Arquivo nao encontrado: %ENGINE_FILE%"
  echo [ERROR] Engine ausente: "%ENGINE_FILE%"
  exit /b 4
)

set "ENGINE_CMD=python"
where py >nul 2>nul
if not errorlevel 1 set "ENGINE_CMD=py -3"

call :log INFO ENGINE_START "cmd=%ENGINE_CMD% %ENGINE_FILE%"
if /I "%VERBOSE%"=="true" (
  if /I "%ENABLE_OPENROUTER_FALLBACK%"=="true" (
    %ENGINE_CMD% "%ENGINE_FILE%" --input "%INPUT_DIR%" --output "%RUN_DIR%" --mode %MODE% --run-id "%RUN_ID%" --verbose --enable-openrouter-fallback
  ) else (
    %ENGINE_CMD% "%ENGINE_FILE%" --input "%INPUT_DIR%" --output "%RUN_DIR%" --mode %MODE% --run-id "%RUN_ID%" --verbose
  )
) else (
  if /I "%ENABLE_OPENROUTER_FALLBACK%"=="true" (
    %ENGINE_CMD% "%ENGINE_FILE%" --input "%INPUT_DIR%" --output "%RUN_DIR%" --mode %MODE% --run-id "%RUN_ID%" --enable-openrouter-fallback
  ) else (
    %ENGINE_CMD% "%ENGINE_FILE%" --input "%INPUT_DIR%" --output "%RUN_DIR%" --mode %MODE% --run-id "%RUN_ID%"
  )
)
set "ENGINE_EXIT=%ERRORLEVEL%"

if "%ENGINE_EXIT%"=="0" (
  call :log INFO WORKFLOW_END "engine_exit=0"
  call :log INFO RUN_END "status=success"
  echo [OK] Runner finalizado com sucesso.
  exit /b 0
) else (
  call :log ERROR WORKFLOW_END "engine_exit=%ENGINE_EXIT%"
  call :log INFO RUN_END "status=failed"
  echo [ERROR] Engine falhou com codigo %ENGINE_EXIT%.
  exit /b 4
)

:usage_error
echo.
echo Uso:
echo   runner_analisar_trades.bat --input "C:\pasta_dia" [--mode quick^|full] [--output "C:\saida"] [--date YYYY-MM-DD] [--dry-run] [--verbose] [--enable-openrouter-fallback]
exit /b 1

:log
set "LOG_LEVEL=%~1"
set "LOG_EVENT=%~2"
set "LOG_MSG=%~3"
set "NOW=%DATE% %TIME%"
>> "%RUN_LOG%" echo [%NOW%] [%LOG_LEVEL%] [%LOG_EVENT%] %LOG_MSG%
if /I "%VERBOSE%"=="true" echo [%LOG_LEVEL%] %LOG_EVENT% - %LOG_MSG%
exit /b 0
