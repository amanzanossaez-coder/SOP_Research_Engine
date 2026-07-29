from dataclasses import dataclass

from models.similarity import Similarity


@dataclass
class Evidence:

    # Episodios utilizados

    matches: list[Similarity]

    # Estadísticos principales

    average_return_5y: float

    median_return_5y: float

    worst_return_5y: float

    best_return_5y: float

    positive_probability: float

    # Recuperación

    average_recovery_months: float | None = None

    median_recovery_months: float | None = None