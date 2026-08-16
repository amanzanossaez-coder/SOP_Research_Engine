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

Read-only, single command, no server:

    python3 generate_shiller_dashboard.py
"""

import base64
import io
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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


def _fig_to_data_uri(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


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


def chart_price(df, episodes) -> str:
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
    ax.set_ylabel("Precio real, sin dividendos (escala log)", fontsize=8.5, color="#666666")
    _style_axes(ax)
    return _fig_to_data_uri(fig)


def chart_series(df, episodes, column, ylabel, as_pct=False) -> str:
    fig, ax = plt.subplots(figsize=(9.2, 2.6))
    _shade_episodes(ax, episodes)
    series = df[column] * 100 if as_pct else df[column]
    ax.plot(df["Date"], series, color=COLOR_LINE, linewidth=1.0, zorder=3)
    mean_value = series.mean()
    ax.axhline(mean_value, color=COLOR_MEAN, linewidth=0.9, linestyle="--", zorder=2)
    latest = df.iloc[-1]
    latest_value = latest[column] * 100 if as_pct else latest[column]
    ax.scatter([latest["Date"]], [latest_value], color=COLOR_TODAY, s=20, zorder=4)
    ax.set_ylabel(ylabel, fontsize=8.5, color="#666666")
    _style_axes(ax)
    return _fig_to_data_uri(fig)


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

    cape_short, cape_long = _context_words(_zscore(cape_today, cape_mean, cape_std))
    inflation_short, inflation_long = _context_words(
        _zscore(latest["InflationRate1Y"], inflation_mean, inflation_std)
    )
    rate_short, rate_long = _context_words(_zscore(latest["Rate GS10"], rate_mean, rate_std))
    drawdown_reading = drawdown_context(latest["Drawdown"])

    return {
        "df": df,
        "episodes": episodes,
        "latest_date": latest_date,
        "latest_drawdown": latest["Drawdown"],
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
        "n_episodes": len(episodes),
        "earliest_date": df["Date"].min(),
    }


def _lower_first(text: str) -> str:
    return text[0].lower() + text[1:] if text else text


def build_executive_summary(data: dict) -> str:
    """
    RE-SHILLER-DASH.2 -- Armando: "falta la frase ejecutiva... eso
    convierte el panel en lectura, no solo visualizacion." Built
    entirely from the same readings the indicator strip shows below it
    (drawdown_context(), _context_words()) -- not a second, separately
    worded judgment that could disagree with the table under it.
    """
    return (
        "Lectura actual: "
        f"{_lower_first(data['drawdown_reading'])}, "
        f"CAPE {_lower_first(data['cape_long'])}, "
        f"inflación {_lower_first(data['inflation_long'])} "
        f"y tipos {_lower_first(data['rate_long'])}."
    )


def build_indicator_strip(data: dict) -> str:
    """
    RE-SHILLER-DASH.2 -- Armando's requested table, "contexto en 10
    segundos" before the charts. Drawdown's "Media histórica" cell is
    an em dash, not a number -- RE-DASH.1.4 already established
    drawdown as "reported as a plain fact, not a z-score" (a series
    that's ~0% most of the time has a near-meaningless mean/std for
    this purpose), kept consistent here rather than inventing a number
    that would misread as comparable to the other three rows.
    """
    rows = [
        ("Drawdown", _fmt_pct(data["latest_drawdown"]), "--", data["drawdown_reading"]),
        ("CAPE", _fmt_num(data["latest_cape"], 1), _fmt_num(data["cape_mean"], 1), data["cape_short"]),
        ("Inflación", _fmt_pct(data["latest_inflation"]), _fmt_pct(data["inflation_mean"]), data["inflation_short"]),
        ("Tipo (10 años)", _fmt_rate(data["latest_rate"]), _fmt_rate(data["rate_mean"]), data["rate_short"]),
    ]
    body = "".join(
        f"<tr><td>{_esc(label)}</td><td class=\"num\">{_esc(hoy)}</td>"
        f"<td class=\"num\">{_esc(media)}</td><td>{_esc(lectura)}</td></tr>"
        for label, hoy, media, lectura in rows
    )
    return f"""
    <table>
      <tr><th>Métrica</th><th class="num">Hoy</th><th class="num">Media histórica</th><th>Lectura</th></tr>
      {body}
    </table>
    """


def render_html(data: dict) -> str:
    df = data["df"]
    episodes = data["episodes"]

    price_img = chart_price(df, episodes)
    cape_img = chart_series(df, episodes, "CAPE", "CAPE")
    inflation_img = chart_series(df, episodes, "InflationRate1Y", "Inflación interanual (%)", as_pct=True)
    rate_img = chart_series(df, episodes, "Rate GS10", "Tipo a 10 años (%)")

    range_label = f"{_fmt_shiller_date(data['earliest_date'])} - {_fmt_shiller_date(data['latest_date'])}"
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

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
  .headline-sub {{ color:#333; margin:0; font-size:1.02rem; font-weight:700; }}
  table {{ border-collapse: collapse; width:100%; font-size:0.88rem; margin-bottom:0.5rem; }}
  td, th {{ text-align:left; padding:0.4rem 0.6rem; border-bottom:1px solid #f0f0f0; vertical-align:top; }}
  th {{ color:#666; font-weight:700; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.04em; white-space:nowrap; }}
  td.num, th.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
  .note {{ font-size:0.82rem; color:#666; margin-top:0.3rem; }}
  .legend {{ font-size:0.78rem; color:#666; margin-top:0.3rem; }}
  .legend .sw {{ display:inline-block; width:0.7rem; height:0.7rem; border-radius:1px; margin-right:0.3rem; vertical-align:middle; }}
  .caveat {{ font-size:0.85rem; color:#4a3410; background:#faf6ee; border-left:2px solid #96650f; padding:0.5rem 0.75rem; margin-top:0.6rem; }}
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

<section class="card">
  <h2>Resumen ejecutivo</h2>
  <p class="headline-sub">{_esc(build_executive_summary(data))}</p>
</section>

<section class="card">
  <h2>Indicadores clave</h2>
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
</section>

<section class="card">
  <h2>CAPE (Cyclically Adjusted P/E)</h2>
  <img src="{cape_img}" alt="CAPE de Shiller, 1871-2026">
  <p class="note">Hoy: {_fmt_num(data['latest_cape'], 1)}. Media de toda la serie: {_fmt_num(data['cape_mean'], 1)} (línea discontinua). Media de los últimos {CAPE_RECENT_YEARS} años: {_fmt_num(data['cape_recent_mean'], 1)}. Desviación típica: {_fmt_num(data['cape_std'], 1)}. Percentil histórico: {_fmt_num(data['cape_percentile'], 0)} -- el CAPE de hoy supera al de aproximadamente ese porcentaje de meses en toda la serie.</p>
</section>

<section class="card">
  <h2>Inflación interanual</h2>
  <img src="{inflation_img}" alt="Inflación interanual (CPI), 1871-2026">
  <p class="note">Hoy: {_fmt_pct(data['latest_inflation'])}. Media de toda la serie: {_fmt_pct(data['inflation_mean'])} (línea discontinua). Desviación típica: {_fmt_pct(data['inflation_std'])}.</p>
</section>

<section class="card">
  <h2>Tipo de interés (bono EEUU 10 años)</h2>
  <img src="{rate_img}" alt="Tipo de interés a 10 años, 1871-2026">
  <p class="note">Hoy: {_fmt_rate(data['latest_rate'])}. Media de toda la serie: {_fmt_rate(data['rate_mean'])} (línea discontinua). Desviación típica: {_fmt_rate(data['rate_std'])}.</p>
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
