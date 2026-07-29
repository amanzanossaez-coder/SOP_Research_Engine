from bisect import bisect_left


class PercentileNormalizer:
    """
    Convierte un valor en su posición relativa (percentil)
    dentro de una distribución histórica.
    """

    def __init__(self, values):

        self.values = sorted(

            float(v)

            for v in values

            if v is not None

        )

    def percentile(self, value):

        if (
            value is None
            or len(self.values) == 0
        ):
            return None

        position = bisect_left(

            self.values,
            float(value),

        )

        return position / len(self.values)