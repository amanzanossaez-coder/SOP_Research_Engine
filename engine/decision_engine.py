from engine.snapshot_engine import SnapshotEngine
from engine.probability_engine import ProbabilityEngine
from engine.similarity_engine import SimilarityEngine
from engine.observable_universe import ObservableUniverse


class DecisionEngine:
    """
    RE-023.5: la similitud pasa a consumir ObservableUniverse en vez
    de dataset.episodes directamente. as_of = self.snapshot.date --
    la fecha de la snapshot evaluada, que en el flujo real de run.py
    es "latest". probability sigue sobre el Dataset completo; no es
    parte del alcance de esta iteración (queda pendiente, con el
    mismo tipo de riesgo temporal, para una iteración futura).
    """

    def __init__(self, dataset):

        self.dataset = dataset

        self.snapshot = SnapshotEngine(dataset).latest()

        self.universe = ObservableUniverse(
            dataset,
            as_of=self.snapshot.date,
        )

        self.probability = ProbabilityEngine(dataset)

        self.similarity = SimilarityEngine(self.universe.episodes())

    def market_position(self):
        # RE-003: posición en ciclo — solo depende del drawdown
        d = self.snapshot.drawdown
        if d > -0.10: return "EN MÁXIMOS"
        if d > -0.20: return "CORRECCIÓN"
        if d > -0.35: return "BEAR MARKET"
        if d > -0.50: return "CRISIS"
        return "COLAPSO"

    def valuation_zone(self):
        # RE-003: valoración — solo depende del CAPE
        cape = self.snapshot.context.cape if self.snapshot.context else None
        if cape is None: return "SIN DATOS"
        if cape < 15: return "BARATA"
        if cape < 22: return "NORMAL"
        if cape < 30: return "CARA"
        return "MUY CARA"

    def volatility_regime(self):
        # RE-003: régimen de volatilidad
        vol = self.snapshot.context.pre_crash_volatility_1y if self.snapshot.context else None
        if vol is None: return "SIN DATOS"
        if vol < 0.10: return "BAJA VOLATILIDAD"
        if vol < 0.18: return "VOLATILIDAD NORMAL"
        if vol < 0.25: return "ALTA VOLATILIDAD"
        return "VOLATILIDAD EXTREMA"

    def market_zone(self):
        # Compatibilidad — usar market_position() para análisis completo
        return self.market_position()

    def expected_return(self):

        return self.probability.median(5)

    def upside(self):

        return self.probability.best_case(5)

    def downside(self):

        return self.probability.worst_case(5)

    def historical_matches(self):

        return self.similarity.top(
            self.snapshot,
            n=10,
        )

    def confidence(self):

        matches = len(

            [

                s

                for s in self.historical_matches()

                if s.score >= 0.75

            ]

        )

        if matches >= 8:
            return "ALTA"

        if matches >= 4:
            return "MEDIA"

        return "BAJA"
