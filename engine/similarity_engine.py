from core.constants import (
    SIMILARITY_SCALES,
    SIMILARITY_WEIGHTS,
)
from core.similarity_metrics import (
    LinearMetric,
    PercentileMetric,
)
from models.similarity_explanation import (
    SimilarityExplanation,
    SimilarityExplanationItem,
)
from models.similarity import Similarity


class SimilarityEngine:
    """
    RE-023.5: deja de depender de un Dataset completo. Acepta
    directamente una coleccion de episodios ya resuelta por quien la
    construye -- hoy, ObservableUniverse.episodes() en el flujo real
    (DecisionEngine), o dataset.episodes en AssessmentEngine, que
    todavia no esta conectado a Universe (fuera de alcance de
    RE-023.5).

    cape_metric se calibra sobre esa misma coleccion salvo que se
    proporcione un override explicito (RE-022). Al recibir episodios
    ya temporalmente seguros, la calibracion queda segura sin tener
    que saber nada de as_of ni de ObservableUniverse -- la seguridad
    la aporta quien construye la coleccion, no este motor.
    """

    def __init__(
        self,
        episodes,
        cape_metric=None,
    ):

        self._episodes = list(episodes)

        self.drawdown_metric = LinearMetric(
            SIMILARITY_SCALES["drawdown"]
        )

        self.duration_metric = LinearMetric(
            SIMILARITY_SCALES["duration"]
        )

        self.speed_metric = LinearMetric(
            SIMILARITY_SCALES["speed"]
        )

        self.recovery_metric = LinearMetric(
            SIMILARITY_SCALES["recovery"]
        )

        if cape_metric is None:

            self.cape_metric = PercentileMetric(

                episode.context.cape

                for episode in self._episodes

                if (
                    episode.context is not None
                    and episode.context.cape is not None
                )

            )

        else:

            self.cape_metric = cape_metric

        self.pre_crash_return_3y_metric = LinearMetric(
            SIMILARITY_SCALES["pre_crash_return_3y"]
        )

        self.volatility_metric = LinearMetric(
            SIMILARITY_SCALES["volatility"]
        )

    def _weighted_score(self, scores):

        active = {
            name: value
            for name, value in scores.items()
            if value is not None
        }

        if not active:
            return 0.0

        total_weight = sum(
            SIMILARITY_WEIGHTS[name]
            for name in active
        )

        result = 0.0

        for name, value in active.items():

            result += (
                value
                * SIMILARITY_WEIGHTS[name]
                / total_weight
            )

        return result

    def compare(self, snapshot):

        results = []

        snapshot_speed = None

        if (
            snapshot.duration_months is not None
            and snapshot.duration_months > 0
        ):
            snapshot_speed = (
                abs(snapshot.drawdown)
                / snapshot.duration_months
            )

        snapshot_context = snapshot.context

        for episode in self._episodes:

            episode_context = episode.context

            drawdown_score = self.drawdown_metric.compare(
                snapshot.drawdown,
                episode.drawdown,
            )

            duration_score = self.duration_metric.compare(
                snapshot.duration_months,
                episode.duration_months,
            )

            speed_score = self.speed_metric.compare(
                snapshot_speed,
                episode.speed_down,
            )

            cape_score = self.cape_metric.compare(
                snapshot_context.cape,
                episode_context.cape,
            )

            pre_crash_return_3y_score = (
                self.pre_crash_return_3y_metric.compare(
                    snapshot_context.pre_crash_return_3y,
                    episode_context.pre_crash_return_3y,
                )
            )

            volatility_score = (
                self.volatility_metric.compare(
                    snapshot_context.pre_crash_volatility_1y,
                    episode_context.pre_crash_volatility_1y,
                )
            )

            recovery_score = self.recovery_metric.compare(
                0,
                episode.recovery_months,
            )

            event_score = self._weighted_score(
                {
                    "drawdown": drawdown_score,
                    "duration": duration_score,
                    "speed": speed_score,
                }
            )

            context_score = self._weighted_score(
                {
                    "cape": cape_score,
                    "pre_crash_return_3y": pre_crash_return_3y_score,
                    "volatility": volatility_score,
                }
            )

            outcome_score = self._weighted_score(
                {
                    "recovery": recovery_score,
                }
            )

            score = self._weighted_score(
                {
                    "drawdown": drawdown_score,
                    "duration": duration_score,
                    "speed": speed_score,
                    "cape": cape_score,
                    "pre_crash_return_3y": pre_crash_return_3y_score,
                    "volatility": volatility_score,
                }
            )

            event = SimilarityExplanation(
                title="Event",
                score=event_score,
                items=[
                    SimilarityExplanationItem(
                        name="Drawdown",
                        score=drawdown_score,
                    ),
                    SimilarityExplanationItem(
                        name="Duration",
                        score=duration_score,
                    ),
                    SimilarityExplanationItem(
                        name="Speed",
                        score=speed_score,
                    ),
                ],
            )

            context = SimilarityExplanation(
                title="Context",
                score=context_score,
                items=[
                    SimilarityExplanationItem(
                        name="CAPE",
                        score=cape_score,
                    ),
                    SimilarityExplanationItem(
                        name="Trend 3Y",
                        score=pre_crash_return_3y_score,
                    ),
                    SimilarityExplanationItem(
                        name="Volatility",
                        score=volatility_score,
                    ),
                ],
            )

            outcome = SimilarityExplanation(
                title="Outcome",
                score=outcome_score,
                items=[
                    SimilarityExplanationItem(
                        name="Recovery",
                        score=recovery_score,
                    ),
                ],
            )

            results.append(
                Similarity(
                    episode=episode,
                    score=score,
                    event=event,
                    context=context,
                    outcome=outcome,
                    drawdown_score=drawdown_score,
                    duration_score=duration_score,
                    speed_score=speed_score,
                    cape_score=cape_score,
                    pre_crash_return_3y_score=pre_crash_return_3y_score,
                    volatility_score=volatility_score,
                    recovery_score=recovery_score,
                )
            )

        results.sort(
            key=lambda x: x.score,
            reverse=True,
        )

        return results

    def top(self, snapshot, n=10, exclude_recent_months=24):
        # RE-004: excluye episodios cuyo peak_date esté en los últimos 24 meses.
        # RE-023.5: redundante en parte con el corte temporal que ya aplica
        # ObservableUniverse (bottom_date <= as_of) cuando el llamante
        # proviene de ahi -- se mantiene deliberadamente hasta RE-023.6,
        # que retirará solo la mitad de fuga temporal y conservará la
        # exclusión de episodios solapados.
        cutoff = snapshot.date - (exclude_recent_months / 12)
        results = [
            s for s in self.compare(snapshot)
            if s.episode.peak_date < cutoff
        ]
        return results[:n]
