from dataclasses import dataclass

from models.context import Context


@dataclass
class Snapshot:

    # Momento temporal
    index: int
    date: float

    # Precio
    price: float

    # Estado del mercado
    drawdown: float
    duration_months: int | None = None

    # Contexto de mercado
    context: Context | None = None