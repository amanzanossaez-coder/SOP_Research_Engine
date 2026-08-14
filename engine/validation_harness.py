from dataclasses import dataclass
from typing import List, Optional

from core.constants import DEFAULT_MATCH_COUNT
from engine.observable_universe import ObservableUniverse
from engine.similarity_engine import SimilarityEngine
from engine.evidence_engine import EvidenceEngine
from models.snapshot import Snapshot


def episode_to_snapshot(episode) -> Snapshot:
    """
    RE-025.1 -- adaptador Episode -> Snapshot.

    No existia en el repo. SimilarityEngine.compare()/top() solo
    aceptan un Snapshot (fecha, drawdown, duration_months, context) --
    nunca un Episode. Para preguntarle al sistema "que hubieras dicho
    en este episodio historico" hace falta reconstruirlo como si fuera
    un Snapshot de consulta, exactamente como DecisionEngine construye
    el Snapshot de "hoy".

    date = episode.bottom_date, no peak_date -- coherente con
    ObservableUniverse (RE-023.4), que ya usa bottom_date como el
    instante en que Event/Context quedan cerrados y observables.

    index/price no participan en ningun metric de SimilarityEngine.
    Se rellenan con los valores reales del propio episodio (no con
    None ni con placeholders inventados) por una sola razon: Snapshot
    es un dataclass compartido con el resto del sistema, y un futuro
    consumidor de estos campos no deberia heredar un valor falso
    fabricado aqui solo para satisfacer el tipo.
    """

    return Snapshot(
        index=episode.bottom_index,
        date=episode.bottom_date,
        price=episode.bottom_price,
        drawdown=episode.drawdown,
        duration_months=episode.duration_months,
        context=episode.context,
    )


@dataclass
class ValidationRecord:
    """
    Una fila del harness: un episodio evaluado contra si mismo,
    excluido de sus propios comparables.

    forecast/actual siguen la regla de diseno del Research Engine:
    None significa ausencia de dato, nunca 0.0 (ver models/evidence.py).

    evaluable es explicito y no se infiere en RE-025.2: un record con
    forecast=None o actual=None simplemente no entra en el MAE, pero
    sigue siendo visible aqui para poder explicar por que.
    """

    episode: object
    horizon_years: int
    forecast: Optional[float]
    actual: Optional[float]
    comparable_count: int
    evaluable: bool


class ValidationHarness:
    """
    RE-025.1 -- Research Validation Engine, primera pieza.

    Responsabilidad unica: producir, por cada episodio del Dataset,
    el par (forecast, actual) que el sistema habria producido si se
    le hubiera preguntado en ese instante historico -- sin calcular
    ningun estadistico agregado todavia (MAE es RE-025.2, hit-rate
    RE-025.3, rank correlation RE-025.4).

    Tres decisiones de diseno deliberadas, no accidentales:

    1. Point-in-time, no LOOCV global. Los comparables de un episodio
       X son ObservableUniverse(dataset, as_of=X.bottom_date).episodes()
       -- el mismo mecanismo temporal que ya usa DecisionEngine en
       produccion (RE-023.5). Comparar X contra los demas episodios
       del Dataset sin restriccion de fecha validaria un sistema
       distinto al que realmente se ejecuta: uno que en 1962 ya
       conociera 2020. Se descarta a proposito -- lo que este harness
       mide tiene que ser el mismo sistema que corre DecisionEngine,
       no una version hipotetica mas informada.

    2. Autoexclusion explicita por bottom_index, no por identidad de
       objeto ni por el filtro de recencia de SimilarityEngine.top().
       ObservableUniverse.episodes() devuelve ObservableEpisode, un
       tipo distinto de Episode por diseno (RE-023.1) -- nunca el
       mismo objeto que el Episode canonico evaluado, asi que un
       `is not` nunca habria excluido nada. bottom_index es el unico
       campo que sobrevive intacto de Episode a ObservableEpisode y
       es unico por episodio; se usa como clave de exclusion. Tampoco
       se reutiliza exclude_recent_months de SimilarityEngine.top()
       para este proposito -- RE-023.6 ya deja escrito que ese filtro
       no nace como proteccion anti-fuga, y apoyarse en el aqui
       crearia una dependencia accidental de como evolucione.

    3. sample_size y evaluated_count son metodos separados y
       explicitos, calculados sobre los records ya producidos -- no
       numeros asumidos de antemano. sample_size cuenta episodios con
       future_return_Xy real conocido (evidencia disponible, en
       principio); evaluated_count cuenta los que ademas produjeron
       forecast (el harness encontro al menos un comparable). La
       diferencia entre ambos es informativa por si misma: dice
       cuantos episodios se quedaron sin precedentes historicos
       suficientes en su propio instante.
    """

    def __init__(self, dataset, n_matches: int = DEFAULT_MATCH_COUNT):

        self.dataset = dataset
        self.n_matches = n_matches

    def _comparable_episodes(self, target_episode):

        universe = ObservableUniverse(
            self.dataset,
            as_of=target_episode.bottom_date,
        )

        return [
            e
            for e in universe.episodes()
            if e.bottom_index != target_episode.bottom_index
        ]

    def evaluate_episode(
        self,
        episode,
        years: int = 5,
    ) -> ValidationRecord:

        actual = getattr(episode, f"future_return_{years}y")

        comparables = self._comparable_episodes(episode)

        if not comparables:

            return ValidationRecord(
                episode=episode,
                horizon_years=years,
                forecast=None,
                actual=actual,
                comparable_count=0,
                evaluable=False,
            )

        snapshot = episode_to_snapshot(episode)

        similarity = SimilarityEngine(comparables)

        matches = similarity.top(snapshot, n=self.n_matches)

        if not matches:

            return ValidationRecord(
                episode=episode,
                horizon_years=years,
                forecast=None,
                actual=actual,
                comparable_count=0,
                evaluable=False,
            )

        evidence = EvidenceEngine().build(matches, years=years)

        forecast = evidence.median_return

        return ValidationRecord(
            episode=episode,
            horizon_years=years,
            forecast=forecast,
            actual=actual,
            comparable_count=len(matches),
            evaluable=(forecast is not None and actual is not None),
        )

    def run(self, years: int = 5) -> List[ValidationRecord]:

        return [
            self.evaluate_episode(episode, years=years)
            for episode in self.dataset.episodes
        ]

    def sample_size(self, records: List[ValidationRecord]) -> int:

        return sum(
            1
            for r in records
            if r.actual is not None
        )

    def evaluated_count(self, records: List[ValidationRecord]) -> int:

        return sum(
            1
            for r in records
            if r.evaluable
        )
