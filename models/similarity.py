from dataclasses import dataclass

from models.observable_episode import ObservableEpisode
from models.explanation import Explanation


@dataclass
class Similarity:
    """
    RE-023.5: episode pasa a tipar ObservableEpisode, no Episode.
    Desde que SimilarityEngine construye Similarity a partir de los
    episodios que le entrega ObservableUniverse, este campo contiene
    de verdad proyecciones observables -- el tipo declarado ahora
    coincide con lo que realmente circula. Ver ADR-004: si esto
    siguiera diciendo Episode, un Episode canonico pasaria el chequeo
    de tipos exactamente igual que un ObservableEpisode, y esa es la
    ambiguedad que se decidio hacer irrepresentable.
    """

    episode: ObservableEpisode

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
