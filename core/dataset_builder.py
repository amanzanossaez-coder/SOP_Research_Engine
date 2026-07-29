from models.dataset import Dataset
from models.episode import Episode


class DatasetBuilder:
    """
    Convierte un DataFrame en un Dataset del dominio.

    Responsabilidad única:
    transformar datos tabulares en objetos Episode.
    """

    def build(self, dataframe):

        episodes = []

        for _, row in dataframe.iterrows():

            episodes.append(
                Episode(
                    date=row["date"],
                    price=row["price"],
                    cape=row["cape"],
                    dividend_yield=row["dividend_yield"],
                    earnings=row["earnings"],
                    cpi=row["cpi"],
                    gs10=row["gs10"],
                )
            )

        return Dataset(episodes)