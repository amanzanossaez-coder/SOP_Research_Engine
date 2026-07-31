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

        if record.forecast is None:
            continue

        if record.actual is None:
            continue

        errors.append(abs(record.forecast - record.actual))

    if not errors:
        return None

    return sum(errors) / len(errors)


EXPLORATORY_DISCLAIMER = (
    "Resultados exploratorios. Tamaño muestral reducido y episodios "
    "no necesariamente independientes entre sí. No constituyen "
    "validación estadística en sentido estricto."
)