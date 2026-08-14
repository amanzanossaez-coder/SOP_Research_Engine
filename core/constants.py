SIMILARITY_WEIGHTS = {

    # Evento

    "drawdown": 0.25,
    "duration": 0.15,
    "speed": 0.10,

    # Contexto

    "cape": 0.20,
    "pre_crash_return_3y": 0.10,
    "volatility": 0.10,

    # Resultado

    "recovery": 0.10,
}


SIMILARITY_SCALES = {

    "drawdown": 0.30,

    "duration": 24.0,

    "speed": 1.00,

    "cape": 20.0,

    "pre_crash_return_3y": 1.00,

    "volatility": 0.30,

    "recovery": 60.0,
}

# Horizontes para los que Episode / ObservableEpisode almacenan
# future_return_Xy / probability_positive_Xy. Fuente unica de verdad:
# ObservableUniverse (masking por horizonte, RE-023.3) y
# EvidenceEngine (validacion de horizonte, RE-024.1) importan esto
# en vez de declarar cada uno su propia lista.

OUTCOME_HORIZONS_YEARS = (1, 3, 5, 10)

# RE-044.1 -- umbrales de la confianza categorica (Constitucion del
# Research Engine, Articulo 7: "confianza categorica Alta/Media/Baja...
# los umbrales se definiran como constantes globales del sistema").
#
# Se aplican sobre Confidence.score (models/confidence.py), un
# promedio de cuatro componentes en [0.0, 1.0]: coverage, consistency,
# diversity, stability. `stability` (ValidationEngine.stability()) es
# hoy un placeholder fijo en 1.0 -- "se implementara cuando comparemos
# versiones del motor" -- lo que garantiza un suelo de 0.25 en el
# score incluso en el peor caso (coverage=consistency=diversity=0).
# Los dos umbrales de abajo dividen el rango alcanzable [0.25, 1.0] en
# tercios iguales (ancho 0.25 cada uno): [0.25, 0.50) Baja,
# [0.50, 0.75) Media, [0.75, 1.0] Alta.
#
# Advertencia que se hereda sin resolver: mientras stability siga
# siendo un placeholder, toda lectura de Alta/Media/Baja incluye ese
# +0.25 garantizado que no es medicion real. Cuando stability se
# implemente de verdad, el suelo del rango alcanzable cambiara y estos
# umbrales deberan revisarse -- no ocurre automaticamente.
CONFIDENCE_SCORE_ALTA_THRESHOLD = 0.75
CONFIDENCE_SCORE_MEDIA_THRESHOLD = 0.50

# RE-044.2 -- Articulo 7, segunda mitad: "los umbrales se definiran
# como constantes globales del sistema. Nunca existiran numeros
# magicos distribuidos por el codigo." Estas dos constantes existian
# ya como literales sueltos, repetidos de forma independiente en
# varios archivos sin relacion declarada entre si.

# Umbral que separa "hay drawdown" (episodio candidato) de ruido de
# mercado normal. Unica fuente de verdad; antes vivia como
# `MIN_DRAWDOWN = -0.10` dentro de engine/drawdown_engine.py, que hoy
# re-exporta este mismo valor (`from core.constants import
# MIN_DRAWDOWN`) para no romper a quien ya hacia
# `from engine.drawdown_engine import MIN_DRAWDOWN`
# (engine/live_episode.py, engine/human_approval_state.py).
MIN_DRAWDOWN = -0.10

# Numero de comparables historicos que el pipeline trata como "muestra
# completa" -- usado como valor por defecto en cuatro sitios
# independientes (engine/research_pipeline.py's matches_count,
# engine/validation_harness.py's n_matches,
# engine/dimension_diagnostic.py's n, y como denominador de
# ValidationEngine.coverage()) que hasta ahora repetian el literal 10
# cada uno por su cuenta, sin relacion declarada -- coincidian por
# convencion, no por diseno explicito.
DEFAULT_MATCH_COUNT = 10

# RE-EXP.1 -- Articulo 8 (Explicabilidad). Umbrales del ExplanationEngine,
# reconectado y corregido esta iteracion (ver engine/explanation_engine.py).

# Cuantas de las siete dimensiones de similitud (core/constants.py's
# SIMILARITY_WEIGHTS) se muestran como "sostienen la analogia" y
# cuantas como "la debilitan" -- top-N / bottom-N sobre el promedio de
# cada dimension entre todos los matches. Heredado sin cambios del
# comportamiento original (3 de 7): con menos de 6 dimensiones con
# datos, los dos grupos pueden solaparse -- caso preexistente, no
# introducido por esta iteracion.
EXPLANATION_DIMENSION_SPLIT_COUNT = 3

# Tope de precedentes disidentes a listar unicamente en el caso limite
# de Evidence.median_return == 0.0 exacto (sin signo claro -- ver
# ExplanationEngine._contradicting_precedents). En los dos casos con
# signo claro (mediana positiva o negativa) se listan TODOS los
# precedentes que contradicen, sin tope -- ese criterio es binario, no
# un ranking que necesite recortarse.
EXPLANATION_MAX_CONTRADICTING_PRECEDENTS = 3
