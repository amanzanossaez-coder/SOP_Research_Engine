from engine.snapshot_engine import SnapshotEngine
from engine.observable_universe import ObservableUniverse
from engine.similarity_engine import SimilarityEngine
from engine.evidence_engine import EvidenceEngine


class DecisionEngine:
    """
    RE-024.2: expected_return()/upside()/downside() dejan de venir
    de ProbabilityEngine (que ignoraba la similitud y agregaba sobre
    los 23 episodios del Dataset completo) y pasan a venir de
    EvidenceEngine sobre exactamente los mismos matches que se
    muestran en pantalla como "top episodios similares".

    ProbabilityEngine desaparece de este flujo por completo.
    DecisionEngine deja de contener ninguna logica estadistica
    propia: no sabe calcular una mediana, un percentil ni un
    minimo/maximo. Esa responsabilidad vive integramente en
    EvidenceEngine/Evidence. DecisionEngine solo orquesta -- pide
    evidencia y la presenta -- igual que ya hacia con Snapshot,
    Universe y Similarity.

    Contrato: DecisionEngine reutiliza una unica coleccion de
    matches para toda la evidencia del analisis -- Evidence.matches
    y lo que devuelve historical_matches() son, con certeza, la
    misma coleccion, nunca el resultado de dos invocaciones
    separadas de SimilarityEngine.top() (que aunque coincidieran en
    contenido no serian los mismos objetos). Hoy eso se logra
    calculando self._matches una unica vez en __init__; si mañana
    cambia la implementacion, esta propiedad debe seguir
    cumpliendose.
    """

    def __init__(self, dataset):

        self.dataset = dataset

        self.snapshot = SnapshotEngine(dataset).latest()

        self.universe = ObservableUniverse(
            dataset,
            as_of=self.snapshot.date,
        )

        self.similarity = SimilarityEngine(self.universe.episodes())

        self._matches = self.similarity.top(
            self.snapshot,
            n=10,
        )

        self.evidence = EvidenceEngine().build(
            self._matches,
            years=5,
        )

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

        return self.evidence.median_return

    def upside(self):

        return self.evidence.best_return

    def downside(self):

        return self.evidence.worst_return

    def historical_matches(self):

        # Copia superficial deliberada: quien reciba esta lista no
        # debe poder alterar la coleccion interna de matches desde
        # fuera. Los Similarity/ObservableEpisode que contiene ya
        # son inmutables por si mismos; esto protege el contenedor.
        return list(self._matches)

    def confidence(self):

        matches = len(

            [

                s

                for s in self._matches

                if s.score >= 0.75

            ]

        )

        if matches >= 8:
            return "ALTA"

        if matches >= 4:
            return "MEDIA"

        return "BAJA"
