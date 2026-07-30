from dataclasses import dataclass

from models.evidence import Evidence
from models.explanation import Explanation


@dataclass
class ResearchResult:
    """
    Complete output produced by the Research Engine.

    The Research Engine is responsible for generating
    objective historical evidence together with the
    explanation of how that evidence was obtained.

    It never contains recommendations or portfolio
    decisions.
    """

    evidence: Evidence

    explanation: Explanation