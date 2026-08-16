"""
SOP -- Panorama histórico (Shiller)
RE-SHILLER-DASH.1 -- first version, agreed with Armando before writing
any code (2026-08-16): "construyamos un dashboard parecido con la
informacion de shiller, con graficas e info relevante."

RE-SHILLER-DASH.2 (same day) -- Armando's structured review of v1:
"lo veo mas como un cuaderno de graficas historicas que como un
dashboard ejecutivo... le falta una capa superior de lectura." Six
concrete changes, all implemented here: an executive-reading sentence
at the top, an indicator strip before the charts, CAPE percentile,
CAPE 10-year mean, an accurate price-series label (see the real
nominal-vs-real finding below), and a "qué NO dice este panel" block.
Page reordered to his proposed structure: resumen ejecutivo -> franja
de indicadores -> precio -> CAPE -> inflación -> tipos -> nota
metodológica.

RE-SHILLER-DASH.3 (same day) -- two more rounds of feedback: (1)
"diseño tipo bain/mckinsey sobre todo en Indicadores clave y resumen
ejecutivo... mira a ver lo de semaforos"; (2) "añadir fecha y valor de
la ultima cifra de referencia para ubicarnos en las graficas". Traffic-
light dots added, but deliberately on a different color axis than the
operational dashboard's -- see _reading_magnitude_color()'s docstring
for why a "muy por encima" CAPE reading is not colored the same way as
a "por debajo del suelo" liquidity reading, even though both end up
red. Each chart now has the last data point's date+value annotated
directly on the image (not only in the caption text below it), per
Armando's "ubicarnos en las gráficas".

RE-SHILLER-DASH.4 (same day) -- Armando, blunt and correct: "de verdad
esto te parece bain o mckinsey? El resumen ejecutivo en lineas con
texto seguido, las cifras cada una por su lado, una con dos decimales,
otras con uno... que poco detalle." Two real defects, not taste: (1)
"Resumen ejecutivo" was one long run-on sentence stringing four clauses
together with commas -- not a headline, a paragraph. Replaced with the
operational dashboard's own proven headline-action/headline-sub split
(short bold title + lighter supporting line), the same pattern Armando
already approved for "Estado hoy" in RE-DASH.1.11 -- reused, not
reinvented. (2) The indicator table mixed 1-decimal (_fmt_pct's
default, used for inflación) and 2-decimal (_fmt_rate's default, used
for tipo) formatting in adjacent rows of the same table -- standardized
to 2 decimals for both percentage rows. This exact mismatch (inflación
1dp, tipo 2dp) already existed in outputs/dashboard.html's own "Datos
de mercado" table before this iteration -- flagged to Armando, not
silently fixed there too (a different file, his call whether to touch
it). Also added a stat-strip (same .stat-strip/.stat-value/.stat-label
pattern RE-DASH.1.11 already established for "Evidencia histórica") as
the primary at-a-glance visual, replacing scattered numbers with four
grouped, dot-coded callout figures.

Generates outputs/shiller_dashboard.html: static charts (matplotlib ->
PNG, embedded inline, no <script> anywhere) over the full Robert
Shiller dataset (1871-2026) exactly as run_drawdown_engine() already
loads and computes it -- same data, same columns, nothing recalculated
independently of the Research Engine.

Purpose, deliberately distinct from outputs/dashboard.html: that one
answers "what should happen today" (decision-support snapshot). This
one is historical/diagnostic -- lets Armando see the whole shape of
the data the engine reasons over, including where it detects each
historical drawdown episode, so the engine's logic is inspectable on a
chart, not just trusted from a table of numbers. Same "evidencia
explicable, no caja negra" principle the whole project already
follows, one level deeper.

Two architecture choices Armando made explicitly, not inferred:
-   Static images (matplotlib -> PNG), not an interactive JS charting
    library -- keeps the zero-<script>, read-only rule
    outputs/dashboard.html has followed since RE-DASH.1.4.
-   A separate file/output, not a new section bolted onto the existing
    operational dashboard -- different audience/purpose, doesn't
    compete for space or density with the decision-support view.

Real finding from RE-SHILLER-DASH.2, not a design choice: the "P"
column drawdown_engine.py uses for episode detection is the raw
NOMINAL S&P index (confirmed against the Shiller workbook's own header
rows -- "S&P Comp."), not inflation-adjusted. "Price" is the real
(inflation-adjusted, no dividends) series. Switched this dashboard's
price chart from "P" to "Price" -- a nominal price line over 155 years
is dominated by cumulative inflation and would misrepresent the
picture for a reader. This does NOT touch drawdown_engine.py or
episode detection -- peak/bottom/recovery dates and % drawdown
magnitudes are unchanged, computed exactly as before on nominal price;
only the line plotted underneath the same shaded episodes changed.

RE-SHILLER-DASH.5 (same day) -- Armando's review of v2: "ya no es solo
un conjunto de gráficas... como v1 está bien. Añadiría poca cosa, pero
hay tres piezas que sí me parecen relevantes." Of the three, he scoped
the iteration himself to two: "Para RE-DASH.2.1 [sic -- this file's own
track is RE-SHILLER-DASH, kept as such below] añadiría solo dos
bloques: 1. Retornos posteriores según CAPE inicial. 2. Resumen de
drawdowns históricos." The third (percentiles for inflación/tipo,
alongside CAPE's existing one) is deliberately deferred, his own call,
not dropped by omission.

-   **Retornos reales posteriores según CAPE inicial** (new section,
    after the CAPE chart): for every month with a valid CAPE reading,
    the real total-return CAGR (dividends reinvested -- same "Price.1"
    basis and same nearest-date/CAGR formula drawdown_engine.py's own
    future_return_* fields already use, just computed for every month
    instead of only episode bottoms) at 5/10/15 years forward, then
    grouped into buckets (todos los meses, CAPE>30/35/40) and reduced
    to the median. Armando's own caveat kept verbatim ("muestra
    descriptiva, no señal operativa... periodos pocos y no
    independientes"), plus a concrete disclosure his caveat implies but
    doesn't spell out: verified by direct inspection that the CAPE>40
    bucket (21 months with 15y-forward data) is almost entirely one
    historical cluster (1999-2000), and CAPE>35 combines two distinct
    periods (1998-2001, 2021-2026) -- not dozens of independent trials,
    a fact worth stating plainly rather than leaving to a generic
    caveat sentence.
-   **Resumen de drawdowns históricos** (new section, after the price
    chart): median/worst drawdown, median peak->bottom duration, median
    bottom->recovery duration, computed directly from the 23 Episode
    objects run_drawdown_engine() already detected -- no new detection
    logic, purely an aggregate reduction of data already shown
    (shaded) on the price chart above it.
-   **Wording fix, "Detalle de indicadores"**: Armando: "inflación
    aparece como 'Cerca de la media', pero 4,23% vs 2,31% puede
    chirriar visualmente." The z-score classification itself is
    correct and NOT changed here (inflación's std is 5.76pp -- a
    century including hyperinflation/deflation makes the "near" band
    genuinely wide; Z_THRESHOLD_NEAR is Armando-confirmed and shared
    with the operational dashboard, out of scope to touch for a
    wording complaint about one row in one table). New
    `_readable_lectura()` is additive, local to this file's "Lectura"
    column only: when the band is "Cerca de la media" but the raw
    value sits above/below the raw mean, it says so explicitly
    ("Por encima de la media, dentro del rango histórico habitual")
    instead of just "Cerca". Same fix applied consistently to all three
    z-scored rows (CAPE, Inflación, Tipo), not only inflación, so the
    table doesn't end up applying two different reading rules to
    dimensions in the same "near" band.

RE-SHILLER-DASH.6 (same day) -- two more points from Armando: "yo aquí,
aparte de la media, introduciría los dos o tres peores episodios de
drawdowns que tienen nombre y apellidos"; "NO entiendo las cifras de la
tabla de CAPE."

-   **Peores episodios con nombre**: new small table inside "Resumen de
    drawdowns históricos" naming the top 3 by magnitude -- 1929
    (Gran Depresión), 2007-2009 (crisis financiera global), both named
    with high confidence, real, well-documented events. The third
    (1872-1877, -47.3%) is flagged, not asserted with the same
    confidence: the engine's detected peak (mayo 1872) precedes the
    conventionally-dated Pánico de 1873 by over a year, and naming
    conventions for that era are less standardized -- said explicitly
    in the table rather than presenting a possibly-wrong label as fact.
-   **CAPE returns table was genuinely unclear, not just unfamiliar**:
    Armando's "no entiendo" pointed at a real gap, not a training
    problem -- the table led with jargon ("CAGR", "anualizado") before
    saying what the numbers mean in plain terms, and never explained
    why 15-year returns are positive when 5/10-year are negative (which
    looks like a contradiction until you know it's mean reversion, not
    stated anywhere). Fixed: a new plain-language paragraph now leads
    the section, translating the CAPE>40 row concretely (annualized
    -4,5%/-3,4%/+2,1% compounds to roughly -21%/-29%/+37% cumulative
    over 5/10/15 years, all below the "todos los meses" baseline of
    7,2%/6,6%/6,7%) before the technical methodology note. Table
    headers also reworded ("5 años" -> unambiguous, "anualizado" stated
    once in the lead paragraph instead of buried in a note underneath).

Read-only, single command, no server:

    python3 generate_shiller_dashboard.py
"""

import base64
import io
import statistics
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from engine.drawdown_engine import run_drawdown_engine
from generate_dashboard import (
    _context_words,
    _esc,
    _fmt_amount,
    _fmt_num,
    _fmt_pct,
    _fmt_rate,
    _fmt_shiller_date,
    _zscore,
    drawdown_context,
)


OUTPUT_PATH = Path("outputs/shiller_dashboard.html")

# 10-year window for CAPE's "no solo comparas contra un mundo antiguo"
# reference (Armando's request) -- distinct from RECENT_WINDOW_YEARS=50
# in generate_dashboard.py, which is a different, already-established
# reference window for a different purpose. Not reused/renamed to avoid
# implying the two dashboards must share one window definition.
CAPE_RECENT_YEARS = 10

# RE-SHILLER-DASH.4 -- grammatically fitted, mid-sentence forms for the
# headline, same pattern as REGIME_DIMENSION_ES in generate_dashboard.py
# (article included, fitted for "con {label} ..."), not reused directly
# since that dict's third key is "interest_rate" not "rate" -- same
# spirit, distinct dict, not a copy-paste that could silently drift if
# generate_dashboard.py's dict changes for its own reasons.
DRIVER_LABEL_ES = {
    "cape": "el CAPE",
    "inflation": "la inflación",
    "rate": "el tipo de interés a 10 años",
}

# RE-SHILLER-DASH.5 -- CAPE buckets for the forward-returns table,
# Armando's own spec ("Todos los meses", ">30", ">35", ">40").
# threshold=None means no filter (all months with a valid CAPE).
CAPE_RETURN_BUCKETS = [
    (None, "Todos los meses"),
    (30, "CAPE > 30"),
    (35, "CAPE > 35"),
    (40, "CAPE > 40"),
]

# 5/10/15 years forward, per Armando's table header. Distinct from
# drawdown_engine.py's Episode.future_return_1y/3y/5y/10y (no 15y
# there, and those are only computed at episode bottoms, not every
# month) -- this file needs a wider horizon and a wider population,
# computed locally, not by extending the Frozen Core's Episode model
# for a presentation-layer table.
FORWARD_RETURN_YEARS = (5, 10, 15)

# RE-SHILLER-DASH.6 -- Armando: "los dos o tres peores episodios de
# drawdowns que tienen nombre y apellidos". Keyed by peak_date (the
# Episode field, matches exactly since these names were assigned by
# looking up the real top-3-by-magnitude episodes from a live run, not
# guessed independently). Two are named with high confidence -- 1929
# and 2007-2009 are about as well-documented as market history gets.
# The third carries an explicit hedge in its own name string rather
# than a separate footnote: the engine's detected peak (1872.05)
# precedes the conventionally-cited Pánico de 1873 by over a year, and
# 19th-century naming conventions are less standardized -- said inline
# so the table itself doesn't overclaim.
NOTABLE_DRAWDOWN_NAMES = {
    1929.09: "Gran Depresión (Crac de 1929)",
    2007.10: "Crisis financiera global (2008)",
    1872.05: "Depresión de la década de 1870 (posible Pánico de 1873 -- fecha de pico no coincide con exactitud, sin confirmar)",
}
N_NOTABLE_DRAWDOWNS = 3

# Same color language as outputs/dashboard.html (.dot.ok/.warn/.bad,
# .pill.ok/.warn/.bad) -- reused here so a reader who has seen one
# dashboard recognizes the other, not a second independent palette.
COLOR_LINE = "#333333"
COLOR_GRID = "#e6e6e2"
COLOR_SPINE = "#cccccc"
COLOR_DRAWDOWN = "#c23b3b"   # same red as .dot.bad -- caída
COLOR_RECOVERY = "#96650f"  # same ochre as .dot.warn -- recuperación
COLOR_MEAN = "#999999"
COLOR_TODAY = "#1a1a1a"


def _reading_magnitude_color(short_label: str) -> str:
    """
    RE-SHILLER-DASH.3 -- Armando asked for semáforos on the z-score
    readings. Deliberately NOT the operational dashboard's ok/warn/bad
    (a value judgment -- "por debajo del suelo" IS bad, structurally).
    A "muy por encima" CAPE reading isn't good or bad by itself --
    context_bar()'s own docstring in generate_dashboard.py says this
    explicitly: "Track is purely positional, no color judgment... that
    stays in Por qué no se actúa". So this semaphore encodes DISTANCE
    FROM HISTORICAL NORM, not sentiment: near=neutral gray,
    notable=ochre, extreme=red -- same hex values as .dot.neutral/
    warn/bad for visual family consistency with the operational
    dashboard, different CSS class names (.mag-dot) so the two
    meanings can't be confused by name.
    """
    if short_label == "Cerca de la media":
        return "near"
    if short_label in ("Por encima", "Por debajo"):
        return "notable"
    return "extreme"


def drawdown_dot_color(drawdown) -> str:
    """
    RE-SHILLER-DASH.3 -- unlike the three z-score readings, "hay una
    caída activa hoy" is a genuine status, not a magnitude -- same
    ok/warn distinction build_porque_rows()'s shared_rows already uses
    in generate_dashboard.py ("Activa" -> warn, "No activa" -> ok),
    reused here rather than forced onto the near/notable/extreme scale
    that doesn't fit a binary state.
    """
    if drawdown is not None and drawdown == 0.0:
        return "ok"
    return "warn"


def _annotate_latest(ax, x, y, label) -> None:
    """
    RE-SHILLER-DASH.3 -- Armando: "añadir fecha y valor de la última
    cifra de referencia para ubicarnos en las gráficas". The caption
    text below each chart already had "Hoy: X", but not the exact date,
    and it wasn't visible while looking at the chart itself -- this
    puts both directly next to the point on the image.
    """
    ax.annotate(
        label,
        xy=(x, y),
        xytext=(-8, 8),
        textcoords="offset points",
        fontsize=7.6,
        color=COLOR_TODAY,
        ha="right",
        va="bottom",
        fontfamily="DejaVu Sans",
        bbox=dict(boxstyle="round,pad=0.28", facecolor="white", edgecolor="#dddddd", linewidth=0.6, alpha=0.92),
        zorder=5,
    )


def _fig_to_data_uri(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


# RE-SHILLER-DASH.4 -- verified before assuming: matplotlib's default
# y-axis tick labels for the linear-scale charts (CAPE/inflación/tipo)
# render with a period ("2.5", "5.0"), not the Spanish comma every
# other number in both dashboards uses. Confirmed by rendering the real
# Rate GS10 chart before writing this fix, not guessed. Applied only to
# chart_series()'s linear axes -- NOT chart_price()'s log-scale axis,
# whose default power-of-ten labels ("10³") have no decimal point to
# convert and would lose their clean form under a plain numeric
# formatter.
def _es_tick_formatter(x, _pos):
    return f"{x:g}".replace(".", ",")


def _style_axes(ax) -> None:
    ax.grid(True, color=COLOR_GRID, linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLOR_SPINE)
    ax.spines["bottom"].set_color(COLOR_SPINE)
    ax.tick_params(colors="#666666", labelsize=8.5)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontfamily("DejaVu Sans")


def _shade_episodes(ax, episodes) -> None:
    """
    Shades each historical episode run_drawdown_engine() already
    detected -- peak-to-bottom in red (drawdown phase), bottom-to-
    recovery in ochre (recovery phase, only when recovery_date is
    known -- fail-closed, no shading drawn from a guessed endpoint).
    Not a second detector: the exact same Episode objects the Research
    Engine matches against.
    """
    for ep in episodes:
        ax.axvspan(ep.peak_date, ep.bottom_date, color=COLOR_DRAWDOWN, alpha=0.12, linewidth=0, zorder=1)
        if ep.recovery_date is not None:
            ax.axvspan(ep.bottom_date, ep.recovery_date, color=COLOR_RECOVERY, alpha=0.08, linewidth=0, zorder=1)


def chart_price(df, episodes, latest_label: str) -> str:
    """
    RE-SHILLER-DASH.2 -- plots "Price" (real, inflation-adjusted, no
    dividends), not "P" (raw nominal) as v1 mistakenly labeled and
    used. See module docstring for the verification behind this.
    """
    fig, ax = plt.subplots(figsize=(9.2, 3.3))
    _shade_episodes(ax, episodes)
    ax.plot(df["Date"], df["Price"], color=COLOR_LINE, linewidth=1.1, zorder=3)
    ax.set_yscale("log")
    latest = df.iloc[-1]
    ax.scatter([latest["Date"]], [latest["Price"]], color=COLOR_TODAY, s=22, zorder=4)
    _annotate_latest(ax, latest["Date"], latest["Price"], latest_label)
    ax.set_ylabel("Precio real, sin dividendos (escala log)", fontsize=8.5, color="#666666")
    _style_axes(ax)
    return _fig_to_data_uri(fig)


def chart_series(df, episodes, column, ylabel, latest_label: str, as_pct=False) -> str:
    fig, ax = plt.subplots(figsize=(9.2, 2.6))
    _shade_episodes(ax, episodes)
    series = df[column] * 100 if as_pct else df[column]
    ax.plot(df["Date"], series, color=COLOR_LINE, linewidth=1.0, zorder=3)
    mean_value = series.mean()
    ax.axhline(mean_value, color=COLOR_MEAN, linewidth=0.9, linestyle="--", zorder=2)
    latest = df.iloc[-1]
    latest_value = latest[column] * 100 if as_pct else latest[column]
    ax.scatter([latest["Date"]], [latest_value], color=COLOR_TODAY, s=20, zorder=4)
    _annotate_latest(ax, latest["Date"], latest_value, latest_label)
    ax.set_ylabel(ylabel, fontsize=8.5, color="#666666")
    _style_axes(ax)
    ax.yaxis.set_major_formatter(FuncFormatter(_es_tick_formatter))
    return _fig_to_data_uri(fig)


def _forward_real_total_return(df, start_date, years):
    """
    RE-SHILLER-DASH.5 -- mirrors drawdown_engine.py's own private
    _future_return() exactly: same "Price.1" basis (real, inflation-
    adjusted, dividends reinvested), same "nearest available date >=
    target" boundary handling, same CAGR formula. The only difference
    is this is callable for ANY month in the series, not only episode
    bottoms -- drawdown_engine.py's future_return_* fields only exist
    at the 23 detected bottoms. Presentation-layer only: does not
    import from or modify drawdown_engine.py, does not touch episode
    detection or the Research Engine's own future_return_* fields.

    Uses Price.1 (dividends reinvested), not "Price" (the series
    plotted in the price chart above, no dividends) -- total real
    return is the standard, and already-established-in-this-codebase,
    definition for "what did this investment actually return", so this
    reuses that definition rather than inventing a second one.
    """
    future_date = start_date + years
    future_rows = df[df["Date"] >= future_date]
    if len(future_rows) == 0:
        return None
    start_rows = df[df["Date"] >= start_date]
    if len(start_rows) == 0:
        return None
    p0 = start_rows.iloc[0]["Price.1"]
    p1 = future_rows.iloc[0]["Price.1"]
    if p0 is None or p0 == 0:
        return None
    return (p1 / p0) ** (1 / years) - 1


def build_cape_return_stats(df) -> list:
    """
    RE-SHILLER-DASH.5 -- Armando: "el bloque más valioso que falta...
    cuando el CAPE estaba en rangos parecidos, ¿qué retornos reales
    anualizados se observaron después?" Not a prediction: a descriptive
    reduction (median) of what already happened, computed once per
    month over the full series, then grouped into CAPE_RETURN_BUCKETS.
    n_months (bucket size) and n_Xy (months with a valid Xy-forward
    return, which shrinks for the longer horizons near the end of the
    series) are kept alongside every median, on purpose -- Armando's
    own caveat is "periodos pocos y no independientes"; a bare median
    with no sample size would hide exactly how thin some of these
    buckets are.
    """
    valid = df[df["CAPE"].notna()].copy()
    for years in FORWARD_RETURN_YEARS:
        valid[f"fwd_{years}y"] = [
            _forward_real_total_return(df, d, years) for d in valid["Date"]
        ]

    rows = []
    for threshold, label in CAPE_RETURN_BUCKETS:
        bucket = valid if threshold is None else valid[valid["CAPE"] > threshold]
        row = {"label": label, "n_months": len(bucket)}
        for years in FORWARD_RETURN_YEARS:
            series = bucket[f"fwd_{years}y"].dropna()
            median = series.median() if len(series) else None
            row[f"median_{years}y"] = median
            row[f"n_{years}y"] = len(series)
            # RE-SHILLER-DASH.6 -- cumulative equivalent of the
            # annualized median, computed here (not hand-typed in the
            # HTML) so the plain-language lead paragraph can quote a
            # real number instead of an approximation that could drift
            # from the table above it.
            row[f"cumulative_{years}y"] = (1 + median) ** years - 1 if median is not None else None
        rows.append(row)
    return rows


def build_drawdown_summary(episodes) -> dict:
    """
    RE-SHILLER-DASH.5 -- Armando: "ya sombreas las 23 caídas, pero falta
    una lectura agregada." Pure aggregation over the Episode objects
    run_drawdown_engine() already produced -- no new detection, no
    recomputation of any peak/bottom/recovery date.
    """
    drawdowns = [e.drawdown for e in episodes if e.drawdown is not None]
    durations = [e.duration_months for e in episodes if e.duration_months is not None]
    recoveries = [e.recovery_months for e in episodes if e.recovery_months is not None]
    return {
        "n": len(episodes),
        "median_drawdown": statistics.median(drawdowns) if drawdowns else None,
        "worst_drawdown": min(drawdowns) if drawdowns else None,
        "median_duration": statistics.median(durations) if durations else None,
        "median_recovery": statistics.median(recoveries) if recoveries else None,
        "n_recovered": len(recoveries),
    }


def build_notable_drawdowns(episodes) -> list:
    """
    RE-SHILLER-DASH.6 -- Armando: "los dos o tres peores episodios de
    drawdowns que tienen nombre y apellidos". Takes the real top-3 by
    magnitude from the 23 detected episodes (not cherry-picked for
    fame) and attaches the name from NOTABLE_DRAWDOWN_NAMES. If a
    future data refresh ever changes which episodes rank in the top 3,
    an unnamed one falls back to a plain, honest label instead of a
    KeyError or a silently wrong name -- fail-visible, not fail-silent.
    """
    worst = sorted(episodes, key=lambda e: e.drawdown)[:N_NOTABLE_DRAWDOWNS]
    rows = []
    for e in worst:
        name = NOTABLE_DRAWDOWN_NAMES.get(e.peak_date, "Episodio sin nombre popular asignado")
        rows.append({
            "name": name,
            "peak_date": _fmt_shiller_date(e.peak_date),
            "bottom_date": _fmt_shiller_date(e.bottom_date),
            "drawdown": e.drawdown,
            "duration_months": e.duration_months,
        })
    return rows


def build_shiller_data() -> dict:
    dataset = run_drawdown_engine()
    df = dataset.data
    episodes = dataset.episodes
    latest = df.iloc[-1]

    cape_series = df["CAPE"].dropna()
    cape_mean = cape_series.mean()
    cape_std = cape_series.std()
    cape_today = latest["CAPE"]

    # RE-SHILLER-DASH.2 -- percentile Armando asked for: the share of
    # historical months whose CAPE was below today's, over the full
    # series (not the matched-episode subset -- a different, wider
    # population than Regime Comparability Gate's, same distinction
    # context_band() already draws in generate_dashboard.py).
    cape_percentile = (cape_series < cape_today).mean() * 100

    latest_date = latest["Date"]
    cape_recent_cutoff = latest_date - CAPE_RECENT_YEARS
    cape_recent_mean = df[df["Date"] >= cape_recent_cutoff]["CAPE"].dropna().mean()

    inflation_mean = df["InflationRate1Y"].mean()
    inflation_std = df["InflationRate1Y"].std()
    rate_mean = df["Rate GS10"].mean()
    rate_std = df["Rate GS10"].std()

    cape_z = _zscore(cape_today, cape_mean, cape_std)
    inflation_z = _zscore(latest["InflationRate1Y"], inflation_mean, inflation_std)
    rate_z = _zscore(latest["Rate GS10"], rate_mean, rate_std)

    cape_short, cape_long = _context_words(cape_z)
    inflation_short, inflation_long = _context_words(inflation_z)
    rate_short, rate_long = _context_words(rate_z)
    drawdown_reading = drawdown_context(latest["Drawdown"])

    # RE-SHILLER-DASH.3/4 -- which dimension "drives" the headline:
    # whichever of the three has the largest absolute z-score, i.e.
    # the most anomalous reading relative to its own history -- not an
    # arbitrary pick, the same magnitude axis _reading_magnitude_color()
    # already uses per-row. Keeps (key, short, long) together so the
    # headline builder doesn't have to re-derive which dimension won.
    driver_key, driver_short, driver_long = max(
        [
            (abs(cape_z or 0), "cape", cape_short, cape_long),
            (abs(inflation_z or 0), "inflation", inflation_short, inflation_long),
            (abs(rate_z or 0), "rate", rate_short, rate_long),
        ],
        key=lambda row: row[0],
    )[1:]

    return {
        "df": df,
        "episodes": episodes,
        "latest_date": latest_date,
        "latest_date_label": _fmt_shiller_date(latest_date),
        "latest_drawdown": latest["Drawdown"],
        "latest_price_real": latest["Price"],
        "latest_cape": cape_today,
        "latest_inflation": latest["InflationRate1Y"],
        "latest_rate": latest["Rate GS10"],
        "cape_mean": cape_mean,
        "cape_std": cape_std,
        "cape_percentile": cape_percentile,
        "cape_recent_mean": cape_recent_mean,
        "inflation_mean": inflation_mean,
        "inflation_std": inflation_std,
        "rate_mean": rate_mean,
        "rate_std": rate_std,
        "drawdown_reading": drawdown_reading,
        "cape_short": cape_short,
        "cape_long": cape_long,
        "inflation_short": inflation_short,
        "inflation_long": inflation_long,
        "rate_short": rate_short,
        "rate_long": rate_long,
        "driver_key": driver_key,
        "driver_long": driver_long,
        "driver_magnitude_color": _reading_magnitude_color(driver_short),
        "n_episodes": len(episodes),
        "earliest_date": df["Date"].min(),
        "cape_return_rows": build_cape_return_stats(df),
        "drawdown_summary": build_drawdown_summary(episodes),
        "notable_drawdowns": build_notable_drawdowns(episodes),
    }


def _lower_first(text: str) -> str:
    return text[0].lower() + text[1:] if text else text


def build_headline(data: dict) -> str:
    """
    RE-SHILLER-DASH.4 -- replaces the RE-SHILLER-DASH.2 single run-on
    sentence. Armando: "el resumen ejecutivo en líneas con texto
    seguido... que poco detalle." A McKinsey-style headline is short
    and leads with the one fact that matters; the four-clause sentence
    gave every dimension equal weight regardless of whether anything
    about it was actually notable.

    Returns one short title sentence built around market status +
    whichever dimension is most anomalous today (driver_key/driver_long,
    same computation the headline dot and the indicator table's dots
    already use -- not a second judgment).

    RE-SHILLER-DASH.4b -- Armando, same day, on the first version of
    this fix: "repites los datos, en pequeño y en grande" -- correct,
    the four-figure subtitle this function used to also return duplicated
    the stat-strip immediately below it verbatim (same four numbers,
    same order). Dropped the subtitle entirely: build_stat_strip()
    already is the detail layer now ("las cifras cada una por su lado"),
    the headline only needs to say the one sentence that matters.
    """
    drawdown = data["latest_drawdown"]
    if drawdown is not None and drawdown == 0.0:
        market = "Mercado en máximo histórico"
    elif drawdown is not None:
        market = f"Mercado con una caída del {_fmt_pct(abs(drawdown))} desde máximos"
    else:
        market = "Estado de mercado no disponible"

    if data["driver_magnitude_color"] == "near":
        return f"{market}. CAPE, inflación y tipos dentro de sus rangos históricos normales."

    driver_label = DRIVER_LABEL_ES[data["driver_key"]]
    return f"{market}, con {driver_label} {_lower_first(data['driver_long'])}."


def build_stat_strip(data: dict) -> str:
    """
    RE-SHILLER-DASH.4 -- Armando: "las cifras cada una por su lado".
    Same .stat-strip/.stat-value/.stat-label pattern already approved
    for "Evidencia histórica" in the operational dashboard (RE-DASH.
    1.11) -- reused, not a new visual language. Each tile gets the same
    dot already computed for the indicator table below it (RE-SHILLER-
    DASH.3), so the two can't disagree.
    """
    tiles = [
        (_fmt_num(data["latest_cape"], 1), f"CAPE (percentil {_fmt_num(data['cape_percentile'], 0)})", "mag-dot", _reading_magnitude_color(data["cape_short"])),
        (_fmt_pct(data["latest_drawdown"]), "Drawdown", "dot", drawdown_dot_color(data["latest_drawdown"])),
        (_fmt_pct(data["latest_inflation"], 2), "Inflación interanual", "mag-dot", _reading_magnitude_color(data["inflation_short"])),
        (_fmt_rate(data["latest_rate"]), "Tipo a 10 años", "mag-dot", _reading_magnitude_color(data["rate_short"])),
    ]
    body = "".join(
        f'<div class="stat"><div class="stat-value"><span class="{dot_class} {color}"></span>{_esc(value)}</div>'
        f'<div class="stat-label">{_esc(label)}</div></div>'
        for value, label, dot_class, color in tiles
    )
    return f'<div class="stat-strip">{body}</div>'


def _readable_lectura(short_label: str, value, mean) -> str:
    """
    RE-SHILLER-DASH.5 -- Armando: en "Detalle de indicadores", inflación
    muestra "Cerca de la media" pese a que 4,23% vs 2,31% (casi el
    doble) "puede chirriar visualmente". The z-score classification is
    correct and NOT changed here: inflación's std is 5.76pp (a century
    including hyperinflation and deflation makes the "near" band
    genuinely wide), Z_THRESHOLD_NEAR is Armando-confirmed and shared
    with the operational dashboard (generate_dashboard.py's own
    _context_words()) -- not touched, out of scope for a wording
    complaint about one column in one table. This is additive and
    local: when the band is "Cerca de la media" but the raw value sits
    above/below the raw mean, say so explicitly instead of just "Cerca"
    -- same fix applied to all three z-scored rows (CAPE, Inflación,
    Tipo) for consistency, not only the row Armando happened to point
    at. Does not change the dot color (still "near") or which dimension
    counts as the headline's driver -- both still key off the untouched
    short_label from _context_words().
    """
    if short_label != "Cerca de la media" or value is None or mean is None:
        return short_label
    if value > mean:
        return "Por encima de la media, dentro del rango histórico habitual"
    if value < mean:
        return "Por debajo de la media, dentro del rango histórico habitual"
    return short_label


def build_indicator_strip(data: dict) -> str:
    """
    RE-SHILLER-DASH.2/3/4 -- Armando's requested table, "contexto en 10
    segundos" before the charts, now with a dot per row (semáforo).
    Drawdown's "Media histórica" cell is an em dash, not a number --
    RE-DASH.1.4 already established drawdown as "reported as a plain
    fact, not a z-score" (a series that's ~0% most of the time has a
    near-meaningless mean/std for this purpose), kept consistent here
    rather than inventing a number that would misread as comparable to
    the other three rows. Drawdown's dot uses ok/warn (a real status);
    the other three use the near/notable/extreme magnitude scale --
    see _reading_magnitude_color()'s docstring for why they're not the
    same color language.

    RE-SHILLER-DASH.4 -- Inflación forced to 2 decimals (was _fmt_pct's
    default of 1), matching Tipo's 2 decimals -- Armando: "una con dos
    decimales, otras con uno". The exact same mismatch (_fmt_pct's 1dp
    default vs. _fmt_rate's 2dp default) already exists in outputs/
    dashboard.html's own Datos de mercado table -- not changed here,
    flagged to Armando separately since that's a different file.

    RE-SHILLER-DASH.5 -- "Lectura" text now runs through
    _readable_lectura() so a "cerca de la media" reading also says
    above/below the raw mean when that's true (see that function's
    docstring). Dot colors unchanged -- still keyed off the raw
    short_label, not the readable text.
    """
    rows = [
        ("Drawdown", _fmt_pct(data["latest_drawdown"]), "--", data["drawdown_reading"], "dot", drawdown_dot_color(data["latest_drawdown"])),
        ("CAPE", _fmt_num(data["latest_cape"], 1), _fmt_num(data["cape_mean"], 1), _readable_lectura(data["cape_short"], data["latest_cape"], data["cape_mean"]), "mag-dot", _reading_magnitude_color(data["cape_short"])),
        ("Inflación", _fmt_pct(data["latest_inflation"], 2), _fmt_pct(data["inflation_mean"], 2), _readable_lectura(data["inflation_short"], data["latest_inflation"], data["inflation_mean"]), "mag-dot", _reading_magnitude_color(data["inflation_short"])),
        ("Tipo (10 años)", _fmt_rate(data["latest_rate"]), _fmt_rate(data["rate_mean"]), _readable_lectura(data["rate_short"], data["latest_rate"], data["rate_mean"]), "mag-dot", _reading_magnitude_color(data["rate_short"])),
    ]
    body = "".join(
        f"<tr><td>{_esc(label)}</td><td class=\"num\">{_esc(hoy)}</td>"
        f"<td class=\"num\">{_esc(media)}</td>"
        f"<td><span class=\"{dot_class} {color}\"></span>{_esc(lectura)}</td></tr>"
        for label, hoy, media, lectura, dot_class, color in rows
    )
    return f"""
    <table>
      <tr><th>Métrica</th><th class="num">Hoy</th><th class="num">Media histórica</th><th>Lectura</th></tr>
      {body}
    </table>
    """


def build_cape_returns_table(rows: list) -> str:
    """
    RE-SHILLER-DASH.5 -- Armando's requested format: CAPE inicial |
    retorno real 5a/10a/15a (mediana). "N (meses)" appended per bucket
    -- not in his original mockup, added because his own caveat
    ("periodos pocos y no independientes") is much more concrete with
    the actual count next to each median than as a generic sentence
    below the table.
    """
    body = "".join(
        "<tr><td>{label}</td>{cells}<td class=\"num\">{n}</td></tr>".format(
            label=_esc(row["label"]),
            cells="".join(
                f'<td class="num">{_esc(_fmt_pct(row[f"median_{y}y"], 1))}</td>'
                for y in FORWARD_RETURN_YEARS
            ),
            n=row["n_months"],
        )
        for row in rows
    )
    header_cells = "".join(f'<th class="num">A {y} años</th>' for y in FORWARD_RETURN_YEARS)
    return f"""
    <table>
      <tr><th>CAPE inicial</th>{header_cells}<th class="num">N (meses)</th></tr>
      {body}
    </table>
    """


def build_notable_drawdowns_table(rows: list) -> str:
    body = "".join(
        f"<tr><td>{_esc(r['name'])}</td>"
        f"<td class=\"num\">{_esc(r['peak_date'])} -&gt; {_esc(r['bottom_date'])}</td>"
        f"<td class=\"num\">{_esc(_fmt_pct(r['drawdown']))}</td>"
        f"<td class=\"num\">{r['duration_months']} meses</td></tr>"
        for r in rows
    )
    return f"""
    <table>
      <tr><th>Episodio</th><th class="num">Pico -&gt; Fondo</th><th class="num">Caída</th><th class="num">Duración</th></tr>
      {body}
    </table>
    """


def build_drawdown_summary_table(summary: dict) -> str:
    rows = [
        ("Episodios de caída detectados", str(summary["n"])),
        ("Caída mediana", _fmt_pct(summary["median_drawdown"])),
        ("Peor caída", _fmt_pct(summary["worst_drawdown"])),
        ("Duración mediana, pico -> fondo", f"{_fmt_num(summary['median_duration'], 0)} meses" if summary["median_duration"] is not None else "No disponible"),
        ("Recuperación mediana, fondo -> máximo previo", f"{_fmt_num(summary['median_recovery'], 0)} meses" if summary["median_recovery"] is not None else "No disponible"),
    ]
    body = "".join(
        f"<tr><td>{_esc(label)}</td><td class=\"num\">{_esc(value)}</td></tr>"
        for label, value in rows
    )
    return f"""
    <table>
      <tr><th>Métrica</th><th class="num">Valor</th></tr>
      {body}
    </table>
    """


def render_html(data: dict) -> str:
    df = data["df"]
    episodes = data["episodes"]
    fecha = data["latest_date_label"]

    # RE-SHILLER-DASH.3 -- "fecha y valor de la última cifra... para
    # ubicarnos en las gráficas": one label per chart, built here (not
    # inside the chart functions) from the same values/formatters the
    # captions below each chart already use, so the on-image annotation
    # and the text note can't show two different numbers.
    price_img = chart_price(df, episodes, f"{fecha}: {_fmt_num(data['latest_price_real'], 0)}")
    cape_img = chart_series(df, episodes, "CAPE", "CAPE", f"{fecha}: {_fmt_num(data['latest_cape'], 1)}")
    inflation_img = chart_series(
        df, episodes, "InflationRate1Y", "Inflación interanual (%)",
        f"{fecha}: {_fmt_pct(data['latest_inflation'])}", as_pct=True,
    )
    rate_img = chart_series(df, episodes, "Rate GS10", "Tipo a 10 años (%)", f"{fecha}: {_fmt_rate(data['latest_rate'])}")

    range_label = f"{_fmt_shiller_date(data['earliest_date'])} - {fecha}"
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    headline_title = build_headline(data)

    # RE-SHILLER-DASH.5 -- pulled out of the caveat f-string below for
    # readability; count of months behind the "CAPE > 40" bucket,
    # verified by direct inspection (see module docstring) to be almost
    # entirely one historical cluster (1999-2000), not independent
    # trials.
    cape_gt_40_n = next(r["n_months"] for r in data["cape_return_rows"] if r["label"] == "CAPE > 40")

    # RE-SHILLER-DASH.6 -- Armando: "NO entiendo las cifras de la tabla
    # de CAPE." Pulled out so the plain-language lead paragraph can
    # quote real, computed cumulative figures (not hand-typed
    # approximations) for the row closest to today's CAPE (41,4) versus
    # the "todos los meses" baseline, in the same sentence.
    cape_gt_40_row = next(r for r in data["cape_return_rows"] if r["label"] == "CAPE > 40")
    cape_all_row = next(r for r in data["cape_return_rows"] if r["label"] == "Todos los meses")

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>SOP -- Panorama histórico (Shiller)</title>
<style>
  body {{ font-family: -apple-system, Helvetica, Arial, sans-serif; font-size:0.88rem; background:#f7f7f5; color:#1a1a1a; margin:0; padding:2rem; line-height:1.5; }}
  header {{ margin-bottom: 1.5rem; }}
  h1 {{ font-size: 1.4rem; font-weight:700; margin-bottom: 0.2rem; letter-spacing:-0.01em; }}
  .subtitle {{ color:#666; font-size:0.9rem; margin:0 0 0.6rem 0; }}
  .header-grid {{ display:flex; gap:2rem; flex-wrap:wrap; font-size:0.85rem; color:#666; }}
  .card {{ background:#fff; border:1px solid #ddd; border-left:3px solid #ddd; border-radius:2px; padding:1rem 1.25rem; margin-bottom:1rem; text-align:left; }}
  .card h2 {{ font-size:0.95rem; font-weight:700; margin-top:0; margin-bottom:0.4rem; padding-bottom:0.4rem; border-bottom:1px solid #eee; letter-spacing:0.01em; }}
  .card img {{ width:100%; height:auto; display:block; margin:0.4rem 0; }}
  /* RE-SHILLER-DASH.4 -- same headline-action/headline-sub split as
     outputs/dashboard.html's "Estado hoy" (RE-DASH.1.11), reused here
     rather than the RE-SHILLER-DASH.2 run-on sentence Armando called
     out ("en líneas con texto seguido"). */
  .headline-action {{ font-size:1.15rem; font-weight:700; letter-spacing:-0.01em; display:flex; align-items:center; margin:0; }}
  /* Same .stat-strip/.stat-value/.stat-label pattern already approved
     for "Evidencia histórica" (RE-DASH.1.11) -- reused, not a new
     visual language, so headline figures read as grouped tiles instead
     of scattered numbers ("las cifras cada una por su lado"). */
  .stat-strip {{ display:flex; flex-wrap:wrap; gap:2rem; margin:0.6rem 0 0.2rem; }}
  .stat-value {{ font-size:1.5rem; font-weight:700; letter-spacing:-0.01em; display:flex; align-items:center; font-variant-numeric:tabular-nums; }}
  .stat-label {{ font-size:0.76rem; color:#666; margin-top:0.15rem; max-width:11rem; }}
  table {{ border-collapse: collapse; width:100%; font-size:0.88rem; margin-bottom:0.5rem; }}
  td, th {{ text-align:left; padding:0.4rem 0.6rem; border-bottom:1px solid #f0f0f0; vertical-align:top; }}
  th {{ color:#666; font-weight:700; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.04em; white-space:nowrap; }}
  td.num, th.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
  .note {{ font-size:0.82rem; color:#666; margin-top:0.3rem; }}
  .legend {{ font-size:0.78rem; color:#666; margin-top:0.3rem; }}
  .legend .sw {{ display:inline-block; width:0.7rem; height:0.7rem; border-radius:1px; margin-right:0.3rem; vertical-align:middle; }}
  .caveat {{ font-size:0.85rem; color:#4a3410; background:#faf6ee; border-left:2px solid #96650f; padding:0.5rem 0.75rem; margin-top:0.6rem; }}

  /* RE-SHILLER-DASH.3 -- two dot languages, deliberately distinct
     (see _reading_magnitude_color()'s docstring in the Python for the
     full reasoning): .dot is a real status (ok/warn), same hex values
     as outputs/dashboard.html's own .dot for visual consistency
     between the two dashboards. .mag-dot is distance-from-historical-
     norm, not sentiment -- same hex values reused, different class
     name so the two can't be read as the same judgment. */
  .dot, .mag-dot {{ display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:0.5rem; flex-shrink:0; vertical-align:middle; }}
  .dot.ok {{ background:#2f8f4e; }}
  .dot.warn {{ background:#96650f; }}
  .mag-dot.near {{ background:#999999; }}
  .mag-dot.notable {{ background:#96650f; }}
  .mag-dot.extreme {{ background:#c23b3b; }}
  .card.accent-ok {{ border-left-color:#2f8f4e; }}
  .card.accent-near {{ border-left-color:#999999; }}
  .card.accent-notable {{ border-left-color:#96650f; }}
  .card.accent-extreme {{ border-left-color:#c23b3b; }}
</style>
</head>
<body>
<header>
  <h1>SOP -- Panorama histórico (Shiller)</h1>
  <p class="subtitle">Serie completa de Robert Shiller ({range_label}), tal y como la carga y calcula el Research Engine. Solo lectura, sin gráficas interactivas.</p>
  <div class="header-grid">
    <span>Generado: {generated_at}</span>
    <span>Episodios de caída detectados en toda la serie: {data['n_episodes']}</span>
  </div>
</header>

<section class="card accent-{data['driver_magnitude_color']}">
  <h2>Resumen ejecutivo</h2>
  <p class="headline-action"><span class="mag-dot {data['driver_magnitude_color']}"></span>{_esc(headline_title)}</p>
  {build_stat_strip(data)}
</section>

<section class="card">
  <h2>Detalle de indicadores</h2>
  {build_indicator_strip(data)}
</section>

<section class="card">
  <h2>S&amp;P 500 -- precio real, sin dividendos</h2>
  <img src="{price_img}" alt="Precio real del S&amp;P 500, 1871-2026, con episodios de caída sombreados">
  <p class="legend">
    <span class="sw" style="background:{COLOR_DRAWDOWN};opacity:.4"></span>Fase de caída (pico -&gt; fondo)
    &nbsp;&nbsp;<span class="sw" style="background:{COLOR_RECOVERY};opacity:.4"></span>Fase de recuperación (fondo -&gt; recuperación)
    &nbsp;&nbsp;<span class="sw" style="background:{COLOR_TODAY}"></span>Hoy
  </p>
  <p class="note">Precio real (ajustado por inflación), sin dividendos reinvertidos, escala logarítmica -- necesaria para que un siglo y medio de crecimiento compuesto quepa en una sola gráfica legible. Las {data['n_episodes']} zonas sombreadas son los episodios que run_drawdown_engine() detecta en toda la serie, los mismos que usa el resto del sistema -- no una segunda detección. Nota técnica: la detección de episodios en sí (fechas de pico/fondo/recuperación, % de caída) se calcula sobre el precio nominal, sin ajustar por inflación -- esta gráfica solo cambia qué línea de precio se dibuja, no cómo se detectan los episodios.</p>
  <p class="note">Último dato disponible: {fecha} -- {_fmt_num(data['latest_price_real'], 0)}.</p>
</section>

<section class="card">
  <h2>Resumen de drawdowns históricos</h2>
  {build_drawdown_summary_table(data['drawdown_summary'])}
  <p class="note">Lectura agregada de las {data['n_episodes']} caídas sombreadas en la gráfica de arriba -- mismos episodios, sin recalcular nada. Las {data['n_episodes']} han recuperado su máximo previo dentro de la serie (ninguna sigue abierta a día de hoy, coherente con que el mercado está en máximo histórico ahora mismo).</p>
  <h2 style="margin-top:1rem;">Los peores episodios, con nombre</h2>
  {build_notable_drawdowns_table(data['notable_drawdowns'])}
  <p class="note">Los tres peores por magnitud, de los {data['n_episodes']} detectados. 1929 y 2007-2009 son identificaciones de alta confianza (episodios ampliamente documentados). El tercero incluye su propia advertencia en el nombre: la fecha de pico que detecta el motor no coincide con exactitud con el Pánico de 1873 tal y como se documenta habitualmente -- no verificado con precisión.</p>
</section>

<section class="card">
  <h2>CAPE (Cyclically Adjusted P/E)</h2>
  <img src="{cape_img}" alt="CAPE de Shiller, 1871-2026">
  <p class="note">Media de toda la serie: {_fmt_num(data['cape_mean'], 1)} (línea discontinua). Media de los últimos {CAPE_RECENT_YEARS} años: {_fmt_num(data['cape_recent_mean'], 1)}. Desviación típica: {_fmt_num(data['cape_std'], 1)}. Percentil histórico: {_fmt_num(data['cape_percentile'], 0)} -- el CAPE de hoy supera al de aproximadamente ese porcentaje de meses en toda la serie.</p>
  <p class="note">Último dato disponible: {fecha} -- {_fmt_num(data['latest_cape'], 1)}.</p>
</section>

<section class="card">
  <h2>Retornos reales posteriores según CAPE inicial</h2>
  <p class="note" style="margin-top:0;">Cómo leer esta tabla: para cada mes de la serie con el CAPE en el rango indicado, ¿cuánto valió realmente (ajustado por inflación, dividendos reinvertidos) haber invertido a partir de ahí, N años después? La cifra es un <strong>porcentaje anual</strong>, no acumulado -- un -4,5% anual durante 5 años no es "-4,5% en total", es más. Ejemplo concreto con la fila que más se parece a hoy (CAPE actual: {_fmt_num(data['latest_cape'], 1)}): en los {cape_gt_40_row['n_months']} meses históricos con CAPE &gt; 40, la mediana fue {_fmt_pct(cape_gt_40_row['median_5y'], 1)} anual a 5 años -- equivalente a un {_fmt_pct(cape_gt_40_row['cumulative_5y'], 0)} acumulado en esos 5 años -- {_fmt_pct(cape_gt_40_row['median_10y'], 1)} anual ({_fmt_pct(cape_gt_40_row['cumulative_10y'], 0)} acumulado) a 10 años, y {_fmt_pct(cape_gt_40_row['median_15y'], 1)} anual ({_fmt_pct(cape_gt_40_row['cumulative_15y'], 0)} acumulado) a 15 años. Que el signo cambie de negativo a positivo entre 10 y 15 años no es un error: es reversión a la media -- el mercado tardó más en dar retorno positivo, pero incluso a 15 años ese {_fmt_pct(cape_gt_40_row['median_15y'], 1)} anual queda muy por debajo del {_fmt_pct(cape_all_row['median_15y'], 1)} anual de "todos los meses" (la fila sin filtrar, la referencia de fondo).</p>
  {build_cape_returns_table(data['cape_return_rows'])}
  <p class="note">Retorno real total anualizado (CAGR, dividendos reinvertidos), medido desde cada mes con el CAPE indicado hasta N años después, mediana por grupo -- mismo cálculo que ya usa el Research Engine para future_return_5y/10y en drawdown_engine.py, aplicado aquí a todos los meses de la serie, no solo a los 23 fondos de episodio.</p>
  <p class="caveat">Muestra descriptiva, no señal operativa. Los periodos con CAPE extremo son pocos y no independientes: los {cape_gt_40_n} meses de la fila "CAPE &gt; 40" proceden casi en su totalidad de un único episodio histórico (1999-2000, más los últimos meses de hoy, aún sin retorno futuro que medir); "CAPE &gt; 35" combina dos periodos distintos (1998-2001 y 2021-2026), no docenas de casos independientes.</p>
</section>

<section class="card">
  <h2>Inflación interanual</h2>
  <img src="{inflation_img}" alt="Inflación interanual (CPI), 1871-2026">
  <p class="note">Media de toda la serie: {_fmt_pct(data['inflation_mean'], 2)} (línea discontinua). Desviación típica: {_fmt_pct(data['inflation_std'], 2)}.</p>
  <p class="note">Último dato disponible: {fecha} -- {_fmt_pct(data['latest_inflation'], 2)}.</p>
</section>

<section class="card">
  <h2>Tipo de interés (bono EEUU 10 años)</h2>
  <img src="{rate_img}" alt="Tipo de interés a 10 años, 1871-2026">
  <p class="note">Media de toda la serie: {_fmt_rate(data['rate_mean'])} (línea discontinua). Desviación típica: {_fmt_rate(data['rate_std'])}.</p>
  <p class="note">Último dato disponible: {fecha} -- {_fmt_rate(data['latest_rate'])}.</p>
</section>

<section class="card">
  <h2>Nota metodológica</h2>
  <p class="note">"Lectura" en la franja de indicadores y en el resumen ejecutivo usa el mismo criterio (z-score contra la media/desviación de toda la serie, bandas confirmadas por Armando) que ya usa el bloque "Datos de mercado" del dashboard operativo -- un mismo idioma entre los dos paneles, no dos criterios distintos.</p>
  <p class="caveat">Qué NO dice este panel: no dice si comprar o vender, no evalúa gates, no propone postura ni acción. Solo sitúa el mercado actual frente a su propia historia. La lectura del día -- qué autoriza y qué no -- sigue viviendo únicamente en el dashboard operativo (dashboard.html).</p>
</section>

</body>
</html>
"""


def main() -> None:

    data = build_shiller_data()
    output = render_html(data)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(output, encoding="utf-8")

    print(f"Panorama histórico generado: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
