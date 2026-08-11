"""
SOP Research Engine
Manual Entry Parsing -- RE-032.7

Shared parsing for the manually-typed cells every operator-facing xlsx
in this project uses (data/raw/dry_powder_ledger.xlsx,
data/raw/human_approval_attestations.xlsx, and by extension any future
one). Extracted from engine/dry_powder_ledger_state.py (no logic
change) so a second adapter (engine/human_approval_state.py) does not
carry its own copy of the same placeholder-token and date-format
handling -- the same anti-duplication discipline this session already
applied to market_crisis (RE-032.6) and the Shiller-month conversion
(RE-041.7 -> engine.live_episode.calendar_date_to_shiller_month()).

PLACEHOLDER_TOKENS matches personal_capacity_facts_gate.py's own
"pendiente" convention (RE-043.1) -- "not filled in yet" reads as
missing/None everywhere in this project, never as a false value.
"""

from datetime import date, datetime
from typing import Optional


PLACEHOLDER_TOKENS = {"pendiente"}


def to_float_or_none(value) -> Optional[float]:

    if value is None:
        return None

    if isinstance(value, str) and value.strip().lower() in PLACEHOLDER_TOKENS:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_calendar_date_or_none(value) -> Optional[date]:

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    if isinstance(value, str):

        text = value.strip()

        if not text or text.lower() in PLACEHOLDER_TOKENS:
            return None

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(text, fmt).date()
            except ValueError:
                continue

    return None
