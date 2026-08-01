from typing import List, Optional

from engine.validation_harness import ValidationRecord


def mean_absolute_error(
    records: List[ValidationRecord],
) -> Optional[float]:
    """
    Mean Absolute Error (MAE).

    Compara el forecast generado por EvidenceEngine frente al
    retorno real observado.

    Solo se utilizan registros evaluables.
    """

    errors = []

    for record in records:

        if not record.evaluable:
            continue

        errors.append(abs(record.forecast - record.actual))

    if not errors:
        return None

    return sum(errors) / len(errors)


def directional_hit_rate(
    records: List[ValidationRecord],
) -> Optional[float]:
    """
    Directional Hit Rate.

    Compara si forecast y retorno real observado tienen el mismo signo.

    Solo se utilizan registros evaluables con forecast y actual
    distintos de cero. Un cero no expresa direccion.
    """

    hits = []

    for record in records:

        if not record.evaluable:
            continue

        if record.forecast == 0 or record.actual == 0:
            continue

        hits.append(
            (record.forecast > 0) == (record.actual > 0)
        )

    if not hits:
        return None

    return sum(hits) / len(hits)


def _average_ranks(values: List[float]) -> List[float]:
    """
    Ranking 1-indexado con empates resueltos por average rank: dos
    valores iguales reciben el promedio de las posiciones que
    ocuparian si se desempataran arbitrariamente. Es la convencion
    estandar de Spearman -- evita que el orden de llegada (o de
    construccion de la lista) decida silenciosamente un desempate.
    """

    n = len(values)

    order = sorted(range(n), key=lambda i: values[i])

    ranks = [0.0] * n

    i = 0

    while i < n:

        j = i

        while (
            j + 1 < n
            and values[order[j + 1]] == values[order[i]]
        ):
            j += 1

        average_rank = (i + j) / 2 + 1

        for k in range(i, j + 1):
            ranks[order[k]] = average_rank

        i = j + 1

    return ranks


def rank_correlation(
    records: List[ValidationRecord],
) -> Optional[float]:
    """
    Spearman rank correlation (RE-025.4) entre forecast y actual,
    sobre records evaluables -- misma condicion que
    mean_absolute_error()/directional_hit_rate(), sin excepcion para
    ceros: aqui un cero es un valor mas a ordenar, no una ausencia de
    direccion (esa distincion solo aplicaba a directional_hit_rate).

    Empates resueltos con average ranks (_average_ranks) -- calculado
    como correlacion de Pearson sobre los rangos, que es exactamente
    Spearman's rho cuando no hay empates y su generalizacion correcta
    cuando si los hay (la formula clasica 1 - 6*sum(d^2)/(n*(n^2-1))
    asume ranks sin empatar y se desvia si se aplica directamente
    sobre datos empatados). En este dataset los empates son reales,
    no un caso de esquina: varios episodios comparten forecast exacto
    porque EvidenceEngine.median_return() puede repetirse cuando el
    conjunto de matches no cambia de un episodio al siguiente.

    Responde una pregunta distinta a directional_hit_rate(): no si el
    signo coincide, sino si un forecast mas alto tiende a acompañar
    un retorno real mas alto -- por eso sigue siendo informativa
    incluso sabiendo que 0/19 forecasts fueron negativos (RE-025.3).

    None si hay menos de 2 records evaluables, o si todos los
    forecasts (o todos los actuals) son identicos -- el ranking no
    contiene informacion y la correlacion no esta definida. Ausencia
    de evidencia, nunca 0.0: misma regla de diseno que el resto de
    este modulo y de Evidence (RE-024.1) -- un 0.0 aqui afirmaria
    "sin correlacion", no "no se pudo calcular".
    """

    forecasts = []
    actuals = []

    for record in records:

        if not record.evaluable:
            continue

        forecasts.append(record.forecast)
        actuals.append(record.actual)

    n = len(forecasts)

    if n < 2:
        return None

    forecast_ranks = _average_ranks(forecasts)
    actual_ranks = _average_ranks(actuals)

    if len(set(forecast_ranks)) == 1:
        return None

    if len(set(actual_ranks)) == 1:
        return None

    mean_forecast_rank = sum(forecast_ranks) / n
    mean_actual_rank = sum(actual_ranks) / n

    covariance = sum(
        (fr - mean_forecast_rank) * (ar - mean_actual_rank)
        for fr, ar in zip(forecast_ranks, actual_ranks)
    )

    forecast_variance = sum(
        (fr - mean_forecast_rank) ** 2
        for fr in forecast_ranks
    )

    actual_variance = sum(
        (ar - mean_actual_rank) ** 2
        for ar in actual_ranks
    )

    denominator = (forecast_variance * actual_variance) ** 0.5

    if denominator == 0:
        return None

    return covariance / denominator


EXPLORATORY_DISCLAIMER = (
    "Resultados exploratorios. Tamaño muestral reducido y episodios "
    "no necesariamente independientes entre sí. No constituyen "
    "validación estadística en sentido estricto."
)
