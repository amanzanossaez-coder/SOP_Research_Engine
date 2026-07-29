from models.context import Context
from models.dataset import Dataset
from models.episode import Episode

from loaders.shiller_loader import load_shiller_data


MIN_DRAWDOWN = -0.10


def calculate_running_peak(df):

    df["RunningPeak"] = df["P"].cummax()

    return df


def calculate_drawdown(df):

    df["Drawdown"] = (df["P"] - df["RunningPeak"]) / df["RunningPeak"]

    return df


def calculate_volatility(df):

    df["Return"] = df["Price.1"].pct_change()

    df["Volatility1Y"] = (
        df["Return"]
        .rolling(12)
        .std()
        * (12 ** 0.5)
    )

    return df


def detect_drawdowns(df):

    drawdowns = []

    in_drawdown = False

    peak = None
    peak_before = None

    peak_index = None
    peak_before_index = None

    bottom = None
    bottom_index = None

    for i, row in df.iterrows():

        if row["Drawdown"] == 0:

            peak = row
            peak_index = i

            if in_drawdown:

                drawdowns.append(
                    {
                        "peak": peak_before,
                        "peak_index": peak_before_index,
                        "bottom": bottom,
                        "bottom_index": bottom_index,
                        "recovery": row,
                        "recovery_index": i,
                    }
                )

                in_drawdown = False

        elif row["Drawdown"] <= MIN_DRAWDOWN:

            if not in_drawdown:

                peak_before = peak
                peak_before_index = peak_index

                bottom = row
                bottom_index = i

                in_drawdown = True

            elif row["Drawdown"] < bottom["Drawdown"]:

                bottom = row
                bottom_index = i

    return drawdowns


def _real_return(df, start_date, end_date):

    start = df[df["Date"] <= start_date]

    end = df[df["Date"] >= end_date]

    if len(start) == 0 or len(end) == 0:
        return None

    start = start.iloc[-1]
    end = end.iloc[0]

    return (end["Price.1"] - start["Price.1"]) / start["Price.1"]


def filter_episodes(drawdowns, df):

    episodes = []

    for d in drawdowns:

        duration_months = int(
            round(
                (d["bottom"]["Date"] - d["peak"]["Date"]) * 12
            )
        )

        pre_crash_return_3y = _real_return(
            df,
            d["peak"]["Date"] - 3,
            d["peak"]["Date"],
        )

        episodes.append(

            Episode(

                peak_index=d["peak_index"],
                bottom_index=d["bottom_index"],

                peak_date=d["peak"]["Date"],
                bottom_date=d["bottom"]["Date"],

                peak_price=d["peak"]["P"],
                bottom_price=d["bottom"]["P"],

                drawdown=d["bottom"]["Drawdown"],

                recovery_index=d["recovery_index"],

                duration_months=duration_months,

                context=Context(

                    cape=d["bottom"]["CAPE"],

                    pre_crash_return_3y=pre_crash_return_3y,

                    pre_crash_volatility_1y=d["bottom"]["Volatility1Y"],

                    inflation=None,

                    interest_rate=None,

                ),

            )

        )

    return episodes


def enrich_recovery(df, episodes):

    for episode in episodes:

        recovery = df[
            (df["Date"] > episode.bottom_date)
            & (df["P"] >= episode.peak_price)
        ]

        if len(recovery) == 0:
            continue

        first = recovery.iloc[0]

        episode.recovery_date = first["Date"]

        episode.recovery_months = int(
            round(
                (first["Date"] - episode.bottom_date) * 12
            )
        )

        recovery_rows = df[df["Date"] == first["Date"]]

        if len(recovery_rows) > 0:
            episode.recovery_index = recovery_rows.index[0]

    return episodes


def _future_return(df, bottom_date, years):
    # RE-001: CAGR real anualizado. No retorno acumulado.
    future_date = bottom_date + years
    future = df[df["Date"] >= future_date]
    if len(future) == 0:
        return None
    future_row = future.iloc[0]
    bottom_rows = df[df["Date"] >= bottom_date]
    if len(bottom_rows) == 0:
        return None
    p0 = bottom_rows.iloc[0]["Price.1"]
    p1 = future_row["Price.1"]
    if p0 is None or p0 == 0:
        return None
    return (p1 / p0) ** (1 / years) - 1


def enrich_future_returns(df, episodes):

    for episode in episodes:

        episode.future_return_1y = _future_return(
            df,
            episode.bottom_date,
            1,
        )

        episode.future_return_3y = _future_return(
            df,
            episode.bottom_date,
            3,
        )

        episode.future_return_5y = _future_return(
            df,
            episode.bottom_date,
            5,
        )

        episode.future_return_10y = _future_return(
            df,
            episode.bottom_date,
            10,
        )

    return episodes


def run_drawdown_engine():

    df = load_shiller_data()

    if df is None:
        return None

    df = calculate_running_peak(df)

    df = calculate_drawdown(df)

    df = calculate_volatility(df)

    drawdowns = detect_drawdowns(df)

    episodes = filter_episodes(drawdowns, df)

    episodes = enrich_recovery(df, episodes)

    episodes = enrich_future_returns(df, episodes)

    return Dataset(
        data=df,
        episodes=episodes,
    )