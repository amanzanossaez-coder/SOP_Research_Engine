from engine.evidence_engine import EvidenceEngine
from engine.observable_universe import ObservableUniverse
from engine.similarity_engine import SimilarityEngine
from engine.snapshot_engine import SnapshotEngine
from models.research_result import ResearchResult


class ResearchEngine:
    """
    Orchestrates the objective Research pipeline.

    RE-027.3 rebuilds ResearchEngine as a thin facade over the same
    operative flow already verified through DecisionEngine:

    SnapshotEngine
    -> ObservableUniverse
    -> SimilarityEngine.top()
    -> EvidenceEngine
    -> ResearchResult

    ResearchEngine produces evidence. It never produces portfolio
    decisions, recommendations or protocol actions.
    """

    def run(
        self,
        dataset,
        matches_count: int = 10,
        horizon_years: int = 5,
    ) -> ResearchResult:

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
