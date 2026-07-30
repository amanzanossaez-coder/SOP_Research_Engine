from models.explanation import Explanation


class ExplanationEngine:
    """
    Builds a human-readable explanation of the evidence.

    This engine never modifies the evidence.
    It only explains how it was produced.
    """

    def __init__(self, matches):

        self.matches = matches

    def build(self):

        sample_size = len(self.matches)

        top_matches = self.matches[:5]

        strongest = []
        weakest = []

        if self.matches:

            first = self.matches[0]

            dimensions = [
                ("Drawdown", first.event.drawdown_similarity),
                ("Duration", first.event.duration_similarity),
                ("Speed", first.event.speed_similarity),
                ("CAPE", first.context.cape_similarity),
                ("Trend 3Y", first.context.trend_similarity),
                ("Volatility", first.context.volatility_similarity),
                ("Recovery", first.outcome.recovery_similarity),
            ]

            dimensions.sort(
                key=lambda x: x[1],
                reverse=True,
            )

            strongest = dimensions[:3]
            weakest = dimensions[-3:]

        notes = [
            f"Evidence generated from {sample_size} historical episodes."
        ]

        return Explanation(

            sample_size=sample_size,

            top_matches=top_matches,

            strongest_dimensions=strongest,

            weakest_dimensions=weakest,

            notes=notes,

        )
    