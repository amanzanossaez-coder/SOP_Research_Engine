from engine.research_pipeline import build_research_result
from engine.validation_engine import ValidationEngine


class AssessmentEngine:
    """
    Interprets Research evidence without rebuilding the Research pipeline.

    RE-029.3 makes AssessmentEngine consume build_research_result(), the
    same source of truth used by DecisionEngine and ResearchEngine. This
    keeps Snapshot -> ObservableUniverse -> SimilarityEngine.top() ->
    EvidenceEngine in one place.

    Confidence remains out of scope for RE-029.3. It is still computed
    by ValidationEngine, including the current stability placeholder
    that returns 1.0. That score must not be used as a capital-allocation
    gate until the placeholder is replaced or explicitly governed.
    """

    def __init__(self, dataset):

        self.dataset = dataset

        self.research = build_research_result(
            dataset,
            matches_count=10,
            horizon_years=5,
        )

        self.snapshot = self.research.snapshot

        self.matches = self.research.matches

        self.evidence = self.research.evidence

        self.validation = ValidationEngine()

        self.confidence = self.validation.confidence(
            self.matches,
        )

    def drawdown_zone(self):

        d = self.snapshot.drawdown

        if d > -0.10:
            return "NORMAL"

        if d > -0.20:
            return "CORRECTION"

        if d > -0.35:
            return "BEAR MARKET"

        return "CRISIS"

    def expected_return_5y(self):

        return self.evidence.median_return

    def upside_potential(self):

        return self.evidence.percentile(0.90)

    def downside_risk(self):

        return self.evidence.worst_return
