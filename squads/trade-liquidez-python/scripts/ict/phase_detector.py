"""
ICT Phase Detector — Aula 1 (Elements of a Trade Setup).

Classifica em qual das 4 condições ICT o mercado está num timeframe:

  expansion    — preço se afasta rapidamente do equilibrium (impulse)
  retracement  — preço retorna a uma faixa recém-criada (pullback parcial)
  reversal     — quebra de estrutura, mudança direcional
  consolidation — range estreito, swings sobrepostos (acumulação)

Sequência ICT obrigatória:
  consolidation -> expansion -> (retracement | reversal) -> ...
  (consolidation NUNCA vai direto pra retracement ou reversal)

A "phase" é informativa para scoring — combinada com bias direcional, define
se o trade é a-favor (alta convicção) ou contra (baixa convicção).
"""

from dataclasses import dataclass
from typing import Literal, Optional

from .structure import detect_swings, classify_structure, Pivot


PhaseKind = Literal['expansion', 'retracement', 'reversal', 'consolidation', 'unknown']


@dataclass
class PhaseResult:
    phase: PhaseKind
    direction: str         # 'up' | 'down' | 'neutral'
    confidence: float      # 0-1
    last_swing_size_pips: float = 0.0
    range_size_pips: float = 0.0
    note: str = ""

    def __repr__(self):
        return f"Phase({self.phase}/{self.direction}, conf={self.confidence:.2f})"


def classify_phase(df, depth: int = 5, point: float = 0.00001,
                   consolidation_factor: float = 0.5) -> PhaseResult:
    """
    Classifica fase do mercado para o timeframe representado por df.

    Heurísticas:
      - Calcula swings (depth=5 default — apropriado para H1/H4/M15)
      - Mede range total (high - low) das últimas N velas
      - Mede tamanho do último swing direcional
      - Aplica regras:
          * Se últimos 3-4 swings têm sobreposição alta E range pequeno → consolidation
          * Se último swing > 1.5x mediana E na direção da estrutura → expansion
          * Se preço atual está entre 30-65% retração do último expansion → retracement
          * Se BOS detectado (alternância HH/LL ou LH/HL) → reversal
          * Caso contrário → unknown

    Args:
        df: DataFrame OHLC (mínimo 30 candles para significância)
        depth: parâmetro de pivot detection
        point: ponto do par (para conversão em pips)
        consolidation_factor: range_atual < (range_swing_medio * factor) → consolidation

    Returns:
        PhaseResult
    """
    if df is None or len(df) < (2 * depth + 5):
        return PhaseResult(phase='unknown', direction='neutral', confidence=0.0,
                           note="dados insuficientes")

    pip = point * 10
    pivots = detect_swings(df, depth=depth, point=point)

    if len(pivots) < 3:
        # Range puro — sem pivots = consolidation
        h_max = float(df['high'].max())
        l_min = float(df['low'].min())
        rng = (h_max - l_min) / pip if pip > 0 else 0
        return PhaseResult(phase='consolidation', direction='neutral',
                           confidence=0.6, range_size_pips=rng,
                           note="poucos pivots — range puro")

    structure = classify_structure(pivots, lookback=4)
    last_n = pivots[-4:]

    # Tamanho dos últimos swings (em pips)
    swing_sizes = []
    for i in range(1, len(last_n)):
        size_pips = abs(last_n[i].price - last_n[i - 1].price) / pip if pip > 0 else 0
        swing_sizes.append(size_pips)
    median_swing = sorted(swing_sizes)[len(swing_sizes) // 2] if swing_sizes else 0
    last_swing_size = swing_sizes[-1] if swing_sizes else 0

    # Range total das últimas 30 velas
    recent = df.tail(30)
    range_pips = (float(recent['high'].max()) - float(recent['low'].min())) / pip if pip > 0 else 0

    # 1) Reversal: BOS detectado (alternância de estrutura)
    if structure['bos_detected']:
        direction = 'up' if structure['last_low_kind'] == 'HL' else 'down'
        confidence = min(1.0, last_swing_size / max(median_swing, 1.0))
        return PhaseResult(
            phase='reversal',
            direction=direction,
            confidence=confidence,
            last_swing_size_pips=last_swing_size,
            range_size_pips=range_pips,
            note=f"BOS detectado ({structure['last_high_kind']}/{structure['last_low_kind']})"
        )

    # 2) Consolidation: range pequeno em relação ao swing médio
    if median_swing > 0 and range_pips < (median_swing * (1.0 + consolidation_factor)):
        return PhaseResult(
            phase='consolidation', direction='neutral',
            confidence=0.7, last_swing_size_pips=last_swing_size,
            range_size_pips=range_pips,
            note=f"range {range_pips:.0f}pips ~ swing médio {median_swing:.0f}pips"
        )

    # 3) Expansion: último swing é grande e na direção da estrutura
    if median_swing > 0 and last_swing_size >= (median_swing * 1.3):
        # Direção: a do último swing
        if len(last_n) >= 2:
            last_pivot = last_n[-1]
            prev_pivot = last_n[-2]
            up = last_pivot.price > prev_pivot.price
            direction = 'up' if up else 'down'
        else:
            direction = structure['direction']
        confidence = min(1.0, last_swing_size / median_swing / 2)  # max conf em ~2x median
        return PhaseResult(
            phase='expansion', direction=direction, confidence=confidence,
            last_swing_size_pips=last_swing_size, range_size_pips=range_pips,
            note=f"último swing {last_swing_size:.0f}pips vs mediana {median_swing:.0f}pips"
        )

    # 4) Retracement: preço atual está dentro do último expansion swing (30-65% da retração)
    if len(last_n) >= 2:
        last_p = last_n[-1]
        prev_p = last_n[-2]
        cur_close = float(df['close'].iloc[-1])
        swing_high = max(last_p.price, prev_p.price)
        swing_low  = min(last_p.price, prev_p.price)
        swing_range = swing_high - swing_low

        if swing_range > 0:
            # Que % do swing já retraiu?
            if last_p.price > prev_p.price:
                # Swing de baixa→alta: retracement = (swing_high - close) / swing_range
                retr_pct = (swing_high - cur_close) / swing_range
                direction = 'up'  # estrutura ainda é ascendente, esperando continuação
            else:
                retr_pct = (cur_close - swing_low) / swing_range
                direction = 'down'

            if 0.30 <= retr_pct <= 0.65:
                return PhaseResult(
                    phase='retracement', direction=direction,
                    confidence=0.7,
                    last_swing_size_pips=last_swing_size, range_size_pips=range_pips,
                    note=f"retraçao ~{retr_pct*100:.0f}% do último swing"
                )

    # 5) Caso default — direção pela estrutura
    return PhaseResult(
        phase='unknown', direction=structure['direction'],
        confidence=0.4,
        last_swing_size_pips=last_swing_size, range_size_pips=range_pips,
        note="fora dos padrões claros"
    )
