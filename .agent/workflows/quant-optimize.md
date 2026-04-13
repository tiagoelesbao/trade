description: "Otimiza os parâmetros matemáticos do script quantitativo Jim Simons usando busca em grade e replay engine."

# Comandos
commands:
  - name: quant-optimize
    description: "Inicia Bateria Aleatória de Mutação de Parâmetros de Backtest"

# Etapas
steps:
  - id: step_optim
    description: "Executar o Motor Genético de Otimização Paramétrica para ajustar a matriz do robô às volatilidades recentes e maximizar Win Rate de forma automatizada e cega."
    tools:
      - name: run_command
        args:
          CommandLine: "python squads/trade-liquidez-python/scripts/optimize_hyperparams.py"
          Cwd: "."
          WaitMsBeforeAsync: 60000

  - id: step_verify
    description: "Ler o Relatório Final para conferir se houve saltos de Win Rate após os ajustes, caso aplicável."
    tools:
      - name: run_command
        args:
          CommandLine: "python squads/trade-liquidez-python/scripts/market_replay.py"
          Cwd: "."
          WaitMsBeforeAsync: 3000

  - id: step_report
    description: "Ler relatorio_executivo.md modificado após o quant-optimize e apresentar o novo Set de Parâmetros que foi fixado em config.yaml."
