import dataclasses

from core.constants import OUTCOME_HORIZONS_YEARS
from models.observable_episode import from_episode


# RE-024.1: horizontes movidos a core.constants.OUTCOME_HORIZONS_YEARS
# -- antes vivian aqui como una tupla local propia de este archivo,
# duplicados con la lista que EvidenceEngine necesitaba declarar
# por su cuenta.
# Un valor "future_return_Xy" solo es observable en as_of si
# bottom_date + X <= as_of.


def _mask_horizon(value, bottom_date: float, years: int, as_of: float):
    """
    RE-023.3: un dato anclado a un horizonte de X anios desde el
    fondo del episodio solo es observable si ese horizonte ya se
    habria cumplido en as_of. Si todavia no se habria cumplido, el
    dato no existe en as_of -- independientemente de si el Dataset
    canonico ya lo tiene calculado con datos reales posteriores.
    """

    if bottom_date + years <= as_of:
        return value

    return None


def _mask_outcome(episode, as_of: float):
    """
    RE-023.3: enmascara los campos Outcome de un ObservableEpisode
    que todavia no serian observables en as_of.

    No toca Event ni Context -- son causales, nunca se enmascaran.
    No decide si el propio episodio deberia existir en as_of; eso lo
    resuelve el filtro de RE-023.4, antes de llegar aqui.
    """

    recovery_observable = (
        episode.recovery_date is not None
        and episode.recovery_date <= as_of
    )

    horizon_fields = {
        f"future_return_{years}y": _mask_horizon(
            getattr(episode, f"future_return_{years}y"),
            episode.bottom_date,
            years,
            as_of,
        )
        for years in OUTCOME_HORIZONS_YEARS
    }

    probability_fields = {
        f"probability_positive_{years}y": _mask_horizon(
            getattr(episode, f"probability_positive_{years}y"),
            episode.bottom_date,
            years,
            as_of,
        )
        for years in OUTCOME_HORIZONS_YEARS
    }

    return dataclasses.replace(

        episode,

        recovery_index=(
            episode.recovery_index if recovery_observable else None
        ),
        recovery_date=(
            episode.recovery_date if recovery_observable else None
        ),
        recovery_months=(
            episode.recovery_months if recovery_observable else None
        ),

        **horizon_fields,
        **probability_fields,
    )


def _exists_at(episode, as_of: float) -> bool:
    """
    RE-023.4: un episodio existe como evidencia consolidada en as_of
    solo si su fondo ya se alcanzo (bottom_date <= as_of).

    Mientras el mercado sigue cayendo no conocemos el drawdown
    final, la duracion, el CAPE ni la volatilidad del fondo -- el
    Event/Context del episodio todavia no esta cerrado. Por eso el
    corte es bottom_date, no peak_date: peak_date solo marca cuando
    empezo la caida, no cuando el episodio queda definido.

    Este criterio sustituye, para efectos de fuga temporal, al
    filtro por peak_date que hoy vive dentro de
    SimilarityEngine.top(). No sustituye la otra funcion de ese
    filtro -- excluir episodios demasiado cercanos en el tiempo a la
    consulta para evitar comparar contra evidencia solapada -- que
    resuelve un problema distinto y debe seguir viva ahi, aplicada
    sobre la salida de este metodo, hasta que se decida lo
    contrario explicitamente.
    """

    return episode.bottom_date <= as_of


class ObservableUniverse:
    """
    Representa el conocimiento legitimamente observable por el
    Research Engine en un instante temporal determinado (as_of).

    No es una simple vista filtrada del Dataset canonico: determina
    el conjunto de entidades -- episodios, calibraciones,
    distribuciones -- sobre las que el motor puede razonar en ese
    instante (ADR-003).

    Garantias constitucionales:

    G1. Observabilidad temporal -- en as_of solo existe lo que podia
        observarse en as_of.
    G2. Derivacion causal -- cualquier dato derivado se construye
        exclusivamente con informacion observable en as_of.
    G3. Inmutabilidad -- ni ObservableUniverse ni lo que entrega
        puede mutarse. El Dataset canonico nunca se modifica.
    G4. Consistencia -- todo lo que sale de un mismo
        ObservableUniverse pertenece al mismo instante temporal.

    --------------------------------------------------------------
    Decision de diseno P1 (resuelta antes de RE-023.2)
    --------------------------------------------------------------

    ObservableUniverse NO conserva una referencia al Dataset
    canonico completo. Conserva unicamente una proyeccion del
    DataFrame ya recortada a as_of (self._observable_data). Guardar
    el Dataset completo "por si acaso" y confiar en que cada futuro
    metodo aplique el corte temporal por su cuenta es el patron que
    produjo la fuga de CAPE percentile. Aqui el dato inseguro
    simplemente no existe dentro del objeto.

    --------------------------------------------------------------
    RE-023.2 -> RE-023.3 -> RE-023.4
    --------------------------------------------------------------

    RE-023.2 dejo episodes() como transformacion identidad, para
    validar el cableado sin mezclarlo con reglas temporales.

    RE-023.3 introdujo el masking de Outcome por campo/horizonte,
    sin cambiar cuantos episodios se devuelven.

    RE-023.4 (este cambio) introduce el primer cambio al universo de
    evidencia: episodes() ya no devuelve todos los episodios del
    Dataset. Solo devuelve aquellos cuyo bottom_date <= as_of -- los
    que ya existen como evidencia consolidada en ese instante.

    Lo que RE-023.4 deliberadamente NO hace: no toca
    SimilarityEngine.top() ni DecisionEngine. El filtro por
    peak_date que hoy vive dentro de SimilarityEngine sigue ahi sin
    cambios -- retirar su mitad de fuga temporal solo es seguro
    cuando SimilarityEngine consuma este universo en vez de
    dataset.episodes directamente, y ese wiring todavia no existe.
    Hacerlo antes dejaria una ventana sin ninguna proteccion. Su
    otra mitad -- excluir episodios demasiado recientes para evitar
    comparar contra evidencia solapada -- no le corresponde a
    ObservableUniverse en absoluto y debe sobrevivir aparte.
    """

    def __init__(self, dataset, as_of: float):

        self._as_of = as_of

        # Proyeccion temporal del DataFrame canonico. Este es el
        # unico DataFrame accesible dentro del objeto -- nunca se
        # guarda ni se expone dataset.data completo.
        self._observable_data = dataset.data[
            dataset.data["Date"] <= as_of
        ].copy()

        self._observable_episodes = [
            _mask_outcome(from_episode(episode), as_of)
            for episode in dataset.episodes
            if _exists_at(episode, as_of)
        ]

    def as_of(self) -> float:

        return self._as_of

    def episodes(self) -> list:

        # Copia defensiva: la lista interna no debe poder mutarse
        # desde fuera, aunque cada ObservableEpisode ya sea
        # inmutable por si mismo (frozen dataclass).
        return list(self._observable_episodes)

    # cape_metric() se incorpora en una iteracion posterior, una vez
    # decidido como se calibra sobre self._observable_data /
    # self._observable_episodes sin reintroducir fuga temporal.
