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

                print(
                    f"      "
                    f"{item.name:<15}"
                    f"{item.score:.1%}"
                )

            print()


if __name__ == "__main__":

    main()