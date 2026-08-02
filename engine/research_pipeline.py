from engine.evidence_engine import EvidenceEngine
from engine.observable_universe import ObservableUniverse
from engine.similarity_engine import SimilarityEngine
from engine.snapshot_engine import SnapshotEngine
from models.research_result import ResearchResult


def build_research_result(
    dataset,
    matches_count: int = 10,
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

    return ResearchResult(
        snapshot=snapshot,
        matches=matches,
        evidence=evidence,
    )
