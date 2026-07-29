from dataclasses import dataclass
from statistics import mean
from typing import List

import pandas as pd

from models.episode import Episode


@dataclass
class Dataset:

    data: pd.DataFrame
    episodes: List[Episode]

    # -----------------------------
    # Filtros
    # -----------------------------

    def drawdowns_greater_than(self, threshold: float):

        return [
            e
            for e in self.episodes
            if e.drawdown <= threshold
        ]

    def recovered_in_less_than(self, months: int):

        return [
            e
            for e in self.episodes
            if (
                e.recovery_months is not None
                and e.recovery_months <= months
            )
        ]

    # -----------------------------
    # Estadísticos
    # -----------------------------

    def average_return_1y(self):

        values = [
            e.future_return_1y
            for e in self.episodes
            if e.future_return_1y is not None
        ]

        return mean(values)

    def average_return_3y(self):

        values = [
            e.future_return_3y
            for e in self.episodes
            if e.future_return_3y is not None
        ]

        return mean(values)

    def average_return_5y(self):

        values = [
            e.future_return_5y
            for e in self.episodes
            if e.future_return_5y is not None
        ]

        return mean(values)

    def average_return_10y(self):

        values = [
            e.future_return_10y
            for e in self.episodes
            if e.future_return_10y is not None
        ]

        return mean(values)

    def positive_probability_1y(self):

        values = [
            e.future_return_1y
            for e in self.episodes
            if e.future_return_1y is not None
        ]

        positives = sum(v > 0 for v in values)

        return positives / len(values)

    def positive_probability_3y(self):

        values = [
            e.future_return_3y
            for e in self.episodes
            if e.future_return_3y is not None
        ]

        positives = sum(v > 0 for v in values)

        return positives / len(values)

    def positive_probability_5y(self):

        values = [
            e.future_return_5y
            for e in self.episodes
            if e.future_return_5y is not None
        ]

        positives = sum(v > 0 for v in values)

        return positives / len(values)

    def positive_probability_10y(self):

        values = [
            e.future_return_10y
            for e in self.episodes
            if e.future_return_10y is not None
        ]

        positives = sum(v > 0 for v in values)

        return positives / len(values)