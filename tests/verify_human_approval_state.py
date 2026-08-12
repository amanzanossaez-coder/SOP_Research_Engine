#!/usr/bin/env python3
"""
SOP Research Engine
Human Approval State Verification

RE-032.7 -- synthetic checks on _build_patrimonio_attestations() (row
parsing, market_crisis_at_registration lookup), plus a real-pipeline
check on build_local_human_approval_inputs() against the actual
data/raw/human_approval_attestations.xlsx (empty today).
"""

from pathlib import Path
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from engine.gate_combination import DEPLOY_AGGRESSIVELY, DEPLOY_PARTIALLY, CONSERVE
from engine.human_approval import HumanApprovalGate, MISSING
from engine.human_approval_state import (
    _build_patrimonio_attestations,
    build_local_human_approval_inputs,
)
from loaders.human_approval_loader import load_human_approval_raw


def assert_equal(label: str, actual, expected) -> None:

    if actual != expected:
        raise AssertionError(
            f"{label}: expected {expected!r}, got {actual!r}"
        )


def main() -> None:

    # -- Synthetic Shiller series: 2026.06 in crisis (-15%, below --
    # -- MIN_DRAWDOWN -10%), 2026.07 not (-3%) --

    shiller_df = pd.DataFrame(
        {"Date": [2026.01, 2026.06, 2026.07], "Drawdown": [0.0, -0.15, -0.03]}
    )

    events = [
        {
            "fecha": "2026-06-15",
            "postura": DEPLOY_AGGRESSIVELY,
            "crisis_personal": "Sí",
            "nota": "durante la caída",
            "autoriza_techo_90": "Sí",
        },
        {
            "fecha": "2026-07-20",
            "postura": DEPLOY_PARTIALLY,
            "crisis_personal": "No",
            "nota": "mercado ya recuperado",
            "autoriza_techo_90": "No",
        },
        {
            "fecha": "fecha invalida",
            "postura": DEPLOY_PARTIALLY,
            "crisis_personal": "No",
            "nota": "fila corrupta, fecha",
            "autoriza_techo_90": "No",
        },
        {
            "fecha": "2026-05-01",
            "postura": "Not A Real Posture",
            "crisis_personal": "No",
            "nota": "fila corrupta, postura",
            "autoriza_techo_90": "No",
        },
        {
            "fecha": "2026-08-01",
            "postura": DEPLOY_PARTIALLY,
            "crisis_personal": "No",
            "nota": "flag marcado pero postura no es Deploy Aggressively -- pasa igual, sin efecto (RE-032.10 point 2 lo decide human_approval.py, no aquí)",
            "autoriza_techo_90": "Sí",
        },
    ]

    attestations, explanations = _build_patrimonio_attestations(events, shiller_df)

    assert_equal("attestations_count", len(attestations), 3)
    assert_equal("explanations_count", len(explanations), 2)

    first, second, third = attestations

    assert_equal("first_posture", first.approved_posture_ceiling, DEPLOY_AGGRESSIVELY)
    assert_equal("first_personal_crisis", first.personal_crisis_declared, True)
    assert_equal(
        "first_market_crisis_at_registration",
        first.market_crisis_at_registration,
        True,
    )
    assert_equal(
        "first_authorizes_ceiling_90", first.authorizes_dry_powder_ceiling_90, True
    )

    assert_equal("second_posture", second.approved_posture_ceiling, DEPLOY_PARTIALLY)
    assert_equal("second_personal_crisis", second.personal_crisis_declared, False)
    assert_equal(
        "second_market_crisis_at_registration",
        second.market_crisis_at_registration,
        False,
    )
    assert_equal(
        "second_authorizes_ceiling_90", second.authorizes_dry_powder_ceiling_90, False
    )

    # -- Flag marked Sí on a row whose posture is NOT Deploy --
    # -- Aggressively: passed through raw, unconditionally -- whether --
    # -- it does anything is human_approval.py's decision, not this --
    # -- adapter's (RE-B design note) --

    assert_equal("third_posture", third.approved_posture_ceiling, DEPLOY_PARTIALLY)
    assert_equal(
        "third_authorizes_ceiling_90", third.authorizes_dry_powder_ceiling_90, True
    )

    # -- No Shiller series supplied -- market_crisis_at_registration --
    # -- defaults to False, never guessed True --

    attestations_no_df, _ = _build_patrimonio_attestations(
        events[:1], shiller_df=None
    )
    assert_equal(
        "no_shiller_df_market_crisis",
        attestations_no_df[0].market_crisis_at_registration,
        False,
    )

    # -- Loader: real file, both patrimonio tabs present, empty today --

    raw = load_human_approval_raw()
    assert raw is not None, "real ledger file should load"
    assert_equal("raw_patrimonios", set(raw.keys()), {"AMS", "AML"})
    for name, rows in raw.items():
        assert_equal(f"raw_{name}_empty", rows, [])

    # -- Full real pipeline: MISSING for both, since no attestation --
    # -- has ever been registered --

    real_inputs = build_local_human_approval_inputs()
    assert real_inputs is not None
    assert_equal("real_inputs_patrimonios", set(real_inputs.keys()), {"AMS", "AML"})

    gate = HumanApprovalGate()
    for name, inputs in real_inputs.items():
        result = gate.evaluate(inputs)
        assert_equal(f"real_{name}_state", result.state, MISSING)
        assert_equal(f"real_{name}_blocked", result.blocked, True)

    print("HUMAN APPROVAL STATE : STABLE")


if __name__ == "__main__":
    main()
