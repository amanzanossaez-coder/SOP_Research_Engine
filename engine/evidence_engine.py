from statistics import mean, median

from models.evidence import Evidence


class EvidenceEngine:

    def __init__(self, matches):

        self.matches = matches

    def build(self):

        returns = [
            s.episode.future_return_5y
            for s in self.matches
            if s.episode.future_return_5y is not None
        ]

        recoveries = [
            s.episode.recovery_months
            for s in self.matches
            if s.episode.recovery_months is not None
        ]

        positive = [
            r
            for r in returns
            if r > 0
        ]

        return Evidence(

            matches=self.matches,

            average_return_5y=(
                mean(returns)
                if returns else 0.0
            ),

            median_return_5y=(
                median(returns)
                if returns else 0.0
            ),

            worst_return_5y=(
                min(returns)
                if returns else 0.0
            ),

            best_return_5y=(
                max(returns)
                if returns else 0.0
            ),

            positive_probability=(
                len(positive) / len(returns)
                if returns else 0.0
            ),

            average_recovery_months=(
                mean(recoveries)
                if recoveries else None
            ),

            median_recovery_months=(
                median(recoveries)
                if recoveries else None
            ),

        )