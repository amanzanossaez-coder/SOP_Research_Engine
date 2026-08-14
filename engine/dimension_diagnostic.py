from typing import List

from core.constants import DEFAULT_MATCH_COUNT
from engine.observable_universe import ObservableUniverse
from engine.similarity_engine import SimilarityEngine
from engine.evidence_engine import EvidenceEngine
from engine.validation_harness import ValidationRecord, episode_to_snapshot


# RE-PRED.14 -- dimensiones activas en el score combinado de
# SimilarityEngine.compare()/top(). "recovery" se excluye a proposito:
# RE-021 ya la retiro del score global por fuga de datos (es Outcome,
# solo se conoce despues de que el episodio se resuelve) -- incluirla
# aqui reintroduciria exactamente el problema que esa iteracion
# corrigio. No es una omision, es la misma regla aplicada de nuevo.
DIMENSION_SCORE_FIELDS = [
    "drawdown_score",
    "duration_score",
    "speed_score",
    "cape_score",
    "pre_crash_return_3y_score",
    "volatility_score",
]


def _comparable_episodes(dataset, target_episode) -> list:
    """
    RE-PRED.14 -- misma reimplementacion controlada que ya existe en
    engine/baseline_harness.py (RE-PRED.9) y engine/validation_harness.py
    (RE-025.1): ObservableUniverse(dataset, as_of=target_episode
    .bottom_date).episodes(), autoexcluyendo por bottom_index. Tercera
    copia deliberada, no una dependencia cruzada nueva -- mismo criterio
    que ya se justifico en RE-PRED.9.
    """

    universe = ObservableUniverse(
        dataset,
        as_of=target_episode.bottom_date,
    )

    return [
        e
        for e in universe.episodes()
        if e.bottom_index != target_episode.bottom_index
    ]


def dimension_forecast(
    dataset,
    episode,
    score_field: str,
    years: int = 5,
    n: int = DEFAULT_MATCH_COUNT,
    exclude_recent_months: int = 24,
):
    """
    RE-PRED.14 -- forecast aislado a UNA sola dimension de similitud.

    Reutiliza SimilarityEngine.compare() sin modificarlo: ese metodo ya
    calcula, para cada comparable, el score individual de cada dimension
    (drawdown_score, cape_score, etc.), ademas del score combinado que
    top() usa para seleccionar matches. Este diagnostico simplemente
    reordena esos scores ya calculados por una sola dimension en vez de
    por el score combinado -- no reimplementa ninguna metrica de
    similitud propia.

    Aplica el mismo filtro de recencia que top() (peak_date < cutoff,
    RE-023.6) antes de reordenar, para que la comparacion sea justa: la
    unica diferencia frente a SimilarityEngine.top() debe ser el criterio
    de orden, no las reglas de exclusion.

    Devuelve (forecast, comparable_count) -- forecast es
    EvidenceEngine().build(matches, years).median_return sobre los top-n
    seleccionados por esa dimension sola.
    """

    comparables = _comparable_episodes(dataset, episode)

    if not comparables:
        return None, 0

    snapshot = episode_to_snapshot(episode)

    similarity = SimilarityEngine(comparables)

    scored = similarity.compare(snapshot)

    cutoff = snapshot.date - (exclude_recent_months / 12)

    scored = [s for s in scored if s.episode.peak_date < cutoff]

    # Algunos comparables pueden no tener contexto suficiente para una
    # dimension concreta (p.ej. pre_crash_return_3y_score es None sin
    # 3 anios previos de precio) -- SimilarityEngine._weighted_score()
    # ya excluye esos None del score combinado sin tratarlos como "muy
    # distintos". Aislar una sola dimension debe respetar la misma
    # regla: None no es comparable con un float, se excluye, no se
    # ordena como si fuera el peor valor posible.
    scored = [
        s
        for s in scored
        if getattr(s, score_field) is not None
    ]

    if not scored:
        return None, 0

    scored.sort(
        key=lambda s: getattr(s, score_field),
        reverse=True,
    )

    matches = scored[:n]

    evidence = EvidenceEngine().build(matches, years=years)

    return evidence.median_return, len(matches)


def dimension_records(
    dataset,
    model_records: List[ValidationRecord],
    score_field: str,
) -> List[ValidationRecord]:
    """
    RE-PRED.14 -- produce ValidationRecord aislados a una dimension,
    alineados 1:1 con los del modelo. Mismo principio de RE-PRED.8/9:
    evaluable y actual se heredan del modelo, nunca se decide un
    criterio de inclusion propio para el diagnostico.
    """

    records = []

    for record in model_records:

        forecast, comparable_count = dimension_forecast(
            dataset,
            record.episode,
            score_field,
            years=record.horizon_years,
        )

        records.append(
            ValidationRecord(
                episode=record.episode,
                horizon_years=record.horizon_years,
                forecast=forecast,
                actual=record.actual,
                comparable_count=comparable_count,
                evaluable=(record.evaluable and forecast is not None),
            )
        )

    return records
