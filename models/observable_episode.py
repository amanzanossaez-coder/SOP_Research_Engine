from dataclasses import dataclass

from models.context import Context
from models.episode import Episode


@dataclass(frozen=True)
class ObservableEpisode:
    """
    Representa un Episode tal como podia observarse en un instante
    temporal determinado (as_of).

    No hereda de Episode (ver ADR-004). La relacion no es de
    especializacion (IS-A), sino de proyeccion (DERIVED-FROM): un
    ObservableEpisode nunca debe poder pasar donde se espera un
    Episode canonico, ni al reves. Mantenerlos como tipos
    independientes hace ese error imposible de representar, no solo
    improbable.

    RE-023.2: transformacion identidad. Todos los campos son
    identicos a los del Episode de origen. El masking de los campos
    Outcome que todavia no serian observables en as_of llega en
    RE-023.3 -- este archivo no aplica ningun corte temporal.
    """

    # Indices

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

    # Recuperacion (Outcome -- se enmascarara en RE-023.3)

    recovery_index: int | None = None
    recovery_date: float | None = None
    recovery_months: int | None = None

    # Evento (Event/Context -- causal, nunca se enmascara)

    duration_months: int | None = None

    # Contexto (Context -- puramente causal; se comparte por
    # referencia con el Episode de origen sin copiar, porque Context
    # no contiene ningun campo Outcome. Si algun dia se anade un
    # campo no causal a Context, esta linea deja de ser segura.)

    context: Context | None = None

    # Rentabilidades posteriores (Outcome -- se enmascararan en RE-023.3)

    future_return_1y: float | None = None
    future_return_3y: float | None = None
    future_return_5y: float | None = None
    future_return_10y: float | None = None

    # Probabilidades (Outcome)

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


def from_episode(episode: Episode) -> ObservableEpisode:
    """
    Construye la proyeccion observable de un Episode canonico.

    RE-023.2: copia campo por campo, sin enmascarar Outcome.
    """

    return ObservableEpisode(
        peak_index=episode.peak_index,
        bottom_index=episode.bottom_index,
        peak_date=episode.peak_date,
        bottom_date=episode.bottom_date,
        peak_price=episode.peak_price,
        bottom_price=episode.bottom_price,
        drawdown=episode.drawdown,
        recovery_index=episode.recovery_index,
        recovery_date=episode.recovery_date,
        recovery_months=episode.recovery_months,
        duration_months=episode.duration_months,
        context=episode.context,
        future_return_1y=episode.future_return_1y,
        future_return_3y=episode.future_return_3y,
        future_return_5y=episode.future_return_5y,
        future_return_10y=episode.future_return_10y,
        probability_positive_1y=episode.probability_positive_1y,
        probability_positive_3y=episode.probability_positive_3y,
        probability_positive_5y=episode.probability_positive_5y,
        probability_positive_10y=episode.probability_positive_10y,
    )
