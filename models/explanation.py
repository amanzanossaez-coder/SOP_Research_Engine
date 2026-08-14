from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ContradictingPrecedent:
    """
    RE-EXP.1 -- a single historical match whose actual outcome
    disagrees with the evidence's central estimate
    (Evidence.median_return) at the same horizon.

    This is explicit counter-evidence (Articulo 8: "identificar las
    variables que sustentan cada resultado y las variables que lo
    contradicen"), not a similarity diagnostic -- it says nothing
    about how alike the episode looked going in, only that its actual
    result disagreed with what the evidence concluded.
    """

    episode_date: float
    actual_return: float
    similarity_score: float


@dataclass
class Explanation:
    """
    Human-readable explanation of the historical evidence.

    This object exists only to explain
    how the Research Engine reached its evidence.

    It never contains recommendations
    or portfolio decisions.

    RE-EXP.1 -- reconnected and corrected. Two independent problems
    fixed together, both surfaced by the same audit against the
    Research Engine's Articulo 8:

    1. strongest_dimensions/weakest_dimensions read
       first.event.drawdown_similarity -- an attribute that never
       existed on the real SimilarityExplanation object; confirmed by
       running it: AttributeError. Also only looked at the single
       best match, never averaged across the sample. Renamed to
       supporting_similarity_dimensions/weak_similarity_dimensions and
       now averaged over every match (see
       engine/explanation_engine.py).

    2. Articulo 8 requires variables that CONTRADICT a result, not
       only ones that support it. Nothing here did that before --
       strongest/weakest dimensions describe how good the historical
       analogy is, not whether history actually agrees with the
       conclusion. contradicting_precedents is new: historical matches
       whose actual return disagreed in sign with
       Evidence.median_return (or, when the median has no clear sign,
       the matches furthest from it) -- see
       ExplanationEngine._contradicting_precedents for the exact rule.
    """

    # Historical sample

    sample_size: int

    # Similar historical episodes

    top_matches: list["Similarity"]

    # Dimensions ranked by importance, averaged across the whole
    # match set (RE-EXP.1 -- no longer just the single best match)

    supporting_similarity_dimensions: list[tuple[str, float]]

    weak_similarity_dimensions: list[tuple[str, float]]

    # RE-EXP.1 -- explicit counter-evidence, distinct from the
    # similarity diagnostics above. May legitimately be empty; see
    # notes for why (evidence unavailable vs. genuinely no dissent).

    contradicting_precedents: list[ContradictingPrecedent]

    # Optional observations

    notes: list[str]
