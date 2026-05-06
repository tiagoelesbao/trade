"""
ICT Daily Range Algorithm — Aula 2 (Smart Money Paradigm).

Rastreia em qual fase do "ciclo do dia" o mercado está, baseado no fuso UTC e
nos extremos formados ao longo do dia.

Mapa diário ICT (UTC):
  21:00-04:00  Asia consolidation (early 21-23 = exhaustion real)
  04:00-07:00  Judas Swing zone (manipulação pré-London — News Driven)
  07:00-10:00  London open expansion (forma high/low do dia)
  10:00-13:00  London continuation
  13:00-13:30  NY 8-8:30 news embargo (volatility spike)
  13:30-15:00  NY open expansion
  15:00-16:00  London close reversal
  16:00-21:00  NY afternoon → end-of-day consolidation

Persistência:
  data/daily_state_{YYYYMMDD}.json — estado por par. Reset à meia-noite UTC.

Uso típico:
  state = load_or_init_state(symbol)
  state.update(df_h1)           # atualiza extremos e fase
  print(state.current_phase, state.day_high, state.day_low)
  save_state(symbol, state)
"""

import json
import os
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Optional


_DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),  # scripts/ -> ../
    "data"
)
os.makedirs(_DATA_DIR, exist_ok=True)


# Mapa de fases ICT (UTC) — alinhado com config.yaml/session_windows
DAILY_PHASES = [
    ('asia_early',      21, 24, 'Asia early (exhaustion post-NY)'),
    ('asia_judas',       0,  7, 'Asia continuation / Judas zone'),
    ('london_open',      7, 10, 'London open expansion'),
    ('london_cont',     10, 13, 'London continuation'),
    ('ny_news_embargo', 13, 14, 'NY 8-8:30 news embargo'),
    ('ny_expansion',    14, 15, 'NY open expansion'),
    ('london_close',    15, 16, 'London close reversal'),
    ('ny_afternoon',    16, 21, 'NY afternoon / end-of-day'),
]


def get_current_phase(now_utc: Optional[datetime] = None) -> tuple:
    """Retorna (phase_id, label, hour_utc) para a hora UTC atual."""
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)
    h = now_utc.hour
    for phase_id, start, end, label in DAILY_PHASES:
        if start < end and start <= h < end:
            return phase_id, label, h
    return 'unknown', 'fora de fase', h


@dataclass
class DailyState:
    """
    Estado do dia para um par específico.

    asia_low/high — formados durante 21-07 UTC (Asia + Judas)
    judas_swing_done — quando preço sai do range Asia em direção contrária ao
                       que será o trend do dia (manipulação que forma o low/high
                       intraday). Detectado quando preço fura asia_low/high mas
                       reverte.
    london_open_high/low — extremos durante 07-13 UTC
    day_high/low — extremos do dia inteiro
    current_phase — fase atual do dia (computada na hora)

    Tipicamente o London open define o high (ou low) do dia. Se o preço atual
    estiver muito longe desse extremo (>1.5x range Asian) é forte sinal de
    expansion confirmada.
    """
    symbol: str
    date_iso: str                         # YYYY-MM-DD UTC
    asia_high: Optional[float] = None
    asia_low:  Optional[float] = None
    asia_high_time: Optional[str] = None
    asia_low_time:  Optional[str] = None

    judas_swing_detected: bool = False
    judas_direction:      Optional[str] = None  # 'up'|'down' — direção da varredura
    judas_high:           Optional[float] = None
    judas_low:            Optional[float] = None

    london_open_high: Optional[float] = None
    london_open_low:  Optional[float] = None

    day_high: Optional[float] = None
    day_low:  Optional[float] = None
    day_high_time: Optional[str] = None
    day_low_time:  Optional[str] = None

    last_update_utc: Optional[str] = None
    current_phase: str = 'unknown'
    current_phase_label: str = ''

    def update_from_dataframe(self, df_h1, point: float = 0.00001):
        """
        Atualiza o estado lendo um DataFrame H1 do par.
        df_h1 deve ter coluna 'time' já em pd.Timestamp (assumido em fuso MT5
        — vamos converter para UTC subtraindo o offset estimado).
        """
        if df_h1 is None or len(df_h1) == 0:
            return

        now_utc = datetime.now(timezone.utc)
        self.last_update_utc = now_utc.isoformat()
        self.current_phase, self.current_phase_label, _ = get_current_phase(now_utc)

        # Para cada vela H1 do dia atual UTC:
        #   - se hora ∈ Asia (21-07): atualiza asia_high/low
        #   - se hora ∈ London (07-13): atualiza london_open_high/low
        #   - todas: atualiza day_high/low
        # Como df['time'] está em fuso MT5 server, convertemos via offset.
        # Aqui simplificamos: usamos os valores de high/low e time direto;
        # o orquestrador (ict_context_engine) vai limitar df_h1 ao dia atual.
        try:
            day_high = float(df_h1['high'].max())
            day_low  = float(df_h1['low'].min())
            self.day_high = day_high if (self.day_high is None or day_high > self.day_high) else self.day_high
            self.day_low  = day_low  if (self.day_low  is None or day_low  < self.day_low)  else self.day_low
        except Exception:
            return

    def to_dict(self) -> dict:
        return asdict(self)


def _state_path(date_iso: str) -> str:
    """data/daily_state_YYYYMMDD.json — único arquivo para todos os pares no dia."""
    yyyymmdd = date_iso.replace("-", "")
    return os.path.join(_DATA_DIR, f"daily_state_{yyyymmdd}.json")


def load_or_init_state(symbol: str, date_iso: Optional[str] = None) -> DailyState:
    """
    Carrega estado persistido para (symbol, date_iso). Se não existir, retorna
    DailyState vazio para o dia.
    """
    if date_iso is None:
        date_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    path = _state_path(date_iso)
    if not os.path.exists(path):
        return DailyState(symbol=symbol, date_iso=date_iso)

    try:
        with open(path, 'r', encoding='utf-8') as f:
            blob = json.load(f) or {}
        sym_data = blob.get(symbol)
        if not sym_data:
            return DailyState(symbol=symbol, date_iso=date_iso)
        # Reconstrói DailyState a partir do dict — campos novos ficam com default
        return DailyState(**{k: v for k, v in sym_data.items()
                              if k in DailyState.__dataclass_fields__})
    except Exception:
        return DailyState(symbol=symbol, date_iso=date_iso)


def save_state(state: DailyState):
    """Persiste estado de UM par. Merge com outros pares no mesmo arquivo do dia."""
    path = _state_path(state.date_iso)

    blob = {}
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                blob = json.load(f) or {}
        except Exception:
            blob = {}

    blob[state.symbol] = state.to_dict()
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(blob, f, indent=2, default=str)
    except Exception:
        pass


def cleanup_old_states(days_to_keep: int = 7):
    """Remove arquivos daily_state_*.json com mais de `days_to_keep` dias."""
    if not os.path.exists(_DATA_DIR):
        return
    today = datetime.now(timezone.utc)
    for fname in os.listdir(_DATA_DIR):
        if not fname.startswith("daily_state_") or not fname.endswith(".json"):
            continue
        try:
            yyyymmdd = fname.replace("daily_state_", "").replace(".json", "")
            file_date = datetime.strptime(yyyymmdd, "%Y%m%d").replace(tzinfo=timezone.utc)
            age_days = (today - file_date).days
            if age_days > days_to_keep:
                os.remove(os.path.join(_DATA_DIR, fname))
        except Exception:
            continue
