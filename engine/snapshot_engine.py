from models.context import Context
from models.snapshot import Snapshot


class SnapshotEngine:

    def __init__(self, dataset):

        self.dataset = dataset

    def _real_return(self, start, end):

        if start <= 0:
            return None

        return (end / start) - 1.0

    def _build_snapshot(self, index) -> Snapshot:

        data = self.dataset.data

        row = data.iloc[index]

        peak_index = (
            data.iloc[: index + 1]["Price.1"]
            .idxmax()
        )

        duration_months = index - peak_index

        pre_crash_return_3y = None

        if peak_index >= 36:

            start_price = data.iloc[
                peak_index - 36
            ]["Price.1"]

            end_price = data.iloc[
                peak_index
            ]["Price.1"]

            pre_crash_return_3y = self._real_return(
                start_price,
                end_price,
            )

        pre_crash_volatility_1y = row["Volatility1Y"]

        context = Context(

            cape=row["CAPE"],

            pre_crash_return_3y=pre_crash_return_3y,

            pre_crash_volatility_1y=pre_crash_volatility_1y,

            inflation=row["InflationRate1Y"],

            # RE-038.1 -- antes hardcoded a None. "Rate GS10" -- mismo
            # criterio y misma columna que drawdown_engine.py::
            # filter_episodes() usa ahora para los episodios historicos,
            # para que ambos lados de la comparacion de Regime
            # Comparability Gate usen la misma fuente.
            interest_rate=row["Rate GS10"],

        )

        return Snapshot(

            index=index,

            date=row["Date"],

            price=row["Price.1"],

            drawdown=row["Drawdown"],

            duration_months=duration_months,

            context=context,

        )

    def at(self, index) -> Snapshot:

        return self._build_snapshot(index)

    def latest(self) -> Snapshot:

        # RE-038.1 -- se retira el print de depuracion "POSIBLES
        # COLUMNAS MACRO" que buscaba a mano la columna de tipo de
        # interes en cada ejecucion. Ya cumplio su proposito: identifico
        # "Rate GS10", ahora conectada explicitamente en _build_snapshot.

        data = self.dataset.data

        return self._build_snapshot(len(data) - 1)