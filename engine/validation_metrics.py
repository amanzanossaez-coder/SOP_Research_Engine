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


EXPLORATORY_DISCLAIMER = (
    "Resultados exploratorios. Tamaño muestral reducido y episodios "
    "no necesariamente independientes entre sí. No constituyen "
    "validación estadística en sentido estricto."
)
