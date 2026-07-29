from engine.probability_engine import ProbabilityEngine
from engine.similarity_engine import SimilarityEngine
from engine.snapshot_engine import SnapshotEngine
from engine.validation_engine import ValidationEngine


class AssessmentEngine:

    def __init__(self, dataset):

        self.dataset = dataset

        self.snapshot = SnapshotEngine(dataset).latest()

        self.similarity = SimilarityEngine(dataset)

        self.matches = self.similarity.top(
            self.snapshot,
            n=10,
        )

        self.validation = ValidationEngine()

        self.confidence = self.validation.confidence(
            self.matches,
        )

        self.probability = ProbabilityEngine(dataset)

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

        return self.probability.median(5)

    def upside_potential(self):

        return self.probability.percentile(5, 0.90)

    def downside_risk(self):

        return self.probability.worst_case(5)