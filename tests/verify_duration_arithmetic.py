#!/usr/bin/env python3
"""
SOP Research Engine
Calendar-month Duration Verification

Regression test for RE-BUG.2.
It verifies that drawdown duration and recovery duration are calculated
with calendar-month arithmetic, not YYYY.MM float subtraction.
"""

from pathlib import Path
from typing import Optional
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from engine.date_utils import months_between, year_month
from engine.drawdown_engine import run_drawdown_engine


EXPECTED_EPISODE_MONTHS = [
    (1872.05, 1877.06, 61, 1880.02, 32),
    (1880.03, 1880.05, 2, 1880.10, 5),
    (1881.06, 1896.08, 182, 1900.12, 52),
    (1902.09, 1903.10, 13, 1905.03, 17),
    (1906.09, 1907.11, 14, 1909.08, 21),
    (1909.12, 1921.08, 140, 1925.01, 41),
    (1929.09, 1932.06, 33, 1954.09, 267),
    (1956.07, 1957.12, 17, 1958.09, 9),
    (1959.07, 1960.10, 15, 1961.02, 4),
    (1961.12, 1962.06, 6, 1963.09, 15),
    (1966.01, 1966.10, 9, 1967.08, 10),
    (1968.12, 1970.06, 18, 1972.03, 21),
    (1973.01, 1974.12, 23, 1980.07, 67),
    (1980.11, 1982.07, 20, 1982.11, 4),
    (1987.08, 1987.12, 4, 1989.07, 19),
    (1990.06, 1990.10, 4, 1991.02, 4),
    (1998.07, 1998.09, 2, 1998.12, 3),
    (2000.08, 2003.02, 30, 2007.05, 51),
    (2007.10, 2009.03, 17, 2013.03, 48),
    (2018.09, 2018.12, 3, 2019.04, 4),
    (2020.01, 2020.03, 2, 2020.08, 5),
    (2021.12, 2022.10, 10, 2023.12, 14),
    (2025.02, 2025.04, 2, 2025.07, 3),
]


def check_equal(label: str, actual, expected) -> Optional[str]:
    if actual != expected:
        return f"{label}: expected {expected}, got {actual}"

    return None


def rounded(value: float | None) -> float | None:
    if value is None:
        return None

    return round(value, 2)


def main() -> None:
    dataset = run_drawdown_engine()

    regressions = [
        check_equal("year_month_2026_10", year_month(2026.10), (2026, 10)),
        check_equal(
            "months_between_1929_1932",
            months_between(1929.09, 1932.06),
            33,
        ),
        check_equal(
            "months_between_same_year",
            months_between(2020.01, 2020.03),
            2,
        ),
        check_equal(
            "months_between_month_decreases",
            months_between(2021.12, 2022.10),
            10,
        ),
        check_equal("episodes", len(dataset.episodes), 23),
    ]

    actual_episode_months = [
        (
            rounded(episode.peak_date),
            rounded(episode.bottom_date),
            episode.duration_months,
            rounded(episode.recovery_date),
            episode.recovery_months,
        )
        for episode in dataset.episodes
    ]

    regressions.append(
        check_equal(
            "episode_months",
            actual_episode_months,
            EXPECTED_EPISODE_MONTHS,
        )
    )

    regressions = [
        regression
        for regression in regressions
        if regression is not None
    ]

    if regressions:
        print("DURATION ARITHMETIC : REGRESSION DETECTED")

        for regression in regressions:
            print(regression)

        raise SystemExit(1)

    print("DURATION ARITHMETIC : STABLE")
    print(f"episodes: {len(dataset.episodes)}")
    print("1929.09_to_1932.06: 33")


if __name__ == "__main__":
    main()
