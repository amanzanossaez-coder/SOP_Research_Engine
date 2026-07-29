from dataclasses import dataclass

from models.episode import Episode
from models.explanation import Explanation


@dataclass
class Similarity:

    episode: Episode

    score: float

    event: Explanation
    context: Explanation
    outcome: Explanation

    # Evento

    drawdown_score: float
    duration_score: float
    speed_score: float

    # Contexto

    cape_score: float
    pre_crash_return_3y_score: float
    volatility_score: float

    # Resultado

    recovery_score: float