from engine.evidence_engine import EvidenceEngine
from engine.observable_universe import ObservableUniverse
from engine.similarity_engine import SimilarityEngine
from engine.snapshot_engine import SnapshotEngine
from engine.validation_engine import ValidationEngine


class AssessmentEngine:

    def __init__(self, dataset):

        self.dataset = dataset

        self.snapshot = SnapshotEngine(dataset).latest()

        # RE-024.3:
        # AssessmentEngine adopta el mismo flujo operativo que
        # DecisionEngine:
        #
        # Dataset -> ObservableUniverse -> Similarity -> Evidence
        #
        # ValidationEngine permanece sin cambios en esta iteración.

        self.universe = ObservableUniverse(
            dataset,
            as_of=self.snapshot.date,
        )

        self.similarity = SimilarityEngine(
            self.universe.episodes(),
        )

        self.matches = self.similarity.top(
            self.snapshot,
            n=10,
        )

        self.validation = ValidationEngine()

        self.confidence = self.validation.confidence(
            self.matches,
        )

        self.evidence = EvidenceEngine().build(
            self.matches,
            years=5,
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