from engine.snapshot_engine import SnapshotEngine
from engine.similarity_engine import SimilarityEngine
from engine.evidence_engine import EvidenceEngine
from engine.explanation_engine import ExplanationEngine
from engine.assessment_engine import AssessmentEngine


class ResearchEngine:
    """
    Orchestrates the complete research pipeline.

    The Research Engine never manipulates DataFrames directly.
    It coordinates the domain engines.
    """

    def __init__(self):

        self.snapshot_engine = SnapshotEngine()
        self.evidence_engine = EvidenceEngine()
        self.explanation_engine = ExplanationEngine()
        self.assessment_engine = AssessmentEngine()

    def run(self, dataset):

        # 1. Build current market snapshot

        snapshot = self.snapshot_engine.build(dataset)

        # 2. Find similar historical episodes

        similarity_engine = SimilarityEngine(dataset)
        similarities = similarity_engine.compare(snapshot)

        # 3. Generate historical evidence

        evidence = self.evidence_engine.build(similarities)

        # 4. Generate explanation

        explanation = self.explanation_engine.build(similarities)

        # Assessment and inference will be incorporated
        # in future iterations.

        return {
            "evidence": evidence,
            "explanation": explanation,
        }