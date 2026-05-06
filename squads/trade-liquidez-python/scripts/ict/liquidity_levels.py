"""
ICT Liquidity Levels — Aula 3 (Multi-timeframe + Mindset).

Identifica zonas onde liquidez (stops) tende a se acumular:

  1. Untested recent highs/lows — pivots formados que ainda não foram retestados
     "Untested levels are influential going in the future" (ICT Aula 3 ~14:50)

  2. Equal highs/lows (double tops/bottoms) — duas máximas/mínimas próximas
     "Big bull's eye for liquidity raids" (ICT Aula 3 ~15:35)

Esses níveis funcionam como ALVOS PROVÁVEIS de raid pelo smart money — preço
tende a varrer essas regiões e reverter (ou continuar com momentum).

Funções principais:
  find_untested_levels(df, pivots, last_n=20) -> dict
  find_equal_levels(pivots, tolerance_pips=5, point=...) -> list[tuple]
  next_levels(price, untested, equal) -> dict {above, below, distance_pips}
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass

from .structure import Pivot


@dataclass
class LiquidityLevel:
    price: float
    kind: str          # 'high' | 'low' | 'equal_high' | 'equal_low'
    pivots: List[Pivot]   # 1 ou 2 pivots que formam o level
    times_tested: int = 0  # quantas vezes preço tocou e respeitou
    note: str = ""

    def __repr__(self):
        return f"Liq({self.kind}@{self.price:.5f}, tested={self.times_tested})"


def find_untested_levels(df, pivots: List[Pivot], last_n_candles: int = 20,
                         tolerance_pips: float = 3.0,
                         point: float = 0.00001) -> List[LiquidityLevel]:
    """
    Levels formados há tempo (pivots fora das últimas N velas) que NÃO foram
    retestados nas últimas N velas.

    Lógica:
      - Para cada pivot fora da janela recente:
        * Se kind == 'high': não foi retestado se max(high) das últimas N velas
          está mais de `tolerance_pips` ABAIXO do pivot.price
        * Se kind == 'low': não foi retestado se min(low) das últimas N está
          mais de `tolerance_pips` ACIMA do pivot.price.

    Esses levels são alvos prováveis de varredura futura.
    """
    if df is None or not pivots:
        return []

    pip = point * 10
    tolerance = tolerance_pips * pip

    if len(df) < last_n_candles + 1:
        return []

    recent_max = float(df['high'].tail(last_n_candles).max())
    recent_min = float(df['low'].tail(last_n_candles).min())
    cutoff_index = len(df) - last_n_candles

    untested: List[LiquidityLevel] = []
    for p in pivots:
        if p.index >= cutoff_index:
            continue   # pivot está na janela recente — ignorar

        if p.kind == 'high' and (p.price - recent_max) > tolerance:
            untested.append(LiquidityLevel(
                price=p.price, kind='high', pivots=[p], times_tested=0,
                note=f"untested high ({p.price - recent_max:.5f} acima do max recente)"
            ))
        elif p.kind == 'low' and (recent_min - p.price) > tolerance:
            untested.append(LiquidityLevel(
                price=p.price, kind='low', pivots=[p], times_tested=0,
                note=f"untested low ({recent_min - p.price:.5f} abaixo do min recente)"
            ))

    return untested


def find_equal_levels(pivots: List[Pivot], tolerance_pips: float = 5.0,
                      point: float = 0.00001,
                      max_distance_candles: int = 50) -> List[LiquidityLevel]:
    """
    Detecta pares de pivots do mesmo tipo (high+high ou low+low) cujo preço
    está dentro de `tolerance_pips` E não estão muito distantes em tempo
    (max_distance_candles entre os índices).

    Equal highs ⇒ buy stops empilhados acima — magnetiza preço pra cima.
    Equal lows  ⇒ sell stops empilhados abaixo — magnetiza preço pra baixo.
    """
    if not pivots or len(pivots) < 2:
        return []

    pip = point * 10
    tolerance = tolerance_pips * pip
    equal_levels: List[LiquidityLevel] = []
    seen_pairs = set()

    for i, p1 in enumerate(pivots):
        for p2 in pivots[i + 1:]:
            if p1.kind != p2.kind:
                continue
            if abs(p2.index - p1.index) > max_distance_candles:
                continue
            if abs(p1.price - p2.price) > tolerance:
                continue

            avg_price = (p1.price + p2.price) / 2
            kind = f"equal_{p1.kind}"
            key = (round(avg_price, 5), kind)
            if key in seen_pairs:
                continue
            seen_pairs.add(key)

            equal_levels.append(LiquidityLevel(
                price=avg_price, kind=kind, pivots=[p1, p2], times_tested=2,
                note=f"equal {p1.kind}s @ {p1.price:.5f} & {p2.price:.5f} (dist {p2.index - p1.index} candles)"
            ))

    return equal_levels


def next_levels(current_price: float, levels: List[LiquidityLevel],
                point: float = 0.00001) -> dict:
    """
    Dado o preço atual e uma lista de levels, retorna o próximo level
    ACIMA e ABAIXO do preço, com distância em pips.

    Returns:
      {
        'above': LiquidityLevel | None,
        'below': LiquidityLevel | None,
        'above_distance_pips': float,
        'below_distance_pips': float,
      }
    """
    pip = point * 10

    above_candidates = [l for l in levels if l.price > current_price]
    below_candidates = [l for l in levels if l.price < current_price]

    above = min(above_candidates, key=lambda l: l.price - current_price) if above_candidates else None
    below = max(below_candidates, key=lambda l: l.price)               if below_candidates else None

    return {
        'above': above,
        'below': below,
        'above_distance_pips': ((above.price - current_price) / pip) if (above and pip > 0) else 0.0,
        'below_distance_pips': ((current_price - below.price) / pip) if (below and pip > 0) else 0.0,
    }
