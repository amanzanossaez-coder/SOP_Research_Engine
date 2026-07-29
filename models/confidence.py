from dataclasses import dataclass


@dataclass
class Confidence:

    # Cobertura de la evidencia
    coverage: float

    # Estabilidad entre versiones del motor
    stability: float

    # Consistencia de los resultados históricos
    consistency: float

    # Diversidad de los precedentes
    diversity: float

    # Score agregado de confianza
    score: float