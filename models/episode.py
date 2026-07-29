from dataclasses import dataclass

from models.context import Context


@dataclass
class Episode:

    # Índices

    peak_index: int
    bottom_index: int

    # Fechas

    peak_date: float
    bottom_date: float

    # Precios

    peak_price: float
    bottom_price: float

    # Mercado

    drawdown: float

    # Recuperación

    recovery_index: int | None = None
    recovery_date: float | None = None

    recovery_months: int | None = None

    # Evento

    duration_months: int | None = None

    # Contexto

    context: Context | None = None

    # Rentabilidades posteriores

    future_return_1y: float | None = None
    future_return_3y: float | None = None
    future_return_5y: float | None = None
    future_return_10y: float | None = None

    # Probabilidades

    probability_positive_1y: float | None = None
    probability_positive_3y: float | None = None
    probability_positive_5y: float | None = None
    probability_positive_10y: float | None = None

    @property
    def speed_down(self) -> float | None:

        if self.duration_months is None:
            return None

        if self.duration_months == 0:
            return None

        return abs(self.drawdown) / self.duration_months