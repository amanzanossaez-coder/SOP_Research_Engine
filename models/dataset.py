from dataclasses import dataclass
from typing import List

import pandas as pd

from models.episode import Episode


@dataclass
class Dataset:
    """
    RE-044.3 -- Dataset vuelve a ser solo estructura (Constitucion del
    Research Engine, Articulo 3: Modelos representa, Motor calcula).

    Hasta esta iteracion cargaba diez metodos propios (dos filtros,
    ocho estadisticos: medias y probabilidades de retorno a 1/3/5/10
    anios) que nunca tenian consumidor real en el pipeline -- eco de
    la etapa ProbabilityEngine, retirada por completo en RE-024.2 y
    sustituida por EvidenceEngine/Evidence, que es donde esa
    responsabilidad vive integramente hoy. Retirados, no reubicados:
    sin un consumidor real que los ejerza, moverlos a un engine nuevo
    habria sido invertir trabajo en una rama sin uso, exactamente lo
    que este proyecto evita por diseno (Articulo 9, Parsimonia).

    Si esta logica vuelve a hacer falta, se reimplementa contra la
    forma actual de Episode y con un consumidor real desde el primer
    commit -- no se resucita esta version.
    """

    data: pd.DataFrame
    episodes: List[Episode]
