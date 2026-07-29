from core.normalization import PercentileNormalizer


class SimilarityMetric:
    """
    Contrato base para todas las métricas de similitud.
    """

    def compare(self, a, b):

        raise NotImplementedError


class LinearMetric(SimilarityMetric):
    """
    Similitud basada en distancia lineal.
    """

    def __init__(self, scale):

        self.scale = scale

    def compare(self, a, b):

        if a is None or b is None:
            return None

        score = 1.0 - abs(a - b) / self.scale

        return max(0.0, score)


class PercentileMetric(SimilarityMetric):
    """
    Similitud basada en percentiles históricos.
    """

    def __init__(self, historical_values):

        self.normalizer = PercentileNormalizer(
            historical_values
        )

        self.linear = LinearMetric(
            scale=1.0
        )

    def compare(self, a, b):

        a_percentile = self.normalizer.percentile(
            a
        )

        b_percentile = self.normalizer.percentile(
            b
        )

        return self.linear.compare(
            a_percentile,
            b_percentile,
        )