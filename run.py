from engine.drawdown_engine import run_drawdown_engine
from engine.decision_engine import DecisionEngine
import engine.snapshot_engine


print("RUN.PY")
print("SnapshotEngine cargado desde:")
print(engine.snapshot_engine.__file__)
print()


def fmt(x):

    if x is None:
        return "---"

    return f"{x:.2%}"


def main():

    dataset = run_drawdown_engine()

    decision = DecisionEngine(dataset)

    print("=" * 70)
    print("SOP RESEARCH ENGINE")
    print("=" * 70)
    print()

    print("DECISION ENGINE")
    print("-" * 70)

    print(f"Posición mercado    : {decision.market_position()}")
    print(f"Valoración          : {decision.valuation_zone()}")
    print(f"Régimen volatilidad : {decision.volatility_regime()}")
    print(f"Retorno esperado 5Y : {fmt(decision.expected_return())}  ← CAGR real anualizado")
    print(f"Potencial máximo    : {fmt(decision.upside())}")
    print(f"Peor caso histórico : {fmt(decision.downside())}")
    print(f"Confianza           : {decision.confidence()}")

    print()

    print("DEBUG SPEED")
    print("-" * 70)

    snapshot = decision.snapshot

    snapshot_speed = None

    if (
        snapshot.duration_months is not None
        and snapshot.duration_months > 0
    ):
        snapshot_speed = (
            abs(snapshot.drawdown)
            / snapshot.duration_months
        )

    print(f"Snapshot drawdown : {snapshot.drawdown:.2%}")
    print(f"Snapshot duration : {snapshot.duration_months}")
    print(f"Snapshot speed    : {snapshot_speed}")

    print()

    print("TOP EPISODIOS SIMILARES")
    print("-" * 70)

    similares = decision.historical_matches()

    for s in similares:

        print(
            f"{s.score:6.1%}"
            f" | {s.episode.peak_date:.2f}"
            f" -> "
            f"{s.episode.bottom_date:.2f}"
            f" | {s.episode.drawdown:.2%}"
        )

        for explanation in (
            s.event,
            s.context,
            s.outcome,
        ):

            print(
                f"    {explanation.title}"
                f" ({explanation.score:.1%})"
            )

            for item in explanation.items:

                score = (
                    "---"
                    if item.score is None
                    else f"{item.score:.1%}"
                )

                print(
                    f"      "
                    f"{item.name:<15}"
                    f"{score:>8}"
                )

            print()

    print("=" * 70)
    print("SIMILARITY DIAGNOSTICS")
    print("=" * 70)

    n = len(similares)

    if n > 0:

        def avg(attribute):

            values = [
                getattr(s, attribute)
                for s in similares
                if getattr(s, attribute) is not None
            ]

            if not values:
                return None

            return sum(values) / len(values)

        diagnostics = [
            ("Drawdown", avg("drawdown_score")),
            ("Duration", avg("duration_score")),
            ("Speed", avg("speed_score")),
            ("CAPE", avg("cape_score")),
            ("Trend 3Y", avg("pre_crash_return_3y_score")),
            ("Volatility", avg("volatility_score")),
            ("Recovery", avg("recovery_score")),
        ]

        print()

        for name, value in diagnostics:

            text = (
                "N/A"
                if value is None
                else f"{value:.1%}"
            )

            print(
                f"{name:<15}"
                f"{text:>8}"
            )


if __name__ == "__main__":

    main()