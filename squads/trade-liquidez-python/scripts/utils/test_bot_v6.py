"""
Test Bot v6.0 - Validação de Integração
=========================================
Testa o bot_liquidez.py v6.0 sem executar trades reais.

Validações:
1. Conexão MT5
2. Conexão Supabase via TradeLifecycleManager
3. Criação de sinal (signal_detected)
4. Transições de estado (approved, filled, open, closed)
5. Funções principais do bot
"""

import MetaTrader5 as mt5
import sys
from datetime import datetime
from trade_lifecycle_manager import TradeLifecycleManager

def test_mt5_connection():
    """Testa conexão com MT5."""
    print("\n" + "="*65)
    print("TEST 1: Conexão MT5")
    print("="*65)

    if not mt5.initialize():
        print("[FAIL] Não foi possível conectar ao MT5")
        return False

    account_info = mt5.account_info()
    print(f"[OK] Conectado ao MT5")
    print(f"     Conta: {account_info.login}")
    print(f"     Balance: ${account_info.balance:.2f}")
    print(f"     Equity: ${account_info.equity:.2f}")

    return True

def test_lifecycle_connection():
    """Testa conexão com Supabase via TradeLifecycleManager."""
    print("\n" + "="*65)
    print("TEST 2: Conexão Supabase (TradeLifecycleManager)")
    print("="*65)

    try:
        lifecycle = TradeLifecycleManager()
        print("[OK] TradeLifecycleManager inicializado")

        # Testar leitura
        result = lifecycle.client.table("signals_liquidez").select("id").limit(1).execute()
        print(f"[OK] Conexão Supabase funcionando")
        print(f"     {len(result.data)} registro(s) encontrado(s)")

        return True, lifecycle
    except Exception as e:
        print(f"[FAIL] Erro ao conectar Supabase: {e}")
        return False, None

def test_signal_creation(lifecycle):
    """Testa criação de sinal."""
    print("\n" + "="*65)
    print("TEST 3: Criação de Sinal (signal_detected)")
    print("="*65)

    try:
        # Criar sinal de teste
        signal = lifecycle.create_signal(
            symbol="EURUSD",
            trade_type="BUY",
            price=1.09500,
            sl=1.09400,
            tp=1.09650,
            wick_pct=0.35,
            magic_number=999999  # Magic number de teste
        )

        if not signal:
            print("[FAIL] Falha ao criar sinal")
            return False, None

        print(f"[OK] Sinal criado com sucesso")
        print(f"     ID: {signal['id']}")
        print(f"     Status: {signal['status']}")
        print(f"     Symbol: {signal['symbol']}")

        return True, signal
    except Exception as e:
        print(f"[FAIL] Erro ao criar sinal: {e}")
        return False, None

def test_state_transitions(lifecycle, signal):
    """Testa transições de estado."""
    print("\n" + "="*65)
    print("TEST 4: Transições de Estado")
    print("="*65)

    signal_id = signal['id']

    try:
        # Transição 1: signal_detected -> approved
        print("\n[TEST] Transição: signal_detected -> approved")
        lifecycle.approve_signal(signal_id, agent_opinions=[{"agent": "test", "verdict": "approve"}])

        updated = lifecycle.get_signal_by_id(signal_id)
        if updated['status'] == 'approved':
            print(f"[OK] Status = approved")
        else:
            print(f"[FAIL] Status esperado: approved, obtido: {updated['status']}")
            return False

        # Transição 2: approved -> filled
        print("\n[TEST] Transição: approved -> filled")
        test_position_id = 123456789  # Position ID fictício
        lifecycle.mark_as_filled(signal_id, test_position_id)

        updated = lifecycle.get_signal_by_id(signal_id)
        if updated['status'] == 'filled' and updated['position_id'] == test_position_id:
            print(f"[OK] Status = filled, position_id = {test_position_id}")
        else:
            print(f"[FAIL] Transição filled falhou")
            return False

        # Transição 3: filled -> open
        print("\n[TEST] Transição: filled -> open")
        lifecycle.mark_as_open(signal_id)

        updated = lifecycle.get_signal_by_id(signal_id)
        if updated['status'] == 'open':
            print(f"[OK] Status = open")
        else:
            print(f"[FAIL] Status esperado: open, obtido: {updated['status']}")
            return False

        # Transição 4: open -> closed
        print("\n[TEST] Transição: open -> closed")
        test_pnl = 15.50
        test_exit_price = 1.09650
        lifecycle.close_trade(test_position_id, test_pnl, test_exit_price)

        updated = lifecycle.get_signal_by_id(signal_id)
        if updated['status'] == 'closed' and updated['pnl'] == test_pnl:
            print(f"[OK] Status = closed, P&L = ${test_pnl}")
        else:
            print(f"[FAIL] Transição closed falhou")
            return False

        print("\n[OK] Todas as transições funcionaram corretamente!")
        return True

    except Exception as e:
        print(f"[FAIL] Erro nas transições: {e}")
        return False

def test_bot_functions():
    """Testa funções principais do bot."""
    print("\n" + "="*65)
    print("TEST 5: Funções do Bot")
    print("="*65)

    try:
        # Importar funções do bot
        import sys
        import os
        sys.path.insert(0, os.path.dirname(__file__))

        from bot_liquidez import get_rates, get_validated_zones, calculate_rsi

        # Testar get_rates
        print("\n[TEST] get_rates(EURUSD, M15, 100)")
        df = get_rates("EURUSD", mt5.TIMEFRAME_M15, 100)
        if df is not None and len(df) > 0:
            print(f"[OK] {len(df)} candles obtidos")
        else:
            print(f"[FAIL] Falha ao obter candles")
            return False

        # Testar get_validated_zones
        print("\n[TEST] get_validated_zones()")
        point = mt5.symbol_info("EURUSD").point
        zones = get_validated_zones(df, point)
        print(f"[OK] {len(zones)} zonas identificadas")

        # Testar calculate_rsi
        print("\n[TEST] calculate_rsi()")
        rsi = calculate_rsi(df['close'])
        if rsi is not None and len(rsi) > 0:
            print(f"[OK] RSI calculado: {rsi.iloc[-1]:.2f}")
        else:
            print(f"[FAIL] Falha ao calcular RSI")
            return False

        print("\n[OK] Todas as funções do bot funcionaram!")
        return True

    except Exception as e:
        print(f"[FAIL] Erro ao testar funções: {e}")
        import traceback
        traceback.print_exc()
        return False

def cleanup_test_signal(lifecycle, signal_id):
    """Remove sinal de teste do banco."""
    print("\n" + "="*65)
    print("CLEANUP: Removendo sinal de teste")
    print("="*65)

    try:
        lifecycle.client.table("signals_liquidez").delete().eq("id", signal_id).execute()
        print(f"[OK] Sinal de teste removido: {signal_id}")
    except Exception as e:
        print(f"[WARNING] Falha ao remover sinal de teste: {e}")

def main():
    """Executa todos os testes."""
    print("\n" + "="*80)
    print(" BOT v6.0 - SUITE DE TESTES")
    print(" " + str(datetime.now()))
    print("="*80)

    # Test 1: MT5
    if not test_mt5_connection():
        print("\n[ABORT] Não foi possível conectar ao MT5")
        return

    # Test 2: Supabase
    success, lifecycle = test_lifecycle_connection()
    if not success:
        print("\n[ABORT] Não foi possível conectar ao Supabase")
        mt5.shutdown()
        return

    # Test 3: Criação de sinal
    success, signal = test_signal_creation(lifecycle)
    if not success:
        print("\n[ABORT] Falha ao criar sinal de teste")
        mt5.shutdown()
        return

    signal_id = signal['id']

    # Test 4: Transições de estado
    if not test_state_transitions(lifecycle, signal):
        print("\n[FAIL] Transições de estado falharam")
        cleanup_test_signal(lifecycle, signal_id)
        mt5.shutdown()
        return

    # Test 5: Funções do bot
    if not test_bot_functions():
        print("\n[FAIL] Funções do bot falharam")
        cleanup_test_signal(lifecycle, signal_id)
        mt5.shutdown()
        return

    # Cleanup
    cleanup_test_signal(lifecycle, signal_id)

    # Resultado Final
    print("\n" + "="*80)
    print(" RESULTADO FINAL")
    print("="*80)
    print("[SUCCESS] Todos os testes passaram! [OK]")
    print("\nBot v6.0 está pronto para uso:")
    print("  1. Lifecycle Manager funcionando")
    print("  2. Estados transitando corretamente")
    print("  3. Funções do bot operacionais")
    print("  4. Conexões MT5 e Supabase OK")
    print("\nPróximos passos:")
    print("  - Execute: python bot_liquidez.py")
    print("  - Monitore: localhost:3000/historico")
    print("="*80)

    mt5.shutdown()

if __name__ == "__main__":
    main()
