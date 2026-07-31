#!/usr/bin/env python3
"""
RE-023.2 / RE-023.3 / RE-023.4 -- Validacion de ObservableUniverse.

Verifica:

1. Paridad de campos entre Episode y ObservableEpisode.

2. RE-023.2 -- identidad en ausencia de masking o filtrado: con un
   as_of mas alla de cualquier horizonte real, episodes() debe
   coincidir campo a campo, episodio a episodio, con dataset.episodes.

3. RE-023.3 -- masking temporal: dentro del subconjunto observable
   en un as_of historico, los campos Outcome que todavia no
   existirian deben ser None, por horizonte, sin tocar Event ni
   Context.

4. RE-023.4 -- existencia temporal: episodes() solo debe devolver
   episodios cuyo bottom_date <= as_of. Los posteriores no deben
   aparecer en absoluto, ni siquiera con su Outcome enmascarado.
"""

import dataclasses
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.drawdown_engine import run_drawdown_engine
from engine.observable_universe import ObservableUniverse
from models.episode import Episode
from models.observable_episode import ObservableEpisode


CAUSAL_FIELDS = (
    "peak_index",
    "bottom_index",
    "peak_date",
    "bottom_date",
    "peak_price",
    "bottom_price",
    "drawdown",
    "duration_months",
    "context",
)

OUTCOME_HORIZON_FIELDS = (
    "future_return_1y",
    "future_return_3y",
    "future_return_5y",
    "future_return_10y",
    "probability_positive_1y",
    "probability_positive_3y",
    "probability_positive_5y",
    "probability_positive_10y",
)

RECOVERY_FIELDS = (
    "recovery_index",
    "recovery_date",
    "recovery_months",
)


def check_field_parity() -> bool:

    episode_fields = {f.name for f in dataclasses.fields(Episode)}
    observable_fields = {
        f.name for f in dataclasses.fields(ObservableEpisode)
    }

    missing_in_observable = episode_fields - observable_fields
    missing_in_episode = observable_fields - episode_fields

    ok = True

    if missing_in_observable:
        print(
            "✗ Campos en Episode ausentes en ObservableEpisode: "
            f"{missing_in_observable}"
        )
        ok = False

    if missing_in_episode:
        print(
            "✗ Campos en ObservableEpisode ausentes en Episode: "
            f"{missing_in_episode}"
        )
        ok = False

    if ok:
        print("✓ Paridad de campos Episode <-> ObservableEpisode")

    return ok


def check_identity_without_masking_or_filtering(dataset) -> bool:

    as_of = float(dataset.data["Date"].max()) + 100

    universe = ObservableUniverse(dataset, as_of=as_of)

    observable = universe.episodes()

    ok = True

    if len(observable) != len(dataset.episodes):
        print(
            "✗ Numero de episodios distinto: "
            f"Dataset={len(dataset.episodes)} "
            f"ObservableUniverse={len(observable)}"
        )
        return False

    for original, projected in zip(dataset.episodes, observable):

        if not isinstance(projected, ObservableEpisode):
            print("✗ episodes() no devuelve ObservableEpisode")
            ok = False
            continue

        if isinstance(projected, Episode):
            print(
                "✗ ObservableEpisode no debe ser instancia de "
                "Episode (ADR-004: tipos independientes)"
            )
            ok = False

        for field in dataclasses.fields(Episode):

            name = field.name

            original_value = getattr(original, name)
            projected_value = getattr(projected, name)

            if original_value != projected_value:
                print(
                    f"✗ Episodio peak={original.peak_date}: "
                    f"campo '{name}' difiere sin motivo temporal "
                    f"({original_value!r} != {projected_value!r})"
                )
                ok = False

    if ok:
        print(
            "✓ Sin nada que enmascarar ni filtrar, episodes() sigue "
            "siendo identidad (RE-023.2)"
        )

    return ok


def check_temporal_masking(dataset) -> bool:

    as_of = 1990.0

    universe = ObservableUniverse(dataset, as_of=as_of)

    observable_by_bottom = {
        e.bottom_date: e for e in universe.episodes()
    }

    ok = True

    for original in dataset.episodes:

        if original.bottom_date > as_of:
            continue  # RE-023.4 se valida aparte

        projected = observable_by_bottom.get(original.bottom_date)

        label = f"peak={original.peak_date} bottom={original.bottom_date}"

        if projected is None:
            print(f"✗ {label}: deberia existir en as_of={as_of} y no aparece")
            ok = False
            continue

        # Event / Context nunca se enmascaran.

        for name in CAUSAL_FIELDS:

            original_value = getattr(original, name)
            projected_value = getattr(projected, name)

            if original_value != projected_value:
                print(
                    f"✗ {label}: campo causal '{name}' fue "
                    f"modificado ({original_value!r} != "
                    f"{projected_value!r}) -- Event/Context no "
                    "deben enmascararse nunca"
                )
                ok = False

        # Recovery: observable solo si ya ocurrio y ocurrio <= as_of.

        recovery_should_be_observable = (
            original.recovery_date is not None
            and original.recovery_date <= as_of
        )

        for name in RECOVERY_FIELDS:

            projected_value = getattr(projected, name)

            if recovery_should_be_observable:
                original_value = getattr(original, name)
                if projected_value != original_value:
                    print(
                        f"✗ {label}: '{name}' deberia ser observable "
                        f"en as_of={as_of} y no lo es"
                    )
                    ok = False
            else:
                if projected_value is not None:
                    print(
                        f"✗ {label}: '{name}' deberia estar "
                        f"enmascarado (None) en as_of={as_of}, "
                        f"vale {projected_value!r}"
                    )
                    ok = False

        # Rentabilidades / probabilidades futuras: observable por
        # horizonte, no en bloque.

        for field_name in OUTCOME_HORIZON_FIELDS:

            years = int(field_name.split("_")[-1].rstrip("y"))

            horizon_observable = (
                original.bottom_date + years <= as_of
            )

            projected_value = getattr(projected, field_name)

            if horizon_observable:
                original_value = getattr(original, field_name)
                if projected_value != original_value:
                    print(
                        f"✗ {label}: '{field_name}' deberia ser "
                        f"observable en as_of={as_of} y no lo es"
                    )
                    ok = False
            else:
                if projected_value is not None:
                    print(
                        f"✗ {label}: '{field_name}' deberia estar "
                        f"enmascarado (None) en as_of={as_of}, "
                        f"vale {projected_value!r}"
                    )
                    ok = False

    if ok:
        print(
            "✓ Masking temporal correcto en as_of=1990.0 dentro del "
            "universo observable (por campo/horizonte, "
            "Event/Context intactos)"
        )

    return ok


def check_temporal_existence(dataset) -> bool:

    as_of = 1950.0

    universe = ObservableUniverse(dataset, as_of=as_of)

    observable = universe.episodes()

    expected_bottoms = {
        e.bottom_date for e in dataset.episodes if e.bottom_date <= as_of
    }
    future_bottoms = {
        e.bottom_date for e in dataset.episodes if e.bottom_date > as_of
    }

    observed_bottoms = {e.bottom_date for e in observable}

    ok = True

    if observed_bottoms != expected_bottoms:
        print(
            "✗ RE-023.4: el conjunto de episodios observables en "
            f"as_of={as_of} no coincide con bottom_date <= as_of\n"
            f"  esperado: {sorted(expected_bottoms)}\n"
            f"  obtenido: {sorted(observed_bottoms)}"
        )
        ok = False

    leaked = observed_bottoms & future_bottoms

    if leaked:
        print(
            f"✗ RE-023.4: episodios con bottom_date > as_of={as_of} "
            f"aparecen en episodes(): {sorted(leaked)}"
        )
        ok = False

    if len(dataset.episodes) == len(observable):
        print(
            "✗ RE-023.4: en as_of=1950.0 el numero de episodios "
            "deberia ser menor que el total del Dataset (23) -- "
            f"salio {len(observable)}, el filtro no esta actuando"
        )
        ok = False

    if ok:
        print(
            f"✓ RE-023.4: episodes() en as_of={as_of} devuelve "
            f"exactamente los {len(observable)} episodios con "
            "bottom_date <= as_of, ninguno posterior"
        )

    return ok


def main():

    print("=" * 60)
    print("RE-023.2 / RE-023.3 / RE-023.4 -- VALIDACION")
    print("=" * 60)
    print()

    dataset = run_drawdown_engine()

    checks = [
        check_field_parity(),
        check_identity_without_masking_or_filtering(dataset),
        check_temporal_masking(dataset),
        check_temporal_existence(dataset),
    ]

    print()

    if all(checks):
        print("RESULTADO: OK")
        sys.exit(0)

    print("RESULTADO: FALLO")
    sys.exit(1)


if __name__ == "__main__":
    main()
