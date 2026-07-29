from models.context import Context
from models.snapshot import Snapshot


class SnapshotEngine:

    def __init__(self, dataset):

        self.dataset = dataset

    def _real_return(self, start, end):

        if start <= 0:
            return None

        return (end / start) - 1.0

    def latest(self) -> Snapshot:

        data = self.dataset.data

        print("\n========== POSIBLES COLUMNAS MACRO ==========\n")

        for column in data.columns:

            name = str(column).upper()

            if (
                "CPI" in name
                or "RATE" in name
                or "GS" in name
                or "YIELD" in name
                or "INTEREST" in name
            ):
                print(column)

        print("\n=============================================\n")

        current_index = len(data) - 1

        row = data.iloc[current_index]

        peak_index = (
            data.iloc[: current_index + 1]["Price.1"]
            .idxmax()
        )

        duration_months = current_index - peak_index

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

            inflation=row["CPI"],

            interest_rate=None,

        )

        return Snapshot(

            index=current_index,

            date=row["Date"],

            price=row["Price.1"],

            drawdown=row["Drawdown"],

            duration_months=duration_months,

            context=context,

        )