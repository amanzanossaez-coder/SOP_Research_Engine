from models.dataset import Dataset


class InferenceEngine:

    def __init__(self, dataset: Dataset):
        self.dataset = dataset

    def average_return(self, years: int) -> float:

        values = []

        for e in self.dataset.episodes:

            value = getattr(e, f"future_return_{years}y")

            if value is not None:
                values.append(value)

        return sum(values) / len(values)

    def positive_probability(self, years: int) -> float:

        values = []

        for e in self.dataset.episodes:

            value = getattr(e, f"future_return_{years}y")

            if value is not None:
                values.append(value > 0)

        return sum(values) / len(values)

    def drawdowns_greater_than(self, threshold: float):

        return [
            e
            for e in self.dataset.episodes
            if e.drawdown <= threshold
        ]

    def recovered_in_less_than(self, months: int):

        return [
            e
            for e in self.dataset.episodes
            if e.recovery_months is not None
            and e.recovery_months <= months
        ]