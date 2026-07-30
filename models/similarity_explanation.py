from dataclasses import dataclass


@dataclass
class SimilarityExplanationItem:
    """
    Explains the contribution of a single similarity dimension.
    """

    name: str
    score: float


@dataclass
class SimilarityExplanation:
    """
    Explains why one historical episode is considered similar
    to the current market snapshot.

    This explanation is local to a single Similarity object.
    It must not be confused with the global Research Explanation.
    """

    title: str
    score: float
    items: list[SimilarityExplanationItem]