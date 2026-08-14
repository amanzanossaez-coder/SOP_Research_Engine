from core.confidence import categorize
from engine.research_pipeline import build_research_result
from engine.validation_engine import ValidationEngine


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

    RE-027.5: DecisionEngine deja de reimplementar el pipeline de
    Research. Consume la misma fuente de verdad que ResearchEngine:
    build_research_result(). Asi, Snapshot -> ObservableUniverse ->
    SimilarityEngine.top() -> EvidenceEngine vive en un solo sitio.

    RE-044.1: confidence() dejo de ser la excepcion a la regla de
    arriba. Hasta esta iteracion calculaba su propio conteo de matches
    con score >= 0.75 y sus propios umbrales (>=8, >=4) -- logica
    estadistica propia, contradiciendo directamente el parrafo
    anterior. Ahora delega en ValidationEngine.confidence() (la misma
    fuente que ya usaba AssessmentEngine) + core.confidence.categorize()
    -- una sola forma de leer confianza en todo el motor, no dos que
    podian discrepar en silencio. A dia de esta iteracion discrepaban:
    la logica vieja leia BAJA para el snapshot real de hoy: la nueva
    lee ALTA (score 0.884). Ver core/confidence.py para el porque y el
    caveat pendiente (stability sigue siendo un placeholder).
    """

    def __init__(self, dataset):

        self.dataset = dataset

        self.research = build_research_result(
            dataset,
            matches_count=10,
            horizon_years=5,
        )

        self.snapshot = self.research.snapshot

        self._matches = self.research.matches

        self.evidence = self.research.evidence

        self.validation = ValidationEngine()

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

        # RE-044.1 -- delega en el sistema unico de confianza
        # (ValidationEngine.confidence() + core.confidence.categorize()),
        # ya no calcula su propio umbral. Ver docstring de la clase.

        return categorize(
            self.validation.confidence(self._matches).score
        )
