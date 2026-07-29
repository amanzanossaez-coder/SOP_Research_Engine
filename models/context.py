from dataclasses import dataclass


@dataclass
class Context:

    # Valoración

    cape: float | None = None

    # Tendencia previa

    pre_crash_return_3y: float | None = None

    # Régimen del mercado

    pre_crash_volatility_1y: float | None = None

    # Macroeconomía

    inflation: float | None = None

    interest_rate: float | None = None