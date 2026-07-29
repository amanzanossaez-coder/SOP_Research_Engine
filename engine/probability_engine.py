from models.dataset import Dataset


class ProbabilityEngine:

    def __init__(self, dataset: Dataset):
        self.dataset = dataset

    def distribution(self, years: int):

        values = []

        for e in self.dataset.episodes:

            value = getattr(e, f"future_return_{years}y")

            if value is not None:
                values.append(value)

        values.sort()

        return values

    def percentile(self, years: int, p: float):

        values = self.distribution(years)

        if not values:
            return None

        index = int((len(values) - 1) * p)

        return values[index]

    def median(self, years: int):

        return self.percentile(years, 0.50)

    def worst_case(self, years: int):

        values = self.distribution(years)

        if not values:
            return None

        return values[0]

    def best_case(self, years: int):

        values = self.distribution(years)

        if not values:
            return None

        return values[-1]