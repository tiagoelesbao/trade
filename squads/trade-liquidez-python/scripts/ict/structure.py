"""
ICT Structure — Detecção de swings (pivots) e estrutura.

Detecta high/low pivots em DataFrames OHLC. Pivot high = vela cuja máxima é
maior que `depth` velas antes E `depth` velas depois (mesmo critério ICT
clássico para identificar swing points).

Funções principais:
  detect_swings(df, depth=5) -> list[Pivot]
  classify_structure(pivots) -> dict — última estrutura identificada (HH/HL/LL/LH)
  bias_from_structure(structure) -> 'bullish'|'bearish'|'neutral'
"""

from dataclasses import dataclass
from typing import List, Literal, Optional


PivotKind = Literal['high', 'low']


@dataclass
class Pivot:
    """
    Um swing point identificado.

    Attributes:
        index: posição no DataFrame original (iloc)
        kind:  'high' ou 'low'
        price: preço do pivot (high se kind=='high', low se kind=='low')
        time:  timestamp da vela
        strength: float — distância média (em pips) para as `depth` velas vizinhas;
                  pivots mais "destacados" têm strength maior.
    """
    index: int
    kind: PivotKind
    price: float
    time: object
    strength: float = 0.0

    def __repr__(self):
        t_str = str(self.time)[:16]
        return f"Pivot({self.kind} @ {self.price:.5f}, idx={self.index}, t={t_str}, str={self.strength:.1f})"


def detect_swings(df, depth: int = 5, point: float = 0.00001) -> List[Pivot]:
    """
    Detecta pivots highs e lows em df (OHLC pandas DataFrame).

    Pivot high na posição i: df['high'].iloc[i] > df['high'].iloc[i-depth..i+depth]
    Pivot low na posição i:  df['low'].iloc[i]  < df['low'].iloc[i-depth..i+depth]

    Args:
        df: DataFrame com colunas 'open', 'high', 'low', 'close', 'time'
        depth: quantas velas a esquerda e direita devem confirmar o pivot
        point: tamanho do ponto do par (para calcular strength em pips)

    Returns:
        Lista de Pivot ordenados por index (ordem cronológica).
    """
    if df is None or len(df) < (2 * depth + 1):
        return []

    pip = point * 10
    pivots: List[Pivot] = []

    highs = df['high'].values
    lows = df['low'].values
    times = df['time'].values

    for i in range(depth, len(df) - depth):
        h = highs[i]
        l = lows[i]

        # Pivot high: i é maior que todos os vizinhos (depth para cada lado)
        is_pivot_high = True
        is_pivot_low  = True
        for j in range(1, depth + 1):
            if h <= highs[i - j] or h <= highs[i + j]:
                is_pivot_high = False
            if l >= lows[i - j] or l >= lows[i + j]:
                is_pivot_low = False
            if not is_pivot_high and not is_pivot_low:
                break

        if is_pivot_high:
            # Strength: média da diferença entre h e os vizinhos (em pips)
            neighbors = [highs[i - j] for j in range(1, depth + 1)] + \
                        [highs[i + j] for j in range(1, depth + 1)]
            strength = ((h - sum(neighbors) / len(neighbors)) / pip) if pip > 0 else 0.0
            pivots.append(Pivot(index=i, kind='high', price=float(h),
                                time=times[i], strength=float(strength)))
        elif is_pivot_low:
            neighbors = [lows[i - j] for j in range(1, depth + 1)] + \
                        [lows[i + j] for j in range(1, depth + 1)]
            strength = ((sum(neighbors) / len(neighbors) - l) / pip) if pip > 0 else 0.0
            pivots.append(Pivot(index=i, kind='low', price=float(l),
                                time=times[i], strength=float(strength)))

    return pivots


def classify_structure(pivots: List[Pivot], lookback: int = 4) -> dict:
    """
    Classifica a estrutura recente (últimos N pivots).

    Identifica:
      - last_high_kind: 'HH' (higher high) | 'LH' (lower high) | None
      - last_low_kind:  'HL' (higher low)  | 'LL' (lower low)  | None
      - bos_detected:   True se houve break of structure recente
      - direction:      'up' | 'down' | 'neutral'

    Lógica:
      Bullish structure: HH + HL (highs e lows sobem)
      Bearish structure: LH + LL (highs e lows descem)
      Reversal/BOS:     HH+LL ou LH+HL — alternância

    Args:
        pivots: lista de Pivot (ordem cronológica)
        lookback: quantos pivots considerar (default 4 = 2 highs + 2 lows típicos)
    """
    if not pivots or len(pivots) < 2:
        return {
            'last_high_kind': None,
            'last_low_kind':  None,
            'bos_detected':   False,
            'direction':      'neutral',
            'last_high':      None,
            'last_low':       None,
        }

    recent = pivots[-lookback:] if len(pivots) >= lookback else pivots
    highs = [p for p in recent if p.kind == 'high']
    lows  = [p for p in recent if p.kind == 'low']

    last_high_kind: Optional[str] = None
    last_low_kind:  Optional[str] = None

    if len(highs) >= 2:
        last_high_kind = 'HH' if highs[-1].price > highs[-2].price else 'LH'
    if len(lows) >= 2:
        last_low_kind = 'HL' if lows[-1].price > lows[-2].price else 'LL'

    # Direction
    direction = 'neutral'
    if last_high_kind == 'HH' and last_low_kind == 'HL':
        direction = 'up'
    elif last_high_kind == 'LH' and last_low_kind == 'LL':
        direction = 'down'

    # BOS: highs em uma direção + lows em outra (estrutura quebrada)
    bos_detected = False
    if last_high_kind and last_low_kind:
        if (last_high_kind == 'HH' and last_low_kind == 'LL') or \
           (last_high_kind == 'LH' and last_low_kind == 'HL'):
            bos_detected = True

    return {
        'last_high_kind': last_high_kind,
        'last_low_kind':  last_low_kind,
        'bos_detected':   bos_detected,
        'direction':      direction,
        'last_high':      highs[-1] if highs else None,
        'last_low':       lows[-1]  if lows  else None,
    }


def bias_from_structure(structure: dict) -> str:
    """
    Converte resultado de classify_structure em bias direcional simples.
    Retorna: 'bullish' | 'bearish' | 'neutral'
    """
    d = structure.get('direction', 'neutral')
    if d == 'up':   return 'bullish'
    if d == 'down': return 'bearish'
    return 'neutral'
