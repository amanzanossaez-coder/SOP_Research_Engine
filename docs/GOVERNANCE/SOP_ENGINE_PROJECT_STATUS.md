# SOP ENGINE PROJECT STATUS

**Version:** 2.33\
**Status:** Core Stable — Evidence Layer Aligned

------------------------------------------------------------------------

# Honest Progress Snapshot (RE-DOC-005)

Updated at the end of every work session, per Armando's standing
instruction. This is a deliberately separate axis from the rest of
this document: everywhere else records what exists and what is
verified. This table records a judgment call -- how far each block
actually is from being real, operationally usable governance, not just
correctly implemented in isolation. "Design/specification complete"
and "operationally usable today" are tracked as different numbers on
purpose; collapsing them into one blended percentage would flatter the
system's actual readiness.

As of RE-PRED.17 (2026-08-17). Nota RE-PRED.17: "Similarity Engine v2"
(citado como próximo hito) resultó tener dos problemas al verificarlo
antes de diseñar -- la premisa estaba desactualizada (duración,
velocidad, tendencia, volatilidad y ponderaciones ya existen en v1), y
la evidencia ya reunida (RE-PRED.13-16, confirmada con bootstrap de
clusters dependientes) argumenta en contra de "más dimensiones" como
siguiente paso: aislar cada dimensión no recupera la correlación de
rango positiva que sí tiene un heurístico trivial de mean-reversion.
Decisión de Armando, presentada con tres opciones: dejarlo como está.
Cero cambios de código. Nota RE-KERNEL.1: primer módulo real
del Kernel (`engine/kernel.py`), extraído de `audit_posture.py` sin
cambiar ninguna decisión -- solo los fragmentos K4/gobernanza ya
implementados (Evidence Quality, Regime Comparability, Personal
Capacity Facts, Human Approval, Dry Powder), K1/K2/K3/K5/K6 siguen sin
spec. Verificado carácter a carácter contra la salida anterior; única
diferencia real encontrada (reordenación de un print del loader, no un
cambio de contenido) investigada y documentada, no descartada sin
mirar. Nota RE-DOC-006: recap de proyecto a
petición de Armando destapó que `CONSTITUTION.md` seguía marcando el
dashboard como "pendiente" y no mencionaba el panorama histórico de
Shiller en absoluto -- corregido, ver el Design Decision de más abajo.
Cero cambios funcionales, solo sincronización de documentación con lo
que el repo ya tenía construido. Nota RE-SHILLER-DASH.8: la
sección de retornos por CAPE se había pasado de frenada respondiendo a
"no entiendo" -- cuatro párrafos antes de la tabla. Reducida a dos: qué
es el CAGR en una línea, y una conclusión corta y directa (zona
extrema -> retornos inferiores, muestra pequeña -> contexto, no señal),
en el tono exacto que pidió Armando. Cero cambios a cifras. Nota
RE-SHILLER-DASH.7: "peores
episodios con nombre" ahora se elige solo entre siglo XX-XXI (peak_date
>= 1900) -- el tercer puesto pasa de un episodio de 1872-1877 con fecha
no verificada a 2000-2002 (burbuja puntocom), bien documentado. Cero
ambigüedad de fecha en los tres nombres ahora. Nota RE-SHILLER-DASH.6: los 3
peores episodios de caída, con nombre, dentro de "Resumen de drawdowns
históricos" -- 1929 y 2008 con alta confianza, el tercero (1872-1877)
con advertencia explícita de fecha no verificada en el propio nombre.
Además, la tabla "Retornos reales posteriores según CAPE inicial" tenía
un problema real de claridad, no de familiaridad -- Armando no la
entendía porque llevaba jerga técnica antes que explicación; ahora
lleva un párrafo en llano al principio con un ejemplo concreto
(acumulado, no solo anualizado) y cabeceras reescritas. Cero cambios a
cifras subyacentes, solo presentación y explicación. Nota
RE-SHILLER-DASH.5: dos
bloques nuevos en el panel Shiller, ambos pedidos y acotados por
Armando ("añadiría solo dos bloques"): retornos reales posteriores
según CAPE inicial (5/10/15 años, mediana por bucket, con N por
bucket para que "pocos y no independientes" sea una cifra, no solo una
frase) y un resumen agregado de las 23 caídas históricas (mediana,
peor caída, duraciones). Además, ajuste de redacción en "Detalle de
indicadores": "cerca de la media" ahora aclara si el valor bruto está
por encima o por debajo cuando eso es cierto, sin tocar el criterio de
z-score compartido con el dashboard operativo. Cero cambios a
drawdown_engine.py, gates o al dashboard operativo. Nota RE-SHILLER-DASH.4: el
resumen ejecutivo del panel Shiller pasa de una frase corrida a
headline-action/headline-support + stat-strip (mismo patrón ya
aprobado para "Estado hoy"/"Evidencia histórica" en el dashboard
operativo), a petición directa de Armando ("¿de verdad esto te parece
bain o mckinsey?"). Inflación pasa a 2 decimales en todo el panel
(estaba en 1, inconsistente con Tipo). Corregidas también las
etiquetas de eje en formato inglés en las gráficas lineales. Cero
cambios a cifras o cálculos -- solo presentación. Nota RE-SHILLER-DASH.3: añadidos
semáforos (verde/gris/ámbar/rojo) a Indicadores clave y Resumen
ejecutivo -- en una escala deliberadamente distinta a la del dashboard
operativo (distancia a la media histórica, no juicio de valor) para no
implicar que "muy por encima" del CAPE es "malo". Y anotación de fecha
+ valor del último dato directamente sobre cada gráfica, no solo en el
texto. Cero cambios a cifras o cálculos. Nota RE-SHILLER-DASH.1/2: nuevo
panel `generate_shiller_dashboard.py` -> `outputs/shiller_dashboard.html`,
separado del dashboard operativo -- gráficas estáticas (matplotlib,
cero `<script>`) sobre la serie completa de Shiller (1871-2026),
reutilizando `run_drawdown_engine()` sin recalcular nada. Tras revisión
de Armando: resumen ejecutivo, franja de indicadores, percentil de
CAPE (99,0, verificado) y media a 10 años (32,4, verificado) añadidos.
Hallazgo técnico real, no buscado: el gráfico de precio usaba la
columna nominal ("P") en vez de la real ("Price") -- corregido; la
detección de episodios del Research Engine (`drawdown_engine.py`)
sigue sobre precio nominal, sin cambios, fuera de alcance de esta
iteración. Cero cambios a gates, protocolos, motores o cifras del
dashboard operativo. Nota RE-DASH.1.21: la Liquidez deja de
ser una tabla con barra de 84px y pasa a una tarjeta por patrimonio a
petición explícita de Armando ("demasiado pequeña y demasiado
escondida... el suelo y techo no se ven directamente, solo aparecen en
tooltip"), tras seis rondas puliendo esa celda sin resolverlo -- señal
de que el contenedor era el problema, no el diseño. Suelo/techo ahora
visibles como texto, no solo en hover; misma lógica de zonas, marcador
y cifra auditada de RE-DASH.1.14-1.16, sin recalcular nada. Confirmado
por Armando ("así está ok"). Nota RE-DASH.1.20: "Valor" (Datos de
mercado) era la única columna de valores que seguía alineada a la
derecha tras RE-DASH.1.18 -- Armando lo señaló en captura y, al haber
dos direcciones válidas en conflicto, se le preguntó en vez de
inferir; eligió izquierda para las tres (Valor, Human Approval,
Liquidez disponible). Cero cambios a cifras -- solo alineación de
celda. Nota RE-DASH.1.19: la alerta
"Régimen no comparable (CAPE)" era opaca para Armando -- reescrita en
lenguaje llano ("No hay episodios comparables con un CAPE tan alto."),
misma comparación ya existente, solo cambia la redacción. RE-DASH.1.18:
"Liquidez disponible" desalineada con "Human Approval" pese a compartir
ancho de columna (RE-DASH.1.17) -- se debía a que una estaba alineada a
la derecha y la otra a la izquierda; corregido. RE-DASH.1.17: las dos
tablas de "Estado por patrimonio" se auto-dimensionaban de forma
independiente y desalineaban cada columna entre sí (el "triángulo" que
Armando señaló) -- ahora comparten un esquema de anchos fijo.
RE-DASH.1.16: el marcador de la barra de liquidez quedaba medio fuera
del track en los extremos, y las zonas de color apenas se distinguían
-- corregido con marcador anclado dentro del track y marcas de límite
que no dependen del contraste de color. Cero cambios a gates,
protocolos o cifras en las cuatro -- puramente capa de presentación.
Nota RE-DASH.1.15: captura real de
Armando destapó dos fallos reales en la barra de liquidez de
RE-DASH.1.14 -- el marcador usaba una escala distinta a la de las
zonas de color y por eso se salía visualmente de la barra (confirmado
en pantallazo: "esto es un desastre a nivel de diseño"), y la cifra
mostrada ("posición vs. suelo/techo") en realidad era solo la
distancia a un único límite, ambigua tal y como estaba etiquetada.
Ambos corregidos: marcador convertido a la misma escala que las zonas,
cifra ahora nombra el límite explícitamente ("sobre techo"/"bajo
suelo"). Cero cambios a gates, protocolos o cifras -- capa de
presentación. Nota RE-DASH.1.14: la barra de
liquidez añadida en RE-DASH.1.13 gana tres zonas de color fijas
(déficit/objetivo/ocioso, rojo/verde/ámbar) sobre el propio track,
a partir de una referencia de diseño que Armando compartió
explícitamente como adaptable ("no lo tomes al pie de la letra");
suelo/techo, retirados de la vista principal en RE-DASH.1.13, vuelven
como tooltip nativo (`title`) sobre la barra -- no un control
interactivo nuevo, metadato pasivo igual que el resto del dashboard.
RE-DASH.1.13: corregido un problema real de cabeceras partiéndose en
dos líneas (confirmado con una captura de pantalla real de Armando, no
supuesto), y añadida una barra visual de posición para liquidez
(suelo/techo), mismo patrón que Armando ya validó en Datos de mercado.
RE-DASH.1.12 (documentada esta misma sesión, con retraso respecto al
código): columna Estado alineada con Postura, y un bug real de
tipografía corregido (Alertas y subtítulos heredaban el tamaño por
defecto del navegador). Cero cambios a gates, protocolos o cifras
mostradas -- puramente capa de presentación. Sigue sin tocar ningún
gate, protocolo ni motor. No altera ninguna cifra de progreso técnico
de esta tabla:

| Bloque | Avance honesto |
|---|---:|
| Research Engine core | 95% |
| Research Validation | 100% técnico / validez predictiva no demostrada |
| Evidence Quality Gate | 75-80% |
| Regime Comparability Gate | 75-80% |
| Personal Capacity definición | 90-95% |
| Personal Capacity operativo real | 45-50% |
| Gate Combination / Posture Mapper | 75-80% aislado |
| Dry Powder Protocol | 85-90% aislado (techo extraordinario del 90% vía Human Approval ya calculado por fórmula, RE-C; sigue sin wiring a run.py/DecisionEngine) |
| Dry Powder -- rastreo de episodio en vivo | 85-90% (los siete campos de DryPowderProtocolInputs computables; corregido un vacío real de silencio en postura no reconocida encontrado en revisión crítica -- RE-041.8; falta solo wiring a run.py/DecisionEngine, deliberadamente no autorizado) |
| Portfolio Reallocation | 0-5% |
| Human Approval especificación | 50% |
| Human Approval operativo real | 85-90% (demostrado end-to-end en audit_posture.py como prerrequisito independiente; autorización extraordinaria del 90% completa de punta a punta -- RE-032.10 B+C; primera atestación real cargada en ambos patrimonios 2026-08-13 -- AMS Deploy Aggressively bajo cooling-off de 14 días hasta 2026-08-27, AML Conserve vigente de inmediato al no ser subida de tolerancia respecto al suelo implícito; todavía sin wiring a run.py, deliberado) |
| Dashboard operativo (RE-DASH.1.21) | 100% del alcance actual (estático, solo lectura; liquidez como tarjeta por patrimonio, Dry Powder, Human Approval, alertas, datos de mercado); sin filtros, sin gráficos interactivos -- deliberadamente fuera de alcance salvo que un uso real lo justifique |
| Panorama histórico Shiller (RE-SHILLER-DASH.8) | 100% del alcance actual (estático, solo lectura, gráficas 1871-2026 + resumen ejecutivo, indicadores con semáforo, drawdowns históricos con episodios nombrados, retornos reales por nivel de CAPE); explícitamente no evalúa gates ni propone postura -- esa lectura sigue solo en el dashboard operativo |
| Kernel -- fragmentos existentes unificados (RE-KERNEL.1) | 100% de la extracción (K4/gobernanza ya implementados, ahora en un módulo importable, `audit_posture.py` como wrapper fino verificado idéntico); 0% de K1/K2/K3/K5/K6 -- sin spec, sin código, no es el Kernel constitucional completo |

Hoy, por primera vez, los nueve hechos verificables de un patrimonio
real (AMS) resolvieron todos a favorable -- `ADEQUATE`, cero campos sin
medir, cero rupturas. AML también tiene los nueve hechos completos, sin
ninguno pendiente, y su único bloqueo (`liquidity_adequate`) es un
hallazgo real, no un vacío de datos. Ningún campo se rellenó a ciegas:
uno de los criterios (concentración de cartera de AML) se verificó
directamente contra el archivo fuente antes de aceptar la valoración
propuesta, y esa verificación cambió la imagen ("repartido en 3
fondos" resultó ser ~91% del mismo índice bajo dos proveedores
distintos) sin cambiar la conclusión final (Armando confirmó que la
concentración en SP500 es la tesis de partida del SOP, no un fallo).

El Dry Powder Protocol (RE-041.1) tiene ahora su primer código:
módulo aislado, sin estado, con las cuatro reglas (tramo sobre pólvora
seca remanente, cadencia dual, techo por postura sobre la pólvora
inicial del episodio, ratchet) y los parámetros v1 exactos de la
especificación. Dos correcciones reales se hicieron sobre la
especificación detallada que Armando entregó -- un caso sin definir en
la lógica de ratchet/techo, y un `KeyError` real con la postura
`Blocked` que la propia rama de correción 1 hizo aflorar -- ambas
señaladas y confirmadas antes de escribir código. Sigue sin estar
conectado a `posture_mapper.py`, `gate_combination.py`, `run.py` ni a
`DecisionEngine`; sigue sin rastreo de episodio en vivo (eso sigue
siendo responsabilidad de un futuro llamador). El canal
atestiguado/Human Approval (RE-032.4) sigue sin una sola línea de
código propia -- este módulo solo lee un booleano de aprobación que
otro componente tendría que producir.

RE-041.2 detecta episodios de mercado en vivo, sin estado: reutiliza
`calculate_running_peak`/`calculate_drawdown` de `drawdown_engine.py`
(sin tocar ese archivo) para responder si hay un episodio activo hoy y
desde cuándo. Comprobado contra `data/raw/shiller.xlsx` real: a fecha
2026.07 el mercado está exactamente en su pico, sin episodio activo.
De los siete campos que pide `DryPowderProtocolInputs`, esto resuelve
dos (hay episodio / desde cuándo) de forma automática. Los otros
cinco -- pólvora seca inicial del episodio, pólvora seca remanente,
capital acumulado desplegado, y los dos campos de cadencia -- siguen
sin ninguna fuente, porque nadie salvo Armando puede observarlos.
Construir ese ledger a ciegas habría sido justo el tipo de caja negra
que este proyecto rechaza explícitamente; se le presentó la disyuntiva
antes de escribir código y confirmó una pestaña xlsx (no un JSON) como
formato, pendiente de diseñar en una próxima iteración.

------------------------------------------------------------------------

# Purpose

This document is the technical source of truth for the Research Engine.

The Research Engine is **not** the SOP itself.

Its sole responsibility is transforming historical market data into
objective, reproducible and explainable evidence.

The SOP (Sistema Operativo Patrimonial) is the product.

The Constitution and the governance protocols decide how that evidence
is used.

------------------------------------------------------------------------

# Source of Truth Declaration (RE-DOC-001)

This document is the single official source of truth for the status
of the Research Engine.

`docs/ROADMAP.md` and `docs/PROJECT_STATE.md` are **not** authoritative.
They predate this declaration, contain roadmap information that no
longer matches this document, and are marked pending consolidation.
They should not be updated as a substitute for this file. A future,
dedicated iteration will merge or retire them — not before the
Observable Universe block (RE-023.x) is stabilized.

------------------------------------------------------------------------

# Documentation History Policy (RE-DOC-002)

The changelog preserves project history. It should record what was
known, claimed or shipped at the time of each version, not silently
rewrite past entries to match later knowledge.

When a later iteration supersedes a prior metric, interpretation or
claim, the correction should be documented forward in the new version
that discovered or authorized the change. Prior changelog entries may
only be edited when they contain a dangerous factual error that would
mislead current use of the system if left unqualified.

This policy follows from RE-025.5: earlier documentation had reported
MAE=7.05%, and the pinned runtime later established MAE=7.03% as the
canonical value. The correct governance pattern is to preserve the
fact that the value changed and explain why, not make the historical
path appear cleaner than it was.

------------------------------------------------------------------------

# Governance Principles

-   The Constitution is the highest authority.
-   Engines produce evidence, never portfolio decisions.
-   The architecture is modular.
-   Every module has one responsibility.
-   Explainability is preferred over sophistication.
-   Small compatible iterations are preferred over large refactorings.

------------------------------------------------------------------------

# Current Architecture

    Raw Data
        │
    Dataset Engine
        │
    Snapshot Engine
        │
    Similarity Engine
        │
    Evidence Engine
        │
    Assessment Engine
        │
    Inference Engine
        │
    Constitution
        │
    Protocols
        │
    Dashboard

------------------------------------------------------------------------

# Execution State (as of RE-030.3)

This diagram describes the intended architecture. It does not
describe what `run.py` actually executes today. Distinguishing
"exists in the repository", "participates in the executed flow", and
"matches this diagram's named objects" is deliberate -- conflating
them is exactly the kind of drift this document exists to prevent.

## Operative flow

The only path whose end-to-end methodological consistency has been
verified:

    Dataset
        │
    SnapshotEngine
        │
    ObservableUniverse
        │
    SimilarityEngine
        │
    EvidenceEngine
        │
    DecisionEngine

## Exists, but outside the operative flow

  Component           State
  ------------------- ------------------------------------------------
  AssessmentEngine     Exists, compiles. Not called by run.py. As of
                        RE-029.3 it consumes build_research_result(),
                        the same shared Research pipeline used by
                        DecisionEngine and ResearchEngine. RE-029.4
                        verifies its public helper outputs after that
                        refactor. The temporal-safety and research
                        source-of-truth duplication concerns are
                        resolved. Confidence remains a separate
                        ValidationEngine path
                        (coverage/consistency/diversity/stability, with
                        stability hardcoded to 1.0). RE-029.5 defines
                        any future evidence-quality link to capital
                        posture as a gate / ceiling, not a weighted
                        input, and explicitly excludes the current
                        confidence score from SOP capital gates while
                        stability remains hardcoded. RE-029.6 defines
                        the initial Evidence Quality Gate dimensions and
                        records that the gate starts conservative because
                        current Research Validation does not yet show
                        reliable discriminatory power. RE-029.7 defines
                        the calibration boundary: any relaxation from
                        conservative must be pre-registered, discrete
                        and evidence-led, never inferred from the
                        aggregate confidence score. RE-029.8 defines
                        the first future implementation scope: a
                        separate EvidenceQualityGate structure, with
                        local snapshot inputs separated from global
                        model-validation state, and not wired into
                        run.py or DecisionEngine. RE-029.9 defines the
                        acceptance criteria for that first future code
                        change. RE-030.1 adds the isolated
                        EvidenceQualityGate module and verification
                        test, still outside the operative flow. RE-030.2
                        adds a local Evidence -> LocalEvidenceQualityInputs
                        adapter, also outside the operative flow.
  InferenceEngine      Exists. Its responsibility (queries over
                        episodes -- drawdowns_greater_than,
                        recovered_in_less_than) remains valid. Not part
                        of the operative flow today.
  ProbabilityEngine    Exists physically. No longer used by the
                        operative flow. Its only remaining caller is
                        AssessmentEngine, which is itself outside the
                        operative flow -- so it is, transitively,
                        unused in what actually runs.
  ExplanationEngine    Exists. References attributes that do not exist
                        on SimilarityExplanation (e.g.
                        first.event.drawdown_similarity) -- would raise
                        AttributeError if ever called. Never called
                        today.
  ResearchEngine       Exists and executes a verified research pipeline
                        facade (RE-027.2-RE-027.5). It is not called by
                        run.py yet. Produces ResearchResult by delegating
                        to the shared build_research_result() pipeline,
                        the same source of truth consumed by
                        DecisionEngine.
  EvidenceQualityGate  Exists as an isolated structure (RE-030.1). Not
                        called by run.py. Not called by DecisionEngine.
                        Not called by AssessmentEngine. Does not consume
                        AssessmentEngine.confidence().score. Separates
                        local snapshot inputs from global model-validation
                        state. RE-030.2 adds
                        build_local_evidence_quality_inputs(evidence),
                        using Evidence as the single source of truth for
                        the selected match set. Defaults fail-closed:
                        today's real local inputs plus non-validated
                        global state produce `not measurable`; fully
                        measured but not yet authorized inputs produce
                        `conservative`.
  Regime Comparability Gate
                        Planned / documented boundary only (RE-031.1).
                        No code exists. Not called by run.py,
                        DecisionEngine, AssessmentEngine or
                        EvidenceQualityGate. Intended to cap capital
                        posture when today's market regime is not
                        structurally comparable to the historical
                        evidence being used.
  Personal Capacity     Classified in RE-032.2 as a mixed control --
  Boundary              Armando's explicit decision, not inferred.
                        RE-032.3 enumerates the nine verifiable-facts
                        categories; RE-032.4 defines the attested-
                        judgement channel and the Human Approval
                        procedural boundary. RE-032.5 adds the first
                        isolated code for the verifiable-facts half:
                        engine/personal_capacity_facts_gate.py. Not
                        called by run.py, DecisionEngine, AssessmentEngine
                        or any other gate -- isolated, same as
                        EvidenceQualityGate and RegimeComparabilityGate
                        were before their respective posture-mapper
                        integrations. No real-pipeline data source
                        exists for any of the nine facts -- all live
                        outside the Research Engine, so only synthetic
                        verification is possible. Verifiable-facts
                        channel (liquidity, debt service, concentration,
                        etc.) is the future computable-gate half --
                        participates in gate combination via min(), same
                        ceiling-only pattern as Evidence Quality and
                        Regime Comparability. Attested-judgement channel
                        (drawdown tolerance, psychological capacity,
                        etc.) is the Human Approval half -- never enters
                        gate-combination math, never an automatic
                        ceiling. RE-032.1's two-channel separation is
                        preserved by construction, not merged into one
                        score.
  Capital Posture       Vocabulary documented only (RE-033.1). No code
                        exists. No posture engine exists. No gate
                        combination logic exists. RE-033.1 defines the
                        ordered posture vocabulary that future gates may
                        cap. RE-034.1 documents the combination boundary:
                        `Blocked` first, then the most restrictive
                        posture ceiling, with Evidence Quality not
                        measurable treated differently from unavailable
                        Regime Comparability / Personal Capacity.
                        RE-034.2 defines first-code acceptance criteria
                        for that future combination layer. RE-034.3
                        adds the isolated gate-combination module and
                        verification test. RE-034.4 documents that it
                        exists and passes verification, but remains
                        outside the operative flow. RE-PRED.1 opens the
                        predictive-validity boundary: no new validation
                        claim is made until target, model freeze,
                        baselines, holdout policy and live-tracking
                        protocol are defined. RE-PRED.2 audits the
                        current predictive target implemented by code.
                        RE-PRED.3 defines the provisional target-freeze
                        boundary while leaving source-column semantics
                        not fully verified. RE-PRED.4 verifies that
                        Shiller `Price.1` is Real Total Return Price.
                        RE-PRED.5 defines ordered acceptance criteria
                        for any future definitive target freeze.
  Research Validation  Exists (RE-025.1-RE-026.1.2), fully independent of
  Harness               run.py -- invoked manually, no wiring exists or
                        is planned yet. Deliberately offline: for each
                        historical episode it replays DecisionEngine's
                        own methodology -- ObservableUniverse(as_of=
                        episode.bottom_date) for comparables,
                        SimilarityEngine.top() for matches,
                        EvidenceEngine.build() for the forecast -- so it
                        validates the system that actually runs, not a
                        hypothetical one. Self-exclusion of the episode
                        under evaluation is by bottom_index, never by
                        object identity (ObservableUniverse.episodes()
                        returns ObservableEpisode, a type deliberately
                        distinct from Episode -- RE-023.1/ADR-004 --
                        so `is not` would never have excluded anything).
                        Unrelated to ValidationEngine above despite the
                        similar name -- see Component Status.
  Predictive Validity  Boundary opened in RE-PRED.1. Documentation
  Boundary              only. No code. No new calculation. No validation
                        claim. Defines what future predictive validation
                        must specify before any holdout, live tracking
                        or gate relaxation can be treated as evidence.
                        RE-PRED.2 audits the current target: annualized
                        5-year CAGR from `Price.1`, used as both
                        Evidence forecast surface and Research
                        Validation actual. RE-PRED.3 treats that target
                        as the provisional freeze candidate, but does
                        not verify whether `Price.1` is real / nominal
                        or price / total-return. RE-PRED.4 verifies
                        `Price.1` as Real Total Return Price from the
                        source workbook header. RE-PRED.5 records that
                        source-column semantics are verified, but
                        bottom-detection semantics are not yet audited.
                        RE-PRED.6 audits bottom detection and episode
                        boundaries, and records two verified findings:
                        price-basis asymmetry and date-arithmetic
                        duration bug. RE-BUG.1 promotes the duration
                        bug to near-term code-fix priority and defines
                        acceptance criteria. RE-BUG.2 fixes calendar-
                        month duration arithmetic. RE-BUG.3 documents
                        the downstream impact and canonical post-fix
                        metrics. RE-DATA.1 records future Shiller data
                        update automation as a validated-data pipeline,
                        not a blind download. RE-PRED.7 defines the
                        absolute-vs-excess-return boundary: absolute
                        return is the existing descriptive Evidence
                        surface, unchanged; excess return over a
                        primary naive baseline is the future predictive-
                        validity surface, to be implemented in the
                        Research Validation Harness, not in Evidence.
                        RE-PRED.8 defines acceptance criteria for that
                        primary baseline: a point-in-time expanding
                        median of `future_return_5y`, reusing
                        `ObservableUniverse` and bottom_index
                        self-exclusion, evaluated over the same
                        evaluable records already used by the model.
                        It also corrects RE-PRED.7's rank-correlation
                        claim forward: because this baseline varies per
                        episode, it does have rank variation, and its
                        rank correlation is a real, computable
                        comparison against the model's. RE-PRED.9
                        implements that baseline in code:
                        `engine/baseline_harness.py` and
                        `tests/verify_baseline_harness.py`. RE-PRED.10
                        records the canonical baseline values, confirmed
                        under the pinned runtime, and the resulting
                        finding: the model does not beat the primary
                        baseline on any of the three canonical metrics --
                        it ties on directional hit-rate and loses on MAE
                        and rank correlation. Predictive validity is not
                        demonstrated relative to this baseline. RE-PRED.11
                        implements two secondary baselines (zero,
                        mean-reversion) to isolate whether that finding
                        is an artifact of the primary baseline choice --
                        results pending pinned-runtime confirmation.
                        RE-PRED.12 records, as an explicit open question,
                        that no baseline comparison on this evaluated
                        sample addresses whether any excess value is
                        distinguishable from sampling noise given N=19
                        dependent records. RE-PRED.13 records the
                        canonical secondary-baseline values, confirmed
                        under the pinned runtime, and the resulting
                        full-picture finding: the model is not uniformly
                        dominated -- it clearly beats zero and
                        mean-reversion on MAE, ties both on hit-rate, but
                        loses to mean-reversion on rank correlation by a
                        full sign flip. The RE-PRED.10.1 deferral trigger
                        was evaluated explicitly and did not activate.
                        RE-PRED.14 tests the signal-dilution hypothesis
                        registered in RE-PRED.13 by isolating each active
                        SimilarityEngine dimension and does not find
                        support for it: every dimension in isolation
                        remains negative on rank correlation, none close
                        to mean-reversion's positive value. A revised,
                        still-unauthorized hypothesis is registered:
                        nearest-neighbor selection may not preserve
                        monotonic rank order the way a direct function of
                        the query's own value does, regardless of which
                        single dimension drives the selection. RE-PRED.15
                        closes the RE-PRED.12 method gap:
                        `engine/dependence_bootstrap.py` implements a
                        cluster bootstrap over independence clusters built
                        from the union of the RE-025.8 overlapping-outcome-
                        window and RE-025.9 repeated-forecast-group
                        diagnostics, producing dependence-aware confidence
                        intervals for the model, the primary and mean-
                        reversion baselines, and their paired excess --
                        structurally verified outside the pinned runtime
                        only. RE-PRED.16 records the canonical results,
                        confirmed under the pinned runtime: 3 independence
                        clusters (sizes 10, 8, 1), not the 4 seen in the
                        unpinned structural smoke test -- hand-verified
                        against the already-canonical RE-025.8/RE-025.9
                        tables, confirming the pinned result and not the
                        sandbox one. The excess vs. primary baseline on
                        rank correlation is not distinguishable from
                        sampling noise (90% interval [-0.06068, 0.02514],
                        straddles zero); the excess vs. mean-reversion on
                        rank correlation is robust and does not straddle
                        zero (90% interval [-0.94270, -0.34208]) -- the
                        RE-PRED.13 full sign-flip finding survives
                        dependence-aware resampling, the primary-baseline
                        loss does not.

## Matches the diagram's named objects: ResearchEngine aligned

The architecture above names `ResearchEngine` producing a
`ResearchResult`. RE-027.1 verified that the prior object was stale and
dangerous to patch in isolation. RE-027.2-RE-027.4 rebuild and verify
that named object. RE-027.5 then removes the remaining duplication by
extracting the shared research pipeline into one source of truth:

    build_research_result(dataset)
        │
    SnapshotEngine(dataset).latest()
        │
    ObservableUniverse(dataset, as_of=snapshot.date)
        │
    SimilarityEngine(universe.episodes()).top(snapshot, n=10)
        │
    EvidenceEngine().build(matches, years=5)
        │
    ResearchResult

Both `ResearchEngine` and `DecisionEngine` consume
`build_research_result()`. This resolves the RE-027.1 design risk: the
same research pipeline no longer exists as two independent
implementations that could drift apart.

Verified result from `tests/verify_research_engine.py` after RE-027.5:

-   `RESEARCH ENGINE : STABLE`
-   `snapshot_date: 2026.07`
-   `matches: 10`
-   `horizon_years: 5`
-   `median_return: 0.11386676352177`
-   `worst_return: -0.01091948933253`
-   `best_return: 0.13767334934864`
-   `return_count: 9`
-   `positive_count: 8`
-   `negative_count: 1`
-   `zero_count: 0`
-   `non_positive_probability: 0.11111111111111`
-   `return_spread: 0.14859283868117`

Remaining execution-state gap: `run.py` still calls `DecisionEngine`
directly. This no longer creates a duplicated research pipeline:
`DecisionEngine` and `ResearchEngine` share the same underlying
`build_research_result()` source of truth. Wiring the CLI entry point
through `ResearchEngine` remains a later integration choice, not an
unresolved defect in the RE-027 rebuild.

## Other known-broken, disconnected code

`core/dataset_builder.py` builds `Episode` with fields (`date`,
`price`, `dividend_yield`, `earnings`, `cpi`, `gs10`) that do not
exist on the current `Episode`, and calls `Dataset(episodes)` with
one positional argument where two are required. Never executed by
anything in the operative flow.

------------------------------------------------------------------------

# Core Maturity Declaration

Starting with **version 1.0**, the Core architecture is considered
**stable**.

The following components are frozen as part of the Core:

-   Dataset Engine
-   Snapshot Engine
-   Drawdown calculations
-   Similarity Engine
-   Probability calculations
-   Normalization framework
-   Core domain models

Changes to these components should only occur when:

-   a functional defect exists,
-   objective evidence demonstrates incorrect behaviour,
-   or a governance decision explicitly authorizes the modification.

The primary effort of the project now shifts away from infrastructure
and towards functional capabilities:

1.  Evidence generation.
2.  Market assessment.
3.  Evidence-based inference.
4.  Executable constitutional rules.
5.  Portfolio governance protocols.

This declaration marks the end of the infrastructure phase and the
beginning of the functional phase of the Sistema Operativo Patrimonial.

------------------------------------------------------------------------

# Frozen Core Policy

The Core should remain stable.

Infrastructure refactoring must never be performed simply because a
cleaner design is possible.

Changes require objective justification.

## Exceptions invoked

-   **RE-021.** Similarity Engine (frozen) was modified to remove
    `recovery` (an Outcome variable) from the global similarity
    score. Justification: objective evidence of a data-leakage
    defect — Outcome participating in episode selection biased the
    resulting evidence. Authorized under "a functional defect
    exists."

RE-025.1-RE-026.1.2 invoke no exception: the Research Validation
Harness consumes `ObservableUniverse`, `SimilarityEngine` and
`EvidenceEngine` exactly as published, through their existing public
interfaces. RE-027.1 is documentation-only audit work, and
RE-027.2-RE-027.5 rebuild `ResearchResult` / `ResearchEngine`, add
smoke tests, and extract the shared research pipeline around the same
published Snapshot, Observable Universe, Similarity and Evidence
surfaces. No frozen component was modified to build Research
Validation, to verify its canonical metrics, or to close the
`ResearchEngine` gap. RE-028.1 is documentation-only scope work for a
future Evidence Engine v2. RE-028.2 implements that Evidence v2 as an
additive Evidence-layer change, not a frozen Core modification.
RE-029.1 and RE-029.2 are documentation-only Assessment / SOP
governance scope audits. RE-029.3 refactors `AssessmentEngine` to
consume the shared Research pipeline without modifying frozen Core
components. RE-029.4 adds verification for the public Assessment helper
surface. RE-029.5, RE-029.6, RE-029.7, RE-029.8 and RE-029.9 are
documentation-only governance iterations: no frozen component changes
are invoked. RE-030.1 adds a new isolated gate module and focused test,
without modifying Frozen Core or operative wiring. RE-030.2 extends that
isolated module with a local input adapter; Frozen Core and operative
wiring remain unchanged. RE-031.1 is documentation-only scope work for
the Regime Comparability Gate. RE-032.1 is documentation-only
classification work for Personal Capacity. RE-033.1 is
documentation-only vocabulary work for Capital Posture. RE-034.1 is
documentation-only gate-combination boundary work.

------------------------------------------------------------------------

# Component Status

  Component                    Status
  ---------------------------- ------------------------------------
  Dataset Engine               Stable
  Snapshot Engine               Stable
  Similarity Engine             Stable (RE-021 exception — see Frozen Core Policy)
  Observable Universe           Stable in operative flow (wired through DecisionEngine, RE-023.5; AssessmentEngine wired in RE-024.3)
  Evidence Engine                v2 — additive descriptive sample-shape
                                  fields added in RE-028.2. Existing
                                  v1 fields and semantics preserved.
  Research Engine                v1 — rebuilt facade over the shared verified research pipeline (RE-027.2-RE-027.5). Produces ResearchResult. Smoke-tested. Not called by run.py yet.
  Assessment Engine              v1 — consumes the shared Research
                                  pipeline as of RE-029.3. Public
                                  helpers smoke-tested in RE-029.4. Not
                                  called by run.py. RE-029.6 defines
                                  Evidence Quality as a governance gate
                                  composed of objective dimensions, but
                                  no executable thresholds yet.
                                  RE-029.7 documents the calibration
                                  boundary for moving beyond the initial
                                  conservative gate state.
                                  RE-029.8 documents the future
                                  implementation scope without changing
                                  code.
                                  RE-029.9 documents acceptance criteria
                                  for the first isolated gate PR.
                                  Remaining issue is confidence
                                  calibration/boundary, not temporal
                                  leakage or Research pipeline
                                  duplication.
  Evidence Quality Gate          v0 — isolated structure added in
                                  RE-030.1. Compiles and has focused
                                  verification. RE-030.2 adds local
                                  Evidence input adapter. Not wired into run.py,
                                  DecisionEngine, AssessmentEngine or
                                  ValidationEngine. No thresholds, no
                                  capital posture mapping and no
                                  operative authority. RE-035.1 closes
                                  both remaining stub inputs:
                                  independence_dispersion_measured is no
                                  longer hardcoded False -- it is computed
                                  from real pairwise outcome-window overlap
                                  across the current match set (same
                                  definition as RE-025.8, applied to a live
                                  query instead of the offline validation
                                  harness). predictive_validation_status
                                  gains a recognized "not demonstrated"
                                  value with a sharper explanation, per the
                                  RE-PRED.10.1 decision not to add a new
                                  top-level gate state. Still not wired
                                  into any operative flow. Still no
                                  thresholds and no capital posture
                                  mapping -- RE-034.1's provisional mapping
                                  remains documentation-only.
  Regime Comparability Gate      Boundary documented in RE-031.1.
                                  RE-036.1 adds the first isolated
                                  implementation:
                                  `engine/regime_comparability_gate.py`.
                                  Three dimensions active (cape,
                                  inflation, interest_rate) -- already
                                  populated in `Context` per episode and
                                  unused by `SimilarityEngine`'s score, so
                                  no new data ingestion was needed.
                                  Strict [min, max] coverage check against
                                  the current match set only (local, not
                                  global), no percentile or margin --
                                  deliberate choice to defer that question
                                  until an actual outlier problem is
                                  observed. Volatility / liquidity /
                                  policy / market-structure dimensions
                                  remain explicitly not measurable -- no
                                  data source exists for them. Still not
                                  wired into run.py, DecisionEngine,
                                  EvidenceQualityGate or
                                  gate_combination. RE-034.1's posture
                                  mapping has no entry yet for this gate's
                                  real states -- that remains a separate,
                                  future governance decision, not a
                                  consequence of this code existing.
                                  Correction to RE-036.1 (RE-DOC-002):
                                  that iteration claimed `inflation`/
                                  `interest_rate` were "already populated
                                  in Context per episode" -- false, both
                                  were hardcoded `None` for every episode
                                  and for today's snapshot's
                                  `interest_rate`. RE-037.1's real
                                  audit dry-run exposed this (both
                                  dimensions read `not measurable`).
                                  RE-038.1 wires both for real, and
                                  additionally corrects `inflation` from
                                  a raw CPI index level (near-monotonic
                                  over a century, would make coverage
                                  fail almost tautologically) to a
                                  trailing 12-month rate
                                  (`InflationRate1Y`).
  Personal Capacity Boundary     Classification boundary documented in
                                  RE-032.1. RE-032.2 resolves the primary
                                  classification question: mixed control,
                                  Armando's explicit decision. RE-032.3
                                  enumerates the nine verifiable-facts
                                  categories (liquidity, near-term cash
                                  needs, fixed obligations, debt service,
                                  income concentration, portfolio
                                  concentration, required emergency
                                  reserve, known time horizon
                                  constraints, fiscal/operational
                                  constraints), each with an operational
                                  definition and a source classification
                                  (all currently manual entry / outside
                                  the Research Engine, some computable if
                                  a position/vehicle ledger existed).
                                  Still no code, no thresholds, no
                                  capital posture mapping implemented --
                                  enumeration is not implementation.
                                  Verifiable facts -> future computable
                                  gate, combined via min() like Evidence
                                  Quality/Regime Comparability. Attested
                                  judgement -> Human Approval
                                  prerequisite, outside gate-combination
                                  math entirely. This also answers one of
                                  RE-032.1's open
                                  questions directly: Personal Capacity
                                  participates in gate combination AND
                                  sits inside Human Approval -- split by
                                  channel, not either/or. RE-032.4 defines
                                  the attested-judgement channel's five
                                  categories and the Human Approval
                                  procedural boundary in full: binary
                                  veto (not min()), 90-day fixed validity,
                                  a universal 14-day cooling-off on any
                                  tolerance-increasing revision (not
                                  contingent on crisis detection),
                                  extended to 30 days when market_crisis
                                  (objective, Drawdown <= MIN_DRAWDOWN) or
                                  personal_crisis (self-declared,
                                  explicitly documented as a weaker,
                                  asymmetric signal) is active. Tolerance-
                                  reducing revisions apply immediately,
                                  always. Still no code, no storage
                                  schema, no wiring. RE-032.5 adds the
                                  first isolated code for the
                                  verifiable-facts half:
                                  `engine/personal_capacity_facts_gate.py`.
                                  Nine `Optional[bool]` local inputs,
                                  uniform positive polarity. Three
                                  states -- `constrained` if any fact
                                  confirms a breach, `adequate` only if
                                  all nine are confirmed, `not
                                  measurable` otherwise (missing data is
                                  never favorable). Emergency reserve
                                  breach additionally sets an orthogonal
                                  `blocked` flag, reusing
                                  `GateCombinationInput.blocked`
                                  (RE-034.3) -- resolves RE-032.3's open
                                  question about its binary-vs-graded
                                  treatment: both, not either/or, same
                                  pattern as Personal Capacity's own
                                  channel split. Provisional, stated as
                                  such: only emergency reserve produces
                                  a hard block in this iteration: other
                                  failed facts only constrain. No
                                  real-pipeline data source exists for
                                  any of the nine facts -- synthetic
                                  verification only. Not wired into
                                  posture_mapper.py or
                                  gate_combination.py -- integration is
                                  RE-040.x, still open.
  Capital Posture Vocabulary     Documented in RE-033.1. No code. No
                                  posture engine. No gate combination
                                  implementation. `Blocked` is documented
                                  as an orthogonal veto. RE-041.1 fills
                                  in RE-033.1's two explicitly deferred
                                  numbers -- `Deploy Partially`'s bounded
                                  fraction and `Deploy Aggressively`'s
                                  maximum amount -- with a full Dry
                                  Powder Protocol specification.
                                  Documentation-only, no code, no
                                  operative wiring. `Conserve`/`Prepare`/
                                  `Blocked` remain 0% deployment,
                                  unchanged from RE-033.1. Mechanism:
                                  tranches sized as a fraction of
                                  remaining Dry Powder (not initial
                                  capital), gated by a dual cadence
                                  (minimum days OR additional drawdown
                                  points since the last tranche, reusing
                                  the same `Drawdown` field already used
                                  by `market_crisis` in RE-032.4), capped
                                  by a per-posture cumulative ceiling
                                  that acts only as a backstop for
                                  extreme, prolonged scenarios -- not the
                                  everyday control, which remains the
                                  tranche+cadence mechanism. A ratchet
                                  rule prevents refilling the cumulative
                                  ceiling by oscillating between
                                  postures; only a new episode (full
                                  recovery to a new peak, same definition
                                  already used by `drawdown_engine.py`)
                                  resets it. Going beyond the
                                  `Deploy Aggressively` ceiling requires
                                  a fresh Human Approval attestation
                                  (RE-032.4) -- reuses that existing
                                  mechanism rather than inventing a new
                                  one. Explicitly noted: under today's
                                  real Evidence Quality state
                                  (`not measurable`), this protocol
                                  cannot trigger regardless of drawdown
                                  depth -- built for when evidence
                                  quality is validated, not for
                                  immediate effect.
  Gate Combination Layer         v0 — isolated structure added in
                                  RE-034.3. `engine/gate_combination.py`
                                  exists and is verified by
                                  `tests/verify_gate_combination.py`.
                                  Not wired into run.py, DecisionEngine,
                                  AssessmentEngine or ValidationEngine.
                                  No posture engine. No thresholds. No
                                  protocol rules. No operative authority.
                                  RE-034.5 extends RE-034.1's provisional
                                  ceiling-mapping table with Regime
                                  Comparability's three real states from
                                  RE-036.1: `not comparable` -> `Conserve`;
                                  `comparable` -> `Deploy Aggressively`
                                  (the top of the ordered scale, so this
                                  gate can never itself be the binding
                                  constraint when satisfied -- the actual
                                  ceiling comes from Evidence Quality or
                                  Personal Capacity). Documentation-only;
                                  no code implements this mapping yet.
                                  RE-037.1 implements that mapping in code
                                  for the first time:
                                  `engine/posture_mapper.py` translates
                                  `EvidenceQualityGateResult` and
                                  `RegimeComparabilityGateResult` into
                                  `GateCombinationInput` per RE-034.1/
                                  RE-034.5's tables, and
                                  `evaluate_capital_posture()` combines
                                  the two real gates that exist today via
                                  `combine_gate_outputs()`, unmodified.
                                  Personal Capacity explicitly excluded --
                                  not classified (RE-032.1), no gate
                                  exists -- so this combined posture is
                                  provably optimistic relative to a full
                                  combination, and that gap is stated in
                                  the module, not hidden. Still not wired
                                  into run.py or DecisionEngine; this is
                                  an isolated, read-only composition layer
                                  for audit/dry-run, not the future
                                  Capital Posture Engine. RE-038.1 wires
                                  the previously-stubbed inflation/
                                  interest_rate data this layer depends
                                  on, confirmed under pinned runtime:
                                  cape_covered=False,
                                  inflation_covered=True,
                                  interest_rate_covered=True, state
                                  `not comparable`. RE-039.1 extracts
                                  this same audit dry-run into a
                                  standalone root-level script,
                                  `audit_posture.py`, mirroring run.py's
                                  precedent -- no logic change, just a
                                  way to run the check without the full
                                  test suite. RE-040.1 extends
                                  `posture_mapper.py` with a third,
                                  optional translator:
                                  `personal_capacity_facts_to_gate_input()`,
                                  per this document's new table
                                  (`not measurable`/`constrained` ->
                                  `Conserve`, `adequate` -> `Deploy
                                  Aggressively`). `evaluate_capital_
                                  posture()` gains an optional third
                                  parameter, default `None` -- when
                                  omitted, behaves exactly as before,
                                  no ghost gate. `blocked` propagates
                                  directly from the facts gate's own
                                  emergency-reserve veto (RE-032.5) into
                                  `combine_gate_outputs()`'s existing
                                  `Blocked` short-circuit -- first real
                                  exercise of that mechanism by any
                                  gate. The combined result remains, by
                                  construction, optimistic even when
                                  this third gate is supplied: the
                                  attested-judgement/Human Approval
                                  channel (RE-032.4) has no code and is
                                  never included. `audit_posture.py` and
                                  the real-pipeline dry-run in
                                  `tests/verify_posture_mapper.py` are
                                  intentionally left at two gates -- no
                                  real data source exists for any of the
                                  nine facts, so there is nothing honest
                                  to feed the third input there.
  Predictive Validity Boundary   Opened in RE-PRED.1. Documentation
                                  only. No code. No new calculations.
                                  No predictive-validity claim. Defines
                                  the future validation contract: target
                                  audit, model freeze, baselines,
                                  holdout policy, uncertainty treatment
                                  and live tracking. RE-PRED.2 audits
                                  the current implemented target.
                                  RE-PRED.3 defines the target-freeze
                                  decision boundary and provisional
                                  freeze candidate. RE-PRED.4 verifies
                                  `Price.1` source-column semantics.
                                  RE-PRED.5 defines target-freeze
                                  acceptance criteria. RE-PRED.6 audits
                                  bottom detection / episode boundaries
                                  and records a verified duration
                                  arithmetic bug affecting Evidence
                                  recovery statistics. RE-BUG.1 defines
                                  acceptance criteria for the future fix.
                                  RE-BUG.2 fixes the bug in code.
                                  RE-BUG.3 records the post-fix canonical
                                  metrics and match set. RE-PRED.7 defines
                                  the absolute-vs-excess-return boundary:
                                  absolute return remains the existing
                                  Evidence descriptive surface; excess
                                  return over a primary naive baseline
                                  becomes the future predictive-validity
                                  surface, computed in the Research
                                  Validation Harness. No baseline value is
                                  computed yet. RE-PRED.8 defines
                                  acceptance criteria for that primary
                                  baseline as a point-in-time expanding
                                  median of `future_return_5y`, reusing
                                  `ObservableUniverse` and bottom_index
                                  self-exclusion, evaluated over the same
                                  evaluable records already used by the
                                  model. It corrects RE-PRED.7 forward:
                                  because this baseline varies per
                                  episode, its rank correlation is a real,
                                  computable comparison, not an undefined
                                  quantity. Still no code and no computed
                                  value. RE-PRED.9 implements the
                                  baseline in code
                                  (`engine/baseline_harness.py`,
                                  `tests/verify_baseline_harness.py`),
                                  reusing `ObservableUniverse` and the
                                  existing MAE / hit-rate / rank
                                  correlation functions unmodified.
                                  Structurally verified (record
                                  alignment, the no-missing-forecast
                                  invariant) outside the pinned runtime
                                  only. RE-PRED.10 records the canonical
                                  baseline values, confirmed under
                                  `RUNTIME : PINNED`: baseline MAE
                                  0.06740858559979 vs model MAE
                                  0.06928793787076 (baseline wins);
                                  baseline hit-rate 0.94736842105263,
                                  identical to the model (tie); baseline
                                  rank correlation -0.23171864780822 vs
                                  model -0.26505171850685 (baseline
                                  wins). The model does not beat the
                                  primary baseline on any of the three
                                  canonical metrics. Predictive validity
                                  is not demonstrated relative to this
                                  baseline. A proposal to formalize a
                                  `NOT_DEMONSTRATED` gate state was
                                  raised and deliberately deferred: it
                                  would rest on one baseline over a
                                  non-independent N=19 sample, and today
                                  it would not change the resulting
                                  posture ceiling (still `Conserve`,
                                  `Prepare` allowed) versus the existing
                                  `not measurable` state. RE-PRED.11
                                  implements two secondary baselines
                                  (zero, mean-reversion) to test whether
                                  the finding is an artifact of the
                                  primary baseline choice, structurally
                                  verified outside the pinned runtime
                                  only. RE-PRED.12 records that
                                  baseline-choice robustness and
                                  sampling-noise robustness are different
                                  questions -- secondary baselines answer
                                  the first, not the second. The
                                  gate-state decision is deferred until
                                  the full three-baseline picture is
                                  confirmed under the pinned runtime.
                                  RE-PRED.13 records that picture,
                                  confirmed: model MAE 0.06929 beats zero
                                  0.12749 and mean-reversion 0.18159
                                  clearly; hit-rate ties all three at
                                  0.94737; rank correlation is where the
                                  model loses -- primary baseline
                                  -0.23172 and mean-reversion +0.26316
                                  both beat the model's -0.26505, the
                                  mean-reversion case a full sign flip.
                                  The RE-PRED.10.1 trigger ("loses to the
                                  full set on a majority of metrics") is
                                  evaluated explicitly and does not
                                  activate -- the model wins MAE against
                                  two of three baselines. `NOT_DEMONSTRATED`
                                  remains deferred. A working hypothesis
                                  is registered, not authorized as fact:
                                  drawdown depth alone may order future
                                  returns better than SimilarityEngine's
                                  multidimensional conditioning, possibly
                                  through signal dilution across
                                  dimensions -- flagged for future
                                  investigation, no SimilarityEngine
                                  change made or authorized. RE-PRED.14
                                  tests that hypothesis, confirmed under
                                  the pinned runtime: no single active
                                  dimension (drawdown -0.19692, duration
                                  -0.24916, speed -0.20327, cape -0.21701,
                                  pre_crash_return_3y -0.26353,
                                  volatility -0.23414) reproduces
                                  mean-reversion's +0.26316 rank
                                  correlation. Signal dilution is not
                                  supported as the explanation. A revised
                                  hypothesis is registered, not
                                  authorized: the gap may be structural
                                  (nearest-neighbor selection vs. a
                                  direct monotonic function), not a
                                  weighting problem. RE-PRED.15
                                  implements a dependence-aware cluster
                                  bootstrap (engine/dependence_bootstrap.py)
                                  answering RE-PRED.12: independence
                                  clusters from the union of RE-025.8 and
                                  RE-025.9, resampled at cluster level,
                                  producing percentile confidence
                                  intervals for the model, both baselines
                                  and their paired excess. RE-PRED.16
                                  records the canonical results, confirmed
                                  under the pinned runtime: 3 independence
                                  clusters, sizes 10/8/1 (not the 4 seen in
                                  the unpinned smoke test -- hand-verified
                                  against RE-025.8/RE-025.9's own canonical
                                  tables, confirming the pinned count).
                                  MAE excess vs. primary baseline is small
                                  but robust (90% CI [-0.00356, -0.00045],
                                  model loses, does not straddle zero); MAE
                                  excess vs. mean-reversion is large and
                                  robust (90% CI [0.08355, 0.14025], model
                                  wins). Hit-rate excess is exactly zero at
                                  every percentile against both baselines
                                  -- the tie holds under resampling, not
                                  just at the point estimate. Rank
                                  correlation excess vs. primary baseline
                                  straddles zero (90% CI [-0.06068,
                                  0.02514]) -- RE-PRED.13's "model loses to
                                  primary on rank correlation" finding is
                                  not distinguishable from sampling noise
                                  given this dependence structure. Rank
                                  correlation excess vs. mean-reversion
                                  does not straddle zero (90% CI [-0.94270,
                                  -0.34208]) -- the full sign-flip finding
                                  is robust, not an artifact of N=19's
                                  dependence.
  Data Update Automation         Planned. RE-DATA.1 records future
                                  Shiller source refresh policy:
                                  downloadable source may be automated
                                  later, but only through validation,
                                  backup, tests and explicit logging.
                                  No downloader exists. Current updates
                                  remain manual.
  Inference Engine               Planned
  Constitution                   Planned
  Protocol Engine                Planned
  Dashboard                      Planned
  Research Validation Harness    v1 — harness + MAE + directional hit-rate + rank correlation + pinned runtime dependencies + effective-N caveat + overlapping outcome window diagnostic + repeated forecast diagnostic + synthesis + functional smoke test (RE-025.1-RE-026.1.2). Offline only, not wired into run.py.

**Note — naming collision, not a duplication of function.**
`ValidationEngine` (`engine/validation_engine.py`) and the Research
Validation Harness (`engine/validation_harness.py` +
`engine/validation_metrics.py`) are two unrelated components that
happen to share a name fragment:

-   `ValidationEngine` scores the *confidence* of a single, present-day
    decision (coverage/consistency/diversity/stability), and feeds
    `AssessmentEngine.confidence()` -- itself outside the operative
    flow (see Execution State).
-   The Research Validation Harness backtests the *historical accuracy*
    of the Similarity/Evidence pipeline itself, across all past
    episodes, offline. It does not compute confidence and is not
    consumed by `AssessmentEngine` or `DecisionEngine`.

Do not conflate the two when reading the codebase or this document.

------------------------------------------------------------------------

# Evidence Definition

Evidence must always contain three dimensions.

## Evidence

Objective historical statistics.

Examples:

-   mean outcome
-   median outcome
-   probability
-   recovery time
-   dispersion

## Confidence

How trustworthy the evidence is.

Examples:

-   sample size
-   similarity quality
-   consistency

## Quality

Quality of the historical dataset.

Examples:

-   missing data
-   structural breaks
-   outliers
-   coverage

------------------------------------------------------------------------

# Design Decisions

## RE-001

Future performance is measured using CAGR.

## RE-002

Evidence uses `future_return_5y`.

## RE-003

Assessment separates:

-   Market Position
-   Valuation Zone
-   Volatility Regime

## RE-004

Similarity excludes recent historical episodes by default.

## RE-005

Confidence is part of the Evidence object.

No standalone Confidence Engine will exist.

## RE-021

Outcome (`recovery`) removed from the global similarity score in
`SimilarityEngine`. Recovery remains under Outcome, descriptive only
— it must never influence which episodes are selected as matches.
See Frozen Core Policy exception above.

## RE-022

`SimilarityEngine.__init__` accepts an optional `cape_metric`
parameter, so a calibration built from observable episodes only can
be injected instead of recalculating over the full canonical
Dataset. Not yet wired to any caller.

## RE-023.1 — ObservableEpisode

New, independent type (does not inherit from `Episode`) representing
an episode as it could be observed at a given instant. Deliberately
not a subtype of `Episode`, to make it impossible for a canonical
and an observable episode to be substituted for one another by
accident.

## RE-023.2 — ObservableUniverse (skeleton)

`ObservableUniverse(dataset, as_of)` introduced. `episodes()` is an
identity transformation at this stage — validates the plumbing
before any temporal rule is added. Internally stores a copy of
`dataset.data` already filtered to `as_of`, never a reference to the
full canonical Dataset, so future methods cannot forget to filter it.

## RE-023.3 — Temporal masking of Outcome

`ObservableUniverse` masks Outcome fields (`recovery_*`,
`future_return_Xy`, `probability_positive_Xy`) to `None` when they
would not yet be observable at `as_of`, evaluated per field/horizon
— not per episode. Event and Context are never masked.

## RE-023.4 — Temporal existence of episodes

`ObservableUniverse.episodes()` now excludes episodes whose
`bottom_date > as_of` entirely. Cutoff uses `bottom_date`, not
`peak_date`: Event/Context are only fixed once the bottom is
reached. This does not yet replace the `peak_date`-based filter in
`SimilarityEngine.top()` — that removal is scoped for RE-023.6,
after wiring (RE-023.5) exists.

## RE-023.5 — Wiring: DecisionEngine consumes ObservableUniverse

`DecisionEngine` builds `ObservableUniverse(dataset, as_of=snapshot.date)`
and passes `universe.episodes()` into `SimilarityEngine`, which now
accepts an episode collection directly instead of a `Dataset`. CAPE
percentile calibration is fixed as a side effect: it is computed from
whatever collection `SimilarityEngine` receives, so once that
collection is Universe-sourced, the calibration is temporally safe
without any change to the calibration logic itself.
`AssessmentEngine` was mechanically adjusted to keep working
(`SimilarityEngine(dataset.episodes)`) but was deliberately not
connected to `ObservableUniverse` — out of scope, tracked under
RE-024.3.

RE-DOC-003 later corrected this historical description: RE-024.3 did
connect `AssessmentEngine` to `ObservableUniverse`. The current
remaining issue is that `AssessmentEngine` still duplicates the
research pipeline locally instead of delegating to the shared
`build_research_result()` source of truth introduced in RE-027.5.

## RE-023.6 — Responsibility correction in SimilarityEngine.top()

No behaviour change. The `peak_date < cutoff` filter cannot be split
into a "leakage" clause and a "RE-004 independence" clause — it is
one expression serving RE-004 alone, whose leakage-blocking effect is
an imprecise (peak_date, not bottom_date) side effect, kept
deliberately for callers that bypass ObservableUniverse. Comment
corrected to attribute temporal safety exclusively to
ObservableUniverse. RE-DOC-003 later verified that `AssessmentEngine`
no longer belongs to that bypassing-caller category after RE-024.3.

## RE-024.1 — Evidence generalized

`Evidence` is no longer coupled to a 5-year horizon: fields renamed
without the `_5y` suffix, `horizon_years` made explicit,
`percentile(p)` computed on demand (not precomputed), single shared
percentile algorithm (`percentile_from_sorted`, also used for
`median_return`/`worst_return`/`best_return` to avoid disagreeing
with `percentile(0.5)` on even-sized match lists). `years` and `p`
are validated (`OUTCOME_HORIZONS_YEARS`, shared with
`ObservableUniverse`; `0.0 <= p <= 1.0`). Absence of evidence returns
`None`, never `0.0` — a Research-Engine-wide design rule now, not
just this object's: a 0.0 is a statistical claim, absence of data is
not. No public behaviour change; nothing consumed the generalized
object yet.

## RE-024.2 — DecisionEngine migrated off ProbabilityEngine

`expected_return()`/`upside()`/`downside()` now come from
`EvidenceEngine` built over the exact same `matches` shown as "top
episodios similares" — not from `ProbabilityEngine`'s unconditional
aggregation over the full 23-episode Dataset. `DecisionEngine`
computes `self._matches` once in `__init__` so `Evidence.matches` and
`historical_matches()` are guaranteed to be the same collection, not
two separate calls to `SimilarityEngine.top()`. `ProbabilityEngine`
no longer imported or instantiated by `DecisionEngine`.
`DecisionEngine` contains no statistical logic of its own (verified:
no `mean`/`median`/`sorted`/`percentile` calls in the class). Result
verified against an independent, by-hand recomputation from the
displayed episodes, not just against passing tests. `run.py` diff
confirmed targeted to exactly the affected lines.

## RE-025.1 — Research Validation Harness

`engine/validation_harness.py` introduces `ValidationHarness`. For
each historical episode it builds the forecast the system would have
produced by replaying, exactly, the same methodology `DecisionEngine`
uses for the present: `ObservableUniverse(dataset,
as_of=episode.bottom_date)` supplies temporally-safe comparables,
`SimilarityEngine.top()` selects matches, `EvidenceEngine.build()`
yields the forecast (`median_return`). Framed as "Research
Validation", not "statistical validation" — the sample is small and
episodes are not independent; see RE-025.2's disclaimer.

Two design constraints are load-bearing, not stylistic:

**Point-in-time, not global leave-one-out.** Comparables for episode
X are restricted to episodes observable as of X's own `bottom_date`.
Comparing X against all other 22 episodes regardless of chronology
would validate a hypothetical system that already knows 2020 while
evaluating 1962 — a different, easier system than the one that
actually runs. `ObservableUniverse` also masks each comparable's own
`future_return_Xy` per RE-023.3, so no comparable can leak a future
outcome that would not yet have been known either.

**Self-exclusion by `bottom_index`, not object identity.**
`ObservableUniverse.episodes()` returns `ObservableEpisode`, a type
deliberately distinct from `Episode` and never substitutable for it
(RE-023.1/ADR-004). Because of that, the episode under evaluation is
never the same object as its projection inside the universe —
`s.episode is not target_episode` would silently exclude nothing.
`bottom_index` is the one field that survives the `Episode ->
ObservableEpisode` projection unchanged and is unique per episode; it
is used as the exclusion key instead.

`sample_size()` (episodes with a real, realized `future_return_Xy`)
and `evaluated_count()` (episodes that additionally produced a
forecast) are computed methods, not asserted constants — the gap
between them is itself diagnostic. Verified against the live Shiller
dataset: 23 episodes total, `sample_size` = 21 (2022.10 and 2025.04
have no realized 5y return yet), `evaluated_count` = 19 (1877.06 and
1880.05 additionally had 0 and 1 comparable respectively in their own
instant, and produced no forecast).

Produces `ValidationRecord(episode, horizon_years, forecast, actual,
comparable_count, evaluable)` only. No aggregate statistic — that is
RE-025.2.

Naming risk, flagged deliberately: unrelated to the pre-existing
`engine/validation_engine.py` (`ValidationEngine`). See the note under
Component Status.

## RE-025.2 — MAE (canonical Research Validation metric)

`engine/validation_metrics.py` adds `mean_absolute_error()`: the mean
of `|forecast - actual|` over the `evaluable` records produced by
RE-025.1, in the same annualized-CAGR units as
`EvidenceEngine.median_return` — no unit conversion, no new
assumption. `None` if no record is evaluable, following the same
Research-Engine-wide rule as `Evidence` (RE-024.1): absence of
evidence is `None`, never `0.0`. Ships together with
`EXPLORATORY_DISCLAIMER`, a literal string callers must surface
alongside the number — this harness produces exploratory evidence
over a small, non-independent sample, not statistical validation in
the strict sense.

Measured against the live dataset: MAE = 7.03% over the 19 evaluated
episodes. Read with caution before treating it as a stable figure —
it is a mean over 19 points, and a single one (1932.06, bottom of the
Great Depression) contributes 18.91 points of error on its own, more
than double any other episode's. Hit-rate (RE-025.3) and rank
correlation (RE-025.4) are the intended check on whether 7.03% is
representative or driven by that outlier.

**Deviation resolved.** The first shipped version of
`mean_absolute_error()` filtered records with two explicit `is None`
checks on `forecast` and `actual`, instead of reading
`record.evaluable` — the flag RE-025.1 already computes for exactly
this purpose. The two criteria agreed on the live dataset, so no
measured result was ever wrong, but the function held its own,
duplicate notion of "is this record usable" and could have silently
diverged from `ValidationHarness` if `evaluable`'s definition ever
changed (e.g., a minimum `comparable_count`). Fixed: the loop now
reads `if not record.evaluable: continue`. Re-verified against the
live dataset after the fix — sample_size=21, evaluated_count=19,
MAE=7.03%, unchanged.

## RE-025.3 — Directional Hit Rate

`engine/validation_metrics.py` adds `directional_hit_rate()`: the
share of evaluable validation records where forecast and realized
return have the same sign. It uses `ValidationRecord.evaluable`,
like `mean_absolute_error()`, and excludes zero-valued forecast or
actual returns because zero does not express a direction.

Measured against the live dataset: directional hit-rate = 94.74%
(18/19). Supporting counts: 19 directional records, 19 positive
forecasts, 0 negative forecasts, 18 positive actuals, 1 negative
actual, 18 hits, 1 miss. MAE was rechecked in the same run and
remained unchanged at 7.03%.

Interpretation is deliberately constrained. This high hit-rate is
not evidence, by itself, that `SimilarityEngine` has meaningful
directional skill. In this sample, `EvidenceEngine.median_return`
never produced a negative forecast: 0/19 forecasts were negative.
The metric therefore mostly reflects the fact that 18/19 realized
5-year returns in the evaluated sample were positive. A naive rule
that always predicted "positive" would have produced almost the same
directional result. RE-025.3 is useful as a diagnostic check, not as
a strong validation claim.

This finding increases the importance of RE-025.4: rank correlation
is expected to be more informative here because it evaluates ordering
of forecast strength against realized outcomes, not just sign.

## RE-025.4 — Rank Correlation

`engine/validation_metrics.py` adds `rank_correlation()`: Spearman
rank correlation between forecast and realized return over evaluable
validation records. Unlike `directional_hit_rate()`, zero values are
not excluded: a zero is a valid value to rank, not an absence of
direction.

Ranks use average-rank tie handling. This is not cosmetic in the live
dataset: the 19 evaluable records contain only 7 unique forecast
values, because `EvidenceEngine.median_return()` can repeat when the
effective match set produces the same median. Average ranks avoid
letting input order decide ties silently.

Measured against the live dataset: rank_count=19,
unique_forecasts=7, unique_actuals=19, Spearman rank correlation =
-0.2290. MAE remained 7.03% and directional hit-rate remained
94.74% in the same verification run.

Interpretation remains exploratory. The negative value is a weak
negative rank relationship in this small, non-independent sample: in
this validation slice, higher forecast ranks did not correspond to
higher realized-return ranks. It should not be read as a formal
statistical rejection of the method, but it is materially more
informative than RE-025.3 because it tests ordering rather than
merely sign.

## RE-025.5 — Runtime reproducibility

`requirements.txt` is now a real dependency file, not an empty
directory. It pins the runtime libraries that materially affect
Research Validation calculations:

-   pandas==3.0.5
-   numpy==2.5.1
-   openpyxl==3.1.5

This is a methodological requirement, not project hygiene. RE-025.4
exposed that different pandas/numpy environments can produce
different validation records and therefore different aggregate
metrics. The canonical Research Validation numbers are the numbers
computed under the pinned runtime above:

-   MAE = 0.07025011023213769 (7.03%).
-   Directional hit-rate = 0.9473684210526315 (94.74%).
-   Rank correlation = -0.22902466816870654.
-   Unique forecast values among evaluable records = 7.

Earlier RE-025 documentation that reported MAE as 7.05% is superseded
by this pinned-runtime result. The difference is small in presentation
but important in principle: validation evidence is only reproducible
when the computational environment is reproducible.

This does not solve effective sample size. `n=19` remains an
operative count of evaluable records, not a claim that 19 independent
observations exist. Effective N is addressed conceptually in
RE-025.6, but not converted into a numeric correction yet.

## RE-025.6 — Effective sample size caveat

Research Validation now explicitly separates operational count from
independent evidence. The live validation set contains 19 evaluable
records, but `n=19` is only a count of records that produced both a
forecast and a realized 5-year return. It is not, by itself, a claim
that 19 statistically independent observations exist.

The first source of dependence is mechanical and outcome-side:
overlap between realized 5-year return windows. If two evaluated
episodes share part of their future 5-year window, part of their
`actual` return is literally measured over the same market interval.
That makes the two validation records less independent than two
non-overlapping observations, even if the forecast procedure is
otherwise point-in-time safe.

This 5-year-window overlap criterion is necessary, but not sufficient.
RE-025.4 exposed a second, forecast-side dependence channel: repeated
forecasts. The 19 evaluable records contain only 7 unique forecast
values. For example, 1998.09 and 2009.03 do not overlap in their
future 5-year realized-return windows, but both received the exact
same forecast value: 0.113866763522. That can happen when
`SimilarityEngine.top()` produces match sets whose median return is
effectively the same, and it means rows that look independent on the
outcome side can still share forecast structure.

RE-025.6 therefore does not publish a numeric effective N. It records
the methodological boundary: current Research Validation metrics are
exploratory diagnostics over 19 evaluable records, with known
dependence through at least two channels:

-   overlapping realized 5-year return windows;
-   repeated forecasts / potentially overlapping comparable sets.

Future work may quantify these channels separately. Until then,
MAE, directional hit-rate and rank correlation must not be described
as if they were computed over 19 independent observations.

## RE-025.7 — Core verification coverage for validation metrics

`tests/verify_core.py` now includes `engine/validation_metrics.py`
in its structural Engine checks.

This is not a functional test of MAE, directional hit-rate, rank
correlation or dependency diagnostics. `verify_core.py` only checks
that expected project paths exist. The purpose of RE-025.7 is narrower:
once `validation_metrics.py` became a real Research Validation module,
the core verification suite should at least recognize its existence.

Verified result: `python3 tests/verify_core.py` passes 6/6 checks and
reports `CORE STATUS : STABLE`.

## RE-025.8 — Overlapping outcome window diagnostic

`engine/validation_metrics.py` adds
`overlapping_outcome_windows(records)`: a diagnostic that returns
pairs of evaluable validation records whose realized 5-year outcome
windows overlap. It is a dependency diagnostic, not a new accuracy
metric.

The function deliberately returns pairs, not just a count, to preserve
explainability. It filters with `record.evaluable`, matching the
canonical Research Validation criterion used by MAE, directional
hit-rate and rank correlation. It does not change `ValidationHarness`
and does not alter any existing metric.

Window overlap is defined as:

    start_a < end_b and start_b < end_a

where:

    start = episode.bottom_date
    end = episode.bottom_date + horizon_years

The dataset stores dates as `YYYY.MM`, where `.01` through `.12`
represent months, not year fractions. For this diagnostic, comparing
dates and adding an integer 5-year horizon are valid operations:
`1932.06 + 5 == 1937.06`. Direct subtraction of these floats is not
valid for duration or ratio calculations: `1933.01 - 1932.12` would
produce `0.89`, not one month. RE-025.8 therefore publishes no overlap
duration and no overlap ratio.

Measured against the live dataset: 23 episodes, sample_size=21,
evaluated_count=19, overlap_pairs=10. The overlapping pairs are:

-   1903.10 / 1907.11
-   1957.12 / 1960.10
-   1957.12 / 1962.06
-   1960.10 / 1962.06
-   1962.06 / 1966.10
-   1966.10 / 1970.06
-   1970.06 / 1974.12
-   1987.12 / 1990.10
-   1998.09 / 2003.02
-   2018.12 / 2020.03

This strengthens the RE-025.6 conclusion: `n=19` is an operative
count, not an independent sample-size claim. RE-025.8 still does not
publish a numeric effective N. It only makes one known dependence
channel directly observable.

## RE-025.9 — Repeated forecast group diagnostic

`engine/validation_metrics.py` adds
`repeated_forecast_groups(records)`: a diagnostic that groups
evaluable validation records sharing the exact same forecast value.
It returns only groups with more than one record.

This is a forecast-side dependency diagnostic, not a new accuracy
metric and not a proof that the underlying comparable sets are
identical. `ValidationRecord` stores `comparable_count`, but not the
actual matched episodes selected by `SimilarityEngine.top()`. RE-025.9
therefore makes repeated forecasts observable without claiming to
measure comparable-set overlap directly.

Measured against the live dataset: 23 episodes, sample_size=21,
evaluated_count=19, unique_forecasts=7,
repeated_forecast_groups=4, records_in_repeated_groups=16.

The repeated forecast groups are:

-   0.090162141571: 1982.07 / 1987.12 / 2018.12 (3 records)
-   0.113866763522: 1990.10 / 1998.09 / 2009.03 / 2020.03 (4 records)
-   0.127427505966: 1921.08 / 1932.06 / 1970.06 / 1974.12 (4 records)
-   0.158567951617: 1903.10 / 1907.11 / 1957.12 / 1960.10 / 1962.06 (5 records)

This materially strengthens the RE-025.6 caveat. Of 19 evaluable
records, 16 fall into repeated forecast groups. Only 3 records have a
forecast value that is unique within the evaluated sample. This does
not invalidate MAE, directional hit-rate or rank correlation, but it
does mean those diagnostics must not be read as if each row carried a
fully independent forecast signal.

## RE-025.10 — Research Validation synthesis

RE-025.1 through RE-025.9 establish Research Validation as a coherent
offline diagnostic layer for the Similarity/Evidence pipeline. It is
point-in-time, uses the same public interfaces as the operative
DecisionEngine flow, computes canonical exploratory metrics, pins the
runtime that makes those metrics reproducible, and documents the main
known dependence channels in the evaluated sample.

The current canonical validation surface is:

-   sample_size = 21;
-   evaluated_count = 19;
-   MAE = 0.07025011023213769 (7.03%) under pinned runtime;
-   directional_hit_rate = 0.9473684210526315 (94.74%);
-   rank_correlation = -0.22902466816870654;
-   overlap_pairs = 10 realized 5-year window overlaps;
-   repeated_forecast_groups = 4;
-   records_in_repeated_forecast_groups = 16/19.

The interpretation is intentionally bounded. These numbers are useful
evidence about how the current Research Engine behaves, but they are
not strong statistical validation. The high directional hit-rate is
not very discriminating because 0/19 forecasts were negative. Rank
correlation is more informative than hit-rate but remains exploratory.
MAE is outlier-sensitive at this sample size. Most importantly, `n=19`
is an operative count, not an independent sample-size claim.

RE-025.8 and RE-025.9 make the independence caveat concrete:

-   outcome-side dependence is observable through 10 overlapping
    realized 5-year windows;
-   forecast-side dependence is observable because 16/19 evaluable
    records share a forecast value with at least one other record.

No numeric effective N is published. That is deliberate. The system now
knows enough to avoid overstating its evidence, but not enough to
compress the dependence structure into a defensible single adjusted
sample-size number. Future work may quantify effective N, comparable
set overlap, or other dependence structures, but RE-025 closes the
current block as exploratory validation with explicit limitations.

## RE-026.1 — Research Validation metrics functional smoke test

`tests/verify_validation_metrics.py` adds a functional smoke test for
the canonical Research Validation surface established by RE-025. It is
not a replacement for the offline harness; it is a regression guard
around the values that the harness and metrics now publish.

The test verifies:

-   episodes = 23;
-   sample_size = 21;
-   evaluated_count = 19;
-   MAE = 0.07025011023213769;
-   directional_hit_rate = 0.9473684210526315;
-   rank_correlation = -0.22902466816870654;
-   overlap_pairs = 10;
-   repeated_forecast_groups = 4.

RE-026.1.1 made the test executable directly from `tests/` by adding
the repository root to `sys.path` before importing `engine.*` modules.

RE-026.1.2 added a runtime gate before metric assertions. The test now
reads `requirements.txt`, compares the pinned package versions against
the active Python environment, and refuses to verify canonical metrics
outside the pinned runtime. This is deliberate: RE-025.5 showed that
different pandas/numpy versions can change validation outputs. A
runtime mismatch must therefore fail as an environment problem, not as
an ambiguous metric regression.

Verified result:

-   `RUNTIME : PINNED`
-   `RESEARCH VALIDATION METRICS : STABLE`

## RE-027.1 — ResearchEngine audit and rebuild decision

RE-027.1 audits `engine/research_engine.py` against the operative flow
that has actually been verified through `DecisionEngine` and Research
Validation.

The current `ResearchEngine` is not a partially working engine. It is
a stale architectural placeholder whose constructor and runtime logic
no longer match the rest of the repository:

-   `SnapshotEngine()` is instantiated without `dataset`;
-   `ExplanationEngine()` is instantiated without `matches`;
-   `AssessmentEngine()` is instantiated without `dataset`;
-   `SnapshotEngine.build(dataset)` is called even though no such
    method exists;
-   `SimilarityEngine` is built directly from `dataset`, bypassing
    `ObservableUniverse`;
-   `SimilarityEngine.compare(snapshot)` is used instead of
    `SimilarityEngine.top(snapshot, n=10)`;
-   evidence would therefore be built from all compared episodes, not
    only from the selected nearest matches, if the constructor errors
    were patched in isolation;
-   `ExplanationEngine` remains broken if called;
-   the method returns a plain dictionary instead of a `ResearchResult`.

The dangerous failure mode is not only that the current object crashes.
If its constructor errors were fixed without correcting the pipeline
contract, it could run while producing evidence from the wrong sample.
That would be worse than an explicit exception, because the system
would appear operational while silently mixing irrelevant historical
episodes into the evidence layer.

Design decision: the rebuilt `ResearchEngine` must be a thin facade
over the pipeline already verified through `DecisionEngine`:

    SnapshotEngine(dataset).latest()
        │
    ObservableUniverse(dataset, as_of=snapshot.date)
        │
    SimilarityEngine(universe.episodes()).top(snapshot, n=10)
        │
    EvidenceEngine().build(matches, years=5)
        │
    ResearchResult

It must not become a second independent implementation of the same
pipeline. A duplicated pipeline would create another place where
architecture and execution can drift apart.

Completed rebuild sequence:

1.  RE-027.2 — redefine `models/research_result.py` so it represents
    the real Research output.
2.  RE-027.3 — rebuild `engine/research_engine.py` around the verified
    operative pipeline.
3.  RE-027.4 — add a functional smoke test for the rebuilt
    `ResearchEngine`.

## RE-027.2 — ResearchResult aligned with operative Research output

RE-027.2 updates `models/research_result.py` so `ResearchResult`
represents the objective Research output now produced by the verified
pipeline.

`ResearchResult` contains:

-   `snapshot`;
-   selected `matches`;
-   resulting `evidence`.

It deliberately does not contain recommendations, portfolio decisions,
assessment confidence or explanations. Those belong to downstream
decision / explanation responsibilities, not to the objective Research
result.

This keeps `ResearchResult` aligned with the Evidence Layer that has
already been validated through RE-025.x and RE-026.x.

## RE-027.3 — ResearchEngine rebuilt as operative pipeline facade

RE-027.3 rebuilds `engine/research_engine.py` as a thin facade over the
same operative research flow already verified through `DecisionEngine`:

    SnapshotEngine(dataset).latest()
        │
    ObservableUniverse(dataset, as_of=snapshot.date)
        │
    SimilarityEngine(universe.episodes()).top(snapshot, n=10)
        │
    EvidenceEngine().build(matches, years=5)
        │
    ResearchResult

The rebuilt engine removes the stale constructor state that previously
instantiated engines with invalid arguments. It also removes the
dangerous `SimilarityEngine.compare()` path, which would have built
evidence from all compared episodes rather than the selected nearest
matches.

Design boundary: `ResearchEngine` is a Research facade only. It does
not call `ExplanationEngine`, `AssessmentEngine` or
`ProbabilityEngine`.

RE-027.3 did not yet eliminate all architecture risk: it still
contained its own copy of the same orchestration later consumed by
`DecisionEngine`. RE-027.5 supersedes that implementation detail by
extracting the shared pipeline into `engine/research_pipeline.py`.

## RE-027.4 — ResearchEngine functional smoke test

RE-027.4 adds `tests/verify_research_engine.py`.

The test verifies that the rebuilt `ResearchEngine` executes the
expected research pipeline and returns a stable `ResearchResult`
surface.

Verified result:

-   `RESEARCH ENGINE : STABLE`
-   `snapshot_date: 2026.07`
-   `matches: 10`
-   `horizon_years: 5`
-   `median_return: 0.11386676352177`
-   `worst_return: -0.01091948933253`
-   `best_return: 0.13767334934864`

This verified that `ResearchEngine` worked, but did not by itself close
the single-source-of-truth concern raised in RE-027.1. RE-027.5 closes
that remaining gap.

## RE-027.5 — Shared Research pipeline source of truth

RE-027.5 adds `engine/research_pipeline.py` with
`build_research_result()`.

This function is now the single source of truth for the objective
Research pipeline:

    SnapshotEngine
        │
    ObservableUniverse
        │
    SimilarityEngine.top()
        │
    EvidenceEngine
        │
    ResearchResult

Both `DecisionEngine` and `ResearchEngine` delegate to this shared
function. This resolves the contradiction identified after RE-027.4:
`ResearchEngine` was described as a facade, but the code still
reimplemented the same orchestration in a second location.

After RE-027.5, future changes to the objective Research pipeline have
one implementation point, not two.

Verified:

-   `engine/research_pipeline.py`, `engine/research_engine.py` and
    `engine/decision_engine.py` compile.
-   `tests/verify_research_engine.py` remains stable.
-   `tests/verify_validation_metrics.py` remains stable.
-   `DecisionEngine` keeps the existing public evidence surface while
    consuming the shared Research pipeline internally.

## RE-DOC-003 — AssessmentEngine status correction

RE-DOC-003 corrects the project status document after verifying
`engine/assessment_engine.py` directly.

Earlier status text continued to say that `AssessmentEngine` built
`SimilarityEngine` directly from `dataset.episodes` and was never
connected to `ObservableUniverse`. That was no longer true: RE-024.3
already changed `AssessmentEngine` to build:

    SnapshotEngine(dataset).latest()
        │
    ObservableUniverse(dataset, as_of=snapshot.date)
        │
    SimilarityEngine(universe.episodes()).top(snapshot, n=10)
        │
    EvidenceEngine().build(matches, years=5)

Corrected interpretation:

-   The temporal-safety concern is resolved for `AssessmentEngine`.
-   `AssessmentEngine` remains outside `run.py`.
-   `AssessmentEngine` still duplicates the Research pipeline locally
    instead of consuming `build_research_result()`.
-   The remaining issue is maintainability / source-of-truth drift, not
    temporal leakage.

This correction is documentation-only. No code changed.

## RE-028.1 — Evidence Engine v2 scope audit

RE-028.1 scopes Evidence Engine v2 before code changes.

Current verified Evidence contract:

-   `EvidenceEngine.build(matches, years=5)` consumes selected
    similarity matches and returns a descriptive `Evidence` object.
-   `Evidence` stores the historical sample (`matches`,
    `episodes_count`, `horizon_years`), return statistics
    (`average_return`, `median_return`, `worst_return`,
    `best_return`, `positive_probability`), recovery statistics and
    `percentile(p)`.
-   Absence of evidence is represented by `None`, never `0.0`.
-   `percentile(p)`, `median_return`, `worst_return` and `best_return`
    share the same percentile rule through `percentile_from_sorted()`.

Current verified consumers:

-   `build_research_result()` consumes `EvidenceEngine` as the shared
    source of truth for `DecisionEngine` and `ResearchEngine`.
-   `AssessmentEngine` still consumes `EvidenceEngine` separately
    until it is migrated to `build_research_result()`.
-   `ValidationHarness` consumes `EvidenceEngine.median_return` as the
    canonical forecast in offline Research Validation.

RE-028 v2 must therefore be additive and backwards-compatible:

-   Existing public fields must keep their names and semantics.
-   Existing consumers must continue to work without code changes.
-   New fields should describe the evidence sample more explicitly;
    they must not encode recommendations, portfolio decisions or
    assessment/confidence.
-   `EvidenceEngine` may compute richer descriptive diagnostics, but
    interpretation of those diagnostics belongs to Assessment / SOP
    governance, not to Evidence.

Candidate v2 additions are sample-shape and explainability fields such
as return count, positive/negative counts, dispersion, downside/upside
distribution markers or explicit sample coverage. Final field selection
is deliberately deferred to RE-028.2 after this contract boundary.

Out of scope for RE-028.1:

-   no change to `models/evidence.py`;
-   no change to `engine/evidence_engine.py`;
-   no AssessmentEngine migration;
-   no SimilarityEngine v2 work;
-   no new portfolio or recommendation logic.

This is a scope gate, not an implementation iteration.

## RE-028.2 — Evidence Engine v2 descriptive sample shape

RE-028.2 implements the first Evidence Engine v2 surface as an
additive, backwards-compatible extension.

`models/evidence.py` adds descriptive sample-shape fields:

-   `return_count`
-   `positive_count`
-   `negative_count`
-   `zero_count`
-   `non_positive_probability`
-   `return_spread`

`engine/evidence_engine.py` computes those fields from the same
horizon-specific return sample already used for
`average_return`, `median_return`, `worst_return`, `best_return` and
`positive_probability`.

Compatibility rule:

-   existing Evidence fields keep their names and semantics;
-   the new fields have defaults, so older direct `Evidence(...)`
    construction remains compatible;
-   absence of evidence still uses `None` for probability/spread fields
    where a numeric value would imply observed data.

Interpretation boundary:

-   Evidence describes the historical sample;
-   Evidence does not score confidence;
-   Evidence does not recommend portfolio action;
-   Evidence does not decide whether the SOP should deploy, hold or
    block capital.

Verified result from `tests/verify_research_engine.py` after RE-028.2:

-   `RESEARCH ENGINE : STABLE`
-   `matches: 10`
-   `return_count: 9`
-   `positive_count: 8`
-   `negative_count: 1`
-   `zero_count: 0`
-   `non_positive_probability: 0.11111111111111`
-   `return_spread: 0.14859283868117`

The distinction between `episodes_count=10` and `return_count=9` is
intentional: the selected historical sample can contain matches that do
not yet have a realized return at the requested horizon. Evidence v2
makes that sample coverage visible without turning it into an
assessment score.

## RE-028.3 — Evidence percentile field gate

RE-028.3 decides not to add new named percentile fields yet.

Current verified behavior:

-   `Evidence.percentile(p)` already exposes arbitrary downside/upside
    return percentiles on demand.
-   `median_return`, `worst_return`, `best_return` and
    `percentile(p)` share the same `percentile_from_sorted()` rule.
-   Evidence v2 already describes the current sample shape through
    return_count, positive/negative/zero counts,
    non_positive_probability and return_spread.

Design decision:

-   Explicit named percentile fields such as p10/p25/p75/p90 are
    deferred until Assessment or SOP governance defines why those exact
    thresholds are needed.
-   Evidence must not make arbitrary interpretive cutoffs look
    canonical just because they were convenient to compute.
-   Until a protocol needs named thresholds, `percentile(p)` remains
    the correct descriptive interface.

Boundary:

-   Evidence can describe a distribution.
-   Evidence must not decide which percentile is "defensive",
    "aggressive", "safe" or "actionable".
-   Those labels belong to Assessment / SOP governance, not to
    EvidenceEngine.

This is documentation-only scope control. No code changed.

## RE-028.4 — Evidence Engine v2 closure gate

RE-028.4 closes the current Evidence Engine v2 block.

Verified Evidence v2 surface:

-   existing return statistics remain unchanged;
-   `return_count` makes realized sample coverage explicit;
-   positive / negative / zero counts describe the sign distribution;
-   `non_positive_probability` describes observed downside frequency;
-   `return_spread` describes observed return range;
-   `percentile(p)` remains available for arbitrary distribution
    inspection without promoting any threshold to canonical status.

Closure decision:

-   No additional Evidence fields are added in this block.
-   Evidence v2 is now descriptive enough for the next layer to consume.
-   Further interpretation belongs to Assessment / SOP governance:
    capital tranches, dry-powder deployment, invalidation flags and
    confidence language must be defined outside Evidence.

Known boundary after RE-028.4:

-   Evidence can say what happened in comparable historical episodes.
-   Evidence can expose sample coverage, sign mix, downside frequency,
    spread and arbitrary percentiles.
-   Evidence cannot say whether to deploy capital, how much to deploy,
    whether evidence is sufficient, or whether a SOP protocol should
    be activated.

This closes Evidence Engine v2 for the current architecture pass.

## RE-029.1 — Assessment / SOP governance scope audit

RE-029.1 opens the Assessment / SOP governance block as documentation-only
scope work.

The purpose is to define the boundary before writing rules:

-   Evidence describes objective historical observations.
-   Assessment interprets evidence quality, fragility and applicability.
-   SOP governance maps that interpretation into capital posture.
-   Human approval remains the final control for any capital deployment.

Primary objective hierarchy:

1.  Avoid irreversible error.
2.  Preserve capital in real terms.
3.  Maximize long-term return only after the first two constraints are
    respected.

This hierarchy is a governance choice, not an output of the model. If
the order changes, the rest of the SOP changes with it.

Dry powder definition:

`Dry powder` means deployable investable liquidity available within a
short operational window without principal impairment. It is not limited
to literal cash; it may include money-market instruments, T-bills or
credit lines that the owner is explicitly willing to use
countercyclically.

Protocol separation:

-   Dry Powder Protocol: idle or reserved deployable capital becomes
    invested capital. It increases net risk exposure and is governed by
    the capital posture language below.
-   Portfolio Reallocation Protocol: one risk asset is sold to buy
    another risk asset. It does not necessarily increase net risk
    exposure; it changes concentration and requires its own future
    invalidators, including liquidity and risk of the asset sold,
    correlation between the asset sold and the asset bought, and the
    cost of crystallizing the loss on the asset sold.

These are separate SOP protocols. They must not be collapsed into one
rule merely because both can occur during a drawdown.

Capital posture language:

-   Conserve.
-   Prepare.
-   Deploy partially.
-   Deploy aggressively.

`Blocked` is not a fifth intensity level. It is an orthogonal veto flag
that can override any posture when the framework itself is not reliable
enough to act.

Initial invalidation gates:

-   Evidence quality: weak or degraded historical evidence, including
    validation diagnostics, sample fragility, dispersion or insufficient
    comparable support.
-   Regime comparability: the current drawdown must have structurally
    meaningful precedent, not only numerical proximity.
-   Personal capacity: even good evidence is unusable if deployable
    liquidity, operational readiness or personal constraints make action
    inappropriate.

Human approval policy:

-   `Conserve` and `Prepare` may be logged without committing capital.
-   `Deploy partially` and `Deploy aggressively` require explicit human
    approval with timestamp before execution.
-   A `Blocked` flag always forces human review before any deployment
    action.

Boundary:

-   No code changes in RE-029.1.
-   No thresholds are defined yet.
-   No automatic capital decisions are introduced.
-   No `AssessmentEngine` rewrite is performed in this iteration.

The Engine may surface flags and descriptive evidence. It must not
decide capital deployment by itself.

## RE-029.2 — AssessmentEngine boundary audit

RE-029.2 audits `engine/assessment_engine.py` against the RE-029.1
boundary before changing code.

Verified current behaviour:

-   `AssessmentEngine` is not called by `run.py`.
-   It does use `ObservableUniverse(dataset, as_of=snapshot.date)`, so
    the older temporal-safety concern is resolved.
-   It builds evidence from `SimilarityEngine.top(..., n=10)` and
    `EvidenceEngine().build(..., years=5)`.
-   It still implements that research flow locally instead of
    delegating to the shared `build_research_result()` pipeline used by
    `DecisionEngine` and `ResearchEngine`.
-   It computes confidence through `ValidationEngine`, using
    coverage/consistency/diversity/stability, with stability currently
    hardcoded to 1.0.
-   It exposes interpretive helpers such as `drawdown_zone()`,
    `expected_return_5y()`, `upside_potential()` and `downside_risk()`.

Boundary conclusion:

-   Evidence production belongs to the shared Research pipeline.
-   Evidence description belongs to `EvidenceEngine`.
-   Evidence interpretation may belong to `AssessmentEngine`.
-   Capital posture, dry-powder deployment, portfolio reallocation and
    human approval belong to SOP governance, not to `AssessmentEngine`.

Therefore `AssessmentEngine` v2 should not become a decision engine. Its
next code iteration should first remove source-of-truth duplication by
consuming `build_research_result()` or `ResearchResult`, then expose
assessment flags about evidence quality, fragility and applicability.
It must not produce portfolio actions, capital amounts or automatic
deployment instructions.

This is documentation-only scope control. No code changed.


## RE-DOC-004 — Assessment / SOP boundary follow-up notes

RE-DOC-004 records two scope notes discovered after RE-029.2.

First, `AssessmentEngine.drawdown_zone()` and SOP capital posture are
separate axes. `drawdown_zone()` currently labels market severity
(`NORMAL`, `CORRECTION`, `BEAR MARKET`, `CRISIS`). Capital posture labels
(`Conserve`, `Prepare`, `Deploy partially`, `Deploy aggressively`) govern
action intensity. Market severity may become one input into posture, but
it is not itself a deployment decision. These taxonomies must not be
merged silently just because both describe drawdown context.

Second, stepped error tolerance remains explicitly pending. The intended
governance direction is conservative by default and aggressive only when
independent signals converge. RE-029.1 deliberately defines no thresholds
and no trigger logic, so this principle is recorded here as future SOP
governance work, not as current executable behavior.

Boundary:

-   No code changes.
-   No thresholds are defined.
-   No automatic capital decisions are introduced.
-   Future posture logic must preserve the distinction between market
    severity, evidence quality, personal capacity and capital action.

## RE-029.3 — AssessmentEngine consumes shared Research pipeline

RE-029.3 refactors `engine/assessment_engine.py` so `AssessmentEngine`
consumes `build_research_result(dataset, matches_count=10,
horizon_years=5)` instead of rebuilding Snapshot -> ObservableUniverse
-> SimilarityEngine.top() -> EvidenceEngine locally.

This closes the source-of-truth duplication identified in RE-029.2.
`AssessmentEngine`, `DecisionEngine` and `ResearchEngine` now share the
same objective Research pipeline for evidence production.

Boundary:

-   No capital posture.
-   No dry-powder deployment.
-   No portfolio reallocation.
-   No automatic recommendations.

Confidence remains out of scope. `AssessmentEngine.confidence()` still
uses `ValidationEngine`, including stability hardcoded to 1.0. That
score must not feed SOP capital gates until a later
governance/calibration pass defines it.

## RE-029.4 — AssessmentEngine public helper verification

RE-029.4 verifies that the public Assessment helper surface remains
stable after RE-029.3.

Verified result:

-   `drawdown_zone`: NORMAL
-   `expected_return_5y`: 0.113866763521769
-   `upside_potential`: 0.132855208016562
-   `downside_risk`: -0.010919489332530
-   `matches`: 10

This verifies the public helper outputs, not confidence calibration and
not SOP capital posture.

------------------------------------------------------------------------

## RE-029.5 — Confidence-to-posture gate boundary

RE-029.5 defines how evidence quality may connect to SOP capital
posture before any executable rules are written.

Decision:

-   Evidence quality / confidence is a gate, not a weighted input.
-   Weak evidence caps the maximum allowed capital posture regardless
    of expected return.
-   Evidence quality must not be averaged into a composite capital score
    that can be offset by attractive return expectations or unrelated
    favorable signals.

Rationale:

-   A weighted score optimizes, but can become a black box.
-   A gate protects: if evidence quality is insufficient, the reason for
    limiting posture remains explicit and auditable.
-   This follows the primary objective hierarchy: avoid irreversible
    error before preserving capital, and preserve capital before
    maximizing return.

Gate combination:

-   Evidence quality, regime comparability and personal capacity combine
    by veto / most restrictive ceiling.
-   One failed gate cannot be compensated by other gates.
-   The final capital posture cannot exceed the lowest ceiling produced
    by any active gate.

Current confidence restriction:

-   The current `AssessmentEngine` confidence score must not be used as
    the evidence-quality gate.
-   Reason: the score still includes `stability=1.0` as a hardcoded
    placeholder, which gives a false 25% weight to a non-measured
    dimension.
-   Until stability is calibrated, any future evidence-quality gate must
    inspect individual dimensions directly (coverage, consistency,
    diversity and explicit stability status) or remain documentation-only.

Boundary:

-   No thresholds are defined.
-   No capital posture rules are implemented.
-   No code changed.

------------------------------------------------------------------------

## RE-029.6 — Evidence Quality Gate dimensions

RE-029.6 defines the documentary shape of the Evidence Quality Gate.
It does not implement the gate and does not define numeric thresholds.

The purpose of the gate is to cap maximum SOP capital posture according
to the quality of the evidence base. Evidence quality remains a ceiling,
not a weighted source of conviction. It can restrict capital posture; it
cannot make posture more aggressive by itself.

Starting posture:

-   The initial Evidence Quality Gate state must be conservative.
-   The current Research Validation surface is useful engineering
    evidence, but it does not yet demonstrate predictive validity.
-   Directional hit-rate is not discriminating in the current sample:
    0/19 evaluable forecasts were negative, so the 94.74% hit-rate
    mostly reflects that 18/19 realized 5-year outcomes were positive.
-   Rank correlation is weakly negative under the pinned runtime
    (`-0.22902466816870654`), so higher forecast ranks have not yet
    corresponded to higher realized-return ranks in this validation
    slice.
-   Therefore the gate must not start at Neutral by default. Neutral or
    more permissive states must be earned later through validation, not
    assumed from engineering consistency.

Evidence Quality dimensions:

1.  Coverage.

    Measures whether enough usable comparable evidence exists for the
    research claim being made. This aligns with the existing
    `ValidationEngine` coverage concept and with Research Validation's
    distinction between `sample_size` and `evaluated_count`.

2.  Consistency.

    Measures whether the evidence points in a coherent direction across
    the selected comparable set. This aligns with the existing
    `ValidationEngine` consistency concept. Consistency is descriptive;
    it must not be converted into a capital recommendation by itself.

3.  Diversity.

    Measures whether the evidence is supported by meaningfully different
    historical precedents rather than a narrow cluster of similar cases.
    This aligns with the existing `ValidationEngine` diversity concept.

4.  Independence / dispersion.

    Measures whether the evidence sample carries independent information
    or is structurally concentrated. This dimension captures the
    Research Validation findings from RE-025.6, RE-025.8 and RE-025.9:
    `n=19` is an operative count, not an independent sample-size claim;
    10 evaluated pairs have overlapping realized 5-year outcome windows;
    and 16/19 evaluable records belong to repeated forecast groups.

5.  Predictive validation status.

    Measures whether the Research Engine has demonstrated that its
    forecasts discriminate outcomes, not merely that the pipeline is
    reproducible. Current status is conservative: MAE is informative but
    outlier-sensitive, directional hit-rate is not discriminating, and
    rank correlation is weakly negative.

Relationship with existing `ValidationEngine`:

-   Existing `ValidationEngine` dimensions may inform future Evidence
    Quality implementation, especially coverage, consistency and
    diversity.
-   The current aggregate `AssessmentEngine.confidence().score` must not
    be used as the Evidence Quality Gate.
-   Reason: the score still includes hardcoded `stability=1.0`, and it
    does not capture the Research Validation independence / dispersion
    caveat.
-   RE-029.6 therefore defines dimensions, not executable scoring.

What Evidence Quality may limit:

-   Maximum capital posture.
-   Maximum aggressiveness of Dry Powder deployment.
-   Maximum aggressiveness of Portfolio Reallocation.
-   Whether an otherwise attractive Research output may be acted on
    beyond a conservative posture.

What Evidence Quality may not do:

-   It may not create a Risk ON posture by itself.
-   It may not override Dry Powder constraints.
-   It may not override Portfolio Reallocation constraints.
-   It may not override personal-capacity constraints.
-   It may not convert attractive expected return into permission for
    aggressive capital deployment when evidence quality is weak.

Protocol separation:

-   Dry Powder Protocol and Portfolio Reallocation Protocol remain
    separate governance protocols.
-   Dry Powder governs deployable liquidity.
-   Portfolio Reallocation governs changes to existing exposure.
-   Evidence Quality governs the maximum posture allowed by the evidence
    base across both protocols.
-   Final posture still follows veto logic: the most restrictive active
    gate wins.

Boundary:

-   No thresholds are defined.
-   No enum or state machine is implemented.
-   No capital posture rules are implemented.
-   No code changed.

------------------------------------------------------------------------

## RE-029.7 — Evidence Quality Gate calibration boundary

RE-029.7 defines the calibration boundary for the Evidence Quality Gate.
It does not implement the gate and does not define numeric thresholds.

Architectural meaning of conservative:

-   The gate is fail-closed, not fail-open.
-   Evidence must actively justify any posture above the conservative
    ceiling against explicit, pre-registered criteria.
-   The default is not a middle state. Uncertainty resolves toward
    restriction because opportunity cost is subordinate to irreversible
    error in the SOP objective hierarchy.
-   Gate states must be discrete. Evidence Quality must not become a
    continuous capital-allocation function derived from a score.
-   A continuous score would reintroduce the optimization pressure that
    RE-029.5 rejected when it defined evidence quality as a gate rather
    than a weighted input.

Conditions for moving from conservative toward neutral:

-   Criteria must be pre-registered before the evidence is evaluated.
-   The decision must not be made ad hoc because a current result appears
    attractive.
-   All Evidence Quality dimensions must be measured without
    placeholders, including stability.
-   Future validation must show positive discriminatory power under a
    pre-registered validation protocol. Rank correlation positive and
    distinguishable from zero is one possible form of such evidence, but
    RE-029.7 does not define it as the only future criterion.
-   Directional metrics must be compared against naive baselines. A
    hit-rate only matters if it improves on trivial rules such as always
    predicting a positive return.
-   Error metrics such as MAE must be compared against naive baselines,
    such as unconditional historical mean or median forecasts, before
    they can support a less restrictive gate.
-   Sample dependence must be measured, bounded or explicitly discounted.
    It must not be hidden behind nominal record counts.

Current evidence that does not suffice:

-   MAE of 7.03% is informative, but not yet compared against a naive
    point-in-time baseline.
-   Directional hit-rate of 94.74% is not discriminating in the current
    sample because 0/19 evaluable forecasts were negative.
-   Rank correlation is weakly negative under the pinned runtime
    (`-0.22902466816870654`).
-   `n=19` is an operative count, not an independent sample-size claim,
    because Research Validation already documents overlapping realized
    outcome windows and repeated forecast groups.

Dimension readiness:

-   Coverage is genuine but weak. It counts usable matches, but does not
    yet judge whether those matches are strong analogies.
-   Diversity is genuine but weak. It uses decade dispersion as a coarse
    proxy and does not guarantee regime independence.
-   Consistency is real but not yet governance-grade. It measures return
    dispersion among matches, but can be inflated by temporally
    concentrated or structurally dependent observations.
-   Stability is not measured. It is currently hardcoded to `1.0` and
    must be treated as unavailable, not as weak positive evidence.
-   Independence / dispersion and predictive validation status are
    documented dimensions, but not yet implemented as local gate
    measurements.

Prohibited shortcuts:

-   `AssessmentEngine.confidence().score` must not be used as the
    Evidence Quality Gate.
-   It must not be used as a temporary proxy until something better
    exists. That path would turn a placeholder into governance logic.
-   Aggregate Research Validation metrics must not be cited as the
    quality of a specific current snapshot. They describe historical
    model behaviour, not local evidence quality for today's match set.
-   Attractive expected return must not compensate for weak evidence
    quality.
-   No emergency or urgency argument may relax the Evidence Quality Gate
    ad hoc. Relaxation requires a numbered, documented governance
    iteration.

Open governance question:

-   A future human-approval mechanism must decide whether an exception
    iteration written during the crisis that motivates it deserves the
    same authority as one written before the pressure existed.
-   Possible safeguards include a second approver, a cooling-off period
    or a rule requiring that emergency exceptions be defined before the
    triggering event.
-   RE-029.7 records this as an open governance question only. It does
    not solve the approval mechanism.

Boundary:

-   No thresholds are defined.
-   No enum or state machine is implemented.
-   No capital posture rules are implemented.
-   No code changed.

------------------------------------------------------------------------

## RE-029.8 — Evidence Quality Gate implementation scope

RE-029.8 defines the allowed scope of the first future
`EvidenceQualityGate` implementation. It does not implement the gate.

The first code iteration, when authorized, should create structure only.
It must not introduce numeric thresholds, automatic capital posture
changes or operative wiring into the current execution path.

Implementation boundary:

-   Do not modify `AssessmentEngine.confidence().score`.
-   Do not use `AssessmentEngine.confidence().score` as a temporary
    proxy.
-   Do not modify `ValidationEngine` in the first gate implementation.
-   Do not wire the first `EvidenceQualityGate` implementation into
    `run.py`.
-   Do not wire it into `DecisionEngine`.
-   The first implementation should exist, compile and be testable in
    isolation before it governs anything operative.

Separate input channels:

The future gate must not receive its inputs as one flat list of
"allowed evidence." RE-029.7 already distinguishes global Research
Validation from local snapshot quality. The implementation should
preserve that distinction in its shape.

1.  Local snapshot evidence quality.

    This channel describes the current match set only.

    Initial local inputs may include:

    -   local coverage;
    -   local consistency;
    -   local diversity.

    These values are about today's selected evidence sample. They do not
    prove that the model has predictive skill globally.

2.  Global model-validation state.

    This channel describes whether the Research Engine, as a model, has
    demonstrated predictive discrimination under pre-registered
    validation criteria.

    Current global state is conservative / not validated. Existing
    Research Validation metrics are useful diagnostics, but they do not
    yet justify a neutral gate state.

    Global validation state must not be collapsed into local match-set
    quality.

Dimension clarification:

-   RE-029.6 defines five official Evidence Quality dimensions:
    coverage, consistency, diversity, independence / dispersion and
    predictive validation status.
-   `stability` is not currently an official Evidence Quality Gate
    dimension.
-   `stability` belongs to the legacy `ValidationEngine` /
    `confidence.score` path today.
-   RE-029.7 evaluates `stability` only because the hardcoded
    `stability=1.0` blocks use of `confidence.score` as a gate or proxy.
-   Independence / dispersion does not automatically absorb stability.
    Independence / dispersion concerns the structure of the evidence
    sample. Stability concerns the stability of the engine or its
    outputs across versions, conditions or runs.
-   If stability is ever added to the Evidence Quality Gate, it must be
    introduced explicitly in a later numbered iteration.

Conceptual output states:

The future gate must distinguish absence of measurement from measured
insufficiency. This follows the same design principle as Evidence:
absence of evidence is not `0.0`.

The conceptual output therefore needs at least three states:

-   not measurable;
-   conservative;
-   future less-restrictive state, name not yet finalized.

`not measurable` means the gate lacks required measurements. It is not
the same as "measured and insufficient." Both may cap posture
conservatively, but they must remain explainably different states.

Future implementation rule:

-   The first code change should model structure and explanations only.
-   It should preserve local/global input separation.
-   It should preserve discrete output states.
-   It should default to fail-closed.
-   It should remain outside the operative flow until thresholds,
    calibration and human approval are documented in later iterations.

Boundary:

-   No code changed.
-   No thresholds are defined.
-   No enum names are finalized.
-   No capital posture rules are implemented.
-   No operative wiring is authorized.

------------------------------------------------------------------------

## RE-029.9 — Evidence Quality Gate first-code acceptance criteria

RE-029.9 defines the acceptance criteria for the first future code PR
that introduces an isolated `EvidenceQualityGate` structure. It does not
implement that PR.

The purpose is to make the next transition from documentation to code
auditable. A future PR should be accepted or rejected by reading its
diff against these criteria.

Expected files:

-   A future implementation may introduce a new isolated module, likely
    `engine/evidence_quality_gate.py`.
-   A future verification may introduce a focused test, likely
    `tests/verify_evidence_quality_gate.py`.
-   File names are not finalized by RE-029.9, but the responsibility is:
    one isolated gate module and one focused verification surface.

Required implementation properties:

-   The gate exists and compiles in isolation.
-   The gate is not wired into `run.py`.
-   The gate is not wired into `DecisionEngine`.
-   The gate does not modify `AssessmentEngine`.
-   The gate does not modify `ValidationEngine`.
-   The gate does not read or reuse
    `AssessmentEngine.confidence().score`.
-   The gate keeps local snapshot evidence quality separate from global
    model-validation state.
-   The gate exposes discrete output states, including at least
    `not measurable` and `conservative`.
-   The gate defaults to fail-closed.
-   The gate returns explanations, not only state labels.

Required test properties:

-   Tests must verify structure and behaviour, not only importability.
-   With today's available dimensions -- partial local inputs, no local
    implementation of independence / dispersion, no local implementation
    of predictive validation status and global model-validation state
    still not validated -- the gate must return `not measurable` or
    `conservative`.
-   The same test must reject any less-restrictive state under today's
    inputs.
-   Incomplete inputs or `None` values must produce `not measurable`, not
    a crash and not an assumed default score.
-   This follows the RE-024.1 Evidence rule: absence of evidence is not
    `0.0`.

Explanation requirements:

-   Explanations must identify the specific channel or dimension causing
    the cap.
-   A generic explanation such as "insufficient evidence" is not
    acceptable by itself.
-   Acceptable explanations should name causes such as:

    -   local coverage unavailable;
    -   local consistency unavailable;
    -   local diversity unavailable;
    -   global model-validation state not validated;
    -   predictive validation status unavailable;
    -   independence / dispersion not measured.

Frozen Core rejection criterion:

-   The first `EvidenceQualityGate` PR must not modify Frozen Core.
-   Any modification to Frozen Core in that PR is grounds for rejection
    unless a separate numbered iteration explicitly invokes the Frozen
    Core Policy exception before the code change.

Explicit non-goals for the first code PR:

-   No numeric thresholds.
-   No capital posture mapping.
-   No automatic recommendations.
-   No runtime wiring.
-   No changes to `DecisionEngine`.
-   No changes to `AssessmentEngine`.
-   No changes to `ValidationEngine`.
-   No replacement of `confidence.score`.
-   No use of aggregate Research Validation metrics as local snapshot
    quality.

Boundary:

-   No code changed.
-   No thresholds are defined.
-   No enum names are finalized.
-   No capital posture rules are implemented.
-   No operative wiring is authorized.

------------------------------------------------------------------------

## RE-030.1 — Isolated Evidence Quality Gate

RE-030.1 introduces the first isolated `EvidenceQualityGate` code
structure.

This is the first implementation step after the RE-029 governance block.
It follows the acceptance criteria documented in RE-029.9.

Files added:

-   `engine/evidence_quality_gate.py`
-   `tests/verify_evidence_quality_gate.py`

Implemented structure:

-   `LocalEvidenceQualityInputs`
-   `GlobalModelValidationState`
-   `EvidenceQualityGateResult`
-   `EvidenceQualityGate`
-   `NOT_MEASURABLE`
-   `CONSERVATIVE`

Architecture:

-   Local snapshot evidence quality and global model-validation state are
    separate input channels.
-   Local inputs currently include coverage, consistency, diversity and
    whether independence / dispersion has been measured.
-   Global input currently captures predictive validation status.
-   The gate returns a discrete state plus explanations.
-   Absence of measurement is represented as `not measurable`, not as a
    numeric default.
-   The gate defaults fail-closed.

Current behaviour:

-   Today's partial inputs return `not measurable`.
-   Incomplete local inputs or missing global validation state return
    `not measurable`.
-   Fully measured inputs with predictive validation marked `validated`
    still return `conservative`, because no less-restrictive state is
    authorized yet.
-   Explanations identify specific causes, such as local coverage
    unavailable, predictive validation status unavailable, independence /
    dispersion not measured, or global model-validation state not
    validated.

Verification:

`tests/verify_evidence_quality_gate.py` verifies:

-   today's available inputs produce `not measurable` or `conservative`,
    never a less-restrictive state;
-   incomplete inputs / `None` values produce `not measurable`;
-   explanations name specific channels or dimensions;
-   fully measured but not yet authorized inputs produce `conservative`.

Verified result:

-   `EVIDENCE QUALITY GATE : STABLE`
-   `today_state: not measurable`
-   `incomplete_state: not measurable`
-   `measured_but_not_authorized_state: conservative`

Boundary:

-   No thresholds are defined.
-   No capital posture mapping is implemented.
-   No automatic recommendation is implemented.
-   No runtime wiring is implemented.
-   `run.py` is unchanged.
-   `DecisionEngine` is unchanged.
-   `AssessmentEngine` is unchanged.
-   `ValidationEngine` is unchanged.
-   Frozen Core is unchanged.

------------------------------------------------------------------------

## RE-030.2 — Local Evidence Quality input adapter

RE-030.2 adds the first adapter from real Research output into local
Evidence Quality inputs.

Function added:

    build_local_evidence_quality_inputs(evidence)

Design:

-   The adapter receives only `evidence`.
-   It does not receive `matches` separately.
-   `Evidence` remains the single source of truth for the selected match
    set through `evidence.matches`.
-   This prevents source-of-truth drift between an `Evidence` object and
    a separately supplied match list.

Local dimensions:

-   `coverage` is calculated from usable evidence:

        min(evidence.return_count / 10.0, 1.0)

    It deliberately does not use `len(evidence.matches) / 10.0`.
    Today's snapshot has 10 selected matches but only 9 usable realized
    returns at the evidence horizon, so local coverage is 0.9, not 1.0.

-   `consistency` is calculated from realized returns at the same horizon
    as the `Evidence` object:

        future_return_{evidence.horizon_years}y

    This avoids the legacy `ValidationEngine` default horizon
    (`future_return_3y`) and keeps local consistency aligned with the
    returns that produced `Evidence.median_return`,
    `Evidence.worst_return` and `Evidence.best_return`.

-   `diversity` is calculated from the number of decades represented in
    `evidence.matches`, divided by the selected match count.

-   `independence_dispersion_measured` remains `False`.

Isolation clarification:

RE-030.1 was isolated in the strongest sense: the gate structure had no
dependency on other project modules.

RE-030.2 introduces a narrower form of isolation. The adapter reads the
existing `Evidence` object and its `Similarity` matches, so it is no
longer zero-dependency. It remains architecturally isolated because
nothing calls it from the operative flow:

-   `run.py` is unchanged.
-   `DecisionEngine` is unchanged.
-   `AssessmentEngine` is unchanged.
-   `ValidationEngine` is unchanged.

Verified current local values:

-   `real_local_coverage: 0.90000000000000`
-   `real_local_consistency: 0.95184562290644`
-   `real_local_diversity: 0.60000000000000`
-   `real_today_state: not measurable`

The focused verification pins the exact current values. It does not
settle thresholds, capital posture mapping or governance authority.

Boundary:

-   No thresholds are defined.
-   No capital posture mapping is implemented.
-   No automatic recommendation is implemented.
-   No runtime wiring is implemented.
-   `run.py` is unchanged.
-   `DecisionEngine` is unchanged.
-   `AssessmentEngine` is unchanged.
-   `ValidationEngine` is unchanged.
-   Frozen Core is unchanged.

------------------------------------------------------------------------

## RE-031.1 — Regime Comparability Gate boundary

RE-031.1 defines the first boundary for the Regime Comparability Gate.
It is documentation-only.

Purpose:

The Regime Comparability Gate asks whether the historical evidence being
used by the Research Engine is structurally applicable to the current
market regime.

It does not ask whether the market is attractive.

It does not ask whether expected return is high.

It asks whether the current regime is comparable enough to the regimes
represented in the evidence sample for the evidence to be allowed to
support capital posture.

Architectural role:

-   Regime comparability is a gate / ceiling, not a weighted input.
-   It can cap maximum capital posture.
-   It cannot make posture more aggressive by itself.
-   It cannot compensate for weak Evidence Quality.
-   It cannot override Personal Capacity.
-   It combines with other gates by veto / most restrictive ceiling.

Relationship with Evidence Quality:

-   Evidence Quality asks whether the evidence sample is internally
    usable and whether the model has demonstrated predictive validity.
-   Regime Comparability asks whether the current regime is structurally
    represented by that evidence.
-   These questions are related but not identical.
-   A high-quality evidence sample can still be a poor guide if today's
    regime is structurally outside the sample.
-   A comparable regime does not make weak evidence strong.

Relationship with `AssessmentEngine.drawdown_zone()`:

-   `drawdown_zone()` is a market severity taxonomy.
-   It is not a regime-comparability gate.
-   It may help describe the current market state, but it does not decide
    whether today's regime is comparable to historical precedents.
-   RE-031.1 does not modify `AssessmentEngine`.

Candidate dimensions:

The first implementation is not authorized yet, but future Regime
Comparability work may need to evaluate dimensions such as:

-   valuation regime;
-   inflation regime;
-   interest-rate regime;
-   earnings / margin regime;
-   volatility regime;
-   liquidity / credit regime;
-   policy / intervention regime;
-   market-structure regime.

These are candidate dimensions only. RE-031.1 defines no thresholds and
does not decide which dimensions become executable.

Current state:

-   No Regime Comparability code exists.
-   No local regime-comparability inputs exist.
-   No global regime taxonomy exists.
-   No thresholds exist.
-   No capital posture mapping exists.
-   The gate is not measurable today.

Default stance:

-   Until measured, Regime Comparability must be treated as unavailable,
    not favorable.
-   Absence of regime comparability evidence must not be represented as a
    positive score.
-   If a future gate requires a state before measurement exists, it must
    fail closed.

Prohibited shortcuts:

-   Do not use `drawdown_zone()` as a regime-comparability proxy.
-   Do not use expected return as a regime-comparability proxy.
-   Do not use Evidence Quality as a regime-comparability proxy.
-   Do not infer comparability from the fact that `SimilarityEngine`
    found matches.
-   Do not relax the gate ad hoc because a current market opportunity
    appears attractive.

Open questions:

-   Which regime dimensions are observable with current data?
-   Which dimensions require new data sources?
-   Should regime comparability be measured locally against the selected
    match set, globally against the full historical universe, or both?
-   Can regime comparability be computed, or does it require an explicit
    human regime assessment for some dimensions?
-   How should regime comparability interact with future Personal
    Capacity classification?

Boundary:

-   No code changed.
-   No thresholds are defined.
-   No regime taxonomy is finalized.
-   No capital posture mapping is implemented.
-   No operative wiring is authorized.

------------------------------------------------------------------------

## RE-032.1 — Personal Capacity classification boundary

RE-032.1 defines the first boundary for Personal Capacity.
It is documentation-only.

Primary classification question:

    Is Personal Capacity a parallel gate,
    a human-approval requirement,
    or a mixed control?

RE-032.1 deliberately does not assume the answer.

Purpose:

Personal Capacity asks whether the person can responsibly assume risk
now.

It does not measure market opportunity.

It does not measure evidence quality.

It does not measure regime comparability.

It asks whether the person's current financial and behavioural capacity
allows any capital posture above the conservative floor.

Architectural role:

-   Personal Capacity may become a gate, a human-approval prerequisite or
    a mixed control.
-   Until classified, it must not be treated as a fully computable gate.
-   If it becomes a gate, it must act as a ceiling, not a weighted input.
-   It cannot make posture more aggressive by itself.
-   It cannot compensate for weak Evidence Quality.
-   It cannot compensate for poor Regime Comparability.
-   It must fail closed when required facts or attestations are missing.

Two input channels:

Future Personal Capacity work must not collapse all personal dimensions
into one opaque score. Inputs must remain separated into at least two
channels.

1.  Verifiable facts.

    These are objective or documentable conditions, such as:

    -   available liquidity;
    -   near-term cash needs;
    -   fixed obligations;
    -   debt service;
    -   income concentration;
    -   portfolio concentration;
    -   required emergency reserve;
    -   known time horizon constraints.

2.  Attested judgement.

    These are human declarations or judgements, not stable objective
    measurements, such as:

    -   perceived income stability;
    -   willingness to tolerate drawdown;
    -   ability to avoid forced selling;
    -   psychological capacity to hold through stress;
    -   household or life constraints not captured in financial data.

These channels may both restrict posture, but they must not be averaged
into a single score.

Drawdown tolerance risk:

Declared tolerance to drawdown is least reliable when it matters most.

A tolerance statement made in calm conditions is more useful than a
revision made during a crisis. A change in declared tolerance during a
drawdown should be treated with the same suspicion as an emergency
exception that relaxes a gate under pressure.

Future governance should therefore prefer pre-registered personal
capacity attestations over crisis-time revisions. RE-032.1 does not
define the approval mechanism, but records the risk explicitly.

Relationship with Human Approval:

-   Personal Capacity may belong partly or entirely inside Human
    Approval.
-   If so, it should be treated as an approval prerequisite rather than a
    parallel technical gate.
-   If some parts are computable and others attested, future design must
    preserve that separation.
-   Gate combination cannot be finalized until Personal Capacity is
    classified.

Prohibited shortcuts:

-   Do not convert Personal Capacity into an opaque confidence score.
-   Do not average verifiable facts with attested judgement.
-   Do not treat a missing attestation as favorable.
-   Do not treat crisis-time risk tolerance revisions as equally reliable
    as pre-registered attestations.
-   Do not allow attractive market evidence to compensate for inadequate
    Personal Capacity.

Open questions:

-   Which Personal Capacity facts can be verified from existing records?
-   Which facts require manual entry?
-   Which dimensions require explicit human attestation?
-   Should attestations expire?
-   Should crisis-time attestation changes require a cooling-off period
    or second approval?
-   Does Personal Capacity participate in gate-combination logic, or does
    it sit inside Human Approval before any capital action is allowed?

Boundary:

-   No code changed.
-   No thresholds are defined.
-   No personal-capacity taxonomy is finalized.
-   No capital posture mapping is implemented.
-   No operative wiring is authorized.
-   Personal Capacity is not yet classified as a gate.

------------------------------------------------------------------------

## RE-033.1 — Capital Posture vocabulary and ordering

RE-033.1 formalizes the Capital Posture vocabulary and ordering.
It is documentation-only.

This iteration does not implement posture logic. It defines the ordered
posture ceiling that future gates may cap.

Ordered posture states:

From most restrictive to least restrictive:

1.  `Conserve`
2.  `Prepare`
3.  `Deploy Partially`
4.  `Deploy Aggressively`

`Blocked` is not part of this ordered scale. It is an orthogonal veto.

State definitions:

### Conserve

No new exposure.

No Dry Powder deployment.

No Portfolio Reallocation outside routine rebalances already scheduled
outside this SOP process.

`Conserve` is the fail-closed floor.

### Prepare

No new exposure.

No Dry Powder deployment.

No Portfolio Reallocation.

`Prepare` may authorize planning, identifying funding sources,
redirecting future contributions to cash or preparing Dry Powder
capacity.

It does not authorize selling existing strategic positions unless a
future Dry Powder Protocol explicitly allows it.

### Deploy Partially

Authorizes deploying a bounded fraction of available Dry Powder into the
identified opportunity.

RE-033.1 does not define that fraction.

Portfolio Reallocation remains governed by its own future protocol.
Deploying Dry Powder does not automatically authorize reallocating
existing positions.

### Deploy Aggressively

Authorizes deploying the maximum Dry Powder amount allowed by future
protocols.

It does not automatically authorize Portfolio Reallocation.

Dry Powder deployment and Portfolio Reallocation remain independent
authorizations with their own gates.

### Blocked

Orthogonal veto.

`Blocked` overrides any ordered posture state.

It must carry an explicit reason, following the explanation standard
already required from the Evidence Quality Gate.

It may be activated by any future gate or by human approval governance,
provided the reason is documented.

Rule 1 — gate state to posture ceiling:

A gate's internal state must first map to a posture ceiling for that
gate.

Current mapping:

-   `not measurable` caps at `Conserve`;
-   `conservative` caps at `Conserve`.

These two states have the same posture ceiling today but different
explanations:

-   `not measurable` means required measurement is missing;
-   `conservative` means the gate was measured but does not authorize a
    less restrictive ceiling.

This preserves the project-wide rule: absence of evidence is not `0.0`.

Rule 2 — combining posture ceilings:

Future gate combination must operate on posture ceilings, not raw
internal scores.

Among ordered posture states, the most restrictive ceiling wins.

If `Blocked` is active, `Blocked` wins over all ordered states.

Worked current-state inference:

Current known gate states:

-   Evidence Quality: `not measurable`;
-   Regime Comparability: `not measurable`;
-   Personal Capacity: not classified / unavailable;
-   `Blocked`: false unless explicitly activated.

Documentation-level inference:

    Final capital posture ceiling: Conserve

This is a documentation-level inference, not executable logic. No
Capital Posture Engine exists yet.

Open question:

Can any gate permit `Prepare` while Evidence Quality remains
`not measurable`, or is measurable Evidence Quality a prerequisite for
any posture above `Conserve`?

RE-033.1 records this question for future gate-combination work. It does
not answer it.

Boundary:

-   No code changed.
-   No posture engine is implemented.
-   No gate combination logic is implemented.
-   No thresholds are defined.
-   No Dry Powder Protocol rules are implemented.
-   No Portfolio Reallocation Protocol rules are implemented.
-   No operative wiring is authorized.

------------------------------------------------------------------------

## RE-034.1 — Gate combination boundary

RE-034.1 defines the boundary for combining gate outputs into a final
Capital Posture ceiling.

It is documentation-only.

No posture engine is implemented.

Combination inputs:

Future combination logic must not consume scores.

It should consume discrete gate outputs such as:

-   gate name;
-   gate internal state;
-   posture ceiling;
-   `Blocked` flag;
-   explanation.

The combination layer must operate on posture ceilings and veto flags,
not raw confidence or validation scores.

Combination order:

1.  If any gate or human approval control activates `Blocked`, final
    output is `Blocked`.
2.  If `Blocked` is not active, combine ordered posture ceilings by
    taking the most restrictive ceiling.

Ordered posture scale:

    Conserve < Prepare < Deploy Partially < Deploy Aggressively

Non-deployment vs deployment:

RE-034.1 separates non-deployment postures from deployment postures.

Non-deployment postures:

-   `Conserve`
-   `Prepare`

Deployment postures:

-   `Deploy Partially`
-   `Deploy Aggressively`

Evidence Quality prerequisite:

Evidence Quality not measurable blocks deployment.

It does not, by itself, necessarily block `Prepare`.

Reason:

`Prepare` does not commit capital. It authorizes planning and
preparation only. Deployment states commit capital based on evidence.
Therefore measurable Evidence Quality is a hard prerequisite for
`Deploy Partially` or `Deploy Aggressively`, but not necessarily for
`Prepare`.

Asymmetric unavailable-gate treatment:

This exception applies to Evidence Quality only.

Unavailable Regime Comparability caps at `Conserve`.

Unavailable Personal Capacity, while still unclassified, caps at
`Conserve` as a placeholder.

Reason:

Evidence Quality uncertainty means the system does not know how much to
trust the expected-return evidence. That blocks capital deployment but
does not necessarily block preparation.

Regime Comparability uncertainty means the system does not know whether
the current situation is structurally comparable enough to historical
precedents to justify any reaction.

Personal Capacity unavailability means the system does not know whether
the person can act responsibly at all.

Those uncertainties are more fundamental than uncertainty about the
return estimate, so they cap at `Conserve` until measured or classified.

Current gate-ceiling mapping:

-   Evidence Quality `not measurable` -> `Prepare`;
-   Evidence Quality `conservative` -> `Conserve`;
-   Regime Comparability `not measurable` -> `Conserve`;
-   Personal Capacity unavailable / unclassified -> `Conserve`;
-   Any `Blocked` flag -> `Blocked`.

This mapping is provisional and documentary. It exists to make the
current architecture auditable before implementation.

Worked current-state inference:

Current known states:

-   Evidence Quality: `not measurable` -> `Prepare`;
-   Regime Comparability: `not measurable` -> `Conserve`;
-   Personal Capacity: unavailable / unclassified -> `Conserve`;
-   `Blocked`: false unless explicitly activated.

Combination:

    min(Prepare, Conserve, Conserve) = Conserve

Documentation-level result:

    Final capital posture ceiling: Conserve

This is a documentation-level inference, not executable logic. No
Capital Posture Engine exists yet.

Personal Capacity placeholder:

Personal Capacity is included in the worked example only as an
unavailable placeholder.

RE-032.1 has not classified Personal Capacity as a parallel gate, Human
Approval prerequisite or mixed control. Future combination logic must be
revised after that classification.

Open questions:

-   Can `Prepare` ever be authorized solely by Regime Comparability while
    Evidence Quality remains `not measurable`?
-   Should Regime Comparability have its own non-deployment exception in
    future, or is `not measurable -> Conserve` permanent?
-   Does Personal Capacity belong in gate combination, or inside Human
    Approval before any capital action is considered?
-   How should explanations be composed when several gates cap posture at
    the same level?

Boundary:

-   No code changed.
-   No posture engine is implemented.
-   No gate combination logic is implemented.
-   No thresholds are defined.
-   No Dry Powder Protocol rules are implemented.
-   No Portfolio Reallocation Protocol rules are implemented.
-   No Human Approval implementation is added.
-   No operative wiring is authorized.

------------------------------------------------------------------------

## RE-034.2 — Gate combination first-code acceptance criteria

RE-034.2 defines acceptance criteria for the first isolated
gate-combination code.

It is documentation-only.

No posture engine is implemented.

Purpose:

The first code change must make the RE-034.1 combination boundary
testable without connecting it to the operative SOP flow.

It must model structure, ordering and explanations only.

It must not implement thresholds, protocols or automatic capital action.

Required behavior:

1.  `Blocked` wins before any ordered-posture comparison.

    If any gate or human approval control marks `Blocked`, the combined
    result must be `Blocked` regardless of all posture ceilings.

2.  Without `Blocked`, the most restrictive posture ceiling wins.

    The ordered scale is:

        Conserve < Prepare < Deploy Partially < Deploy Aggressively

3.  The current real-state anchor must be pinned as a regression test.

    With today's known gate states:

    -   Evidence Quality: `not measurable` -> `Prepare`;
    -   Regime Comparability: `not measurable` -> `Conserve`;
    -   Personal Capacity: unavailable / unclassified -> `Conserve`;
    -   `Blocked`: false.

    The combined output must be exactly:

        Conserve

    This test protects the worked RE-034.1 example from becoming only
    prose.

4.  Evidence Quality must not override more restrictive gates.

    A test must verify that if Evidence Quality authorizes up to
    `Deploy Aggressively` but Regime Comparability or Personal Capacity
    caps at `Conserve`, the combined output remains `Conserve`.

    This prevents the Evidence Quality exception from being misread as
    Evidence Quality dominance.

5.  Evidence Quality `not measurable` must not be flattened back to
    `Conserve`.

    A test must verify that:

    -   Evidence Quality: `not measurable` -> `Prepare`;
    -   Regime Comparability: `Deploy Aggressively`;
    -   Personal Capacity: `Deploy Aggressively`;
    -   `Blocked`: false.

    The combined output must be:

        Prepare

    This protects the RE-034.1 distinction between preparation and
    deployment from regression.

6.  Unavailable Regime Comparability must cap at `Conserve`.

    A test must verify that unavailable or `not measurable` Regime
    Comparability caps the combined result at `Conserve`, even if other
    gates allow less restrictive posture.

7.  Unavailable Personal Capacity must cap at `Conserve` while its role
    remains unclassified.

    A test must verify the placeholder behavior documented in RE-034.1.
    Future work may revise this after Personal Capacity is classified,
    but the first code must not silently assume it is favorable.

8.  Explanations must preserve traceability.

    The combined output must identify which gate or control caused the
    final ceiling or `Blocked` result.

    A generic explanation such as "insufficient evidence" is not enough.
    The explanation must name the specific limiting gate or control, for
    example:

    -   `Regime Comparability: not measurable`;
    -   `Personal Capacity: unavailable`;
    -   `Evidence Quality: not measurable, deployment blocked`;
    -   `Human Approval: blocked`.

9.  Inputs must be discrete.

    The combination function must consume posture ceilings, `Blocked`
    flags and explanations. It must not consume raw scores,
    `confidence.score`, MAE, hit-rate, rank correlation or any other
    validation metric directly.

Required isolation:

The first code change may add an isolated combination module and a
verification test.

It must not be wired into:

-   `run.py`;
-   `DecisionEngine`;
-   `AssessmentEngine`;
-   `ValidationEngine`;
-   Frozen Core.

Automatic rejection criteria:

A future PR fails RE-034.2 if it:

-   connects combination logic to the operative flow;
-   changes Frozen Core;
-   consumes raw scores instead of discrete gate ceilings;
-   treats Evidence Quality as dominant over the other gates;
-   maps Evidence Quality `not measurable` directly to `Conserve`;
-   treats unavailable Regime Comparability as favorable;
-   treats unavailable Personal Capacity as favorable;
-   returns a final posture without naming the limiting cause;
-   implements thresholds;
-   implements Dry Powder Protocol rules;
-   implements Portfolio Reallocation Protocol rules;
-   implements Human Approval.

Boundary:

-   No code changed.
-   No posture engine is implemented.
-   No gate combination logic is implemented.
-   No thresholds are defined.
-   No protocol rules are implemented.
-   No operative wiring is authorized.

------------------------------------------------------------------------

## RE-034.4 — Gate combination implementation status

RE-034.4 documents the status after the first isolated
gate-combination code.

It is documentation-only.

Implemented in RE-034.3:

-   `engine/gate_combination.py`;
-   `tests/verify_gate_combination.py`.

Verified command:

    python3 tests/verify_gate_combination.py

Verified output:

    GATE COMBINATION : STABLE

What now exists:

-   discrete Capital Posture constants:
    `Conserve`, `Prepare`, `Deploy Partially`,
    `Deploy Aggressively`, `Blocked`;
-   ordered posture comparison for non-blocked gates;
-   `Blocked` precedence over posture ordering;
-   discrete gate-combination input objects;
-   combined result with traceable explanations;
-   regression coverage for today's documentary state:
    Evidence Quality `not measurable`, Regime Comparability
    `not measurable`, Personal Capacity unavailable / unclassified and
    `Blocked=false` combine to `Conserve`;
-   regression coverage for the Evidence Quality asymmetry:
    Evidence Quality `not measurable` caps at `Prepare`, not `Conserve`,
    when the other gates allow less restrictive posture;
-   regression coverage proving that Evidence Quality does not override
    a more restrictive Regime Comparability or Personal Capacity cap.

What does not exist:

-   no Capital Posture Engine;
-   no automatic recommendation;
-   no thresholds;
-   no Dry Powder Protocol rules;
-   no Portfolio Reallocation Protocol rules;
-   no Human Approval implementation;
-   no adapter from live gate outputs into the combination layer;
-   no operative wiring.

Operative boundary:

`engine/gate_combination.py` exists in the repository.

It does not participate in the `run.py` execution path.

It is not called by `DecisionEngine`.

It is not called by `AssessmentEngine`.

It is not called by `ValidationEngine`.

It does not consume `confidence.score`.

It does not consume MAE, hit-rate, rank correlation or any raw
Research Validation metric.

Current posture inference:

The documented current-state inference remains:

    min(Prepare, Conserve, Conserve) = Conserve

This is still an architectural inference and test fixture.

It is not an executable SOP recommendation.

Next implementation boundary:

Future work may define adapters from actual gate outputs into
`GateCombinationInput`.

That future work must remain isolated unless a later numbered iteration
explicitly authorizes operative wiring.

Boundary:

-   Documentation updated only.
-   No code changed in RE-034.4.
-   No posture engine is implemented.
-   No thresholds are defined.
-   No protocol rules are implemented.
-   No operative wiring is authorized.

------------------------------------------------------------------------

## RE-PRED.1 — Predictive validity boundary

RE-PRED.1 opens the predictive-validity block.

It does not demonstrate predictive capacity.

It defines what would have to be true before the SOP may claim that the
Research Engine has predictive validity.

It is documentation-only.

No code changed.

No new calculation is executed.

No new validation claim is made.

Purpose:

The Research Engine currently produces objective, reproducible and
explainable historical evidence.

Current Research Validation does not yet show reliable predictive
discrimination:

-   rank correlation is weakly negative;
-   hit-rate is not discriminating because the evaluated forecasts lack
    meaningful sign variation;
-   MAE lacks a sufficiently specified naive baseline comparison;
-   the nominal sample size is not the independent effective sample size.

RE-PRED.1 therefore separates engineering validity from predictive
validity.

Engineering validity means the pipeline is reproducible and
methodologically consistent.

Predictive validity means the forecasts demonstrate useful out-of-sample
relationship to future realized outcomes, against pre-defined baselines,
with uncertainty reported.

RE-PRED.1 only defines the boundary for that second claim.

Predictive target audit:

Before freezing a predictive target, the project must audit what the
current code actually calculates.

At minimum, the audit must establish:

-   which return field is evaluated today;
-   whether the return is nominal or real;
-   whether it is price return or total return;
-   whether the horizon is exactly five years or convention-dependent;
-   which date anchors start and end the realized-return window;
-   whether missing future returns are excluded, imputed or treated as
    unavailable;
-   whether validation evaluates absolute return, excess return, rank or
    direction.

The future target must either match the current operative calculation or
explicitly authorize a change.

It must not diverge from implementation by accident.

Predictive claims:

Predictive validity must be decomposed into separate claims.

1.  Ranking validity.

    Higher forecasts should tend to correspond to higher realized
    outcomes.

    Rank correlation is the natural diagnostic surface for this claim.

    Ranking validity may be useful even if exact magnitudes are not yet
    calibrated.

2.  Calibration validity.

    Forecast magnitudes should resemble realized magnitudes better than
    pre-defined naive magnitude estimates.

    This is a stronger claim than ranking validity.

3.  Directional validity.

    Forecast sign should carry useful information only when the sample
    has meaningful sign variation.

    A high hit-rate with almost no negative forecasts is not, by itself,
    predictive evidence.

Future model-validation state may need to represent these claims
separately. A single `validated` / `not validated` string may be too
coarse if ranking improves before calibration.

Validation surfaces:

Future predictive validation must separate at least three surfaces.

1.  Existing historical backtest.

    This is useful for diagnostics, reproducibility and failure-mode
    discovery.

    It is not fully clean out-of-sample evidence because the Similarity
    Engine was designed while exposed to the historical dataset.

2.  Prospective holdout from the freeze date.

    A clean holdout cannot be created retroactively from data already
    used to design, inspect or iterate the model.

    Any historical holdout claim must therefore be treated cautiously.

    A genuinely clean holdout starts only after the model, dataset
    cutoff, target, metrics and baselines are frozen.

3.  Live tracking.

    Live tracking is the slowest but most honest evidence source.

    It should begin as soon as the logging protocol is defined, even if
    the later evaluation horizon takes years to mature.

Model freeze requirement:

No holdout or live-tracking result may count as clean predictive evidence
unless the evaluated model was frozen before the forecast was observed.

The freeze must include:

-   code version or commit;
-   dataset cutoff;
-   feature definitions;
-   similarity dimensions;
-   similarity weights;
-   episode-selection rules;
-   forecast horizon;
-   target definition;
-   metrics;
-   baselines;
-   missing-data rules.

Changing the model after seeing validation results makes the affected
sample exploratory again.

Without this freeze, validation risks becoming p-hacking with extra
steps.

Baseline requirement:

Predictive claims must be compared against pre-defined naive baselines.

RE-PRED.1 does not define pass/fail thresholds.

It requires future work to specify baselines before evaluation.

Candidate baselines include:

-   unconditional historical mean or median;
-   constant forecast equal to the full historical universe expected
    return;
-   zero-return or no-change forecast where appropriate to the target;
-   simple mean-reversion rule based on drawdown depth, without
    similarity matching.

The model does not become predictive merely by beating one trivial
baseline.

Future validation must explain which baseline each claim is tested
against and why that comparison is appropriate to the target.

Uncertainty requirement:

No future metric should be interpreted from its point estimate alone.

Given the known dependence documented in RE-025.6, RE-025.8 and
RE-025.9, uncertainty estimates must respect dependence between
observations.

An i.i.d. bootstrap is not sufficient by default.

Future work should consider block-aware resampling or another method
that preserves overlapping outcome windows and repeated forecast groups.

Effective sample size:

The current `n=19` is an operational count, not an independent sample
size.

RE-PRED future work should move from qualitative warning to quantitative
effective-sample-size estimation where feasible.

Until then, predictive claims must remain conservative.

Live tracking log:

Future live tracking should be append-only.

The minimum record should include:

-   timestamp;
-   model commit or version;
-   dataset cutoff;
-   snapshot inputs;
-   forecast horizon;
-   forecast summary;
-   forecast distribution or match-return distribution;
-   selected matches;
-   Evidence Quality state;
-   Regime Comparability state if available;
-   Personal Capacity state if available;
-   combined posture ceiling if available;
-   human approval state if available;
-   whether any action was taken;
-   later realized outcome when available.

The purpose is to know, years later, exactly what was forecast, by which
model, using which data, and under which governance state.

No gate relaxation in RE-PRED.1:

RE-PRED.1 does not authorize any relaxation of Evidence Quality, Regime
Comparability, Personal Capacity or Capital Posture.

It does not set numeric thresholds.

It does not change the current posture inference.

If future predictive evidence remains weak:

The project must treat permanent weak predictive evidence as a named
design branch, not as an implementation failure.

If predictive validity never becomes demonstrable, the Research Engine
may remain a descriptive and contextual evidence system rather than a
forecast-backed deployment engine.

In that scenario, any future capital deployment would need a different
transparent justification framework. It should not pretend to be backed
by predictive validation that does not exist.

RE-PRED.1 does not decide that branch.

It records it as a probable architectural question for future
constitutional governance if the evidence does not improve.

Boundary:

-   No code changed.
-   No new calculations executed.
-   No new metrics introduced.
-   No target frozen yet.
-   No model frozen yet.
-   No holdout created yet.
-   No live-tracking log implemented.
-   No predictive-validity claim made.
-   No gate threshold changed.
-   No capital posture mapping changed.
-   No operative wiring authorized.

------------------------------------------------------------------------

## RE-PRED.2 — Predictive target audit

RE-PRED.2 audits the predictive target currently implemented by code.

It does not freeze the target.

It does not change the target.

It is documentation-only.

No code changed.

No new validation claim is made.

Audited code path:

-   `engine/drawdown_engine.py`;
-   `engine/evidence_engine.py`;
-   `engine/validation_harness.py`;
-   `engine/validation_metrics.py`;
-   `engine/research_pipeline.py`;
-   `models/evidence.py`;
-   `models/episode.py`;
-   `models/observable_episode.py`;
-   `tests/verify_validation_metrics.py`.

Current target field:

The operative five-year predictive target is:

    future_return_5y

It is stored on `Episode` and `ObservableEpisode`.

It is generated by:

    enrich_future_returns()

using:

    _future_return(df, bottom_date, years=5)

Current target formula:

`_future_return()` computes:

    (p1 / p0) ** (1 / years) - 1

Therefore the current target is an annualized CAGR, not a cumulative
multi-year return.

Return unit:

Returns are decimal annualized rates.

Example:

    0.1138667635

means approximately 11.39% annualized, not 11.39% cumulative over five
years.

Price source:

The code uses:

    Price.1

from the Shiller data frame.

`P` is used to detect drawdowns and recovery against historical price
levels.

`Price.1` is used for:

-   future returns;
-   pre-crash return;
-   rolling volatility input.

The code comment labels `_future_return()` as:

    CAGR real anualizado. No retorno acumulado.

Based on the Shiller column layout inspected in the source file,
`Price.1` appears to be the real total-return price index rather than
raw nominal price. RE-PRED.2 does not rename or re-map that column; it
records the current implementation and leaves formal source-column
aliasing for future work if needed.

Date anchors:

The start anchor is:

    bottom_date

For p0, `_future_return()` selects the first row with:

    Date >= bottom_date

For p1, it sets:

    future_date = bottom_date + years

and selects the first row with:

    Date >= future_date

The realized-return window therefore starts at the drawdown bottom and
ends at the first available Shiller observation at or after the target
horizon date.

Missing future returns:

`_future_return()` returns `None` when:

-   no future row exists at or after `bottom_date + years`;
-   no bottom row exists at or after `bottom_date`;
-   p0 is `None`;
-   p0 is zero.

There is no imputation.

There is no conversion of missing outcome to 0.0.

This is consistent with the Evidence rule that absence of evidence is
`None`, never zero.

Evidence forecast surface:

`EvidenceEngine.build(matches, years=5)` reads:

    future_return_5y

from each selected match.

It drops `None` values.

It sorts the realized return sample.

It sets:

-   `average_return`;
-   `median_return`;
-   `worst_return`;
-   `best_return`;
-   `positive_probability`;
-   Evidence v2 return-shape fields.

`median_return` is calculated through `percentile_from_sorted(returns,
0.50)`, not through `statistics.median()`.

The forecast used by current Research Validation is:

    evidence.median_return

Current validation actual:

`ValidationHarness.evaluate_episode(episode, years=5)` reads:

    actual = episode.future_return_5y

The harness then reconstructs the historical snapshot at the episode
bottom, builds comparable matches through the same
ObservableUniverse -> SimilarityEngine -> EvidenceEngine path, and
compares:

    forecast = evidence.median_return
    actual = episode.future_return_5y

Evaluability:

A validation record is evaluable only when both values exist:

    forecast is not None and actual is not None

Records with missing actual or missing forecast remain visible in the
harness but do not enter MAE, directional hit-rate or rank correlation.

Current validation surfaces:

The current metrics evaluate the same target in different ways:

-   MAE evaluates absolute error between forecast CAGR and realized CAGR;
-   directional hit-rate evaluates sign agreement, excluding zero
    forecast or zero actual;
-   rank correlation evaluates whether higher forecast CAGR ranks
    correspond to higher realized CAGR ranks.

The current validation does not evaluate:

-   excess return versus a baseline;
-   cumulative five-year return;
-   nominal return;
-   price-only return;
-   total-return attribution separately;
-   calibration by forecast quantile.

Current horizon:

The shared Research pipeline defaults to:

    horizon_years = 5

Evidence supports other stored horizons, but the current canonical
Research Validation metrics and SOP evidence surface use the five-year
horizon.

Current mature-outcome status:

The current dataset contains 23 drawdown episodes.

At the five-year horizon:

-   21 episodes have realized `future_return_5y`;
-   19 records are evaluable by the Research Validation harness;
-   2022.10 has no realized five-year return yet;
-   2025.04 has no realized five-year return yet.

Important distinction:

RE-PRED.2 audits the implemented target.

It does not decide that this target is the correct future governance
target.

Future work must explicitly decide whether the frozen predictive target
should remain:

    annualized real total-return CAGR from drawdown bottom to five years

or whether SOP governance requires a different target.

If a different target is chosen, that must be a numbered architectural
change, not a silent validation change.

Open questions:

-   Should `Price.1` be formally aliased in code or documentation as the
    real total-return price index?
-   Should governance evaluate real total return, real price return,
    nominal return, or excess return?
-   Should the target remain annualized CAGR or become cumulative return?
-   Should target windows use first observation at or after horizon date,
    nearest observation, or exact monthly alignment?
-   Should missing future outcomes remain `None` only, or should live
    tracking distinguish "not yet matured" from "missing data"?
-   Should future validation evaluate the same target for all gates, or
    should Evidence Quality, Regime Comparability and Capital Posture use
    different target surfaces?

Boundary:

-   No code changed.
-   No target frozen.
-   No metric changed.
-   No validation result changed.
-   No baseline introduced.
-   No holdout introduced.
-   No live-tracking log introduced.
-   No gate threshold changed.
-   No capital posture mapping changed.
-   No operative wiring authorized.

------------------------------------------------------------------------

## RE-PRED.3 — Target freeze decision boundary

RE-PRED.3 defines the decision boundary for freezing the predictive
target.

It does not freeze the model.

It does not create a holdout.

It is documentation-only.

No code changed.

Decision:

The currently implemented target remains the provisional freeze
candidate:

    future_return_5y

Defined operationally as:

    annualized 5-year CAGR from drawdown bottom,
    calculated from Shiller `Price.1`,
    using the first available observation at or after bottom_date + 5.

Reason:

The target is already implemented and consumed consistently by:

-   `EvidenceEngine`;
-   the shared Research pipeline;
-   `AssessmentEngine`;
-   Research Validation.

Changing the target before model freeze would create a new divergence
risk between code, validation and documentation.

The correct next step is therefore not to redesign the target silently,
but to treat the implemented target as the provisional candidate while
documenting what remains unresolved.

Not yet verified:

RE-PRED.3 does not claim that `Price.1` is definitively:

-   real rather than nominal;
-   total-return rather than price-only.

RE-PRED.2 established that the code uses `Price.1`.

It did not formally verify the semantic meaning of that column.

The phrase "real total-return" must therefore not be used as a settled
property of the frozen target until the Shiller source-column semantics
are verified.

Required future verification:

Before definitive target freeze, the project must verify the meaning of
`Price.1` by inspecting the official Shiller dataset structure or
another authoritative source for the spreadsheet columns.

The verification must decide whether `Price.1` should be formally
documented as:

-   real price index;
-   real total-return index;
-   nominal price index;
-   nominal total-return index;
-   or another source-specific construct.

Until then, the provisional target should be described as:

    annualized 5-year CAGR from `Price.1`

not as:

    annualized real total-return CAGR

CAGR vs cumulative return:

The provisional target remains annualized CAGR, not cumulative
five-year return.

This preserves consistency with the current code and validation metrics.

However, this choice changes how existing error metrics must be read.

MAE reinterpretation:

The canonical MAE reported by Research Validation is an error over
annualized CAGR.

It is not an error over cumulative five-year return.

Therefore:

    MAE ~= 7.03%

means approximately 7.03 percentage points of annualized-rate error, not
7.03 percentage points of total five-year outcome error.

Over a five-year compounding window, an annualized error can imply a
larger cumulative-outcome difference.

Any future governance discussion must preserve that distinction.

Absolute vs excess return:

RE-PRED.3 does not decide whether predictive validation should ultimately
evaluate absolute return or excess return versus a baseline.

That decision belongs with baseline design.

Until baselines are defined, the provisional target remains the absolute
implemented target:

    future_return_5y

Bottom-date anchor:

The provisional start anchor remains:

    bottom_date

This is consistent with the current Research Validation harness, which
asks what the system would have forecast at the drawdown bottom.

RE-PRED.3 does not authorize changing the anchor to peak date, recovery
date, signal date or action date.

Maturity vs missingness:

The code currently represents unavailable future outcomes as `None`.

That remains correct.

Future live tracking should distinguish:

-   not yet matured;
-   structurally missing data;
-   unavailable because of source failure.

RE-PRED.3 does not implement that distinction.

Freeze status:

The target is not definitively frozen.

It is designated as the provisional freeze candidate.

Definitive target freeze requires at minimum:

-   verification of `Price.1` semantics;
-   explicit decision on annualized vs cumulative return;
-   explicit decision on absolute vs excess return;
-   explicit decision on bottom-date anchor;
-   explicit missing-outcome taxonomy for live tracking;
-   numbered documentation recording the freeze.

Boundary:

-   No code changed.
-   No target definitively frozen.
-   No model frozen.
-   No holdout created.
-   No baseline introduced.
-   No validation result changed.
-   No gate threshold changed.
-   No capital posture mapping changed.
-   No operative wiring authorized.

------------------------------------------------------------------------

## RE-PRED.4 — Source column semantics verification

RE-PRED.4 verifies the semantic meaning of the Shiller source column
used by the current predictive target.

It is documentation-only.

No code changed.

Verified source:

The verification was performed against the real project file:

    data/raw/shiller.xlsx

using the workbook header rows that `shiller_loader.py` skips with:

    header=7

The inspected header area was:

    rows 4-8

No merged cells were present in that header area, so each header label
belongs to its exact column.

Verified column mapping:

Column H is loaded by pandas as:

    Price

Its stacked header labels are:

    row 7: Real
    row 8: Price

Therefore column H is:

    Real Price

Column J is loaded by pandas as:

    Price.1

because the visible row-8 label `Price` is duplicated and pandas
deduplicates the second occurrence.

Its stacked header labels are:

    row 5: Real
    row 6: Total
    row 7: Return
    row 8: Price

Therefore column J / `Price.1` is:

    Real Total Return Price

Result:

The inference recorded in RE-PRED.2 is now verified.

`Price.1` is the Shiller Real Total Return Price column.

Current predictive target semantics:

The currently implemented target:

    future_return_5y

is therefore:

    annualized real total-return CAGR
    from drawdown bottom
    over the five-year horizon
    using Shiller Real Total Return Price

This confirms:

-   real rather than nominal;
-   total return rather than price-only;
-   annualized CAGR rather than cumulative return.

What remains provisional:

RE-PRED.4 verifies source-column semantics.

It does not definitively freeze the predictive target.

It does not decide whether SOP governance should ultimately prefer:

-   absolute return or excess return;
-   annualized CAGR or cumulative return;
-   bottom-date anchor or another action anchor.

Those decisions still require numbered future iterations.

Documentation correction:

Future references may describe the current implemented target as:

    annualized real total-return CAGR from drawdown bottom

They should still distinguish:

-   current implemented target;
-   provisional freeze candidate;
-   definitive frozen target.

MAE interpretation:

The RE-PRED.3 MAE reinterpretation remains valid.

The canonical MAE is error over annualized real total-return CAGR, not
cumulative five-year real total return.

Boundary:

-   No code changed.
-   No target definitively frozen.
-   No metric changed.
-   No validation result changed.
-   No baseline introduced.
-   No holdout introduced.
-   No live-tracking log introduced.
-   No gate threshold changed.
-   No capital posture mapping changed.
-   No operative wiring authorized.

------------------------------------------------------------------------

## RE-PRED.5 — Target freeze acceptance criteria

RE-PRED.5 defines acceptance criteria for any future definitive target
freeze.

It does not freeze the target.

It does not freeze the model.

It is documentation-only.

No code changed.

Purpose:

The project must not freeze a predictive target just because the current
implementation already exists.

It may use the implemented target as the provisional freeze candidate,
but definitive freeze requires an ordered set of decisions and
verifications.

Ordered dependency structure:

The target-freeze criteria are not a flat checklist.

They have dependencies.

Future work must respect this order.

1.  Target mechanics and semantics.

    The project must first verify what the target means mechanically and
    economically.

    Already verified:

    -   `future_return_5y` uses `Price.1`;
    -   `Price.1` is Shiller Real Total Return Price;
    -   the return is annualized CAGR;
    -   the horizon is five years;
    -   missing mature outcomes remain `None`, never 0.0.

    Not yet audited:

    -   how `bottom_date` is selected;
    -   how drawdown episodes are detected;
    -   how episode start, bottom and recovery are delimited;
    -   whether the bottom-detection algorithm is the correct target
        anchor for predictive governance.

    Therefore "target semantically verified" is not fully complete yet.
    Source-column semantics are verified; bottom-detection semantics are
    not.

2.  Target unit and horizon decision.

    The project must decide whether the definitive target remains:

        annualized real total-return CAGR over five years

    or whether governance requires a different unit or horizon.

    This must be decided before baselines are designed.

3.  Absolute vs excess-return decision.

    The project must decide whether predictive validation evaluates:

    -   absolute realized return; or
    -   excess return over a baseline.

    This decision must come before baseline design.

    A baseline used only for comparison is not the same as a baseline
    subtracted from the target.

4.  Baseline design.

    Baselines may only be defined after the absolute-vs-excess decision.

    If the target remains absolute return, baselines are comparators.

    If the target becomes excess return, a baseline becomes part of the
    target construction.

    RE-PRED.5 therefore prohibits closing baseline design before the
    absolute-vs-excess target decision is explicit.

5.  Missingness taxonomy.

    The target freeze must distinguish at least:

    -   not yet matured;
    -   structurally missing data;
    -   unavailable because of source failure.

    Current code uses `None`, which remains correct as a representation
    of unavailable outcome. Future live tracking needs a richer
    explanation layer so that different `None` causes do not collapse
    into one state.

6.  Model freeze reference.

    RE-PRED.5 does not redefine the model freeze checklist.

    The authoritative freeze checklist is the one defined in RE-PRED.1.

    Future target-freeze work must reference that checklist rather than
    duplicating it.

    This avoids two competing sources of truth for what "frozen model"
    means.

7.  Target unfreeze criteria.

    A frozen target must not be reopened because early validation
    results are disappointing.

    Reopening a target after observing results would convert future
    validation into exploratory analysis unless the reason was
    pre-authorized.

    Acceptable future unfreeze reasons may include:

    -   discovered source-data error;
    -   verified source-column mapping error;
    -   discovered target-construction bug;
    -   authoritative change in the source dataset structure;
    -   documented governance decision that the target no longer matches
        the SOP objective.

    Unacceptable unfreeze reasons include:

    -   poor validation performance;
    -   desire to improve MAE after seeing results;
    -   desire to improve hit-rate after seeing results;
    -   desire to improve rank correlation after seeing results;
    -   market pressure or urgency.

Acceptance criteria for definitive target freeze:

A future target-freeze PR or documentation iteration is acceptable only
if it:

-   states the target field;
-   states the target formula;
-   states the source column and verified source-column semantics;
-   states the start anchor;
-   states the end anchor;
-   states the horizon;
-   states annualized vs cumulative unit;
-   states absolute vs excess-return choice;
-   states missingness taxonomy;
-   references the RE-PRED.1 model-freeze checklist;
-   states target unfreeze criteria;
-   explicitly confirms that no validation results were used to tune the
    target after freeze evaluation began.

Current status:

The implemented target remains the provisional freeze candidate.

It is not definitively frozen.

The main blocker is no longer `Price.1` semantics.

The remaining blockers are:

-   bottom-detection / episode-boundary audit;
-   absolute vs excess-return decision;
-   baseline design after that decision;
-   missingness taxonomy;
-   formal freeze / unfreeze governance.

Boundary:

-   No code changed.
-   No target definitively frozen.
-   No model frozen.
-   No baseline introduced.
-   No holdout created.
-   No live-tracking log introduced.
-   No validation result changed.
-   No gate threshold changed.
-   No capital posture mapping changed.
-   No operative wiring authorized.

------------------------------------------------------------------------

## RE-PRED.6 — Bottom detection / episode boundary audit

RE-PRED.6 audits how the current code selects `bottom_date` and defines
drawdown episodes.

It is documentation-only.

No code changed.

Audited code:

    engine/drawdown_engine.py

Audited functions:

-   `calculate_running_peak()`;
-   `calculate_drawdown()`;
-   `detect_drawdowns()`;
-   `filter_episodes()`;
-   `enrich_recovery()`;
-   `_future_return()`.

Current definitions:

Peak:

`RunningPeak = P.cummax()`.

The peak is the cumulative historical maximum of nominal price `P` up to
the current row.

`detect_drawdowns()` updates the active peak whenever:

    Drawdown == 0

Drawdown:

`calculate_drawdown()` computes:

    (P - RunningPeak) / RunningPeak

Therefore drawdown severity is measured against nominal price `P`, not
against `Price.1`.

Episode start:

An episode starts when the system is outside a drawdown episode and:

    Drawdown <= MIN_DRAWDOWN

with:

    MIN_DRAWDOWN = -0.10

At that moment, the code stores the prior full-recovery peak as
`peak_before` and initializes the bottom as the current row.

Bottom:

While an episode is active, the bottom is updated whenever:

    row["Drawdown"] < bottom["Drawdown"]

The bottom is therefore the most negative drawdown observed inside the
active episode.

Recovery:

Recovery is detected when:

    Drawdown == 0

The episode is appended only in that recovery branch.

This means recovered drawdowns are included, but an unrecovered drawdown
still active at the end of the dataset is structurally excluded.

Duration:

`duration_months` is currently calculated as:

    int(round((bottom_date - peak_date) * 12))

Recovery months:

`recovery_months` is currently calculated as:

    int(round((recovery_date - bottom_date) * 12))

Target anchor:

`_future_return()` starts the predictive target window from:

    bottom_date

not from:

-   the -10% trigger date;
-   the peak date;
-   recovery date;
-   action date;
-   human approval date.

Confirmed limits:

-   The drawdown threshold is hardcoded at -10%.
-   Episode detection uses nominal price `P`.
-   Future return uses `Price.1`.
-   The model learns only from drawdowns that later recovered.
-   The target starts at the final bottom, not at the first trigger.

Verified finding 1 — price-basis asymmetry:

Episode detection and target measurement use different price bases.

Drawdown detection uses:

    P

which is nominal price.

Target returns use:

    Price.1

which RE-PRED.4 verified as Real Total Return Price.

Therefore:

-   what counts as a drawdown episode is measured on nominal price;
-   what the model later predicts is measured on real total return.

This is a real methodological asymmetry.

RE-PRED.6 does not decide whether it is wrong.

It records that definitive target freeze must explicitly accept,
reject or redesign this asymmetry.

Verified finding 2 — unrecovered drawdowns are structurally excluded:

`drawdowns.append(...)` exists only inside the recovery branch of
`detect_drawdowns()`.

Therefore an active drawdown that has not returned to `Drawdown == 0` by
the end of the dataset never becomes an `Episode`.

It is never available to:

-   `ObservableUniverse`;
-   `SimilarityEngine`;
-   `EvidenceEngine`;
-   Research Validation.

The current dataset run contains 23 episodes and all have
`recovery_date`.

So this property does not currently create a missing active episode in
the produced episode list.

But it is structural: the model's historical universe consists only of
crises that eventually recovered.

Verified finding 3 — duration arithmetic bug:

The current code subtracts dates encoded as floats in `YYYY.MM` format.

That arithmetic is not calendar-month arithmetic.

This affects:

-   `duration_months`;
-   `recovery_months`.

A data check against the current dataset found discrepancies in all 23
episodes when compared with true calendar-month arithmetic.

Example:

    peak:   1929.09
    bottom: 1932.06

Current code:

    36 months

Calendar-month calculation:

    33 months

The observed recovery-month discrepancy reaches up to 7 months.

Severity:

This is a verified bug, not merely a methodological question.

It affects fields currently produced by the system:

-   `Episode.duration_months`;
-   `Episode.recovery_months`;
-   `Evidence.average_recovery_months`;
-   `Evidence.median_recovery_months`.

It affects Similarity directly because `duration_months` participates in
duration scoring and also in speed scoring through `abs(drawdown) /
duration_months`.

RE-PRED.6 does not fix the bug.

It records it as a required follow-up before definitive target freeze or
any governance reliance on recovery-duration evidence.

Implications for target freeze:

RE-PRED.6 completes part of the bottom-anchor audit, but it does not
clear the target for definitive freeze.

Remaining blockers include:

-   deciding whether nominal-price drawdown detection is acceptable for a
    real-total-return target;
-   deciding whether unrecovered drawdowns should remain structurally
    excluded;
-   fixing or formally accepting the date-arithmetic bug;
-   re-verifying any affected canonical metrics after the bug decision.

Boundary:

-   No code changed.
-   No bug fixed.
-   No target definitively frozen.
-   No model frozen.
-   No baseline introduced.
-   No holdout created.
-   No validation result changed.
-   No gate threshold changed.
-   No capital posture mapping changed.
-   No operative wiring authorized.

------------------------------------------------------------------------

## RE-BUG.1 — Calendar-month duration bug acceptance criteria

RE-BUG.1 defines acceptance criteria for fixing the date-arithmetic bug
identified in RE-PRED.6.

It is documentation-only.

No code changed.

Bug classification:

This is a verified implementation bug.

It is not a methodology question.

The current code calculates calendar durations by subtracting floats in
`YYYY.MM` format:

    int(round((bottom_date - peak_date) * 12))
    int(round((recovery_date - bottom_date) * 12))

That is not calendar-month arithmetic.

Affected fields:

-   `Episode.duration_months`;
-   `Episode.recovery_months`;
-   `Evidence.average_recovery_months`;
-   `Evidence.median_recovery_months`.

Directly affected behavior:

-   Similarity duration scoring, because `episode.duration_months` is
    compared directly against `snapshot.duration_months`;
-   Similarity speed scoring, because `snapshot_speed` is calculated as
    `abs(drawdown) / duration_months`.

This means the bug is not limited to recovery-statistic fields.

Correcting duration arithmetic may change the actual match set selected
by `SimilarityEngine.top()`.

Priority:

This bug must be near the head of the code-fix queue.

Reason:

It already affects public Research / Evidence outputs.

Any future consumer of Evidence recovery statistics could read those
fields without knowing they are wrong.

Required fix behavior:

The future fix must calculate month distance from `YYYY.MM` encoded
dates by converting year and month components explicitly.

For two dates:

    start = YYYY.MM
    end   = YYYY.MM

the correct month distance must be:

    (end_year - start_year) * 12 + (end_month - start_month)

The fix must not use direct float subtraction.

Required examples:

The future test must include at least:

    1929.09 -> 1932.06 = 33 months

This case currently returns 36 months.

The test should also include a same-year cross-month case and a
multi-year case whose month component decreases.

Required regression scope:

The future verification must prove:

-   all 23 current drawdown episodes have calendar-correct
    `duration_months`;
-   all recovered episodes have calendar-correct `recovery_months`;
-   no duration uses float date subtraction;
-   `Evidence.average_recovery_months` and
    `Evidence.median_recovery_months` are recalculated from corrected
    `recovery_months`;
-   the fix does not change `future_return_5y`;
-   the fix does not change source-column semantics;
-   the fix does not change episode threshold logic;
-   the fix does not change the nominal-price vs real-total-return
    asymmetry documented in RE-PRED.6.
-   the fix compares today's selected match identifiers before and after
    the correction.

Expected downstream impact:

Because `duration_months` participates in two active Similarity
dimensions, correcting it may change:

-   selected matches;
-   Evidence return statistics;
-   Evidence Quality local inputs;
-   Research Validation metrics.

Such changes are acceptable if caused by corrected duration arithmetic.

They must be reported explicitly in the future fix iteration.

They must not be hidden as unrelated regression noise.

If selected matches do not change, that fact must be reported explicitly
as well.

The future fix must not assume that canonical numbers survive unchanged:

-   `Evidence.return_count`;
-   `Evidence.median_return`;
-   `Evidence.worst_return`;
-   `Evidence.best_return`;
-   Research Validation MAE;
-   directional hit rate;
-   rank correlation.

Required tests:

The future code change should add or update a focused verification test.

Minimum assertions:

-   date-to-month conversion helper returns correct values;
-   1929.09 to 1932.06 returns 33;
-   every produced episode has corrected `duration_months`;
-   every recovered episode has corrected `recovery_months`;
-   public Evidence recovery statistics are based on corrected values;
-   today's top-match identifiers are compared before and after the fix;
-   `verify_research_engine.py` passes after the fix;
-   `verify_assessment_engine.py` passes after the fix;
-   `verify_validation_metrics.py` is rerun after the fix, with expected
    values updated only if changed matches or corrected arithmetic explain
    the difference;
-   the existing Research pipeline still runs.

Rejected shortcuts:

-   Do not patch only the 1929 case.
-   Do not round float differences differently.
-   Do not keep using `YYYY.MM` float subtraction.
-   Do not silently update canonical validation numbers without
    explaining whether changed Similarity matches caused the change.
-   Do not assume Similarity is unaffected without comparing match
    identifiers.
-   Do not combine this bug fix with target-freeze, baseline, holdout or
    gate-threshold work.

Boundary:

-   No code changed in RE-BUG.1.
-   No bug fixed yet.
-   No target changed.
-   No episode-detection redesign authorized.
-   No price-basis asymmetry decision made.
-   No unrecovered-drawdown decision made.
-   No validation metrics recalculated.
-   No operative wiring authorized.

------------------------------------------------------------------------

## RE-BUG.3 — Calendar-month duration fix impact record

RE-BUG.3 documents the impact of the RE-BUG.2 code fix.

It is documentation-only.

No code changed.

Fix status:

RE-BUG.2 fixed the verified calendar-month duration bug by adding
centralized date arithmetic and replacing direct `YYYY.MM` float
subtraction in `engine/drawdown_engine.py`.

The fix introduced:

-   `engine/date_utils.py`;
-   corrected `duration_months` calculation;
-   corrected `recovery_months` calculation;
-   `tests/verify_duration_arithmetic.py`;
-   updated canonical Research, Assessment and Research Validation
    verification expectations.

Verification status:

The post-fix pinned-runtime verification passes:

-   `tests/verify_duration_arithmetic.py`;
-   `tests/verify_research_engine.py`;
-   `tests/verify_assessment_engine.py`;
-   `tests/verify_validation_metrics.py`.

Forward-looking documentation rule:

The pre-fix canonical values remain part of project history.

They must not be silently rewritten.

From RE-BUG.2 onward, the post-fix values below are the official
current canonical values.

Current snapshot match set:

The current `SimilarityEngine.top()` match identifiers, expressed as
`bottom_date`, are:

    [
        2018.12,
        1998.09,
        1966.10,
        2020.03,
        1960.10,
        1990.10,
        2022.10,
        1962.06,
        1880.05,
        1903.10,
    ]

Current Evidence / Research canonical values:

-   `Evidence.median_return`: `0.10192496249726091`;
-   `Evidence.worst_return`: `-0.01091948933252962`;
-   `Evidence.best_return`: `0.13767334934864284`;
-   `Evidence.return_count`: `9`;
-   `Evidence.positive_count`: `8`;
-   `Evidence.negative_count`: `1`;
-   `Evidence.zero_count`: `0`;
-   `Evidence.non_positive_probability`: `0.1111111111111111`;
-   `Evidence.return_spread`: `0.14859283868117246`.

Current Assessment canonical values:

-   `expected_return_5y`: `0.10192496249726091`;
-   `upside_potential`: `0.13285520801656237`;
-   `downside_risk`: `-0.01091948933252962`;
-   `drawdown_zone`: `NORMAL`;
-   `matches`: `10`.

Current Research Validation canonical values:

-   `episodes`: `23`;
-   `sample_size`: `21`;
-   `evaluated_count`: `19`;
-   `mae`: `0.06928793787076225`;
-   `directional_hit_rate`: `0.9473684210526315`;
-   `rank_correlation`: `-0.26505171850684983`;
-   `overlap_pairs`: `10`;
-   `repeated_forecast_groups`: `5`.

Impact interpretation:

The fix corrected an objectively wrong duration calculation.

The change affected active Similarity scoring through both direct
duration scoring and speed scoring.

Therefore changes in selected matches, Evidence statistics and Research
Validation metrics are expected consequences of the corrected arithmetic,
not unrelated regressions.

Methodological interpretation:

The predictive-validity conclusion does not improve because of this fix.

The updated validation surface remains conservative:

-   rank correlation remains negative;
-   directional hit-rate remains non-discriminant;
-   the effective sample-size caveat remains unresolved;
-   Evidence Quality remains unable to justify capital deployment on
    predictive-validity grounds.

Boundary:

-   No target changed.
-   No target freeze authorized.
-   No baseline decision made.
-   No holdout policy changed.
-   No episode-detection redesign authorized.
-   No price-basis asymmetry decision made.
-   No unrecovered-drawdown decision made.
-   No gate threshold changed.
-   No operative wiring changed.

------------------------------------------------------------------------

## RE-DATA.1 — Shiller source update automation note

RE-DATA.1 records a future data-update capability.

It is documentation-only.

No code changed.

Current state:

The Shiller dataset is updated manually.

The local source file remains:

    data/raw/shiller.xlsx

Future capability:

A later iteration may add a controlled updater, for example:

    python3 tools/update_shiller_data.py

The updater may download the Shiller source workbook from the official
Shiller data site.

Boundary:

This must not be implemented as a blind download-and-overwrite step.

Any future automated update must:

-   download the source file to a temporary location first;
-   preserve or back up the previous local workbook;
-   verify the expected workbook structure;
-   verify that `Price.1` still maps to Real Total Return Price;
-   verify required columns before replacing local data;
-   verify that the latest observation is not older than the current
    local source;
-   run the loader / drawdown / research verification tests after the
    update;
-   log the source URL, update date, prior latest observation and new
    latest observation;
-   fail closed if validation does not pass.

Timing:

This is not a near-term priority.

It should be revisited after the RE-PRED target / baseline work is
closed, because changing data sources while target semantics are still
open would make validation harder to interpret.

Rejected shortcut:

Do not silently replace `data/raw/shiller.xlsx` from the network without
structural validation and test reruns.

------------------------------------------------------------------------

## RE-PRED.7 — Absolute vs Excess Return Boundary

RE-PRED.7 defines whether predictive validity should be evaluated
against absolute 5-year return, excess return over a naive baseline, or
both, in separate channels.

It is documentation-only.

No code changed.

Two channels, not one:

-   Absolute return channel: what happened after the drawdown bottom.
    This is the existing Evidence descriptive surface
    (`Evidence.median_return`, `future_return_5y`). No new field, no
    renamed field. Its purpose is descriptive evidence, not a
    predictive-validity claim by itself.
-   Excess return channel: whether the model's forecast adds value over
    a naive rule that requires no similarity matching. This is the
    future predictive-validity surface. It does not exist yet.

Motivation:

RE-025.3 already found that a rule that always predicts "positive"
produces almost the same directional hit rate as the current model,
because 0/19 forecasts were negative in the evaluated sample. A model
can score well on an absolute-return metric while adding no
discriminating value over a rule that ignores current conditions
entirely. Absolute-return metrics alone cannot distinguish those two
cases. Excess return can.

Primary baseline:

The primary baseline for excess return is the unconditional historical
mean/median `future_return_5y` across the full episode set, evaluated
point-in-time (same `ObservableUniverse` discipline as RE-025.1) so it
does not itself leak future information. This baseline answers the
sharpest question available today: does conditioning the forecast on
the current snapshot via `SimilarityEngine` add anything beyond "stocks
have historically gone up over 5 years"?

Secondary baselines, already named in RE-PRED.1, remain diagnostic, not
headline: constant full-universe forecast, zero/no-change, simple
mean-reversion. This is a mandatory-comparison requirement, not a
beat-all-four requirement.

Per-metric mechanics are not uniform:

-   MAE and directional hit-rate require an actual baseline forecast
    series to compute excess against. Excess MAE is baseline MAE minus
    model MAE (positive means the model beats the baseline). Excess
    hit-rate is defined analogously.
-   Rank correlation does not need a baseline forecast series. A
    constant-forecast baseline has no rank variation, so its rank
    correlation is undefined / zero by construction. The existing rank
    correlation value already tests whether the model's forecast
    ordering carries information beyond none. No new "excess"
    transformation is needed for this metric; this boundary states that
    explicitly so it is not built twice.

Placement:

Excess return is a Research Validation Harness concept, not an Evidence
concept. Evidence describes a live snapshot's matched sample and has no
"actual" to compare against; excess return is only computable in
backtest, across historical episodes with realized outcomes. This
iteration keeps that boundary explicit so no future implementation adds
baseline or excess-return logic into `models/evidence.py` or
`engine/evidence_engine.py`.

Expected outcome, stated in advance:

Given RE-025.3 (a trivial rule already matches the model's hit rate) and
RE-BUG.3 (rank correlation moved further negative after the duration
fix, not less negative), the most likely outcome once excess return is
actually computed (a future iteration) is that the primary baseline
matches or beats the model on at least one canonical metric. That
outcome, if it occurs, must be recorded plainly as a finding, not
softened or treated as an implementation problem to fix.

Rejected shortcuts:

-   Do not treat absolute-return metrics (current MAE, hit-rate, rank
    correlation) as if they already constitute predictive-validity
    evidence.
-   Do not compute excess return using a single blended baseline that
    mixes the four candidate baselines into one number.
-   Do not add baseline or excess-return fields to `Evidence` or
    `models/evidence.py`.
-   Do not apply the same excess-return transformation to rank
    correlation as to MAE / hit-rate.
-   Do not compute any baseline value in this iteration.

Boundary:

-   No code changed in RE-PRED.7.
-   No baseline value computed.
-   No excess-return metric implemented.
-   No target freeze changed.
-   No gate threshold changed.
-   No operative wiring changed.
-   No Evidence field added.

------------------------------------------------------------------------

## RE-PRED.8 — Primary baseline acceptance criteria

RE-PRED.8 defines acceptance criteria for computing the primary
excess-return baseline defined in RE-PRED.7. It also corrects
RE-PRED.7's rank-correlation claim forward.

It is documentation-only.

No code changed.

Correction to RE-PRED.7:

RE-PRED.7 stated that rank correlation "does not need a baseline
forecast series" because "a constant-forecast baseline has no rank
variation." That claim implicitly assumed a single global baseline
number computed once over the full 23-episode dataset. That design
would violate the point-in-time discipline established in RE-025.1 — it
would inform a 1907 episode's baseline with data from 2020, which did
not yet exist in 1907. The primary baseline, as specified below, is not
a single constant: it is a point-in-time expanding statistic that varies
per episode. It therefore does have rank variation, and its rank
correlation against realized outcomes is a real, computable comparison
against the model's rank correlation, not an undefined quantity. This
correction is recorded here rather than silently rewriting RE-PRED.7,
per RE-DOC-002.

Baseline definition:

For each evaluable episode `X`, with `bottom_date = t`:

    baseline_forecast(X) = median(future_return_5y) over
    ObservableUniverse(dataset, as_of=t).episodes(),
    excluding X by bottom_index

This reuses the exact same temporal-safety machinery already verified
for the model's own forecast in RE-025.1 (`ObservableUniverse`,
self-exclusion by `bottom_index`) — no new mechanism is introduced. The
only difference from the model's forecast is that the baseline is
unconditional: it does not pass through `SimilarityEngine.top()`, so it
does not condition on the current snapshot's similarity to `X`.

Statistic choice:

Median, not mean, is the primary baseline statistic. It matches the
model's own canonical statistic (`Evidence.median_return`), keeping the
comparison apples-to-apples. Mean may be recorded as a secondary
diagnostic, never as the headline comparator.

Sample alignment:

The baseline is evaluated over exactly the same evaluable record set
already established by `ValidationHarness` (today: 19 records). No
separate inclusion or exclusion criteria are invented for the baseline.
Using a different sample for baseline vs. model would bias the
comparison.

Metrics:

Three head-to-head comparisons against the model's existing canonical
metrics, side by side, not blended:

-   Baseline MAE vs model MAE (`0.06928793787076225`).
-   Baseline directional hit-rate vs model directional hit-rate
    (`0.9473684210526315`).
-   Baseline rank correlation vs model rank correlation
    (`-0.26505171850684983`).

Excess is reported as baseline MAE minus model MAE for MAE (lower is
better, so a positive excess means the model wins), and as model minus
baseline for hit-rate and rank correlation (higher is better, so a
positive excess means the model wins).

Deferred to a later iteration:

-   Secondary baselines (constant full-universe forecast, zero /
    no-change, simple mean-reversion) are not defined here. If the
    constant full-universe forecast is used later, it must be labeled
    explicitly as not point-in-time-safe and used as a diagnostic only,
    never as a headline comparator.
-   Actual baseline computation and values belong to the next code
    iteration, not to RE-PRED.8.

Rejected shortcuts:

-   Do not use a single global constant baseline computed once over all
    23 episodes.
-   Do not invent a separate evaluable-record definition for the
    baseline.
-   Do not use mean as the primary baseline statistic.
-   Do not blend MAE, hit-rate and rank correlation excess into one
    score.
-   Do not compute any baseline value in this iteration.

Boundary:

-   No code changed in RE-PRED.8.
-   No baseline value computed.
-   No excess-return metric implemented.
-   No secondary baseline defined.
-   No target freeze changed.
-   No gate threshold changed.
-   No operative wiring changed.

------------------------------------------------------------------------

## RE-PRED.9 — Primary baseline implementation

RE-PRED.9 implements the primary baseline defined in RE-PRED.8 in code.

New files:

-   `engine/baseline_harness.py` — `baseline_forecast()`, computing the
    point-in-time expanding median of `future_return_{years}y` by
    reusing `ObservableUniverse` and bottom_index self-exclusion, the
    same temporal-safety machinery already verified for the model's own
    forecast in RE-025.1; `BaselineHarness`, producing baseline
    `ValidationRecord`s aligned 1:1 with the model's, inheriting
    `evaluable` and `actual` directly rather than deciding its own
    inclusion criteria; `missing_baseline_forecast_count()`, an explicit
    diagnostic for the invariant below; `excess_summary()`, the
    head-to-head comparison required by RE-PRED.8, reusing
    `mean_absolute_error()`, `directional_hit_rate()` and
    `rank_correlation()` from `engine/validation_metrics.py`
    unmodified.
-   `tests/verify_baseline_harness.py` — functional smoke test.

No existing file was modified except `tests/verify_core.py`, which adds
`engine/baseline_harness.py` to its structural Engines list, following
the RE-025.7 precedent.

No Frozen Core component was touched. `ObservableUniverse`,
`SimilarityEngine`, `EvidenceEngine` and the existing metric functions
are consumed through their public interfaces exactly as published, the
same pattern already used to justify RE-025.1-RE-026.1.2 under the
Frozen Core Policy.

Invariant proven by construction, not merely observed:

If a model `ValidationRecord` is evaluable, its baseline counterpart
can never have `forecast=None`. The model's `SimilarityEngine.top()`
matches are drawn from `_comparable_episodes(dataset, episode)` — the
exact same unconditional pool this baseline uses without narrowing by
similarity. If at least one of the model's matches had a non-`None`
`future_return_{years}y` (a necessary condition for the model to be
evaluable), that same value is present in the baseline's pool. The
verification test checks this invariant explicitly via
`missing_baseline_forecast_count()` rather than assuming it holds.

Sample alignment, verified structurally:

-   `episodes = 23`, `sample_size = 21`, `evaluated_count = 19` — the
    existing canonical values, unchanged.
-   Baseline record count equals model record count.
-   Baseline evaluable count equals model evaluable count.
-   `missing_baseline_forecast_count = 0`.

Verification status:

`tests/verify_baseline_harness.py` was run outside the pinned runtime
only, to confirm the code executes without error and the structural
invariants above hold. It was not run under `requirements.txt`.

No baseline value is canonical yet. `mean_absolute_error()`,
`directional_hit_rate()` and `rank_correlation()` applied to the
baseline records produce real numbers in that non-pinned run, but
RE-025.5 already established that different pandas/numpy versions can
change these exact computations. Treating a non-pinned result as
canonical here would repeat, on new code, the same category of mistake
RE-BUG.2 spent an entire iteration correcting. The next iteration
(RE-PRED.10) records the canonical baseline values once
`tests/verify_baseline_harness.py` has been run and confirmed under the
pinned runtime.

Rejected shortcuts:

-   Do not treat a non-pinned execution result as canonical.
-   Do not hardcode `EXPECTED_*` baseline constants before pinned-runtime
    confirmation.
-   Do not modify `engine/validation_metrics.py` to special-case the
    baseline; reuse it unmodified.
-   Do not let the baseline invent its own evaluable set.

Boundary:

-   No Frozen Core component modified.
-   No existing file modified except `tests/verify_core.py` (structural
    list only).
-   No canonical baseline value established.
-   No secondary baseline implemented.
-   No target freeze changed.
-   No gate threshold changed.
-   No operative wiring changed.

------------------------------------------------------------------------

## RE-PRED.10 — Canonical baseline values and predictive-validity finding

RE-PRED.10 records the canonical primary baseline values, confirmed by
running `tests/verify_baseline_harness.py` under `RUNTIME : PINNED`
(`requirements.txt`), and the finding that follows from them.

It is documentation-only.

No code changed.

Structural verification, confirmed under the pinned runtime:

-   `episodes = 23`, `sample_size = 21`, `evaluated_count = 19`,
    `baseline_evaluated_count = 19`.
-   `missing_baseline_forecast_count = 0` — the invariant proven by
    construction in RE-PRED.9 (a baseline forecast can never be `None`
    when the corresponding model record is evaluable) holds empirically
    on the live dataset, not only in principle.

Canonical baseline values:

    model_mae:                 0.06928793787076
    baseline_mae:               0.06740858559979
    excess_mae:                -0.00187935227097

    model_hit_rate:             0.94736842105263
    baseline_hit_rate:          0.94736842105263
    excess_hit_rate:            0.00000000000000

    model_rank_correlation:    -0.26505171850685
    baseline_rank_correlation: -0.23171864780822
    excess_rank_correlation:   -0.03333307069863

Values are recorded to the fourteen decimal places produced by
`tests/verify_baseline_harness.py`'s own print formatting. This is the
precision actually captured from the pinned-runtime execution; it is
not re-derived to a higher precision.

Reading excess: for MAE, `excess_mae = baseline MAE - model MAE`,
positive meaning the model wins. For hit-rate and rank correlation,
`excess = model metric - baseline metric`, positive meaning the model
wins (RE-PRED.8/RE-PRED.9 convention).

Finding, stated plainly, as committed to in advance in RE-PRED.7 and
RE-PRED.8:

The model does not beat the primary baseline on any of the three
canonical metrics.

-   MAE: the baseline wins. Baseline error is 0.06741, model error is
    0.06929 — the baseline is closer to realized outcomes on average.
-   Directional hit-rate: exact tie. Both are 0.94737. This adds no new
    information beyond what RE-025.3 already established — a
    conditionless prediction of "positive" was already known to match
    the model's directional performance.
-   Rank correlation: the baseline wins. Baseline correlation is
    -0.23172, model correlation is -0.26505 — the model's ordering of
    forecast strength is further from informative than the baseline's,
    though both remain weakly negative.

Interpretation:

Conditioning the forecast on the current snapshot's similarity to
historical episodes, via `SimilarityEngine`, does not currently produce
a forecast that is more accurate, more discriminating, or better
ordered than simply taking the unconditional historical median of
comparable episodes observable at each point in time. On this canonical
19-record evaluated sample, predictive validity is not demonstrated
relative to this baseline.

This finding does not by itself prove `SimilarityEngine` conditioning
has no value under any circumstance — the evaluated sample remains
small, non-independent (RE-025.6, RE-025.8, RE-025.9), and only one
primary baseline has been tested. It does mean the burden of proof
established in RE-PRED.1 has not been met: this is not a case where
predictive validity is assumed to be a matter of time or more code. The
governing principle recorded at the start of the Predictive Validity
Boundary applies directly here: predictive validity must first be shown
to exist before any threshold or gate-relaxation design proceeds as if
it did.

Connection to Evidence Quality Gate:

This sharpens, but does not by itself change, the existing
`EvidenceQualityGate` state. RE-029.6 already recorded that the gate
starts conservative because current Research Validation does not yet
show reliable discriminatory power. This finding replaces that
qualitative judgment with a direct, head-to-head quantitative result:
not merely "hit-rate is non-discriminating and rank correlation is
weakly negative," but "the model loses to a naive baseline on two of
three canonical metrics and ties on the third." No gate threshold or
posture ceiling is changed by this iteration — RE-029.7's calibration
boundary still requires an explicit, pre-registered governance decision
before any gate state changes, and this finding argues for continued
conservatism, not relaxation.

Rejected shortcuts:

-   Do not soften this finding or reframe it as an implementation
    problem to fix.
-   Do not treat the exact directional hit-rate tie as if it were
    informative on its own, independent of RE-025.3's existing finding.
-   Do not use this finding to automatically change any gate threshold
    or capital posture ceiling.
-   Do not treat this single primary-baseline result as a final verdict
    on predictive validity; secondary baselines and a larger or
    differently-sampled evaluation remain open.

Boundary:

-   No code changed in RE-PRED.10.
-   No gate threshold changed.
-   No capital posture ceiling changed.
-   No target freeze changed.
-   No secondary baseline computed.
-   No operative wiring changed.

------------------------------------------------------------------------

## RE-PRED.10.1 — Deferred: `NOT_DEMONSTRATED` gate state proposal

A proposal was raised, immediately after RE-PRED.10, to formalize a
third `EvidenceQualityGate` output state, `NOT_DEMONSTRATED`, distinct
from `NOT_MEASURABLE` and `CONSERVATIVE`, taking precedence over local
input completeness (a globally disproven method cannot be rescued by a
well-measured local sample).

The proposal is deferred, not rejected, for three reasons:

-   It would rest on a single baseline comparison over a non-independent
    N=19 sample (RE-025.6, RE-025.8, RE-025.9) -- the same category of
    overreaction-to-one-data-point the project's robustness axiom exists
    to prevent.
-   `EvidenceQualityGate.evaluate()`'s current code already forces
    `NOT_MEASURABLE` today regardless of global state, because
    `independence_dispersion_measured` is hardcoded `False`
    (RE-030.1/RE-030.2). A new state would today produce the identical
    posture-ceiling consequence (`Conserve`, `Prepare` allowed) as the
    existing `not measurable` state -- no operative behavior depends on
    making the distinction yet.
-   Adding a new state touches the taxonomy `GateCombination` (RE-034)
    already consumes, before there is a concrete behavioral reason for
    treating it differently from `NOT_MEASURABLE`.

Explicit trigger for revisiting: once RE-PRED.11's secondary baselines
are confirmed under the pinned runtime, if the model loses to the full
set (primary, zero, mean-reversion) on a majority of canonical metrics,
the case for a formal `NOT_DEMONSTRATED` state becomes materially
stronger and should be reopened. If the model beats one or more
secondary baselines while only losing to the primary, the finding is
more nuanced and likely does not warrant a new top-level state --
sharper `explanations` text within the existing two-state model may be
sufficient instead.

Boundary:

-   No code changed.
-   No new gate state added.
-   No posture ceiling changed.
-   This is not a rejection of the underlying finding from RE-PRED.10 --
    only of formalizing it into gate architecture before a fuller
    evidentiary basis exists.

------------------------------------------------------------------------

## RE-PRED.11 — Secondary baselines implementation

RE-PRED.11 implements two secondary baselines in
`engine/baseline_harness.py`, to isolate whether the RE-PRED.10 finding
is an artifact of the primary baseline choice.

It extends an already-isolated, non-Frozen-Core file (RE-PRED.9). No
existing function in that file is modified. No other file changes.

New functions:

-   `zero_forecast(episode)` -- returns `0.0` unconditionally. No
    parameters, no dependency on `ObservableUniverse` or any comparable.
    By construction, `directional_hit_rate()` excludes `forecast == 0`
    records and `rank_correlation()` returns `None` when all forecasts
    are identical -- this baseline can only produce a signal in MAE.
    This is expected, not a defect.
-   `mean_reversion_forecast(episode)` -- returns `-episode.drawdown`.
    Coefficient 1, zero parameters fitted against history. Uses only
    `episode.drawdown`, an Event field already known at the episode's
    own bottom -- no comparable episodes, no calibration. Deliberately
    the simplest defensible definition of "reversion," not the only
    possible one: a history-calibrated version was rejected to avoid
    introducing a new overfitting risk inside what must remain a naive
    baseline.
-   `build_baseline_records(model_records, forecast_fn)` -- generic
    constructor for baselines that do not need `ObservableUniverse`.
    Same RE-PRED.8 rule as `BaselineHarness`: `evaluable` and `actual`
    are inherited directly from the model's own records, never decided
    separately for the baseline.

`tests/verify_secondary_baselines.py` re-asserts the existing canonical
model and primary-baseline values (RE-BUG.3, RE-PRED.10) as a regression
guard, asserts the expected `None` degeneracy of zero's hit-rate and
rank correlation, and prints the full three-way comparison table (model
/ primary baseline / zero / mean-reversion). It does not hardcode
canonical zero/mean-reversion values -- those require pinned-runtime
confirmation, the same discipline RE-PRED.9 established and RE-BUG.2
motivated.

Boundary:

-   No Frozen Core component modified.
-   No existing function modified.
-   No canonical secondary-baseline value established.
-   No gate state changed.
-   No target freeze changed.
-   No operative wiring changed.

------------------------------------------------------------------------

## RE-PRED.12 — Open question: sampling-noise robustness

RE-PRED.12 records an explicit open question that RE-PRED.11's
secondary baselines do not, and cannot, resolve.

It is documentation-only. No code changed.

Two distinct notions of robustness:

-   Baseline-choice robustness: is the RE-PRED.10 finding specific to
    the point-in-time expanding median, or does it hold against other
    naive baselines too? RE-PRED.11 answers this.
-   Sampling-noise robustness: are the excess differences observed
    (e.g. -0.00187935227097 excess MAE, -0.03333307069863 excess rank
    correlation from RE-PRED.10) distinguishable from chance, given that
    all evaluations share the same 19 evaluable records, already
    documented as non-independent through two channels (RE-025.6):
    overlapping realized 5-year outcome windows (RE-025.8) and repeated
    forecasts (RE-025.9)? RE-PRED.11 does not answer this -- every
    additional baseline is still scored against the same dependent
    19-record sample.

This is not a new discovery. It follows directly from RE-025.6, which
already declined to publish a numeric effective N. It is recorded here,
specifically, so that a favorable or unfavorable secondary-baseline
result is not mistaken for statistical confirmation either way.

What this explicitly does not authorize:

-   An i.i.d. bootstrap over the 19 records -- prohibited by RE-PRED.1's
    uncertainty requirement, which requires dependence-aware resampling,
    not naive resampling that ignores the known overlap and repeated-
    forecast structure.
-   Treating N=19 as if it were 19 independent observations for any
    significance statement.

This gap is not resolved by this iteration. It remains open, tracked
here, for future dependence-aware uncertainty work -- scope and method
not yet defined.

Boundary:

-   No code changed.
-   No statistical test implemented.
-   No effective-N value published.
-   No gate state changed.

------------------------------------------------------------------------

## RE-PRED.13 — Canonical secondary baseline values and full-picture finding

RE-PRED.13 records the canonical secondary-baseline values, confirmed
by running `tests/verify_secondary_baselines.py` under
`RUNTIME : PINNED`, and the full-picture finding that follows.

It is documentation-only. No code changed.

Structural verification, confirmed under the pinned runtime:

-   `episodes = 23`, `evaluated_count = 19` — unchanged.
-   `zero_hit_rate` and `zero_rank_correlation` are `None`, exactly as
    expected by construction (RE-PRED.11): `directional_hit_rate()`
    excludes `forecast == 0`, and `rank_correlation()` returns `None`
    when all forecasts are identical.
-   `missing_reversion_forecast_count = 0` — no evaluable model record
    produced a missing mean-reversion forecast.

Canonical secondary-baseline values:

    zero_mae:                       0.12749337012113
    reversion_mae:                  0.18158697149305
    excess_mae_vs_zero:             0.05820543225037
    excess_mae_vs_reversion:        0.11229903362229

    zero_hit_rate:                  None
    reversion_hit_rate:             0.94736842105263
    excess_hit_rate_vs_reversion:   0.00000000000000

    zero_rank_correlation:          None
    reversion_rank_correlation:     0.26315789473684
    excess_rank_correlation_vs_reversion: -0.52820961324369

Full comparison table (model, primary baseline from RE-PRED.10, zero,
mean-reversion):

    Metric              Model      Primary    Zero       Reversion
    MAE                 0.06929    0.06741*   0.12749    0.18159
    Directional hit-rate 0.94737   0.94737    None       0.94737
    Rank correlation    -0.26505   -0.23172*  None       0.26316*

    * beats the model on that metric

Finding, stated plainly:

The model is not uniformly dominated. It clearly beats zero and
mean-reversion on MAE — 0.06929 versus 0.12749 and 0.18159
respectively, a wide margin either way. It ties all measurable
baselines on directional hit-rate. Where it loses is rank correlation:
the primary baseline beats it by a moderate margin, and mean-reversion
beats it by a full sign flip — mean-reversion's rank correlation is
positive (0.26316), the model's is negative (-0.26505).

RE-PRED.10.1 trigger, evaluated explicitly:

RE-PRED.10.1 pre-registered a trigger for reopening the
`NOT_DEMONSTRATED` gate-state proposal: "if the model loses to the full
set (primary, zero, mean-reversion) on a majority of canonical
metrics." That condition does not hold — the model wins MAE against two
of the three baselines. The proposal remains deferred. Per
RE-PRED.10.1's own alternative, sharper `explanations` text within the
existing `NOT_MEASURABLE`/`CONSERVATIVE` states remains the appropriate
tool if this distinction needs to be made visible, not a new top-level
state.

Working hypothesis, registered but not authorized as fact:

Mean-reversion's positive rank correlation against the model's negative
one is a striking, specific result: drawdown depth alone, with no
comparables and no calibration, orders realized 5-year outcomes better
than `SimilarityEngine`'s multidimensional conditioning does on this
sample. One candidate explanation is signal dilution — blending
drawdown depth with duration, speed, CAPE, pre-crash return and
volatility (`SIMILARITY_WEIGHTS`, `core/constants.py`) may be
weighting away the single dimension carrying the strongest ordering
information, in favor of episodes that resemble the current snapshot
contextually without capturing the magnitude of the reversion. This is
recorded as a working hypothesis for future investigation, not a
diagnosis. No `SimilarityEngine` change is made or authorized by this
iteration — that component remains Frozen Core, and RE-021 already
establishes the evidentiary bar for touching it.

Mandatory caveat (per RE-PRED.12):

Both the +0.26316 and -0.26505 rank correlations above are computed
over the same 19 evaluable records already documented as
non-independent (RE-025.6, RE-025.8, RE-025.9). Neither figure is
established as distinguishable from sampling noise. This finding
sharpens the picture of what the model does on this sample; it does not
resolve, and must not be read as resolving, RE-PRED.12's open question.

Rejected shortcuts:

-   Do not read this as vindicating the model — it still loses to the
    primary baseline and to mean-reversion on rank correlation.
-   Do not read this as confirming `NOT_DEMONSTRATED` — the
    pre-registered trigger explicitly did not activate.
-   Do not treat the signal-dilution hypothesis as established; it is
    unauthorized speculation about mechanism, clearly labeled as such.
-   Do not treat +0.26316 or -0.26505 as stable, final values immune to
    sampling noise.

Boundary:

-   No code changed in RE-PRED.13.
-   No gate state changed.
-   No capital posture ceiling changed.
-   No `SimilarityEngine` change made or authorized.
-   No target freeze changed.
-   No operative wiring changed.

------------------------------------------------------------------------

## RE-PRED.14 — Similarity dimension diagnostic: signal-dilution hypothesis not supported

RE-PRED.14 adds an exploratory, read-only diagnostic to test the
signal-dilution hypothesis registered in RE-PRED.13, and records the
result confirmed under the pinned runtime.

New files:

-   `engine/dimension_diagnostic.py` -- `dimension_forecast()` isolates
    one active `SimilarityEngine` dimension at a time by re-sorting the
    already-computed per-dimension scores that
    `SimilarityEngine.compare()` returns, instead of the blended score
    `top()` uses. Applies the same `peak_date` recency cutoff as
    `top()`. Excludes `recovery` deliberately -- RE-021 already removed
    it from the combined score as a data-leakage fix, and this
    diagnostic has no business reopening that. `dimension_records()`
    produces `ValidationRecord`s aligned with the model's, inheriting
    `evaluable`/`actual` per the same RE-PRED.8 rule, with `evaluable`
    additionally requiring a non-`None` forecast -- unlike RE-PRED.9's
    primary baseline, a single-dimension top-10 is not guaranteed to
    contain a resolved outcome by construction, so this must be checked,
    not assumed.
-   `tests/diagnostic_similarity_dimensions.py` -- not a `verify_*.py`
    regression gate. Makes no canonical claim, asserts no expected
    values, prints a comparison table. Still enforces the pinned-runtime
    gate (RE-025.5) before printing anything, because the reproducibility
    rule applies regardless of whether the script is exploratory.

No Frozen Core component modified. `SimilarityEngine.compare()` is
consumed exactly as published, the same justification pattern already
used for RE-025.1 and RE-PRED.9.

A real bug was found and fixed during construction, not in
`SimilarityEngine`: sorting by `pre_crash_return_3y_score` raised
`TypeError` because that score is `None` for episodes without three
years of prior price history. Fixed by excluding `None`-scored
comparables from that dimension's ranking, mirroring exactly how
`SimilarityEngine._weighted_score()` already excludes `None` from the
blended score -- absence of a dimension's signal is not treated as
maximal dissimilarity.

Results, confirmed under `RUNTIME : PINNED`:

    Dimension                  Evaluated   MAE      Hit-rate   Rank corr.
    model (blended, RE-BUG.3)  19          0.06929  0.94737    -0.26505
    drawdown_score              19          0.06765  0.94737    -0.19692
    duration_score               19          0.07079  0.94737    -0.24916
    speed_score                  19          0.07049  0.94737    -0.20327
    cape_score                   19          0.06899  0.94737    -0.21701
    pre_crash_return_3y_score    19          0.06592  0.94737    -0.26353
    volatility_score              19          0.06740  0.94737    -0.23414
    mean-reversion (RE-PRED.13, ref.)        0.18159  0.94737     0.26316

All six dimensions returned `evaluated = 19`, matching the model -- in
this run, isolating a single dimension did not reduce the evaluable set,
though the module docstring records that this is not guaranteed in
general.

Finding, stated plainly:

The signal-dilution hypothesis, as registered in RE-PRED.13, is not
supported. If blending were diluting a real positive signal present in
one dimension, isolating that dimension should have recovered something
closer to mean-reversion's positive rank correlation. It did not: every
dimension in isolation remains negative, ranging from -0.19692
(drawdown, the closest to positive) to -0.26353 (pre_crash_return_3y,
effectively matching the blended model). No single active
`SimilarityEngine` dimension is the hidden source of mean-reversion's
advantage.

Revised working hypothesis, registered but not authorized as fact:

The gap may not be a weighting problem at all. Mean-reversion is a
direct, monotonic function of the query episode's own drawdown depth --
by construction, a larger drawdown always produces a larger forecast,
preserving rank order exactly. `SimilarityEngine`, even sorted by a
single dimension, still selects a top-10 nearest-neighbor set and
forecasts the median outcome of whichever historical episodes happen to
rank closest -- a mechanism that does not preserve the query's own rank
order the same way, regardless of which dimension drives the selection.
If this is correct, the gap is not fixable by reweighting dimensions; it
would require reconsidering whether nearest-neighbor selection is the
right conditioning mechanism at all -- a materially larger question,
explicitly out of scope for this iteration.

Caveat (per RE-PRED.12, with extra force):

Every column above is computed over an even smaller, still-dependent
slice of the same 23-episode dataset -- isolating a dimension does not
add independent observations. This is hypothesis generation, not
hypothesis confirmation. The revised hypothesis above is speculation
about mechanism, clearly labeled, not a finding.

Rejected shortcuts:

-   Do not treat this as confirming or ruling out any mechanism with
    statistical confidence.
-   Do not treat the revised hypothesis as established; it is
    unauthorized speculation, one plausible explanation among others.
-   Do not use this diagnostic's results to modify `SimilarityEngine`,
    `SIMILARITY_WEIGHTS`, or any Frozen Core component.
-   Do not treat per-dimension `evaluated = 19` as guaranteed in future
    runs or future datasets.

Boundary:

-   No Frozen Core component modified.
-   No `SimilarityEngine` change made or authorized.
-   No gate state changed.
-   No target freeze changed.
-   No operative wiring changed.

------------------------------------------------------------------------

## RE-PRED.15 — Dependence-aware cluster bootstrap

RE-PRED.15 closes the method gap opened in RE-PRED.12: whether the
excess differences observed against the primary baseline (RE-PRED.10)
and mean-reversion (RE-PRED.13) are distinguishable from sampling
noise, given that all 19 evaluable records are already documented as
non-independent through two channels (RE-025.6): overlapping realized
5-year outcome windows (RE-025.8) and repeated forecasts (RE-025.9).

New file: `engine/dependence_bootstrap.py`.

Method, agreed with Armando before implementation:

-   `independence_clusters(records)` partitions evaluable records into
    clusters via connected components over the union of two edge
    sources: pairs returned by `overlapping_outcome_windows()`
    (RE-025.8) and groups returned by `repeated_forecast_groups()`
    (RE-025.9). No new dependence criterion is introduced -- both edge
    sources are the same diagnostics already validated in RE-025.6/8/9,
    connected here for the first time. Clusters are returned as
    positions, not objects, so the same partition applies unchanged to
    any parallel `ValidationRecord` list sharing the same order --
    model, primary baseline (RE-PRED.9) or secondary baseline
    (RE-PRED.11) -- an invariant those modules already guarantee.
-   `cluster_bootstrap_ci()` resamples whole clusters with replacement,
    never individual records, preserving intra-cluster dependence
    instead of destroying it. This is the dependence-aware resampling
    RE-PRED.1 requires; an i.i.d. bootstrap over the 19 records remains
    explicitly prohibited (RE-PRED.12).
-   `cluster_bootstrap_paired_excess()` applies the identical cluster
    draw, in the same replica, to both model and baseline records
    before computing the excess -- not two independent bootstraps
    subtracted afterward. This preserves the paired variance structure
    that RE-PRED.10/11's excess figures already rely on (model and
    baseline are always evaluated on the same episodes, row for row).
-   One fixed cluster partition, built once from the model's own
    records, is reused for every bootstrap in this iteration --
    standalone and paired. Outcome-window overlap (RE-025.8) is
    episode/horizon-based and therefore identical for the model and
    both baselines; repeated-forecast grouping (RE-025.9) is
    model-specific by construction (it reflects `SimilarityEngine.top()`
    match-set structure, which neither baseline shares), and using the
    model's partition uniformly is what makes "paired" resampling
    well-defined across all three series.
-   Seed and replicate count are fixed constants, not free script
    parameters: `BOOTSTRAP_SEED=42`, `BOOTSTRAP_REPLICATES=5000`.
    Percentile interval fixed at (5, 95) -- a 90% interval, an explicit
    design choice, not the only possible one.
-   A bootstrap replica where a metric function returns `None` (e.g.
    `rank_correlation()` degenerating when a resample happens to
    produce identical forecasts) is excluded from that metric's
    percentile, not treated as `0.0` -- the same absence-of-evidence
    rule used throughout this module. `valid_replicates` is reported
    explicitly alongside every interval.

New test file: `tests/diagnostic_dependence_bootstrap.py` -- not a
`verify_*.py` regression gate. Asserts no expected values. Still
enforces the pinned-runtime gate (RE-025.5) before printing anything.
Reports, for MAE / hit-rate / rank correlation: the model's own
interval, the primary and mean-reversion baselines' intervals, and the
paired excess interval against each. Zero baseline is explicitly out
of scope for this iteration -- RE-PRED.13 already found it loses to
the model on MAE by a wide, unambiguous margin; only primary and
mean-reversion were flagged as open by RE-PRED.12.

`tests/verify_core.py` adds `engine/dependence_bootstrap.py` to its
structural Engine checks, per the RE-025.7/RE-PRED.9 precedent.

Structural smoke test, run outside the pinned runtime -- not
canonical: 4 independence clusters over the 19 evaluable records,
sizes `[10, 7, 1, 1]`. If this holds under the pinned runtime, it
confirms directly what RE-025.6/8/9 already implied qualitatively:
`n=19` behaves, for dependence purposes, much closer to a handful of
independent observations than to 19.

The bootstrap itself uses no pandas/numpy -- pure stdlib `random` with
a fixed integer seed, which is version-stable. The same reproducibility
discipline applies regardless (RE-025.5): interval values are not
canonical until confirmed under the pinned runtime, and no source of
non-determinism is assumed absent just because the arithmetic doesn't
touch the pinned-version-sensitive libraries.

What this does not authorize:

-   No `SimilarityEngine`, `EvidenceEngine` or `ObservableUniverse`
    change.
-   No gate-state change.
-   No reinterpretation of RE-PRED.13's point-estimate finding until
    the confidence intervals are confirmed under the pinned runtime.
-   No claim, yet, about whether any excess interval does or does not
    straddle zero -- that is exactly what pinned-runtime confirmation
    will determine, recorded in a future iteration.

Boundary:

-   Two new files: `engine/dependence_bootstrap.py`,
    `tests/diagnostic_dependence_bootstrap.py`.
-   `tests/verify_core.py` updated to recognize the new engine file.
-   No Frozen Core component modified.
-   No existing metric function
    (`mean_absolute_error`/`directional_hit_rate`/`rank_correlation`)
    modified or reimplemented.
-   No gate state changed.
-   No operative wiring changed.
-   No canonical interval values published yet -- pending pinned-runtime
    confirmation, to be recorded in a future iteration.

------------------------------------------------------------------------

## RE-PRED.16 — Canonical dependence-aware bootstrap values

RE-PRED.16 records the canonical results of RE-PRED.15's bootstrap,
confirmed by running `tests/diagnostic_dependence_bootstrap.py` under
`RUNTIME : PINNED`, closing RE-PRED.12's open question.

It is documentation-only. No code changed.

Cluster structure, confirmed:

    independence_clusters: 3
    cluster_sizes (desc): [10, 8, 1]

This differs from the 4 clusters (`[10, 7, 1, 1]`) seen in RE-PRED.15's
unpinned structural smoke test. Hand-verified against the already-
canonical RE-025.8 overlap pairs and RE-025.9 repeated-forecast groups:
tracing the union of both edge sets by hand over the 19 evaluable
records produces exactly the 10-node and 8-node components reported
here, plus one untouched singleton -- confirming the pinned result, not
the sandbox one. The discrepancy is attributed to the sandbox's
unpinned environment producing slightly different underlying forecast
values, which changes `repeated_forecast_groups()`'s exact-float-
equality grouping -- not a defect in the new bootstrap code. This is
the same discipline RE-025.5 already established, now demonstrated
concretely: even code that touches no pandas/numpy directly can surface
environment-dependent results, because it consumes forecasts computed
upstream by code that does.

Canonical bootstrap results (seed=42, replicates=5000, 90% interval):

    Metric      Series                          [low, high]              valid
    MAE         model                           [0.05796, 0.07982]       5000/5000
    MAE         primary baseline (RE-PRED.10)   [0.05440, 0.07937]       5000/5000
    MAE         mean-reversion (RE-PRED.13)     [0.14151, 0.22008]       5000/5000
    MAE         excess vs primary               [-0.00356, -0.00045]    5000/5000
    MAE         excess vs mean-reversion        [0.08355, 0.14025]       5000/5000

    hit-rate    model                           [0.88235, 1.00000]       5000/5000
    hit-rate    primary baseline                [0.88235, 1.00000]       5000/5000
    hit-rate    mean-reversion                  [0.88235, 1.00000]       5000/5000
    hit-rate    excess vs primary               [0.00000, 0.00000]       5000/5000
    hit-rate    excess vs mean-reversion        [0.00000, 0.00000]       5000/5000

    rank_corr   model                           [-0.51587, -0.12759]    4814/5000
    rank_corr   primary baseline                [-0.54100, -0.06691]    4814/5000
    rank_corr   mean-reversion                  [0.20362, 0.42683]       4814/5000
    rank_corr   excess vs primary               [-0.06068, 0.02514]     4814/5000
    rank_corr   excess vs mean-reversion        [-0.94270, -0.34208]    4814/5000

`valid_replicates` for rank correlation is 4814/5000 (96.3%) -- the
remaining replicas degenerate to `None` when a resample happens to
produce identical forecasts or actuals, excluded per the module's
absence-of-evidence rule, not imputed.

Finding, stated plainly, per metric:

MAE. The model's small loss to the primary baseline (RE-PRED.10:
excess -0.00188) is real, not noise -- the 90% interval is entirely
negative and does not straddle zero, though the margin itself is
small. The model's large win over mean-reversion (RE-PRED.13) is also
real and robust -- the interval is entirely positive, no ambiguity.

Hit-rate. The exact tie holds under resampling at every percentile
computed, against both baselines. This metric has no discriminating
power on this sample, confirmed, not just observed once.

Rank correlation -- the metric RE-PRED.13 flagged as the model's
weakest point. Two different answers for two different comparisons:

-   Vs. the primary baseline: NOT distinguishable from sampling noise.
    The 90% interval `[-0.06068, 0.02514]` straddles zero. RE-PRED.13's
    "the primary baseline beats the model on rank correlation" finding
    does not survive dependence-aware resampling -- it could be
    sampling noise given how few independent clusters actually exist.
-   Vs. mean-reversion: distinguishable from sampling noise, and
    strongly so. The 90% interval `[-0.94270, -0.34208]` is entirely
    negative, nowhere near zero. RE-PRED.13's full sign-flip finding
    (`+0.26316` vs `-0.26505`) is robust to the known dependence
    structure -- it is not an artifact of treating 19 dependent records
    as if they were independent.

This is RE-PRED.12's open question, answered concretely: baseline
choice matters for how much confidence a finding deserves. The primary-
baseline rank-correlation loss was real-looking but turns out to be
noise-fragile; the mean-reversion sign-flip was equally real-looking
and turns out to be robust. Neither could have been told apart from the
point estimates alone -- that is exactly why RE-PRED.12 refused to let
either be read as resolved until this iteration.

Rejected shortcuts:

-   Do not read the primary-baseline rank-correlation result as
    "resolved in the model's favor" -- "not distinguishable from noise"
    is not the same as "the model is fine on this metric."
-   Do not read the mean-reversion rank-correlation result as
    strengthened beyond what it already was -- RE-PRED.13's point
    estimate already showed the sign flip; this iteration confirms it
    is not a sampling artifact, nothing more.
-   Do not treat the hit-rate tie as informative about predictive
    quality -- it was already known to carry no signal in this
    comparison (RE-PRED.11/13); this iteration only confirms the tie is
    stable under resampling.
-   Do not extrapolate these intervals to a different N, dataset, or
    universe -- they are specific to the current 23-episode dataset and
    its current dependence structure.

Boundary:

-   No code changed in RE-PRED.16.
-   No `SimilarityEngine` change made or authorized.
-   No gate state changed.
-   No capital posture ceiling changed.
-   No operative wiring changed.
-   No target freeze changed.

------------------------------------------------------------------------

## RE-035.1 — Close EvidenceQualityGate's remaining stub inputs

RE-035.1 closes the two hardcoded stubs in `engine/evidence_quality_gate.py`
identified while scoping governance work: `independence_dispersion_measured`
was always `False`, and `predictive_validation_status` only special-cased
the literal string `"validated"`, collapsing every other case -- including
a formally tested-and-not-demonstrated result -- into the same generic
"not validated" explanation.

First finding, before any code: fixing these stubs does not, by itself,
change today's system-level capital posture. RE-034.1 already documents
that Regime Comparability Gate and Personal Capacity Boundary being
entirely unbuilt (0% -- boundary docs only) caps posture at `Conserve`
regardless of what Evidence Quality says. That remains the real
bottleneck; RE-035.1 is correctness work on Evidence Quality Gate, not a
fix to the visible decision output.

Changes:

-   `_overlapping_match_pairs(evidence)` -- new function. Counts pairs
    within the CURRENT match set (`evidence.matches`) whose outcome
    windows (`bottom_date` .. `bottom_date + horizon_years`) overlap.
    Same boolean definition as RE-025.8's `overlapping_outcome_windows()`,
    reimplemented rather than reused: that function takes
    `ValidationRecord` (offline backtesting, one `horizon_years` per
    record), this takes `Similarity` matches sharing one
    `evidence.horizon_years` -- different enough types that forcing a
    shared function would need a more convoluted adapter than a small
    parallel implementation. Fourth controlled duplication of this
    pattern in the project (validation_harness, baseline_harness,
    dimension_diagnostic already reimplement the analogous
    `ObservableUniverse`/`bottom_index` exclusion for the same reason).
-   `LocalEvidenceQualityInputs.overlapping_match_pairs: Optional[int]` --
    new field, so the measurement is exposed, not silently discarded
    behind a bare boolean.
-   `build_local_evidence_quality_inputs()` now sets
    `independence_dispersion_measured=True` and
    `overlapping_match_pairs=<real count>`, computed from the actual
    match set, instead of hardcoding `False`.
-   `PREDICTIVE_VALIDATION_NOT_DEMONSTRATED = "not_demonstrated"` -- new
    recognized input value for `predictive_validation_status`. Does not
    add a new gate output state -- `EvidenceQualityGate.evaluate()` still
    only returns `NOT_MEASURABLE` or `CONSERVATIVE`, per RE-PRED.10.1's
    explicit decision to sharpen explanations rather than add a third
    state. When this value is passed, `evaluate()` now appends a specific
    explanation ("evaluated under a pre-registered protocol, required
    advantage not shown") instead of the generic "not validated" one.
    The module holds no RE-PRED-specific numbers -- it is the caller's
    responsibility to decide when this value applies, keeping the gate
    structure decoupled from any one research finding.
-   `tests/verify_evidence_quality_gate.py` updated: the hardcoded
    `False` expectation is replaced with a real-value check; a new case
    exercises the `not_demonstrated` path explicitly.

Structural verification: a synthetic smoke test (three mock episodes,
one overlapping pair) confirmed `_overlapping_match_pairs()` and the new
`evaluate()` branch behave as designed before any pinned-runtime check.

Confirmed under `RUNTIME : PINNED`, real pipeline, real match set:

    independence_dispersion_measured: True
    overlapping_match_pairs: 5
    state (predictive_validation_status=PREDICTIVE_VALIDATION_NOT_DEMONSTRATED):
        not measurable
    explanations: ["predictive validation status: not demonstrated --
        evaluated under a pre-registered protocol, required advantage
        not shown"]

The "independence / dispersion not measured" explanation no longer
appears, exactly as designed -- the gate's remaining `NOT_MEASURABLE`
reason today is purely `predictive_validation_status`, not a stub.

Separate, pre-existing, unrelated finding surfaced while running the
full test suite: `tests/verify_evidence_quality_gate.py`'s existing
`EXPECTED_LOCAL_CONSISTENCY` assertion (fixed in RE-030.2) now fails --
`0.9518456229064439` expected, `0.9524468147359584` produced, a
5th-decimal drift. RE-035.1 does not touch consistency computation at
all, and Armando confirmed he did not modify the Shiller source file.
Root cause not yet investigated -- candidate explanation is an upstream
Shiller data revision (historical CPI revisions shift real returns for
all episodes, not just recent ones), not confirmed. This is logged as
an open item for a future iteration, deliberately not fixed here: RE-
DOC-002 prohibits silently rewriting a canonical value without
understanding why it changed.

What this does not authorize:

-   No gate output state added beyond `NOT_MEASURABLE`/`CONSERVATIVE`.
-   No threshold defined for `overlapping_match_pairs` -- it is exposed,
    not yet used to fail or pass anything, consistent with
    coverage/consistency/diversity today also having no threshold, only
    a presence check.
-   No wiring into `run.py`, `DecisionEngine`, `AssessmentEngine` or
    `ValidationEngine`.
-   No capital posture mapping change -- RE-034.1's provisional mapping
    stands unchanged.
-   No claim that this changes today's system-level posture output.

Boundary:

-   Two files changed: `engine/evidence_quality_gate.py`,
    `tests/verify_evidence_quality_gate.py`.
-   No Frozen Core component modified.
-   No `SimilarityEngine`, `EvidenceEngine` or `ObservableUniverse`
    change.
-   No gate state changed.
-   No operative wiring changed.
-   No fix attempted for the unrelated `EXPECTED_LOCAL_CONSISTENCY`
    drift -- logged as an open item, not resolved in this iteration.

------------------------------------------------------------------------

## RE-036.1 — Regime Comparability Gate: first measurable dimensions

RE-036.1 adds the first isolated implementation of the Regime
Comparability Gate boundary defined in RE-031.1.

Motivating finding, before any code: RE-031.1 left open which regime
dimensions are observable with current data. `models/context.py`
already carries `cape`, `inflation` and `interest_rate` per episode --
computed and populated, but `SimilarityEngine`'s score only consumes
`cape`, `pre_crash_return_3y` and `pre_crash_volatility_1y`.
`inflation` and `interest_rate` sit unused. This answers RE-031.1's
open question for three of its eight candidate dimensions without any
new data ingestion: valuation, inflation and interest-rate regime are
observable today.

Design, agreed with Armando before implementation:

-   Scope: local, against the current match set only (`evidence.
    matches`), not the full historical universe. This is RE-031.1's own
    framing of the question -- is the evidence actually informing
    today's decision structurally representative of today's regime --
    not a question about the dataset as a whole.
-   Method: strict `[min, max]` coverage. For each active dimension,
    does today's snapshot value fall within the range spanned by that
    dimension's values across the current matches? Binary, not graded --
    no percentile, no margin, no distance metric. Explicit reasoning:
    a single extreme match could widen the range and make a regime look
    "covered" when it barely is (small-N sensitivity, `n≈10`). Decision:
    do not anticipate this with un-observed-yet complexity (percentiles,
    trimmed ranges) -- start with the strict, fully transparent,
    zero-magic-number version; if an outlier problem is actually
    observed later, document it as a finding and address it then, not
    now.
-   Fail-closed, per RE-031.1: `None` (not `False`) when today's value
    or the match set's values for a dimension are missing -- absence of
    measurement is never treated as coverage, and is never treated as
    non-coverage either. It is its own explicit state.
-   Does not use `SimilarityEngine`'s selection, its scores, or Evidence
    Quality as a comparability proxy -- explicit prohibitions in
    RE-031.1. Coverage is measured independently of which episodes
    were selected as "similar"; a match can be close by drawdown/
    duration/speed and still sit in a completely different valuation
    or rate regime than today.

New file: `engine/regime_comparability_gate.py`.

-   `LocalRegimeComparabilityInputs` -- `Optional[bool]` per dimension
    (`cape_covered`, `inflation_covered`, `interest_rate_covered`), not
    a score. `None` = not measurable, `True`/`False` = measured result.
-   `_dimension_covered(today_value, match_values)` -- the strict
    `[min, max]` check, `None` if either side is unavailable.
-   `RegimeComparabilityGate.evaluate()` -- returns one of three states:
    `NOT_MEASURABLE` (zero dimensions measurable), `NOT_COMPARABLE` (at
    least one measured dimension falls outside its matches' range),
    `COMPARABLE` (all measured dimensions fall inside). A fresh,
    minimal vocabulary specific to this gate -- not reused from
    `EvidenceQualityGate`'s `NOT_MEASURABLE`/`CONSERVATIVE` pair, because
    the underlying question is different: Evidence Quality asks whether
    the sample is internally sound; Regime Comparability asks whether
    the sample even spans today's conditions. `NOT_COMPARABLE` has no
    equivalent on the Evidence Quality side.
-   `build_local_regime_comparability_inputs(snapshot, evidence)` --
    `snapshot` is the sole source of truth for today's regime;
    `evidence.matches` is the sole source of truth for the historical
    sample actually in use. Same non-drifting-inputs principle as
    `build_local_evidence_quality_inputs(evidence)`.

New test file: `tests/verify_regime_comparability_gate.py`. Exercises
`_dimension_covered()` directly (inside range, below, above, on
boundary, missing today value, empty match values, all-`None` match
values) and all three gate states with synthetic inputs. Also runs the
real pipeline and asserts the builder returns well-typed output -- this
iteration makes no canonical claim about what today's real snapshot
produces, only that the gate runs correctly end to end.

`tests/verify_core.py` updated to recognize both
`engine/evidence_quality_gate.py` (missing from that list since
RE-030.1) and `engine/regime_comparability_gate.py`.

Structural verification: synthetic checks for `_dimension_covered()`
and all three gate states pass in this sandbox. A synthetic end-to-end
check (mock snapshot/matches, values placed intentionally outside
range) confirms the builder and gate compose correctly. The real
pipeline run is pending pinned-runtime confirmation.

What this does not authorize:

-   No wiring into `run.py`, `DecisionEngine`, `AssessmentEngine`,
    `EvidenceQualityGate` or `gate_combination.py`.
-   No entry added to RE-034.1's posture-ceiling mapping table for
    `NOT_COMPARABLE` or `COMPARABLE` -- deciding how this gate's states
    cap posture is a separate governance decision, not a default
    consequence of the code existing.
-   No percentile, margin or outlier-robustness logic -- explicitly
    deferred until an actual problem is observed, per Armando's
    decision above.
-   No claim about volatility, liquidity/credit, policy or
    market-structure regime -- these remain unmeasurable, no data
    source exists for them yet.
-   No `SimilarityEngine`, `EvidenceEngine` or `ObservableUniverse`
    change.

Boundary:

-   Two new files: `engine/regime_comparability_gate.py`,
    `tests/verify_regime_comparability_gate.py`.
-   `tests/verify_core.py` updated to recognize both new/missing
    engine files.
-   No Frozen Core component modified.
-   No gate state changed.
-   No operative wiring changed.
-   No capital posture mapping changed.
-   Canonical real-pipeline values not published -- pending
    pinned-runtime confirmation.

## RE-036.2 — corrects a false claim in RE-036.1's own comment

Documentation-only, found by Armando in the same cold critical review
that produced RE-032.9 and RE-041.8, and deliberately deferred at the
time (lowest severity of the three, no live-code consequence) until
there was time to close it.

`REGIME_DIMENSIONS`'s comment stated that cape/inflation/interest_rate
were chosen because none of the three are "consumidas por
SimilarityEngine" -- false for cape specifically: the same comment,
two lines later, names cape as one of the three inputs to
`SimilarityEngine`'s own score (`cape`/`pre_crash_return_3y`/
`pre_crash_volatility_1y`). The comment contradicted itself.

Checked whether this is only a wording problem or a real design gap:
it is only wording. `RegimeComparabilityGate`'s own class docstring
already states the actual governing rule -- "No usa SimilarityEngine
ni evidence quality como proxy de comparabilidad" -- and the code
respects it: `SimilarityEngine` uses cape as one weighted dimension
inside a distance metric to *rank and select* matching episodes;
`RegimeComparabilityGate` independently checks whether *today's* raw
cape value falls inside the *selected* matches' `[min, max]` range.
Same underlying number, two unrelated questions -- cape appearing in
both places is not a violation of the separation RE-031.1 requires,
only the original comment's stated justification for choosing it was
wrong.

Fixed by rewriting the comment: states plainly that cape *is*
consumed by `SimilarityEngine` (inflation/interest_rate are not), and
explains why that overlap is fine rather than asserting the opposite.

What this does not authorize:

-   No change to `REGIME_DIMENSIONS`'s contents, to
    `_dimension_covered()`'s logic, or to any gate state.
-   No change to `SimilarityEngine`.
-   No re-examination of the other two findings from the same review
    (RE-032.9, RE-041.8 -- both already closed separately).

Boundary:

-   One file changed: `engine/regime_comparability_gate.py` (comment
    only).
-   No test changes -- nothing behavioral changed.
-   No Frozen Core component touched.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones.

------------------------------------------------------------------------

## RE-034.5 — Regime Comparability posture-ceiling mapping

RE-034.5 extends RE-034.1's provisional gate-ceiling mapping table with
the three real states RE-036.1 introduced for the Regime Comparability
Gate. It is documentation-only. No code changed.

RE-034.1 only anticipated a binary "not measurable" state for Regime
Comparability, because no code existed yet at the time. RE-036.1 gives
the gate three real states: `NOT_MEASURABLE`, `NOT_COMPARABLE`,
`COMPARABLE`. This iteration closes that gap. Per RE-DOC-002, RE-034.1's
original table is not rewritten -- this adds to it, forward.

Design, agreed with Armando before recording:

-   Regime Comparability `not comparable` -> `Conserve`. At least as
    restrictive as `not measurable`. This is not absence of
    information -- it is confirmed evidence that today's regime sits
    outside the historical sample actually informing the decision.
    Extrapolation risk, not uncertainty.
-   Regime Comparability `comparable` -> `Deploy Aggressively`, the top
    of the ordered scale. Reasoning: RE-031.1 requires this gate to
    never make posture more aggressive by itself, only cap it. Since
    combination takes the minimum ceiling across all gates, mapping the
    passing state to the top is the only way to encode "this gate
    imposes no restriction of its own" -- it can never become the
    binding constraint when satisfied. When Regime Comparability
    passes, the real ceiling is decided entirely by Evidence Quality
    and Personal Capacity, exactly as RE-031.1 requires ("a comparable
    regime does not make weak evidence strong").

Updated mapping table (supersedes RE-034.1's for Regime Comparability
only; Evidence Quality and Personal Capacity entries unchanged):

-   Evidence Quality `not measurable` -> `Prepare`;
-   Evidence Quality `conservative` -> `Conserve`;
-   Regime Comparability `not measurable` -> `Conserve`;
-   Regime Comparability `not comparable` -> `Conserve`;
-   Regime Comparability `comparable` -> `Deploy Aggressively`;
-   Personal Capacity unavailable / unclassified -> `Conserve`;
-   Any `Blocked` flag -> `Blocked`.

RE-034.1 open question closed: "Should Regime Comparability have its
own non-deployment exception in future, or is `not measurable ->
Conserve` permanent?" Answer: `not measurable` stays at `Conserve`
permanently as the fail-closed default -- that part of the question is
resolved by definition, not by new logic. The real question was what
happens once measurement exists at all, and RE-036.1 now provides that:
`comparable` removes the cap, `not comparable` confirms it.

Remaining RE-034.1 open questions, unaffected by this iteration:

-   Can `Prepare` ever be authorized solely by Regime Comparability
    while Evidence Quality remains `not measurable`? Still open --
    this iteration does not touch Evidence Quality's own mapping.
-   Does Personal Capacity belong in gate combination, or inside Human
    Approval? Still open, RE-032.1 remains unclassified.
-   How should explanations be composed when several gates cap posture
    at the same level? Still open.

What this does not authorize:

-   No code implementing this mapping -- it exists only as a documented
    decision. No function converts
    `RegimeComparabilityGateResult.state` into a `posture_ceiling`
    string yet.
-   No wiring into `gate_combination.py`, `DecisionEngine` or `run.py`.
-   No change to Evidence Quality's or Personal Capacity's own mapping
    entries.

Boundary:

-   No code changed.
-   No posture engine implemented.
-   No operative wiring authorized.
-   Documentation-only update to RE-034.1's provisional table, per
    RE-DOC-002's forward-correction discipline.

------------------------------------------------------------------------

## RE-037.1 — Isolated posture mapper (Evidence Quality + Regime Comparability)

RE-037.1 implements, for the first time in code, the mapping tables
documented in RE-034.1 and RE-034.5 -- turning "which posture ceiling
does this gate state imply" from a documentation-level worked example
into a real, callable function, still fully isolated from any
operative flow.

New file: `engine/posture_mapper.py`.

-   `EVIDENCE_QUALITY_POSTURE_CEILING` / `REGIME_COMPARABILITY_POSTURE_
    CEILING` -- dict literals, one entry per documented mapping row.
    Every entry traces to a specific status-doc section (RE-034.1 for
    Evidence Quality, RE-034.5 for Regime Comparability); no mapping is
    invented here.
-   `evidence_quality_to_gate_input()` / `regime_comparability_to_gate_
    input()` -- translate a gate's already-computed `Result` into a
    `GateCombinationInput`. Neither re-evaluates gate logic; both raise
    `ValueError` on an unrecognized state rather than silently
    defaulting to a ceiling -- an undocumented state must fail loudly,
    not resolve to a guess.
-   `evaluate_capital_posture(evidence_quality_result,
    regime_comparability_result)` -- composes both translations and
    calls `combine_gate_outputs()` (`engine/gate_combination.py`,
    RE-034.3) exactly as published. No combination logic is
    reimplemented.

Explicit, load-bearing caveat: Personal Capacity does not participate.
RE-032.1 has not classified it (parallel gate / human-approval
prerequisite / mixed control) and no code implements it. Per RE-034.1's
own worked example, an unavailable/unclassified Personal Capacity caps
posture at `Conserve` -- omitting it here means `evaluate_capital_
posture()`'s output is provably at least as permissive as a complete
combination would be. This is stated directly in the function's
docstring, not left implicit.

New test file: `tests/verify_posture_mapper.py`.

-   Synthetic checks: each documented mapping row individually: `blocked
    =False` always (neither gate has a veto mechanism yet); unrecognized
    states raise `ValueError`; several combined scenarios confirm the
    `min()` semantics -- notably that Regime Comparability `comparable`
    (mapped to the top of the scale) never overrides a more restrictive
    Evidence Quality state, and that `not comparable` caps posture even
    when Evidence Quality alone would allow more.
-   Real-pipeline audit dry-run: builds both gates' real results against
    today's snapshot and prints the full chain -- individual states,
    explanations, and the combined ceiling. Explicitly uses
    `PREDICTIVE_VALIDATION_NOT_DEMONSTRATED` for
    `GlobalModelValidationState`, reflecting RE-PRED.16's confirmed
    finding -- a deliberate choice stated in the script, not an
    automatic default. Read-only: prints a report, does not persist or
    act on anything.

`tests/verify_core.py` updated to recognize `engine/posture_mapper.py`
and (previously missing) `engine/gate_combination.py`.

Structural verification: synthetic checks for every mapping row,
unrecognized-state errors, and four combined scenarios pass in this
sandbox. The real-pipeline dry-run could not complete in this sandbox
this iteration -- the same intermittent iCloud file-lock issue already
seen in RE-035.1/RE-036.1 (`OSError: Resource deadlock avoided`), this
time failing on a plain module import before any data access. Unrelated
to this change. Pending pinned-runtime confirmation.

What this does not authorize:

-   No wiring into `run.py`, `DecisionEngine`, `AssessmentEngine` or
    `ValidationEngine`.
-   No claim that this is the Capital Posture Engine -- that remains a
    larger, future, operative component; this is a smaller, isolated
    composition layer for audit purposes only.
-   No Personal Capacity placeholder invented to fill the gap --
    explicitly absent, explicitly stated.
-   No change to `gate_combination.py`, `evidence_quality_gate.py` or
    `regime_comparability_gate.py`.
-   No capital action of any kind -- this layer prints or returns a
    ceiling, it does not act on it.

Boundary:

-   Two new files: `engine/posture_mapper.py`,
    `tests/verify_posture_mapper.py`.
-   `tests/verify_core.py` updated to recognize both new/missing
    engine files.
-   No Frozen Core component modified.
-   No existing gate or combination module modified.
-   No gate state changed.
-   No operative wiring changed.
-   Canonical real-pipeline audit output not published -- pending
    pinned-runtime confirmation.

------------------------------------------------------------------------

## RE-038.1 — Connect inflation/interest_rate; fix inflation level vs. rate

RE-038.1 closes two data-wiring gaps surfaced by RE-037.1's real audit
dry-run, and corrects a design error made in RE-036.1.

Correction to RE-036.1 (RE-DOC-002, forward, not silently rewritten):
that iteration stated `inflation` and `interest_rate` were "already
populated in `Context` per episode" -- this was false. Both fields were
hardcoded `None` in `engine/drawdown_engine.py::filter_episodes()` for
every historical episode, and `interest_rate` was also hardcoded `None`
in `engine/snapshot_engine.py::_build_snapshot()` for today's snapshot
(`inflation` there was already wired to `row["CPI"]`). This is exactly
why RE-037.1's real dry-run showed both dimensions as `not measurable`
-- not a data-availability question, a stub, discovered only once the
posture mapper made the full chain visible end to end.

Fix, part one -- wiring:

-   `engine/drawdown_engine.py::filter_episodes()`:
    `inflation`/`interest_rate` now read from the dataframe instead of
    being hardcoded.
-   `engine/snapshot_engine.py::_build_snapshot()`: `interest_rate` now
    reads from the dataframe (`inflation` was already correct).
-   `interest_rate` uses the `Rate GS10` column (US 10-Year Treasury
    Constant Maturity Rate) -- identified from
    `SnapshotEngine.latest()`'s own leftover debug print (`POSIBLES
    COLUMNAS MACRO`), now removed since it served its purpose.
-   Both fields share CAPE's existing characteristic of not filtering
    `NaN` at the source (`loaders/shiller_loader.py` only coerces
    `Date`/`P`) -- not a new risk introduced here, an existing,
    project-wide pattern, out of scope to fix in this iteration.

Fix, part two -- a real design error, caught before it mattered:
wiring `inflation` to raw `CPI` (the fix originally planned) would have
been wrong. `CPI` is an index level, near-monotonically increasing over
a century of history. Comparing today's level against any historical
episode's level would make Regime Comparability's `[min, max]` coverage
check fail almost tautologically -- not because today's inflation
regime is genuinely unprecedented, but because the index is chronologically
later, which it always will be. This was caught by inspecting the real
dry-run's numbers (a raw CPI level around 336) before publishing it as
a finding, not by design review alone.

-   New function `engine/drawdown_engine.py::calculate_inflation_rate()`
    -- adds `InflationRate1Y = CPI.pct_change(12)` to the dataframe,
    same `.rolling()`/`.pct_change()` pattern already used by
    `calculate_volatility()`. Called from `run_drawdown_engine()`
    immediately after `calculate_volatility()`.
-   Both `Context.inflation` sites (episodes and snapshot) now read
    `InflationRate1Y`, not `CPI`.

Structural verification, real pipeline, this sandbox -- NOT canonical:

    Before fix:  inflation_covered=None, interest_rate_covered=None
    After fix:   cape_covered=False, inflation_covered=True,
                 interest_rate_covered=True
    Regime Comparability state: not comparable
    Regime Comparability explanations: ["cape: today's value outside
        the matched episodes' range"]

Only CAPE remains out of range. This is a materially cleaner result
than before the fix -- the earlier `not comparable` verdict from
RE-037.1's dry-run was contaminated by two dimensions being
unmeasurable, not genuinely uncovered; today's result isolates the
actual signal.

A `FutureWarning` from pandas appeared during this sandbox run
(`Downcasting object dtype arrays on .fillna/.ffill/.bfill is
deprecated`), triggered inside `pct_change()` handling leading `NaN`
values in `CPI`. Not an error, not addressed in this iteration --
flagged so it is not mistaken for something new if it appears under
the pinned runtime too.

What this does not authorize:

-   No change to `SimilarityEngine`, `SIMILARITY_WEIGHTS`, or any
    Frozen Core component -- neither `inflation` nor `interest_rate`
    is consumed there.
-   No NaN-filtering fix for CAPE or any other Context field -- flagged
    as a known, pre-existing, project-wide characteristic, not resolved
    here.
-   No change to RE-036.1's `[min, max]` coverage method itself.
-   No claim about the `EXPECTED_LOCAL_CONSISTENCY` drift (RE-030.2) --
    unrelated, still open, deliberately left alone per the earlier
    decision not to touch data provenance questions without a
    confirmed root cause.

Boundary:

-   Two files changed: `engine/drawdown_engine.py`,
    `engine/snapshot_engine.py`.
-   No new files.
-   No Frozen Core component modified.
-   No gate, gate-combination or posture-mapper module modified.
-   No gate state-mapping table changed.
-   No operative wiring changed.
-   Confirmed under Armando's pinned runtime, exact match to sandbox:
    `cape_covered=False, inflation_covered=True,
    interest_rate_covered=True`, state `not comparable`, combined
    posture ceiling `Conserve`. As with all real-pipeline dry-run
    output in this document, this is a read against today's snapshot,
    not a frozen historical metric -- it will change as the date
    changes, and is never treated as a canonical claim in the
    RE-DOC-002 sense.

------------------------------------------------------------------------

## RE-039.1 — Standalone posture audit CLI

RE-039.1 extracts the real-pipeline audit dry-run that already lived
inside `tests/verify_posture_mapper.py` (its final section, added in
RE-037.1) into a dedicated, standalone entry-point script,
`audit_posture.py`, at repository root.

No logic changes. Same imports, same gate construction, same
`evaluate_capital_posture()` call, same disclaimers reproduced
verbatim (NOT a decision, not wired into `run.py` or `DecisionEngine`,
Personal Capacity excluded, result provably no more restrictive than
the real posture). The only difference from the version embedded in
the test file is the absence of assertions and a dedicated
`if __name__ == "__main__"` entry point, so it can be run on its own
(`python3 audit_posture.py`) without running the full verification
suite.

Placement follows the existing precedent set by `run.py`: a root-level
script that is not itself part of "Core" and is therefore not listed
in `tests/verify_core.py`'s checks, consistent with `run.py` also not
being listed there.

What this does not authorize:

-   No new gate, no new dimension, no change to any mapping table.
-   No wiring into `run.py` or `DecisionEngine`.
-   No change to `tests/verify_posture_mapper.py` -- the dry-run logic
    there is left in place, not removed, so the test suite's coverage
    of the real pipeline is unaffected.

Boundary:

-   One new file: `audit_posture.py`.
-   No files modified.
-   No Frozen Core component touched.
-   No gate, gate-combination or posture-mapper module modified.

------------------------------------------------------------------------

## RE-032.2 — Personal Capacity classified as a mixed control

RE-032.2 resolves RE-032.1's primary classification question:

    Is Personal Capacity a parallel gate,
    a human-approval requirement,
    or a mixed control?

Answer: mixed control. This is Armando's explicit decision, not an
inference drawn from the surrounding design -- recorded here as a
governance decision, the same way every prior consequential choice in
this document has been (RE-036.1's dimension proposal, RE-034.5's
posture-ceiling table, RE-037.1's implementation approach all required
the same explicit sign-off before being written).

Reasoning offered at decision time, for the record: RE-032.1 already
mandated that Personal Capacity's two input channels -- verifiable
facts and attested judgement -- must not be averaged into a single
score. That requirement is, structurally, already a mixed-control
design; classifying it as a pure gate or pure Human-Approval
requirement would have meant walking back a constraint RE-032.1 had
already set. A pure gate would force self-reported, crisis-sensitive
inputs like drawdown tolerance through the same automatic min()
combination as objective evidence -- exactly the "opaque confidence
score" RE-032.1 prohibits, and exactly the input most unreliable when
it matters most (RE-032.1's own drawdown-tolerance-risk paragraph). A
pure Human-Approval requirement would discard computability for the
half of Personal Capacity that is genuinely objective and verifiable
(liquidity, debt service, concentration) for no structural reason.

Resolved split:

-   Verifiable-facts channel (available liquidity, near-term cash
    needs, fixed obligations, debt service, income concentration,
    portfolio concentration, required emergency reserve, known time
    horizon constraints): becomes a future computable gate. When
    implemented, it participates in gate combination via `min()`,
    exactly like Evidence Quality and Regime Comparability -- ceiling
    only, cannot make posture more aggressive, fails closed on missing
    data.
-   Attested-judgement channel (perceived income stability,
    willingness to tolerate drawdown, ability to avoid forced selling,
    psychological capacity to hold through stress, household/life
    constraints): becomes a Human Approval prerequisite. It never
    enters `gate_combination.py`'s math, never produces an automatic
    posture ceiling, and is never computed by an engine -- consistent
    with the Constitution's principle that engines produce evidence,
    never portfolio decisions.

This directly answers one of RE-032.1's own open questions: "Does
Personal Capacity participate in gate-combination logic, or does it
sit inside Human Approval before any capital action is allowed?" --
both, split by channel, not either/or.

What this does not authorize:

-   No code. This is a classification decision, not an implementation.
-   No new gate, no new file, no schema for which specific facts or
    attestations are collected.
-   No Human Approval workflow defined -- its existence is now
    required by this classification, but its mechanics (who approves,
    how, how often, expiry, cooling-off periods after crisis-time
    revisions) remain fully open, per RE-032.1's own open-questions
    list.
-   No change to `posture_mapper.py`, `gate_combination.py`, or any
    existing gate's mapping table.
-   Does not resolve which specific facts are verifiable from existing
    records versus requiring manual entry -- still open.

Boundary:

-   No files changed except this document.
-   No code, no thresholds, no taxonomy.
-   Personal Capacity remains entirely outside the operative flow and
    outside the existing posture-mapper audit tooling
    (`audit_posture.py`, `tests/verify_posture_mapper.py`) -- both
    continue to state its exclusion explicitly, unchanged by this
    classification.

------------------------------------------------------------------------

## RE-032.3 — Personal Capacity: verifiable-facts categories

RE-032.3 enumerates the nine verifiable-facts categories that will
make up the computable half of Personal Capacity's mixed control
(RE-032.2). It answers, for each category, RE-032.1's own open
question of whether it can be verified from existing records or
requires manual entry. It does not define numeric thresholds, does
not implement a gate, and does not decide how the categories combine
with each other -- that is RE-032.5's scope.

Eight of the nine categories restate RE-032.1's own "verifiable facts"
list; the ninth (fiscal/operational constraints) is a new addition,
made explicit here rather than left implicit inside "known time
horizon constraints," because it has a distinct failure mode: paper
liquidity that is not real liquidity because of tax cost or a
structural lock-up.

1.  **Available liquidity** -- unencumbered liquid assets (cash and
    equivalents), excluding capital already allocated to the SOP's own
    thesis. Determines the real margin before a forced sale is needed
    in a drawdown. Source: manual entry -- outside the Research
    Engine's scope, lives in Armando's own accounting / SOP ledger.

2.  **Near-term cash needs** -- committed spending over roughly the
    next 12 months that cannot be covered without liquidating a
    position. A gate blind to this could authorize deployment that
    later forces a sale at a bad time. Source: manual entry.

3.  **Fixed obligations** -- non-discretionary recurring payments
    (mortgage, insurance, etc.). Reduces real maneuvering room in a
    drawdown regardless of declared tolerance. Source: manual entry.

4.  **Debt service** -- share of income or net worth committed to debt
    (principal plus interest). Leveraged debt reduces real tolerance
    independent of what is declared. Source: manual entry (a simple
    calculation if balance/rate are recorded).

5.  **Income concentration** -- dependence on a single income source.
    If income and market share the same cycle, real risk capacity is
    lower than it appears. Source: manual entry / semi-objective.

6.  **Portfolio concentration** -- degree to which investable net
    worth is concentrated in few assets/asset classes. Affects how far
    total net worth can fall in an adverse scenario, independent of
    the market signal itself. Source: computable if a position ledger
    exists (outside the Research Engine today).

7.  **Required emergency reserve** -- minimum liquidity that must
    always be protected, regardless of any market gate. Source: manual
    entry, value set a priori, not continuously recalibrated. Flagged
    as a likely candidate for a different treatment than the other
    eight categories: a binary breach (below reserve -> hard block)
    rather than a graded contributor to a combined score. Not decided
    here -- explicitly deferred to RE-032.5.

8.  **Known time horizon constraints** -- dated events requiring
    liquidity at a known point (home purchase, planned retirement,
    tuition). A gate blind to this could authorize deployment that
    collides with an already-planned need. Source: manual entry.

9.  **Fiscal / operational constraints** -- tax cost of liquidating
    (capital gains, tax-year windows) and structural access
    restrictions (lock-ups, illiquid vehicles). Source: manual entry /
    semi-computable if vehicle and liquidity date are recorded.

What this does not authorize:

-   No numeric thresholds for any category.
-   No code, no new gate, no schema or storage for these facts.
-   No decision on how the nine categories combine with each other
    (weighted, all-must-pass, worst-case-dominates, etc.) -- open for
    RE-032.5.
-   No resolution of the Required Emergency Reserve's binary-vs-graded
    question -- explicitly flagged, not decided.
-   No change to the attested-judgement channel or Human Approval --
    that remains RE-032.4's scope, deliberately kept separate per the
    ordering correction agreed before this iteration (define the
    computable channel first; the attested channel and its Human
    Approval boundary together, in one iteration, since for that
    channel the boundary IS the content).

Boundary:

-   No files changed except this document.
-   No code, no thresholds, no combination logic.
-   Personal Capacity remains entirely outside the operative flow.

------------------------------------------------------------------------

## RE-032.4 — Personal Capacity: attested-judgement channel + Human Approval procedural boundary

RE-032.4 defines, in a single iteration, both the attested-judgement
channel's categories and the Human Approval mechanics that govern it.
Unlike RE-032.3 (facts enumerated, thresholds deferred), this channel
has no separate future implementation step where numbers get decided
later -- for a channel that cannot be honestly computed, the procedural
boundary *is* the content. This ordering was corrected earlier in this
session: it was originally planned as a fourth, later, and separate
"Human Approval boundary" step; collapsing it into this iteration
avoids defining attested-judgement content twice.

Categories (restated from RE-032.1, unchanged): perceived income
stability; willingness to tolerate drawdown; ability to avoid forced
selling; psychological capacity to hold through stress; household or
life constraints not captured in financial data.

Human Approval mechanics:

1.  **Nature.** Human Approval is not a scored gate and does not
    participate in `combine_gate_outputs()`'s `min()` posture
    combination. It is a binary procedural prerequisite for capital
    action. This makes explicit, not new, a principle already stated
    at the top of this document: engines produce evidence, never
    portfolio decisions.

2.  **Who approves.** Armando, as sole principal. No delegated or
    second approver is defined. A future accountability-partner role
    is out of scope here.

3.  **States.** `missing`, `valid`, `expired`, `under_cooling_off`.
    These describe the attestation's status. A tolerance-reducing
    revision is an immediate event, not a persistent state -- it never
    produces `under_cooling_off`.

4.  **Validity.** Exactly 90 calendar days from the registration
    timestamp -- a fixed rolling window, not a calendar quarter, to
    avoid calendar-edge ambiguity (e.g., attesting March 29 and
    expiring April 1).

5.  **Rule of block.** If the state is `missing`, `expired` or
    `under_cooling_off`, no capital action may proceed, regardless of
    the posture ceiling computed by Evidence Quality, Regime
    Comparability or the future Personal Capacity facts gate.
    Analysis, monitoring and preparation remain fully functional --
    only execution is blocked. Fail-closed, same principle as Evidence
    Quality Gate's defaults.

6.  **Tolerance direction.** Defined against RE-033.1's existing
    ordered posture scale (`Conserve < Prepare < Deploy Partially <
    Deploy Aggressively`), not by subjective wording. A revision
    "increases" tolerance if it would authorize a strictly less
    restrictive posture ceiling than the currently valid attestation;
    it "reduces" tolerance otherwise, including ties.

7.  **Cooling-off, universal by default.** Any tolerance-increasing
    revision enters a 14-day cooling-off period before taking effect,
    unconditionally -- not contingent on detecting a crisis. During
    cooling-off, the previously valid attestation remains in force.
    Tolerance-reducing revisions apply immediately, always, regardless
    of crisis state.

8.  **Crisis as an aggravating extension, not a trigger.** Two crisis
    signals extend the cooling-off from 14 to 30 days when active:
    `market_crisis` (objective -- live snapshot `Drawdown <=
    MIN_DRAWDOWN`, the same constant `drawdown_engine.py` already uses
    to detect historical episodes; not self-reported, cannot be
    avoided or misjudged) and `personal_crisis` (a self-declared vital
    event -- job loss, divorce, illness, etc.).

    Explicit, load-bearing design correction made this session: an
    earlier draft made `personal_crisis` a *trigger* for cooling-off,
    conditional on it being declared. That was rejected. The failure
    mode RE-032.1 already named -- a tolerance revision is least
    reliable exactly when it matters most -- applies just as much to
    the *decision to declare* a personal crisis as it does to the
    tolerance attestation itself: the same stress, denial or avoidance
    that erodes judgement under pressure can just as easily suppress
    the declaration that would have protected against it. Making
    protection depend on accurate self-detection at the worst possible
    moment would have quietly reintroduced the exact vulnerability
    this entire mechanism exists to close.

    The fix is structural, not a better detector: the 14-day
    cooling-off applies to every tolerance increase regardless of
    declared state, so an undeclared personal crisis is still covered
    by the baseline friction. `personal_crisis` (like `market_crisis`)
    only ever makes the control *stricter* when active -- it is never
    required for the baseline protection to work.

    Honest limitation, stated rather than hidden: `market_crisis` and
    `personal_crisis` are not equally reliable. `market_crisis` is
    objective and cannot be evaded. `personal_crisis` is self-reported
    and therefore exactly as unreliable, in the moment it matters
    most, as the thing it exists to help guard against. It is kept in
    the design because declaring it when it is true makes protection
    stronger, and there is no incentive to falsely declare one --
    but its absence must never be read as evidence that no personal
    crisis exists. This is recorded as an accepted, permanent
    limitation, not a problem this iteration claims to have solved.

Future possibility, noted but explicitly out of scope here: deltas in
the verifiable-facts channel (RE-032.3) -- e.g., a sharp drop in
liquidity or a spike in debt service over a short window -- could
someday serve as an indirect, passive proxy for an undeclared personal
crisis. Not designed in this iteration; would require tracking fact
history, which does not exist yet.

What this does not authorize:

-   No code, no storage schema, no attestation form or UI.
-   No change to `gate_combination.py`, `posture_mapper.py`, or any
    existing gate's mapping table.
-   Does not resolve Required Emergency Reserve's binary-vs-graded
    question (RE-032.3, still open, deferred to RE-032.5).
-   Does not build any facts-history/delta mechanism for the noted
    future personal-crisis proxy.
-   Does not solve `personal_crisis` under-reporting -- explicitly
    documented as accepted, not solved.

Boundary:

-   No files changed except this document.
-   No code, no thresholds implemented, no wiring.
-   Personal Capacity remains entirely outside the operative flow.
-   Closes Path A's classification/definition arc for both channels
    (RE-032.2 classification, RE-032.3 verifiable facts, RE-032.4
    attested judgement + Human Approval). First-code implementation
    (facts gate, RE-032.5) remains open, next.

------------------------------------------------------------------------

## RE-032.5 — Personal Capacity Facts Gate: first isolated code

RE-032.5 adds the first code for Personal Capacity's computable half
-- the nine verifiable-facts categories enumerated in RE-032.3. The
attested-judgement channel and Human Approval boundary (RE-032.4) are
entirely separate and remain undecided in code; nothing here computes
them or ever will, by design.

New file: `engine/personal_capacity_facts_gate.py`.

Structure, same pattern as `EvidenceQualityGate` (RE-030.1) and
`RegimeComparabilityGate` (RE-036.1):

-   `LocalPersonalCapacityFactsInputs` -- nine `Optional[bool]`
    fields, one per RE-032.3 category, uniform positive polarity
    throughout (`True` = adequate/acceptable/covered/manageable,
    `False` = confirmed breach, `None` = not measured). A missing fact
    is never treated as favorable.
-   `PersonalCapacityFactsGate.evaluate()` combines the nine into a
    `PersonalCapacityFactsGateResult`.

Combination logic, three states:

-   `constrained` if any of the nine is `False` -- one confirmed
    breach is sufficient; a real problem does not need the full
    picture to be visible before it counts.
-   `adequate` only if all nine are `True` -- full confirmation
    required, partial data never qualifies.
-   `not measurable` otherwise (some `None`, no confirmed breach) --
    the fail-closed default: absence of evidence is not evidence of
    adequacy, same principle as the other two gates.

Result carries `failed_fields`, `missing_fields` and `blocking_fields`
explicitly, not just a state string and free-text explanations --
more structurally auditable, consistent with this document's
explainability-over-sophistication principle.

Emergency Reserve resolved: RE-032.3 flagged Required Emergency
Reserve as a likely candidate for different treatment (binary breach
vs. graded contributor) without deciding it. RE-032.5 resolves it as
both, not either/or -- the same pattern already used for Personal
Capacity's own channel split. `emergency_reserve_adequate` counts
toward the graded `state` like the other eight fields, and
additionally sets an orthogonal `blocked` flag when `False`, reusing
`GateCombinationInput.blocked` (RE-034.3) rather than inventing a new
mechanism. `state` and `blocked` are independent: a blocked result
typically also carries `state=constrained`, never `state="Blocked"` --
that string belongs only to `gate_combination.py`'s `BLOCKED` constant,
consumed by a future translator (RE-040.x), not produced here.

Provisional, stated as such, not expanded: only
`emergency_reserve_adequate` is a hard-block field in this iteration
(`HARD_BLOCK_FIELDS = ["emergency_reserve_adequate"]`). Other failed
facts only degrade `state` to `constrained`. Whether additional facts
(e.g. confirmed forced-sale risk, extreme debt service) should become
hard blockers, and on what principle, is left open for a future
iteration. Not decided here by ad hoc expansion under time pressure --
each of those candidates is arguably already a threshold question
within an existing category (extreme debt service is a stricter
`debt_service_manageable` threshold, not a new category), and
widening `blocked` too easily would dilute its meaning as a genuine
circuit-breaker.

Honest limitation, stated rather than hidden: unlike the other two
gates, this one has no `build_local_*_inputs()` function and no
real-pipeline data source. None of the nine facts is tracked anywhere
in this repository -- all live in Armando's own accounting / SOP
ledger, outside the Research Engine's declared scope. Only synthetic
verification is possible until that changes; `tests/verify_
personal_capacity_facts_gate.py` has no real-pipeline dry-run section,
unlike `tests/verify_regime_comparability_gate.py` or `tests/verify_
posture_mapper.py`.

New test file: `tests/verify_personal_capacity_facts_gate.py` --
synthetic checks: all-unmeasured, all-adequate, single regular
failure, reserve failure (state + blocked together), reserve
unmeasured (not treated as breach), partial data with no failure,
failure dominating missing data, and multiple simultaneous failures
including reserve.

`tests/verify_core.py` updated to recognize
`engine/personal_capacity_facts_gate.py`.

What this does not authorize:

-   No wiring into `run.py`, `DecisionEngine`,
    `posture_mapper.py` or `gate_combination.py` -- integration is
    RE-040.x, explicitly future work, same staged pattern already used
    for the other two gates before their own posture-mapper
    integrations (RE-034.5/RE-037.1).
-   No numeric thresholds for any of the nine facts -- this gate only
    combines already-determined booleans; determining them (e.g. what
    counts as "adequate" liquidity) happens entirely outside this
    repository.
-   No expansion of hard-block fields beyond emergency reserve.
-   No attested-judgement channel or Human Approval code -- RE-032.4's
    content is not represented here and never will be computed.
-   No resolution of how this gate's states map to posture ceilings --
    that mapping table is RE-040.x's scope, mirroring RE-034.5's
    precedent for Regime Comparability.

Boundary:

-   Two new files: `engine/personal_capacity_facts_gate.py`,
    `tests/verify_personal_capacity_facts_gate.py`.
-   One file modified: `tests/verify_core.py`.
-   No Frozen Core component touched.
-   No existing gate, gate-combination or posture-mapper module
    modified.
-   Personal Capacity remains entirely outside the operative flow.

------------------------------------------------------------------------

## RE-040.1 — Personal Capacity Facts Gate wired into posture_mapper

RE-040.1 integrates RE-032.5's `PersonalCapacityFactsGate` into
`engine/posture_mapper.py`, following the same staged pattern already
used for `EvidenceQualityGate` (RE-030.1 -> RE-034.5/RE-037.1) and
`RegimeComparabilityGate` (RE-036.1 -> RE-034.5/RE-037.1): isolated
gate first, posture-ceiling mapping and combination wiring second.

New posture-ceiling table, `PERSONAL_CAPACITY_FACTS_POSTURE_CEILING`:

    not measurable -> Conserve
    constrained    -> Conserve
    adequate       -> Deploy Aggressively

`adequate -> Deploy Aggressively` does not mean "authorizes an
aggressive deployment" -- it means this gate imposes no restriction of
its own, exactly the same reading already established for Regime
Comparability's `comparable -> Deploy Aggressively` (RE-034.5). The
actual ceiling, if any, still comes from whichever gate is genuinely
restrictive; `min()` in `combine_gate_outputs()` enforces that. This is
stated explicitly in the code comment, not left to be inferred, after
this exact ambiguity was flagged during review before writing the code.

`not measurable -> Conserve`, stricter than Evidence Quality's
`not measurable -> Prepare` (RE-034.1): not knowing whether someone can
personally afford the risk is treated as more serious than not knowing
whether the model's predictions are validated.

New function `personal_capacity_facts_to_gate_input()`, same pattern
as the other two translators: raises `ValueError` on an unrecognized
state, copies `explanations` through unchanged. `blocked` propagates
directly from `PersonalCapacityFactsGateResult.blocked` (RE-032.5's
emergency-reserve veto, currently the only one) into
`GateCombinationInput.blocked` -- no reinterpretation. This is the
first time any gate actually exercises `combine_gate_outputs()`'s
`Blocked` short-circuit (RE-034.3), which until now had only been
tested synthetically.

`evaluate_capital_posture()` gains a third parameter,
`personal_capacity_facts_result`, optional, default `None`. Reviewed
and confirmed before writing: when omitted, no gate is added to the
combination -- not a placeholder, not a default-favorable value, no
ghost gate. Existing two-gate callers (`audit_posture.py`,
`tests/verify_posture_mapper.py`'s real-pipeline dry-run) are
unaffected by construction, not merely by convention.

Explicitly reviewed and confirmed before writing: when `blocked=True`
reaches `combine_gate_outputs()`, the cause must not go dark.
`personal_capacity_facts_to_gate_input()` copies the full
`explanations` list through (which already includes, e.g., `"hard
block: emergency_reserve_adequate"` from RE-032.5), so the formatted
combined result names the actual blocking field, not just the fact
that something is blocked.

Even with this third gate wired in, the combined result remains, by
construction, optimistic: the attested-judgement channel and Human
Approval procedural boundary (RE-032.4) have no code and are never
computed here or anywhere. This is stated in
`evaluate_capital_posture()`'s own docstring, not left implicit.

`audit_posture.py` and the real-pipeline section of `tests/verify_
posture_mapper.py` are deliberately left unchanged, at two gates only:
no real data source exists for any of the nine verifiable facts (per
RE-032.5's own stated limitation), so there is nothing honest to
supply as the third argument there. The dry-run's disclaimer text is
updated to name this precisely, rather than leave the older, now
partially-inaccurate "Personal Capacity excluded" wording in place.

New synthetic tests in `tests/verify_posture_mapper.py`: per-state
translation checks, blocked propagation into the translated
`GateCombinationInput`, three-gate combined scenarios (facts adequate
-- ceiling still set by the weakest gate; facts constrained -- becomes
the binding gate), and the reserve-breach case producing `Blocked`
with the specific cause visible in the combined explanations.

What this does not authorize:

-   No change to `engine/gate_combination.py` -- `combine_gate_outputs()`
    is consumed exactly as published (RE-034.3), same discipline as
    RE-037.1.
-   No change to `EvidenceQualityGate` or `RegimeComparabilityGate`'s
    own mapping tables.
-   No wiring into `run.py` or `DecisionEngine` -- the entire
    posture-mapper layer remains an isolated, read-only composition
    for audit/dry-run, not the future Capital Posture Engine.
-   No real data feeding Personal Capacity Facts anywhere -- still
    entirely synthetic.
-   No attested-judgement/Human Approval code -- RE-032.4's content
    remains undecided in code, permanently, by design.

Boundary:

-   One file modified: `engine/posture_mapper.py`.
-   One test file modified: `tests/verify_posture_mapper.py`.
-   No new files.
-   No Frozen Core component touched.
-   No existing gate's internal logic modified.
-   Personal Capacity remains entirely outside the operative flow.

------------------------------------------------------------------------

## RE-041.1 — Dry Powder Protocol specification

RE-041.1 fills in the two numbers RE-033.1 deliberately left open:
`Deploy Partially`'s bounded fraction and `Deploy Aggressively`'s
maximum amount. Documentation-only -- no code, no operative wiring, no
automatic execution. `Conserve`, `Prepare` and `Blocked` remain 0%
deployment, exactly as RE-033.1 already fixed; this iteration does not
touch them.

A priori, not calibrated: same discipline already applied throughout
Personal Capacity's definition. No number here was fit against the
19-episode historical sample -- the mechanism follows from risk-
management structure (multi-leg drawdowns are common; irreversible,
all-at-once commitment removes optionality for a worse leg later),
not from backtesting against this project's small sample.

Mechanism, four rules:

1.  **Tranche on remainder.** Each deployment event releases a fixed
    fraction of the Dry Powder remaining at that moment (`DP_t`), not
    of the initial episode balance. This alone produces an asymptotic
    decay curve that never reaches zero -- but, checked explicitly
    during design review, decay alone is not a substitute for an
    explicit ceiling: enough events can still deploy the large majority
    of Dry Powder without any single decision authorizing that total.
    Rule 3 exists specifically to close that gap.

2.  **Dual cadence.** A new tranche requires either a minimum number
    of days since the last one, or additional drawdown of a fixed
    number of percentage points (absolute, not relative) since the
    last tranche -- reusing the live snapshot's `Drawdown` field,
    the same one `market_crisis` already uses in RE-032.4, not a new
    concept. `Deploy Aggressively` gets both a larger tranche and a
    shorter cadence than `Deploy Partially` -- intensity escalates
    with posture on both dimensions, not just one.

3.  **Per-posture cumulative ceiling, backstop only.** Each posture
    carries a maximum cumulative fraction of the episode's initial Dry
    Powder that may ever be deployed while that posture (or a more
    permissive one) is active. This is explicitly a circuit-breaker for
    extreme, prolonged scenarios, not the everyday control -- day to
    day, posture, remaining balance and cadence already do the
    limiting. Setting the ceiling too tight would reintroduce the
    exact paralysis a single fixed global cap was rejected for during
    design review (a long multi-leg crash exhausting the cap on an
    early leg, then blocking further deployment even as the evidence
    stays favorable and valuations improve).

4.  **Ratchet; reset only by episode.** The effective ceiling is the
    highest one reached so far in the current episode -- posture
    dropping back to `Prepare` and rising again does not refill spent
    capacity. Explicitly closed during design review: without this
    rule, cycling between postures could be used to "recharge" tranche
    capacity, reopening exactly the kind of self-serving loophole this
    session has repeatedly closed elsewhere (RE-032.4's crisis-time
    revision asymmetry is the same principle applied here). The
    cumulative counter resets only when a new episode begins -- full
    recovery to a new peak, the same definition `drawdown_engine.py`
    already uses for episode boundaries, not a calendar period.

Beyond the `Deploy Aggressively` ceiling: blocked, unless a fresh
Human Approval attestation (RE-032.4) explicitly authorizes it. Reuses
the existing procedural mechanism rather than inventing a new one --
the last fraction of Dry Powder is never spent by formula alone.

Parameters (v1, subject to revision, not treated as permanent):

    Deploy Partially:
        tranche (% of remaining Dry Powder):     12%
        cumulative ceiling (% of episode's
            initial Dry Powder):                 40%
        cadence:  30 days OR 5.0 percentage points
                  of additional drawdown

    Deploy Aggressively:
        tranche (% of remaining Dry Powder):     22%
        cumulative ceiling (% of episode's
            initial Dry Powder):                 80%
        cadence:  14 days OR 5.0 percentage points
                  of additional drawdown

    Beyond 80%: blocked without a fresh Human Approval
    attestation (RE-032.4). v1 never authorizes 100%
    deployment by formula alone.

Sanity check performed before adopting these numbers (illustrative,
not a claim about real market behavior): under a fast, repeated
price-trigger scenario, `Deploy Aggressively`'s 80% ceiling is reached
around the 7th tranche; `Deploy Partially`'s 40% ceiling around the
4th. Both bind only under a genuinely severe, prolonged scenario, not
in ordinary operation -- consistent with the backstop framing in
Rule 3.

Design process note: two independently drafted proposals were compared
before adopting this specification. One used a single 21-day cadence
for both postures, which would have silently dropped the
intensity-escalates-with-posture principle already agreed earlier in
this session (`Deploy Aggressively` should unlock faster, not just
larger, tranches). Rejected for that specific, technical reason -- not
for tone, though that proposal's self-congratulatory framing
("impecable", "hermético") was also noted as a caution sign worth
naming: language that declares a design closed and perfect is often a
sign it has not been stress-tested enough. Its one genuinely good idea
-- treating the fraction beyond the ceiling as requiring an explicit
unlocking decision rather than staying silently frozen forever -- was
kept and tied to the existing Human Approval mechanism (RE-032.4)
rather than a new one.

Explicitly noted, not hidden: under today's real Evidence Quality
state (`not measurable`, per `tests/verify_posture_mapper.py`'s real
dry-run), combined posture cannot exceed `Prepare` regardless of
drawdown depth. This protocol cannot trigger today no matter how
severe a real drawdown becomes. It is specified now as forward
infrastructure, for if and when Evidence Quality is ever validated --
not because it changes anything immediately.

What this does not authorize:

-   No code. No `DryPowderProtocol` module, no wiring into
    `posture_mapper.py`, `gate_combination.py`, `run.py` or
    `DecisionEngine`.
-   No automatic execution of any deployment -- this remains, even
    once coded, subject to Human Approval per the existing policy
    (`Deploy Partially`/`Deploy Aggressively` require explicit
    human approval with timestamp before execution, already fixed
    earlier in this document).
-   No relaxation of Evidence Quality, Regime Comparability or
    Personal Capacity's existing gates or ceilings.
-   No claim that these specific numbers are final -- v1, explicitly
    revisable, not fit against history.
-   No change to Portfolio Reallocation Protocol, which remains a
    fully separate, still-undefined protocol per RE-029.1's original
    separation.

Boundary:

-   No files changed except this document.
-   No code, no thresholds implemented in any module, no operative
    wiring.
-   This protocol remains entirely outside the operative flow, same as
    every gate and the posture-mapper layer it would eventually
    consume.

------------------------------------------------------------------------

## RE-030.3 — EXPECTED_LOCAL_CONSISTENCY root cause found and corrected (closes B1)

RE-030.3 closes the `EXPECTED_LOCAL_CONSISTENCY` drift left open and
deliberately unresolved since earlier this session (logged as B1):
`tests/verify_evidence_quality_gate.py` expected `0.9518456229064439`,
Armando's pinned runtime measured `0.9524468147359584`. At the time,
root cause could not be confirmed from available evidence, and
re-downloading Shiller data to investigate was explicitly rejected --
it would have destroyed forensic value and required re-verifying
nearly every canonical value in the project (see the earlier decision
in this document). The drift was logged and deliberately left alone.

Root cause investigation (this iteration), by direct evidence, not
guesswork:

1.  Ruled out a floating-point tie-flip at the match-set boundary
    (hypothesis: a numpy/pandas version difference flips which episode
    lands in the top-10 cutoff). Measured the actual 10th-vs-11th-place
    similarity score gap in the real pipeline: 0.019 -- several orders
    of magnitude larger than any plausible cross-version floating-point
    noise (~1e-15). This mechanism cannot explain a drift of this size.
2.  Confirmed `SimilarityEngine.compare()`'s sort is stable, with
    ties broken by the fixed original episode order -- no `set` or
    dict-iteration nondeterminism anywhere in the ranking path.
3.  Confirmed via `git log --oneline -- data/raw/shiller.xlsx`: exactly
    one commit in the file's entire history (the initial project
    commit). The Shiller data file has never changed. This also
    corrects an earlier, mistaken note in this document claiming "no
    git history for the data file" -- that was this session's sandbox
    `git log` crashing on path-filtered queries (a known, recurring
    instability), not an actual absence of history. The file is
    tracked normally; it simply required Armando's own terminal to
    read reliably.
4.  Confirmed via `git diff` between the commit that added
    `SIMILARITY_WEIGHTS`/`SIMILARITY_SCALES` history and today: the
    only change to `core/constants.py` ever made (RE-024.1) is purely
    additive (`OUTCOME_HORIZONS_YEARS`) and does not touch either
    dictionary's values.
5.  Confirmed via `git diff` between the commit that introduced
    `build_local_evidence_quality_inputs()` (RE-030.2) and the commit
    that first measured the drift (RE-035.1): the `returns`/
    `pstdev(returns)` consistency-calculation block in
    `engine/evidence_quality_gate.py` is byte-identical across that
    range. The formula itself never changed.
6.  Found the actual cause: `RE-BUG.2` (calendar-month duration
    arithmetic fix) sits chronologically between RE-030.2 and
    RE-035.1. RE-BUG.3 already documents that this fix corrected
    `duration_months` and `recovery_months` calculations project-wide.
    `duration_months` feeds `SimilarityEngine`'s `duration_score`
    directly and `speed_score` indirectly (via `speed_down`) --
    changing it shifts every episode's similarity ranking, which can
    and did change which episodes land in the top-10 match set feeding
    `pstdev()`. RE-BUG.3 explicitly lists which verification suites it
    updated after the fix (`verify_research_engine.py`,
    `verify_assessment_engine.py`, `verify_validation_metrics.py`) --
    `tests/verify_evidence_quality_gate.py` is not on that list. It was
    missed, not wrong: `0.9518456229064439` was the correct pre-fix
    value at the moment RE-030.2 recorded it; RE-BUG.2 legitimately
    changed the ground truth two iterations later, and nothing ever
    went back to refresh this one constant.

This was not a transcription error, not sandbox noise, not a data
change, and not a package-pinning inconsistency. It is a fully
explained, already-approved consequence of a bug fix this project
already reviewed and accepted (RE-BUG.1/RE-BUG.2/RE-BUG.3) -- the only
error was a documentation-refresh gap.

Fix, forward-corrected (RE-DOC-002), not silently rewritten:
`tests/verify_evidence_quality_gate.py`'s `EXPECTED_LOCAL_CONSISTENCY`
updated to `0.9524468147359584`, with an inline comment recording the
root cause, confirmed under Armando's pinned runtime.
`EXPECTED_LOCAL_COVERAGE` and `EXPECTED_LOCAL_DIVERSITY` were checked
and remain correct -- coverage depends only on match count (unchanged
at 9 of 10) and diversity on the set of decades spanned by the match
set (unchanged at the same six decades), so neither happened to be
sensitive to which specific episodes shifted at the match-set boundary.

What this does not authorize:

-   No change to `engine/evidence_quality_gate.py`'s logic -- the
    consistency formula itself was confirmed correct and untouched.
-   No change to `SimilarityEngine`, `SIMILARITY_WEIGHTS`,
    `SIMILARITY_SCALES`, or any Frozen Core component.
-   No re-verification of other canonical values in this document --
    this investigation's scope was strictly `EXPECTED_LOCAL_CONSISTENCY`
    only; other constants were not audited by this iteration and are
    not implied to be at similar risk without their own investigation.
-   No retroactive rewrite of RE-030.2 or RE-BUG.3's own changelog
    entries -- the correction is recorded forward, here, per RE-DOC-002.

Boundary:

-   One file modified: `tests/verify_evidence_quality_gate.py`.
-   No new files.
-   No Frozen Core component touched.
-   No gate logic modified.
-   Structural verification only in this sandbox -- pending
    confirmation under Armando's pinned runtime before being treated as
    fully closed.

------------------------------------------------------------------------

## RE-DOC-005 — Honest Progress Snapshot policy

RE-DOC-005 establishes a standing, recurring section at the top of
this document (see "Honest Progress Snapshot" above), updated at the
end of every work session per Armando's explicit instruction.

Purpose: every other section of this document records what exists and
what has been verified -- a factual, backward-looking record. This
snapshot is different in kind: it is a judgment call about how close
each block actually is to being usable, not just correctly built. The
two questions are deliberately kept separate wherever they diverge --
most sharply for Personal Capacity and Human Approval, where the code
is real and tested but there is no real data or tooling behind it
anywhere. Collapsing "designed" and "operational" into one blended
number would flatter readiness that does not exist.

Discipline for future updates:

-   Each session's update replaces the table and the closing line, not
    the surrounding policy text.
-   Percentages are estimates, not measurements -- they should read as
    a considered judgment, not a computed metric. Round numbers or
    ranges are preferred over false precision.
-   Where "specification" and "operational" diverge meaningfully for a
    block, both are recorded as separate rows or separate figures --
    never merged into an average that would understate how far the
    block is from being real.
-   The closing one-line verdict should say plainly what changed and
    what still blocks the system from acting, even when that is
    uncomfortable to state -- consistent with this document's existing
    RE-DOC-002 discipline of not smoothing over history.

Boundary:

-   Documentation-only. No code.
-   This snapshot does not replace or override the Component Status
    tables, Design Decision log or Changelog -- it is a compact,
    judgment-based summary layered on top of them.

------------------------------------------------------------------------

## RE-042.1 — Personal Capacity Facts: real data captured for both patrimonios (AMS/AML)

RE-032.5 built the gate's logic against synthetic inputs only, with an
explicit, stated limitation: no `build_local_personal_capacity_facts_inputs()`
adapter exists anywhere, because no real data source existed either.
RE-042.1 closes half of that gap -- the data half, not the code half --
by reviewing Armando's two real portfolio-tracking files (his own,
"AMS", and his parents', "AML") and mapping RE-032.3's nine
verifiable-facts categories against real figures for both.

This was a discussion-first exercise, not a code exercise, and it
surfaced a real design question neither RE-032.3 nor RE-032.5
anticipated: `LocalPersonalCapacityFactsInputs` is a single-patrimonio
dataclass, and Armando manages two. That question is not resolved by
this iteration -- it is captured as open, deliberately, rather than
guessed at.

What came out of the discussion, confirmed by Armando line by line:

-   Liquidity model unified across both patrimonios into two layers:
    a colchón (safety floor, never touched, sized differently per
    patrimonio -- 30.000€ for AMS from ~4 years of its annual income
    gap, 125.000€ for AML from years of full annual expense, since AML
    runs a surplus and has no gap to speak of) and a pólvora seca
    range with its own suelo/techo (AMS: 70.000-120.000€; AML:
    125.000-175.000€, confirmed to reproduce Armando's original
    250-300k total-liquidity figure exactly).
-   Money-market funds folded into the liquidity bucket rather than
    tracked as a separate asset class, per Armando's correction --
    their function is dry powder, so their classification should say
    so.
-   Debt service fixed permanently at "manageable" for both
    patrimonios -- no debt exists or is planned for either.
-   "Fixed obligations manageable" collapsed into a derived read of
    annual expenses vs. recurring income, per Armando's own
    clarification that this is what he meant by "obligaciones fijas"
    -- not an independent input.
-   Income concentration resolved qualitatively rather than by asking
    for exact income figures: AMS has three sources, none dominant,
    partial market correlation via ETF dividends; AML's dominant
    source (75%) is public pension income, structurally the most
    stable income type available, with the total (80.000€) far
    exceeding expenses (30-35.000€).
-   AML's Planes de Pensiones (1.157.519,11€, 27,4% of net worth)
    confirmed permanently excluded from liquidity/dry powder -- not
    only legally illiquid outside retirement/long-term unemployment/
    severe illness, but tax-punitive by design: withdrawal is taxed as
    earned income, which combined with Armando's parents' pensions
    would push them near the 50% marginal bracket. They are earmarked
    as inheritance, not deployable capital, under any scenario.
-   An arithmetic error in Armando's own initial reserve sizing for
    AMS (a stated "3 years of expenses" that neither of the two
    obvious readings of his own numbers produced) was caught and
    corrected before being recorded -- Armando confirmed the intended
    figure was ~4 years of the annual income gap.

Concrete findings this produced, none of which existed before this
data was assembled:

-   AML's current dry powder (74.375€) sits 50.625€ below its own
    125.000€ suelo -- the safety cushion is intact, but the
    opportunity-capital reserve is under-armed relative to Armando's
    own target.
-   AMS's current liquidity (172.330,77€) sits 22.330,77€ above its
    own 150.000€ techo -- idle cash by Armando's own definition, with
    no offsetting deficit anywhere else in that patrimonio.
-   AML's Pibank time deposit (85.000€) matures 2026-08-26, its
    Myinvestor deposit (60.000€) matures 2026-09-29 -- both flagged as
    the near-term source for AML's not-yet-operational Fondo
    Monetario.

Deliverable: `data/raw/personal_capacity_facts.xlsx`, three tabs
(Notas, AMS, AML), built with the project's `xlsx` skill discipline --
formulas rather than hardcoded derived values, blue font for manual
inputs, black for formulas, cell-level source citations pointing back
to each real portfolio file's sheet and field, and the "Total
patrimonio" row shaded per Armando's request for visual emphasis.
Recalculated via LibreOffice with zero formula errors across 37
formulas; every derived figure above was read from the recalculated
file, not computed independently in this document.

What this does not authorize:

-   No adapter code. `build_local_personal_capacity_facts_inputs()`
    (or equivalent) still does not exist. This file is not consumed by
    `PersonalCapacityFactsGate`, `posture_mapper.py`, or any other
    code -- it is a structured manual/semi-automatic input artifact
    only.
-   No resolution of the two-patrimonio representation question at the
    dataclass level. `LocalPersonalCapacityFactsInputs` remains
    single-patrimonio in code. Whether the future adapter produces two
    separate gate evaluations, a combined one, or something else is
    explicitly undecided.
-   No change to `PersonalCapacityFactsGate`, `posture_mapper.py`, the
    Dry Powder Protocol specification, or any Frozen Core component.
-   Two open items intentionally left for Armando, not silently
    assumed: AMS's income-concentration qualitative call (adequate /
    not) is still pending his explicit confirmation; the 155.000€ vs.
    150.000€ rounding on AMS's total-liquidity ceiling implies a
    120.000€ pólvora-techo assumption that has not been explicitly
    confirmed as final.

Boundary:

-   One new file: `data/raw/personal_capacity_facts.xlsx`. No code
    files touched.
-   No Frozen Core component touched.
-   Personal Capacity remains entirely outside the operative flow.
-   Documentation of real data, not real automation -- the honest
    progress this represents is captured explicitly as a separate,
    smaller number than "operational" would imply (see Honest Progress
    Snapshot, RE-DOC-005).

------------------------------------------------------------------------

## RE-043.1 — Personal Capacity Facts: real adapter, generic across patrimonios

RE-043.1 closes the code half of the gap RE-042.1 left open: a real
`build_local_personal_capacity_facts_inputs()` now reads
`data/raw/personal_capacity_facts.xlsx` and produces one
`LocalPersonalCapacityFactsInputs` per patrimonio, evaluated by
`PersonalCapacityFactsGate` and combined into a real capital posture
via `posture_mapper.py` -- for the first time with real numbers, not
synthetic ones.

Architecture decision, confirmed by Armando before any code was
written: AMS and AML are two independent capital postures, never
merged into one. This is not incidental -- it is required for a
second, explicit reason Armando gave: the system must scale to future
third-party patrimonios by adding a spreadsheet tab, not by touching
code. The adapter reflects this directly: it iterates every sheet in
the workbook except "Notas" and treats each as an independent
patrimonio, locating each required value by the exact text of its
"Concepto" cell rather than by row/column coordinate. Any sheet is
free to carry extra breakdown rows or notes that differ from every
other sheet, as long as it reuses the canonical labels the adapter
requires.

RE-032.3 explicitly declined to set numeric thresholds for any of its
nine categories ("No numeric thresholds for any category"). Turning
raw spreadsheet numbers into the gate's booleans required deciding
that boundary for the first time -- proposed, critiqued, and revised
before being written, not invented unilaterally:

1.  **Available liquidity** -- `liquidez_total_actual >= suelo_total_liquidez`.
2.  **Near-term cash needs** -- `ingresos_recurrentes >= gasto_anual`
    OR `liquidez_total_actual >= colchón`. Documented explicitly:
    "covered" accepts being covered by the safety cushion, not only by
    ongoing income.
3.  **Fixed obligations** -- v1 alias of #2, not an independent check.
    Per Armando's own clarification that "obligaciones fijas" means
    annual expenses, the same figure #2 already uses.
4.  **Debt service** -- read from the "Servicio de deuda manejable"
    cell, not hardcoded in code. An earlier draft of this proposal
    fixed this to `True` in Python; Armando's review caught it as a
    real near-bug, not a style note -- a hardcoded constant would never
    notice if either patrimonio took on debt in the future.
5.  **Income concentration** -- read directly from a "Valoración
    cualitativa (concentración de ingresos)" cell (renamed from the
    ambiguous "Valoración cualitativa" RE-042.1 originally used, now
    that a second such cell exists in the same sheet).
6.  **Portfolio concentration** -- same pattern, new cell "Valoración
    cualitativa (concentración de cartera)" added to both sheets.
7.  **Required emergency reserve** -- `liquidez_total_actual >= colchón`,
    hard block on breach (RE-032.5, unchanged). Documented explicitly
    that this shares its underlying liquidity figure with #1 at a
    different threshold (suelo vs. colchón) -- two deliberately
    different tests on the same number, not two independent data
    points, per Armando's review.
8.  **Known time horizon constraints** -- new cell "Próximo evento con
    necesidad de liquidez conocida". Only the explicit token "Ninguno
    conocido" reads as favorable; a blank cell reads as not-measured,
    never as favorable by default.
9.  **Fiscal / operational constraints** -- new cell "Restricciones
    fiscales pendientes", same explicit-token discipline as #8
    ("Ninguna conocida"). An earlier draft of this proposal defaulted
    an empty cell to `True` on the reasoning that the one known fiscal
    trap (AML's Planes de Pensiones) was already excluded elsewhere --
    Armando's review rejected this as a real fail-closed violation
    regardless of how safe the reasoning felt, not a style
    preference.

Input-type taxonomy, the condition Armando set for green-lighting this
work: every field now has a documented `input_type` in
`FIELD_INPUT_TYPES` (`engine/personal_capacity_facts_gate.py`) --
`COMPUTED` (derived purely from other recorded figures), `OPERATOR_FACT`
(entered directly because no formula exists, e.g. debt service),
or `OPERATOR_JUDGMENT` (a structured call the operator makes visible
in the same sheet, e.g. income concentration). This is a three-way
split, not the two-way split first proposed in review: collapsing
`OPERATOR_JUDGMENT` into the same treatment as RE-032.4's attested
channel would import machinery (cooling-off periods, 90-day validity)
built specifically against self-interested revision under emotional
stress -- a risk that does not apply to an analytical judgment like
income-source diversification. `FIELD_INPUT_TYPES` is asserted in code
to stay in sync with `FACT_FIELDS`, not just documented by convention.

A bug caught by the first real-pipeline run, not by review: the
"Pendiente" placeholder Armando's own spreadsheet convention uses for
"not filled in yet" was initially read by `_to_bool_explicit_none_token()`
as real content -- any non-blank, non-"Ninguno/Ninguna conocida" text
resolved to `False` ("confirmed breach"), so both new fields showed as
confirmed failures for both patrimonios before a single manual cell
had been filled in. The practical posture outcome was unaffected
(`False` and `None` both push the ceiling toward `Conserve`), but the
explanation was dishonest -- exactly what this iteration's own
provenance discipline exists to prevent. Fixed by treating "pendiente"
as a null-equivalent token, identically to a blank cell.

Concrete, end-to-end validation: running the real adapter today
produces AMS at `not measurable` (four fields still "Pendiente") and
AML at `constrained`, driven specifically by `liquidity_adequate:
confirmed breach` -- the exact same finding RE-042.1 established by
manual arithmetic (AML's 74.375€ of dry powder sits below its
125.000€ suelo). This is the first time that finding has come out of
the automated pipeline rather than a spreadsheet formula read by a
human. `audit_posture.py` now loops over every patrimonio the workbook
contains and prints a combined posture per patrimonio; both currently
resolve to `Conserve`, but for AML that ceiling now has a genuine
Personal Capacity contribution in its explanation, not just Regime
Comparability riding alone.

New file: `loaders/personal_capacity_facts_loader.py` -- raw
Concepto/Valor extraction only, no boolean interpretation, mirroring
the existing `loaders/shiller_loader.py` / `engine/drawdown_engine.py`
split (raw file I/O stays out of engine modules).

What this does not authorize:

-   No wiring into `run.py` or `DecisionEngine` -- `audit_posture.py`
    remains a read-only dry-run, exactly as RE-039.1 established.
-   No change to the attested-judgement / Human Approval channel
    (RE-032.4) -- it remains entirely uncoded, by design, and
    `OPERATOR_JUDGMENT` fields are explicitly not routed through it.
-   No change to `PersonalCapacityFactsGate.evaluate()`'s own logic,
    `HARD_BLOCK_FIELDS`, `gate_combination.py`, or any Frozen Core
    component.
-   No resolution of what "Restricciones fiscales pendientes" or
    "Próximo evento con necesidad de liquidez conocida" should say for
    either patrimonio -- both remain "Pendiente" (not-measured), left
    for Armando to fill in, not guessed at.
-   No numeric threshold for portfolio concentration -- category 6
    stays an operator judgment call precisely because no threshold was
    agreed.

Boundary:

-   New file: `loaders/personal_capacity_facts_loader.py`.
-   Modified: `engine/personal_capacity_facts_gate.py` (taxonomy +
    adapter + helpers), `audit_posture.py` (per-patrimonio loop),
    `tests/verify_personal_capacity_facts_gate.py` (real-pipeline
    section), `tests/verify_posture_mapper.py` (corrected a now-stale
    claim that no real data source existed), `data/raw/personal_capacity_facts.xlsx`
    (three new cells per patrimonio, two renamed for lookup
    disambiguation).
-   No Frozen Core component touched.
-   Structural verification only in this sandbox (all `tests/verify_*.py`
    pass except the three pre-existing, unrelated
    `RUNTIME : MISMATCH` failures and one `match_bottoms` tie-order
    difference in `verify_research_engine.py` -- none of today's
    changed files are imported anywhere in that test's dependency
    chain, so this is the same sandbox-vs-pinned-runtime gap already
    documented elsewhere in this project, not a regression introduced
    here). Pending confirmation under Armando's pinned runtime.

------------------------------------------------------------------------

## RE-043.2 — Personal Capacity Facts: remaining manual inputs resolved, first ADEQUATE result

RE-043.2 closes the four "Pendiente" cells RE-043.1 deliberately left
open rather than guessed at (AMS income/portfolio concentration, AML
portfolio concentration, and the known-horizon-event field for both
patrimonios), plus the two fiscal facts flagged as still missing.

Before writing "Adecuado" for AML's portfolio concentration on
Armando's summary alone ("repartido en 3 fondos"), the underlying
`02. Fondos Myinvestor` sheet was read directly. The claim was true but
incomplete: three fund vehicles exist, but two of them (Vanguard
US500, Fidelity S&P500) track the same index, so the real split is
Vanguard 87.2% + Fidelity 0.4% + iShares Developed World 4.0% -- roughly
91% effectively the same US-large-cap bet under two providers, not
three genuinely different exposures. This total reconciles exactly
against the Resumen tab's Fondos RV figure (2.183.088,49€) once the
sheet's own TOTAL row -- which bundles in 199.375€ of cash sitting in
the same brokerage account, confirmed to the cent against the
Liquidez+Depósitos figure -- is excluded. Presented back to Armando
before any cell was written; his answer did not change the boolean
(US/S&P500 concentration is the SOP's own starting thesis, not a flaw)
but the verification stands on its own -- the input this iteration
would otherwise have accepted uncritically was less diversified than
described.

Similarly, Iberdrola's "10,6% dividend yield" (from `05. Acciones`)
was confirmed to be yield on original cost basis (110.827,52€), not on
current market value (356.040€, where the real yield is ~3,3%) --
recorded as context, not as the number itself, so a future reader
does not mistake cost-basis yield for current yield.

New fiscal fact: AML also carries a pending tax-loss carryforward
(-162.000€, TEF), previously uncaptured. Both patrimonios' minusvalías
(AMS -215.092€, AML -162.000€) now carry the same note: a 4-year
window to offset against future capital gains, after which the credit
expires unused if not applied. Recorded as informational context on
each minusvalía row, not as a new boolean -- a minusvalía is favorable
(reduces future tax), not a restriction, so `fiscal_operational_constraints_manageable`
stays read from "Restricciones fiscales pendientes" (now "Ninguna
conocida" for both, confirmed explicitly, not assumed).

New context row, not a new fact: AMS's income concentration is
"Adecuado" (Armando confirmed the distribution itself is fine), but he
flagged a different, real objective that doesn't map to any of
RE-032.3's nine categories -- closing the 7.000€/year gap with
predictable passive income rather than the variable consultancy income
that has covered it historically. Recorded as an "Objetivo declarado"
row next to the gap calculation, explicitly labelled as context for a
future reader, not a tenth fact silently added to the gate.

Result: for the first time, both patrimonios have all nine fields
populated with real, explicit values -- zero "Pendiente" cells left.
AMS evaluates to `ADEQUATE` (nine of nine favorable). AML evaluates to
`CONSTRAINED` with exactly one failed field (`liquidity_adequate`) and
zero missing fields -- the dry-powder shortfall already established in
RE-042.1/RE-043.1 is now the sole, isolated reason for AML's ceiling,
not one signal mixed in with several unknowns.

What this does not authorize:

-   No change to `PersonalCapacityFactsGate`, the adapter's threshold
    logic, or `FIELD_INPUT_TYPES` -- this iteration is data only.
-   No numeric concentration threshold introduced for portfolio
    concentration -- still an operator judgment call, confirmed rather
    than computed.
-   No new field added for AMS's declared income objective -- it is
    context, explicitly not one of the nine gate inputs.
-   No wiring into `run.py` or `DecisionEngine`.

Boundary:

-   One file modified: `data/raw/personal_capacity_facts.xlsx` (six
    cells resolved from "Pendiente", one new minusvalía row for AML,
    one new context row for AMS, notes updated on both existing
    minusvalía rows).
-   One test file modified: `tests/verify_personal_capacity_facts_gate.py`
    (real-pipeline expectations updated: AMS now `ADEQUATE`, AML's
    `missing_fields` now asserted empty).
-   No code files touched besides that test.
-   No Frozen Core component touched.
-   Structural verification only in this sandbox -- zero formula
    errors across the recalculated workbook, `PersonalCapacityFactsGate`
    and `audit_posture.py` both re-run against the updated file and
    confirmed to produce the results described above. Pending
    confirmation under Armando's pinned runtime.

------------------------------------------------------------------------

## RE-DASH.1.14 — Dashboard: three-zone liquidity bar

Armando shared a detailed design reference (his own words: "no lo
tomes al pie de la letra, solo como referencia mejorable") for a
"liquidity range bar" -- three colored zones (déficit/objetivo/
ocioso), suelo/techo/actual labels, a diagnostic word. Compared
against RE-DASH.1.13's bar rather than adopted verbatim:

-   Color mapping (rojo=bajo suelo, verde=dentro, ámbar=sobre techo,
    explicitly not verde for "over ceiling" since idle liquidity is a
    SOP finding, not a win) was already exactly what
    `liquidity_status()` returns -- confirmed, not changed.
-   Added what was genuinely missing: three color zones on the track
    itself (same pale tints as `.pill.bad/.ok/.warn`, not new colors),
    computed from `LIQUIDITY_BAR_CLAMP_MIN/MAX` -- the same constants
    that clamp the marker's position, so a boundary and a marker
    resting on it can never silently disagree.
-   Suelo/techo absolute figures, dropped from the visible row in
    RE-DASH.1.13 to declutter per Armando's own prior request, restored
    as a `title` attribute (native HTML hover tooltip, no script) --
    same justification as `<details>` elsewhere: metadata available on
    demand, not clutter in the default view. Still also in Detalle
    técnico.
-   Declined the "two cards, one per patrimonio" layout from the
    reference: kept the existing row-per-patrimonio table. Reasoned,
    not silent -- Armando's own prior instruction this same session
    was to make Datos de mercado fit "en una línea" and reduce density;
    a full separate card per patrimonio would have worked against
    that, and diverged from the row-based pattern "Postura y permisos"
    and "Datos de mercado" already use. Told to Armando directly, with
    an offer to build the card layout instead if he still prefers it
    after seeing the reasoning.

What this does not authorize:

-   No change to `liquidity_status()`, `liquidity_gap()`, or any gate/
    protocol file -- the zone boundaries and marker position are both
    presentation-layer derivations of numbers those functions already
    return.

Boundary:

-   One file modified: `generate_dashboard.py`
    (`LIQUIDITY_BAR_CLAMP_MIN/MAX` constants; `liquidity_bar()` gains
    the zone gradient and `title` tooltip).
-   No Frozen Core component touched.
-   Verified by direct execution against real data:
    `outputs/dashboard.html` regenerated. Spot-checked: AMS's marker
    at 115% (ámbar zone, past the techo boundary) and AML's at -15%
    (rojo zone, past the suelo boundary) -- both match the
    already-verified real figures. Zone boundaries computed as 11.5%/
    88.5%, matching the -15/115 clamp bounds by construction. Full
    `tests/verify_*.py` suite re-run: same four pre-existing failures,
    nothing new.

------------------------------------------------------------------------

## RE-PRED.17 — Similarity Engine v2 (dimension enrichment): not
   pursued, decision recorded

Armando pidió avanzar a "Similarity Engine v2" tras RE-KERNEL.1, citado
como "próximo hito" en la documentación de proyecto. Antes de proponer
diseño, verificación directa contra el código real encontró dos cosas:

1.  **La premisa estaba desactualizada.** Duración, velocidad,
    tendencia previa (`pre_crash_return_3y`), volatilidad y
    ponderaciones (`SIMILARITY_WEIGHTS`, `core/constants.py`) ya están
    implementadas en `engine/similarity_engine.py` -- no son trabajo
    pendiente. La nota de "próximo hito: enriquecer con nuevas
    dimensiones" en `PROJECT_STATE.md` (ya retirado, Sección 9) estaba
    desactualizada.
2.  **La evidencia ya reunida argumenta en contra de "más dimensiones"
    como próximo paso productivo.** `RE-PRED.13`-`RE-PRED.16` (ya
    canónicas, confirmadas bajo runtime fijado, con bootstrap de
    clusters dependientes, no solo estimaciones puntuales) encontraron:
    el modelo combinado tiene rank correlation negativa (-0,26505)
    contra los retornos reales a 5 años; un heurístico trivial de
    mean-reversion (solo -drawdown, sin comparables) tiene rank
    correlation positiva (+0,26316); esa brecha es real bajo
    resampling dependence-aware, no ruido de muestra (RE-PRED.16,
    intervalo del 90% `[-0,94270, -0,34208]`, enteramente negativo);
    y aislar cada dimensión activa una a una (RE-PRED.14) no recupera
    correlación positiva en ninguna -- descartando que sea un problema
    de ponderación. La hipótesis de trabajo registrada, no autorizada
    como hecho: el problema podría ser el propio mecanismo de vecino-
    más-cercano-y-mediana, no las dimensiones que alimenta.

Presentado a Armando explícitamente, con tres opciones (dejarlo como
está; investigar el mecanismo de selección en vez de las dimensiones;
añadir dimensiones de todas formas pese al hallazgo). Decisión:
**dejarlo como está.** `SimilarityEngine` sigue siendo Frozen Core, sus
limitaciones ya están honestamente reportadas (Evidence Quality Gate
ya marca `predictive_validation_status` como `NOT_DEMONSTRATED`, per
RE-PRED.16's confirmed finding), y no se añaden dimensiones que la
evidencia ya reunida sugiere que no resolverían el problema real.

What this does not authorize:

-   No change to `SimilarityEngine`, `SIMILARITY_WEIGHTS`, or any
    Frozen Core component -- esta iteración es puramente una decisión
    documentada, cero código.
-   No reopens RE-PRED.13-16's findings -- se citan, no se
    reinterpretan.
-   No closes the door permanently -- "investigar el mecanismo de
    selección" queda registrado como la dirección con mejor
    justificación evidencial si algún día se retoma, distinta de
    "añadir dimensiones".

Boundary:

-   Documentation-only. No code changed.
-   `docs/CONSTITUTION.md` Sección 10 actualizada para reflejar esta
    decisión, no solo "baja prioridad, sin disparador".

------------------------------------------------------------------------

## RE-KERNEL.1 — Kernel assembly layer: extracción de audit_posture.py
   a un módulo importable

Armando, sobre unificar el Kernel: "extraer lo que ya existe a un
módulo" -- explícitamente NO diseñar K1/K2/K3/K5/K6 (Constitución,
Sección 5), que hoy no tienen ni spec. Confirmado con tres precisiones
suyas antes de escribir código:

1.  **Docstring defensivo** en `engine/kernel.py`: dice explícitamente
    que esto NO es el Kernel constitucional completo, solo centraliza
    los fragmentos K4/gobernanza ya implementados (Evidence Quality,
    Regime Comparability, Personal Capacity Facts, Human Approval,
    Dry Powder) -- no implementa K1/K2/K3/K5/K6, no ejecuta decisiones,
    no está wired a `run.py`/`DecisionEngine`.
2.  **Contrato de `None`**: el segundo elemento de la tupla que
    devuelve `build_kernel_results()` es `None` única y exclusivamente
    cuando `data/raw/personal_capacity_facts.xlsx` no se encuentra --
    nunca para otros fallos (falta de atestación de Human Approval,
    falta de ledger, sin episodio activo), que se representan como
    resultados parciales con el campo afectado a `None`, exactamente
    como ya hacía `audit_posture.py`.
3.  **Criterio de aceptación**: salida de `audit_posture.py` idéntica
    antes/después del refactor.

**Desviación real encontrada al implementar, no aplicada en
silencio**: el diseño original (aprobado literalmente por Armando)
proponía que `build_kernel_results()` devolviera un `None` desnudo
para toda la tupla cuando falta el fichero de hechos personales. Eso
habría sido incorrecto -- `audit_posture.py`, en esa misma rama,
siempre imprimió Evidence Quality, Regime Comparability y una postura
combinada de solo esos dos gates (nunca dependieron de ese fichero).
Un `None` desnudo habría hecho imposible reproducir esa salida.
Corregido: `KernelMarketResult` siempre se devuelve; solo el segundo
elemento (por patrimonio) puede ser `None`. Se añadió también
`combined_posture_without_personal_capacity` a `KernelMarketResult`
-- el fallback de dos gates que el script original computaba en esa
rama -- para que el wrapper no tenga que re-derivar lógica de gates
por su cuenta.

**Segunda diferencia real encontrada al verificar, no ignorada**: la
comparación carácter a carácter reveló una diferencia genuina (no
cosmética por defecto, investigada antes de descartarla): dos líneas
de aviso ("Etiquetas de Concepto repetidas...") cambian de posición
en la salida. Rastreado hasta su origen exacto:
`loaders/personal_capacity_facts_loader.py:93` -- un `print()` directo
dentro del loader (no un `warnings.warn()`, no va a stderr), que se
dispara en el momento en que se llama al loader. Como
`build_kernel_results()` calcula todo antes de que el wrapper imprima
nada, ese aviso ahora sale al principio en vez de a mitad de
ejecución -- mismo texto exacto, misma información, distinta posición
en el stream. Verificado explícitamente: excluyendo esas dos líneas,
el resto de la salida es idéntico carácter a carácter.

What this does not authorize:

-   No K1/K2/K3/K5/K6 -- siguen sin spec, sin código.
-   No wiring a `run.py` ni `DecisionEngine`.
-   No cambio a ningún gate, protocolo, ni a la separación Human
    Approval / `min()` de gates (Sección 5, Constitución) -- Human
    Approval sigue siendo un campo separado en
    `KernelPatrimonioResult`, nunca combinado dentro de
    `combined_posture`.

Boundary:

-   One file added: `engine/kernel.py` (`KernelMarketResult`,
    `KernelPatrimonioResult`, `build_kernel_results()`).
-   One file rewritten as a thin wrapper: `audit_posture.py` -- toda
    su lógica de orquestación (RE-039.1 a RE-C) se movió a
    `engine/kernel.py` sin cambiar una sola decisión; este archivo
    ahora solo llama y imprime.
-   No Frozen Core component touched -- ningún gate, protocolo, ni
    loader modificado en su lógica (el `print()` del loader que causó
    la reordenación ya existía, no se tocó).
-   Verified by direct execution against real data: salida de
    `python3 audit_posture.py` capturada antes y después del refactor;
    diff exacto de solo dos líneas (el aviso reordenado, explicado
    arriba); excluyendo esas dos líneas, cero diferencias. Full
    `tests/verify_*.py` suite re-run: mismo único fallo preexistente
    (`verify_research_engine.py`, orden, no valores), nada nuevo.

------------------------------------------------------------------------

## RE-DOC-006 — Constitución y Avance honesto sincronizados con el
   estado real del dashboard

Armando pidió un recap del estado del proyecto (2026-08-17). Al
verificar directamente contra el repo, en vez de contra la memoria de
la conversación, aparecieron dos huecos reales de documentación, no
solo de estilo:

-   `CONSTITUTION.md`, Sección 4 (tabla de módulos) y Sección 10
    (Pendiente), seguían diciendo que "Dashboard" estaba **pendiente**
    y que RE-DASH.1 estaba "listo para empezar en cuanto se retome" --
    cuando en realidad el dashboard operativo llevaba hasta
    RE-DASH.1.21, y el panorama histórico de Shiller (RE-SHILLER-
    DASH.1 a .8, un panel completo, no una nota al margen) no aparecía
    mencionado en ningún sitio de la Constitución.
-   La tabla "Avance honesto" de este mismo documento tenía una única
    fila de "Dashboard (RE-DASH.1)" congelada en el estado de
    RE-DASH.1.12 -- desactualizada desde antes de que empezara la
    mayor parte del trabajo de diseño de esta sesión.

Corregido: Sección 4 y Sección 9 de `CONSTITUTION.md` reflejan ahora
los dos dashboards como existentes (con qué cubre cada uno); Sección
10 marca la categoría "Construible ya" como vacía explícitamente (no
se borra sin más -- se dice que está vacía y por qué, siguiendo el
mismo principio de esta tabla de no ocultar huecos); la tabla "Avance
honesto" de abajo separa el dashboard operativo del panorama histórico
en dos filas, cada una con su alcance real.

What this does not authorize:

-   No functional change anywhere -- pure documentation sync, zero
    code touched.

Boundary:

-   Two files modified: `docs/CONSTITUTION.md` (Sección 4 tabla de
    módulos, Sección 9 Entregables, Sección 10 Pendiente) and this
    file (Avance honesto table).
-   No Frozen Core component touched.
-   Verified by direct inspection: `git log` confirms RE-DASH.1.21 and
    RE-SHILLER-DASH.1-8 are committed and pushed; the previous
    Constitution text was checked against that log before being
    corrected, not assumed stale from memory.

------------------------------------------------------------------------

## RE-SHILLER-DASH.8 — Panorama histórico: sección de CAPE, de cuatro
   párrafos a dos

Armando: "simplifica el apartado de CAPE. Que sea facil de ver como se
construye ese CAGR... me gusta una conclusion mas de este tipo en lugar
de tanta palabrería donde te pierdes", con un ejemplo textual del tono
que quería. Tenía razón -- el arreglo de RE-SHILLER-DASH.6 para "no
entiendo" se pasó de frenada: un párrafo "cómo leer esta tabla", un
ejemplo trabajado con 6 cifras, una nota de metodología y un caveat --
cuatro párrafos antes de llegar a la tabla.

Reducido a dos: una línea sobre qué es el número ("ya descuenta la
inflación y reinvierte dividendos"), y una conclusión con la forma
exacta que pidió Armando (zona extrema -> retornos muy inferiores a la
media, especialmente a 5-10 años; muestra pequeña y concentrada ->
contexto de valoración, no señal operativa). El ejemplo de retorno
acumulado y el detalle de qué periodos concretos forman cada bucket
(1999-2000, 1998-2001/2021-2026, de RE-SHILLER-DASH.5/6) se retiran de
la vista -- siguen registrados en gobernanza si hace falta recuperarlos,
la columna N sigue exponiendo el tamaño de muestra por fila.

What this does not authorize:

-   No change to any underlying number -- pure text/paragraph
    reduction in the presentation layer.

Boundary:

-   One file modified: `generate_shiller_dashboard.py` (removed the
    now-unused `cumulative_Xy` computation from
    `build_cape_return_stats()`; removed the `cape_gt_40_n`/
    `cape_gt_40_row`/`cape_all_row` lookups from `render_html()`;
    "Retornos reales posteriores según CAPE inicial" card reduced from
    four paragraphs to two).
-   No Frozen Core component touched.
-   Verified by direct execution against real data: `outputs/
    shiller_dashboard.html` regenerated and extracted -- section now
    shows exactly two paragraphs plus the table, no dead code left
    behind. Full `tests/verify_*.py` suite re-run: same single
    pre-existing failure (`verify_research_engine.py`, ordering only),
    nothing new. `generate_dashboard.py` (operational) regenerated
    separately, unaffected.

------------------------------------------------------------------------

## RE-SHILLER-DASH.7 — Panorama histórico: episodios con nombre,
   acotados al siglo XX-XXI

Armando, inmediato tras RE-SHILLER-DASH.6: "centra los episodios en el
siglo XX y XXi." Resuelve directamente el propio flag de riesgo de
alucinación que RE-SHILLER-DASH.6 dejó abierto sobre el tercer episodio
nombrado (1872-1877, correspondencia no verificada con el Pánico de
1873) -- en vez de intentar confirmar esa fecha con una fuente, la
selección de "peores episodios con nombre" ahora filtra el fondo de
episodios a peak_date >= 1900 antes de tomar los 3 peores. Nuevo tercer
lugar: 2000.08->2003.02 (-43,7%), estallido de la burbuja puntocom --
bien documentado, sin ambigüedad de fecha, igual que los otros dos.

What this does not authorize:

-   No change to episode detection or any gate -- a narrower ranking
    pool over the same 23 episodes, nothing recalculated.

Boundary:

-   One file modified: `generate_shiller_dashboard.py`
    (`NOTABLE_DRAWDOWN_MIN_YEAR` added; `NOTABLE_DRAWDOWN_NAMES`'s
    third entry replaced; `build_notable_drawdowns()` filters the pool
    before ranking; the table's caveat note simplified since all three
    names are now high-confidence).
-   No Frozen Core component touched.
-   Verified by direct execution against real data: `outputs/
    shiller_dashboard.html` regenerated and extracted. Table now shows
    exactly 1929.09->1932.06 (-84,8%, Gran Depresión), 2007.10->
    2009.03 (-50,8%, crisis financiera global de 2008), 2000.08->
    2003.02 (-43,7%, estallido de la burbuja puntocom) -- confirmed via
    direct query that these are the real top-3-by-magnitude episodes
    with peak_date >= 1900 among the 23 detected. Full
    `tests/verify_*.py` suite re-run: same single pre-existing failure
    (`verify_research_engine.py`, ordering only), nothing new.

------------------------------------------------------------------------

## RE-SHILLER-DASH.6 — Panorama histórico: episodios con nombre, y la
   tabla de CAPE explicada de verdad

Armando, inmediatamente tras ver RE-SHILLER-DASH.5: "yo aquí, aparte de
la media, introduciría los dos o tres peores episodios de drawdowns que
tienen nombre y apellidos"; "NO entiendo las cifras de la tabla de
CAPE."

-   **Peores episodios con nombre**, nueva tabla dentro de "Resumen de
    drawdowns históricos": los 3 peores por magnitud de los 23
    detectados (no elegidos por fama, calculados). 1929.09->1932.06
    (-84,8%) = Gran Depresión / Crac de 1929; 2007.10->2009.03 (-50,8%)
    = crisis financiera global de 2008 -- ambos identificados con alta
    confianza, episodios ampliamente documentados. El tercero,
    1872.05->1877.06 (-47,3%), lleva su propia advertencia dentro del
    nombre en vez de una nota aparte: la fecha de pico que detecta el
    motor precede en más de un año al Pánico de 1873 tal y como se
    documenta habitualmente, la correspondencia no está verificada con
    precisión -- riesgo de alucinación señalado explícitamente en vez
    de una etiqueta histórica presentada como hecho.
-   **La tabla de CAPE no se entendía porque le faltaba explicación, no
    porque Armando no supiera leerla**: llevaba jerga ("CAGR",
    "anualizado") antes de decir qué significan los números, y nunca
    explicaba por qué el retorno a 15 años es positivo cuando el de 5 y
    10 es negativo (parece una contradicción sin saber que es reversión
    a la media). Corregido con un párrafo en lenguaje llano al principio
    de la sección, con un ejemplo concreto usando la fila más parecida
    a hoy (CAPE > 40): -4,5%/-3,4%/+2,1% anual a 5/10/15 años equivale a
    -21%/-30%/+36% acumulado en esos mismos periodos -- cifras
    acumuladas calculadas en Python junto a las medianas, no escritas a
    mano en el texto, para que no puedan desalinearse de la tabla.
    Contraste explícito con la fila "todos los meses" (6,7% anual a 15
    años) para que quede claro que incluso el "positivo" a 15 años
    queda muy por debajo de lo normal. Cabeceras de columna reescritas
    ("A 5 años" en vez de "Retorno real 5a").

What this does not authorize:

-   No change to `drawdown_engine.py`, episode detection, or any gate --
    both fixes are new content/wording in the presentation layer only.

Boundary:

-   One file modified: `generate_shiller_dashboard.py`
    (`NOTABLE_DRAWDOWN_NAMES`, `N_NOTABLE_DRAWDOWNS` added;
    `build_notable_drawdowns()`, `build_notable_drawdowns_table()`
    added; `build_cape_return_stats()` now also computes
    `cumulative_Xy` per bucket/horizon; new plain-language lead
    paragraph and reworded headers in the CAPE returns section).
-   No Frozen Core component touched.
-   Verified by direct execution against real data: `outputs/
    shiller_dashboard.html` regenerated and extracted. Named episodes
    table shows exactly the 3 real top-by-magnitude episodes with
    correct dates/durations (1929-09->1932-06, 33 meses; 2007-10->
    2009-03, 17 meses; 1872-05->1877-06, 61 meses). CAPE lead paragraph
    shows "-4,5% anual ... -21% acumulado" / "-3,4% anual ... -30%
    acumulado" / "2,1% anual ... 36% acumulado" for CAPE>40, matching
    the table's own median row exactly (no drift, since both come from
    the same computed dict). Full `tests/verify_*.py` suite re-run:
    same single pre-existing failure (`verify_research_engine.py`,
    ordering only), nothing new. `generate_dashboard.py` (operational)
    regenerated separately, unaffected.

------------------------------------------------------------------------

## RE-SHILLER-DASH.5 — Panorama histórico: retornos por CAPE, resumen
   de drawdowns, lectura más clara

Armando's structured review of v2: "ya no es solo un conjunto de
gráficas... como v1 está bien. Añadiría poca cosa, pero hay tres piezas
que sí me parecen relevantes." He scoped the iteration himself to two
of the three: "añadiría solo dos bloques: 1. Retornos posteriores según
CAPE inicial. 2. Resumen de drawdowns históricos." The third (CAPE-style
percentiles for inflación/tipo) is his own deferral, not dropped by
omission -- next round, if he wants it.

-   **Retornos reales posteriores según CAPE inicial** (new section,
    after the CAPE chart). For every month with a valid CAPE reading,
    the real total-return CAGR at 5/10/15 years forward -- same
    "Price.1" basis (dividends reinvested) and same nearest-date/CAGR
    formula `drawdown_engine.py`'s own `future_return_5y/10y` already
    use, just computed for every month instead of only the 23 episode
    bottoms (new, local `_forward_real_total_return()` -- does not
    touch `drawdown_engine.py`). Grouped into Armando's own buckets
    (todos los meses, CAPE>30/35/40), reduced to the median, with an
    N-per-bucket column he didn't ask for but that makes his own
    caveat concrete rather than generic: verified by direct inspection
    that the "CAPE > 40" bucket (24 months) is almost entirely one
    historical cluster (1999-2000, plus today's still-too-recent
    months with no forward return yet), and "CAPE > 35" combines two
    distinct periods (1998-2001, 2021-2026) -- not dozens of
    independent trials. Armando's caveat sentence kept verbatim
    alongside that disclosure.
-   **Resumen de drawdowns históricos** (new section, after the price
    chart): median/worst drawdown, median peak->bottom duration, median
    bottom->recovery duration -- pure aggregation over the same 23
    `Episode` objects already shaded on the price chart, no new
    detection logic. All 23 have recovered within the series (none
    still open), consistent with the market being at an all-time high
    today.
-   **Wording fix, "Detalle de indicadores"**: Armando: "inflación
    aparece como 'Cerca de la media', pero 4,23% vs 2,31% puede
    chirriar visualmente." The z-score classification is correct and
    NOT changed (inflación's std is 5.76pp -- a century spanning
    hyperinflation/deflation makes the "near" band genuinely wide;
    `Z_THRESHOLD_NEAR` is Armando-confirmed and shared with the
    operational dashboard's own `_context_words()` -- out of scope to
    touch for a one-table wording complaint). New, local
    `_readable_lectura()`: when the band is "Cerca de la media" but the
    raw value sits above/below the raw mean, the "Lectura" column says
    so explicitly ("Por encima de la media, dentro del rango histórico
    habitual") instead of just "Cerca" -- applied consistently to all
    three z-scored rows (CAPE, Inflación, Tipo), not only the row
    Armando pointed at. Dot color and headline-driver selection
    untouched -- both still key off the raw, unmodified short_label.

What this does not authorize:

-   No change to `drawdown_engine.py`, any gate, protocol, model, or
    loader -- the forward-return calculation is new, local, presentation-
    layer code in `generate_shiller_dashboard.py` only, deliberately not
    added to the Frozen Core's `Episode` model.
-   No change to `generate_dashboard.py`'s `_context_words()` or
    `Z_THRESHOLD_NEAR` -- shared, Armando-confirmed thresholds used by
    the operational dashboard too; the wording fix is local to this
    file's own "Lectura" column text only.

Boundary:

-   One file modified: `generate_shiller_dashboard.py`
    (`CAPE_RETURN_BUCKETS`, `FORWARD_RETURN_YEARS` added;
    `_forward_real_total_return()`, `build_cape_return_stats()`,
    `build_drawdown_summary()`, `_readable_lectura()`,
    `build_cape_returns_table()`, `build_drawdown_summary_table()`
    added; `build_shiller_data()` returns two new keys;
    `build_indicator_strip()`'s Lectura column now runs through
    `_readable_lectura()`; two new `<section class="card">` blocks in
    `render_html()`).
-   No Frozen Core component touched.
-   Verified by direct execution against real data: `outputs/
    shiller_dashboard.html` regenerated and extracted. Retornos por
    CAPE: Todos los meses 7,2%/6,6%/6,7% (n=1747); CAPE>30 -1,1%/
    -1,1%/2,2% (n=135); CAPE>35 -4,1%/-3,0%/2,1% (n=69); CAPE>40
    -4,5%/-3,4%/2,1% (n=24) -- all computed directly, not estimated.
    Resumen de drawdowns: 23 episodios, caída mediana -22,5%, peor
    caída -84,8% (confirmed as the 1929.09->1932.06 episode, sanity-
    checked against the known Great Depression drawdown), duración
    mediana 14 meses, recuperación mediana 15 meses. Detalle de
    indicadores: Inflación now reads "Por encima de la media, dentro
    del rango histórico habitual", Tipo reads "Por debajo de la media,
    dentro del rango histórico habitual" (4,44% vs media 4,48%, correct
    direction), CAPE's "Muy por encima" unchanged (not in the "near"
    band, function is a no-op there). Full `tests/verify_*.py` suite
    re-run: same single pre-existing failure (`verify_research_engine.py`,
    ordering only), nothing new. `generate_dashboard.py` (operational)
    regenerated separately, unaffected.

------------------------------------------------------------------------

## RE-SHILLER-DASH.4 — Panorama histórico: headline de verdad, no
   frase corrida, y decimales consistentes

Armando, tras ver el resultado de RE-SHILLER-DASH.3, sin rodeos: "¿de
verdad esto te parece bain o mckinsey? El resumen ejecutivo en líneas
con texto seguido, las cifras cada una por su lado, una con dos
decimales, otras con uno... qué poco detalle. Ponte las pilas." Dos
defectos reales, no de gusto:

-   **"Resumen ejecutivo" era una sola frase corrida** encadenando
    cuatro ideas con comas -- no un titular, un párrafo. Sustituido por
    el mismo patrón headline-action/headline-support ya aprobado por
    Armando para "Estado hoy" en el dashboard operativo (RE-DASH.1.11)
    -- reutilizado, no inventado. `build_headline()` (nueva función)
    calcula un título corto (estado de mercado + el indicador más
    anómalo hoy, mismo cálculo de z-score que ya usa el dot y la tabla,
    no un segundo juicio) y una línea de apoyo con las cuatro cifras
    clave sin comas dentro de la frase. Se añade un `.stat-strip` (el
    mismo patrón ya aprobado para "Evidencia histórica" en RE-DASH.1.11)
    con esas cuatro cifras como bloques grandes, cada una con su propio
    dot -- "las cifras cada una por su lado", tal cual lo pidió.
-   **Decimales inconsistentes dentro de la misma tabla**: Inflación
    usaba el default de `_fmt_pct` (1 decimal) y Tipo el de `_fmt_rate`
    (2 decimales), en filas contiguas de "Detalle de indicadores".
    Corregido forzando 2 decimales en Inflación en todo el archivo
    (franja, resumen, notas de gráfica). Hallazgo colateral, no pedido:
    este mismo desajuste (inflación a 1 decimal, tipo a 2) existe hoy
    en la tabla "Datos de mercado" del dashboard OPERATIVO
    (`generate_dashboard.py`) -- confirmado por grep, no corregido ahí
    sin que Armando lo decida, es un archivo distinto.
-   **Hallazgo técnico adicional, no buscado**: las etiquetas del eje Y
    en las gráficas de CAPE/inflación/tipo (escala lineal) usaban
    decimales en formato inglés ("2.5", "7.5") por el formateador por
    defecto de matplotlib -- inconsistente con la coma española usada
    en todo el resto de ambos paneles. Corregido con un
    `FuncFormatter` nuevo (`_es_tick_formatter`), aplicado solo a los
    ejes lineales (`chart_series()`), no al eje logarítmico del precio
    (`chart_price()`), cuyas etiquetas en potencias de 10 no tienen
    punto decimal que convertir.

What this does not authorize:

-   No change to any gate, protocol, model, loader, or the Research
    Engine -- purely presentation-layer fixes to the new panel.

Boundary:

-   One file modified: `generate_shiller_dashboard.py`
    (`DRIVER_LABEL_ES` added; `build_shiller_data()` now also returns
    `driver_key`/`driver_long`; `build_executive_summary()` replaced by
    `build_headline()` + new `build_stat_strip()`; `build_indicator_
    strip()`'s Inflación row forced to 2 decimals; `_es_tick_formatter()`
    added and applied inside `chart_series()`; CSS gains `.headline-
    action`/`.headline-support`/`.stat-strip`/`.stat-value`/`.stat-
    label`, copied from the operational dashboard's own values).
-   No Frozen Core component touched.
-   Verified by direct execution against real data: `outputs/
    shiller_dashboard.html` regenerated and extracted. Resumen
    ejecutivo: "Mercado en máximo histórico, con el CAPE muy por
    encima de su media histórica." / stat-strip "CAPE 41,4 (percentil
    99) · Drawdown 0,0% · Inflación 4,23% · Tipo 10a 4,44%" -- Inflación
    now 2 decimals everywhere (was 4,2% in RE-SHILLER-DASH.3, now
    4,23%, matching Tipo's decimal count). Rate GS10 chart PNG visually
    inspected: y-axis now reads "2,5 / 5 / 7,5 / 10 / 12,5 / 15", comma
    decimals confirmed. Full `tests/verify_*.py` suite re-run: same
    four pre-existing failures, nothing new. `generate_dashboard.py`
    (operational) regenerated separately, unaffected.
-   **RE-SHILLER-DASH.4b (same day, immediate follow-up)**: first
    version of this fix still returned a `headline_subtitle` line
    ("CAPE 41,4 (percentil 99) · Drawdown 0,0% · Inflación 4,23% ·
    Tipo 10a 4,44%") directly above the new stat-strip, which shows the
    exact same four numbers again. Armando: "repites los datos, en
    pequeño y en grande." Correct -- the subtitle was a leftover from
    before the stat-strip existed. `build_headline()` now returns only
    the title string; the subtitle and its `.headline-support` CSS rule
    are removed. Verified: regenerated output's Resumen ejecutivo card
    now shows the headline sentence once, followed directly by the
    stat-strip, no duplicate figures. Full test suite re-run: same
    single pre-existing failure (`verify_research_engine.py`, ordering
    only), nothing new.

------------------------------------------------------------------------

## RE-SHILLER-DASH.3 — Panorama histórico: semáforos y anotación de
   última fecha/valor

Two more rounds of feedback from Armando on the same day: "diseño tipo
bain/mckinsey sobre todo en Indicadores clave y resumen ejecutivo...
mira a ver lo de semáforos o algo parecido"; "añadir fecha y valor de
la última cifra de referencia para ubicarnos en las gráficas."

-   **Semáforos, on a deliberately different color axis than the
    operational dashboard's.** `outputs/dashboard.html`'s `.dot.ok/
    warn/bad` is a value judgment (below suelo IS bad, structurally).
    A "muy por encima" CAPE reading isn't good or bad by itself --
    `context_bar()`'s own docstring in `generate_dashboard.py` already
    says this table is "descriptive context, not a verdict." New
    `_reading_magnitude_color()` encodes distance from historical norm
    instead: near (gray) / notable (ochre) / extreme (red) -- same hex
    values as the operational dashboard's dots for visual family
    consistency, different CSS class (`.mag-dot`, not `.dot`) so the
    two meanings can't be confused by name. Drawdown's dot stays on
    the real ok/warn scale (reuses `build_porque_rows()`'s existing
    "Activa"->warn/"No activa"->ok distinction) since "hay una caída
    activa" is a genuine status, not a magnitude, and doesn't fit the
    near/notable/extreme axis.
-   Indicator strip gets one dot per row. Resumen ejecutivo gets a dot
    and a matching card accent border, both colored by whichever of
    CAPE/inflación/tipos has the largest absolute z-score today --
    computed, not picked by eye (today: CAPE, |z|=3.11, far ahead of
    inflación's 0.33 and tipos' -0.02).
-   **Última fecha/valor on the charts themselves**, not only in the
    caption text below, per "para ubicarnos en las gráficas". New
    `_annotate_latest()` places a small boxed label next to the latest
    point on all four charts. Caption paragraphs also gained an
    explicit "Último dato disponible: {fecha} -- {valor}" line (they
    previously said "Hoy: X" with no date).

What this does not authorize:

-   No change to any gate, protocol, model, loader, or the Research
    Engine -- purely presentation-layer additions to the new panel.

Boundary:

-   One file modified: `generate_shiller_dashboard.py`
    (`_reading_magnitude_color()`, `drawdown_dot_color()`,
    `_annotate_latest()` added; indicator strip and resumen ejecutivo
    gain dots/accent; all four chart functions take a `latest_label`
    and annotate it; new `.dot`/`.mag-dot`/`.card.accent-*` CSS).
-   No Frozen Core component touched.
-   Verified by direct execution against real data: `outputs/
    shiller_dashboard.html` regenerated and extracted. Resumen
    ejecutivo card: `accent-extreme`, dot `extreme` (CAPE is the
    driver, confirmed by its z-score being the largest of the three).
    Indicator strip: Drawdown `dot ok`, CAPE `mag-dot extreme`,
    Inflación `mag-dot near`, Tipo `mag-dot near` -- all match
    already-verified readings. Chart annotations show "2026-07: 41,4"
    (CAPE) and "2026-07: 7504" (precio real), both visually inspected
    on the rendered PNGs and legible against the plotted line. Full
    `tests/verify_*.py` suite re-run: same four pre-existing failures,
    nothing new.

------------------------------------------------------------------------

## RE-SHILLER-DASH.2 — Panorama histórico: executive layer, and a real
   nominal-vs-real price finding

Armando's structured review of v1: "lo veo más como un cuaderno de
gráficas históricas que como un dashboard ejecutivo... le falta una
capa superior de lectura." Six concrete changes requested, plus one
real technical finding surfaced while implementing change #5:

-   **Resumen ejecutivo**: one sentence at the top, built from the
    same `drawdown_context()`/`_context_words()` readings the
    indicator strip shows below it (imported from
    `generate_dashboard.py`, not reimplemented) -- can't disagree with
    the table under it because it's the same computation, not a second
    independent judgment in prose.
-   **Franja de indicadores**: a 4-row table (Drawdown, CAPE,
    Inflación, Tipo a 10 años) before the charts, per Armando's own
    mockup. His mockup read inflación as "Por encima" by eyeballing
    4,2% vs. 2,3% -- checked against the same z-score bands the
    operative dashboard already uses (confirmed by Armando for
    RE-DASH.1.4) and flagged the disagreement rather than silently
    picking one: inflación's z-score is 0.33 (std=5,8pp, so +1,9pp is
    less than half a standard deviation) -- "Cerca de la media", not
    "Por encima". Used the verified z-score reading; told Armando the
    discrepancy and why, left the choice open if he prefers the
    eyeballed version instead.
-   **Percentil de CAPE**: computed directly (share of historical
    months with a lower CAPE than today's) -- 99,0. Armando's own
    estimate ("percentil histórico 98/99 aprox") checked out.
-   **Media de CAPE a 10 años**: computed directly -- 32,36 -> "32,4",
    matching the figure Armando already had. New `CAPE_RECENT_YEARS =
    10` constant, deliberately not reusing `RECENT_WINDOW_YEARS = 50`
    from `generate_dashboard.py` -- different window, different
    purpose, not forced into one shared constant.
-   **Precio real, no nominal**: Armando's request to clarify the
    price chart's label ("¿es Price o Price.1?") led to checking the
    actual column, not guessing -- and it was neither. `chart_price()`
    was plotting `df["P"]`, which the Shiller workbook's own header
    rows identify as "S&P Comp." (raw nominal price, not adjusted for
    inflation). `df["Price"]` is the real (inflation-adjusted, no
    dividends) series. Switched the chart to `"Price"` and corrected
    the label to "S&P 500 -- precio real, sin dividendos". Verified
    computationally before concluding anything: at the latest row `P`
    and `Price` are equal (expected -- "real" terms are anchored to
    today's dollars, so nominal=real for the most recent observation
    by construction); at row 0 (1871) `P`=4.44 vs `Price`=119.94,
    confirming the ~27x gap is cumulative inflation, not an error.
    Explicitly scoped: this changes only which line this one chart
    draws. `drawdown_engine.py`'s own episode detection (peak/bottom/
    recovery dates, % drawdown) still runs on nominal `P`, unchanged,
    out of scope -- flagged to Armando as a real fact about the core
    engine's existing behavior, not something this iteration touches
    or judges.
-   **"Qué NO dice este panel"**: added as its own block in a new
    "Nota metodológica" card at the end, near-verbatim to Armando's
    wording.
-   Page reordered to Armando's proposed structure: resumen ejecutivo
    -> franja de indicadores -> precio -> CAPE -> inflación -> tipos
    -> nota metodológica.
-   `drawdown_context()` extracted from `generate_dashboard.py`'s
    inline block into a shared function both scripts import -- the new
    dashboard needed the identical "plain fact, not z-score" drawdown
    reading RE-DASH.1.4 already established (a market at 0% drawdown
    would misleadingly read as "cerca de la media" under z-score
    banding), and duplicating that logic in a second file risked the
    two drifting apart.

What this does not authorize:

-   No change to `drawdown_engine.py`, episode detection, or any
    gate/protocol file. The nominal-vs-real finding is reported, not
    acted on -- switching the core engine's own price basis would be a
    separate, much larger decision requiring Armando's explicit
    sign-off, not a side effect of a chart-label fix.

Boundary:

-   Two files modified: `generate_shiller_dashboard.py` (executive
    summary, indicator strip, CAPE percentile/10-year mean, real-price
    chart, restructured page, methodology card) and
    `generate_dashboard.py` (`drawdown_context()` extracted as a
    shared function; `render_html()`'s inline block replaced with a
    call to it -- output unchanged, verified below).
-   No Frozen Core component touched.
-   Verified by direct execution against real data: `python3
    generate_dashboard.py` re-run after the `drawdown_context()`
    extraction -- `outputs/dashboard.html` still contains "Mercado en
    máximo histórico" exactly as before. `python3
    generate_shiller_dashboard.py` re-run -- indicator strip shows
    Drawdown 0,0%/--/"Mercado en máximo histórico", CAPE 41,4/17,8/
    "Muy por encima", Inflación 4,2%/2,3%/"Cerca de la media", Tipo
    4,44%/4,48%/"Cerca de la media"; CAPE note shows percentil 99,
    media 10 años 32,4; resumen ejecutivo sentence matches the same
    four readings. Price chart's real-price line rendered and visually
    inspected -- shows the 1966-1982 real bear market and 1982-2000
    real bull market clearly, a materially different (and more honest)
    shape than the nominal version. Full `tests/verify_*.py` suite
    re-run: same four pre-existing failures, nothing new.

------------------------------------------------------------------------

## RE-SHILLER-DASH.1 — Panorama histórico (Shiller): new static-chart
   dashboard, first version

Armando, after RE-DASH.1.21 landed: "estaba pensando... que
construyamos un dashboard parecido con la información de shiller, con
gráficas e info relevante, ¿tiene sentido?" Answered directly before
building, not by default agreement: yes, for a stated reason --
distinct purpose from `outputs/dashboard.html` (decision-support
snapshot for today vs. historical/diagnostic exploration), and it lets
Armando visually verify what `run_drawdown_engine()`'s episode
detection is doing against the real historical series instead of
trusting it from tables alone. Also named the one real trade-off
before starting: this sits outside the project's own stated next
milestone (Similarity Engine v2, per `PROJECT_STATE.md`) -- not a
blocker, a separate file touching none of the same code, but a
conscious sequencing choice, not a silent one.

Two architecture questions asked directly rather than inferred (both
genuine forks, not details):

-   Static charts (matplotlib -> PNG, no `<script>`) vs. interactive
    (a JS charting library). Armando chose static -- preserves the
    zero-`<script>`, read-only rule `outputs/dashboard.html` has kept
    since RE-DASH.1.4; an interactive library would have been an
    architecture change, not a detail, so not decided silently.
-   New separate file/output vs. a new section inside the existing
    operational dashboard. Armando chose separate -- different
    audience/purpose, keeps the decision-support dashboard from
    absorbing scope that isn't its job.

New `generate_shiller_dashboard.py` -> `outputs/shiller_dashboard.html`:

-   Reuses `run_drawdown_engine()` directly -- same `Dataset`, same
    `Episode` objects, same computed columns (`CAPE`,
    `InflationRate1Y`, `Rate GS10`, `Drawdown`) the Research Engine and
    `outputs/dashboard.html` already use. No new loader, no
    independently recomputed figures.
-   Four charts: S&P price (log scale, v1 used `"P"` -- corrected to
    real price in RE-SHILLER-DASH.2, see below), CAPE, inflación
    interanual, tipo a 10 años -- chosen because they are exactly the
    three "regime dimensions" `RegimeComparabilityGate` already
    evaluates plus the price/drawdown anchor, not an arbitrary
    selection.
-   Each historical episode `run_drawdown_engine()` detects is shaded
    on every chart (red = fase de caída, ochre = fase de recuperación)
    -- the same `Episode` objects the Research Engine matches against,
    not a second detector.
-   Reuses `generate_dashboard.py`'s existing Spanish-format helpers
    (`_esc`, `_fmt_amount`, `_fmt_num`, `_fmt_pct`, `_fmt_rate`,
    `_fmt_shiller_date`) by direct import rather than reimplementing
    number formatting a second time.
-   Same color language as the operational dashboard (`.dot.ok/.warn/
    .bad` reds/ochres/greens) reused for the shading, not a second
    independent palette.

What this does not authorize:

-   No change to any gate, protocol, model, loader, or the Research
    Engine itself -- purely a new, read-only presentation layer over
    data those already produce.

Boundary:

-   One new file: `generate_shiller_dashboard.py` ->
    `outputs/shiller_dashboard.html`. No existing file modified in
    this entry (the `drawdown_context()` extraction is
    RE-SHILLER-DASH.2, not this one).
-   No Frozen Core component touched.
-   Verified by direct execution against real data: `outputs/
    shiller_dashboard.html` generated, all four PNG charts extracted
    and visually inspected (episodes correctly shaded at 1929, 2000,
    2008; today marked at the latest point on each series). Full
    `tests/verify_*.py` suite re-run after generating: same four
    pre-existing failures, nothing new -- confirms importing from
    `generate_dashboard.py` introduced no side effects.

------------------------------------------------------------------------

## RE-DASH.1.21 — Dashboard: liquidity moves from a table cell to a
   full-width card per patrimonio

Armando's own detailed design critique, unprompted by a screenshot
this time -- a written proposal after six rounds (RE-DASH.1.13-1.20)
polishing the liquidity indicator inside an 84px table cell: "la idea
de barra es buena, pero tal como está ahora queda demasiado pequeña y
demasiado escondida dentro de una tabla... el suelo y techo no se ven
directamente, solo aparecen en tooltip. Eso obliga a interpretar." He
proposed one full-width card per patrimonio (bullet-chart style):
visible suelo/techo text, a full-width three-zone bar, the
exceso/déficit caption, and a one-line diagnosis sentence.

Agreed with the core critique before building, not silently -- two
points it corrected: (1) the suelo/techo tooltip-only display
(RE-DASH.1.14) was always in tension with this dashboard's own rule
everywhere else (`<details>`, no hidden state, nothing requiring
interaction to read) -- introduced as an anti-clutter compromise that
didn't hold for the block's single most load-bearing number; (2) six
rounds failing to make one 84px cell work is itself a signal the
container was wrong, not that a seventh polish pass was needed. This
reverses my own RE-DASH.1.14 decision to decline a card layout (then
reasoned as "diverges from the row-based pattern the rest of the card
uses") -- his argument here (suelo/techo must be visible, not just
implied) outweighs that consistency concern.

-   New `liquidity_card()` replaces `liquidity_bar()` -- reuses, not
    reimplements: `liquidity_status()`, `liquidity_gap()`, the same
    `LIQUIDITY_BAR_CLAMP_MIN/MAX`-derived zone/tick math from
    RE-DASH.1.14/1.16, and the same boundary-labeled caption from
    RE-DASH.1.15. Only the container changed -- full-width instead of
    84px, suelo/techo now visible as text at each end of the bar (the
    `title` tooltip is kept too, as a redundant convenience, not the
    only way to see it).
-   New `liquidity_diagnosis()`: one-line reading per Armando's spec,
    keyed off the same `status_color` `liquidity_status()` already
    returns -- not a fourth independent judgment about the same three
    states.
-   Declined, with reasoning given to Armando, the optional summary
    table he offered ("si quieres conservar tabla... pero visualmente
    mandaría la barra") -- every figure in it (actual/suelo/techo/
    diferencia) is already visible on the card itself, so adding it
    back as a table would be pure redundancy. Reversible if he still
    wants it.
-   "Postura y permisos" stays a table -- categorical status data
    (postura/Human Approval/Dry Powder), not a range-against-threshold
    metric, so a bullet-chart card doesn't fit it. Flagged to Armando,
    not silently decided, that this leaves two visual formats inside
    one card (Liquidez as cards, Postura as a table): judged
    appropriate given the different data shapes, not an inconsistency
    to fix.
-   RE-DASH.1.17's `.patrimonio-table` shared-width class existed only
    to keep Liquidez's and Postura's table columns lined up with each
    other -- with Liquidez no longer a table, it has nothing left to
    synchronize against. Removed from Postura (reverts to
    content-sized columns) and its now-orphaned CSS deleted, along
    with the RE-DASH.1.15/1.16 `.ctx-bar.liq` variant rules
    `liquidity_bar()` used (function removed, rules removed with it --
    `context_bar()`'s own `.ctx-bar`/`.ctx-dot`/`.ctx-tick` at 52px are
    untouched).

What this does not authorize:

-   No change to `liquidity_status()`, `liquidity_gap()`, or any gate/
    protocol/loader file -- this is a container change around numbers
    those functions already compute.

Boundary:

-   One file modified: `generate_dashboard.py` (`liquidity_bar()`
    removed; new `liquidity_card()`/`liquidity_diagnosis()`; Liquidez
    section of `patrimonio_body` now cards instead of a table; Postura
    table reverts to `table-layout:auto`; new `.liq-card` CSS family;
    orphaned `.patrimonio-table`/`.ctx-bar.liq` CSS removed).
-   No Frozen Core component touched.
-   Verified by direct execution against real data: `outputs/
    dashboard.html` regenerated and extracted. AMS: card shows
    "167.273,00 €" actual, "100.000,00 €"/"150.000,00 €" suelo/techo
    visible as text, marker at 98.0% (inset, warn/ámbar), caption
    "+17.273,00 € sobre techo", diagnosis "Liquidez por encima del
    techo: exceso disponible, no restricción." AML: "199.375,00 €"
    actual, "250.000,00 €"/"300.000,00 €" suelo/techo, marker at 2.0%
    (bad/rojo), caption "-50.625,00 € bajo suelo", diagnosis "Liquidez
    por debajo del suelo: limita la capacidad personal." -- all match
    already-verified real figures, nothing recalculated. Rendered as a
    live visual preview from the real generated HTML/CSS; Armando
    confirmed ("así está ok"). Full `tests/verify_*.py` suite re-run:
    same four pre-existing failures, nothing new. Grepped for
    remaining `liquidity_bar(` and `.patrimonio-table` references:
    none outside this changelog's own prose.

------------------------------------------------------------------------

## RE-DASH.1.20 — Dashboard: one left-aligned convention for every
   value column

Armando's screenshot, cropped to the right edge of the page: "Liquidez
Disponible" (left-aligned since RE-DASH.1.18) sitting above "Human
Approval" (already left) sitting above "Valor" in Datos de mercado
(still right-aligned, `td.num`) -- "podrías alinear estas columnas?"
Two directions were both technically valid (right-align everything
back per the original "financial report" convention, or left-align
everything to match 1.18), and they conflict, so this was asked
directly rather than inferred: "¿Qué alineación quieres para las
cifras?" Armando's answer: "Valor, Human Approval y Liquidez
disponible deben estar alineadas y justificadas a la izqda."

-   Dropped `class="num"` from "Valor"'s header and its five data
    cells (Fecha de datos, Caída actual, CAPE, Inflación, Tipo de
    interés) in the Datos de mercado table -- the one remaining
    right-aligned value column in the dashboard. Every value column
    now shares one left-aligned convention.
-   `td.num`/`th.num`'s CSS rule is left in place, unused for now, not
    deleted -- a general-purpose alignment utility, not something tied
    to this specific table; removing it would be a separate,
    unrequested cleanup.

What this does not authorize:

-   No change to any figure, formatter, or gate -- `_fmt_pct()`,
    `_fmt_num()`, `_fmt_rate()` outputs are unchanged, only their
    cells' text-align.

Boundary:

-   One file modified: `generate_dashboard.py` (`class="num"` removed
    from six cells in the Datos de mercado table).
-   No Frozen Core component touched.
-   Verified by direct execution against real data: `outputs/
    dashboard.html` regenerated, extracted, and rendered as a live
    preview from the real HTML/CSS before reporting done. Full
    `tests/verify_*.py` suite re-run: same four pre-existing failures,
    nothing new.

------------------------------------------------------------------------

## RE-DASH.1.19 — Dashboard: plain-language "not comparable" alert

Armando saw "Régimen no comparable (CAPE)" in Alertas and asked what
it meant, then "no acabo de entenderlo, ¿cuál es ese rango del que
hablas?". Answered with the real numbers first (not guessed): today's
CAPE is 41.37; the 10 historical episodes matched as comparable range
from 14.82 (1990.06) to 33.53 (1998.07) -- no matched episode reaches
anywhere near today's level. Armando then asked for the alert itself
to say that plainly: "cambialo... por algo mas comprensible... 'no hay
episodios comparables con un CAPE tan alto'".

-   New `REGIME_DIMENSION_ALERT_ES` mapping (noun phrase + alto-form +
    bajo-form per dimension, since Spanish gender/article differ: "un
    CAPE"/alto/bajo, "una inflación"/alta/baja, "un tipo de
    interés"/alto/bajo -- a single shared adjective across all three
    would have been grammatically wrong for inflación).
-   The alert now reuses `_regime_direction()` -- the exact same
    today-vs-matched-range comparison `RegimeComparabilityGate`/
    `_dimension_covered()` already makes and "Por qué no se actúa"
    already renders -- not a second, independently-computed judgment.
    Only the wording is new.

What this does not authorize:

-   No change to `RegimeComparabilityGate`, `_dimension_covered()`, or
    any matching/evidence logic -- this changes only how an existing,
    already-computed direction is worded in the Alertas list.

Boundary:

-   One file modified: `generate_dashboard.py` (new
    `REGIME_DIMENSION_ALERT_ES`; `build_alerts()`'s "not comparable"
    branch rewritten to use it).
-   No Frozen Core component touched.
-   Verified by direct execution against real data: today's cape
    41.368..., matched episodes' cape range [14.818..., 33.532...]
    (10 episodes, one with a NaN cape context excluded) -- confirmed
    via direct script execution before writing any wording, not
    assumed. `outputs/dashboard.html` regenerated: Alertas now reads
    "No hay episodios comparables con un CAPE tan alto." Full
    `tests/verify_*.py` suite re-run: same four pre-existing failures,
    nothing new.

------------------------------------------------------------------------

## RE-DASH.1.18 — Dashboard: align "Liquidez disponible" with "Human
   Approval"

Armando, after RE-DASH.1.17: "alinea liquidez disponible con human
approval y posicios vs con dry powder."

-   Column 3 ("Liquidez disponible") was right-aligned (`td.num`, for
    tabular-nums digit scanning) while column 3 of the table below
    ("Human Approval") is plain left-aligned text. With both tables
    now sharing identical fixed column widths (RE-DASH.1.17), that
    alignment mismatch became visible as the two tables' column 3
    starting at different x positions. Dropped the right-alignment so
    both read from the same left edge.
-   Column 4 ("Posición vs. suelo/techo" / "Dry Powder") was checked,
    not assumed: both were already left-aligned by default (neither
    carries `.num`), so no change was needed there -- confirmed by
    extracting the real generated HTML before touching anything.

What this does not authorize:

-   No change to any figure -- `_fmt_amount()`'s output is unchanged,
    only its cell's text-align.

Boundary:

-   One file modified: `generate_dashboard.py` (`class="num"` removed
    from the "Liquidez disponible" header and data cells).
-   No Frozen Core component touched.
-   Verified by direct execution against real data: `outputs/
    dashboard.html` regenerated, extracted, and rendered as a live
    preview from the real HTML/CSS before reporting done. Full
    `tests/verify_*.py` suite re-run: same four pre-existing failures,
    nothing new.

------------------------------------------------------------------------

## RE-DASH.1.17 — Dashboard: shared column widths across the two
   "Estado por patrimonio" tables

Armando's screenshot of RE-DASH.1.16's result: "Puedes alinear
'Estado' y 'postura'? Puedes equilibrar ese triángulo entre
liquidez/posición y Dry Powder y Human Approval?"

-   "Liquidez" and "Postura y permisos" are two independent `<table>`
    elements, each sized by `table-layout:auto` from its own content
    only. A wide element in one (the liquidity bar) and a short one in
    the other (Dry Powder's text) pulled each table's own column 4 to
    a different width, staggering every column boundary between the
    two tables -- the "triángulo" Armando named. No amount of content
    changes inside either table can fix that; only forcing both tables
    onto one shared width scheme can.
-   New `.patrimonio-table` class: `table-layout:fixed` with explicit,
    identical `nth-child` percentage widths (13/21/28/38%) applied to
    both tables, so column 1 (Patrimonio) and column 2 (Estado/
    Postura) land at the same x in both, and columns 3-4 split the
    remaining width the same way in both instead of each table
    expanding its own odd column to fill leftover space.

What this does not authorize:

-   No change to any gate, protocol, model, loader, or figure -- pure
    column-width CSS on two already-existing tables.

Boundary:

-   One file modified: `generate_dashboard.py` (new
    `.patrimonio-table` CSS class; applied to both tables in "Estado
    por patrimonio").
-   No Frozen Core component touched.
-   Verified by direct execution against real data: `outputs/
    dashboard.html` regenerated, extracted, and rendered as a live
    preview from the real HTML/CSS. Full `tests/verify_*.py` suite
    re-run: same four pre-existing failures, nothing new.

------------------------------------------------------------------------

## RE-DASH.1.16 — Dashboard: liquidity bar marker inset and boundary
   ticks

Armando, after seeing the RE-DASH.1.15 fix rendered: "me gusta el
contenido pero el diseño que me aparece es claramente mejorable aún."
Two real, specific legibility problems, not a vague "make it prettier"
ask:

-   The marker's `left` position (0%/100% at the range extremes) plus
    its own `translateX(-50%)` centers the dot exactly on the track's
    edge, so half its own width hung off the track into blank cell
    space -- looked disconnected from its own bar, especially at the
    two most common alert-worthy positions (below suelo / above
    techo). Fixed by insetting the *visual* position to 6%-94%
    (`dot_visual_pct`), a display-only clamp that changes nothing
    about `dot_pct`'s meaning for zone math.
-   The three pale zone tints (deliberately dulled, reused from
    `.pill.bad/.ok/.warn`, not new colors -- per Armando's standing
    "no debe leer como oportunidad" instruction on this color
    language) were too close in lightness to register as distinct
    zones on a thin 4px line with no border -- read as one pale smudge
    in his screenshot. Fixed without raising saturation (which would
    have fought that same standing instruction): added tick marks at
    the suelo/techo boundaries (reusing the existing `.ctx-tick`
    pattern already used for context_bar()'s mean marker) so the
    boundary is visible independent of color contrast, thickened the
    track 4px->6px, and added a hairline border so it has a visible
    edge against the white table background.
-   All of this scoped to a new `.ctx-bar.liq` / `.ctx-dot`-under-
    `.liq` variant, so `context_bar()`'s already-approved 52px/4px
    market-data rows are untouched.

What this does not authorize:

-   No change to `liquidity_status()`, `liquidity_gap()`, or the
    RE-DASH.1.15 coordinate fix -- purely a legibility pass on top of
    already-correct positions.

Boundary:

-   One file modified: `generate_dashboard.py` (`dot_visual_pct`
    inset in `liquidity_bar()`; two new `<span class="ctx-tick">`
    elements at the zone boundaries; `.ctx-bar.liq` gains height/
    border, `.ctx-bar.liq .ctx-dot`/`.ctx-tick` gain matching
    top-offsets).
-   No Frozen Core component touched.
-   Verified by direct execution against real data: `outputs/
    dashboard.html` regenerated. AMS's dot at 94.0% (inset from the
    raw 100%), AML's at 6.0% (inset from 0%), both still inside their
    respective zone. Rendered as a live visual preview from the real
    generated HTML/CSS before reporting done. Full `tests/verify_*.py`
    suite re-run: same four pre-existing failures, nothing new.

------------------------------------------------------------------------

## RE-DASH.1.15 — Dashboard: liquidity bar marker/coordinate bug and
   ambiguous figure label, both from a real screenshot

Armando's screenshot of the shipped RE-DASH.1.14 bar: "esto es un
desastre a nivel de diseño... la cifra que aparece no es posición vs
suelo/techo, sino posición vs techo." Two separate real defects, not
one:

-   **Marker/zone coordinate mismatch (the "desastre").** RE-DASH.1.14's
    verification claimed the marker sat "at 115% (ámbar zone)" -- true
    of the underlying number, false of what actually rendered. The
    zone gradient converts the clamped logical percent (-15 to 115,
    percent of the suelo-techo span) into a 0-100% display scale
    before painting (`floor_pct`/`ceiling_pct`). The marker's CSS
    `left` skipped that conversion and used the clamped logical
    percent directly -- so `left:115%` placed the dot 15% of the bar's
    own width past its right edge, and `left:-15%` placed it 15% past
    the left edge, both floating detached from the track exactly as
    Armando's screenshot showed. This is a verification gap on my
    part: RE-DASH.1.14 checked that the clamped number was correct,
    not that it was correct *on the same coordinate system as the
    zones it needed to sit inside*. Fixed by routing the marker
    through the identical span conversion the zones already use --
    one coordinate system, not two silently different ones.
-   **Ambiguous figure.** `liquidity_gap()` always returns a gap
    against a single boundary (suelo or techo, whichever applies),
    never both at once -- but the label showed only a bare signed
    amount under a column header reading "Posición vs. suelo/techo",
    which read as if the number compared against both. Fixed at the
    label, not the header: the boundary is now named explicitly
    ("+17.273,00 € sobre techo" / "-50.625,00 € bajo suelo" / "+X €
    sobre suelo" when within range), so the figure is self-explanatory
    regardless of what the column header says.
-   Also widened `.ctx-bar.liq` from 52px to 84px (a variant class, not
    a change to `context_bar()`'s existing 52px track) -- at 52px the
    two edge zones were only ~6px wide, functionally invisible.

What this does not authorize:

-   No change to `liquidity_status()` or `liquidity_gap()` -- both
    remain the single source of truth for the underlying numbers; this
    fixes only how the marker's position and the gap figure are
    rendered.

Boundary:

-   One file modified: `generate_dashboard.py` (`liquidity_bar()`
    marker position now converted through the same span as the zone
    boundaries; explicit boundary wording added to the label; new
    `.ctx-bar.liq` CSS variant at 84px).
-   No Frozen Core component touched.
-   Verified by direct execution against real data: `outputs/
    dashboard.html` regenerated. Recomputed AMS (167.273,00 €, floor
    100.000, ceiling 150.000) -> marker `left:100.0%` (right edge,
    inside the ámbar zone which starts at 88.5%), label "+17.273,00 €
    sobre techo"; AML (199.375,00 €, floor 250.000, ceiling 300.000)
    -> marker `left:0.0%` (left edge, inside the rojo zone which ends
    at 11.5%), label "-50.625,00 € bajo suelo". Both markers now sit
    visibly on the track, inside the zone their status color implies.
    Rendered as a live visual preview from the real generated HTML and
    CSS (not a reinterpretation) before reporting done. Full
    `tests/verify_*.py` suite re-run: same four pre-existing failures,
    nothing new.

------------------------------------------------------------------------

## RE-DASH.1.13 — Dashboard: one-line headers, liquidity as a visual gauge

Armando sent a real screenshot of the shipped file: "Serie completa
(1871-2026)" and "Últimos 50 años (1976-2026)" were wrapping to two
lines in his actual browser, not just in a narrow preview -- confirmed
before touching anything, not assumed. Also: "me gusta mucho el
indicador... en datos de mercado, ¿podrías hacer algo similar con
liquidez?"

-   Table headers (`<th>`) are always short, single-line labels by
    design (per RE-DASH.1.11's own comment) -- so `white-space:nowrap`
    now enforces that rather than hoping column width happens to be
    enough. The uppercase+letter-spacing treatment RE-DASH.1.11 added
    was exactly what pushed "Serie completa (1871-2026)" past its
    column and caused the real wrap.
-   Applied the same `nowrap` discipline to `.ctx` (the context-bar
    row) so a bar+label pair can't split across two lines either.
-   New `liquidity_bar()`, the same gauge pattern as `context_bar()`:
    a marker on a track. Replaces the separate "Rango de liquidez
    (suelo/techo)" text column and "Exceso/Déficit" number column in
    "Estado por patrimonio" with one visual unit -- track spans
    suelo-to-techo, marker shows today's position (clamped to
    -15%/115% so an out-of-range value still shows near the edge
    instead of vanishing), exact signed € exceso/déficit kept as the
    bar's caption (same `liquidity_gap()` figure already used, not
    recalculated). Unlike `context_bar()`'s track (deliberately no
    color judgment), this track's endpoints ARE the safe zone by
    construction, so the marker reuses the same status_color
    `liquidity_status()` already returned -- reinforcing the Estado
    pill, not a second independent judgment; no new color language.
-   The absolute suelo/techo € figures are not shown as literal
    numbers in the main view anymore -- relocated, not dropped, to a
    new row in Detalle técnico's per-patrimonio block, so anyone who
    wants the raw figures can still open it.

What this does not authorize:

-   No change to any gate, protocol, model or loader file, and no
    change to any figure -- `liquidity_gap()`/`liquidity_status()`
    remain the single source of truth for the underlying numbers, the
    bar only visualizes what they already return.

Boundary:

-   One file modified: `generate_dashboard.py` (new
    `liquidity_bar()`; `th`/`.ctx` gain `white-space:nowrap`;
    Liquidez table restructured to 4 columns; suelo/techo moved into
    `technical_patrimonios`).
-   No Frozen Core component touched.
-   Verified by direct execution against real data:
    `outputs/dashboard.html` regenerated. Spot-checked: AMS's marker
    at 115% (clamped, ámbar, above techo) and AML's at -15% (clamped,
    rojo, below suelo) match the real liquidity figures and the
    already-verified exceso/déficit amounts (+17.273,00 €/-50.625,00 €).
    Market table headers no longer wrap. Full `tests/verify_*.py`
    suite re-run: same four pre-existing failures, nothing new.

------------------------------------------------------------------------

## RE-DASH.1.12 — Dashboard: column alignment and typography coherence

Armando's screenshot of "Estado por patrimonio" plus a direct
critique: "necesito que seas coherente con la tipografía y tamaños de
letra... estado de liquidez alineado a la izquierda con postura...
la parte de alertas parece tener otra tipografía y tamaño distinto."

-   "Estado" moved from the last column of the Liquidez table to
    right after "Patrimonio" -- the same position "Postura" already
    occupies in the table below. The two pill columns now share the
    same x-position when scanning down the card, instead of sitting
    under unrelated headers at very different offsets.
-   Diagnosed the typography complaint by checking, not guessing: the
    CSS had no explicit `font-size` on `body`. Every other component
    (tables, pills, notes, headline) had its own explicit rem-based
    size (14-15px), but anything without one -- the `<ul><li>` in
    Alertas, and the bare `<p><strong>` sub-section labels ("Liquidez",
    "Postura y permisos", "Otros hallazgos") -- fell back to the
    browser default (16px), reading as a second, larger typeface.
    Fixed at the source: `body { font-size:0.88rem }`, plus explicit
    `.alerts` styling (no default UA list markers/indent, matching
    row rhythm) and a new `.subhead` class for the sub-section labels
    instead of bare `<p><strong>`.

What this does not authorize:

-   No change to any gate, protocol, model or loader file, and no
    change to any figure or the underlying data-collection logic.

Boundary:

-   One file modified: `generate_dashboard.py` (Liquidez table column
    order; `body` gains an explicit `font-size`; `.alerts`/`.subhead`
    classes added and applied).
-   No Frozen Core component touched.
-   Verified by direct execution against real data:
    `outputs/dashboard.html` regenerated. Spot-checked: Estado and
    Postura pill columns land at the same position; Alertas list items
    render at the same size as table text. Full `tests/verify_*.py`
    suite re-run: same four pre-existing failures, nothing new.

------------------------------------------------------------------------

## RE-DASH.1.11 — Dashboard: McKinsey/Bain-style visual redesign

Armando: "quiero que trabajes un diseño tipo consultoría Bain o
McKinsey... mantén lo que consideres que ya encaja y modifica o
elimina todo diseño que se salga de sus directrices." Explicit
creative authority, bounded by a well-known reference. Reviewed the
full CSS/HTML against consulting-report conventions (numbers
right-aligned for scanability, muted small-caps table headers, sharp
corners over rounded UI chrome, a single dominant headline message,
headline metrics as tiles rather than a cramped list) and changed only
what didn't fit -- the ok/warn/bad/neutral status-color system, the
pill/dot vocabulary, the card structure and all data/gate logic were
kept unchanged, per Armando's own instruction to preserve what already
fits.

Changes:

-   Numeric table columns (Liquidez disponible, Rango de liquidez,
    Exceso/Déficit, Valor de mercado) right-aligned with
    `font-variant-numeric:tabular-nums` -- text stayed left-aligned.
    New `.num` utility class, applied to both `<td>` and matching
    `<th>`.
-   Table headers (`<th>`) restyled small, gray, uppercase,
    letter-spaced -- muted relative to the data, not competing with
    it. Not applied to `.pill` values: several pill values are full
    sentences ("Muy alto frente al histórico comparable"), and
    uppercase hurts readability at that length, unlike short column
    labels.
-   Card and pill corner radius reduced (8px/10px -> 2-3px) -- reads
    as a printed report rather than rounded app chrome.
-   "Estado hoy" card gets a left-border accent in the same
    ok/warn/bad/neutral color already used for dots and pills -- one
    status language, not a second one. Mixed-posture case (AMS/AML
    diverge) gets a neutral accent, not a guess at which posture
    "wins" (RE-043.1).
-   Evidencia histórica's four scalar indicators moved from a cramped
    two-column `.kv` table to a horizontal `.stat-strip` of number/
    label tiles -- the pattern for a small set of headline numbers is
    tiles, not a list to "read as records".
-   The "Qué mira este bloque" methodology paragraph moved below the
    indicators as a `.note`, per Armando's explicit instruction
    (indicators first, explanation as a de-emphasized caption after).

Armando's review after seeing the rendered result (five reasons it
was the right kind of change, four things to check before closing):
confirmed as evidence-based, not a rubber stamp --

1.  Amber for "Conservar" could read as "atención / oportunidad,
    casi verde" rather than "prudente/limitado". Fixed: dulled the
    warn color from a bright gold (`#c98a00`/`#fbe8c6`) to a duller
    ochre-brown (`#96650f`/`#f0e6d3`) across dot, pill and card accent
    together -- one color change, not three drifting variants.
2.  A large "10,2%" in the stat strip must not read as a
    recommendation. Fixed: replaced the caveat sentence with Armando's
    own wording ("Esta evidencia no autoriza despliegue por sí sola: la
    validez predictiva sigue no demostrada") and gave it a new
    `.caveat` style distinct from `.note` -- tinted background, left
    rule in the same warn ochre, more visual weight than a footnote --
    so it holds its own next to the large numbers instead of being
    easy to skip.
3.  The status accent border must not be the only signal; large text
    should remain the primary carrier, color only support. Checked,
    not changed: the headline text ("NO ACTUAR" etc.) was already the
    dominant visual element before this round and remains so -- the
    accent border is additive, not a replacement. Flagged to Armando
    as an inference, not silently assumed: if he actually wanted the
    headline reworded to a posture-label format ("Postura SOP hoy:
    Conservar") rather than the existing action-command wording, that
    is a distinct, one-line follow-up, not done here.
4.  The technical block must not surface `not_demonstrated`,
    `Price.1`, `return_count` etc. near the top. Checked, not changed:
    `Detalle técnico` was already the last card in `render_html()`'s
    output order and already collapsed by default (`<details>`, per
    RE-DASH.1's original design) -- confirmed via direct index
    comparison in the rendered HTML, not assumed from memory of the
    code.

What this does not authorize:

-   No change to any gate, protocol, model or loader file. No change
    to `build_dashboard_data()` or any figure shown -- purely
    presentation-layer.
-   Does not reopen the ok/warn/bad/neutral status vocabulary itself,
    the pill/dot pattern, or the card-per-block structure -- Armando's
    instruction was to keep what fits, and these were judged to fit.

Boundary:

-   One file modified: `generate_dashboard.py` (CSS block; `_card()`
    gains an optional `accent` parameter; `.num`/`.caveat` classes
    added and applied; Evidencia histórica body restructured).
-   No Frozen Core component touched. No gate, protocol, model or
    loader file touched.
-   Verified by direct execution against real data:
    `outputs/dashboard.html` regenerated twice (initial redesign, then
    the four-point revision). Spot-checked: old warn hex values
    (`#c98a00`, `#fbe8c6`, `#8a5a00`) absent from the output; new
    caveat paragraph present with Armando's exact wording; `Detalle
    técnico` confirmed last in document order and inside a collapsed
    `<details>`. Full `tests/verify_*.py` suite re-run both times:
    same four pre-existing failures, nothing new.

------------------------------------------------------------------------

## RE-DASH.1.10 — Dashboard: abandons launchd, one-click regeneration instead

RE-DASH.1.9's fix did not work either. Diagnosed with Armando's help,
step by step, before touching any file again:

-   Interactive test (`zsh "<path>/regenerate_dashboard.sh"` run
    directly in Terminal): succeeded -- `logs/dashboard_regen.log`
    got a real new entry, `outputs/dashboard.html` regenerated. This
    proves the script, the file, and its permissions are all fine.
-   `brctl download "<path>/regenerate_dashboard.sh"` (forces full
    iCloud materialization) followed by unload/reload of the launchd
    job: failed again, identical error
    (`zsh: can't open input file: ...`), twice. This rules out the
    iCloud-placeholder-not-downloaded theory RE-DASH.1.9 implicitly
    relied on.

Conclusion, now evidence-based rather than guessed: the failure is
specific to *launchd's background invocation* of a file inside iCloud
Drive (`~/Library/Mobile Documents/com~apple~CloudDocs/`), most likely
a macOS privacy/sandboxing restriction on background processes -- not
a quoting bug (RE-DASH.1.8's theory), not a materialization bug
(RE-DASH.1.9's implicit theory), and not fixable by rewriting the
script or the plist again. Two attempts already failed on two
different, specific theories; a third blind attempt was not proposed
-- offered the choice to Armando instead (deeper TCC diagnostics vs.
abandon background automation vs. try cron instead of launchd).
Armando chose to abandon the background trigger.

Replaced with the simplest mechanism proven to actually work: a
double-clickable `Actualizar Dashboard.command` at the repo root.
Double-clicking a `.command` file opens Terminal and runs it
interactively -- the exact context RE-DASH.1.10's own diagnostic just
confirmed works, every time, with this exact file. No daemon, no
background permission surface, nothing to silently fail. Less
"automatic" than RE-DASH.1.8's original ambition, but it is the
option consistent with this project's stated preference for
robustness over sophistication: a system Armando can trust and
understand over one that looks more automatic but fails silently in
the background.

Removed as dead code: `scripts/com.armando.sop-dashboard-regen.plist`
and `scripts/regenerate_dashboard.sh` (the `scripts/` directory is now
empty and was not kept). Leaving non-functional launchd config in the
repo would have misled a future reader into believing background
auto-regeneration works.

What this does not authorize:

-   No change to `generate_dashboard.py` -- the `.command` file calls
    it unmodified, same as every prior mechanism attempted.
-   Does not reopen RE-DASH.1.8/1.9's launchd approach without new
    evidence -- if background automation is revisited later, it needs
    an actual TCC/permissions diagnosis first (Console.app, or
    Armando confirming a specific System Settings grant), not another
    blind retry of the same mechanism.

Boundary:

-   `scripts/com.armando.sop-dashboard-regen.plist` and
    `scripts/regenerate_dashboard.sh` deleted. New file:
    `Actualizar Dashboard.command` (repo root).
-   No Frozen Core component touched. No gate, protocol, model or
    loader file touched. `generate_dashboard.py` itself untouched
    across all of RE-DASH.1.8/1.9/1.10.
-   Verified: the diagnostic interactive run in RE-DASH.1.10 already
    proved this exact invocation pattern (`zsh` running this file
    directly, from Terminal) regenerates the dashboard correctly. The
    `.command` file's own `read "?..."` pause-before-close line is
    standard zsh syntax, not independently tested in this sandbox (no
    `zsh` here) -- low risk, since the regeneration itself uses the
    identical proven pattern; only the closing prompt is new.

------------------------------------------------------------------------

## RE-DASH.1.9 — Dashboard: fixes RE-DASH.1.8's real launchd failure

Armando installed RE-DASH.1.8's launchd job and it failed on the real
first run. `logs/launchd_stderr.log` on his machine (read through the
synced folder, not reproduced in this sandbox) showed:

    /bin/zsh: can't open input file: /Users/armando/.../scripts/regenerate_dashboard.sh

The RE-DASH.1.8 boundary note had explicitly flagged that the
`zsh -l -c "<quoted path>"` invocation could not be verified from this
sandbox (no macOS/launchd here) -- that risk materialized. Diagnosis:
`-c`'s argument is supposed to be parsed by zsh as a command string,
with the embedded literal double-quotes stripped as shell quoting; in
practice zsh instead treated the argument as a script *file* to open
directly (the exact error a bare `zsh <path>` invocation produces),
not as a `-c` command string. Root cause not fully re-derived from
first principles here (would require testing directly against zsh on
a Mac, not assumed) -- fixed by removing the fragile construction
instead of trying to patch the quoting further:

-   `scripts/com.armando.sop-dashboard-regen.plist`: `ProgramArguments`
    now directly execs the script by its absolute path (one array
    element, no shell wrapper at the launchd level at all). launchd
    execs it via `execve()`, no shell tokenizes the path, so a path
    containing spaces needs no quoting -- eliminates the entire class
    of bug RE-DASH.1.8 hit.
-   `scripts/regenerate_dashboard.sh`: the login-shell PATH pickup
    (needed so `python3` resolves the same way it does in an
    interactive Terminal) moved *inside* the script, wrapping only the
    `python3 generate_dashboard.py` call in a nested
    `zsh -l -c 'python3 generate_dashboard.py'`. That inner command
    string has no path, no spaces and no embedded quotes -- nothing
    left to get wrong the same way.

What this does not authorize:

-   No change to `generate_dashboard.py` or `WatchPaths`/
    `RunAtLoad`/`ThrottleInterval` -- only the invocation mechanism
    that failed.

Boundary and the same explicit verification gap as RE-DASH.1.8, still
open:

-   Two files modified: `scripts/com.armando.sop-dashboard-regen.plist`,
    `scripts/regenerate_dashboard.sh`.
-   Verified: plist re-parses as well-formed XML; the script's mkdir/
    cd/logging logic re-ran successfully in this sandbox (`python3`
    substituted directly for the nested `zsh -l -c` call, since this
    sandbox has no `zsh` to test that exact line).
-   **Still not verified from this sandbox**: the nested
    `zsh -l -c 'python3 generate_dashboard.py'` line itself, or that
    launchd's direct exec of a shebang script with a space-containing
    path behaves as documented. Armando needs to unload the old job,
    reload the corrected plist, and confirm via
    `logs/dashboard_regen.log` / `logs/launchd_stderr.log` that this
    attempt actually succeeds -- this entry records what was fixed and
    why, not a confirmed-working end state.

------------------------------------------------------------------------

## RE-DASH.1.8 — Dashboard: reactive auto-regeneration (launchd, not an agent)

Armando noticed `outputs/dashboard.html` did not reflect an edit he
had just made to `personal_capacity_facts.xlsx` -- correct behaviour
by RE-DASH.1's own design ("static, read-only", regenerated only when
`generate_dashboard.py` is run), but not what he wants operationally.
Asked explicitly for it to become "operativo actualizándose sin tener
que pasar por ti" -- automatic, and specifically *not* routed through
an agent each time.

Given that framing, the right answer is a deterministic OS-level job,
not a scheduled agent invocation: an agent call still means an LLM in
the loop for a purely mechanical regeneration, which is exactly the
dependency Armando asked to remove, and is a heavier, less
inspectable mechanism than the task requires. Added:

-   `scripts/regenerate_dashboard.sh`: a thin wrapper -- `cd` to the
    repo, run `python3 generate_dashboard.py`, append output to
    `logs/dashboard_regen.log`. No logic of its own; never
    duplicates or reimplements anything `generate_dashboard.py`
    already does.
-   `scripts/com.armando.sop-dashboard-regen.plist`: a macOS launchd
    agent definition using `WatchPaths` on `data/raw/` (all four raw
    source files, not just `personal_capacity_facts.xlsx` --
    `shiller.xlsx`, `dry_powder_ledger.xlsx` and
    `human_approval_attestations.xlsx` are equally inputs to the same
    dashboard). Runs the wrapper via a login shell (`zsh -l -c`) so it
    inherits the same `PATH` an interactive Terminal session already
    uses successfully -- not launchd's minimal default `PATH`, which
    could otherwise resolve a different, dependency-less `python3`.
    `RunAtLoad` regenerates once on login too, so staleness is capped
    at "since last login" even with no file edits. `ThrottleInterval`
    of 10s guards against a single Excel save firing more than one
    filesystem event.
-   `.gitignore` gains `logs/` (runtime output, same principle as
    `outputs/`).

What this does not authorize:

-   No change to `generate_dashboard.py`'s data collection or
    rendering logic -- the wrapper calls it unmodified.
-   Nothing is active until Armando runs the install commands himself
    (`cp` the plist to `~/Library/LaunchAgents/`, `launchctl load`).
    Writing these files does not turn on the automation.

Boundary and an explicit verification gap, stated plainly rather than
glossed over:

-   Three new files (`scripts/regenerate_dashboard.sh`,
    `scripts/com.armando.sop-dashboard-regen.plist`) and one edited
    (`.gitignore`). No Frozen Core component touched, no gate,
    protocol, model or loader file touched, `generate_dashboard.py`
    itself untouched.
-   Verified: the plist is well-formed XML (parsed successfully). The
    wrapper script's own logic (cd, mkdir, call
    `generate_dashboard.py`, append to log) was run end-to-end in this
    sandbox under `bash` (the sandbox has no `zsh`) with the real Mac
    path substituted for the sandbox mount path, and produced a
    correct log entry and a regenerated `outputs/dashboard.html`.
-   **Not verified, and cannot be from this sandbox**: launchd itself,
    the `zsh -l -c` invocation, `WatchPaths` actually firing on a real
    file edit, or whether the executable bit set here survives the
    iCloud sync to Armando's Mac. This sandbox is a separate Linux
    environment mounting the same iCloud folder -- it is not
    Armando's Mac, has no `launchd`, and this design follows standard
    launchd `WatchPaths`/`RunAtLoad`/`ThrottleInterval` semantics from
    documentation, not empirical confirmation on his machine. Armando
    should confirm the first real trigger via
    `logs/dashboard_regen.log` and `logs/launchd_stderr.log` after
    installing it.

------------------------------------------------------------------------

## RE-DASH.1.7 — Dashboard: directional regime wording + one-line evidence label

Armando, reviewing RE-DASH.1.6's output: "Fuera del rango que tuvieron
los episodios parecidos" was still not concrete enough -- asked for
something like "Muy alto frente al histórico comparable". Also flagged
"Retorno mediano posterior (valor típico, no promedio)" as too long
to read on one line, asking for something shorter and clearer.

-   "Por qué no se actúa": the regime row now states direction (alto/
    bajo), not just "outside range". This required real data the gate
    result itself doesn't expose -- `RegimeComparabilityGateResult`
    only carries a boolean-equivalent state, not which side of the
    range today's value fell on. Rather than guess, added
    `_regime_direction()`, which reuses the exact same comparison
    `RegimeComparabilityGate._dimension_covered()` already makes
    (`snapshot.context.<dim>` vs. `[episode.context.<dim> for episode
    in evidence.matches]`) to determine, from the real matched-episode
    values, whether today's value sits above the max or below the min.
    Verified against real data: CAPE=41,4 is above the matched
    episodes' maximum -- "Muy alto frente al histórico comparable".
    Restructured `build_porque_rows()` to emit one row per failing
    regime dimension (was one combined row listing all failing
    dimensions together) -- necessary because direction can differ per
    dimension, and cramming two directions into one pill value would
    have been either wrong or unreadable. Fail-closed: if direction
    cannot be determined from the real match data (missing values),
    falls back to the RE-DASH.1.6 generic phrasing rather than
    guessing "alto"/"bajo".
-   "Evidencia histórica": shortened "Retorno mediano posterior (valor
    típico, no promedio)" to "Retorno mediano posterior". No
    information lost -- "mediano" already precisely means median, not
    average; the parenthetical was pedagogical, not information-
    bearing, and "peor caso"/"mejor caso" already establish this is a
    distribution, not a single figure. Now renders on one line.

What this does not authorize:

-   No change to `RegimeComparabilityGate` or any other gate. The new
    direction calculation is presentation-layer only, reusing data the
    dashboard already had access to (`evidence.matches`,
    `snapshot.context`) -- it does not feed back into `regime_result`
    or any posture decision.

Boundary:

-   One file modified: `generate_dashboard.py` (new
    `_regime_direction()` helper; `build_porque_rows()`'s "not
    comparable" branch restructured to one row per dimension;
    Evidencia histórica label shortened).
-   No Frozen Core component touched. No gate, protocol, model or
    loader file touched.
-   Verified by direct execution against real data: `outputs/dashboard.html`
    regenerated. Spot-checked: "Régimen (CAPE): Muy alto frente al
    histórico comparable" (verified 41,4 > max of the matched
    episodes' CAPE values, not asserted); "Retorno mediano posterior"
    renders on one line. Full `tests/verify_*.py` suite re-run: same
    four pre-existing failures, nothing new.

------------------------------------------------------------------------

## RE-DASH.1.6 — Dashboard: three correctness/density fixes on RE-DASH.1.5's output

Armando reviewed the RE-DASH.1.5 output before committing and flagged
three issues, one of them a real factual error, not just a clarity
problem:

-   "Por qué no se actúa": RE-DASH.1.5's wording, "Régimen (CAPE):
    Fuera del rango de episodios parecidos", still did not say range
    *of what* -- Armando flagged it as unclear on first read ("no se
    entiende"). Reworded to "Fuera del rango que tuvieron los
    episodios parecidos" (and the mirror "Dentro del rango que
    tuvieron los episodios parecidos" for the comparable case) --
    naming explicitly that the range belongs to the comparable
    episodes themselves, not an unstated external threshold.
    Re-confirmed against `regime.explanations` ("cape: today's value
    outside the matched episodes' range") that this reading matches
    the gate's real finding.
-   "Datos de mercado": the two context-window headers used
    inconsistent formats -- "serie Shiller 1871-2026" (a hardcoded
    year range) next to "últimos 50 años, desde 1976-07" (a duration +
    start month). Unified to the same "AAAA-AAAA" pattern for both,
    now computed from the real Shiller dates
    (`dataset.data["Date"].min()/.max()`, never hardcoded): "Serie
    completa (1871-2026)" / "Últimos 50 años (1976-2026)". Also
    addressed Armando's density concern: split the header into two
    rows (`rowspan`/`colspan`, plain HTML table structure, not a new
    interactive control) so each header cell is short instead of one
    long compound string per column. Removed the explanatory
    `<p class="note">` paragraph under the table per Armando's
    explicit "esto sobra" -- the table headers now carry that meaning
    on their own.
-   "Evidencia histórica": the intro sentence said the block "busca
    caídas históricas parecidas al momento actual del mercado", which
    is factually wrong today -- the market is at an all-time high
    (drawdown 0,0%), not falling. Traced the real matching logic
    before rewording (not assumed): `SimilarityEngine.compare()`
    scores each historical episode against *today's snapshot* across
    three groups of dimensions at once -- Event (drawdown, duration,
    speed), Context (CAPE, 3-year pre-crash trend, volatility), and
    Outcome (recovery) -- and `top()` returns the 10 highest-scoring
    episodes. Today's snapshot legitimately has drawdown=0, so the
    block is not "searching for similar drops" -- it is comparing
    today's full market condition, including the absence of a drop,
    against historical drops on several dimensions at once. Reworded
    the intro to say exactly that, without overclaiming which
    dimension dominates the ranking (weights are not asserted here,
    only that multiple dimensions are used).

What this does not authorize:

-   No change to any gate, protocol or engine logic. The two new date
    fields (`market_full_start`, `market_latest_date`) are read
    directly from `dataset.data["Date"]`, already loaded for the
    pipeline -- no new data source.
-   Does not reopen or second-guess the "Régimen" wording decided in
    RE-DASH.1.5 -- re-verified, not changed.

Boundary:

-   One file modified: `generate_dashboard.py` (`build_dashboard_data()`
    gains `market_full_start`/`market_latest_date`; `build_porque_rows()`'s
    two regime-state value strings reworded; `render_html()`'s Datos
    de mercado table header and Evidencia histórica intro paragraph
    rewritten; no new helper functions).
-   No Frozen Core component touched. No gate, protocol, model or
    loader file touched.
-   Verified by direct execution against real data: `outputs/dashboard.html`
    regenerated. Spot-checked: market table headers read "Serie
    completa (1871-2026)" / "Últimos 50 años (1976-2026)" -- same
    format, both computed, neither hardcoded; explanatory paragraph
    removed; Evidencia histórica intro no longer implies an active
    drop. Full `tests/verify_*.py` suite re-run: same four
    pre-existing failures, nothing new.

------------------------------------------------------------------------

## RE-DASH.1.5 — Dashboard: five-point polish pass on RE-DASH.1.4's output

Armando reviewed the RE-DASH.1.4 output and flagged five concrete
readability issues, all addressed directly against real data, no new
design conversation needed:

-   "Por qué no se actúa": the CAPE row's value pill said bare
    "No comparable" with no referent -- unclear what it was being
    compared against. `build_porque_rows()`'s three regime-state
    branches reworded to be self-explanatory on their own:
    "Fuera del rango de episodios parecidos" (was "No comparable"),
    "Dentro del rango de episodios parecidos" (was "Comparable"),
    "Sin datos suficientes para comparar" (was "No medible").
-   "Estado por patrimonio": liquidity table missing the actual
    exceso/déficit figure. Unified the separate Suelo/Techo columns
    into one "Rango de liquidez (suelo / techo)" column and added an
    "Exceso/Déficit" column. Reuses the pre-audited spreadsheet
    formulas already computed inside `personal_capacity_facts.xlsx`
    ("Exceso/(Déficit) vs. suelo/techo de liquidez"), read via the
    same `concepto_map` already used for suelo/techo -- not
    recalculated in Python, avoiding a second, potentially-drifting
    source of truth. New `liquidity_gap()` helper selects the figure
    matching the current status (gap vs. techo if above ceiling, gap
    vs. suelo otherwise -- the buffer already secured when within
    range). New `_fmt_signed_amount()` prefixes "+" for positive
    values so exceso/déficit reads unambiguously at a glance. Verified
    against real data: AMS +22.330,77 € (above techo), AML
    -50.625,00 € (below suelo) -- both match the figures independently
    confirmed via direct execution in RE-DASH.1.3.
-   All string values/labels across the file now start capitalized
    ("Muy por encima de su media histórica", not "muy por encima...";
    "No disponible", not "no disponible") -- confirmed by grep that no
    lowercase-starting return string remains in the six formatter
    functions, `context_band()`'s six branches, or the standalone
    `drawdown_context` fallback.
-   "Evidencia histórica": table values could drift far to the right
    on wide viewports, reading as "perdidos" (disconnected from their
    label). Added a `.kv` table class constraining the table to
    `max-width:640px` and its first column to `width:55%`, keeping
    label and value visually close regardless of viewport width.
-   "Datos de mercado": the single historical-context column (full
    Shiller series, 1871-2026) is now joined by a second column,
    "Contexto reciente (últimos 50 años, desde {fecha})" -- z-score
    context computed over the same series sliced to the trailing 50
    years (`RECENT_WINDOW_YEARS = 50`, cutoff computed the same way
    `drawdown_engine.py` already subtracts integer years from an
    AAAA.MM float date, e.g. `peak_date - 3`). Full-history column is
    kept, not replaced -- Armando's explicit "dejamos la columna con
    el histórico y añadimos una columna". Verified: cutoff resolves to
    1976-07 against a latest date of 2026-07; CAPE reads "muy por
    encima" in both windows, inflación and tipo de interés read
    "cerca de" in both.

What this does not authorize:

-   No change to any gate, protocol or engine logic, and no new data
    source -- the recent-window statistics reuse the same
    `dataset.data` already loaded for the full-history column, sliced
    by date; the liquidity gap figures reuse formulas already computed
    inside the source workbook, not recalculated.
-   Does not revisit the RE-DASH.1.4 decision to drop "qué haría
    falta para cambiar el estado" -- not raised again this round.

Boundary:

-   One file modified: `generate_dashboard.py` (`build_dashboard_data()`
    gains `market_context_recent`/`recent_window_start` and per-
    patrimonio `liquidity_gap_floor`/`liquidity_gap_ceiling`;
    `render_html()` and `build_porque_rows()` updated to consume them;
    two new small helpers, `liquidity_gap()` and
    `_fmt_signed_amount()`; CSS gains `.kv`).
-   No Frozen Core component touched. No gate, protocol, model or
    loader file touched.
-   Verified by direct execution against real data: `outputs/dashboard.html`
    regenerated and spot-checked against the values above. Full
    `tests/verify_*.py` suite re-run: same four pre-existing failures
    (pandas/numpy pin mismatches ×3, known tie-break ordering
    difference ×1), nothing new -- and `generate_dashboard.py` is not
    imported by the test suite regardless.

------------------------------------------------------------------------

## RE-DASH.1.4 — Dashboard: "lectura rápida" design pass, agreed before coding

Full design conversation with Armando, same day, explicitly before any
code: "no dispares todavía en ejecutar, vamos a centrarnos antes en
dejarlo bien perfilado." Every change below was proposed, corrected or
confirmed in that conversation first; nothing here is a unilateral
implementation choice.

Adopted as agreed:

-   "Estado hoy": colored dot (semáforo) next to dominant action text
    -- Armando's own framing, "el color ayuda; la palabra manda."
-   "Por qué no se actúa": rebuilt from prose bullets to one compact
    row per variable (label + pill value) -- `build_porque_rows()`
    replaces the old sentence-based `build_reasons()`.
-   "Estado por patrimonio": rebuilt as two separate compact tables
    (Armando's explicit choice, option B) -- Liquidez (cifra real,
    suelo, techo, estado) and Postura y permisos (postura, Human
    Approval, Dry Powder), keeping money and permissions visually
    separate.
-   "Datos de mercado": added a historical-context column, z-score
    against the full Shiller series (1871-2026, Armando's explicit
    choice over a shorter window), banded at the thresholds he
    confirmed (\|z\|<0.5 / <1.5 / >=1.5). Drawdown reported as plain
    fact ("en máximo histórico" / "caída del X%"), not a z-score --
    comparing a series that is usually exactly zero to its own mean
    would not have read honestly.
-   "Evidencia histórica": reworded once more, folding horizon and
    "fondo del episodio" into one intro sentence, directly answering
    both questions Armando asked in the prior turn instead of leaving
    them for him to infer from a technical row label.
-   Title kept, subtitle added: "Lectura de mercado, evidencia y
    autorización patrimonial. Solo lectura."

One feature discussed at length and explicitly dropped, not built,
after Armando himself raised doubt about it ("sinceramente no sé si
de verdad necesitamos esta pregunta"): "Qué haría falta para pasar de
Conservar a Preparar." Verified by direct execution before answering,
not assumed: ran `DryPowderProtocol().evaluate()` with
`current_posture=Prepare` (pólvora seca disponible, episodio
hipotético activo) -- result: `status=posture no deployment,
authorized_amount=0.0`, identical to `Conserve`. `TRANCHE_PARAMETERS`
only defines tranches for `Deploy Partially`/`Deploy Aggressively`.
Combined with the RE-DASH.1.4-conversation finding that Evidence
Quality Gate structurally caps the combined ceiling at `Prepare`
regardless of Regime/Personal Capacity (confirmed the same day,
`not measurable -> Prepare`; `validated` would map to the MORE
restrictive `Conserve` -- RE-037.1's own design), a "path to Prepare"
feature would have described a transition with zero practical
consequence, added no information beyond "Por qué no se actúa" just
grammatically inverted, and pushed the dashboard's tone toward
"roadmap to action" -- against this project's standing discipline (no
simuladores, no proyecciones, no falsa sensación de progreso).

What this does not authorize:

-   No change to any gate, protocol or engine logic. Two new,
    independent, read-only statistics
    (`dataset.data["CAPE"/"InflationRate1Y"/"Rate GS10"].mean()/.std()`)
    computed directly in `generate_dashboard.py` from data the
    pipeline already loads -- no new data source, no `Dataset`/
    `drawdown_engine.py` change.
-   Does not build, or leave a stub for, "qué haría falta" -- the
    decision was to drop it, not defer it; if it resurfaces, that is a
    new proposal against a real need, not a resurrection of this one.

Boundary:

-   One file modified: `generate_dashboard.py` (rewritten
    presentation layer; `build_dashboard_data()` gains
    `market_context`, otherwise unchanged).
-   No Frozen Core component touched. No gate, protocol, model or
    loader file touched.
-   Verified by direct execution against real data: `outputs/dashboard.html`
    regenerated. Spot-checked: "Estado hoy" shows a warn-colored dot +
    "NO ACTUAR" / "No hay caída de mercado activa."; "Por qué no se
    actúa" shows four one-line rows (Caída de mercado / Régimen (CAPE)
    / Validez predictiva / AML — Liquidez); Estado por patrimonio's
    liquidity table shows AMS "por encima del techo" and AML "por
    debajo del suelo" with real figures; Datos de mercado shows CAPE
    "muy por encima de su media histórica" (41,4 vs. a Shiller-series
    mean well below that) and tipo de interés/inflación "cerca de su
    media histórica". Full `tests/verify_*.py` suite re-run: same four
    pre-existing failures, nothing new.

------------------------------------------------------------------------

## RE-DASH.1.3 — Dashboard: real liquidity ceiling, correcting RE-DASH.1.2's error

Armando caught a real mistake in RE-DASH.1.2 the same day: "revisalo
bien porque tenemos techo y suelo de liquidez para AMS y AML."
RE-DASH.1.2's claim that no ceiling existed was checked against the
wrong source -- `engine.personal_capacity_facts_gate.REQUIRED_LABELS`,
which lists only the fields `PersonalCapacityFactsGate` itself scores,
not the full set of columns the workbook actually carries. Reading
`data/raw/personal_capacity_facts.xlsx` directly (via
`load_personal_capacity_facts_raw()`, already used since RE-DASH.1.2
for the floor figure) shows a real "Techo de liquidez total (máximo
óptimo)" column: 150.000 € for AMS, 300.000 € for AML, alongside
`Exceso/(Déficit) vs. techo de liquidez` already computed in the
sheet. The error was checking the gate's consumed-field allowlist
instead of the raw data actually available -- corrected, not silently
patched: this entry names it plainly.

`LIQUIDITY_CEILING_LABEL` added as a local constant in
`generate_dashboard.py` (not in `REQUIRED_LABELS`, deliberately -- no
gate scores this figure today, so adding it there would misleadingly
imply one does). `liquidity_line()` now reports a real three-way
status: below floor / within range / above ceiling, all against real
numbers.

This surfaced a genuine finding the previous two dashboard iterations
never showed: AMS's real liquidity (172.330,77 €) is currently ABOVE
its own defined ceiling (150.000 €) -- idle liquidity beyond the
optimal range. Reported as informational (amber), explicitly NOT a
gate failure: `PersonalCapacityFactsGate.liquidity_adequate` only
tests the floor (`_safe_ge(liquidez_total, suelo_total_liquidez)`,
RE-032.5's design) -- being above the ceiling does not change the
gate's `adequate` verdict for AMS, and the dashboard text says so
explicitly to avoid implying otherwise. AML remains below its floor
(199.375,00 € vs. 250.000 €), unchanged finding from RE-DASH.1.2.

What this does not authorize:

-   No change to `PersonalCapacityFactsGate` or its `REQUIRED_LABELS`
    -- the ceiling remains unscored by any gate; this iteration only
    displays it.
-   Does not decide whether a ceiling check should ever become part
    of `PersonalCapacityFactsGate`'s logic (e.g. an "exceso de
    liquidez ociosa" fact) -- that would be new gate design, out of
    scope for a display fix, not raised or requested here.

Boundary:

-   One file modified: `generate_dashboard.py`.
-   No Frozen Core component touched. No gate, protocol, model or
    loader file touched.
-   Verified by direct execution against real data: `outputs/dashboard.html`
    regenerated, AMS's panel now reads "172.330,77 € (suelo 100.000,00 €
    / techo 150.000,00 €) -- por encima del techo definido"; AML reads
    "199.375,00 € (suelo 250.000,00 € / techo 300.000,00 €) -- por
    debajo del suelo definido". Full `tests/verify_*.py` suite re-run:
    same four pre-existing failures, nothing new.

------------------------------------------------------------------------

## RE-DASH.1.2 — Dashboard: restructure and real liquidity figures

Armando's second review of the dashboard, same day, with six concrete
proposals plus an explicit invitation to add more: he judged RE-DASH.1.1
readable but still not decisive enough, and gave a target -- "que
alguien pueda abrirlo y entender en 15 segundos: hoy no se hace nada
porque no hay caída activa; aunque hubiera caída, el sistema sigue
limitado por CAPE, evidencia no demostrada y AML bajo liquidez
mínima." No change to `build_dashboard_data()`'s gate/protocol calls
except one addition (real liquidity figures, below) -- this remains a
presentation-only iteration.

Adopted as proposed:

-   Split "Resumen de hoy" into "Estado hoy" (compact: posture + one
    primary reason) and "Por qué no se actúa" (full reason list).
    Dropped RE-DASH.1.1's standalone "Tabla resumen" card -- its
    content is now fully covered by these two cards plus "Estado por
    patrimonio"; keeping all three would have repeated the same
    conclusion three times, against the whole point of this pass.
-   "Estado por patrimonio" rebuilt as a left-aligned "Postura: X /
    Por qué: <bullets>" panel per patrimonio, replacing the three-row
    table.
-   Two phrases rewritten exactly as Armando proposed: the
    predictive-validity sentence now names what RE-PRED.16 actually
    found ("no ha demostrado que sus predicciones mejoren a una
    referencia simple"), and Human Approval's clause now states what
    the standing authorization permits ("La autorización humana
    vigente permite hasta X") instead of the bare "Válido para X".
-   "Nivel del índice" (Shiller Price.1, ~5 million) removed from the
    main Datos de mercado view -- moved into Detalle técnico, labelled
    there as the technical series it is, explicitly not the S&P 500
    level seen in the press (Armando's own point).
-   Evidencia histórica gained an opening sentence ("qué muestra este
    bloque"), relabelled rows, and a closing caveat tying the numbers
    back to predictive validity not being demonstrated.
-   All numbers in the main view now use Spanish decimal/thousands
    convention (`_fmt_pct`/`_fmt_rate`/`_fmt_num`/`_fmt_amount`
    reworked: comma decimal, period thousands) -- matches the exact
    figures in Armando's own illustrative example ("10,2%", "-1,1%",
    "13,8%"), confirmed against real data, not just his mock text.

One proposal corrected, not implemented as drafted, flagged to Armando
directly: he asked for a Patrimonio/Liquidez/Suelo/**Techo**/Estado
table. `PersonalCapacityFactsGate`'s `REQUIRED_LABELS` (and the
underlying `personal_capacity_facts.xlsx` columns) define a floor
(`suelo_total_liquidez`) and an emergency cushion (`colchon`), but no
ceiling -- there is no "techo" concept anywhere in this gate's data
model. Inventing one for display, even a purely cosmetic one, would
have been fabrication -- exactly what this project's fail-closed
discipline exists to prevent. Implemented instead as a real
figure-vs-floor line (`liquidity_line()`): "Liquidez actual: X €
(suelo definido: Y €) -- dentro/por debajo del rango", using the
patrimonio's real numbers, no invented column.

Getting those real numbers required one new, independent, read-only
call: `loaders.personal_capacity_facts_loader.load_personal_capacity_facts_raw()`,
called directly from `generate_dashboard.py` alongside the existing
`build_local_personal_capacity_facts_inputs()` call (which computes
booleans from the same file but never exposes the underlying figures).
This reads `personal_capacity_facts.xlsx` a second time per run --
accepted as a minor inefficiency rather than refactoring the gate
adapter to expose raw figures, since this is a read-only static-report
script, not a hot path, and the alternative would have touched gate
code for a display-only need.

One ordering fix made after first render: the "por qué" bullet list
initially placed the predictive-validity caveat after the
patrimonio-specific extras (e.g. AML's liquidity). Armando's own
"Mi propuesta de orden final" listed predictive validity third and
the patrimonio-specific reason fourth -- reordered to match exactly.

What this does not authorize:

-   No change to any gate, protocol or engine logic. The one new call
    (`load_personal_capacity_facts_raw()`) is a second read of an
    existing file through its existing public loader function --
    `PersonalCapacityFactsGate` itself is untouched.
-   No "techo" figure introduced anywhere, main view or Detalle
    técnico -- confirmed by inspection, this iteration does not add
    one even as a placeholder.

Boundary:

-   One file modified: `generate_dashboard.py`.
-   No Frozen Core component touched. No existing engine, gate,
    protocol, model or loader file touched.
-   Verified by direct execution against real data: `outputs/dashboard.html`
    regenerated twice (once after the initial restructure, once after
    the ordering fix). Spot-checked: "Estado hoy" reads "NO ACTUAR" /
    "No hay caída de mercado activa"; "Por qué no se actúa" lists, in
    order, no-episode / CAPE fuera de rango / validez predictiva no
    demostrada / AML liquidez; AMS shows "172.330,77 € (suelo definido:
    100.000,00 €) -- dentro del rango definido"; AML shows "199.375,00 €
    (suelo definido: 250.000,00 €) -- por debajo del suelo definido";
    Evidencia histórica shows "10,2%" / "-1,1%" / "13,8%", matching
    Armando's own illustrative numbers exactly against real data. Full
    `tests/verify_*.py` suite re-run: same four pre-existing failures,
    nothing new.

------------------------------------------------------------------------

## RE-DASH.1.1 — Dashboard: clarity pass (readable by a first-time viewer)

Armando's review of RE-DASH.1, same day: "no es comprensible para
alguien que lo vea por primera vez... funciona como volcado técnico,
no como panel de mando." Correct -- the six-block layout was
technically accurate but mixed internal state names (`not_demonstrated`,
`under_cooling_off`), code identifiers (`min() combination`, `Price.1`,
`return_count`) and conclusions without translating any of it. No
underlying computation changes in this iteration -- `build_dashboard_data()`
is untouched; only what `render_html()` shows, and in what language.

Rewrote the page structure entirely, per Armando's own proposed order:
Resumen de hoy (single headline conclusion) -> Tabla resumen -> Estado
por patrimonio (AMS/AML) -> Datos de mercado -> Evidencia histórica ->
Detalle técnico (collapsed via native `<details>`/`<summary>` -- a
disclosure widget, not a script or an executable control, so it does
not violate the read-only/no-interactivity boundary). Added a full
Spanish translation layer for every internal state, gate result and
Personal Capacity field name shown in the main view; the old English
identifiers now only appear inside Detalle técnico, which is
explicitly the technical section.

Two corrections made to Armando's own draft text, not just implemented
verbatim -- flagged to him directly, per this project's standing
practice of checking assumptions rather than silently accepting them:

1.  His example headline attributed today's `Conserve` ceiling partly
    to "validez predictiva no demostrada". Checked against
    `engine/posture_mapper.py`'s actual mapping: Evidence Quality's
    `not measurable` state maps to a `Prepare` ceiling, less
    restrictive than the `Conserve` Regime Comparability already
    imposes -- `min()` means Regime Comparability, not predictive
    validity, is what is actually binding today. The headline's
    "Motivos principales" are now built only from whichever gate(s)
    `combined.explanations` already reports as limiting; predictive
    validity stays a separate, always-shown epistemic caveat under
    Evidencia histórica, never framed as a cause of the ceiling.
2.  His first-draft Personal Capacity wording ("Correcto financieramente")
    was too vague and, for `adequate` states like AMS today,
    specifically imprecise -- it does not say all nine facts passed,
    only implies a positive judgement. Personal Capacity summaries are
    now built directly from the gate's own `failed_fields`/
    `missing_fields` when `constrained`, and from an explicit "9/9
    hechos correctos, incluida liquidez" framing when `adequate` --
    matching Armando's own follow-up correction, which asked for the
    same precision.

Real bug found and fixed while rebuilding: `Rate GS10` (10-year US
Treasury yield) in the Shiller data is already expressed in
percentage points (a raw value of 4.44 means 4.44%), confirmed by
reading `Snapshot.context.interest_rate` directly (`interest_rate 4.44`)
before touching any formatting code. RE-DASH.1's formatter multiplied
by 100 a second time, as if it were a decimal fraction like
`drawdown`/`inflation` are -- displaying "444.0%". `_fmt_rate()` is now
a separate formatter from `_fmt_pct()`, used only for this field.

A second, smaller bug caught in self-review before shipping: the
first draft of the Tabla resumen's per-patrimonio "Lectura humana"
lowercased the first letter of the Human Approval clause when
appending it after the capacity clause -- producing "human Approval",
incorrectly de-capitalizing a proper term. Fixed to never lowercase
that clause.

Colors reduced to three semantic values (verde/ámbar/rojo) plus one
muted neutral grey reserved strictly for "no aplica hoy" (e.g. Dry
Powder with no active episode) -- confirmed this is not a fourth
severity level, just an explicit "not applicable" marker, per
Armando's "máximo 3 colores" instruction.

What this does not authorize:

-   No change to any gate, protocol or engine logic, and no change to
    `build_dashboard_data()` -- confirmed by inspection: only
    `render_html()` and its new helper functions (translation tables,
    `build_headline()`, `build_summary_rows()`, the
    `personal_capacity_long/short()`, `human_approval_long()`,
    `dry_powder_long()` humanizers) were touched.
-   Does not add any interactivity beyond the native `<details>`
    disclosure -- still zero `<script>`, `<button>`, `<form>`,
    `onclick` in the generated HTML.
-   Translation coverage is scoped to the vocabulary this pipeline
    actually produces today (confirmed by execution, not guessed) --
    `humanize_explanation()` falls back to the untranslated string for
    anything unmapped rather than inventing a translation, and that
    fallback only surfaces inside Detalle técnico.

Boundary:

-   One file modified: `generate_dashboard.py` (structure and
    rendering rewritten; `build_dashboard_data()` unchanged).
-   No Frozen Core component touched. No existing engine, gate,
    protocol or model file touched.
-   Verified by direct execution against real data twice: once after
    the initial rewrite, once after the Human Approval capitalization
    fix found in self-review. Spot-checked the generated HTML:
    headline reads "NO ACTUAR" with two accurate motivos (CAPE fuera
    de rango; liquidez de AML por debajo del mínimo), GS10 now shows
    "4.44%", Tabla resumen shows "Human Approval" correctly
    capitalized, AMS/AML never fused. Full `tests/verify_*.py` suite
    re-run: same four pre-existing failures, nothing new.

------------------------------------------------------------------------

## RE-DASH.1 — Static SOP/Shiller Audit Dashboard

First presentation/audit-layer deliverable, deliberately numbered
outside the RE-044.x/RE-EXP.x sequence at Armando's own request
(2026-08-14): this touches the Research Engine + SOP audit surface,
but is not a methodological fix to the engine itself.

Spec closed over two rounds with Armando (2026-08-14 initial DASH-001
draft with 4 corrections; 2026-08-15 second pass reframing it as a
"panel de mando" with 3 further corrections) before any code was
written, per this project's standing discipline.

New file: `generate_dashboard.py` (repo root, same pattern as
`audit_posture.py`). Single command:

```
python3 generate_dashboard.py
```

Writes `outputs/dashboard.html` -- static, no server, no JS, no
buttons, no forms. `outputs/` added to `.gitignore` (RE-DASH.1's own
scope decision from the first round: a derived artifact must never be
versioned).

Computes nothing new. Reuses exactly the same calls
`audit_posture.py` already makes end-to-end (drawdown dataset ->
`ResearchEngine` -> Evidence Quality / Regime Comparability /
Personal Capacity Facts gates -> `evaluate_capital_posture()` ->
Human Approval -> Dry Powder Protocol, all per patrimonio), plus one
additional read-only call this script adds:
`engine.live_episode.run_live_episode_detector()`, for the market
block's own episode detail -- same function `dry_powder_ledger_state.py`
already calls internally, not a second implementation of episode
detection.

Six blocks, closing the second-round correction that "Gates" must
never include Human Approval (CONSTITUTION.md v2.0 Section 5, written
the same day, is explicit: Human Approval is never part of
`gate_combination.py`'s `min()`):

1.  Cabecera -- data date, generation timestamp, "Techo de mercado"
    (Evidence Quality + Regime Comparability only -- market-wide by
    design, RE-043.1's own reasoning; explicitly NOT a fused
    per-patrimonio posture).
2.  Mercado Shiller -- price (labelled "Real Total Return Price
    (Shiller Price.1)", confirmed against the real field before
    labelling it), drawdown, CAPE, inflation, GS10, active-episode
    detail.
3.  Gates -- Evidence Quality and Regime Comparability (global, one
    row each), Personal Capacity Facts per patrimonio (one-line
    semaphore only; full detail lives in block 5, not duplicated
    here -- second-round correction 3).
4.  Prerrequisitos y protocolos -- Human Approval and Dry Powder
    Protocol, per patrimonio, explicitly separate from Gates.
5.  Patrimonios -- AMS and AML, each with its own combined posture
    ceiling (Gates including this patrimonio's Personal Capacity
    Facts) and the Personal Capacity Facts detail (failed/missing
    fields) that block 3 only summarized.
6.  Evidencia histórica -- compact only: `return_count`, horizon,
    median/worst/best return, `NOT_DEMONSTRATED` with its source note.
    No top-10 matches table -- explicitly retired from the original
    DASH-001 acceptance criteria in the second round, once "primero
    decisión, luego causa, luego datos mínimos" became the organizing
    rule. Supporting/weak similarity dimensions and contradicting
    precedents exist in `Explanation` but were deliberately left off
    this block too -- not asked for, and adding them would be exactly
    the "dato por si acaso" overload the second round's whole
    reframing existed to prevent.

Alerts block: synthesized, not hand-written -- a fixed list of checks
against this run's actual results (active episode y/n, gate
not-measurable/not-comparable states, per-patrimonio Personal Capacity
blocks/constraints, Human Approval missing/expired/under cooling-off),
capped at 5, each line only appears if true this run. Never a
recommendation.

What this does not authorize:

-   No change to any gate, protocol or engine logic -- this script
    only calls existing functions and renders their output.
-   No wiring to `run.py` or `DecisionEngine`.
-   No interactivity of any kind (no buttons, forms, filters,
    auto-refresh) -- confirmed by direct inspection of the generated
    HTML (zero `<script>`, `<button>`, `<form>`, `onclick`).
-   Does not resolve the open governance question from the first
    round (does a Research Engine script documenting SOP-layer state
    need its own numbering track outside RE-044.x) beyond using
    `RE-DASH.1` as Armando's own confirmed choice -- no broader
    precedent is claimed for future dashboard work.

Boundary:

-   Two files created/modified: `generate_dashboard.py` (new),
    `.gitignore` (`outputs/` added).
-   No Frozen Core component touched. No existing engine, gate,
    protocol or model file touched.
-   Verified by direct execution, not just reading: ran
    `python3 generate_dashboard.py` against real data --
    `outputs/dashboard.html` generated with no exception. Spot-checked
    the generated HTML against the real state already on record in
    this document: no active episode (market at its 2026.07 peak, per
    RE-041.2's own finding), AML Personal Capacity Facts `constrained`
    on `liquidity_adequate` (RE-043.1's real finding), AMS Human
    Approval `under_cooling_off` with pending increase effective
    2026-08-27 (matches the 14-day cooling-off from the first real
    attestation, RE-032.x) -- all consistent, nothing invented. Full
    `tests/verify_*.py` suite re-run: same four pre-existing failures
    (pandas/numpy pin mismatch x3, one known tie-break ordering
    difference in `verify_research_engine.py`), nothing new.

------------------------------------------------------------------------

## RE-044.6 — Research Engine: first real revision of the founding constitution (v1.0 -> v1.1)

Armando reviewed `docs/CONSTITUTION_RESEARCH_ENGINE.md` right after it
was saved (RE-044.5) and marked five things -- his own framing: "no lo
reescribiría, solo una pasada quirúrgica." None change the spirit of
any article; all sharpen wording that today's actual practice had
already tested against.

1.  Relación con `docs/CONSTITUTION.md` added at the top: on conflict,
    `docs/CONSTITUTION.md` governs the whole SOP, this document
    governs only the Research Engine. They were never actually
    competing, but it was not written down.
2.  Artículo 1: "el motor no intenta predecir el futuro" was too
    absolute against what the code actually does -- it computes
    `future_return_5y`, MAE, hit-rate, rank correlation
    (`engine/validation_harness.py`, `engine/validation_metrics.py`).
    New wording distinguishes "promete predecir / emite forecasts
    accionables" (never) from "mide resultados históricos para
    evaluar precedentes y validar hipótesis" (yes, and already does).
3.  Artículo 4: look-ahead bias named explicitly, for both market data
    and episode selection -- the rule was already there in substance
    (`engine/observable_universe.py`'s point-in-time masking,
    RE-023.3), just not in the constitution's own words.
4.  Artículo 7: clarifies Alta/Media/Baja is the required category,
    not a literal code name -- `NOT_MEASURABLE`, `LOW` and similar
    already coexist with this today and were never actually in
    tension with the article, just unstated.
5.  Artículo 8: "variables que lo contradicen" -> "variables y
    precedentes... variables o precedentes que lo contradicen" --
    RE-EXP.1, same day, showed the most useful counter-evidence is
    often a dissenting historical episode, not a weak similarity
    dimension.

Also added: a versioning policy this document did not have --
"cualquier cambio en estos artículos exige incrementar la versión
constitucional y registrar la razón" -- and a "Historial de
revisiones" section applying that policy to itself immediately, not
just stating it abstractly. `core/version.py`'s `CONSTITUTION_VERSION`
bumped `"1.0"` -> `"1.1"` in the same pass, kept in sync per that same
new policy.

What this does not authorize:

-   No change to the number or scope of the twelve articles -- five
    wording edits inside existing articles, one new top-of-document
    policy note. Armando's explicit boundary: "no lo reescribiría."
-   Does not reopen RE-044.1 through RE-EXP.1 -- none of the five
    edits change what those fixes did or require touching them again.

Boundary:

-   Two files modified: `docs/CONSTITUTION_RESEARCH_ENGINE.md`
    (five wording edits, one new policy note, one new "Historial de
    revisiones" section), `core/version.py`
    (`CONSTITUTION_VERSION` "1.0" -> "1.1").
-   No code logic touched.
-   No Frozen Core component touched.

------------------------------------------------------------------------

## RE-044.5 — Research Engine: founding constitution saved as a repo file

Closes the gap every entry from RE-044.1 through RE-EXP.1 noted but
did not fix: the Research Engine's 12-article founding constitution
existed only in conversation, never as a file, since the project
began. `core/version.py` referenced a `CONSTITUTION_VERSION` for a
document that was never in the repository -- confirmed by repo-wide
search before RE-044.1 (README.md, docs/ARCHITECTURE/, docs/RESEARCH/,
docs/VALIDATION/ are all empty stub directories from 2026-07-29,
never populated).

Saved verbatim to `docs/CONSTITUTION_RESEARCH_ENGINE.md`: the twelve
articles, the Axioma Fundamental, and Armando's own closing addition
("el valor del Research Engine no reside en acertar el futuro..."),
unchanged from the text that governed this afternoon's audit -- not a
new or revised version.

Separately corrected: `core/version.py`'s `CONSTITUTION_VERSION` said
`"1.1"`. The saved document's own header says `"Versión 1.0"`, in
Armando's own words, and its text never changed between being written
and being saved -- there was no real "1.1" revision for the constant
to refer to. Corrected to `"1.0"` to match the file that now actually
exists, rather than a revision that never happened.

`docs/CONSTITUTION.md` (the SOP-level document, distinct from this
one) updated in Section 5 to list the new file as a real deliverable,
and its two stale cross-references to this governance doc's version
(`v1.93`, left over from this morning's RE-043.4 work) corrected to
`v1.98` -- found stale while making this edit, not flagged separately.

What this does not authorize:

-   No revision to the twelve articles themselves -- saved exactly as
    written, still v1.0.
-   Does not retroactively edit RE-044.1 through RE-EXP.1's existing
    entries above, which correctly describe the document as missing
    at the time each of them was written -- historical entries record
    state at the time, they are not rewritten when something they
    noted later gets fixed.

Boundary:

-   Three files modified: `docs/CONSTITUTION_RESEARCH_ENGINE.md`
    (new), `core/version.py` (`CONSTITUTION_VERSION` corrected),
    `docs/CONSTITUTION.md` (new deliverable listed, two stale version
    cross-references corrected).
-   No code logic touched -- `core/version.py`'s change is a string
    constant, not behavior.
-   No Frozen Core component touched.

This closes the full afternoon audit against the Research Engine's
12-article founding constitution: the document now exists as a file,
and every violation found against it (Articulo 7: RE-044.1, RE-044.2;
Articulo 3: RE-044.3; Articulo 5: RE-044.4; Articulo 8: RE-EXP.1) has
a corresponding, verified fix.

------------------------------------------------------------------------

## RE-EXP.1 — Research Engine: ExplanationEngine fixed, reconnected, extended to contradicting evidence (Articulo 8)

Fifth and final fix of the audit against the Research Engine's
12-article founding constitution, opened this afternoon. Armando's own
framing, correct and kept: this is a functional correction of
explicabilidad, not a refactor -- numbered RE-EXP.1 at his explicit
request, a separate sequence from RE-044.x because this is a distinct
functional defect (a crash) plus a constitutional gap (Articulo 8),
not another instance of the "found a stale reference, centralized a
constant" pattern the RE-044.x entries share.

`ExplanationEngine.build()` read `first.event.drawdown_similarity`.
Confirmed by running it against real data before proposing anything:
`AttributeError: 'SimilarityExplanation' object has no attribute
'drawdown_similarity'`. The real object flowing through
`Similarity.event/context/outcome` has always been
`SimilarityExplanation` (title, score, items) -- `models/similarity.py`
even had the wrong type hint (`Explanation`) for these three fields,
corrected in the same pass. It also only ever inspected
`self.matches[0]`, never the full sample, and had no concept of
contradicting evidence at all -- only "strongest/weakest similarity
dimension of the single best match," which is a similarity
diagnostic, not evidence that agrees or disagrees with a conclusion.
None of this was caught earlier because `ResearchResult` never wired
the engine in (RE-027.2's deliberate exclusion).

Presented as a choice: (A) fix the crash only, keep the existing
narrow scope, or (B) fix the crash and build real Articulo 8
compliance -- supporting dimensions, weak dimensions, AND genuine
contradicting precedents. Armando chose B and fixed the exact scope
himself:

1.  `ExplanationEngine` reads the real flat fields on `Similarity`
    (`drawdown_score`, `duration_score`, ... `recovery_score`) instead
    of the broken `.event.drawdown_similarity` path.
2.  Averaged across every match in the sample, not just the first.
3.  Renamed `strongest_dimensions`/`weakest_dimensions` to
    `supporting_similarity_dimensions`/`weak_similarity_dimensions` --
    honest about what they measure (analogy quality, not evidentiary
    agreement).
4.  New: `contradicting_precedents`. If `Evidence.median_return` is
    positive, lists matches whose actual return at the same horizon
    was negative; if negative, lists the positive ones; if the median
    has no clear sign (`== 0.0` exactly -- an edge case, unlikely with
    continuous real returns, but Articulo 8 requires an explicit rule,
    not a silent gap), lists the matches furthest from it, capped at
    `EXPLANATION_MAX_CONTRADICTING_PRECEDENTS`. When no true
    counter-examples exist, the notes say so explicitly instead of
    fabricating one -- verified directly (see Boundary).
5.  Fully isolated: `EvidenceEngine` untouched, match selection
    untouched, evidence calculation untouched.
   `ExplanationEngine.__init__` now also takes `evidence` (previously
    only `matches`) specifically to read
    `Evidence.median_return`/`horizon_years` already computed by
    `EvidenceEngine` rather than recomputing an independent median
    here -- same single-source-of-truth reasoning as RE-044.1's
    Confidence unification, not scope creep: it does not touch how
    `Evidence` computes anything, only what `ExplanationEngine`
    consumes from it.

Reconnected: `ResearchResult` gained an `explanation: Explanation`
field, populated by `build_research_result()` -- closing RE-027.2's
"intentionally excluded until it is rebuilt" note for good. Confirmed
zero other construction sites for `ExplanationEngine` existed anywhere
in the repo before changing its constructor signature (repo-wide
grep), so no other caller needed updating.

What this does not authorize:

-   No change to `EvidenceEngine`, `SimilarityEngine`, or how matches
    are selected -- `ExplanationEngine` only consumes their output.
-   `run.py`'s printed output unchanged -- the explanation is now
    available on `ResearchResult.explanation` but not yet displayed
    anywhere. Deliberately out of scope for this iteration; a later,
    separate step if wanted.
-   The dimension supporting/weak split (top-3/bottom-3 of up to 7)
    inherits a pre-existing edge case unchanged: with fewer than 6
    dimensions carrying data, the two groups can overlap. Not
    introduced by this iteration, not fixed by it either.

Boundary:

-   Five files modified: `core/constants.py` (two new named
    constants), `models/similarity.py` (type hint fix,
    `Explanation` -> `SimilarityExplanation`), `models/explanation.py`
    (new `ContradictingPrecedent` dataclass, `Explanation` fields
    renamed/added), `engine/explanation_engine.py` (rewritten:
    fixed data access, averages over the full sample, new
    contradicting-precedent logic), `engine/research_pipeline.py`
    (reconnects `ExplanationEngine`, adds `explanation` to
    `ResearchResult`), `models/research_result.py` (new field +
    updated docstring).
-   No Frozen Core component touched.
-   Verified by direct execution before considering this done, not
    just by reading: (1) real pipeline run -- zero crash, produced
    `supporting_similarity_dimensions`, `weak_similarity_dimensions`,
    and one real `contradicting_precedents` entry (the 1998.09
    episode, actual return -1.09% against a sample median of +10.19%);
    (2) four synthetic cases exercising every branch of
    `_contradicting_precedents()` -- negative median, no evidence
    available, zero counter-examples found, and the median-exactly-zero
    fallback -- all produced the expected explicit message, none
    crashed. Full `tests/verify_*.py` suite re-run: same four
    pre-existing failures, nothing new; `run.py` unchanged
    (`Confianza: ALTA`).

This closes the full afternoon audit: Articulo 7 (RE-044.1, RE-044.2),
Articulo 3 (RE-044.3), Articulo 5 (RE-044.4), Articulo 8 (RE-EXP.1).
Every violation found in the original audit against the Research
Engine's 12-article founding constitution has a corresponding fix,
each proposed as a choice and decided by Armando, not assumed.

------------------------------------------------------------------------

## RE-044.4 — Research Engine: traceability metadata on ResearchResult (Articulo 5)

Fourth fix of the audit against the Research Engine's 12-article
founding constitution. Articulo 5: "toda respuesta producida por el
motor debera poder reconstruirse... datos utilizados, funciones
ejecutadas, parametros empleados, version del motor, fuentes
consultadas." `core/version.py` already defined `ENGINE_NAME`/
`ENGINE_VERSION` specifically for this purpose (its own docstring:
"toda respuesta generada debera incluir esta informacion") -- nothing
ever attached them to an actual result. `ResearchResult` carried only
`snapshot`, `matches`, `evidence`; no version, no parameters, no
execution timestamp.

Added four fields, populated at the single construction site
(`engine/research_pipeline.py::build_research_result()` -- confirmed
via repo-wide search this is the only place `ResearchResult(...)` is
called, so no other call site needed updating): `engine_name`/
`engine_version` (read from `core/version.py`, not reinvented),
`matches_count`/`horizon_years` (the actual parameters that
invocation received), `generated_at` (wall-clock date of execution,
distinct from `snapshot.date`, which is the market date under
analysis, not when the code ran).

Two things deliberately left out, documented in the class docstring
rather than silently absent: "fuentes consultadas" (which data file
fed the `Dataset`) is not included -- `ResearchResult` only knows the
`Dataset` object it was handed, not its origin, and asserting
`data/raw/shiller.xlsx` here would be an unverified claim at this
point in the code (Articulo 12 -- do not substitute absence of
verification with a plausible-sounding guess). "Funciones ejecutadas"
is not added as a per-instance field either -- the pipeline sequence
is fixed and identical for every instance (already documented in the
class docstring), so a runtime field would be redundant, not new
information.

Separately noted, not fixed this iteration: `core/version.py` also
defines `CONSTITUTION_VERSION = "1.1"`, referring to the Research
Engine's own 12-article founding constitution -- which still does not
exist as a file in this repo (see RE-044.1's opening note). A version
constant pointing at a document that isn't there is itself a minor
traceability gap; deferred, since saving that document is Armando's
call, not something to do as a side effect of this fix.

What this does not authorize:

-   No "fuentes consultadas" field added (see above -- would require
    the loader layer to pass provenance through, out of scope here).
-   No change to how `ResearchResult` is consumed --
    `DecisionEngine`/`AssessmentEngine`/`audit_posture.py` all read
    only `.snapshot`/`.matches`/`.evidence` today and are unaffected
    by the new fields.
-   Does not save the missing 12-article constitution document or
    reconcile `CONSTITUTION_VERSION`.

Boundary:

-   Two files modified: `models/research_result.py` (four new
    required fields + docstring explaining what was added and what
    was deliberately left out), `engine/research_pipeline.py` (two
    new imports, four new keyword arguments at the single construction
    site).
-   No Frozen Core component touched.
-   Verified directly: constructed a real `ResearchResult` via
    `DecisionEngine` and printed all four new fields (`SOP Research
    Engine`, `1.0.0`, `10`, `5`, `2026-08-14`) before considering this
    done. Full `tests/verify_*.py` suite re-run: same four
    pre-existing failures, nothing new; `run.py` unchanged
    (`Confianza: ALTA`).

------------------------------------------------------------------------

## RE-044.3 — Research Engine: deliberate removal of dead, broken architecture (Articulo 3)

Third fix of the audit against the Research Engine's 12-article
founding constitution. Armando's framing, kept verbatim because it is
the correct one: this is not cosmetic cleanup, it is retirada de
arquitectura muerta y peligrosa -- not a refactor.

`models/dataset.py`'s `Dataset` carried ten methods (two filters,
eight statistics: averages and positive-return probabilities at
1/3/5/10 years) with zero call sites anywhere in the real pipeline --
confirmed by repo-wide grep before touching anything. Almost
certainly a leftover from the `ProbabilityEngine` stage, which
`DecisionEngine`'s own docstring says "desaparece de este flujo por
completo" (RE-024.2), superseded by `EvidenceEngine`/`Evidence`. A
model class computing statistics is itself an Articulo 3 violation
(Modelos represents, Motor calculates) independent of whether the
methods were ever called.

`core/dataset_builder.py`'s `DatasetBuilder` was worse than unused --
it was broken two different ways. It built `Episode` objects with
fields (`date`, `price`, `cape`...) that do not match the real
`Episode` dataclass (`peak_index`, `bottom_index`, `drawdown`...,
established since `drawdown_engine.py`'s `filter_episodes()`), and
separately called `Dataset(episodes)` positionally against a
dataclass requiring two fields (`data`, `episodes`) -- binding the
episode list to the `data` parameter and leaving `episodes` unfilled.
Two independent `TypeError`s waiting for the first caller. Nothing
calls it; the real pipeline builds `Dataset` directly in
`drawdown_engine.py:312`. Armando's own words on why this matters more
than plain dead code: "no solo está muerto: está roto. Eso es peor
que muerto, porque invita a usar una ruta que parece oficial y falla."

Decision: remove, don't repair, don't relocate. Presented as a choice
(A: remove / B: fix DatasetBuilder + move the ten methods to a new
engine) -- Armando chose A with his own explicit acceptance criteria:
real pipeline keeps passing, `drawdown_engine.py` keeps building
`Dataset` directly, no broken call sites (there were none to begin
with), no new `dataset_engine.py` introduced, `DatasetBuilder` not
repaired. Rebuilding unused logic against an architecture it predates,
with no real consumer waiting, is the same pattern already rejected
this project for X/Y/Z and the calculador de impacto temporal
(Articulo 9, Parsimonia) -- Armando's own reasoning, not just mine.

What this does not authorize:

-   No new `engine/dataset_engine.py` or equivalent -- if this logic
    is needed later, it gets rebuilt against Episode's current shape
    with a real consumer from the first commit, not resurrected as-is.
-   `drawdown_engine.py` untouched -- already built `Dataset` directly,
    never depended on `DatasetBuilder`.
-   No change to `Episode`, `Context`, or any other model.

Boundary:

-   `models/dataset.py` rewritten: `Dataset` is now only the
    dataclass (`data`, `episodes`), with a docstring explaining what
    was removed and why, and what a future reimplementation would owe
    (real consumer, current Episode shape).
-   `core/dataset_builder.py` deleted.
-   `tests/verify_core.py`: removed the one line that checked
    `core/dataset_builder.py` existed -- it was a pure file-existence
    check, never exercised the broken code, so removing it doesn't
    lower real coverage of anything that worked.
-   No Frozen Core component touched.
-   Full `tests/verify_*.py` suite re-run: same four pre-existing
    failures as always, nothing new. `run.py` re-run directly:
    unchanged output, `Confianza: ALTA` as after RE-044.1/RE-044.2.

------------------------------------------------------------------------

## RE-044.2 — Research Engine: centralized scattered magic numbers (Articulo 7)

Second fix of the audit against the Research Engine's 12-article
founding constitution. Articulo 7's second clause: "los umbrales se
definiran como constantes globales del sistema. Nunca existiran
numeros magicos distribuidos por el codigo." Two numbers were found
violating this, independently repeated rather than centralized:

`MIN_DRAWDOWN = -0.10` lived in `engine/drawdown_engine.py`, and --
found only by checking who else imports it before touching it -- is
also imported directly from there by `engine/live_episode.py` and
`engine/human_approval_state.py` (RE-032.4's own definition of market
crisis depends on this exact constant). This is a load-bearing shared
value across the Research Engine AND the SOP gates layer, not an
internal detail.

The default sample size of 10 historical matches was repeated as a
bare literal, independently, in four places with no declared relation
to each other: `engine/research_pipeline.py::build_research_result`'s
`matches_count` default, `engine/validation_harness.py`'s `n_matches`
default, `engine/dimension_diagnostic.py::dimension_forecast`'s `n`
default, and `engine/validation_engine.py::coverage()`'s denominator
(`len(matches) / 10.0`). They agreed by convention, not by design --
nothing forced them to.

Fix: both now live once in `core/constants.py` --
`MIN_DRAWDOWN = -0.10` and `DEFAULT_MATCH_COUNT = 10` -- and every
site above references the constant instead of a literal.
`engine/drawdown_engine.py` re-exports `MIN_DRAWDOWN` unchanged
(`from core.constants import MIN_DRAWDOWN`) specifically so
`engine/live_episode.py` and `engine/human_approval_state.py`'s
existing `from engine.drawdown_engine import MIN_DRAWDOWN` keeps
working untouched -- backward compatibility over a wider, unnecessary
refactor (Constitución del SOP, Artículo 14).

What this does not authorize:

-   No value changed -- `MIN_DRAWDOWN` is still -0.10,
    `DEFAULT_MATCH_COUNT` is still 10. Pure centralization, zero
    behavior change (confirmed: `run.py`'s printed Confianza reading
    stayed `ALTA`, unchanged from RE-044.1).
-   No other magic numbers addressed in this iteration (e.g.
    `snapshot_engine.py`'s hardcoded `36` months / 3 years, noted in
    the original audit but out of scope here -- not blocking, not
    forgotten, just not this iteration's cut).
-   `engine/live_episode.py` and `engine/human_approval_state.py` not
    touched at all -- their existing import keeps resolving through
    the re-export, by design.

Boundary:

-   Six files modified: `core/constants.py` (two new constants +
    rationale), `engine/drawdown_engine.py` (definition replaced by
    re-export), `engine/research_pipeline.py`,
    `engine/validation_harness.py`, `engine/dimension_diagnostic.py`,
    `engine/validation_engine.py` (literal replaced by import in
    each).
-   No Frozen Core component touched.
-   Full `tests/verify_*.py` suite re-run, including specifically
    `verify_live_episode.py` and `verify_human_approval_state.py`
    (the two real consumers of the re-exported `MIN_DRAWDOWN`): both
    pass unchanged. Same four pre-existing failures as always
    (pandas/numpy pin mismatches, `verify_research_engine.py`'s known
    tie-break ordering), nothing new.

------------------------------------------------------------------------

## RE-044.1 — Research Engine: unified categorical Confidence (Articulo 7)

First fix of the audit against the Research Engine's own 12-article
founding constitution (never saved as a repo file until today, see
docs/CONSTITUTION.md's Research Engine section / RESUMEN notes).
Articulo 7 requires categorical Alta/Media/Baja confidence with
thresholds as named global constants -- `core/confidence.py` existed
but was empty.

Investigation found the gap was worse than "file not filled in": two
independent, disconnected confidence computations existed.
`ValidationEngine.confidence()` -> `Confidence` dataclass (coverage +
consistency + diversity + stability, averaged) was consumed only by
`AssessmentEngine`, which is not wired into `run.py` and carries its
own explicit warning that the score "must not be used as a
capital-allocation gate until the placeholder is replaced or
explicitly governed" (`stability` is hardcoded to 1.0, unimplemented).
Separately, `DecisionEngine.confidence()` -- the one `run.py` actually
prints -- computed its own ad-hoc Alta/Media/Baja from a match-count
threshold (score >= 0.75, count >= 8/4), hardcoded inline,
contradicting its own module's documented claim of carrying no
statistical logic of its own (RE-024.2).

Presented two options to Armando: (A) unify into one confidence
system, or (B) keep both but name, centralize and document them as
answering genuinely different questions. Armando chose A.

Implementation: `core/confidence.py` now defines `categorize(score)`,
the single translation from `Confidence.score` to Alta/Media/Baja.
Thresholds added to `core/constants.py`
(`CONFIDENCE_SCORE_ALTA_THRESHOLD = 0.75`,
`CONFIDENCE_SCORE_MEDIA_THRESHOLD = 0.50`), calibrated against the
achievable range of the score given `stability`'s current placeholder
(always +0.25, so the floor is 0.25, not 0.0) -- divides [0.25, 1.0]
into equal thirds. `DecisionEngine.confidence()` now delegates to
`ValidationEngine.confidence(self._matches).score` + `categorize()`
instead of its own logic.

This is a real, visible behavior change, not a pure refactor: for
today's actual snapshot, the old logic read `BAJA`
(few matches scored >= 0.75 individually) and the new one reads `ALTA`
(unified score 0.884 -- coverage 1.0, consistency 0.937, diversity
0.6, stability 1.0 placeholder). Confirmed by running both before
committing to the change, not assumed.

What this does not authorize:

-   Does not implement `stability` for real -- still hardcoded 1.0 in
    `ValidationEngine.stability()`. The caveat AssessmentEngine
    already carried ("must not be used as a capital-allocation gate
    until the placeholder is replaced or explicitly governed") is
    inherited by `DecisionEngine.confidence()` now too, not resolved.
    Documented explicitly in `core/confidence.py` and
    `core/constants.py`, not hidden.
-   Does not change `AssessmentEngine` -- still exposes only the raw
    `Confidence` object, not run through `categorize()`. Left
    untouched deliberately to keep this iteration to the path that is
    actually user-facing (`run.py` via `DecisionEngine`).
-   Does not touch `models/confidence.py`'s dataclass, `coverage()`,
    `consistency()`, or `diversity()` -- computation unchanged, only
    the categorical reading on top of it.
-   No wiring into `run.py`'s call sites beyond what already existed
    -- `run.py` still just calls `decision.confidence()`, unaware its
    internals changed.

Boundary:

-   Three files modified: `core/constants.py` (two new named
    constants + rationale comment), `core/confidence.py` (was empty,
    now `categorize()` + module docstring explaining the prior
    duplication), `engine/decision_engine.py` (`confidence()` method
    replaced, class docstring updated, two new imports, `self.validation`
    added to `__init__`).
-   No Frozen Core component touched.
-   Full `tests/verify_*.py` suite re-run: same four pre-existing
    failures as before this change (pandas/numpy pin mismatches on
    `verify_baseline_harness.py` / `verify_secondary_baselines.py` /
    `verify_validation_metrics.py`, and `verify_research_engine.py`'s
    known tie-break ordering difference) -- nothing new. No test
    asserted a specific `DecisionEngine.confidence()` value, so the
    BAJA -> ALTA change did not require any test update, but was
    verified by direct execution before and after.

------------------------------------------------------------------------

## RE-043.4 — Personal Capacity Facts: stale wiring claim corrected in module docstring

Armando asked what the "Personal Capacity operativo real: 45-50%"
snapshot figure originally meant, which led to reading
`engine/personal_capacity_facts_gate.py` in full. Its header docstring
still said "Still not wired into run.py, DecisionEngine or
gate_combination.py" -- true when written under RE-032.5 (the gate's
first isolated version, before any integration existed), but stale
since RE-040.1: `engine/posture_mapper.py`'s
`personal_capacity_facts_to_gate_input()` and `evaluate_capital_posture()`
translate a `PersonalCapacityFactsGateResult` into a
`GateCombinationInput` and feed it into `gate_combination.py`'s
`combine_gate_outputs()` -- the same `min()` combination Evidence
Quality and Regime Comparability go through. RE-043.1 then wired real
data into that path, and `audit_posture.py` exercises it end-to-end on
every run. Two changelog entries later (RE-040.1, RE-043.1) never
updated the original module docstring that said otherwise.

Fix: the docstring now states the gate is wired into
`gate_combination.py` (via `posture_mapper.py`, since RE-040.1) and
names the exact functions. The only claim that remains true and
unchanged is "not wired into run.py or DecisionEngine" -- still
accurate, still deliberate.

What this does not authorize:

-   No change to `PersonalCapacityFactsGate`'s logic, `FIELD_INPUT_TYPES`,
    or any threshold -- documentation only.
-   No change to `posture_mapper.py` or `gate_combination.py`.
-   No wiring into `run.py` or `DecisionEngine` -- that claim was, and
    remains, correct.

Boundary:

-   One file modified: `engine/personal_capacity_facts_gate.py`
    (module docstring only).
-   `tests/verify_personal_capacity_facts_gate.py` re-run unchanged:
    `PERSONAL CAPACITY FACTS GATE : STABLE`, same AMS `adequate` /
    AML `constrained` (`liquidity_adequate`) results as before.
-   No Frozen Core component touched.
-   Does not resolve, and was not intended to resolve, whether the
    Honest Progress Snapshot's 45-50% figure should change -- that is
    a separate, still-open decision, deliberately not made in this
    iteration.

------------------------------------------------------------------------

## RE-041.1 (code) — Dry Powder Protocol: first isolated module

RE-041.1 had specification but zero code (60-65% especificación / 0%
código per the Honest Progress Snapshot). This iteration adds
`engine/dry_powder_protocol.py` and `tests/verify_dry_powder_protocol.py`
implementing the four rules exactly as specified: tranche sized on
remaining Dry Powder (asymptotic decay, not on the initial amount),
dual cadence (days OR drawdown points, either one is enough), a
per-posture cumulative ceiling expressed as a fraction of the
episode's *initial* Dry Powder, and the ratchet (effective ceiling
never drops back down when posture does, only resets on a new
episode). v1 parameters unchanged from the governance text: Deploy
Partially — 12% tranche, 40% ceiling, 30 days OR 5.0pp cadence; Deploy
Aggressively — 22% tranche, 80% ceiling, 14 days OR 5.0pp cadence.
Beyond 80%: blocked unless `human_approval_above_ceiling` is set, in
which case the module authorizes the *state* but explicitly returns
`authorized_amount = None` rather than computing a number — v1 never
deploys the last fraction of Dry Powder by formula alone.

Armando handed over a fully detailed implementation spec for this
module (dataclasses, constants, five-step evaluation order, required
test scenarios). Two deviations from that spec were flagged to him
before any code was written, and confirmed ("Tú tienes el control. Ok
a las dos correcciones"):

1.  The spec's step 2 (ceiling/ratchet determination) used a two-branch
    literal check: "if highest reached was Aggressively, ceiling is
    80%; otherwise if current is Partially, ceiling is 40%." This
    leaves one real case undefined — the first evaluation right after
    escalating to Deploy Aggressively, if the caller has not yet
    updated `highest_posture_in_episode` to reflect that. Neither
    branch fires; `active_ceiling_pct` would be unset. Fixed by
    computing the effective ceiling posture as
    `max(current_posture, highest_posture_in_episode)` via
    `gate_combination.POSTURE_ORDER` — closes the gap, and is the more
    literal reading of RE-041.1's own text ("the highest one reached
    so far" — "so far" includes now). Caught a second, related bug
    while building this: `POSTURE_ORDER` does not rank `Blocked` at
    all (by design — it has no ordinal position, only a hard stop),
    so a naive `POSTURE_ORDER[posture]` lookup raises `KeyError` the
    first time `current_posture` or `highest_posture_in_episode` is
    `Blocked`. Fixed with a small `_posture_order()` helper that
    treats any unranked posture as lower than every real deployment
    posture, so it can never win the ratchet comparison.
2.  The spec used a Python `Enum` for the result status and
    `frozen=True` dataclasses throughout. Every other gate in this
    project (`EvidenceQualityGate`, `RegimeComparabilityGate`,
    `PersonalCapacityFactsGate`) represents discrete state as plain
    string module-level constants, and `gate_combination.py`'s own
    `POSTURE_ORDER` dict is keyed on those same plain strings — an
    `Enum` here would need `.value` unwrapping at every future
    integration point for no offsetting benefit. Kept plain strings
    for status; kept `frozen=True` on the inputs dataclass, a genuine,
    low-risk improvement that doesn't conflict with anything.

A third, smaller addition beyond the drafted spec, also flagged: the
two cadence fields (`days_since_last_deployment`,
`drawdown_pp_since_last_deployment`) are `Optional`, not required.
Forcing a caller to invent a sentinel (e.g. "9999 days") to represent
"no prior tranche exists yet in this episode" would itself be the kind
of magic-number shortcut this project's fail-closed discipline
rejects elsewhere. Both fields `None` means "first tranche of the
episode" and bypasses the cadence check explicitly, rather than
silently failing it.

The test suite covers, beyond the seven scenarios Armando's spec
listed by name: restrictive postures (Conserve/Prepare/**and**
Blocked, not just the two named), first-tranche-of-episode bypass,
cadence by time alone, cadence by drawdown alone, cadence blocked,
exact trim at the ceiling, the ratchet holding its ceiling after
posture drops back down, the undefined fresh-escalation branch from
correction 1 above, ceiling invaded with and without Human Approval,
and fail-closed rejection of an unrecognized posture string. All pass
on first run after the `Blocked`/`POSTURE_ORDER` fix.

What this does not authorize:

-   No wiring into `posture_mapper.py`, `gate_combination.py`,
    `run.py` or `DecisionEngine` — RE-041.1 explicitly reserves that
    for a future iteration.
-   No episode-state tracking. This module is stateless by design; it
    does not read market data, does not decide when an episode starts
    or ends, and does not compute any of its own inputs.
    `drawdown_engine.py` remains a historical episode-detection engine
    only, confirmed by direct read before this work started — it does
    not track a live/current episode either, so a future caller
    supplying this module's inputs still has that piece to build.
-   No automatic execution of any deployment. Human Approval
    (RE-032.4) still governs execution even once this module exists.
-   No claim the v1 percentages are final.
-   No change to the separate, still-undefined Portfolio Reallocation
    Protocol.
-   Under today's real Evidence Quality state (`not measurable`),
    combined posture cannot exceed `Prepare` — this protocol cannot
    trigger today regardless of drawdown depth. Forward infrastructure
    only, same as the specification itself already noted.

Boundary:

-   Two files added: `engine/dry_powder_protocol.py`,
    `tests/verify_dry_powder_protocol.py`.
-   No existing files modified.
-   No Frozen Core component touched.
-   `tests/verify_dry_powder_protocol.py` follows this project's
    existing `verify_*.py` / `assert_equal` / `main()` convention, not
    `pytest` — confirmed `pytest` is neither in `requirements.txt` nor
    installed in this sandbox, and none of the other 15 test files use
    it.
-   Structural verification only in this sandbox (pandas 2.3.3 / numpy
    2.2.6, not Armando's pinned 3.0.5 / 2.5.1) — this module has no
    pandas/numpy dependency at all (pure `dataclasses`/`typing`), so
    the runtime mismatch that blocks three other test files does not
    apply here. Full suite re-run after this change: no new failures
    beyond the three pre-existing, already-documented ones (runtime
    mismatch on `verify_baseline_harness.py`, `verify_secondary_baselines.py`,
    `verify_validation_metrics.py`; the `match_bottoms` tie-order
    artifact on `verify_research_engine.py`, unrelated to this or any
    prior change this session).

------------------------------------------------------------------------

## RE-041.2 — Live Episode Detector: the automatable half of Dry Powder Protocol's inputs

RE-041.1 (code) left `DryPowderProtocolInputs` entirely caller-supplied
-- no piece of the project could yet answer "is a drawdown episode
active right now, and since when." RE-041.2 closes exactly that piece,
no more: `engine/live_episode.py` (`detect_current_episode()`,
`run_live_episode_detector()`) plus `tests/verify_live_episode.py`.

Before writing this, the actual scope of "episode tracking en vivo"
was checked against what already exists, not assumed. Two things
became clear: (1) `drawdown_engine.py::detect_drawdowns()` only ever
returns CLOSED episodes -- an episode still in progress at the end of
the series is silently dropped, since the loop only appends on a
Drawdown == 0 recovery row. There was no existing code anywhere that
surfaces an unresolved, still-open episode. (2) Of the seven fields
`DryPowderProtocolInputs` needs, only two are honestly derivable from
market data alone: whether an episode is active, and its peak
date/price. The other five -- `initial_dry_powder`,
`remaining_dry_powder`, `cum_deployed_in_episode`,
`days_since_last_deployment`, `drawdown_pp_since_last_deployment`,
`highest_posture_in_episode` -- describe Armando's own liquidity and
his own past deployment decisions, none of which this system can
observe. Building a silent, invented ledger for those would have
violated this project's own stated principle ("el sistema está
pensado para generar evidencia explicable, no una caja negra").
Flagged to Armando before writing any code; he confirmed the split and
chose an xlsx tab (not a JSON state file) for that manual ledger, to
be designed in a following iteration.

`detect_current_episode(df)` deliberately does not call
`detect_drawdowns()` -- it mirrors the same state machine instead,
importing `MIN_DRAWDOWN`, `calculate_running_peak` and
`calculate_drawdown` from `drawdown_engine.py` rather than
redefining them, so both sides share one episode definition and
Frozen Core stays untouched (no edit to `drawdown_engine.py` itself).
Returns `None` if the latest data point is at/above its running peak
or in a dip shallower than `MIN_DRAWDOWN` (-10%); otherwise returns a
`CurrentEpisode` with the peak that started the episode, the deepest
point reached so far, and the as-of (latest) reading.

Checked directly against `data/raw/shiller.xlsx` before finalizing the
test: as of the latest row (2026.07), the market sits exactly at its
running peak (Drawdown 0.0) -- no episode is active today, consistent
with everything else this session. `verify_live_episode.py` asserts
this real-pipeline result explicitly (`None`), noted in the test
itself as an assertion that should correctly start failing the day a
real drawdown begins, not a canonical claim frozen in place.

What this does not authorize:

-   No ledger, no ability to answer `initial_dry_powder`,
    `cum_deployed_in_episode`, or the since-last-tranche fields --
    those remain entirely unbuilt, deferred to the manual-ledger
    iteration Armando has already scoped (xlsx tab).
-   No change to `drawdown_engine.py` (Frozen Core-adjacent, historical
    episode detection) -- only imported from, never edited.
-   No wiring into `dry_powder_protocol.py`, `posture_mapper.py`,
    `gate_combination.py`, `run.py` or `DecisionEngine`.
-   No claim about tomorrow -- this is a live, unstated function; every
    call re-derives the answer from the Shiller file as it stands, no
    caching, no persistence.

Boundary:

-   Two files added: `engine/live_episode.py`,
    `tests/verify_live_episode.py`.
-   No existing files modified.
-   No Frozen Core component touched.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones (three pinned-runtime mismatches, one
    `match_bottoms` tie-order artifact), unchanged from RE-041.1 code.

------------------------------------------------------------------------

## RE-041.3 — Dry Powder Ledger: file structure only, no code

RE-041.2 left five of `DryPowderProtocolInputs`' seven fields with no
source at all -- nothing in the system can observe Armando's real
liquidity or his own past deployment decisions. RE-041.3 adds exactly
one file, `data/raw/dry_powder_ledger.xlsx`, and no code: the manual
ledger Armando confirmed (xlsx tab, not JSON) after the file-placement
question was put to him directly.

Kept as a separate file from `personal_capacity_facts.xlsx` rather
than new tabs in it, per the same reasoning already flagged to
Armando: `personal_capacity_facts.xlsx` is a static snapshot (9 facts,
overwritten in place); this is an append-only log that grows with
every tranche ever executed. Same separation of concerns
`shiller.xlsx` (market) already has from `personal_capacity_facts.xlsx`
(capacity).

Structure, per patrimonio tab (AMS/AML, `Notas` reserved as usual):

-   Section 1, "Episodio actual" -- one marker row pair, filled only
    once an episode is confirmed active: start date (Shiller `AAAA.MM`
    format, must match `CurrentEpisode.peak_date` from
    `engine/live_episode.py`) and the episode's initial Dry Powder in
    euros. Both start as `Pendiente`, same placeholder token
    `personal_capacity_facts_gate.py` already treats as "not measured,"
    not as a false negative.
-   Section 2, "Registro de tramos desplegados" -- append-only, one row
    per tranche actually executed (money moved, not a decision on
    paper): date, amount deployed, posture in effect at that moment
    (data-validation dropdown restricted to `gate_combination.py`'s
    five posture constants, to cut transcription errors during a real
    market-stress moment), free note. Rows are never deleted or
    overwritten; a future episode's boundary is applied by filtering on
    date, not by clearing history.

Deliberately minimal what Armando has to type by hand: date, amount,
posture. Everything else RE-041.1's protocol needs --
`drawdown_pp_since_last_deployment`, `days_since_last_deployment`,
`cum_deployed_in_episode`, `remaining_dry_powder` -- is meant to be
derived later by joining these dated rows against Shiller data, not
entered as separate manual fields. That derivation is not built yet;
this iteration is the file only, per the one-file-per-iteration
discipline this session has followed throughout.

What this does not authorize:

-   No loader, no adapter, no `build_local_dry_powder_ledger_inputs()`
    equivalent -- nothing in the codebase reads this file yet.
-   No wiring into `dry_powder_protocol.py` or anything downstream.
-   No real episode or tranche data entered -- both patrimonios'
    Section 1 read `Pendiente`, Section 2 has no rows, because as of
    RE-041.2 no episode is active and nothing has been deployed.

Boundary:

-   One file added: `data/raw/dry_powder_ledger.xlsx`.
-   No code files touched.
-   No Frozen Core component touched.
-   Structural verification only: reopened with `openpyxl` and
    confirmed sheet names, section headers and placeholder values match
    what was written.

------------------------------------------------------------------------

## RE-041.4 — Dry Powder Ledger adapter: joins live episode detection with the manual ledger

RE-041.4 closes the piece RE-041.2/RE-041.3 deliberately left apart:
`engine/dry_powder_ledger_state.py`
(`compute_ledger_episode_state()`, `build_local_dry_powder_ledger_state()`)
plus `loaders/dry_powder_ledger_loader.py` and
`tests/verify_dry_powder_ledger_state.py`. Given
`data/raw/dry_powder_ledger.xlsx` and today's live market state
(`engine/live_episode.py`), it produces `LedgerEpisodeState` per
patrimonio: `has_active_episode`, `initial_dry_powder`,
`remaining_dry_powder`, `cum_deployed_in_episode`,
`days_since_last_deployment`, `highest_posture_in_episode`, and
explanations.

Deliberately does not produce a ready-to-evaluate
`DryPowderProtocolInputs`. `current_posture` and
`human_approval_above_ceiling` belong to the combined-gate pipeline and
Human Approval respectively -- this module has no business computing
either, and doesn't. A future caller merges this module's output with
those two separately-sourced values.

One small, low-risk correction to the already-shipped RE-041.3 file
before writing this: Section 2's column-A header read "Fecha (AAAA.MM.DD
o AAAA.MM)," which conflated two genuinely different clocks --
`days_since_last_deployment` needs a real calendar date,
`drawdown_pp_since_last_deployment` needs Shiller's monthly cadence.
Corrected to "Fecha (calendario real, AAAA-MM-DD)" before any real data
existed to be affected (both patrimonios' Section 2 were still empty).
Flagged to Armando before touching the file; confirmed.

Two fail-closed judgment calls, made explicit rather than buried in
code: (1) if the ledger's Section 1 marker is missing or its start
date doesn't match the live-detected episode's peak, `initial_dry_powder`
is treated as unknown -- never falls back to a stale figure from a
different episode. (2) if no tranche has been logged yet for the
current episode, `highest_posture_in_episode` defaults to `Conserve`,
so `dry_powder_protocol.py`'s own ratchet grants no unearned benefit
until a tranche is actually logged at a higher posture.

Scoped explicitly, not silently shipped partial:
`drawdown_pp_since_last_deployment` is NOT computed this iteration.
Doing so correctly requires a month-level lookup against the full
prepared Shiller series for the last tranche's date, not just the
terminal snapshot `CurrentEpisode` exposes -- a real feature, deferred
to its own iteration. Its absence is safe: RE-041.1's cadence check is
days OR drawdown-points, so cadence can still be satisfied on days
alone; this field being `None` never blocks or wrongly authorizes
anything.

Tranche dates belonging to the current episode are filtered by
converting each real calendar date to Shiller's `AAAA.MM` month and
comparing against the episode's start month -- a month-level boundary,
not day-level, an inherent consequence of Shiller's monthly cadence,
documented rather than glossed over.

Checked directly against the real files before finalizing the test:
both AMS and AML currently report `has_active_episode=False`,
consistent with RE-041.2's finding that the market sits at its running
peak today.

What this does not authorize:

-   No `DryPowderProtocolInputs` assembly, no wiring into
    `dry_powder_protocol.py`, `posture_mapper.py`, `gate_combination.py`,
    `run.py` or `DecisionEngine`.
-   No `drawdown_pp_since_last_deployment` computation -- explicitly
    deferred, not silently skipped.
-   No real episode or tranche data entered into the ledger -- this
    iteration is adapter code only.

Boundary:

-   Two files added: `loaders/dry_powder_ledger_loader.py`,
    `engine/dry_powder_ledger_state.py`.
-   One test file added: `tests/verify_dry_powder_ledger_state.py`.
-   One existing file corrected (not authored fresh):
    `data/raw/dry_powder_ledger.xlsx` -- Section 2 header wording only,
    no data changed (none existed).
-   No Frozen Core component touched.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones.

------------------------------------------------------------------------

## RE-041.5 — Dry Powder Protocol wired into the audit dry-run (still not into run.py)

RE-041.5 closes the assembly step explicitly deferred in RE-041.4:
`engine/dry_powder_ledger_state.py::to_dry_powder_protocol_inputs()`
merges a `LedgerEpisodeState` with a caller-supplied `current_posture`
and `human_approval_above_ceiling` (default `False`, never assumed
`True`) into a real `DryPowderProtocolInputs`. Returns `None` -- not a
guessed value -- when there's nothing meaningful to evaluate: no
active episode, or an active episode whose ledger isn't resolved yet.

`audit_posture.py` now calls this per patrimonio, using the same
`combined.posture_ceiling` it already prints from
`evaluate_capital_posture()`, and evaluates the result through
`DryPowderProtocol().evaluate()` when assembly succeeds. Run against
the real files today: both AMS and AML print "not evaluated" with
RE-041.2's own explanation ("no active market episode detected"),
because no episode is active -- the value of this iteration is that
the full chain (live episode detection -> ledger -> combined posture
-> protocol evaluation) is now demonstrated end-to-end in one script,
not that it produces a number today.

This is still the same read-only dry-run `audit_posture.py` has been
since RE-039.1 -- not a new decision surface. Nothing about `run.py`,
`DecisionEngine`, or automatic execution changes.

What this does not authorize:

-   No wiring into `run.py` or `DecisionEngine` -- `audit_posture.py`
    remains a standalone, read-only CLI.
-   No change to `human_approval_above_ceiling`'s default -- always
    `False` here, since Human Approval (RE-032.4) still has no code.
-   No change to `drawdown_pp_since_last_deployment`'s RE-041.4 gap --
    still `None`, still safe, still deferred.

Boundary:

-   One file extended: `engine/dry_powder_ledger_state.py`
    (`to_dry_powder_protocol_inputs()` added).
-   One test file extended: `tests/verify_dry_powder_ledger_state.py`.
-   One file extended: `audit_posture.py` (per-patrimonio Dry Powder
    Protocol dry-run printout added).
-   No Frozen Core component touched.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones. `audit_posture.py` re-run directly and confirmed
    to print the expected "not evaluated" result for both patrimonios
    under today's real data.

------------------------------------------------------------------------

## RE-041.6 — Dry Powder Ledger: "Activo / Instrumento" column, catching a real Section 1 misreading

While reviewing RE-041.3's ledger, Armando caught something real: the
file had no place to record WHAT was actually bought, only the amount
deployed. Confirmed this is correctly optional for the protocol
itself -- `dry_powder_protocol.py`'s math never needs to know the
instrument, only how much came out of Dry Powder and when -- but it is
real audit value the ledger should still capture, same spirit as the
project's "evidencia explicable, no caja negra" principle.

Same exchange also surfaced a genuine misreading of Section 1 worth
recording: Armando's first read was that the episode-start date is
"the day the system happens to detect it" (i.e. today, whenever he
runs the check). Corrected: it is `CurrentEpisode.peak_date` from
`engine/live_episode.py` -- the market's last high before the
drawdown began, ordinarily a date in the past relative to whenever
he's filling the cell in, not today's date. Getting this wrong would
silently break RE-041.4's exact-match consistency check (ledger start
vs. live-detected peak) the first time it mattered.

Added "Activo / Instrumento" as a new column E in Section 2 of
`data/raw/dry_powder_ledger.xlsx` (both AMS/AML), appended after Nota
rather than inserted in the middle -- Section 1 shares columns A-D by
row position with Section 2's original four columns, and reordering
would have forced a width change on column D that Section 1's longer
"Nota" text didn't need. `loaders/dry_powder_ledger_loader.py` now
reads it into each tranche dict as `"activo"`. Not consumed by
`engine/dry_powder_ledger_state.py`'s calculations -- record-keeping
only, exactly as scoped.

What this does not authorize:

-   No change to any computed field -- `cum_deployed_in_episode`,
    `highest_posture_in_episode`, etc. are unaffected; `activo` is
    read and stored, never used in arithmetic or posture logic.
-   No real episode or tranche data entered -- still Pendiente/empty.

Boundary:

-   One file corrected: `data/raw/dry_powder_ledger.xlsx` (new column
    only, no data).
-   One file extended: `loaders/dry_powder_ledger_loader.py`.
-   No Frozen Core component touched.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones.

------------------------------------------------------------------------

## RE-041.7 — drawdown_pp_since_last_deployment closed

Closes the gap RE-041.4 explicitly deferred. `engine/live_episode.py`
gains two small additions: `load_prepared_shiller_df()` (extracted
from `run_live_episode_detector()`, no logic change, so a caller can
get the full prepared series rather than just the terminal
`CurrentEpisode` snapshot) and `drawdown_at_month(df, target_month)`
(the market `Drawdown` at the most recent Shiller row on or before a
given `AAAA.MM` month, `None` if before the series' start).

`engine/dry_powder_ledger_state.py::compute_ledger_episode_state()`
gains an optional `shiller_df` parameter. When supplied, it looks up
the market drawdown at the last tranche's month and computes
`drawdown_pp_since_last_deployment` as `(drawdown_then -
as_of_drawdown) * 100`, clamped at `0.0`. The clamp is the real
substance of this iteration, not a formality: a partial market
recovery since the last tranche makes this difference negative, and a
negative number of "additional drawdown points" would be nonsensical
-- worse, if left unclamped it would silently work anyway inside
`dry_powder_protocol.py`'s `>=` cadence check (a negative number never
clears a positive threshold), which is exactly the kind of
accidentally-correct-but-unprincipled result this project's discipline
exists to catch before it ships, not tolerate because it happens not
to bite today. `build_local_dry_powder_ledger_state()` now loads the
Shiller series once per call and reuses it for both live episode
detection and this lookup -- no double read.

Backward compatible: `shiller_df` defaults to `None`, in which case
behaviour is exactly RE-041.4's (field left unset, explanation
recorded) -- no existing caller breaks.

What this does not authorize:

-   No wiring into `run.py`, `DecisionEngine`, `audit_posture.py`'s
    call site needed no changes (it already calls
    `build_local_dry_powder_ledger_state()`, which now supplies the
    Shiller series internally).
-   No change to the cadence rule itself (days OR drawdown-points) --
    this iteration only makes the second leg computable, doesn't
    change how it's used.

Boundary:

-   Two files extended: `engine/live_episode.py`,
    `engine/dry_powder_ledger_state.py`.
-   One test file extended: `tests/verify_dry_powder_ledger_state.py`
    (new synthetic Shiller-series cases, both the deepening and
    clamped-recovery sign cases). Also fixed a latent bug in that same
    test file unrelated to this iteration's logic: an assertion
    hardcoded `date(2026, 8, 10)` as "today" while separately relying
    on `date.today()` -- broke the moment a real day passed (caught
    while running this iteration's tests, one day after RE-041.6
    shipped). Fixed by passing a fixed `as_of_calendar_date` explicitly
    instead of depending on the real clock.
-   No Frozen Core component touched.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones. One unrelated environment issue hit during this
    session's verification and noted, not fixed here:
    `data/raw/personal_capacity_facts.xlsx` was locked by the sandbox's
    iCloud mount (`OSError: Resource deadlock avoided` /
    `BadZipFile`) -- same class of issue as the `.git/index.lock`
    problem documented earlier in this project's history, unrelated to
    any file this iteration touched, expected to clear on Armando's
    own machine.

## RE-041.8 — Dry Powder Ledger: unrecognized postura now leaves a trace

Correctness fix, found by Armando in a second cold critical review he
explicitly requested of the entire day's work (RE-041.x and RE-032.x
together), after RE-032.9 had already closed the first finding from
that review.

The bug: in `compute_ledger_episode_state()`, a tranche row with a
valid `fecha` and `importe` but a missing or unrecognized `postura`
("Pendiente", a typo, an empty cell) was silently excluded from the
`highest_posture_in_episode` computation -- no entry in `explanations`,
nothing to tell Armando it happened. This is inconsistent with the
same loop's handling of `fecha` and `importe`, both of which already
produce an explicit skip-explanation when malformed, and it directly
contradicts `human_approval_state.py`'s own docstring claim of
applying "the same discipline ... already applies to malformed tranche
rows" -- on inspection, that claim was not actually true for postura.
Operational consequence: a tranche that genuinely pushed the episode
to a higher posture, but whose postura cell was left unfilled or
mistyped, would leave the ratchet ceiling silently wrong, with no
visible warning.

Fix: `importe` still counts toward `cum_deployed_in_episode` exactly
as before -- the money was really deployed regardless of whether the
posture that justified it was legibly recorded, so discarding the row
would have been the wrong fix. What changed is that an unrecognized or
missing `postura` now appends an explanation naming the amount and the
unrecognized value, instead of updating nothing and saying nothing.

Deliberately NOT given the same shape as
`human_approval_state.py`'s handling of an unrecognized postura, which
skips the whole row: that is correct there because an attestation IS
its posture -- with nothing else meaningful to keep if it doesn't
resolve. A tranche is a real deployment of money whether or not its
posture field was filled in correctly; mirroring Human Approval's
row-skip here would have silently dropped real deployed capital from
`cum_deployed_in_episode`; a materially worse outcome than the
explanation gap it would have replaced.

Boundary:

-   One file changed: `engine/dry_powder_ledger_state.py`.
-   One file extended: `tests/verify_dry_powder_ledger_state.py` (one
    new case: valid fecha/importe, unrecognized postura -- importe
    still counted, highest_posture_in_episode unaffected by the bad
    row, explanation present).
-   No Frozen Core component touched.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones.

------------------------------------------------------------------------

## RE-032.6 — Human Approval: first isolated code

RE-032.4 fully specified the attested-judgement channel and Human
Approval's procedural mechanics with no code (states, 90-day validity,
14/30-day cooling-off, market_crisis/personal_crisis). RE-032.6 is the
first code against that spec: `engine/human_approval.py`
(`HumanApprovalGate.evaluate()`) plus `tests/verify_human_approval.py`.
Pure logic, no I/O, no storage -- same split as every other gate this
project has built.

Translating RE-032.4's prose into code surfaced a real contradiction
in the governance doc's own text, plus one genuine gap, both resolved
with Armando directly before writing anything:

1.  Rules 5 and 7 conflict as literally written. Rule 5:
    `under_cooling_off` blocks all capital action. Rule 7: "the
    previously valid attestation remains in force" during cooling-off
    -- which implies action CAN proceed, just under the old terms.
    Resolved (Armando's formulation): cooling-off delays the
    *effectiveness* of a tolerance-increasing revision; it never
    invalidates a prior, still-valid attestation. The top-level state
    stays `valid` (governed by the predecessor) with the pending
    revision surfaced separately as `pending_increase`, whenever a
    valid predecessor exists. `under_cooling_off` as a blocking
    top-level state is reserved for when there is no valid predecessor
    to fall back on.
2.  A first-ever attestation is measured against an implicit baseline
    equivalent to `Conserve` -- no attestation is treated the same as
    having attested to nothing but the floor. A first attestation
    authorizing anything above `Conserve` is itself a tolerance
    increase and goes through the same cooling-off as any revision; at
    or below `Conserve` (a tie counts as a decrease, per rule 6) takes
    effect immediately.

`market_crisis` is deliberately not recomputed here -- it is exactly
`engine.live_episode`'s existing `Drawdown <= MIN_DRAWDOWN` check
(RE-041.2), so duplicating that threshold inside Human Approval would
have violated this project's own repeated anti-duplication discipline.
Each `Attestation` instead carries `market_crisis_at_registration: bool`,
a fact about conditions the day that specific attestation was
registered -- left for a future adapter to resolve via
`engine.live_episode.drawdown_at_month()`, the exact primitive
RE-041.7 built yesterday for an unrelated purpose and now reusable
here. Cooling-off length for a revision is fixed by conditions at ITS
OWN registration, not re-evaluated live on every check -- stated as a
readable-but-open interpretation, not a certainty.

What this does not authorize:

-   No storage schema, no attestation form, no
    `data/raw/human_approval_attestations.xlsx` -- Armando has already
    agreed to a per-patrimonio xlsx (same tab-per-patrimonio pattern as
    `personal_capacity_facts.xlsx`/`dry_powder_ledger.xlsx`, not a
    `patrimony` column on a flat table) for a following iteration; not
    built yet.
-   No wiring into `gate_combination.py`, `posture_mapper.py`,
    `run.py` or `DecisionEngine`. Human Approval is explicitly not a
    scored gate (RE-032.4 rule 1) and never participates in
    `combine_gate_outputs()`'s `min()` combination -- it is checked
    separately as a binary procedural prerequisite, a distinction this
    module's docstring restates rather than assumes obvious.
-   Does not resolve `personal_crisis` under-reporting -- still an
    accepted, documented limitation (RE-032.4), not solved.

Boundary:

-   Two files added: `engine/human_approval.py`,
    `tests/verify_human_approval.py`.
-   No existing files modified.
-   No Frozen Core component touched.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones. One unrelated, still-unresolved sandbox
    environment issue: `data/raw/personal_capacity_facts.xlsx` remains
    locked by the iCloud mount (`BadZipFile`/`Resource deadlock
    avoided`) as of this iteration -- unrelated to any file touched
    here, expected to clear on Armando's own machine per the same
    class of issue already documented under RE-041.7.

------------------------------------------------------------------------

## RE-032.7 — Human Approval: real attestation ledger + adapter

Closes the storage/adapter gap RE-032.6 explicitly deferred.
`data/raw/human_approval_attestations.xlsx` (new file, AMS/AML/Notas
tabs, same style as `dry_powder_ledger.xlsx`) is the manual event log
Armando confirmed: one row per attestation, columns limited to what
only he can know -- date, approved posture ceiling (dropdown), whether
a personal crisis was declared that day, a note. No expiry, no
cooling-off state, no "is this valid" column -- per Armando's own
caution, the xlsx records facts, the code computes state.

Two new files do the interpretation: `loaders/human_approval_loader.py`
(raw I/O, same per-patrimonio-tab convention as every loader this
project has) and `engine/human_approval_state.py`
(`build_local_human_approval_inputs()`), which resolves
`market_crisis_at_registration` for each row -- not typed by
Armando -- by converting the row's real calendar date to Shiller's
month and checking `Drawdown <= MIN_DRAWDOWN` at that point, RE-032.4's
own literal definition, reusing `engine.live_episode.drawdown_at_month()`
(RE-041.7) rather than a second copy of that threshold check.

Two small refactors done in service of this, both pure extractions, no
logic change, verified against the existing test suite before
proceeding: `engine.live_episode.calendar_date_to_shiller_month()`
(previously a private copy inside `dry_powder_ledger_state.py`) and a
new `engine/manual_entry_parsing.py`
(`to_float_or_none()`/`to_calendar_date_or_none()`, the
"Pendiente"-aware cell parsing every manual-entry adapter in this
project needs) -- `dry_powder_ledger_state.py` now imports both rather
than keeping its own copies. Consistent with the anti-duplication
discipline Armando himself invoked earlier this session for
`market_crisis`.

Fail-closed on malformed rows: an unparseable date or an unrecognized
posture string is skipped with a printed explanation, never guessed --
same discipline `dry_powder_ledger_state.py` already applies to
malformed tranche rows.

What this does not authorize:

-   No wiring into `gate_combination.py`, `posture_mapper.py`,
    `run.py`, `DecisionEngine`, or `audit_posture.py` -- Human Approval
    remains unconnected to any decision surface, and RE-032.4 rule 1
    (not a scored gate, never blended into a posture ceiling) still
    has no code path exercising it anywhere.
-   No real attestation data entered -- both AMS and AML start empty;
    `HumanApprovalGate.evaluate()` against today's real file correctly
    returns `MISSING`, `blocked=True` for both.

Boundary:

-   One file added: `data/raw/human_approval_attestations.xlsx`.
-   Three files added: `loaders/human_approval_loader.py`,
    `engine/human_approval_state.py`,
    `engine/manual_entry_parsing.py`.
-   One test file added: `tests/verify_human_approval_state.py`.
-   One file refactored (extraction only):
    `engine/dry_powder_ledger_state.py`.
-   One file extended (extraction only): `engine/live_episode.py`
    (`calendar_date_to_shiller_month()`).
-   No Frozen Core component touched.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones, plus the still-unresolved
    `personal_capacity_facts.xlsx` sandbox iCloud lock noted under
    RE-032.6, persisting into this iteration -- unrelated to any file
    touched here.

------------------------------------------------------------------------

## RE-032.8 — Human Approval wired into the audit dry-run

`audit_posture.py` now prints Human Approval's state per patrimonio,
using `build_local_human_approval_inputs()` against the real
`data/raw/human_approval_attestations.xlsx`. Run today: `missing`,
blocked, for both AMS and AML -- expected, since the ledger has no
attestations yet.

The one design decision worth recording: this is printed as a block
completely separate from `COMBINED posture ceiling`, never blended
into it, and not fed into `to_dry_powder_protocol_inputs()`'s
`human_approval_above_ceiling` parameter either. Two distinct reasons:

-   RE-032.4 rule 1 states plainly that Human Approval is not a scored
    gate and never participates in `evaluate_capital_posture()`'s
    `min()` combination -- printing it inside `COMBINED` would
    misrepresent the governance model this project has already
    committed to. The two are independent prerequisites: the combined
    ceiling says what the evidence permits; Human Approval says,
    separately, whether there is current human consent to act at all.
-   `human_approval_above_ceiling` is a narrower, more specific
    authorization (RE-041.1: explicitly clearing the 80% Dry Powder
    ceiling), not the same question as "is there a valid attestation
    at all." Mapping `HumanApprovalResult.blocked` onto that parameter
    would have invented a rule that doesn't exist anywhere in RE-032.4
    or RE-041.1's text -- left at `False`, unchanged from RE-041.5,
    rather than guessed.

What this does not authorize:

-   No wiring into `run.py` or `DecisionEngine`.
-   No change to `human_approval_above_ceiling`'s value or meaning.
-   No blending of Human Approval into `combine_gate_outputs()` or
    `evaluate_capital_posture()`.

Boundary:

-   One file extended: `audit_posture.py`.
-   No Frozen Core component touched.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones. The `personal_capacity_facts.xlsx` sandbox
    iCloud lock noted under RE-032.6/RE-032.7 has cleared as of this
    iteration.

## RE-032.9 — Human Approval: chain-resolution correctness fix

Not a new capability -- a correctness fix on RE-032.6's core logic,
found by Armando in a deliberate critical re-read of the day's work he
explicitly requested ("hacemos la 1 y la 3 ahora"), not caught while
either of us was designing the original version.

The bug: `HumanApprovalGate.evaluate()` decided whether the latest
attestation was a tolerance INCREASE by comparing it only against
`attestations[-2]` -- the raw immediately preceding row -- rather than
against whatever was actually in force. That is wrong whenever the
immediate predecessor never itself took effect (e.g. it was still
mid cooling-off when superseded). Concrete bypass: attest Conserve
(day 0, effective immediately); in a bad moment attest Deploy
Aggressively (day 1, enters 14-day cooling-off, never clears); attest
Deploy Partially (day 2). Compared only against the raw previous row
(Aggressively), Partially reads as a DECREASE and would apply
immediately with zero cooling-off -- even though, compared against
what was truly governing (Conserve, since Aggressively never took
effect), Partially is a real increase that must go through its own
cooling-off. This is precisely the self-gaming pattern (revising
tolerance upward during an emotional moment) the whole mechanism
exists to prevent, reopened by an implementation detail rather than a
design gap.

Fix: a new `_resolve_effective(attestations, as_of_date)` walks the
full chronological history and simulates, step by step, what was
ACTUALLY in force at each attestation's own registration moment --
folding in both cooling-off and the 90-day validity window at every
step, not only for the latest entry. `evaluate()` now computes
`fallback = _resolve_effective(attestations[:-1], as_of_date=latest.registered_at)`
and uses `fallback` everywhere the old two-row lookback (`previous`)
was used: as the baseline for the increase/decrease comparison, and as
the governing posture during a pending increase's cooling-off.

Verified two ways:

-   Manually re-traced against all ten pre-existing test cases in
    `tests/verify_human_approval.py` -- every one produces the same
    result under the new logic (the fix changes behavior only when a
    predecessor never itself took effect, which none of the original
    cases exercised).
-   Added two new adversarial cases reproducing the exact bypass
    above: `bypass_attempt` (Conserve → Aggressively-never-clears →
    Partially, checked the same day) now correctly resolves to `VALID`
    governed by Conserve with Partially parked as `pending_increase`,
    not applied immediately; `bypass_cleared` (same three
    attestations, checked 14 days after Partially's own registration)
    resolves to `VALID` with Partially now in effect on its own
    merits -- confirming the fix delays Partially by its OWN
    cooling-off clock, never borrows or resets against Aggressively's.

No change to the public interface -- `HumanApprovalResult`,
`PendingIncrease`, `HumanApprovalInputs`, `Attestation` all unchanged.
`engine/human_approval_state.py` and `audit_posture.py` required no
changes.

Boundary:

-   One file changed: `engine/human_approval.py` (`_still_valid()` and
    `_resolve_effective()` added; `evaluate()`'s baseline logic
    refactored to use them).
-   One file extended: `tests/verify_human_approval.py` (two new
    adversarial cases).
-   No Frozen Core component touched.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones.

## RE-032.10 — Human Approval: authorizes_dry_powder_ceiling_90 (iteration A, pure logic)

Closes a gap `audit_posture.py` already documented honestly at
RE-032.8, rather than papering over it: `dry_powder_protocol.py`'s
`CEILING_REACHED_APPROVED` status has always required "a fresh Human
Approval attestation" to unlock deployment beyond `Deploy
Aggressively`'s 80% ceiling (RE-041.1), but neither the xlsx nor
`Attestation` ever had anywhere to actually record that authorization
-- `human_approval_above_ceiling` has been hardcoded `False` in
`audit_posture.py` since RE-041.5, deliberately, rather than inventing
a mapping that didn't exist. Armando raised this himself while
reviewing the manual operativo draft for Dry Powder Protocol, and the
full design was negotiated point by point before any code was written
-- same discipline as RE-032.4's original contradictions.

Design, agreed in full before writing this iteration:

1.  Authorizes ampliar el techo de `Deploy Aggressively` del 80% al
    90% de la pólvora seca inicial del episodio -- never 100%, never a
    fixed euro amount. `dry_powder_protocol.py` computing tranches up
    to this new 90% is explicitly deferred to a separate iteration (C,
    below) -- this iteration only produces the boolean that will
    unlock it.
2.  Lives on the SAME attestation row as the posture it depends on
    (`Attestation.authorizes_dry_powder_ceiling_90: bool = False`),
    not a separate registry -- an extension of that specific Human
    Approval, not a new protocol. Only meaningful when that row's
    `approved_posture_ceiling` is `Deploy Aggressively`.
3.  Always a fixed 30-day cooling-off of its own
    (`COOLING_OFF_CEILING_90_DAYS`), deliberately independent of the
    base posture's own 14/30-day cooling-off, even though both equal
    30 under a crisis today -- exceeding the hardest ceiling in the
    system gets maximum friction by default, not whatever friction the
    underlying posture increase happened to need.
4.  Can be registered pre-emptively -- before the 80% ceiling is
    reached, even before any episode is active -- confirmed explicitly
    as the intended use: the 30-day wait should already be paid down
    in a calm moment, not started reactively exactly when a real
    crisis is already underway (the worst possible time to have to
    wait).
5.  Deliberately does NOT know anything about market episodes.
    `registered_at >= episode.peak_date` was considered and rejected
    as a v1 filter: it would have broken point 4 (an attestation made
    before an episode existed would never satisfy "on or after the
    episode's peak"), and it would have given Human Approval a market
    dependency it has never had. "Only usable while an episode is
    actually active" is already guaranteed for free by
    `dry_powder_protocol.py`'s own call structure -- it only ever runs
    when `to_dry_powder_protocol_inputs()` has produced real inputs,
    which itself requires an active, ledger-resolved episode. If
    scoping to a *specific* episode is ever needed, that gets an
    explicit episode field later, not a date inference now -- not
    built ahead of an observed need.
6.  Can never be in effect before the base posture it depends on --
    guaranteed structurally (only ever checked against whichever
    attestation `evaluate()` has already established as the one
    actually governing the base posture, never a still-pending one)
    and arithmetically (30 days can never be less than the 14-or-30
    the base itself required, since both clocks share the same
    `registered_at`). Expires with its own attestation -- gone the
    moment that row falls outside the 90-day validity window, same as
    everything else on it.

Implementation: `_ceiling_90_active(attestation, as_of_date)` checks
the flag, the `Deploy Aggressively` posture requirement, and the
30-day clock in one place; called from every branch of `evaluate()`
against whichever attestation (`latest` or `fallback`) that branch has
already established as effective -- never against a pending one, so
point 6's structural guarantee is enforced by construction, not by
convention.

Four acceptance checks, agreed with Armando before coding, each with
its own test case in `tests/verify_human_approval.py`:

-   Doesn't apply if the governing posture isn't `Deploy Aggressively`,
    even with the flag set on the row (`ceiling_90_wrong_posture`).
-   Never active while the base posture itself is still pending,
    governed by a fallback instead (`ceiling_90_while_base_pending`).
-   Always needs its own 30 days, even once the base posture has
    cleared a shorter 14-day cooling-off
    (`ceiling_90_base_cleared_but_not_own` /
    `ceiling_90_both_cleared`).
-   Expires with its own attestation, past the 90-day validity window
    (`ceiling_90_expired`).

What this does not authorize:

-   No change to `dry_powder_protocol.py` -- it still always returns
    `authorized_amount=None` for `CEILING_REACHED_APPROVED`. Computing
    up to 90% by formula is iteration C, not this one.
-   No change to `data/raw/human_approval_attestations.xlsx`, the
    loader, or `human_approval_state.py` -- no way to actually set this
    flag from real data yet. That is iteration B.
-   No change to `audit_posture.py` -- `human_approval_above_ceiling`
    stays hardcoded `False`, unchanged, until iteration C wires it to
    this field for real.
-   No manual operativo update -- explicitly deferred to iteration D,
    once the capability is real end-to-end, not before.

Boundary:

-   One file changed: `engine/human_approval.py`
    (`authorizes_dry_powder_ceiling_90` added to `Attestation` and
    `HumanApprovalResult`; `COOLING_OFF_CEILING_90_DAYS` constant;
    `_ceiling_90_active()` helper; every `evaluate()` branch updated).
-   One file extended: `tests/verify_human_approval.py` (four new
    cases).
-   No Frozen Core component touched.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones.

------------------------------------------------------------------------

## RE-032.10 iteration B — Excel + loader/adapter for authorizes_dry_powder_ceiling_90

Closes the gap iteration A left open on purpose ("no way to actually
set this flag from real data yet"). Mechanical, same shape every other
manual-entry column in this project already follows.

Changes:

-   `data/raw/human_approval_attestations.xlsx` -- new column E on both
    `AMS` and `AML` tabs, `"Autoriza techo 90% (solo si Deploy
    Aggressively)"`, styled identically to the existing headers (same
    font/fill/alignment as the `Nota` header), `Sí`/`No` dropdown
    validation on `E5:E19` matching `Crisis personal declarada`'s
    existing pattern. Explanatory block added to the `Notas` tab,
    matching that sheet's existing style, spelling out the 80%→90%
    scope, the 30-day independent cooling-off, and that it applies to
    no other ceiling.
-   `loaders/human_approval_loader.py` -- reads column 5 into
    `"autoriza_techo_90"`. Raw load only, same as every other field
    this loader returns -- no interpretation.
-   `engine/human_approval_state.py` -- `_to_bool_crisis_declared`
    renamed to `_to_bool_si_no` (it never actually cared which field it
    was parsing) and reused for the new column, rather than writing a
    second copy of the same Sí/No parsing rule. The parsed boolean is
    passed into `Attestation.authorizes_dry_powder_ceiling_90`
    unconditionally -- even for a row whose posture isn't `Deploy
    Aggressively`. Whether that matters is
    `engine.human_approval._ceiling_90_active()`'s decision alone (it
    already checks the posture); duplicating that check in the adapter
    would be the same rule enforced in two places.

What this does not authorize:

-   No change to `dry_powder_protocol.py` or `audit_posture.py` -- that
    is iteration C, done together with this one in the same session but
    recorded as its own decision below.
-   No real data entered -- both xlsx tabs remain empty (no attestation
    has ever been registered for either patrimonio).

Boundary:

-   Three files changed: `data/raw/human_approval_attestations.xlsx`,
    `loaders/human_approval_loader.py`, `engine/human_approval_state.py`.
-   One file extended: `tests/verify_human_approval_state.py` (new
    field asserted on two existing synthetic rows, plus a new row
    proving the flag passes through raw on a non-`Deploy Aggressively`
    posture).
-   No Frozen Core component touched.

------------------------------------------------------------------------

## RE-032.10 iteration C — wiring authorizes_dry_powder_ceiling_90 into Dry Powder Protocol

The real behavior change: `human_approval_above_ceiling` stops being
hardcoded and `dry_powder_protocol.py` starts computing tranches up to
the extended ceiling by formula, exactly as iteration A's design point
1 specified in advance ("dry_powder_protocol.py will compute tranches
up to this new 90% the same way it already does up to 80%").

What changed, and why it's a real design decision, not just wiring:

-   `engine/dry_powder_protocol.py` -- new constant
    `CEILING_FRACTION_AGGRESSIVE_EXTENDED = 0.90`. In `evaluate()`'s
    Step 2, when `ceiling_posture` is `Deploy Aggressively` AND
    `human_approval_above_ceiling` is `True`, `ceiling_fraction`
    becomes 90% instead of 80% -- nothing else about the tranche
    formula changes; Step 5 computes the same 22%-of-remaining tranche,
    capped by headroom under whichever ceiling is active.
-   This **retires `CEILING_REACHED_APPROVED` as a reachable status**.
    Before this iteration, reaching 80% with Human Approval set
    produced that status with `authorized_amount=None` (RE-041.1
    forbade computing a number by formula because there was no upper
    bound on "beyond the ceiling"). RE-032.10 supplied that bound (90%,
    never 100%) -- which is exactly what makes formula-driven
    computation in that band safe. Once the ceiling itself extends,
    there is nothing left for a separate "approved beyond ceiling, fix
    it manually" status to describe. The constant stays defined (status
    string schema stability, anything already matching on it) but
    `evaluate()` no longer produces it -- flagged explicitly rather than
    silently left as dead, misleading documentation.
-   The extension only ever replaces `Deploy Aggressively`'s own
    ceiling -- never applies to `Deploy Partially`'s 40% ceiling (which
    has no exception mechanism at all, per the manual's own callout),
    and never stacks (90%, not 80%+90%). Both guaranteed structurally:
    the extension check is gated on `ceiling_posture == DEPLOY_
    AGGRESSIVELY` before it can touch `ceiling_fraction` at all.
-   `audit_posture.py` -- `human_approval_above_ceiling` is read
    directly from `ha_result.authorizes_dry_powder_ceiling_90` when a
    Human Approval result exists for the patrimonio, `False` if it
    doesn't (file missing) -- same fail-closed discipline as
    everywhere else in this project: absence of data is never read as
    authorization. New print line added
    (`Human Approval authorizes_dry_powder_ceiling_90 (...)`) for
    visibility even when the value is `False`.

Acceptance checks, agreed with Armando before this iteration (both B
and C) started, each verified in `tests/verify_dry_powder_protocol.py`:

-   `human_approval_above_ceiling=False` → unchanged, 80% ceiling, hard
    stop (`ceiling_no_approval`, pre-existing case, still passes).
-   `True` → extraordinary 90% ceiling, never 100%
    (`extended_within_band`, `extended_trimmed`, `extended_hard_stop`).
-   The tranche stays 22% of remaining, only the ceiling headroom
    changes (`extended_within_band_amount` = 3.96, formula-computed,
    not `None`).
-   No active episode or incomplete ledger → not evaluated at all, flag
    or no flag -- already guaranteed for free by
    `to_dry_powder_protocol_inputs()` returning `None` in that case
    (unchanged code path, no new check needed).
-   The extension never applies to `Deploy Partially`
    (`partially_flag_ignored`).

What this does not authorize:

-   No manual operativo update -- iteration D, still deliberately
    separate, since the manual's 2.5 callout currently tells Armando
    this is "not usable yet" and that needs to change carefully, not as
    a side effect of this entry.
-   No wiring into `run.py`/`DecisionEngine` -- unchanged, still
    explicitly out of scope for the whole project.
-   No further ceiling tier beyond 90% -- if one is ever wanted, that
    is new design work, not a resurrection of `CEILING_REACHED_APPROVED`.

Boundary:

-   Two files changed: `engine/dry_powder_protocol.py`,
    `audit_posture.py`.
-   One file extended: `tests/verify_dry_powder_protocol.py` (import
    swapped `CEILING_REACHED_APPROVED` for
    `CEILING_FRACTION_AGGRESSIVE_EXTENDED`; old `ceiling_approved` case
    replaced by four new cases covering the extended ceiling's full
    behavior).
-   No Frozen Core component touched.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones (`verify_baseline_harness.py`,
    `verify_secondary_baselines.py`, `verify_validation_metrics.py` --
    pinned-runtime mismatches; `verify_research_engine.py` -- a
    pre-existing tie-break ordering difference, unrelated to this
    change).

------------------------------------------------------------------------

# Roadmap

## Pre-Phase Gate

Closed as of RE-027.5.

`ResearchEngine` now exists as a rebuilt, smoke-tested facade over the
shared verified research pipeline. It produces `ResearchResult` from
snapshot, observable universe, selected similarity matches and
evidence. `DecisionEngine` consumes the same shared pipeline, so there
is no second independent implementation of the objective Research
flow.

Evidence Engine v2 or Similarity Engine v2 work can now proceed
without being blocked by a stale named architecture object.

## Phase 1

Evidence Engine v2 — closed for the current architecture pass
(RE-028.1-RE-028.4). Evidence now exposes a stable descriptive surface.
Interpretation moves to Assessment / SOP governance.

## Phase 2

Assessment Engine v2 — opened with RE-029.1 scope audit; boundary
audited in RE-029.2; shared Research pipeline consumed in RE-029.3;
public helpers verified in RE-029.4; confidence-to-posture gate
boundary defined in RE-029.5; Evidence Quality Gate dimensions defined
in RE-029.6; calibration boundary documented in RE-029.7; future
implementation scope bounded in RE-029.8; first-code acceptance
criteria documented in RE-029.9.

RE-029.1 defines the first governance boundary for Assessment / SOP:
four capital-intensity postures, one orthogonal `Blocked` veto, three
initial invalidation gates, and mandatory human approval for capital
deployment. It deliberately does not define numeric thresholds or
automatic actions.

RE-029.2 audits the current `AssessmentEngine`: temporal safety is
already resolved, but it still duplicates the Research pipeline locally
and computes confidence through a separate `ValidationEngine` path.
RE-DOC-004 records two follow-up boundaries before trigger design:
`drawdown_zone()` is market severity, not capital posture; and stepped
error tolerance remains pending until SOP governance defines trigger
logic.

RE-029.3 makes `AssessmentEngine` consume the shared
`build_research_result()` pipeline, closing the Research source-of-truth
duplication identified in RE-029.2. RE-029.4 verifies the public helper
outputs after that refactor. RE-029.5 defines the connection pattern
between confidence / evidence quality and capital posture: gate /
ceiling, not weighted input. Gates combine by veto / most restrictive
ceiling across evidence quality, regime comparability and personal
capacity. The current `AssessmentEngine` confidence score is explicitly
excluded from SOP capital gates while stability remains hardcoded.
RE-029.6 defines the Evidence Quality Gate dimensions: coverage,
consistency, diversity, independence / dispersion and predictive
validation status. It also records the initial conservative stance:
current Research Validation is reproducible but not yet predictive
validation, because hit-rate is not discriminating and rank correlation
is weakly negative. RE-029.7 defines the calibration boundary: the gate
is fail-closed, movement beyond conservative requires pre-registered
criteria, current validation metrics do not suffice, `confidence.score`
is prohibited even as a temporary proxy, and aggregate Research
Validation metrics must not be confused with local snapshot quality.
RE-029.8 defines the first future implementation scope: create a
separate `EvidenceQualityGate` structure only, keep local snapshot
inputs separate from global model-validation state, preserve at least
three conceptual output states (`not measurable`, conservative and a
future less-restrictive state), clarify that `stability` is not one of
the five official Evidence Quality dimensions today, and keep the gate
unwired from `run.py` and `DecisionEngine`. Remaining Assessment / SOP
work is executable thresholds, gate calibration, regime comparability,
personal capacity and capital posture mapping. RE-029.9 defines the
acceptance criteria for the first isolated gate PR: it must be testable,
fail-closed with today's incomplete inputs, explain the specific cause
of any cap, treat `None` or incomplete inputs as `not measurable`, avoid
Frozen Core, and remain unwired from the operative flow.

RE-030.1 implements that first isolated gate structure. It adds
`engine/evidence_quality_gate.py` and
`tests/verify_evidence_quality_gate.py`. The gate separates local
snapshot inputs from global model-validation state, returns discrete
states with explanations, defaults fail-closed and remains outside
`run.py`, `DecisionEngine`, `AssessmentEngine` and `ValidationEngine`.
No thresholds or capital posture mapping exist yet.

RE-030.2 adds `build_local_evidence_quality_inputs(evidence)`, the first
adapter from real Research output into local Evidence Quality inputs.
The adapter uses `Evidence` as the single source of truth for matches,
calculates coverage from usable returns (`return_count`, not selected
match count), calculates consistency at `evidence.horizon_years`, and
keeps independence / dispersion unmeasured. Current real local values:
coverage=0.9, consistency=0.9518456229064439, diversity=0.6. With
global model-validation state still not validated, the gate returns
`not measurable` for today's snapshot.

RE-031.1 opens the Regime Comparability Gate as a separate governance
boundary. It defines regime comparability as a gate / ceiling, not a
weighted input, and separates it from both Evidence Quality and
`AssessmentEngine.drawdown_zone()`. No code, thresholds, regime taxonomy
or capital posture mapping exist yet. Current Regime Comparability state
is not measurable.

RE-032.1 opens the Personal Capacity classification boundary. It does
not assume Personal Capacity is a parallel computable gate. The first
classification question is whether Personal Capacity belongs as a gate,
as a Human Approval prerequisite, or as a mixed control. The document
separates verifiable personal facts from attested judgement and records
the special unreliability of crisis-time drawdown tolerance revisions.
No code, thresholds, personal-capacity taxonomy or capital posture
mapping exist yet.

RE-033.1 formalizes Capital Posture vocabulary and ordering:
`Conserve`, `Prepare`, `Deploy Partially`, `Deploy Aggressively`, with
`Blocked` as an orthogonal veto. It separates internal gate-state mapping
from multi-gate combination. Current `not measurable` and `conservative`
gate states both cap at `Conserve`, with different explanations. Given
current known gate states, the documentation-level capital posture
ceiling is `Conserve`. No posture engine or gate-combination logic exists
yet.

RE-034.1 defines the gate-combination boundary. Combination consumes
discrete posture ceilings and `Blocked` flags, not scores. `Blocked`
wins first; otherwise the most restrictive ordered ceiling wins.
RE-034.1 separates non-deployment postures (`Conserve`, `Prepare`) from
deployment postures (`Deploy Partially`, `Deploy Aggressively`). Evidence
Quality not measurable blocks deployment but may still allow `Prepare`.
Unavailable Regime Comparability and unavailable / unclassified Personal
Capacity cap at `Conserve`. Given current states, the
documentation-level final posture ceiling remains `Conserve`.

RE-034.2 defines first-code acceptance criteria for the future isolated
gate-combination module. The required tests must pin the current real
state to `Conserve`, verify that `Blocked` wins first, verify that the
most restrictive ceiling wins, protect the Evidence Quality
`not measurable -> Prepare` exception from regression, prove that
Evidence Quality does not override more restrictive gates, and require
traceable explanations naming the limiting gate or control.

RE-034.3 adds the isolated gate-combination module and verification test.
RE-034.4 documents its status: `engine/gate_combination.py` exists,
`tests/verify_gate_combination.py` passes, and the module remains outside
the operative flow. It provides discrete posture constants, `Blocked`
precedence, most-restrictive ceiling selection, and traceable limiting
explanations. It does not implement a posture engine, thresholds,
protocol rules, Human Approval or runtime wiring.

RE-PRED.1 opens the predictive-validity boundary. It makes no new
validation claim and runs no new calculation. It defines the future
contract for any predictive claim: audit the actual target before
freezing it, freeze the model before holdout or live tracking,
separate historical backtest from prospective holdout and live tracking,
predefine baselines, report uncertainty under dependence-aware methods,
and treat permanent weak predictive evidence as a named design branch
rather than an implementation bug.

RE-PRED.2 audits the currently implemented predictive target. The
operative target is `future_return_5y`: annualized five-year CAGR from
drawdown bottom, calculated as `(p1 / p0) ** (1 / years) - 1` using
Shiller `Price.1`. Evidence forecasts use `Evidence.median_return` over
matched `future_return_5y` values, and Research Validation compares that
forecast against each episode's realized `future_return_5y`. Missing
future outcomes remain `None`, never 0.0. RE-PRED.2 does not freeze or
change the target.

RE-PRED.3 defines the target-freeze decision boundary. The implemented
target remains the provisional freeze candidate, but not the definitive
frozen target. The existing MAE must be read as error over annualized
CAGR, not cumulative five-year return. Definitive target freeze requires
a future numbered decision.

RE-PRED.4 verifies source-column semantics directly against
`data/raw/shiller.xlsx`. Column H / `Price` is Real Price. Column J /
`Price.1` is Real Total Return Price, with stacked header labels
`Real` / `Total` / `Return` / `Price`. Therefore the current implemented
target is annualized real total-return CAGR from drawdown bottom over
the five-year horizon. This verifies the column semantics, but still
does not definitively freeze the target.

RE-PRED.5 defines target-freeze acceptance criteria. It orders the
remaining work by dependency: target mechanics and semantics first,
unit/horizon and absolute-vs-excess decision before baselines, then
missingness taxonomy, model-freeze reference and target unfreeze
criteria. It records that `Price.1` semantics are verified, but
bottom-detection and episode-boundary semantics are not yet audited.
The implemented target remains provisional, not definitively frozen.

RE-PRED.6 audits bottom detection and episode boundaries. It documents
that drawdown episodes are detected on nominal price `P`, while
future returns are measured on Real Total Return Price `Price.1`.
It also records that unrecovered drawdowns are structurally excluded
because episodes are appended only on recovery. Finally, it records a
verified date-arithmetic bug: `duration_months` and `recovery_months`
are calculated by subtracting `YYYY.MM` floats rather than calendar
months, affecting public Evidence recovery statistics and active
Similarity scoring. No code is changed in RE-PRED.6.

RE-BUG.1 promotes the date-arithmetic duration bug to near-term code-fix
priority. It defines acceptance criteria for a future fix: use explicit
calendar-month arithmetic, verify examples such as 1929.09 -> 1932.06 =
33 months, update public Evidence recovery statistics from corrected
values, compare selected match identifiers before and after the fix,
rerun Research / Assessment / Validation verifications, report any
downstream Similarity / Research Validation changes, and avoid mixing
the bug fix with target-freeze or governance work.

RE-BUG.2 fixes the calendar-month duration bug in code. It introduces
centralized `months_between()` arithmetic, updates drawdown duration and
recovery duration calculations, adds a duration-specific verification
test and updates canonical Research / Assessment / Research Validation
expectations.

RE-BUG.3 documents the post-fix impact. The current canonical evidence
surface now uses `Evidence.median_return = 0.10192496249726091`.
Research Validation now reports `mae = 0.06928793787076225`,
`directional_hit_rate = 0.9473684210526315` and
`rank_correlation = -0.26505171850684983`. These values supersede the
pre-fix values going forward without rewriting the historical record.

RE-DATA.1 records future Shiller data update automation as planned, not
implemented. Any future updater must validate workbook structure,
confirm `Price.1` semantics, back up the prior local source, rerun tests
and log the update before replacing `data/raw/shiller.xlsx`. Manual
updates remain the current process.

RE-PRED.7 defines the absolute-vs-excess-return boundary. Absolute
return stays the existing Evidence descriptive surface; it is not
redefined or renamed. Excess return over a primary naive baseline
(unconditional historical mean/median `future_return_5y`, evaluated
point-in-time) becomes the future predictive-validity surface, to be
computed in the Research Validation Harness, not in Evidence. MAE and
directional hit-rate require an explicit baseline forecast series to
compute excess against; rank correlation already tests ordering against
no signal and needs no separate excess transformation. No baseline value
is computed and no excess-return metric is implemented in this
iteration.

RE-PRED.8 defines acceptance criteria for the primary baseline and
corrects RE-PRED.7's rank-correlation claim forward: that claim assumed
a single global constant baseline, which would not be point-in-time
safe. The primary baseline is instead a point-in-time expanding median
of `future_return_5y`, computed by reusing `ObservableUniverse` and
bottom_index self-exclusion — the same temporal-safety machinery already
verified for the model's own forecast in RE-025.1 — evaluated over the
model's own evaluable record set. Because this baseline varies per
episode, its rank correlation is a real, computable comparison against
the model's, not an undefined quantity. Mean, and the remaining
secondary baselines, remain deferred. No baseline value is computed and
no code changes in this iteration.

RE-PRED.9 implements the primary baseline in code:
`engine/baseline_harness.py` and `tests/verify_baseline_harness.py`.
It reuses `ObservableUniverse`, bottom_index self-exclusion and the
existing MAE / hit-rate / rank correlation functions unmodified — no
Frozen Core component is touched, and no existing file changes except
`tests/verify_core.py`'s structural list. The invariant that a baseline
forecast can never be `None` when the model's own record is evaluable
is proven by construction (the model's matches are a subset of the
baseline's unconditional comparable pool) and checked explicitly by the
test, not assumed. The test has only been run outside the pinned
runtime, to confirm the code executes and the structural invariants
hold. No baseline value is canonical yet; RE-PRED.10 will record the
canonical baseline metrics once confirmed under `requirements.txt`.

RE-PRED.10 records those canonical values, confirmed under
`RUNTIME : PINNED`, and the finding that follows: the model does not
beat the primary baseline on any of the three canonical metrics — it
ties on directional hit-rate (0.94737 both) and loses on MAE
(baseline 0.06741 vs model 0.06929) and rank correlation (baseline
-0.23172 vs model -0.26505). Predictive validity, as defined by
RE-PRED.1's burden of proof, is not demonstrated relative to this
baseline. This sharpens the existing conservative `EvidenceQualityGate`
state with a direct quantitative result but does not itself change any
gate threshold or capital posture ceiling — that remains a separate,
explicit governance decision under RE-029.7.

A proposal to formalize `NOT_DEMONSTRATED` as a third
`EvidenceQualityGate` output state was raised immediately after
RE-PRED.10 and deferred in RE-PRED.10.1: it would rest on one baseline
over a non-independent N=19 sample, and today it would not change the
resulting posture ceiling versus the existing `not measurable` state.
RE-PRED.11 implements two secondary baselines (`zero_forecast`,
`mean_reversion_forecast = -drawdown`) in `engine/baseline_harness.py`
to test whether RE-PRED.10's finding survives a change of baseline,
structurally verified outside the pinned runtime only. RE-PRED.12
records, as an explicit open question, that baseline-choice robustness
(what RE-PRED.11 tests) and sampling-noise robustness (whether any
excess value is distinguishable from chance given N=19 dependent
records) are different questions — this iteration answers only the
first. The gate-state decision is deferred until the full three-baseline
picture is confirmed under the pinned runtime.

RE-PRED.13 records that confirmed picture. The model beats zero and
mean-reversion clearly on MAE (0.06929 vs 0.12749 and 0.18159), ties all
measurable baselines on directional hit-rate, and loses on rank
correlation to both the primary baseline and mean-reversion — the
mean-reversion case a full sign flip (+0.26316 vs the model's -0.26505).
RE-PRED.10.1's trigger ("loses to the full set on a majority of
metrics") was evaluated explicitly and does not activate, so
`NOT_DEMONSTRATED` remains deferred. A working hypothesis is registered,
not authorized as fact: drawdown depth alone may order outcomes better
than `SimilarityEngine`'s multidimensional conditioning, possibly
through signal dilution across `SIMILARITY_WEIGHTS` — flagged for
future investigation only, no Frozen Core change made or authorized.
Both new correlation values remain subject to RE-PRED.12's unresolved
sampling-noise caveat on the same N=19 dependent sample.

RE-PRED.14 adds an exploratory, read-only diagnostic
(`engine/dimension_diagnostic.py`,
`tests/diagnostic_similarity_dimensions.py`) testing the signal-dilution
hypothesis registered in RE-PRED.13 by isolating each active
`SimilarityEngine` dimension. Confirmed under the pinned runtime, no
dimension in isolation reproduces mean-reversion's positive rank
correlation -- all six remain negative, from -0.19692 (drawdown) to
-0.26353 (pre_crash_return_3y). Signal dilution is not supported as the
explanation. A revised hypothesis is registered, not authorized:
nearest-neighbor selection may not preserve monotonic rank order the
way a direct function of the query's own value does. No `SimilarityEngine`
change is made or authorized. RE-PRED.12's sampling-noise caveat applies
with extra force to this smaller, still-dependent slicing.

RE-PRED.15 closes RE-PRED.12's method gap directly.
`engine/dependence_bootstrap.py` builds independence clusters from the
union of RE-025.8's overlapping-outcome-window pairs and RE-025.9's
repeated-forecast groups, then runs a cluster bootstrap (whole clusters
resampled with replacement, never individual records) to produce
dependence-aware confidence intervals for the model, both baselines, and
their paired excess. Seed and replicate count are fixed constants
(`seed=42`, `replicates=5000`), a 90% percentile interval. Structurally
verified outside the pinned runtime only: 4 independence clusters over
the 19 evaluable records, sizes `[10, 7, 1, 1]` -- not a canonical value.
Whether the excess intervals against the primary and mean-reversion
baselines straddle zero is exactly the open question this answers, once
confirmed under the pinned runtime and recorded in a future iteration.

RE-PRED.16 records that confirmation. Canonical clusters: 3, sizes
`[10, 8, 1]` -- hand-verified against RE-025.8/RE-025.9's own canonical
tables. MAE excess vs. primary baseline is small but robust (90% CI
`[-0.00356, -0.00045]`, does not straddle zero); MAE excess vs.
mean-reversion is large and robust (`[0.08355, 0.14025]`). Hit-rate
excess is exactly zero at every percentile against both baselines --
the tie is stable under resampling. Rank correlation gives two
different answers: the excess vs. primary baseline straddles zero
(`[-0.06068, 0.02514]`) -- not distinguishable from sampling noise --
while the excess vs. mean-reversion does not (`[-0.94270, -0.34208]`)
-- RE-PRED.13's full sign-flip finding is robust to the known
dependence structure, not an artifact of it.

## Phase 3

Inference Engine

## Phase 4

Executable Constitution

## Phase 5

Protocol Engine

## Phase 6

Dashboard

Research Validation (RE-025.x) runs alongside these phases as a
cross-cutting concern — it evaluates the accuracy of what Evidence
Engine already produces, rather than belonging to any single phase.
Not yet reflected as its own phase; revisit if the harness grows
enough to justify one.

Effective sample size is documented conceptually in RE-025.6. One
outcome-side dependence channel is observable through RE-025.8, and
one forecast-side dependence channel is observable through RE-025.9.
RE-025.10 closes the current Research Validation block as exploratory
validation with explicit limitations. No numeric effective-N correction
exists yet; Research Validation metrics should keep treating `n=19` as
an operative count, not as an independent statistical sample.

RE-026.1 adds a functional smoke test for that canonical Research
Validation surface. It first verifies the pinned runtime from
`requirements.txt`, then verifies the canonical RE-025 metrics and
dependency diagnostics.

RE-027.1 audited the gap between the documented `ResearchEngine`
object and the operative pipeline already verified through
`DecisionEngine`. RE-027.2-RE-027.4 align `ResearchResult`, rebuild
`ResearchEngine` as a thin facade, and add a functional smoke test.
RE-027.5 then closes the remaining architecture risk by extracting
the shared `build_research_result()` pipeline consumed by both
`DecisionEngine` and `ResearchEngine`.

RE-DOC-003 corrects the status of `AssessmentEngine`: code inspection
confirms that RE-024.3 already connected it to `ObservableUniverse`.
The remaining `AssessmentEngine` issue is duplication of the Research
pipeline, not temporal-safety leakage.

RE-028.1 opens Evidence Engine v2 with a scope audit only. The current
Evidence contract is stable and already consumed by the shared Research
pipeline, the offline Research Validation harness and `AssessmentEngine`.
Evidence v2 must therefore be additive: richer objective description of
the evidence sample, without changing existing fields or moving
assessment/recommendation logic into Evidence.

RE-028.2 implements the first additive Evidence v2 fields:
return_count, positive_count, negative_count, zero_count,
non_positive_probability and return_spread. These fields make the
shape of the realized return sample observable while preserving the
Evidence boundary: description only, no confidence score, no portfolio
recommendation and no SOP action.

RE-028.3 closes the next Evidence v2 scope question without adding
code: named percentile fields are deferred. `Evidence.percentile(p)`
already provides the descriptive surface; fixed percentile names should
only be added after Assessment / SOP governance defines the thresholds
it actually needs.

RE-028.4 closes Evidence Engine v2 for the current architecture pass:
the Evidence layer now has enough objective descriptive shape for the
next layer to consume. Remaining questions are interpretive and belong
to Assessment / SOP governance, not Evidence.

------------------------------------------------------------------------

# Project Axioms

-   SOP is the product.
-   Research Engine produces evidence.
-   Evidence must be explainable.
-   Governance is above prediction.
-   Robustness is preferred over sophistication.
-   Every iteration modifies one responsibility.
-   Stability has priority over novelty.

------------------------------------------------------------------------

# Changelog

## Version 2.33

-   RE-PRED.17: "Similarity Engine v2" (enriquecer con dimensiones) no
    se persigue -- la premisa estaba desactualizada (dimensiones ya
    implementadas en v1) y la evidencia ya reunida (RE-PRED.13-16)
    argumenta en contra de esa dirección concreta. Decisión de Armando
    tras presentarle el hallazgo. Documentation-only. Full details in
    the Design Decision entry above (RE-PRED.17).

## Version 2.32

-   RE-KERNEL.1: `engine/kernel.py` -- primer módulo real del Kernel,
    extracción pura de `audit_posture.py` (K4/gobernanza ya
    implementados: Evidence Quality, Regime Comparability, Personal
    Capacity Facts, Human Approval, Dry Powder). K1/K2/K3/K5/K6 siguen
    sin spec, deliberadamente. `audit_posture.py` pasa a ser un
    wrapper fino. Verificado carácter a carácter contra la salida
    anterior. Full details in the Design Decision entry above
    (RE-KERNEL.1).

## Version 2.31

-   RE-DOC-006: `CONSTITUTION.md` sincronizada con el estado real del
    dashboard -- ya no dice "pendiente" de algo que lleva construido y
    committeado desde hace varias sesiones (RE-DASH.1.21, RE-SHILLER-
    DASH.1-8). Tabla "Avance honesto" separa dashboard operativo y
    panorama histórico en dos filas. Cero cambios funcionales. Full
    details in the Design Decision entry above (RE-DOC-006).

## Version 2.30

-   RE-SHILLER-DASH.8: "Retornos reales posteriores según CAPE inicial"
    reducido de cuatro párrafos a dos -- una línea de metodología, una
    conclusión corta en el tono que pidió Armando. Full details in the
    Design Decision entry above (RE-SHILLER-DASH.8).

## Version 2.29

-   RE-SHILLER-DASH.7: "peores episodios con nombre" acotado a peak_date
    >= 1900 -- reemplaza el episodio de 1872-1877 (fecha no verificada
    con precisión) por el estallido de la burbuja puntocom (2000-2002,
    -43,7%), bien documentado. Full details in the Design Decision
    entry above (RE-SHILLER-DASH.7).

## Version 2.28

-   RE-SHILLER-DASH.6: "Resumen de drawdowns históricos" gains a table
    naming the 3 worst episodes by magnitude (1929, 2007-2009, both
    high-confidence; a third from the 1870s carries an explicit
    unverified-date caveat in its own name). "Retornos reales
    posteriores según CAPE inicial" gains a plain-language lead
    paragraph with a concrete cumulative-return example and reworded
    headers, fixing a real clarity gap Armando flagged ("NO entiendo
    las cifras"). Full details in the Design Decision entry above
    (RE-SHILLER-DASH.6).

## Version 2.27

-   RE-SHILLER-DASH.5: two new sections in the Shiller panel --
    "Retornos reales posteriores según CAPE inicial" (median forward
    real total return at 5/10/15y, bucketed by CAPE level, with sample
    size per bucket) and "Resumen de drawdowns históricos" (median/
    worst drawdown, median duration/recovery across the 23 detected
    episodes). Plus a wording fix in "Detalle de indicadores": "cerca
    de la media" now states above/below the raw mean when true, without
    changing the underlying z-score criterion. Full details in the
    Design Decision entry above (RE-SHILLER-DASH.5).

## Version 2.26

-   RE-SHILLER-DASH.4: Resumen ejecutivo replaces its run-on sentence
    with a headline-action/headline-support split plus a stat-strip of
    grouped, dot-coded figures (same patterns already approved for
    "Estado hoy"/"Evidencia histórica" in RE-DASH.1.11). Inflación
    standardized to 2 decimals throughout (was mismatched against
    Tipo's 2 decimals). Chart y-axis tick labels on linear-scale charts
    fixed from English-period to Spanish-comma decimals. Full details
    in the Design Decision entry above (RE-SHILLER-DASH.4).

## Version 2.25

-   RE-SHILLER-DASH.3: traffic-light dots added to Indicadores clave
    and Resumen ejecutivo, on a distance-from-norm axis distinct from
    the operational dashboard's judgment-based dots, plus a fecha/
    valor annotation on every chart's latest point. Full details in
    the Design Decision entry above (RE-SHILLER-DASH.3).

## Version 2.24

-   RE-SHILLER-DASH.2: executive-reading layer added to the new
    Shiller panel per Armando's structured review (resumen ejecutivo,
    franja de indicadores, percentil de CAPE, media 10 años). Real
    finding surfaced and fixed: the price chart plotted nominal price,
    not real -- corrected, core engine's episode detection unaffected.
    `drawdown_context()` extracted to a shared function used by both
    dashboards. Full details in the Design Decision entry above
    (RE-SHILLER-DASH.2).

## Version 2.23

-   RE-SHILLER-DASH.1: new `generate_shiller_dashboard.py` ->
    `outputs/shiller_dashboard.html`, a separate, read-only, static-
    chart panel over the full Shiller series (1871-2026) -- distinct
    purpose from the operational dashboard, agreed with Armando before
    building. Reuses `run_drawdown_engine()` and existing formatters,
    no new loader, no recalculated figures. Full details in the Design
    Decision entry above (RE-SHILLER-DASH.1).

## Version 2.22

-   RE-DASH.1.21: Liquidez moves from a table row + 84px inline bar to
    one full-width card per patrimonio, per Armando's own detailed
    design proposal after six rounds (1.13-1.20) failing to make the
    small format work. Suelo/techo now visible as text, not only in a
    hover tooltip. Reuses all existing zone/marker/caption math and
    figures unchanged -- container only. Confirmed by Armando. Full
    details in the Design Decision entry above (RE-DASH.1.21).

## Version 2.21

-   RE-DASH.1.20: "Valor" (Datos de mercado) was the last remaining
    right-aligned value column after RE-DASH.1.18 moved "Liquidez
    disponible" left -- Armando's screenshot showed that split.
    Asked which direction he wanted rather than inferring (right
    everywhere, or left everywhere -- both valid, in conflict with
    each other); he chose left for all three (Valor, Human Approval,
    Liquidez disponible). Full details in the Design Decision entry
    above (RE-DASH.1.20).

## Version 2.20

-   RE-DASH.1.19: the "Régimen no comparable (CAPE)" Alertas entry was
    opaque to a non-technical reader (Armando: "no acabo de
    entenderlo"). Reworded to plain language reusing the exact
    existing today-vs-matched-range comparison ("No hay episodios
    comparables con un CAPE tan alto."), with gender/article-correct
    forms per dimension. No change to the underlying comparison. Full
    details in the Design Decision entry above (RE-DASH.1.19).

## Version 2.19

-   RE-DASH.1.18: "Liquidez disponible" was right-aligned while "Human
    Approval" (same column position, other table) is left-aligned
    text -- visible as a mismatch once both tables shared column
    widths (RE-DASH.1.17). Dropped the right-alignment. Full details
    in the Design Decision entry above (RE-DASH.1.18).

## Version 2.18

-   RE-DASH.1.17: the two "Estado por patrimonio" tables auto-sized
    columns independently, staggering every column boundary between
    them (Armando's "triángulo"). New `.patrimonio-table` class forces
    identical `table-layout:fixed` widths on both. Full details in the
    Design Decision entry above (RE-DASH.1.17).

## Version 2.17

-   RE-DASH.1.16: the liquidity bar's marker hung half off the track
    at the range extremes, and its three color zones were too faint to
    read distinctly (Armando: "el diseño... es claramente mejorable").
    Fixed with a visual-only position inset, boundary tick marks, a
    thicker track, and a hairline border -- scoped to this bar variant
    only. Full details in the Design Decision entry above
    (RE-DASH.1.16).

## Version 2.16

-   RE-DASH.1.15: fixes two real defects in the RE-DASH.1.14 liquidity
    bar, both surfaced by Armando's screenshot. (1) The marker's CSS
    position used a different coordinate scale than the color zones it
    was supposed to sit inside, so out-of-range markers rendered
    visibly detached from the track instead of at its edge -- fixed by
    converting the marker through the same span used for the zone
    boundaries. (2) The signed € figure read as a "vs. suelo/techo"
    comparison per the column header but was always a gap against a
    single boundary -- fixed by naming the boundary in the label
    itself ("sobre techo"/"bajo suelo"/"sobre suelo"). Also widened the
    liquidity bar's track from 52px to 84px so the zones are legible.
    Full details in the Design Decision entry above (RE-DASH.1.15).

## Version 2.15

-   RE-DASH.1.14: the liquidity bar (RE-DASH.1.13) gains three fixed
    color zones painted on the track itself -- red (below suelo),
    green (suelo-techo, the objetivo range), amber (above techo, idle
    liquidity) -- from a personal design reference Armando shared and
    explicitly invited adapting, not copying literally. Zone
    boundaries computed from the same `LIQUIDITY_BAR_CLAMP_MIN/MAX`
    constants that already bound the marker's position, so the zones
    and the clamp can't drift apart. Suelo/techo € figures, dropped
    from the main view in RE-DASH.1.13, return as a native `title`
    tooltip on the bar -- passive metadata, not a new interactive
    control. Full details in the Design Decision entry above
    (RE-DASH.1.14).

## Version 2.14

-   RE-DASH.1.13: fixes a real header-wrap bug Armando confirmed with
    a screenshot from his own browser ("Serie completa (1871-2026)"
    wrapping to two lines) -- `white-space:nowrap` on `th`/`.ctx`.
    New `liquidity_bar()` replaces the Liquidez table's separate
    "Rango de liquidez"/"Exceso/Déficit" columns with one visual gauge
    (marker on a suelo-techo track, colored with the same status
    color as the Estado pill, exact € kept as the caption), the same
    pattern as Datos de mercado's context bars that Armando explicitly
    liked. Absolute suelo/techo figures relocated (not dropped) to
    Detalle técnico. Full details in the Design Decision entry above
    (RE-DASH.1.13).

## Version 2.13

-   RE-DASH.1.12: Estado column moved to align with Postura's position
    across the two Estado por patrimonio tables. Fixed a real
    typography bug: `body` had no explicit `font-size`, so Alertas and
    the bare sub-section labels ("Liquidez", "Postura y permisos")
    fell back to the browser default (16px) while every other
    component was explicitly 14-15px -- the "otra tipografía" Armando
    flagged. Full details in the Design Decision entry above
    (RE-DASH.1.12).

## Version 2.12

-   RE-DASH.1.11: McKinsey/Bain-style visual redesign, per Armando's
    explicit direction ("mantén lo que encaja, modifica o elimina lo
    que se sale"). Right-aligned numeric table columns, muted
    uppercase table headers, sharper corners, a status-colored accent
    on "Estado hoy", Evidencia histórica's four indicators as a stat
    strip with the methodology note moved below per his instruction.
    After review, Armando confirmed four fixes: a duller, less
    "opportunity-like" amber; his own wording for the "no autoriza
    despliegue" caveat with more visual weight; confirmed (not
    changed) that large text already carries the primary message, not
    just the color accent; confirmed (not changed) that Detalle
    técnico was already last and collapsed. Zero changes to gates,
    protocols, or any figure shown -- presentation-layer only. Full
    details in the Design Decision entry above (RE-DASH.1.11).

## Version 2.11

-   RE-DASH.1.10: abandons the launchd/`WatchPaths` approach after two
    failed fixes (RE-DASH.1.8, RE-DASH.1.9) and a step-by-step
    diagnosis with Armando that isolated the failure to background
    (launchd) access to a file inside iCloud Drive -- not the script,
    not the plist syntax, not iCloud materialization (all three ruled
    out with direct tests, not assumed). Replaced with
    `Actualizar Dashboard.command` at the repo root: a double-click
    file that runs interactively, the exact context already proven to
    work. Removed the dead `scripts/` files rather than leave
    non-functional automation in the repo. Full details in the Design
    Decision entry above (RE-DASH.1.10).

## Version 2.10

-   RE-DASH.1.9: fixes RE-DASH.1.8's real first-run failure on
    Armando's machine (`zsh: can't open input file`, the
    `zsh -l -c "<quoted path>"` invocation did not behave as
    documented). Removed the shell-wrapping at the launchd level
    entirely -- `ProgramArguments` now execs the script by absolute
    path directly, no quoting involved; the login-shell PATH pickup
    for `python3` moved inside the script itself, wrapping only a
    short, space-free command string. Still not confirmed working
    end-to-end -- Armando needs to reload the corrected job. Full
    details in the Design Decision entry above (RE-DASH.1.9).

## Version 2.09

-   RE-DASH.1.8: reactive auto-regeneration for the dashboard via a
    macOS launchd agent (`scripts/com.armando.sop-dashboard-regen.plist`)
    watching `data/raw/`, plus a thin wrapper script
    (`scripts/regenerate_dashboard.sh`). Deliberately not a scheduled
    agent invocation -- Armando asked for this to work without going
    through an agent each time, so it is a deterministic OS-level job
    calling the unmodified `generate_dashboard.py`. Not active until
    Armando installs it himself. launchd/`WatchPaths` behavior not
    verified from this sandbox (no macOS/launchd here) -- only the
    wrapper script's own logic and the plist's XML validity were
    verified directly. Full details in the Design Decision entry above
    (RE-DASH.1.8).

## Version 2.08

-   RE-DASH.1.7: regime row in "Por qué no se actúa" now states
    direction (alto/bajo) instead of just "outside range", e.g.
    "Régimen (CAPE): Muy alto frente al histórico comparable" --
    computed via a new `_regime_direction()` helper reusing the exact
    comparison the gate itself makes, fail-closed if not
    determinable. Restructured to one row per failing dimension.
    Shortened "Retorno mediano posterior (valor típico, no promedio)"
    to "Retorno mediano posterior" so it renders on one line, no
    information lost. Full details in the Design Decision entry above
    (RE-DASH.1.7).

## Version 2.07

-   RE-DASH.1.6: three correctness/density fixes on RE-DASH.1.5's
    dashboard, caught by Armando before committing. Reworded the
    regime row again ("Fuera del rango que tuvieron los episodios
    parecidos") to name explicitly whose range it is. Unified the two
    Datos de mercado context-window headers to the same computed
    "AAAA-AAAA" format (was a hardcoded year range next to a "desde
    AAAA-MM" string), split the header into two rows to reduce
    density, and dropped a now-redundant explanatory paragraph.
    Corrected a real factual error in Evidencia histórica's intro
    sentence, which implied the market is currently falling (it is at
    an all-time high, drawdown 0,0%) -- reworded after tracing
    `SimilarityEngine.compare()`'s actual multi-dimensional matching
    logic. Full details in the Design Decision entry above
    (RE-DASH.1.6).

## Version 2.06

-   RE-DASH.1.5: five-point polish pass on RE-DASH.1.4's dashboard,
    per Armando's review. Regime rows in "Por qué no se actúa"
    reworded to be self-explanatory ("Fuera del rango de episodios
    parecidos" instead of bare "No comparable"). "Estado por
    patrimonio" liquidity table unified into "Rango de liquidez" +
    "Exceso/Déficit" columns, reusing real spreadsheet figures (AMS
    +22.330,77 €, AML -50.625,00 €). All strings capitalized
    throughout. Evidencia histórica table width-constrained to fix
    values drifting far right. Datos de mercado gains a second,
    trailing-50-years context column alongside the existing
    full-history one. Full details in the Design Decision entry above
    (RE-DASH.1.5).

## Version 2.05

-   RE-DASH.1.4: full "lectura rápida" design pass, agreed with
    Armando before writing any code. Semáforo on Estado hoy, compact
    one-line rows on Por qué no se actúa, two split tables (liquidez /
    postura y permisos) on Estado por patrimonio, historical z-score
    context on Datos de mercado (full Shiller series 1871-2026,
    thresholds confirmed), reworded Evidencia histórica. Explicitly
    dropped "Qué haría falta para pasar de Conservar a Preparar" after
    verifying it would describe a transition with zero practical
    consequence (Prepare authorizes the same 0% Dry Powder deployment
    as Conserve) and no new information. Full details in the Design
    Decision entry above (RE-DASH.1.4).

## Version 2.04

-   RE-DASH.1.3: corrects a real error from RE-DASH.1.2 -- Armando
    caught that a liquidity ceiling ("techo de liquidez") does exist
    in `personal_capacity_facts.xlsx` for both AMS and AML; the prior
    claim that none existed was checked against the wrong source
    (the gate's consumed-field list, not the raw workbook). Fixed:
    real ceiling figures now shown (150.000 € AMS, 300.000 € AML),
    correctly labelled as informational, not gate-scored. Surfaced a
    real finding: AMS's liquidity is currently above its own ceiling.
    Full details in the Design Decision entry above (RE-DASH.1.3).

## Version 2.03

-   RE-DASH.1.2: dashboard restructure per Armando's second review --
    "Estado hoy" / "Por qué no se actúa" split (replacing "Resumen de
    hoy" + "Tabla resumen"), left-aligned per-patrimonio panels, real
    liquidity figures vs. suelo definido (no invented "techo" --
    flagged, not fabricated), two phrases rewritten for precision,
    Spanish decimal/thousands formatting throughout, "Nivel del
    índice" moved out of the main view. `build_dashboard_data()`
    unchanged except one new read-only call
    (`load_personal_capacity_facts_raw()`) for the liquidity figures.
    Full details in the Design Decision entry above (RE-DASH.1.2).

## Version 2.02

-   RE-DASH.1.1: dashboard clarity pass, per Armando's review. New
    order (Resumen de hoy -> Tabla resumen -> Estado por patrimonio ->
    Datos de mercado -> Evidencia histórica -> Detalle técnico
    colapsado), full Spanish translation layer, single headline
    conclusion built only from the actually-limiting gates (not
    predictive validity, corrected from Armando's own draft). Fixed a
    real formatting bug (`Rate GS10` was being multiplied by 100 a
    second time, showing 444.0% instead of 4.44%) and a capitalization
    bug ("human Approval") found in self-review. `build_dashboard_data()`
    unchanged -- presentation only. Full details in the Design
    Decision entry above (RE-DASH.1.1).

## Version 2.01

-   RE-DASH.1: `generate_dashboard.py` -- static, read-only
    `outputs/dashboard.html` audit view (six blocks: cabecera,
    mercado Shiller, gates, prerrequisitos y protocolos, patrimonios
    AMS/AML, evidencia histórica, más alertas). No new computation --
    reuses `audit_posture.py`'s exact pipeline. `outputs/` added to
    `.gitignore`. Verified by direct execution against real data,
    spot-checked against known real state. Full details in the Design
    Decision entry above (RE-DASH.1).

## Version 2.00

-   RE-044.6: first real revision of `docs/CONSTITUTION_RESEARCH_ENGINE.md`
    (v1.0 -> v1.1) after Armando's review -- five wording edits
    (Articulo 1 vs. predictive validation, Articulo 4 look-ahead bias
    named explicitly, Articulo 7 code-name clarification, Articulo 8
    "variables y precedentes", relación con `docs/CONSTITUTION.md`),
    none changing any article's spirit. New versioning policy added
    and applied to itself via a "Historial de revisiones" section.
    `core/version.py`'s `CONSTITUTION_VERSION` synced to `"1.1"`. Full
    details in the Design Decision entry above (RE-044.6).

## Version 1.99

-   RE-044.5: saved `docs/CONSTITUTION_RESEARCH_ENGINE.md` -- the
    12-article founding constitution that governed this afternoon's
    entire audit, existing only in conversation until now. Corrected
    `core/version.py`'s `CONSTITUTION_VERSION` from a stale `"1.1"`
    (no real revision ever happened) to `"1.0"`, matching the saved
    document's own header. `docs/CONSTITUTION.md` updated to list the
    new file and to fix two stale version cross-references (`v1.93`
    -> `v1.98`) found in the same pass. Closes the full afternoon
    audit: Articulo 7 (RE-044.1, RE-044.2), Articulo 3 (RE-044.3),
    Articulo 5 (RE-044.4), Articulo 8 (RE-EXP.1), and now the document
    itself. Full details in the Design Decision entry above (RE-044.5).

## Version 1.98

-   RE-EXP.1: `ExplanationEngine` fixed (was crashing --
    `AttributeError`, confirmed by running it, not just reading it),
    reconnected to `ResearchResult` (closing RE-027.2's exclusion),
    and extended to cover Articulo 8's contradicting-evidence
    requirement -- new `contradicting_precedents`, real historical
    matches whose actual return disagreed with `Evidence.median_return`.
    `models/similarity.py`'s stale type hint
    (`Explanation` -> `SimilarityExplanation`) fixed in the same pass.
    Armando's own scope, verified by direct execution: real pipeline
    run (zero crash, one real dissenting precedent found) plus four
    synthetic cases covering every branch. Closes the full afternoon
    audit against the Research Engine's 12-article constitution.
    Full details in the Design Decision entry above (RE-EXP.1). Full
    `tests/verify_*.py` suite re-run: same four pre-existing failures,
    nothing new; `run.py` unchanged.

## Version 1.97

-   RE-044.4: added traceability metadata to `ResearchResult`
    (Articulo 5) -- `engine_name`, `engine_version`, `matches_count`,
    `horizon_years`, `generated_at`, populated at the single
    construction site in `engine/research_pipeline.py`. Version/name
    read from `core/version.py`, never reinvented. "Fuentes
    consultadas" and a per-instance "funciones ejecutadas" field
    deliberately left out -- reasons documented in the class
    docstring, not silently skipped. Noted, not fixed: `core/version.py`'s
    `CONSTITUTION_VERSION` still points at a 12-article document that
    doesn't exist as a file yet. Full details in the Design Decision
    entry above (RE-044.4). Full `tests/verify_*.py` suite re-run:
    same four pre-existing failures, nothing new; `run.py` unchanged.

## Version 1.96

-   RE-044.3: removed dead, broken architecture (Articulo 3) --
    `models/dataset.py`'s ten unused statistical/filter methods
    (leftover from the retired `ProbabilityEngine` stage) and
    `core/dataset_builder.py`'s `DatasetBuilder`, which was not just
    unused but broken two independent ways (wrong `Episode` fields,
    wrong `Dataset` constructor call). Armando's explicit decision:
    remove, don't repair, don't relocate -- rebuilding logic with no
    real consumer is the same pattern already rejected for X/Y/Z.
    `tests/verify_core.py`'s existence-only check for the deleted file
    removed. Full details in the Design Decision entry above
    (RE-044.3). Full `tests/verify_*.py` suite re-run: same four
    pre-existing failures, nothing new; `run.py` unchanged.

## Version 1.95

-   RE-044.2: centralized scattered magic numbers (Articulo 7, second
    clause). `MIN_DRAWDOWN` and the default 10-match sample size were
    each repeated independently across up to five files. Both now
    live once in `core/constants.py`; `engine/drawdown_engine.py`
    re-exports `MIN_DRAWDOWN` unchanged so `engine/live_episode.py`
    and `engine/human_approval_state.py` (which import it directly,
    and which RE-032.4's market-crisis definition depends on) needed
    no changes. Zero behavior change, confirmed by full test re-run
    including both of those consumers specifically. Full details in
    the Design Decision entry above (RE-044.2).

## Version 1.94

-   RE-044.1: unified categorical Confidence (Articulo 7 of the
    Research Engine's 12-article founding constitution, audited for
    the first time this session). `core/confidence.py` was empty;
    found two independent, disconnected confidence computations
    instead of one gap. Armando chose to unify (Option A) over
    keeping both separately documented (Option B). `run.py`'s printed
    "Confianza" reading changed from `BAJA` to `ALTA` for today's real
    snapshot as a direct, verified consequence -- not a side effect
    that slipped through. `stability`'s placeholder (hardcoded 1.0,
    unimplemented) is inherited into the new path, documented, not
    resolved. Full details in the Design Decision entry above (RE-044.1).
    Full `tests/verify_*.py` suite re-run: same four pre-existing
    failures, nothing new.

## Version 1.93

-   RE-043.4: corrected a stale docstring claim in
    `engine/personal_capacity_facts_gate.py` ("Still not wired into
    run.py, DecisionEngine or gate_combination.py", left over from
    RE-032.5). The gate has in fact been wired into
    `gate_combination.py` since RE-040.1, via
    `engine/posture_mapper.py`. Confirmed by reading
    `posture_mapper.py::evaluate_capital_posture()` and
    `gate_combination.py::combine_gate_outputs()` directly, and by
    `audit_posture.py`'s observed behavior all session ("COMBINED
    posture ceiling" includes Personal Capacity Facts explanations
    per patrimonio). Docstring updated to name the actual wiring path;
    "not wired into run.py or DecisionEngine" remains true and
    unchanged. Documentation only -- no logic touched.
    `tests/verify_personal_capacity_facts_gate.py` re-run: no change
    in output.

## Version 1.92

-   First real Human Approval attestation loaded for `AML`:
    2026-08-13, `Conserve`, no personal crisis declared, techo 90% not
    applicable (only meaningful for `Deploy Aggressively`). Unlike
    AMS's `Deploy Aggressively` attestation, `Conserve` is the
    implicit floor -- not a tolerance increase from nothing, so the
    cooling-off rule does not apply. Verified via `audit_posture.py`:
    `Human Approval state (AML): valid`, `blocked: False`,
    `effective_posture_ceiling: Conserve`, explanation confirms "does
    not increase tolerance relative to the implicit Conserve baseline
    -- applies immediately, no cooling-off". Both patrimonios now
    carry a real, non-empty attestation history for the first time.
-   `tests/verify_human_approval_state.py` updated again: `AML`'s
    "real pipeline" assertions moved from asserting `MISSING`/empty to
    asserting `VALID`/not blocked/`Conserve`, matching the loaded row.
    Unused `MISSING` import dropped. Full suite re-run: same four
    pre-existing failures, nothing new.

## Version 1.91

-   RE-043.2: `loaders/personal_capacity_facts_loader.py`'s
    `RESERVED_SHEETS` extended from `{"Notas"}` to
    `{"Notas", "Cajas", "Proyecciones"}`. Found running
    `audit_posture.py` for real for the first time since those two
    tabs were added (2026-08-13, SOP-level work, not previously
    exercised end-to-end): both were being auto-treated as
    patrimonios, per the RE-043.1 convention that any non-reserved
    sheet in `personal_capacity_facts.xlsx` is one. `Cajas` and
    `Proyecciones` are derived views over AMS/AML, not a patrimonio --
    reserved for the same reason `Notas` is. One-line fix; verified
    `audit_posture.py` now lists only `AMS`/`AML` again, and
    `tests/verify_personal_capacity_facts_gate.py` still passes
    unchanged.
-   First real Human Approval attestation loaded:
    `data/raw/human_approval_attestations.xlsx`, `AMS`, 2026-08-13 --
    `Deploy Aggressively`, no personal crisis declared, techo 90% no
    autorizado. First-ever attestation for this patrimonio counts as a
    tolerance increase from nothing, so it entered 14-day cooling-off
    (not 30 -- no crisis declared), effective 2026-08-27. Verified via
    `audit_posture.py`: `Human Approval state (AMS): under_cooling_off`,
    `blocked: True`, `pending_increase` correctly shows the
    2026-08-27 effective date. `AML` remains empty -- no attestation
    registered for it yet.
-   `tests/verify_human_approval_state.py` updated: the "real pipeline"
    section no longer assumes both patrimonios are empty. `AML` keeps
    asserting empty/`MISSING`. `AMS` now asserts the loaded row's
    contents and that its gate state is either `UNDER_COOLING_OFF` or
    `VALID` (not pinned to one, so the test does not go stale the
    moment 2026-08-27 passes and the attestation naturally becomes
    valid). Full `tests/verify_*.py` suite re-run: no new failures
    beyond the same four pre-existing ones (runtime-pin mismatches on
    `verify_baseline_harness.py` / `verify_secondary_baselines.py` /
    `verify_validation_metrics.py`, and `verify_research_engine.py`'s
    known tie-break ordering difference).

## Version 1.90

-   Added RE-032.10 iteration B: `data/raw/human_approval_attestations.xlsx`
    gets a real column E (`Autoriza techo 90%...`, `Sí`/`No` dropdown,
    styled to match the sheet) on both `AMS` and `AML`, plus an
    explanatory block on the `Notas` tab. `loaders/human_approval_loader.py`
    reads it; `engine/human_approval_state.py` parses it into
    `Attestation.authorizes_dry_powder_ceiling_90` (via
    `_to_bool_si_no`, renamed from `_to_bool_crisis_declared` and
    reused rather than duplicated). Passed through unconditionally,
    even on non-`Deploy Aggressively` rows -- gating on posture stays
    `engine.human_approval`'s job alone.
-   Added RE-032.10 iteration C: `dry_powder_protocol.py` now computes
    tranches by formula up to a 90% extended ceiling
    (`CEILING_FRACTION_AGGRESSIVE_EXTENDED`) when
    `human_approval_above_ceiling` is `True` and the ratchet's ceiling
    posture is `Deploy Aggressively` -- never 100%, never applies to
    `Deploy Partially`'s 40% ceiling, never stacks with the base 80%.
    This retires `CEILING_REACHED_APPROVED` as a reachable status
    (kept defined for schema stability, no longer produced) -- flagged
    explicitly as a real behavior change, not a silent one.
    `audit_posture.py` reads `human_approval_above_ceiling` from
    `ha_result.authorizes_dry_powder_ceiling_90` for real now, `False`
    if no Human Approval result exists for the patrimonio (fail-closed
    unchanged). Verified end-to-end via `audit_posture.py` on the real
    (still-empty) pipeline.
-   `tests/verify_human_approval_state.py` extended (new field on
    existing synthetic rows, plus a non-`Deploy Aggressively` pass-
    through case). `tests/verify_dry_powder_protocol.py`'s old
    `ceiling_approved` case (asserted `CEILING_REACHED_APPROVED`)
    replaced by four new cases covering the extended ceiling's full
    behavior (within-band, trimmed, hard stop at 90%, ignored on
    `Deploy Partially`). Full suite re-run: no new failures beyond the
    same four pre-existing ones.
-   Manual operativo (`docs/MANUAL_OPERATIVO.md`/`.docx`) Section 2
    precision pass, from Armando's own critical review of the
    just-shipped rewrite: explicit contrast between Human Approval's
    calendar-date format and Dry Powder's Shiller-decimal format (2.5);
    clarified the `Fecha` column means the day of the attestation, not
    the day cooling-off ends (2.5); noted that renewing the same
    posture resets the 90-day validity clock immediately (2.2, rule
    4); added an explicit "don't try to force the >80% exception"
    bullet to the quick checklist (2.7). No iteration D yet -- the
    "not usable yet" callout in 2.5 is now factually stale as of this
    same version (B+C closed it) but is deliberately left untouched
    until iteration D updates it properly, not as a side effect here.
-   Updated Honest Progress Snapshot (RE-DOC-005): Dry Powder Protocol
    and Human Approval operativo real, both reflecting B+C closed.

## Version 1.89

-   Added RE-032.10 (iteration A of D): `authorizes_dry_powder_ceiling_90`
    added to `Attestation`/`HumanApprovalResult` in
    `engine/human_approval.py` -- pure logic only, closing a gap
    `audit_posture.py` already documented honestly at RE-032.8 (Human
    Approval could never actually record authorizing Dry Powder
    Protocol beyond its 80% ceiling). Full design negotiated point by
    point with Armando before coding: ceiling moves 80% -> 90% (never
    100%, never a euro amount), lives on the same `Deploy Aggressively`
    row, fixed independent 30-day cooling-off, can be registered
    pre-emptively, deliberately no market-episode coupling (already
    covered for free by `dry_powder_protocol.py`'s own call
    structure), can never take effect before its own base posture.
-   Four new test cases in `tests/verify_human_approval.py`, one per
    acceptance check agreed before coding. Full suite re-run: no new
    failures beyond the same four pre-existing ones.
-   No change yet to the xlsx, loader, `human_approval_state.py`,
    `dry_powder_protocol.py`, `audit_posture.py`, or the manual
    operativo -- iterations B/C/D, explicitly deferred.
-   Updated Honest Progress Snapshot (RE-DOC-005): Human Approval
    operativo real, noting iteration A closed.

## Version 1.88

-   Added RE-036.2: corrected a false claim in `REGIME_DIMENSIONS`'s
    comment (`engine/regime_comparability_gate.py`) -- it said
    cape/inflation/interest_rate were chosen because none are
    consumed by `SimilarityEngine`, contradicted two lines later by
    the same comment naming cape as one of `SimilarityEngine`'s own
    score inputs. Documentation-only, the last of the three findings
    from today's cold critical review (RE-032.9, RE-041.8 already
    closed). Confirmed it's wording only, not a design gap -- cape
    serving two independent purposes (ranking matches vs. checking
    today's raw value against the matches' range) does not violate
    RE-031.1's ban on using `SimilarityEngine` as a comparability
    proxy. No test changes, no behavior changed.

## Version 1.87

-   Added RE-041.8: fixed a real correctness gap in
    `compute_ledger_episode_state()` (`engine/dry_powder_ledger_state.py`),
    found by Armando in a second cold critical review he requested of
    the full day's work. A tranche row with a valid fecha/importe but a
    missing or unrecognized postura was silently excluded from
    `highest_posture_in_episode` with no trace in `explanations` --
    unlike fecha/importe on the same row, which already produce
    explicit skip-explanations when malformed.
-   Fixed by appending an explanation whenever postura doesn't
    resolve, without changing importe/cum_deployed_in_episode behavior
    -- the money still counts, only the missing explanation was added.
    Deliberately not the same shape as `human_approval_state.py`'s
    row-skip for unrecognized posturas: an attestation IS its posture,
    a tranche is real deployed money regardless of whether its posture
    field was legible.
-   Added one new case to `tests/verify_dry_powder_ledger_state.py`
    proving the fix. Full suite re-run: no new failures beyond the
    same four pre-existing ones.
-   Updated Honest Progress Snapshot (RE-DOC-005): Dry Powder --
    rastreo de episodio en vivo, noting the fix.

## Version 1.86

-   Added RE-032.9: fixed a real correctness bug in
    `HumanApprovalGate.evaluate()`, found by Armando in a deliberate
    critical re-read of RE-032.6/RE-032.7 he explicitly requested, not
    caught during original design. The gate compared the latest
    attestation only against the raw immediately-preceding row
    (`attestations[-2]`), which allowed a tolerance-increasing
    revision to bypass cooling-off entirely whenever its immediate
    predecessor had itself never taken effect (e.g. was still under
    its own cooling-off when superseded) -- exactly the self-gaming
    pattern this mechanism exists to prevent.
-   Fixed with a new `_resolve_effective()` that walks the full
    chronological attestation history, simulating cooling-off and
    90-day expiry at every step, instead of a two-row lookback.
-   Added two adversarial test cases to
    `tests/verify_human_approval.py` reproducing the exact bypass and
    proving it is closed. All ten pre-existing cases re-verified
    unchanged. Full suite re-run: no new failures beyond the same four
    pre-existing ones.
-   Updated Honest Progress Snapshot (RE-DOC-005): Human Approval
    operativo real raised 55-60% → 60-65%, noting the fix.

## Version 1.85

-   New standing convention, requested by Armando: every xlsx this
    project creates or edits gets `wrap_text=True` applied on write --
    long cell text (explanatory notes especially) wraps inside the
    cell instead of spilling across the row. Applies going forward
    automatically, not just when asked.
-   Applied retroactively to the three existing project xlsx files
    (`dry_powder_ledger.xlsx`, `human_approval_attestations.xlsx`,
    `personal_capacity_facts.xlsx`) -- cosmetic only, no data changed
    (commits `bc4c965`, `6503f12`).
-   Self-caught mistake in the same pass, recorded rather than
    smoothed over: the first attempt re-saved all three files with
    plain `openpyxl.Workbook.save()`, which does not recalculate
    formulas -- this silently dropped the cached value of every
    formula cell (`personal_capacity_facts.xlsx`'s "Gap anual",
    "Suelo de liquidez total", etc.), and
    `tests/verify_personal_capacity_facts_gate.py` immediately caught
    it (`ams_real_state` came back `not measurable` instead of
    `adequate`). Same class of bug this project has hit before with
    this exact save path. Fixed within the same turn, before handing
    anything to Armando, using the established LibreOffice
    `--convert-to` recalculation workaround (`--outdir` to a scratch
    directory, then copied back -- writing to the same path LibreOffice
    is reading from had failed outright). Full suite re-verified clean
    afterward.
-   No governance-doc entry existed for these two commits until this
    one -- added after the fact rather than left undocumented.

## Version 1.84

-   Added RE-032.8: `audit_posture.py` now prints Human Approval state
    per patrimonio, using the real
    `data/raw/human_approval_attestations.xlsx`. Today: `missing`,
    blocked, for both AMS and AML.
-   Printed as a block fully separate from `COMBINED posture ceiling`
    -- RE-032.4 rule 1 (not a scored gate, never blended into
    `evaluate_capital_posture()`'s combination) -- and not fed into
    `human_approval_above_ceiling` either, since that parameter answers
    a narrower question (explicit authorization beyond the 80% Dry
    Powder ceiling) that a general "is there a valid attestation"
    result does not answer.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones. The `personal_capacity_facts.xlsx` sandbox
    lock noted in RE-032.6/RE-032.7 has cleared.
-   Updated Honest Progress Snapshot (RE-DOC-005): Human Approval
    operativo real 45-50% -> 55-60%.

## Version 1.83

-   Added RE-032.7: `data/raw/human_approval_attestations.xlsx` (new,
    AMS/AML/Notas), `loaders/human_approval_loader.py`,
    `engine/human_approval_state.py`
    (`build_local_human_approval_inputs()`). Ledger records only what
    Armando alone can know (date, approved posture, personal crisis
    declared, note) -- no expiry/cooling-off/validity columns, per his
    own caution that the xlsx is data, not logic.
-   `market_crisis_at_registration` resolved per attestation via
    `engine.live_episode.drawdown_at_month()` against
    `MIN_DRAWDOWN` -- RE-032.4's own literal definition, no duplicated
    threshold logic.
-   Two extraction-only refactors: `engine.live_episode.calendar_date_to_shiller_month()`
    and new `engine/manual_entry_parsing.py`
    (`to_float_or_none()`/`to_calendar_date_or_none()`) --
    `dry_powder_ledger_state.py` now imports both instead of keeping
    private copies. No logic change, verified against its existing
    tests before proceeding.
-   Fail-closed on malformed rows: unparseable dates/unrecognized
    postures are skipped with a printed explanation, never guessed.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones and the still-unresolved
    `personal_capacity_facts.xlsx` sandbox lock noted under RE-032.6.
-   Updated Honest Progress Snapshot (RE-DOC-005): Human Approval
    operativo real 20-25% -> 45-50%.

## Version 1.82

-   Added RE-032.6: `engine/human_approval.py`
    (`HumanApprovalGate.evaluate()`) -- first code for RE-032.4's
    attested-judgement channel/Human Approval boundary. Pure logic, no
    I/O, no storage, not wired anywhere.
-   Resolved a real contradiction between RE-032.4's rules 5 and 7
    (cooling-off blocking vs. "previous attestation remains in force")
    with Armando directly: cooling-off delays effectiveness, never
    invalidates a still-valid predecessor; `under_cooling_off` only
    blocks when no valid predecessor exists. Pending revisions surface
    via a separate `pending_increase` field, not folded into state.
-   Resolved a genuine gap: a first-ever attestation is measured
    against an implicit `Conserve` baseline, so a first attestation
    above `Conserve` goes through cooling-off too, same as any
    revision.
-   `market_crisis` deliberately not recomputed -- reuses
    `engine.live_episode`'s existing `Drawdown <= MIN_DRAWDOWN` check
    (RE-041.2) via a per-attestation `market_crisis_at_registration`
    fact, resolved by a future adapter using
    `engine.live_episode.drawdown_at_month()` (RE-041.7).
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones.
-   Updated Honest Progress Snapshot (RE-DOC-005): Human Approval
    operativo real 0-5% -> 20-25%.

## Version 1.81

-   Added RE-041.7: `engine/live_episode.py` gains
    `load_prepared_shiller_df()` (extracted, no logic change) and
    `drawdown_at_month()`. `dry_powder_ledger_state.py::compute_ledger_episode_state()`
    gains an optional `shiller_df` param and now computes
    `drawdown_pp_since_last_deployment` as `(drawdown_then -
    as_of_drawdown) * 100`, clamped at 0.0 -- a partial market recovery
    since the last tranche must never count as additional drawdown.
    `build_local_dry_powder_ledger_state()` loads Shiller once, reuses
    it for both episode detection and this lookup.
-   Backward compatible: `shiller_df=None` preserves RE-041.4's exact
    prior behaviour.
-   Fixed a latent test bug unrelated to this iteration's logic:
    `tests/verify_dry_powder_ledger_state.py` hardcoded "today" as a
    literal date while also depending on the real clock -- broke one
    day after RE-041.6 shipped, caught while verifying this iteration.
    Fixed with an explicit fixed `as_of_calendar_date`.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones. Noted, not fixed: `data/raw/personal_capacity_facts.xlsx`
    hit a transient iCloud filesystem lock in the sandbox during this
    session's verification (`OSError: Resource deadlock avoided`),
    unrelated to any file this iteration touched.
-   Updated Honest Progress Snapshot (RE-DOC-005): Dry Powder --
    rastreo de episodio en vivo 70-75% -> 85-90%.

## Version 1.80

-   Added RE-041.6: "Activo / Instrumento" column (E) in
    `data/raw/dry_powder_ledger.xlsx` Section 2 -- Armando's own catch
    that the ledger had no place to record what was actually bought.
    Confirmed optional for the protocol's math, real value as an audit
    record. Appended rather than inserted, to avoid a width conflict
    with Section 1's shared columns.
-   `loaders/dry_powder_ledger_loader.py` now reads it into each
    tranche dict as `"activo"` -- not consumed by any calculation.
-   Corrected a real misreading of Section 1 surfaced in the same
    conversation: the episode-start date is
    `engine.live_episode.CurrentEpisode.peak_date` (the market's last
    high before the drawdown), not "the day you happen to check."
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones.

## Version 1.79

-   Added RE-041.5: `engine/dry_powder_ledger_state.py::to_dry_powder_protocol_inputs()`
    -- merges LedgerEpisodeState with a caller-supplied current_posture
    and human_approval_above_ceiling (default False) into a real
    DryPowderProtocolInputs. Returns None (never a guessed value) when
    nothing is resolved enough to evaluate.
-   `audit_posture.py` now runs Dry Powder Protocol per patrimonio
    using the same combined posture it already prints -- full chain
    (live episode -> ledger -> combined posture -> protocol) now
    demonstrated end-to-end in one script. Still read-only, still not
    wired into run.py/DecisionEngine.
-   Run against real data today: both AMS and AML print "not
    evaluated," consistent with RE-041.2's finding that no episode is
    active.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones. `audit_posture.py` re-run directly and confirmed.
-   Updated Honest Progress Snapshot (RE-DOC-005): Dry Powder --
    rastreo de episodio en vivo 55-60% -> 70-75%.

## Version 1.78

-   Added RE-041.4: `loaders/dry_powder_ledger_loader.py` (raw I/O) +
    `engine/dry_powder_ledger_state.py`
    (`compute_ledger_episode_state()`, `build_local_dry_powder_ledger_state()`)
    -- joins RE-041.2's live episode detection with RE-041.3's manual
    ledger to produce `has_active_episode`, `initial_dry_powder`,
    `remaining_dry_powder`, `cum_deployed_in_episode`,
    `days_since_last_deployment`, `highest_posture_in_episode` per
    patrimonio.
-   Two fail-closed rules made explicit: stale/mismatched episode
    marker -> initial dry powder treated as unknown, never a stale
    figure; no tranches logged yet -> highest_posture_in_episode
    defaults to Conserve, no unearned ratchet credit.
-   `drawdown_pp_since_last_deployment` explicitly NOT computed this
    iteration (needs a month-level Shiller lookup, deferred) -- always
    None, documented as a known gap, safe because cadence is days OR
    drawdown-points.
-   Corrected `data/raw/dry_powder_ledger.xlsx` Section 2's header
    wording (real calendar date, not Shiller AAAA.MM) before any real
    data existed -- flagged to Armando before editing, confirmed.
-   Does not assemble `DryPowderProtocolInputs` and does not wire into
    anything -- `current_posture`/`human_approval_above_ceiling`
    remain a future caller's responsibility.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones.
-   Updated Honest Progress Snapshot (RE-DOC-005): Dry Powder --
    rastreo de episodio en vivo 35-40% -> 55-60%.

## Version 1.77

-   Added RE-041.3: `data/raw/dry_powder_ledger.xlsx` -- new file, no
    code. Manual ledger for the five `DryPowderProtocolInputs` fields
    no market data can supply: episode start date + initial Dry Powder
    (Section 1, filled once per episode), and an append-only tranche
    log (Section 2: date, amount, posture-at-execution via a
    data-validation dropdown, note).
-   Kept separate from `personal_capacity_facts.xlsx` (static snapshot
    vs. append-only log) -- same reasoning flagged to Armando before
    building, confirmed by him.
-   Both patrimonio tabs (AMS, AML) start with Section 1 at
    `Pendiente` and Section 2 empty -- consistent with RE-041.2's
    finding that no episode is active today.
-   No loader, no adapter, no wiring -- file structure only, per this
    session's one-file-per-iteration discipline.
-   Updated Honest Progress Snapshot (RE-DOC-005): Dry Powder -- rastreo
    de episodio en vivo 25-30% -> 35-40%.

## Version 1.76

-   Added RE-041.2: `engine/live_episode.py`
    (`detect_current_episode()`, `run_live_episode_detector()`) --
    detects whether a market drawdown episode is currently active and
    since when, purely from Shiller data, no state, no ledger.
-   Mirrors `drawdown_engine.py::detect_drawdowns()`'s state machine
    rather than reusing it directly, because that function silently
    drops any episode still open at the end of the series (only
    appends on a Drawdown == 0 recovery row). Imports `MIN_DRAWDOWN`,
    `calculate_running_peak`, `calculate_drawdown` from
    `drawdown_engine.py` -- no edits to that file.
-   Confirmed against the real `data/raw/shiller.xlsx`: as of 2026.07
    (latest row), the market is exactly at its running peak -- no
    active episode today. `tests/verify_live_episode.py` asserts this
    real-pipeline result explicitly, noted as an assertion that should
    correctly start failing once a real drawdown begins.
-   Scoped explicitly to the two of seven `DryPowderProtocolInputs`
    fields that are honestly derivable from market data alone (is
    there an episode, since when). The other five -- dry powder
    figures and deployment history -- require a manually operated
    ledger only Armando can populate. Flagged before writing code;
    Armando chose an xlsx tab (not JSON) for that ledger, design
    deferred to a following iteration.
-   Full test suite re-run: no new failures beyond the same four
    pre-existing ones.
-   Updated Honest Progress Snapshot (RE-DOC-005): added "Dry Powder --
    rastreo de episodio en vivo" row, 25-30% (auto-detection done,
    manual ledger not yet built).

## Version 1.75

-   Added RE-041.1 (code): first isolated implementation of the Dry
    Powder Protocol -- `engine/dry_powder_protocol.py`,
    `tests/verify_dry_powder_protocol.py`. Stateless, pure function:
    tranche on remaining Dry Powder, dual cadence (days OR drawdown
    points), per-posture cumulative ceiling on the episode's initial
    Dry Powder, ratchet effect. v1 params: Deploy Partially 12%
    tranche / 40% ceiling / 30d or 5.0pp cadence; Deploy Aggressively
    22% tranche / 80% ceiling / 14d or 5.0pp cadence. Beyond 80%:
    blocked without a fresh Human Approval attestation, and even then
    the amount is left `None`, never computed by formula.
-   Two corrections made against Armando's detailed implementation
    spec, flagged and confirmed before writing code: (1) the ceiling
    posture is computed as `max(current_posture,
    highest_posture_in_episode)` via `POSTURE_ORDER`, closing an
    undefined branch in the drafted step-2 logic (first tick after
    escalating to Deploy Aggressively) -- this also surfaced and fixed
    a `KeyError` on posture `Blocked`, which `POSTURE_ORDER` does not
    rank; (2) status uses plain string constants, not `Enum`, matching
    every other gate in the project.
-   `tests/verify_dry_powder_protocol.py` follows the project's
    existing `verify_*.py` convention, not `pytest` (confirmed
    unused/uninstalled anywhere else in the repo).
-   Not wired into `posture_mapper.py`, `gate_combination.py`,
    `run.py` or `DecisionEngine`. No episode-state tracking -- still
    entirely the caller's responsibility.
-   Full test suite re-run: no new failures beyond the three
    pre-existing pinned-runtime mismatches and the pre-existing
    `match_bottoms` tie-order artifact.
-   Updated Honest Progress Snapshot (RE-DOC-005): Dry Powder Protocol
    60-65% especificación / 0% código -> 75-80% aislado / no wired.

## Version 1.74

-   Added RE-043.2: resolved the four remaining "Pendiente" cells left
    open by RE-043.1 (AMS income/portfolio concentration, AML
    portfolio concentration, known-horizon-event for both).
-   Verified AML's "repartido en 3 fondos" claim directly against `02.
    Fondos Myinvestor` before accepting it: two of the three funds
    track the same index, real split is ~91% effectively one
    US-large-cap bet (Vanguard 87.2% + Fidelity 0.4%) vs. iShares
    Developed World 4.0%. Reconciled exactly against the Resumen
    figure once the sheet's bundled cash (199.375€, matches
    Liquidez+Depósitos to the cent) is excluded. Presented to Armando
    before writing anything -- his final call (Adecuado, US/SP500
    concentration is the SOP's own thesis) stood, but the verification
    caught a materially incomplete picture first.
-   Verified Iberdrola's "10,6% dividend yield" is yield on cost basis,
    not current yield (~3,3% on today's market value) -- recorded with
    that distinction, not as a bare number.
-   Added AML's previously-uncaptured minusvalía (-162.000€, TEF).
    Both patrimonios' minusvalías now note the 4-year compensation
    window and that the credit expires unused if not applied in time.
-   Added an "Objetivo declarado" context row for AMS (close the
    7.000€/year gap with passive recurring income, not consultancy) --
    explicitly not a tenth gate field.
-   Result: both patrimonios now have all nine facts populated, zero
    "Pendiente" cells. AMS -> `ADEQUATE` (first time ever, real or
    synthetic, all nine favorable). AML -> `CONSTRAINED` with exactly
    one failed field and zero missing fields.
-   Updated `tests/verify_personal_capacity_facts_gate.py`'s
    real-pipeline expectations to match.
-   Updated Honest Progress Snapshot (RE-DOC-005): Personal Capacity
    operativo real 30-35% -> 45-50%.

## Version 1.73

-   Added RE-043.1: real `build_local_personal_capacity_facts_inputs()`
    adapter, generic across any number of patrimonio tabs
    (data/raw/personal_capacity_facts.xlsx), evaluated as independent
    capital postures per Armando's explicit decision -- AMS and AML
    never merged.
-   Defined, for the first time, the numeric/boolean threshold logic
    RE-032.3 explicitly deferred, for all nine verifiable-facts
    categories -- proposed, critiqued by Armando, and revised before
    being written.
-   Added `FIELD_INPUT_TYPES` taxonomy (COMPUTED / OPERATOR_FACT /
    OPERATOR_JUDGMENT) per field, the condition Armando set for
    green-lighting this iteration -- kept in sync with `FACT_FIELDS`
    by an assertion, not by convention.
-   Fixed a real bug caught by the first real-pipeline run: the
    "Pendiente" placeholder was initially read as confirmed content
    (`False`) instead of not-measured (`None`) for two new fields --
    corrected before being shipped.
-   Fixed a near-bug caught in review before it was written: an
    earlier draft hardcoded `debt_service_manageable = True` in Python
    instead of reading the Excel cell that already existed for it.
-   Fixed a fail-closed violation caught in review before it was
    written: an earlier draft defaulted missing fiscal-constraint data
    to `True`. Corrected to require an explicit token
    ("Ninguna conocida" / "Ninguno conocido"), blank = not-measured.
-   Added `loaders/personal_capacity_facts_loader.py` -- raw
    Concepto/Valor extraction, no interpretation, mirroring the
    `loaders/shiller_loader.py` split.
-   `audit_posture.py` now loops over every patrimonio and prints a
    combined posture per patrimonio. Real result today: AMS `not
    measurable` (four fields pending), AML `constrained` --
    `liquidity_adequate` breach, reproducing RE-042.1's manually-found
    result end-to-end through the automated pipeline for the first
    time.
-   Corrected a now-stale claim in `tests/verify_posture_mapper.py`
    that no real Personal Capacity Facts data source existed.
-   Updated Honest Progress Snapshot (RE-DOC-005): Personal Capacity
    definición 85-90% -> 90-95%; Personal Capacity operativo real
    15-20% -> 30-35%.
-   Three new spreadsheet cells added per patrimonio (portfolio
    concentration judgment, known-horizon-event fact, pending-fiscal-
    restriction fact); two existing cells renamed for lookup
    disambiguation.
-   Not wired into `run.py` or `DecisionEngine`. Attested-judgement /
    Human Approval channel (RE-032.4) remains entirely uncoded.

## Version 1.72

-   Added RE-042.1: real data captured for Personal Capacity Facts
    (RE-032.3) for both of Armando's real patrimonios (AMS/AML) --
    discussion-first, no code.
-   Unified liquidity model across both patrimonios: colchón (safety
    floor, never touched) + pólvora seca range with its own suelo/
    techo. AMS: colchón 30.000€, pólvora 70.000-120.000€. AML: colchón
    125.000€, pólvora 125.000-175.000€ (reproduces Armando's original
    250-300k total-liquidity figure exactly).
-   Surfaced a real open design question not anticipated by RE-032.3/
    RE-032.5: `LocalPersonalCapacityFactsInputs` is single-patrimonio
    in code, Armando manages two. Left explicitly open, not guessed
    at.
-   Concrete findings produced by the real numbers: AML's dry powder
    is 50.625€ below its own suelo (cushion intact, opportunity
    capital under-armed); AMS's liquidity is 22.330,77€ above its own
    techo (idle excess); two AML time deposits maturing 2026-08-26 and
    2026-09-29 flagged as the near-term source for its not-yet-
    operational Fondo Monetario.
-   AML's Planes de Pensiones (1.157.519,11€, 27,4% of net worth)
    confirmed permanently excluded from liquidity/dry powder -- both
    legally illiquid outside narrow exceptions and tax-punitive by
    design (withdrawal taxed as earned income, pushing combined
    marginal rate near 50%); earmarked as inheritance.
-   Deliverable: `data/raw/personal_capacity_facts.xlsx` (Notas/AMS/AML
    tabs, formulas not hardcoded values, cell-level source citations,
    recalculated via LibreOffice with zero formula errors across 37
    formulas).
-   Does not authorize: no adapter code exists yet
    (`build_local_personal_capacity_facts_inputs()` still absent), no
    resolution of the two-patrimonio dataclass question, no change to
    `PersonalCapacityFactsGate` or `posture_mapper.py`.
-   Updated Honest Progress Snapshot (RE-DOC-005): Personal Capacity
    definición 80-85% -> 85-90%; Personal Capacity operativo real
    5-10% -> 15-20% -- real validated data now exists, but zero
    automation and the multi-patrimonio question remain open.

## Version 1.71

-   Added RE-DOC-005: standing "Honest Progress Snapshot" section at
    the top of this document, updated at the end of every work session
    per Armando's explicit instruction.
-   Tracks two deliberately separate axes per block: design/
    specification completeness vs. real operational usability --
    collapsing them into one blended number would flatter readiness
    that does not exist, sharpest for Personal Capacity and Human
    Approval (code real and tested, zero real data or tooling behind
    it anywhere).
-   First snapshot recorded as of RE-030.3: Research Engine core 95%;
    Research Validation 100% technical / predictive validity not
    demonstrated; Evidence Quality Gate 75-80%; Regime Comparability
    Gate 75-80%; Personal Capacity definition 80-85% / operational
    5-10%; Gate Combination/Posture Mapper 75-80% isolated; Dry Powder
    Protocol 60-65% spec / 0% code; Portfolio Reallocation 0-5%; Human
    Approval spec 50% / operational 0-5%.
-   Documentation-only. No code.

## Version 1.70

-   Added RE-030.3: root cause of the `EXPECTED_LOCAL_CONSISTENCY`
    drift (B1) found and corrected, closing the last open item from
    this session's roadmap.
-   Systematically ruled out, with direct evidence: floating-point
    tie-flip at the match-set boundary (actual gap 0.019, far too large
    for cross-version noise), `SimilarityEngine` sort nondeterminism
    (confirmed stable), a Shiller data file change (exactly one commit
    in its entire history), and a `core/constants.py` weights/scales
    change (only ever an additive, unrelated change).
-   Found the real cause: RE-BUG.2's calendar-month duration fix sits
    chronologically between RE-030.2 (set the now-stale expected value)
    and RE-035.1 (measured the drift). It corrected `duration_months`,
    which feeds `SimilarityEngine`'s ranking directly, shifting the
    top-10 match set. RE-BUG.3 updated three other verification suites
    after the fix but missed this one.
-   Corrected forward (RE-DOC-002): `EXPECTED_LOCAL_CONSISTENCY` updated
    to `0.9524468147359584` with root cause recorded inline.
    `EXPECTED_LOCAL_COVERAGE`/`EXPECTED_LOCAL_DIVERSITY` checked and
    confirmed unaffected.
-   Also corrects an earlier, mistaken working note that no git history
    existed for the Shiller data file -- that was sandbox `git log`
    instability on path-filtered queries, not a real absence of
    history.
-   Closes Task #11 and the last remaining open item from this
    session's fixed priority list. No other open items remain except
    ones explicitly deferred by design (Personal Capacity's attested
    channel has no code, by design; Dry Powder Protocol numbers are
    v1, explicitly revisable).

## Version 1.69

-   Added RE-041.1: Dry Powder Protocol specification, filling in
    RE-033.1's two deferred numbers (`Deploy Partially`'s bounded
    fraction, `Deploy Aggressively`'s maximum amount).
    Documentation-only -- no code, no operative wiring.
-   Mechanism: tranches sized on remaining Dry Powder (not initial
    balance), dual cadence (minimum days OR additional drawdown
    points, reusing RE-032.4's `Drawdown` field), per-posture
    cumulative ceiling as a backstop (not the everyday control),
    ratchet with reset only at a new episode, and a hard stop beyond
    the `Deploy Aggressively` ceiling requiring a fresh Human Approval
    attestation (RE-032.4) rather than a new mechanism.
-   v1 parameters: Partially 12%/tranche, 40% cumulative cap, 30-day/
    5pp cadence; Aggressively 22%/tranche, 80% cumulative cap, 14-day/
    5pp cadence. Never 100% by formula alone. Explicitly a priori, not
    calibrated against the 19-episode sample.
-   Explicitly documents that under today's real Evidence Quality
    state (`not measurable`), this protocol cannot trigger regardless
    of drawdown depth -- built as forward infrastructure, not for
    immediate effect.
-   Design process recorded: an earlier draft using a single cadence
    for both postures was rejected for a specific technical reason
    (it would have dropped the intensity-escalates-with-posture
    principle), separate from noting that its self-congratulatory
    framing was itself a caution sign. Its one good idea -- requiring
    explicit unlock beyond the ceiling -- was kept and tied to the
    existing Human Approval mechanism.
-   Closes the last item on this session's fixed priority list
    ("Dry Powder Protocol"). B1 (RE-030.2 consistency drift) remains
    the only other open, deliberately deferred item.

## Version 1.68

-   Added RE-040.1: wires RE-032.5's `PersonalCapacityFactsGate` into
    `engine/posture_mapper.py`. New `PERSONAL_CAPACITY_FACTS_POSTURE_
    CEILING` table (`not measurable`/`constrained` -> `Conserve`,
    `adequate` -> `Deploy Aggressively`, stricter default than Evidence
    Quality's `not measurable` -> `Prepare`).
-   New `personal_capacity_facts_to_gate_input()` translator.
    `evaluate_capital_posture()` gains an optional third parameter,
    default `None` -- omitted means no gate added, never a ghost
    placeholder.
-   `blocked` propagates directly from the facts gate's own
    emergency-reserve veto into `combine_gate_outputs()`'s existing
    `Blocked` short-circuit -- first real exercise of that mechanism.
    `explanations` copied through in full so the specific blocking
    cause stays visible in the combined result, not just the fact of
    being blocked.
-   Combined result remains, by construction, optimistic even with
    this third gate present -- the attested-judgement/Human Approval
    channel (RE-032.4) has no code and is never included.
-   `audit_posture.py` and the real-pipeline dry-run in `tests/verify_
    posture_mapper.py` deliberately left at two gates -- no real data
    source exists for the nine facts; disclaimer text updated to state
    this precisely.
-   New synthetic tests: per-state translation, blocked propagation,
    three-gate combined scenarios including the reserve-breach ->
    `Blocked` case with cause visible in explanations.
-   Design ambiguity flagged and resolved before writing code:
    `adequate -> Deploy Aggressively` documented explicitly as "this
    gate does not restrict," not as "authorizes aggressive deployment."

## Version 1.67

-   Added RE-032.5: first isolated code for Personal Capacity's
    verifiable-facts channel. New `engine/personal_capacity_facts_
    gate.py` -- nine `Optional[bool]` local inputs, uniform positive
    polarity, three states (`constrained`/`adequate`/`not measurable`).
-   Result includes `failed_fields`, `missing_fields` and
    `blocking_fields` explicitly, not just a state string.
-   Resolved RE-032.3's open question on Required Emergency Reserve:
    it counts toward the graded state like the other eight facts, and
    additionally sets an orthogonal `blocked` flag (reusing
    `GateCombinationInput.blocked`, RE-034.3) when breached -- both,
    not either/or. Documented as provisional: only this field is a
    hard blocker in this iteration; expanding to other fields is left
    open, explicitly not decided here.
-   No real-pipeline data source exists for any of the nine facts --
    stated explicitly; only synthetic verification
    (`tests/verify_personal_capacity_facts_gate.py`) is possible.
-   `tests/verify_core.py` updated to recognize the new file.
-   Not wired into `run.py`, `DecisionEngine`, `posture_mapper.py` or
    `gate_combination.py` -- integration is RE-040.x, still open.
-   Closes the first-code half of Path A opened this session; the
    attested-judgement channel is never computed, by design (RE-032.4).

## Version 1.66

-   Added RE-032.4: defines the attested-judgement channel's five
    categories and the full Human Approval procedural boundary in one
    iteration -- binary veto (not `min()`), 90-day fixed validity,
    explicit state taxonomy (`missing`/`valid`/`expired`/
    `under_cooling_off`), tolerance direction defined via RE-033.1's
    posture ordering.
-   Cooling-off is universal: 14 days on any tolerance-increasing
    revision, unconditionally -- not contingent on crisis detection.
    Extended to 30 days when `market_crisis` (objective, `Drawdown <=
    MIN_DRAWDOWN`) or `personal_crisis` (self-declared) is active.
    Tolerance-reducing revisions apply immediately, always.
-   Design correction made this session: an earlier draft made
    `personal_crisis` a required trigger for cooling-off. Rejected --
    it would have made protection depend on accurate self-detection at
    the exact moment self-detection is least reliable, reintroducing
    the vulnerability the mechanism exists to close. Fixed structurally
    by making the 14-day cooling-off unconditional; crisis signals only
    extend it, never gate it.
-   Explicitly documents `personal_crisis`'s unreliability relative to
    `market_crisis` as an accepted, permanent limitation -- not framed
    as solved.
-   Documentation-only. No code, no storage schema, no wiring.
-   Closes Path A's classification/definition arc (RE-032.2, RE-032.3,
    RE-032.4). Next: RE-032.5, first code for the facts-gate half.

## Version 1.65

-   Added RE-032.3: enumerates the nine verifiable-facts categories
    for Personal Capacity's computable channel (liquidity, near-term
    cash needs, fixed obligations, debt service, income concentration,
    portfolio concentration, required emergency reserve, known time
    horizon constraints, fiscal/operational constraints).
-   Each category gets an operational definition and a source
    classification (manual entry vs computable from an existing
    ledger) -- answers RE-032.1's open question directly.
-   Fiscal/operational constraints added as a ninth category, not in
    RE-032.1's original list -- distinct failure mode (paper liquidity
    that isn't real liquidity because of tax cost or lock-up).
-   Flags Required Emergency Reserve as a likely binary-breach case
    rather than a graded input, without deciding it -- deferred to
    RE-032.5.
-   Documentation-only. No thresholds, no code, no combination logic
    between categories.
-   Continues Path A; RE-032.4 (attested-judgement channel + Human
    Approval boundary, combined per the ordering correction agreed
    this session) is next.

## Version 1.64

-   Added RE-032.2: Personal Capacity classified as a mixed control --
    Armando's explicit decision, resolving RE-032.1's primary
    classification question.
-   Verifiable-facts channel (liquidity, debt service, concentration,
    etc.) -> future computable gate, combined via `min()` like Evidence
    Quality and Regime Comparability.
-   Attested-judgement channel (drawdown tolerance, psychological
    capacity, etc.) -> Human Approval prerequisite, never enters
    gate-combination math, never an automatic ceiling.
-   Answers directly one of RE-032.1's open questions: Personal
    Capacity participates in gate combination AND sits inside Human
    Approval -- split by channel, not either/or.
-   Documentation-only. No code, no new gate, no schema for which
    specific facts/attestations are collected, no Human Approval
    workflow mechanics defined -- all remain open for future
    iterations.
-   Starts Path A from the prior session's roadmap review.

## Version 1.63

-   Added RE-039.1: standalone `audit_posture.py` at repository root,
    extracting the real-pipeline audit dry-run already present in
    `tests/verify_posture_mapper.py` into its own entry point. No
    logic change -- same gates, same disclaimers, no assertions, can
    be run on its own without the full verification suite.
-   Placement mirrors `run.py`'s existing precedent: not listed in
    `tests/verify_core.py` (root-level entry scripts aren't "Core").
-   RE-038.1's real-pipeline values confirmed under Armando's pinned
    runtime, exact match to sandbox: `cape_covered=False,
    inflation_covered=True, interest_rate_covered=True`, state
    `not comparable`, combined posture ceiling `Conserve`.
-   Closes items B and C from the "seguimos, dime que tocaria hacer"
    path review (B: data-wiring hygiene, C: standalone posture audit
    tool). Path A (Personal Capacity classification) remains open,
    next only if there is time/energy in a future session.

## Version 1.62

-   Added RE-038.1: connected `inflation`/`interest_rate`, previously
    hardcoded `None` everywhere; corrected `inflation` from raw CPI
    level to a trailing 12-month rate.
-   Corrected forward (RE-DOC-002) a false claim in RE-036.1: these
    fields were never actually populated, despite that iteration's
    text saying so -- surfaced by RE-037.1's real audit dry-run.
-   `engine/drawdown_engine.py`: new `calculate_inflation_rate()`
    (`InflationRate1Y = CPI.pct_change(12)`), same pattern as
    `calculate_volatility()`. `filter_episodes()` now wires both
    fields from the dataframe instead of hardcoding `None`.
-   `engine/snapshot_engine.py`: `interest_rate` now wired to
    `Rate GS10`. Removed the leftover `POSIBLES COLUMNAS MACRO` debug
    print that appeared in every test run -- it had served its
    purpose (identifying the column).
-   Sandbox structural check (NOT canonical): before,
    `inflation_covered`/`interest_rate_covered` were both `None`; after,
    both measurable (`True`), leaving only `cape` as the real driver of
    `not comparable` -- a materially cleaner result.
-   No `SimilarityEngine` change -- neither field is consumed there.
-   Left the `EXPECTED_LOCAL_CONSISTENCY` drift (RE-030.2) and the
    CAPE/context NaN-filtering pattern explicitly untouched -- both
    out of scope for this iteration.

## Version 1.61

-   Added RE-037.1: first code implementation of RE-034.1/RE-034.5's
    posture-ceiling mapping tables.
-   Added `engine/posture_mapper.py`
    (`evidence_quality_to_gate_input()`, `regime_comparability_to_
    gate_input()`, `evaluate_capital_posture()`). Unrecognized gate
    states raise `ValueError` rather than silently defaulting.
-   Explicitly excludes Personal Capacity (RE-032.1 unclassified, no
    gate exists) -- stated in the module, not hidden; output is
    provably at least as permissive as a full combination would be.
-   Added `tests/verify_posture_mapper.py`: synthetic checks for every
    mapping row and combined scenario, plus a read-only audit dry-run
    against today's real snapshot using
    `PREDICTIVE_VALIDATION_NOT_DEMONSTRATED` (RE-PRED.16).
-   `tests/verify_core.py` updated to recognize
    `engine/posture_mapper.py` and (previously missing)
    `engine/gate_combination.py`.
-   Not wired into `run.py`, `DecisionEngine` or any operative flow --
    this is an isolated composition layer for audit purposes, not the
    Capital Posture Engine.
-   Real-pipeline dry-run not completed in sandbox this iteration
    (transient iCloud file-lock error, unrelated to the change);
    pending pinned-runtime confirmation.

## Version 1.60

-   Added RE-034.5: extended RE-034.1's provisional gate-ceiling mapping
    table with Regime Comparability's three real states from RE-036.1.
-   `not comparable` -> `Conserve` (confirmed extrapolation risk, at
    least as restrictive as `not measurable`).
-   `comparable` -> `Deploy Aggressively` (top of the ordered scale --
    the only way to encode "this gate imposes no restriction of its
    own" under min()-based combination; the real ceiling stays decided
    by Evidence Quality and Personal Capacity).
-   Closed RE-034.1's open question about a future non-deployment
    exception for Regime Comparability -- resolved by definition for
    `not measurable`, and by this new mapping for the other two states.
-   Documentation-only. No code changed. No wiring into
    `gate_combination.py` authorized.

## Version 1.59

-   Added RE-036.1: first implementation of the Regime Comparability
    Gate boundary from RE-031.1.
-   Added `engine/regime_comparability_gate.py`
    (`LocalRegimeComparabilityInputs`, `RegimeComparabilityGate`,
    `_dimension_covered()`, `build_local_regime_comparability_inputs()`).
-   Three active dimensions: `cape`, `inflation`, `interest_rate` --
    already populated in `Context` per episode, unused by
    `SimilarityEngine`'s score, no new data ingestion required.
-   Method: strict `[min, max]` coverage of today's snapshot value
    against the current match set's range for each dimension. No
    percentile or margin -- deliberately deferred until an actual
    small-N outlier problem is observed, not anticipated with
    unneeded complexity.
-   Fail-closed per RE-031.1: missing values produce `None`
    (not measurable), never treated as coverage or non-coverage.
-   Three gate states, specific to this gate, not reused from
    `EvidenceQualityGate`: `NOT_MEASURABLE`, `NOT_COMPARABLE`,
    `COMPARABLE`.
-   Added `tests/verify_regime_comparability_gate.py`.
-   `tests/verify_core.py` updated to recognize
    `engine/regime_comparability_gate.py` and (previously missing)
    `engine/evidence_quality_gate.py`.
-   Not wired into any operative flow. No entry added to RE-034.1's
    posture mapping table -- that remains a separate governance
    decision.
-   Structural verification only in this sandbox; real-pipeline
    values pending pinned-runtime confirmation.

## Version 1.58

-   Added RE-035.1: closed both hardcoded stubs in
    `engine/evidence_quality_gate.py`.
-   `independence_dispersion_measured` is now computed for real
    (pairwise outcome-window overlap across the current match set, same
    definition as RE-025.8) instead of hardcoded `False`. New field
    `overlapping_match_pairs` exposes the count.
-   Added `PREDICTIVE_VALIDATION_NOT_DEMONSTRATED` as a recognized
    `predictive_validation_status` value, producing a sharper
    explanation -- no new gate output state added, per RE-PRED.10.1.
-   Updated `tests/verify_evidence_quality_gate.py` accordingly; added a
    case exercising the `not_demonstrated` path.
-   Noted explicitly: this does not change today's system-level capital
    posture -- RE-034.1's mapping still caps at `Conserve` because
    Regime Comparability and Personal Capacity are entirely unbuilt.
-   Confirmed under `RUNTIME : PINNED`: `independence_dispersion_measured
    = True`, `overlapping_match_pairs = 5` on the real match set; the
    `not_demonstrated` explanation path fires correctly.
-   Logged a separate, pre-existing, unrelated finding: the existing
    `EXPECTED_LOCAL_CONSISTENCY` canonical value (RE-030.2) no longer
    matches the live pipeline (`0.9518456229064439` expected,
    `0.9524468147359584` produced). RE-035.1 does not touch consistency
    computation. Root cause not investigated; not fixed in this
    iteration, per RE-DOC-002.

## Version 1.57

-   Added RE-PRED.16: canonical dependence-aware bootstrap values,
    confirmed under `RUNTIME : PINNED`, closing RE-PRED.12.
-   Recorded canonical cluster structure: 3 independence clusters,
    sizes `[10, 8, 1]` -- not the 4 (`[10, 7, 1, 1]`) seen in
    RE-PRED.15's unpinned structural smoke test. Hand-verified against
    RE-025.8/RE-025.9's own canonical tables; discrepancy attributed to
    the unpinned sandbox producing slightly different forecast values,
    which changes `repeated_forecast_groups()`'s exact-float-equality
    grouping -- not a defect in the bootstrap code.
-   Recorded canonical 90% bootstrap intervals for MAE, hit-rate and
    rank correlation, for the model, both baselines, and their paired
    excess (seed=42, replicates=5000).
-   Found that MAE excess vs. both baselines is robust (does not
    straddle zero in either direction); hit-rate excess is exactly zero
    at every percentile against both baselines.
-   Found that rank-correlation excess vs. the primary baseline
    straddles zero -- RE-PRED.13's "model loses to primary on rank
    correlation" finding is not distinguishable from sampling noise.
-   Found that rank-correlation excess vs. mean-reversion does not
    straddle zero -- RE-PRED.13's full sign-flip finding is robust to
    the known N=19 dependence structure, not an artifact of it.
-   No code changed in RE-PRED.16. No gate state changed.

## Version 1.56

-   Added RE-PRED.15: Dependence-aware cluster bootstrap, closing the
    RE-PRED.12 method gap.
-   Added `engine/dependence_bootstrap.py`
    (`independence_clusters()`, `cluster_bootstrap_ci()`,
    `cluster_bootstrap_paired_excess()`) and
    `tests/diagnostic_dependence_bootstrap.py`, an exploratory,
    non-canonical, non-regression-gated script that still enforces the
    pinned-runtime check (RE-025.5).
-   Clusters built via connected components over the union of
    `overlapping_outcome_windows()` (RE-025.8) and
    `repeated_forecast_groups()` (RE-025.9) -- no new dependence
    criterion introduced, both edge sources already validated.
-   Bootstrap resamples whole clusters with replacement, never
    individual records, per RE-PRED.1's dependence-aware resampling
    requirement; i.i.d. resampling over the 19 records remains
    prohibited.
-   Paired excess resampling applies the identical cluster draw to
    model and baseline in the same replica, preserving paired variance
    structure.
-   Fixed, documented constants: `BOOTSTRAP_SEED=42`,
    `BOOTSTRAP_REPLICATES=5000`, 90% percentile interval.
-   `tests/verify_core.py` updated to recognize
    `engine/dependence_bootstrap.py`, per the RE-025.7/RE-PRED.9
    precedent.
-   Structural smoke test outside the pinned runtime, not canonical: 4
    independence clusters over the 19 evaluable records, sizes
    `[10, 7, 1, 1]`.
-   No Frozen Core component modified. No canonical interval values
    published yet -- pending pinned-runtime confirmation, to be
    recorded in a future iteration.

## Version 1.55

-   Added RE-PRED.14: Similarity dimension diagnostic.
-   Added `engine/dimension_diagnostic.py`
    (`dimension_forecast()`, `dimension_records()`,
    `DIMENSION_SCORE_FIELDS`) and
    `tests/diagnostic_similarity_dimensions.py`, an exploratory,
    non-canonical, non-regression-gated script that still enforces the
    pinned-runtime check (RE-025.5).
-   Reused `SimilarityEngine.compare()` unmodified; no Frozen Core
    component changed.
-   Excluded `recovery` from the diagnostic deliberately, per RE-021's
    existing data-leakage fix.
-   Found and fixed a bug in the new diagnostic script itself (not in
    `SimilarityEngine`): sorting by `pre_crash_return_3y_score` failed on
    `None` values; fixed by excluding `None`-scored comparables from
    that dimension's ranking, mirroring
    `SimilarityEngine._weighted_score()`'s existing `None`-exclusion
    rule.
-   Recorded canonical diagnostic results confirmed under
    `RUNTIME : PINNED`: no single active dimension reproduces
    mean-reversion's `+0.26316` rank correlation; all six remain
    negative, from `drawdown_score = -0.19692` to
    `pre_crash_return_3y_score = -0.26353`.
-   Concluded that the signal-dilution hypothesis registered in
    RE-PRED.13 is not supported.
-   Registered a revised hypothesis, explicitly not authorized as fact:
    the gap may be structural (nearest-neighbor selection vs. a direct
    monotonic function of the query's own value), not a dimension-
    weighting problem.
-   Reiterated RE-PRED.12's sampling-noise caveat with extra force for
    this smaller, still-dependent slicing.
-   No `SimilarityEngine` change made or authorized.

## Version 1.54

-   Added RE-PRED.13: Canonical secondary baseline values and
    full-picture finding.
-   Recorded canonical values confirmed under `RUNTIME : PINNED`:
    `zero_mae = 0.12749337012113`, `reversion_mae = 0.18158697149305`,
    `reversion_hit_rate = 0.94736842105263`,
    `reversion_rank_correlation = 0.26315789473684`.
-   Confirmed `zero_hit_rate`/`zero_rank_correlation = None` and
    `missing_reversion_forecast_count = 0`, exactly as expected by
    construction.
-   Recorded the full-picture finding: the model beats zero and
    mean-reversion clearly on MAE, ties all measurable baselines on
    directional hit-rate, and loses on rank correlation to both the
    primary baseline and mean-reversion — the mean-reversion case a
    full sign flip.
-   Evaluated the RE-PRED.10.1 deferral trigger explicitly: does not
    activate. `NOT_DEMONSTRATED` remains a deferred proposal.
-   Registered a working hypothesis, explicitly not authorized as fact:
    possible signal dilution in `SimilarityEngine`'s multidimensional
    weighting versus drawdown depth alone. No Frozen Core change made
    or authorized.
-   Reiterated that both new correlation values remain subject to
    RE-PRED.12's unresolved sampling-noise caveat.
-   No code changed.

## Version 1.53

-   Added RE-PRED.10.1: recorded and deferred a proposal to formalize
    `NOT_DEMONSTRATED` as a third `EvidenceQualityGate` output state.
    Deferral reasons: rests on one baseline over a non-independent N=19
    sample; no operative posture-ceiling consequence today versus the
    existing `not measurable` state; touches `GateCombination` taxonomy
    before a concrete behavioral reason exists. Recorded an explicit
    trigger for revisiting once secondary baselines are confirmed.
-   Added RE-PRED.11: implemented `zero_forecast()` and
    `mean_reversion_forecast()` (`-drawdown`, zero fitted parameters) in
    `engine/baseline_harness.py`, plus generic
    `build_baseline_records(model_records, forecast_fn)`. No existing
    function modified. Added `tests/verify_secondary_baselines.py`,
    re-asserting existing canonical values as a regression guard and
    printing the full three-way comparison table. No canonical
    secondary-baseline value established yet.
-   Added RE-PRED.12: recorded, as an explicit open question,
    that baseline-choice robustness (addressed by RE-PRED.11) and
    sampling-noise robustness (whether excess values are distinguishable
    from chance given N=19 dependent records) are different questions.
    The second remains unresolved and unauthorized for naive i.i.d.
    resampling, per RE-PRED.1.
-   No code changed in RE-PRED.10.1 or RE-PRED.12.

## Version 1.52

-   Added RE-PRED.10: Canonical baseline values and predictive-validity
    finding.
-   Recorded canonical baseline values confirmed under `RUNTIME : PINNED`:
    `baseline_mae = 0.06740858559979`,
    `baseline_hit_rate = 0.94736842105263`,
    `baseline_rank_correlation = -0.23171864780822`.
-   Recorded canonical excess values: `excess_mae = -0.00187935227097`,
    `excess_hit_rate = 0.00000000000000`,
    `excess_rank_correlation = -0.03333307069863`.
-   Confirmed `missing_baseline_forecast_count = 0` empirically under the
    pinned runtime, not only by construction.
-   Recorded the finding plainly, as committed to in advance in
    RE-PRED.7/RE-PRED.8: the model does not beat the primary baseline on
    any of the three canonical metrics — it ties on directional
    hit-rate and loses on MAE and rank correlation.
-   Stated that predictive validity, under RE-PRED.1's burden of proof,
    is not demonstrated relative to this baseline.
-   Connected this finding to the existing conservative
    `EvidenceQualityGate` state (RE-029.6/RE-029.7) as sharpening, not
    changing it — no gate threshold or capital posture ceiling is
    altered by this iteration.
-   No code changed.

## Version 1.51

-   Added RE-PRED.9: Primary baseline implementation.
-   Added `engine/baseline_harness.py`: `baseline_forecast()`,
    `BaselineHarness`, `missing_baseline_forecast_count()`,
    `excess_summary()`.
-   Added `tests/verify_baseline_harness.py`: functional smoke test,
    deliberately without hardcoded canonical baseline values.
-   Added `engine/baseline_harness.py` to `tests/verify_core.py`'s
    structural Engines list.
-   No Frozen Core component modified. No existing file modified except
    `tests/verify_core.py`'s structural list.
-   Reused `ObservableUniverse`, bottom_index self-exclusion and the
    existing MAE / hit-rate / rank correlation functions unmodified —
    no duplicated metric logic.
-   Proved by construction, and checked explicitly in the test, that a
    baseline forecast can never be `None` when the corresponding model
    record is evaluable.
-   Verified structurally (record alignment, evaluable-count alignment,
    the no-missing-forecast invariant) outside the pinned runtime only.
-   Explicitly did not hardcode canonical baseline metrics: RE-025.5
    already established that non-pinned runs can differ from the pinned
    canonical values, and treating a non-pinned result as canonical here
    would repeat the mistake RE-BUG.2 corrected. Canonical baseline
    values are deferred to RE-PRED.10, pending pinned-runtime
    confirmation.

## Version 1.50

-   Added RE-PRED.8: Primary baseline acceptance criteria.
-   Corrected RE-PRED.7's rank-correlation claim forward: the primary
    baseline is not a single global constant, so it does have rank
    variation and its rank correlation is a real, computable comparison
    against the model's — not an undefined quantity.
-   Defined the primary baseline as a point-in-time expanding median of
    `future_return_5y`, reusing `ObservableUniverse` and bottom_index
    self-exclusion — the same temporal-safety machinery already verified
    for the model's own forecast in RE-025.1.
-   Required the baseline to be evaluated over the exact same evaluable
    record set already used by `ValidationHarness` (19 records), not a
    separately invented sample.
-   Fixed median, not mean, as the primary baseline statistic, to keep
    the comparison against `Evidence.median_return` apples-to-apples.
-   Deferred secondary baselines (constant full-universe forecast, zero
    / no-change, mean-reversion) to a later iteration; required the
    constant full-universe forecast, if used later, to be labeled
    explicitly as not point-in-time-safe.
-   No code changed. No baseline value computed. No excess-return metric
    implemented.

## Version 1.49

-   Added RE-PRED.7: Absolute vs Excess Return Boundary.
-   Separated absolute return (existing Evidence descriptive surface,
    unchanged) from excess return over a naive baseline (future
    predictive-validity surface, not yet implemented).
-   Selected the unconditional historical mean/median `future_return_5y`
    as the primary baseline, evaluated point-in-time.
-   Kept constant full-universe forecast, zero/no-change and simple
    mean-reversion as secondary diagnostic baselines, per the RE-PRED.1
    mandatory-comparison requirement.
-   Defined per-metric excess mechanics: MAE and directional hit-rate
    need an explicit baseline forecast series; rank correlation already
    tests ordering against no signal and needs no separate excess
    transformation.
-   Established that excess return belongs to the Research Validation
    Harness, not to `Evidence` or `models/evidence.py`.
-   Recorded, in advance, that the most likely outcome once excess
    return is computed is that the primary baseline matches or beats the
    model on at least one canonical metric, given RE-025.3 and RE-BUG.3.
-   No code changed. No baseline value computed. No excess-return metric
    implemented.

## Version 1.48

-   Added RE-DATA.1: Shiller source update automation note.
-   Recorded that Shiller data updates remain manual today.
-   Recorded future automation as a validated data-update pipeline, not
    a blind network overwrite.
-   Required any future updater to validate workbook structure and
    `Price.1` semantics before replacing local data.
-   Required backup, test reruns and explicit update logging for any
    future automated refresh.
-   Deferred implementation until after RE-PRED target / baseline work
    is closed.
-   No code changed.

## Version 1.47

-   Added RE-BUG.3: Calendar-month duration fix impact record.
-   Documented that RE-BUG.2 fixed the verified calendar-month duration
    arithmetic bug in code.
-   Recorded that the fix affects active Similarity scoring through both
    duration and speed.
-   Recorded the current post-fix match set:
    `[2018.12, 1998.09, 1966.10, 2020.03, 1960.10, 1990.10, 2022.10,
    1962.06, 1880.05, 1903.10]`.
-   Established the post-fix canonical `Evidence.median_return` as
    `0.10192496249726091`.
-   Established the post-fix canonical Research Validation metrics:
    `mae = 0.06928793787076225`,
    `directional_hit_rate = 0.9473684210526315` and
    `rank_correlation = -0.26505171850684983`.
-   Recorded that pre-fix canonical values remain historical and are
    superseded forward, not silently rewritten.
-   Reaffirmed that the predictive-validity conclusion remains
    conservative after the fix.
-   No code changed in RE-BUG.3.

## Version 1.46

-   Added RE-BUG.1: Calendar-month duration bug acceptance criteria.
-   Classified the `duration_months` / `recovery_months` issue as a
    verified implementation bug, not a methodology question.
-   Marked the bug as near-term code-fix priority because it already
    affects public Evidence recovery statistics and active Similarity
    scoring.
-   Required future fix to use explicit calendar-month arithmetic rather
    than `YYYY.MM` float subtraction.
-   Required regression coverage for `1929.09 -> 1932.06 = 33 months`.
-   Required verification that all current episode durations and recovery
    durations are calendar-correct after the fix.
-   Required public Evidence recovery statistics to be recalculated from
    corrected values.
-   Required selected match identifiers to be compared before and after
    the future fix.
-   Required rerunning `verify_research_engine.py`,
    `verify_assessment_engine.py` and `verify_validation_metrics.py`
    after the future fix.
-   Required explicit reporting of any downstream Similarity or Research
    Validation metric changes caused by corrected duration arithmetic.
-   Prohibited mixing the bug fix with target-freeze, baseline, holdout
    or gate-threshold work.
-   No code changed.

## Version 1.45

-   Added RE-PRED.6: Bottom detection / episode boundary audit.
-   Documented current peak, drawdown, episode start, bottom, recovery,
    duration and target-anchor definitions from `engine/drawdown_engine.py`.
-   Confirmed that drawdown detection uses nominal price `P`.
-   Confirmed that target returns use `Price.1`, verified in RE-PRED.4
    as Real Total Return Price.
-   Recorded the price-basis asymmetry between nominal-price episode
    detection and real-total-return target measurement.
-   Recorded that unrecovered drawdowns are structurally excluded because
    episodes are appended only when `Drawdown == 0` recovery occurs.
-   Recorded that the current dataset has 23 episodes and all have
    recovery dates, so the structural exclusion does not currently create
    a missing active episode in the produced episode list.
-   Recorded a verified date-arithmetic bug: `duration_months` and
    `recovery_months` subtract `YYYY.MM` floats instead of calendar
    months.
-   Documented that the duration bug affects public Evidence recovery
    statistics and may affect Similarity.
-   No code changed.

## Version 1.44

-   Added RE-PRED.5: Target freeze acceptance criteria.
-   Ordered target-freeze criteria by dependency instead of presenting a
    flat checklist.
-   Clarified that source-column semantics are verified, but
    bottom-detection and episode-boundary semantics are not yet audited.
-   Required unit / horizon and absolute-vs-excess decisions before
    baseline design.
-   Prohibited closing baseline design before the absolute-vs-excess
    target decision is explicit.
-   Required a future missingness taxonomy distinguishing not-yet-
    matured outcomes, structurally missing data and source failure.
-   Referenced the RE-PRED.1 model-freeze checklist instead of
    duplicating it.
-   Added target unfreeze criteria and prohibited reopening the target
    because validation results are disappointing.
-   Preserved current `future_return_5y` as provisional freeze candidate
    only, not definitive frozen target.
-   No code changed.

## Version 1.43

-   Added RE-PRED.4: Source column semantics verification.
-   Verified directly against `data/raw/shiller.xlsx` that pandas
    `Price.1` corresponds to Shiller column J.
-   Recorded that rows 4-8 of the workbook header were inspected and no
    merged cells were present in that header area.
-   Verified column H / `Price` as Real Price from stacked labels
    `Real` / `Price`.
-   Verified column J / `Price.1` as Real Total Return Price from
    stacked labels `Real` / `Total` / `Return` / `Price`.
-   Promoted the previous RE-PRED.2 inference about `Price.1` to a
    verified fact.
-   Clarified that current `future_return_5y` is annualized real
    total-return CAGR from drawdown bottom over the five-year horizon.
-   Preserved the distinction between implemented target, provisional
    freeze candidate and definitive frozen target.
-   No code changed.

## Version 1.42

-   Added RE-PRED.3: Target freeze decision boundary.
-   Designated the current implemented target, `future_return_5y`, as
    the provisional freeze candidate.
-   Clarified that the target is not definitively frozen.
-   Clarified that `Price.1` source-column semantics are not yet
    verified and must not be described as real total-return until
    confirmed from an authoritative source.
-   Required future verification of whether `Price.1` represents real
    price, real total return, nominal price, nominal total return or
    another source-specific construct.
-   Preserved annualized CAGR as the provisional target form.
-   Added MAE reinterpretation: the canonical MAE is error over
    annualized CAGR, not cumulative five-year return.
-   Deferred absolute vs excess-return choice to future baseline design.
-   Preserved `bottom_date` as the provisional start anchor.
-   Recorded that live tracking should eventually distinguish not-yet-
    matured outcomes from structurally missing data and source failure.
-   No code changed.

## Version 1.41

-   Added RE-PRED.2: Predictive target audit.
-   Audited the current implemented target field: `future_return_5y`.
-   Documented that `_future_return()` computes annualized CAGR:
    `(p1 / p0) ** (1 / years) - 1`.
-   Documented that the current target uses Shiller `Price.1`.
-   Documented that the start anchor is `bottom_date` and the end anchor
    is the first available observation at or after `bottom_date + years`.
-   Documented missing-outcome behavior: future returns remain `None`
    when no mature future row exists or p0 is unavailable / zero.
-   Documented that current Evidence forecasts use
    `Evidence.median_return` over matched `future_return_5y` values.
-   Documented that current Research Validation compares
    `evidence.median_return` against each episode's realized
    `future_return_5y`.
-   Clarified that RE-PRED.2 audits the implemented target but does not
    freeze it or claim it is the final governance target.
-   No code changed.

## Version 1.40

-   Added RE-PRED.1: Predictive validity boundary.
-   Clarified that RE-PRED.1 makes no new predictive-validity claim and
    executes no new calculation.
-   Required a future predictive-target audit before freezing the target:
    return field, nominal vs real, price vs total return, horizon,
    date anchors, missing-data treatment and validation surface.
-   Separated future predictive claims into ranking validity,
    calibration validity and directional validity.
-   Separated validation surfaces into existing historical backtest,
    prospective holdout from freeze date and live tracking.
-   Documented that a retroactive clean holdout is not available by
    default because the Similarity Engine was designed while exposed to
    the historical dataset.
-   Required model freeze before any holdout or live-tracking result can
    count as clean predictive evidence.
-   Required future baseline comparisons to be pre-defined.
-   Required future uncertainty treatment to respect known dependence
    rather than assuming i.i.d. observations.
-   Defined minimum fields for a future append-only live-tracking log.
-   Recorded permanent weak predictive evidence as a named future design
    branch, not an implementation failure.
-   No code changed.

## Version 1.39

-   Added RE-034.4: Gate combination implementation status.
-   Documented that RE-034.3 added `engine/gate_combination.py` and
    `tests/verify_gate_combination.py`.
-   Recorded verified command:
    `python3 tests/verify_gate_combination.py`.
-   Recorded verified output: `GATE COMBINATION : STABLE`.
-   Updated Component Status from boundary-only to isolated
    Gate Combination Layer v0.
-   Clarified that the layer exists and passes verification but remains
    outside the operative flow.
-   Clarified that no Capital Posture Engine, thresholds, protocol rules,
    Human Approval implementation, live gate adapters or runtime wiring
    exist.
-   Preserved the current posture inference:
    `min(Prepare, Conserve, Conserve) = Conserve`.
-   No code changed in RE-034.4.

## Version 1.38

-   Added RE-034.2: Gate combination first-code acceptance criteria.
-   Required a regression test for the current real state:
    Evidence Quality `not measurable`, Regime Comparability
    `not measurable`, Personal Capacity unavailable / unclassified and
    `Blocked=false` must combine to `Conserve`.
-   Required a test proving that Evidence Quality does not override more
    restrictive gates.
-   Required a test proving that Evidence Quality `not measurable` caps
    at `Prepare`, not `Conserve`, when the other gates allow less
    restrictive posture.
-   Required unavailable Regime Comparability and unavailable Personal
    Capacity to cap at `Conserve`.
-   Required combined explanations to name the specific limiting gate or
    control.
-   Repeated first-code isolation boundaries: no `run.py`,
    `DecisionEngine`, `AssessmentEngine`, `ValidationEngine` or Frozen
    Core wiring.
-   No code changed.

## Version 1.37

-   Added RE-034.1: Gate combination boundary.
-   Defined combination inputs as discrete gate outputs: gate name,
    internal state, posture ceiling, `Blocked` flag and explanation.
-   Prohibited combination logic from consuming raw scores.
-   Defined combination order: `Blocked` wins first; otherwise the most
    restrictive ordered posture ceiling wins.
-   Separated non-deployment postures (`Conserve`, `Prepare`) from
    deployment postures (`Deploy Partially`, `Deploy Aggressively`).
-   Documented that Evidence Quality `not measurable` blocks deployment
    but does not necessarily block `Prepare`.
-   Documented the intentional asymmetry: unavailable Regime
    Comparability and unavailable / unclassified Personal Capacity cap
    at `Conserve`, while Evidence Quality `not measurable` caps at
    `Prepare`.
-   Added current-state inference:
    `min(Prepare, Conserve, Conserve) = Conserve`.
-   Clarified that Personal Capacity is included only as an unavailable
    placeholder until RE-032.1 classification is resolved.
-   No code changed.

## Version 1.36

-   Added RE-033.1: Capital Posture vocabulary and ordering.
-   Formalized ordered posture states from most restrictive to least
    restrictive: `Conserve`, `Prepare`, `Deploy Partially`,
    `Deploy Aggressively`.
-   Documented `Blocked` as an orthogonal veto outside the ordered
    posture scale.
-   Defined each posture state in terms of capital consequences.
-   Tightened `Prepare`: it may authorize planning and preparing Dry
    Powder capacity, but not selling existing strategic positions unless
    a future Dry Powder Protocol explicitly allows it.
-   Separated gate-internal state mapping from multi-gate posture-ceiling
    combination.
-   Documented that both `not measurable` and `conservative` currently
    cap at `Conserve`, while preserving different explanations.
-   Added current-state documentation inference: Evidence Quality not
    measurable, Regime Comparability not measurable and Personal Capacity
    unavailable imply `Conserve`.
-   Recorded the open question of whether measurable Evidence Quality is
    a prerequisite for any posture above `Conserve`.
-   No code changed.

## Version 1.35

-   Added RE-032.1: Personal Capacity classification boundary.
-   Framed the primary question as whether Personal Capacity is a
    parallel gate, a Human Approval requirement or a mixed control.
-   Defined Personal Capacity as the question of whether the person can
    responsibly assume risk now, separate from market opportunity,
    Evidence Quality and Regime Comparability.
-   Required future Personal Capacity work to separate verifiable facts
    from attested judgement.
-   Listed candidate verifiable facts such as liquidity, cash needs,
    obligations, debt service, income concentration, portfolio
    concentration, emergency reserve and time horizon constraints.
-   Listed candidate attested judgements such as perceived income
    stability, drawdown tolerance, ability to avoid forced selling and
    psychological capacity to hold through stress.
-   Recorded drawdown tolerance as especially unreliable under crisis
    pressure, and stated that pre-registered attestations should carry
    more weight than crisis-time revisions.
-   Documented that gate-combination logic cannot be finalized until
    Personal Capacity is classified.
-   No code changed.

## Version 1.34

-   Added RE-031.1: Regime Comparability Gate boundary.
-   Defined regime comparability as a gate / ceiling that asks whether
    current market conditions are structurally comparable to the
    historical evidence sample.
-   Separated Regime Comparability from Evidence Quality.
-   Separated Regime Comparability from `AssessmentEngine.drawdown_zone()`,
    which remains a market severity taxonomy, not a comparability gate.
-   Listed candidate future dimensions: valuation, inflation, interest
    rates, earnings / margins, volatility, liquidity / credit, policy /
    intervention and market structure.
-   Documented current state as not measurable: no code, no inputs, no
    taxonomy, no thresholds and no capital posture mapping.
-   Prohibited shortcuts such as using drawdown zone, expected return,
    Evidence Quality or the existence of similarity matches as regime
    comparability proxies.
-   No code changed.

## Version 1.33

-   Added RE-030.2: local Evidence Quality input adapter.
-   Added `build_local_evidence_quality_inputs(evidence)` to translate
    real `Evidence` into `LocalEvidenceQualityInputs`.
-   Kept `Evidence` as the single source of truth for the selected match
    set; no separate `matches` argument is accepted.
-   Calculated local coverage from usable returns:
    `min(evidence.return_count / 10.0, 1.0)`.
-   Verified current local coverage is 0.9, because today's snapshot has
    10 selected matches but 9 usable realized returns.
-   Calculated local consistency at `evidence.horizon_years`, avoiding
    the legacy `ValidationEngine` 3-year default horizon.
-   Verified current local consistency is 0.9518456229064439 and current
    local diversity is 0.6.
-   Verified today's real local inputs plus non-validated global state
    return `not measurable`.
-   Clarified that RE-030.2 is no longer zero-dependency, because it
    reads `Evidence` and its matches, but remains isolated from the
    operative flow.
-   Confirmed no thresholds, no capital posture mapping, no automatic
    recommendation and no operative authority.
-   Frozen Core unchanged.

## Version 1.32

-   Added RE-030.1: isolated Evidence Quality Gate.
-   Added `engine/evidence_quality_gate.py` with local/global input
    separation, discrete state output and specific explanations.
-   Added `tests/verify_evidence_quality_gate.py` as focused
    verification for the isolated gate.
-   Verified today's available inputs return `not measurable` or
    `conservative`, never a less-restrictive state.
-   Verified incomplete inputs / `None` values return `not measurable`.
-   Verified fully measured but not yet authorized inputs return
    `conservative`.
-   Confirmed the gate is not wired into `run.py`, `DecisionEngine`,
    `AssessmentEngine` or `ValidationEngine`.
-   Confirmed no thresholds, no capital posture mapping, no automatic
    recommendation and no operative authority.
-   Frozen Core unchanged.

## Version 1.31

-   Added RE-029.9: Evidence Quality Gate first-code acceptance
    criteria.
-   Documented likely future implementation and verification surfaces:
    an isolated gate module and a focused gate verification test.
-   Required the first future gate PR to compile and test in isolation
    without wiring into `run.py` or `DecisionEngine`.
-   Required tests to assert that today's incomplete inputs produce
    `not measurable` or `conservative`, never a less-restrictive state.
-   Required incomplete inputs or `None` values to produce
    `not measurable`, not crashes or assumed default scores.
-   Required explanations to name the specific channel or dimension
    causing the cap.
-   Made Frozen Core modification a rejection criterion for the first
    gate PR unless a separate numbered exception is authorized first.
-   Reaffirmed non-goals: no thresholds, no capital posture mapping, no
    automatic recommendations, no runtime wiring and no use of aggregate
    Research Validation metrics as local snapshot quality.
-   No code changed.

## Version 1.30

-   Added RE-029.8: Evidence Quality Gate implementation scope.
-   Documented that the first future implementation should create
    structure only: no thresholds, no capital posture rules and no
    operative wiring.
-   Prohibited first implementation changes to
    `AssessmentEngine.confidence().score`, `ValidationEngine`, `run.py`
    and `DecisionEngine`.
-   Required separate input channels for local snapshot evidence quality
    and global model-validation state.
-   Clarified that RE-029.6 defines five official Evidence Quality
    dimensions and that `stability` is not currently one of them.
-   Distinguished independence / dispersion from stability.
-   Required at least three conceptual output states: not measurable,
    conservative and a future less-restrictive state with no finalized
    name yet.
-   Reaffirmed fail-closed behaviour and isolation from the operative
    flow until later threshold, calibration and approval iterations.
-   No code changed.

## Version 1.29

-   Added RE-029.7: Evidence Quality Gate calibration boundary.
-   Defined conservative gate posture as fail-closed, discrete and
    evidence-led.
-   Documented that movement toward neutral requires pre-registered
    criteria, fully measured dimensions, baseline comparisons and
    explicit treatment of sample dependence.
-   Recorded why current Research Validation metrics do not suffice to
    relax the conservative ceiling: MAE lacks a naive baseline,
    hit-rate is not discriminating, rank correlation is weakly negative
    and `n=19` is not an independent sample-size claim.
-   Classified current dimension readiness: coverage and diversity are
    genuine but weak, consistency is real but not yet governance-grade,
    stability is unavailable, and independence / dispersion plus
    predictive validation status are not yet local gate measurements.
-   Prohibited use of `AssessmentEngine.confidence().score` as a gate or
    temporary proxy.
-   Prohibited treating aggregate Research Validation metrics as local
    snapshot evidence quality.
-   Recorded an open governance question about whether exception
    iterations written during the crisis that motivates them require
    extra safeguards.
-   No code changed.

## Version 1.28

-   Added RE-029.6: Evidence Quality Gate dimensions.
-   Defined coverage, consistency, diversity, independence / dispersion
    and predictive validation status as the documentary dimensions of
    evidence quality.
-   Documented that the gate starts conservative because current Research
    Validation does not yet demonstrate predictive discrimination:
    directional hit-rate is not discriminating and rank correlation is
    weakly negative.
-   Reaffirmed that `AssessmentEngine.confidence().score` must not be
    used as the Evidence Quality Gate while `stability=1.0` remains
    hardcoded and sample independence / dispersion is not captured.
-   Clarified what Evidence Quality may limit: maximum capital posture,
    Dry Powder deployment aggressiveness and Portfolio Reallocation
    aggressiveness.
-   Clarified what Evidence Quality may not do: create Risk ON posture,
    override other gates or compensate weak evidence with attractive
    expected return.
-   No code changed.

## Version 1.27

-   Added RE-029.5: confidence-to-posture gate boundary.
-   Defined evidence quality / confidence as a gate and posture ceiling,
    not a weighted input.
-   Defined gate combination as veto / most restrictive ceiling across
    evidence quality, regime comparability and personal capacity.
-   Explicitly excluded current `AssessmentEngine` confidence score from
    SOP capital gates while `stability=1.0` remains hardcoded.
-   No code changed.

## Version 1.26

-   Added RE-029.3: `AssessmentEngine` now consumes the shared
    `build_research_result()` Research pipeline instead of rebuilding
    Snapshot / Observable Universe / Similarity / Evidence locally.
-   Documented that source-of-truth duplication is resolved for
    Assessment evidence production.
-   Added RE-029.4: verified `AssessmentEngine` public helper outputs
    after the refactor.
-   Recorded verified outputs: `drawdown_zone=NORMAL`,
    `expected_return_5y=0.113866763521769`,
    `upside_potential=0.132855208016562`,
    `downside_risk=-0.010919489332530`, `matches=10`.
-   Clarified that confidence remains a separate unresolved path through
    `ValidationEngine`, including hardcoded stability, and must not drive
    SOP capital gates yet.

## Version 1.25

-   Added RE-DOC-004: Assessment / SOP boundary follow-up notes.
-   Clarified that `AssessmentEngine.drawdown_zone()` is a market
    severity taxonomy, not a capital posture taxonomy.
-   Recorded stepped error tolerance as pending SOP governance work:
    conservative by default, aggressive only when independent signals
    converge.
-   Reaffirmed that no thresholds, trigger logic or automatic capital
    decisions are introduced in this documentation pass.
-   No code changed.

## Version 1.24

-   Added RE-029.2: `AssessmentEngine` boundary audit.
-   Verified that `AssessmentEngine` is not called by `run.py`.
-   Verified that the older temporal-safety issue is already resolved:
    it uses `ObservableUniverse(dataset, as_of=snapshot.date)`.
-   Documented the remaining issue: `AssessmentEngine` still duplicates
    the Research pipeline locally instead of consuming
    `build_research_result()` / `ResearchResult`.
-   Documented that `AssessmentEngine` computes confidence through a
    separate `ValidationEngine` path, including hardcoded stability.
-   Clarified the v2 boundary: Assessment may interpret evidence quality,
    fragility and applicability, but must not decide capital posture,
    deployment size, dry-powder usage or portfolio reallocation.
-   No code changed.

## Version 1.23

-   Added RE-029.1: Assessment / SOP governance scope audit.
-   Defined the primary objective hierarchy: avoid irreversible error,
    preserve real capital, then maximize long-term return.
-   Defined dry powder as deployable investable liquidity, not merely
    literal cash.
-   Separated the Dry Powder Protocol from the Portfolio Reallocation
    Protocol: increasing net exposure is not the same decision as
    rotating between risk assets.
-   Established four capital-intensity postures: Conserve, Prepare,
    Deploy partially and Deploy aggressively.
-   Established `Blocked` as an orthogonal veto flag, not a fifth
    intensity level.
-   Added three initial invalidation gates: evidence quality, regime
    comparability and personal capacity.
-   Required explicit human approval with timestamp for partial or
    aggressive deployment.
-   No code changed.

## Version 1.22

-   Added RE-028.4: Evidence Engine v2 closure gate.
-   Declared Evidence v2 closed for the current architecture pass.
-   Confirmed that no additional Evidence fields are added now.
-   Moved remaining interpretive work to Assessment / SOP governance:
    capital tranches, dry-powder deployment, invalidation flags and
    confidence language.
-   Updated Phase 1 roadmap status: Evidence Engine v2 closed for the
    current pass.
-   No code changed.

## Version 1.21

-   Added RE-028.3: Evidence percentile field gate.
-   Confirmed that `Evidence.percentile(p)` remains the active
    descriptive interface for arbitrary distribution markers.
-   Deferred named percentile fields such as p10/p25/p75/p90 until
    Assessment / SOP governance defines their interpretation.
-   Reaffirmed the Evidence boundary: describe distributions, do not
    label them as actionable.
-   No code changed.

## Version 1.20

-   Added RE-028.2: Evidence Engine v2 descriptive sample-shape fields.
-   Extended `models/evidence.py` with additive, defaulted fields:
    return_count, positive_count, negative_count, zero_count,
    non_positive_probability and return_spread.
-   Updated `engine/evidence_engine.py` to compute those fields from
    the same horizon-specific return sample already used by the
    existing return statistics.
-   Updated `tests/verify_research_engine.py` to verify the new
    Evidence v2 surface. Live result: matches=10, return_count=9,
    positive_count=8, negative_count=1, zero_count=0,
    non_positive_probability=0.11111111111111,
    return_spread=0.14859283868117.
-   Reaffirmed the boundary: Evidence describes; Assessment / SOP
    interprets.

## Version 1.19

-   Added RE-028.1: Evidence Engine v2 scope audit before code changes.
-   Documented the current verified Evidence contract and consumers.
-   Established the RE-028 boundary: v2 must be additive and
    backwards-compatible because `EvidenceEngine` is consumed by the
    shared Research pipeline, Research Validation and `AssessmentEngine`.
-   Explicitly excluded recommendations, portfolio decisions and
    confidence/assessment logic from Evidence v2.
-   No code changed.

## Version 1.18

-   Added RE-DOC-003: corrected stale `AssessmentEngine` documentation
    after direct code inspection.
-   Replaced the outdated claim that `AssessmentEngine` was never
    connected to `ObservableUniverse`.
-   Documented that RE-024.3 already made `AssessmentEngine` consume
    `ObservableUniverse(dataset, as_of=snapshot.date)`.
-   Clarified the current issue: `AssessmentEngine` still duplicates
    the Research pipeline locally instead of delegating to
    `build_research_result()`, so the risk is source-of-truth drift, not
    temporal leakage.
-   No code changed.

## Version 1.17

-   Added RE-027.5: extracted `engine/research_pipeline.py` as the
    shared source of truth for the objective Research pipeline.
-   Updated `DecisionEngine` and `ResearchEngine` so both delegate to
    `build_research_result()` instead of maintaining parallel copies of
    Snapshot -> ObservableUniverse -> SimilarityEngine.top() ->
    EvidenceEngine orchestration.
-   Clarified that RE-027.4 verified the rebuilt `ResearchEngine`, but
    RE-027.5 is the iteration that closes the single-source-of-truth
    concern raised in RE-027.1.
-   Confirmed that `run.py` may continue calling `DecisionEngine`
    without duplicating Research pipeline logic, because `DecisionEngine`
    now consumes the same shared pipeline as `ResearchEngine`.
-   Closed the RE-027 Pre-Phase Gate as of RE-027.5.

## Version 1.16

-   Added RE-027.2: `ResearchResult` now represents the objective
    Research output -- snapshot, selected matches and evidence.
-   Added RE-027.3: rebuilt `ResearchEngine` as a thin facade over the
    verified Snapshot -> ObservableUniverse -> SimilarityEngine.top()
    -> EvidenceEngine pipeline.
-   Removed the stale `ResearchEngine` path that instantiated engines
    with invalid constructor arguments and could have used
    `SimilarityEngine.compare()` instead of selected top matches.
-   Added RE-027.4: functional smoke test for the rebuilt
    `ResearchEngine`.
-   Closed the RE-027 Pre-Phase Gate: Evidence Engine v2 and
    Similarity Engine v2 are no longer blocked by the stale named
    ResearchEngine object.
-   Documented the remaining integration boundary: `run.py` still calls
    `DecisionEngine` directly; wiring the CLI entry point through
    `ResearchEngine` remains a future choice.

## Version 1.15

-   Added RE-027.1: audit of the current `ResearchEngine` against the
    verified operative pipeline.
-   Documented that `ResearchEngine.__init__()` currently has three
    independent constructor mismatches: `SnapshotEngine`,
    `ExplanationEngine` and `AssessmentEngine`.
-   Documented that `ResearchEngine.run()` would use
    `SimilarityEngine.compare()` rather than `.top()`, creating a
    silent evidence-sample risk if constructor errors were patched in
    isolation.
-   Established the rebuild decision: `ResearchEngine` must become a
    thin facade over the already verified `DecisionEngine` pipeline,
    not a second independent implementation.
-   Added a Pre-Phase Gate: close the `ResearchEngine` rebuild before
    starting Evidence Engine v2 or Similarity Engine v2 work.

## Version 1.14

-   Added RE-026.1: functional smoke test for the canonical Research
    Validation metrics and diagnostics.
-   Documented RE-026.1.1: the test is executable directly from
    `tests/`.
-   Documented RE-026.1.2: the test verifies the pinned runtime before
    comparing canonical metric values, so environment mismatches fail
    as environment errors rather than ambiguous metric regressions.
-   Verified result: `RUNTIME : PINNED` and
    `RESEARCH VALIDATION METRICS : STABLE`.

## Version 1.13

-   Added RE-025.10: Research Validation synthesis.
-   Consolidated the interpretation of RE-025.6, RE-025.8 and
    RE-025.9 into one closing statement: `n=19` is an operative count,
    not an independent sample-size claim.
-   Summarized the current canonical Research Validation surface:
    sample_size=21, evaluated_count=19, MAE=7.03%, directional
    hit-rate=94.74%, rank_correlation=-0.2290, overlap_pairs=10,
    repeated_forecast_groups=4, and 16/19 records in repeated forecast
    groups.
-   Closed the current RE-025 block as exploratory validation with
    explicit limitations, without publishing a numeric effective N.

## Version 1.12

-   Added RE-025.9: repeated forecast group diagnostic.
-   Added `repeated_forecast_groups(records)` to
    `engine/validation_metrics.py`, grouping evaluable records by exact
    repeated forecast value.
-   Verified against the live dataset: 23 episodes, sample_size=21,
    evaluated_count=19, unique_forecasts=7,
    repeated_forecast_groups=4, records_in_repeated_groups=16.
-   Documented the four repeated forecast groups and clarified that
    this is a forecast-side dependency diagnostic, not proof of
    identical comparable sets.
-   Reaffirmed that no numeric effective N is published yet.

## Version 1.11

-   Added missing RE-025.7 documentation: `tests/verify_core.py` now
    includes `engine/validation_metrics.py` in the structural Engine
    checks.
-   Applied RE-DOC-002 to this document's own changelog: restored the
    historical v1.4, v1.5 and v1.6 MAE references to 7.05%, the value
    documented at the time.
-   Left RE-025.5 as the forward correction that supersedes those
    historical values with the pinned-runtime canonical MAE=7.03%.

## Version 1.10

-   Added RE-025.8: overlapping outcome window diagnostic.
-   Added `overlapping_outcome_windows(records)` to
    `engine/validation_metrics.py`, returning pairs of evaluable
    records whose realized 5-year outcome windows overlap.
-   Verified against the live dataset: 23 episodes, sample_size=21,
    evaluated_count=19, overlap_pairs=10.
-   Documented the `YYYY.MM` date constraint: comparisons and adding
    an integer 5-year horizon are valid for boolean overlap detection;
    direct subtraction is not valid for durations or ratios.
-   Reaffirmed that no numeric effective N is published yet.

## Version 1.9

-   Added RE-DOC-002: documentation history policy.
-   Established that changelog entries preserve historical project
    state; corrections should be documented forward in the version
    that discovers or authorizes them.
-   Recorded the RE-025.5 MAE correction as the motivating example:
    previous documentation reported 7.05%, while the pinned runtime
    established 7.03% as canonical.

## Version 1.8

-   Added RE-025.6: effective sample size caveat for Research
    Validation.
-   Documented that `n=19` is an operative count of evaluable records,
    not an independent sample-size claim.
-   Identified overlapping realized 5-year return windows as the
    first mechanical source of dependence.
-   Recorded a second, forecast-side dependence channel: repeated
    forecasts / potentially overlapping comparable sets. Live dataset
    currently has 19 evaluable records but only 7 unique forecast
    values; 1998.09 and 2009.03 share forecast=0.113866763522 despite
    non-overlapping future 5-year windows.
-   Kept RE-025.6 conceptual only: no numeric effective-N correction
    is published yet.

## Version 1.7

-   Converted `requirements.txt` from an empty directory into a real
    dependency file and pinned the canonical runtime:
    pandas==3.0.5, numpy==2.5.1, openpyxl==3.1.5.
-   Added RE-025.5: runtime reproducibility for Research Validation.
-   Recorded that RE-025.4 exposed environment sensitivity: different
    pandas/numpy versions can produce different validation records and
    therefore different aggregate metrics.
-   Established the pinned-runtime canonical metrics: MAE=7.03%,
    directional hit-rate=94.74%, rank_correlation=-0.2290, and
    unique_forecasts=7.
-   Superseded previous 7.05% MAE references with the pinned-runtime
    value, 7.03%.
-   Deferred effective sample size to RE-025.6; `n=19` remains an
    operative count, not an independence claim.

## Version 1.6

-   Added `rank_correlation()` to `engine/validation_metrics.py`
    (RE-025.4): Spearman rank correlation between forecast and
    realized return over evaluable validation records.
-   Implemented average-rank tie handling because the live validation
    set has repeated forecasts: 19 evaluable records, 7 unique
    forecasts, 19 unique actuals.
-   Verified against the live dataset: rank_count=19,
    rank_correlation=-0.2290, MAE unchanged at 7.05%, directional
    hit-rate unchanged at 94.74%.
-   Documented the interpretation limit: the result is exploratory,
    weakly negative, and more informative than directional hit-rate
    for this sample, but not formal statistical validation.
-   Normalized Research Validation references to RE-025.1-RE-025.4
    now that the whole initial validation metric block is present.

## Version 1.5

-   Added `directional_hit_rate()` to `engine/validation_metrics.py`
    (RE-025.3): directional agreement between forecast and realized
    return over evaluable validation records, excluding zeros.
-   Verified against the live dataset: directional_count=19,
    forecast_positive=19, forecast_negative=0, actual_positive=18,
    actual_negative=1, hits=18, misses=1, hit-rate=94.74%.
-   Documented the key interpretation limit: because 0/19 forecasts
    were negative, the high hit-rate is not strong evidence of
    directional skill; it mostly reflects that almost all realized
    5-year returns in the evaluated sample were positive.
-   Rechecked MAE in the same validation run: unchanged at 7.05%.
-   Left RE-025.4 rank correlation as the next validation metric and
    the more informative follow-up for this sample.

## Version 1.4

-   Added `engine/validation_harness.py` (RE-025.1): Research
    Validation Harness, an offline, point-in-time backtest of the
    Similarity/Evidence pipeline against realized historical
    outcomes. Not wired into `run.py`. Verified against the live
    dataset: sample_size=21, evaluated_count=19 of 23 episodes.
-   Added `engine/validation_metrics.py` (RE-025.2): MAE as the
    canonical Research Validation metric, with a mandatory
    exploratory-evidence disclaimer. Measured MAE=7.05%, flagged as
    outlier-sensitive at this sample size (n=19).
-   Logged, then fixed within the same version, a duplication risk in
    the shipped MAE implementation: `mean_absolute_error()` now reads
    `ValidationRecord.evaluable` instead of recomputing the same
    criterion inline. Re-verified: MAE unchanged at 7.05%.
-   Clarified, in Component Status and Execution State, that the
    Research Validation Harness is unrelated to the pre-existing
    `ValidationEngine` (confidence scoring for `AssessmentEngine`)
    despite the naming collision.
-   Frozen Core Policy: recorded that RE-025.1/RE-025.2 invoke no
    exception — built entirely on existing public interfaces.

## Version 1.3

-   Added "Execution State" section: explicit three-way distinction
    between exists / participates in the operative flow / matches
    the diagram's named objects (RE-023/RE-024 closing review).
-   Logged RE-023.5, RE-023.6, RE-024.1, RE-024.2.
-   Documented ResearchEngine's continued divergence from what
    DecisionEngine actually executes.
-   Catalogued additional known-broken, disconnected code
    (ExplanationEngine, core/dataset_builder.py).

## Version 1.2

-   Declared this document the single source of truth (RE-DOC-001);
    `ROADMAP.md` and `PROJECT_STATE.md` marked non-authoritative
    pending future consolidation.
-   Logged RE-021 through RE-023.4.
-   Recorded the Frozen Core Policy exception invoked by RE-021.
-   Added Observable Universe to Component Status.

## Version 1.1

-   Core declared stable.
-   Governance clarified.
-   Research Engine formally separated from SOP.
-   Infrastructure phase closed.
-   Functional roadmap established.
