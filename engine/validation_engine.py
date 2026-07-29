from statistics import pstdev

from models.confidence import Confidence
from models.similarity import Similarity


class ValidationEngine:

    def coverage(self, matches: list[Similarity]) -> float:

        return min(len(matches) / 10.0, 1.0)

    def consistency(
        self,
        matches: list[Similarity],
        horizon: str = "future_return_3y",
    ) -> float:

        values = []

        for match in matches:

            value = getattr(match.episode, horizon)

            if value is not None:
                values.append(value)

        if len(values) < 2:
            return 0.0

        dispersion = pstdev(values)

        return max(0.0, 1.0 - dispersion)

    def diversity(self, matches: list[Similarity]) -> float:

        decades = set()

        for match in matches:

            year = int(match.episode.bottom_date)

            decades.add((year // 10) * 10)

        return min(len(decades) / max(len(matches), 1), 1.0)

    def stability(self) -> float:

        # Se implementará cuando comparemos versiones del motor.
        return 1.0

    def confidence(
        self,
        matches: list[Similarity],
    ) -> Confidence:

        coverage = self.coverage(matches)

        consistency = self.consistency(matches)

        diversity = self.diversity(matches)

        stability = self.stability()

        score = (
            coverage
            + consistency
            + diversity
            + stability
        ) / 4.0

        return Confidence(
            coverage=coverage,
            stability=stability,
            consistency=consistency,
            diversity=diversity,
            score=score,
        )