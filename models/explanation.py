from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Explanation:
    """
    Human-readable explanation of the historical evidence.

    This object exists only to explain
    how the Research Engine reached its evidence.

    It never contains recommendations
    or portfolio decisions.
    """

    # Historical sample

    sample_size: int

    # Similar historical episodes

    top_matches: list["Similarity"]

    # Dimensions ranked by importance

    strongest_dimensions: list[tuple[str, float]]

    weakest_dimensions: list[tuple[str, float]]

    # Optional observations

    notes: list[str]