from datetime import date

from core.constants import DEFAULT_MATCH_COUNT
from core.version import ENGINE_NAME, ENGINE_VERSION
from engine.evidence_engine import EvidenceEngine
from engine.explanation_engine import ExplanationEngine
from engine.observable_universe import ObservableUniverse
from engine.similarity_engine import SimilarityEngine
from engine.snapshot_engine import SnapshotEngine
from models.research_result import ResearchResult


def build_research_result(
    dataset,
    matches_count: int = DEFAULT_MATCH_COUNT,
    horizon_years: int = 5,
) -> ResearchResult:
    """
    Single source of truth for the objective Research pipeline.

    RE-027.5 extracts the shared Snapshot -> ObservableUniverse ->
    SimilarityEngine.top() -> EvidenceEngine flow so ResearchEngine and
    DecisionEngine cannot drift into two independent implementations.
    """

    snapshot = SnapshotEngine(dataset).latest()

    universe = ObservableUniverse(
        dataset,
        as_of=snapshot.date,
    )

    similarity = SimilarityEngine(
        universe.episodes(),
    )

    matches = similarity.top(
        snapshot,
        n=matches_count,
    )

    evidence = EvidenceEngine().build(
        matches,
        years=horizon_years,
    )

    # RE-EXP.1 -- reconecta ExplanationEngine, excluido desde RE-027.2.
    # Recibe evidence (ademas de matches) para leer median_return/
    # horizon_years ya calculados, sin recalcularlos por su cuenta.
    explanation = ExplanationEngine(matches, evidence).build()

    return ResearchResult(
        snapshot=snapshot,
        matches=matches,
        evidence=evidence,
        explanation=explanation,
        # RE-044.4 -- Articulo 5 (Trazabilidad). engine_name/
        # engine_version vienen de core/version.py, no se reinventan
        # aqui. matches_count/horizon_years son los parametros reales
        # que esta llamada recibio, no un valor asumido.
        engine_name=ENGINE_NAME,
        engine_version=ENGINE_VERSION,
        matches_count=matches_count,
        horizon_years=horizon_years,
        generated_at=date.today(),
    )
