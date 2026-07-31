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
