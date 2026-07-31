from statistics import mean, median

from core.constants import OUTCOME_HORIZONS_YEARS
from models.evidence import Evidence, percentile_from_sorted


class EvidenceEngine:
    """
    Builds objective historical evidence from similar episodes.

    RE-024.1: build() acepta el horizonte (years) como parametro --
    antes estaba fijo a future_return_5y. Selecciona el campo
    future_return_{years}y correspondiente al horizonte pedido.

    Deliberadamente NO se toca hoy: DecisionEngine, AssessmentEngine,
    ProbabilityEngine, SimilarityEngine, ObservableUniverse. Nadie
    consume todavia este Evidence generalizado -- eso es RE-024.2.
    """

    def build(self, matches, years: int = 5):

        if years not in OUTCOME_HORIZONS_YEARS:

            raise ValueError(
                f"years={years!r} no es un horizonte valido -- "
                f"Episode solo almacena future_return_Xy para "
                f"{OUTCOME_HORIZONS_YEARS}"
            )

        field = f"future_return_{years}y"

        returns = sorted(

            value

            for value in (
                getattr(s.episode, field) for s in matches
            )

            if value is not None

        )

        recoveries = [
            s.episode.recovery_months
            for s in matches
            if s.episode.recovery_months is not None
        ]

        positive = [
            r
            for r in returns
            if r > 0
        ]

        return Evidence(

            # Historical sample

            matches=matches,
            episodes_count=len(matches),
            horizon_years=years,

            # Return statistics
            #
            # Ausencia de evidencia -> None, nunca 0.0 (regla de
            # diseño del Research Engine, ver models/evidence.py).
            #
            # median/worst/best usan percentile_from_sorted -- el
            # mismo calculo que expone Evidence.percentile() -- para
            # que evidence.median_return == evidence.percentile(0.5)
            # se cumpla siempre, sin dos algoritmos que puedan
            # desalinearse (statistics.median() promedia el par
            # central en listas de tamaño par; percentile_from_sorted
            # no, y top() suele devolver listas de tamaño par).
            # percentile_from_sorted ya devuelve None si returns esta
            # vacia -- no hace falta un "if returns else ..." aparte.

            average_return=(
                mean(returns)
                if returns else None
            ),

            median_return=percentile_from_sorted(returns, 0.50),

            worst_return=percentile_from_sorted(returns, 0.0),

            best_return=percentile_from_sorted(returns, 1.0),

            positive_probability=(
                len(positive) / len(returns)
                if returns else None
            ),

            # Recovery statistics
            #
            # Sin cambios respecto a la version anterior -- fuera de
            # alcance de RE-024.1.

            average_recovery_months=(
                mean(recoveries)
                if recoveries else None
            ),

            median_recovery_months=(
                median(recoveries)
                if recoveries else None
            ),

        )
