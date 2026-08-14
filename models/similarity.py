from dataclasses import dataclass

from models.observable_episode import ObservableEpisode
from models.similarity_explanation import SimilarityExplanation


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

    RE-EXP.1 -- event/context/outcome estaban tipados como
    `Explanation` (models/explanation.py), que nunca fue el objeto que
    circula en realidad. El runtime siempre entrego
    `SimilarityExplanation` (title, score, items) -- confirmado
    ejecutando el pipeline real. El type hint no rompia nada (Python
    no lo fuerza), pero era una afirmacion de trazabilidad falsa;
    corregido para que diga lo que de verdad pasa por aqui.
    """

    episode: ObservableEpisode

    score: float

    event: SimilarityExplanation
    context: SimilarityExplanation
    outcome: SimilarityExplanation

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
