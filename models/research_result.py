from dataclasses import dataclass

from models.evidence import Evidence
from models.similarity import Similarity
from models.snapshot import Snapshot


@dataclass
class ResearchResult:
    """
    Complete output produced by the Research Engine.

    RE-027.2 aligns ResearchResult with the operative Research
    pipeline that is already verified through DecisionEngine:

    SnapshotEngine
    -> ObservableUniverse
    -> SimilarityEngine.top()
    -> EvidenceEngine

    It contains objective historical evidence and the selected
    historical matches that produced it.

    It does not contain recommendations, portfolio decisions or
    a global explanation object. ExplanationEngine is intentionally
    excluded until it is rebuilt against the current Similarity model.
    """

    snapshot: Snapshot

    matches: list[Similarity]

    evidence: Evidence
