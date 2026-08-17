# SOP — Sistema Operativo Patrimonial

**Versión:** 2.2\
**Última actualización:** 2026-08-17

> Este documento es la autoridad máxima del SOP. Sustituye a las
> versiones anteriores de `CONSTITUTION.md`, `PROJECT_STATE.md`,
> `ROADMAP.md` y `MODEL_ARCHITECTURE.md`, que quedaban marcadas como
> "no autoritativas, pendientes de consolidación" desde RE-DOC-001
> (governance doc v1.2) sin que esa consolidación llegara a hacerse.
>
> **v2.0 (2026-08-15)** fusiona esta Constitución (v1.0–v1.12,
> construida iteración a iteración desde el trabajo real) con el
> texto de 16 artículos que Armando escribió por separado
> ("Constitución del Sistema Operativo Patrimonial") — dos documentos
> con el mismo nombre que nunca se habían reconciliado. La fusión no
> reemplaza el trabajo real por la estructura constitucional; la
> absorbe dentro de ella. Nada de lo verificado hasta hoy se pierde en
> el cambio de forma. El inventario completo que precedió esta fusión
> — qué se solapaba, qué faltaba, qué entraba en conflicto — vive en
> la conversación del 2026-08-15, no se reproduce aquí.
>
> **v2.1 (2026-08-17)** corrige un desajuste real encontrado al hacer
> un recap de proyecto a petición de Armando: las Secciones 4, 9 y 10
> seguían describiendo el Dashboard como "pendiente", sin mencionar
> que el operativo llevaba hasta RE-DASH.1.21 ni que existía ya un
> segundo panel (panorama histórico de Shiller, RE-SHILLER-DASH.1 a
> .8). Corregido -- ver `SOP_ENGINE_PROJECT_STATUS.md`, RE-DOC-006.
> Cero cambios de principios o reglas, solo sincronización con lo que
> el repositorio ya tenía construido.
>
> **v2.2 (2026-08-17)** registra RE-KERNEL.1: primer módulo real del
> Kernel (`engine/kernel.py`), extracción pura de la orquestación que
> vivía dentro de `audit_posture.py` -- sin diseñar ni implementar
> K1/K2/K3/K5/K6, que siguen sin spec. Ver Secciones 4, 5 y 9, y
> `SOP_ENGINE_PROJECT_STATUS.md`, RE-KERNEL.1, para el detalle
> completo y la verificación carácter a carácter.

Para el detalle técnico del Research Engine (motores, gates, tests,
cada iteración con su justificación) sigue rigiendo
`docs/GOVERNANCE/SOP_ENGINE_PROJECT_STATUS.md` como fuente única de
verdad de ese subsistema. Este documento no lo duplica — lo resume y
enlaza. El Research Engine tiene además su propia constitución técnica
de doce artículos: `docs/CONSTITUTION_RESEARCH_ENGINE.md` — separada
de esta porque gobierna un subsistema técnico acotado, no el SOP
completo.

------------------------------------------------------------------------

## 1. Propósito y autoridad

El SOP es un sistema de gobierno diseñado para ayudar a tomar
decisiones patrimoniales de forma objetiva, consistente y sostenible
durante décadas.

Su finalidad no es maximizar la rentabilidad de una operación
concreta, sino aumentar la probabilidad de construir y preservar
patrimonio a largo plazo mediante un proceso de decisión robusto.

El patrimonio no es un fin. Es el medio para alcanzar una mayor
libertad.

El SOP es el producto. No el Research Engine, no un protocolo
individual — el sistema completo de gobierno patrimonial. El Research
Engine es un subsistema: su única función es transformar datos
históricos en evidencia objetiva y explicable. No decide la asignación
patrimonial por sí mismo — produce información; esta Constitución y
los protocolos del SOP determinan cómo se utiliza esa información
(ver Sección 5, Kernel de decisión).

Este documento es la autoridad máxima del SOP. Toda modificación del
sistema — código, protocolos, arquitectura patrimonial — debe poder
justificarse contra él. Si una decisión de diseño no puede señalarse a
un artículo de esta Constitución, no entra.

------------------------------------------------------------------------

## 2. Principios constitucionales

### Jerarquía de objetivos primaria

1. Evitar el error irreversible.
2. Preservar el capital en términos reales.
3. Maximizar el retorno a largo plazo, solo una vez respetadas las dos
   restricciones anteriores.

Esta jerarquía es una decisión de gobierno, no un resultado del
modelo. Si el orden cambia, cambia el resto del SOP con él.

### Filosofía

- El patrimonio solo tiene valor en la medida en que aumenta la
  libertad futura.
- Pensar en décadas, no en meses. Las decisiones se evalúan por su
  impacto acumulado, no por el resultado de una operación concreta.
- Separar evidencia de opinión.
- Mantener una arquitectura patrimonial estable.
- Utilizar reglas verificables — cada restricción real acaba siendo un
  número, un estado discreto, un veto o una atestación explícita, no
  una intención bien redactada.
- El sistema está por encima del individuo en el momento de decidir:
  las reglas existen para proteger al propietario de sus propias
  emociones, no para negar que existan. **El SOP no elimina la
  emoción de la decisión — impide que decida sin fricción.** Human
  Approval (Sección 6) no niega la emoción declarada; la domestica
  con cooling-off y trazabilidad, en vez de fingir que no existe o
  dejarla actuar sin control.
- La simplicidad es una ventaja competitiva. La complejidad solo se
  incorpora cuando demuestra una mejora objetiva — robustez antes que
  sofisticación: preferimos un sistema comprensible, reproducible y
  mantenible a uno más complejo pero difícil de gobernar.
- Toda decisión debe ser explicable. Si no puede justificarse de forma
  clara, no debe ejecutarse. El SOP genera evidencia explicable, nunca
  una caja negra.

### Evidencia

Toda decisión relevante debe apoyarse en evidencia: investigación
histórica, datos cuantitativos, reglas previamente definidas,
simulaciones o validaciones. Nunca en intuiciones no gobernadas. El
Research Engine (Sección 7) es la fuente principal de esa evidencia,
pero no la única — Personal Capacity Facts y Human Approval producen
evidencia propia, de naturaleza distinta (hechos operativos y
consentimiento humano, no precedentes históricos).

------------------------------------------------------------------------

## 3. Arquitectura patrimonial

### Nivel 1 — Propósito y estructura macro

El Patrimonio Financiero existe para sostener la vida elegida y
financiar la libertad futura.

El Patrimonio de Uso es la materialización de esa libertad.

```
Patrimonio Total
   │
   ├── Patrimonio Financiero
   │      Gobernado por reglas verificables, gates y protocolos del SOP.
   │
   │      Caja Motor: sin objetivo numérico fijo.
   │      Trayectoria esperada + seguimiento (Proyecciones), impacto
   │      de extracciones calculado bajo demanda ("El puente").
   │
   │      Arquitectura interna:
   │      Caja Seguridad · Caja Motor · Caja Rentas Pasivas
   │
   │      Protocolos:
   │      Dry Powder Protocol · Human Approval · Portfolio Reallocation Protocol
   │
   └── Patrimonio de Uso
          Decisión personal orientada a calidad de vida.
          Ejemplos: vivienda habitual, Santoña.
          Sin gates cuantitativos, sin cooling-off y sin protocolos
          de despliegue del SOP.
```

### Nivel 2 — Patrimonio Financiero, Patrimonio de Uso y Patrimonio de Consumo

**Patrimonio Financiero.** Es la parte del patrimonio que el SOP
gobierna directamente. Su misión es preservar capital real y sostener
la libertad futura. Caja Motor, su motor de crecimiento a largo plazo,
se gobierna por seguimiento de trayectoria, no por un objetivo
numérico fijo — ver más abajo.

**Patrimonio de Uso.** Su propósito es la utilidad vital y la calidad
de vida. No se mide por rentabilidad financiera y el SOP no impone
puertas automáticas sobre él. Por eso mismo, no vive en
`personal_capacity_facts.xlsx` — ese archivo alimenta el Personal
Capacity Facts Gate, que solo gobierna Patrimonio Financiero.
Verificado el 2026-08-14: la vivienda habitual no aparece en ninguna
hoja de AMS/AML, y esa ausencia es correcta, no un hueco de datos.

**Patrimonio de Consumo — eliminado como categoría.** Coches, relojes,
vacaciones u otros gastos de disfrute son consumo. No son asignación
patrimonial y quedan fuera del balance gobernado por el SOP.

### El puente: extracción de Patrimonio Financiero hacia Patrimonio de Uso

El SOP no bloquea automáticamente una extracción de capital desde
Patrimonio Financiero hacia Patrimonio de Uso.

Lo que sí exige es transparencia sobre el coste de oportunidad.

Antes de extraer capital, el sistema debe estimar el impacto temporal
de esa decisión:

> Comparando el saldo de Caja Motor justo antes y justo después de la
> extracción, ¿a cuántos meses o años atrás en su propia trayectoria
> de crecimiento retrocede ese saldo?

No compara contra ningún objetivo externo — Caja Motor no tiene uno
(ver "Caja Motor: sin objetivo numérico fijo" más abajo). Compara el
saldo contra sí mismo, en el tiempo.

Este cálculo es un **warning informativo**, no una puerta de bloqueo.

La decisión final pertenece a Armando. El SOP informa del coste
financiero; no decide si la utilidad vital compensa ese coste.

El cálculo usará una hipótesis de rentabilidad explícita y revisable.
Puede tomar como referencia información del Research Engine, pero no
queda gobernado automáticamente por la expectativa del Assessment
Engine.

### Caja Motor: sin objetivo numérico fijo, seguimiento de trayectoria

Caja Motor no financia el gasto corriente — de eso se encargan Caja
Seguridad y Caja Rentas Pasivas. Su función es componer a largo plazo,
disponible para extracciones puntuales hacia Patrimonio de Uso cuando
Armando decida usarlas.

Se evaluó (2026-08-13) fijar objetivos cuantificados X/Y/Z a 5/10/15
años por necesidad patrimonial, anclados a posibles extracciones
futuras conocidas. Se descartó: encadenar precio futuro, momento futuro
y retorno futuro en una sola cifra a 15 años acumula tres
incertidumbres independientes y produce una falsa precisión — el mismo
problema que ya se había evitado al no fijar objetivos por proyección
de mercado.

En su lugar, Caja Motor se gobierna así: la hipótesis base v1 (abajo)
define la trayectoria esperada y su seguimiento (`Proyecciones`, hojas
Trayectoria esperada y Seguimiento) — sin objetivo externo, solo
comprobación de ritmo. Cuando una extracción hacia Patrimonio de Uso
se convierta en una decisión real, no una posibilidad, su impacto se
calcula entonces, con el saldo y el precio reales de ese momento — ver
"El puente" arriba y el calculador de impacto temporal (Sección 10).
Caja Seguridad y Caja Rentas Pasivas cumplen funciones distintas y se
gobiernan por sus propias reglas.

**Hipótesis base v1 de rentabilidad:** 7% real anualizado, equivalente
aproximado a 9,4% nominal, usando como referencia la serie total return
real de Shiller (`data/raw/shiller.xlsx`), con dividendos reinvertidos.

También se calculó un escenario condicionado al CAPE de partida. Con
CAPE elevado, los retornos históricos posteriores fueron mucho menores.
Ese escenario se descarta como base por tamaño muestral insuficiente,
no por ignorarlo.

Esta hipótesis no se ajusta automáticamente por CAPE ni por el Research
Engine. Solo puede cambiar mediante actualización explícita de esta
Constitución.

### Nivel 3 — Arquitectura del Patrimonio Financiero: las tres cajas

Las tres cajas dejan de ser "la cartera" y pasan a ser la arquitectura
interna del Patrimonio Financiero — un nivel, no el sistema entero.

| Caja | Objetivo estratégico | Se construye con |
|---|---|---|
| **Seguridad** | Fondo de seguridad + pólvora seca para oportunidades | Liquidez, depósitos, cuentas remuneradas, fondos monetarios |
| **Motor** | Crecimiento compuesto a largo plazo | Fondo indexado Vanguard S&P 500 y otras inversiones a largo plazo |
| **Rentas Pasivas** | Nutrir de liquidez recurrente, reducir la dependencia psicológica de vender patrimonio | ETF JGPI (~5k€/año), inversiones inmobiliarias (~7,5k€/año), oro |

Cada caja tiene un objetivo distinto — no se miden con la misma vara.
Un monetario de rentabilidad mediocre puede ser excelente si cumple
perfectamente su función de liquidez.

Este vocabulario — Seguridad / Motor / Rentas Pasivas, no Crecimiento /
Liquidez / Rentas — es el nombre constitucional oficial, decidido el
2026-08-15: ya vive en código, en `personal_capacity_facts.xlsx` (hoja
`Cajas`) y en todo el governance doc; renombrar tendría un coste de
propagación real sin beneficio funcional.

Esta arquitectura ya está traducida a Excel: la hoja `Cajas` de
`personal_capacity_facts.xlsx` clasifica cada partida de AMS/AML en
estas tres cajas por fórmula, con control de cuadre a 0€ (ver Sección
9, Entregables).

### Nivel 4 — Estrategias de inversión dentro de cada caja

P. ej., dentro de Caja Motor: concentración actual en S&P 500 frente a
diversificación gradual hacia un índice mundial. Sin reglas todavía —
es exactamente el terreno de Portfolio Reallocation Protocol (Sección
6), pendiente en su totalidad.

### Nivel 5 — Productos concretos

Vanguard S&P 500, fondos monetarios, JGPI, etc.

### Por qué esta jerarquía importa

Puedes cambiar cualquier elemento de un nivel inferior sin reescribir
los superiores — cambiar un producto en el Nivel 5 no debería obligar
a tocar el Nivel 1. Es la misma disciplina de responsabilidad única y
estabilidad arquitectónica que ya rige el código del Research Engine,
aplicada al patrimonio completo.

------------------------------------------------------------------------

## 4. Módulos del SOP

El SOP está compuesto por módulos independientes con responsabilidades
claramente definidas. Ningún módulo asume responsabilidades de otro —
misma disciplina de separación de capas que ya rige el Research Engine
(`docs/CONSTITUTION_RESEARCH_ENGINE.md`, Artículo 3), aplicada aquí al
sistema completo.

| Módulo | Responsabilidad | Estado |
|---|---|---|
| **Constitución** | Define los principios permanentes del sistema | Existe — este documento |
| **Arquitectura Patrimonial** | Organiza el patrimonio por funciones (Sección 3) | Existe parcialmente — clasificación en 3 cajas ya traducida a Excel; Nivel 4 (rotación entre estrategias) sin reglas |
| **Kernel** | Aplica las reglas de gobierno y determina si una decisión es válida (Sección 5) | Existe parcialmente — `engine/kernel.py` (RE-KERNEL.1) centraliza en un módulo importable los fragmentos K4/gobernanza ya implementados; K1/K2/K3/K5/K6 siguen sin spec ni código |
| **Protocolos** | Definen cómo actuar ante situaciones concretas (Sección 6) | Existe parcialmente — Dry Powder y Human Approval operativos; Portfolio Reallocation, Rebalanceo y Protección pendientes |
| **Research Engine** | Genera evidencia objetiva para apoyar las decisiones. No decide (Sección 7) | Existe — núcleo cerrado y auditado contra su propia constitución el 2026-08-14 |
| **Dashboard** | Representa el estado del SOP. Nunca modifica el sistema. Su misión es informar | Existe — dos paneles estáticos de solo lectura: operativo (`generate_dashboard.py`, RE-DASH.1.21) y panorama histórico de Shiller (`generate_shiller_dashboard.py`, RE-SHILLER-DASH.8). Sin filtros, sin interactividad, deliberadamente fuera de alcance salvo necesidad real |
| **Reporting** | Documenta decisiones y evolución del sistema en el tiempo | Pendiente — sin diseño todavía |

------------------------------------------------------------------------

## 5. Kernel de decisión

El Kernel del SOP es el modelo lógico que combina restricciones,
gates, protocolos y autorización humana para determinar si una
decisión de capital es válida.

Hoy no existe como módulo único que implemente los seis filtros. Sus
piezas siguen repartidas: `gate_combination.py`, `posture_mapper.py`,
`human_approval.py`, `dry_powder_protocol.py`. Desde RE-KERNEL.1
(2026-08-17), la orquestación de lectura de esas piezas — antes
código inline dentro de `audit_posture.py` — vive en
`engine/kernel.py`, un módulo importable (`build_kernel_results()`)
que cualquier otra parte del sistema puede usar sin duplicar lógica.
`audit_posture.py` es ahora un wrapper fino sobre ese módulo, verificado
carácter a carácter contra su comportamiento anterior. Sigue sin ser
el Kernel ni una herramienta de decisión — su propio docstring lo dice
explícitamente: solo centraliza los fragmentos K4/gobernanza ya
implementados, no los seis filtros.

El diseño lógico completo contempla seis filtros que toda decisión
debería superar:

- **K1. Propósito** — ¿incrementa la libertad futura?
- **K2. Función** — ¿respeta la función de la caja correspondiente?
- **K3. Coherencia** — ¿es compatible con la arquitectura patrimonial?
- **K4. Evidencia** — ¿existe evidencia suficiente? (el único con
  cobertura real hoy, vía Evidence Quality Gate, Regime Comparability
  Gate y Personal Capacity Facts Gate, combinados por `min()` en
  `posture_mapper.py`)
- **K5. Robustez** — ¿seguiría siendo una buena decisión bajo
  escenarios adversos?
- **K6. Simplicidad** — ¿existe una alternativa más simple que consiga
  el mismo resultado?

Una decisión que no supera cualquiera de estos filtros queda
descartada. Human Approval es un prerrequisito independiente, no un
séptimo filtro dentro de este `min()` — nunca se computa a partir de
los otros seis, ni ellos a partir de él (ver Sección 6).

Diseñar y construir K1/K2/K3/K5/K6 sigue siendo trabajo pendiente, sin
disparador que lo haga urgente hoy — ver Sección 10. A diferencia de
la extracción de RE-KERNEL.1 (ingeniería pura sobre lo ya existente),
esto es trabajo de diseño de política: definir qué significa
operativamente cada filtro antes de poder escribir una sola línea de
código para ellos.

------------------------------------------------------------------------

## 6. Protocolos del SOP

| Protocolo | Gobierna | Estado |
|---|---|---|
| **Dry Powder Protocol** | Convertir liquidez ociosa (Caja Seguridad) en capital invertido durante un episodio de caída | 85-90% aislado. Cuatro reglas completas, techo extraordinario del 90% vía Human Approval ya calculado por fórmula (RE-032.10). Sin wiring a `run.py`/`DecisionEngine`, deliberado. |
| **Human Approval** | Consentimiento humano vigente, independiente de si los datos permiten actuar | 85-90% operativo real. Chain-resolution completa, cooling-off 14/30 días, validez 90 días, extensión propia de 30 días para el techo del 90%. Primera atestación real en ambos patrimonios (2026-08-13): AMS Deploy Aggressively, bajo cooling-off hasta 2026-08-27; AML Conserve, vigente de inmediato (no es subida de tolerancia). |
| **Portfolio Reallocation Protocol** | Vender un activo de riesgo del Patrimonio Financiero para comprar otro (rotación **dentro** del Patrimonio Financiero, nunca hacia Patrimonio de Uso) | 0-5%. Sin reglas, sin código, sin Excel. Pendiente en su totalidad — ver Sección 10. |
| **Rebalanceo** | Sin definir | Pendiente — no existe ni como spec. |
| **Protección** | Sin definir | Pendiente — no existe ni como spec. |

Los protocolos son prerrequisitos independientes entre sí — ninguno
compensa a otro. Para actuar hacen falta todos los que apliquen a la
vez: la postura combinada de evidencia, Human Approval vigente, y las
reglas propias del protocolo en cuestión.

Frontera importante fijada el 2026-08-13: mover capital de Patrimonio
Financiero hacia Patrimonio de Uso (p. ej., vender S&P 500 para
financiar Santoña) **no es** una decisión de Portfolio Reallocation
Protocol — es una decisión personal, informada por "El puente"
(Sección 3), no gobernada por ningún protocolo del SOP.

------------------------------------------------------------------------

## 7. Research Engine (resumen)

Núcleo estable: Drawdown Engine, Snapshot Engine, Similarity Engine
(v1), Probability Engine, Inference Engine, Assessment Engine —
producen evidencia objetiva sobre episodios históricos de mercado. Esa
evidencia alimenta Evidence Quality Gate y Regime Comparability Gate,
que junto con Personal Capacity Facts Gate determinan la postura
combinada de capital (`Conserve`/`Prepare`/`Deploy Partially`/`Deploy
Aggressively`/`Blocked`). Probability Engine existe y alimenta la
tubería original del Research Engine (`evidence_engine.py`,
`decision_engine.py`), pero no gobierna la postura actual — no
aparece en ningún gate de la cadena de arriba.

La capa de gates, postura y protocolos no ejecuta operaciones ni
decide asignación por sí misma. No está conectada a `run.py` ni a
`DecisionEngine` — esa integración sigue deliberadamente fuera de
alcance en todo el proyecto (Sección 10).

El Research Engine tiene su propia constitución de doce artículos
(`docs/CONSTITUTION_RESEARCH_ENGINE.md`, v1.1), auditada contra el
código real el 2026-08-14: cinco violaciones encontradas y corregidas
(RE-044.1 a RE-EXP.1). No decide la asignación patrimonial por sí
mismo — su salida es entrada para el Kernel (Sección 5), no una
decisión.

Estado técnico completo, motor a motor, con cada iteración justificada
y cada test verificado: `docs/GOVERNANCE/SOP_ENGINE_PROJECT_STATUS.md`
(v2.32 a fecha de este documento).

------------------------------------------------------------------------

## 8. Triggers de trabajo

Un Trigger es una condición objetiva — un evento observable o una
decisión real ya tomada — que justifica empezar a construir algo. Un
Trigger inicia trabajo; nunca ejecuta una acción automáticamente sobre
el patrimonio, eso corresponde a los Protocolos (Sección 6), no a este
principio.

**No se construyen protocolos ni módulos especulativos sin una
decisión real o un evento observable que lo exija.** Esta regla ya se
ha aplicado en la práctica varias veces antes de nombrarse:

- Se descartaron los objetivos X/Y/Z de Caja Motor (2026-08-13) por
  encadenar incertidumbres sin necesidad real — ver "Caja Motor: sin
  objetivo numérico fijo" (Sección 3).
- El calculador de impacto temporal se construirá cuando exista una
  extracción real, no como proyección anticipada.
- Portfolio Reallocation Protocol sigue sin código porque no existe
  hoy una necesidad real de reasignación.

Formalizar este principio como Trigger no cambia nada de lo ya
decidido — le da nombre a un criterio que el proyecto ya venía
aplicando de forma consistente.

------------------------------------------------------------------------

## 9. Entregables existentes

Lo que hoy existe de verdad en el repositorio, no lo que está previsto:

**Motores y gates** (`engine/`) — módulos principales, incluyendo el
núcleo del Research Engine, `evidence_quality_gate.py`,
`regime_comparability_gate.py`, `personal_capacity_facts_gate.py`,
`gate_combination.py`, `posture_mapper.py`, `dry_powder_protocol.py`,
`dry_powder_ledger_state.py`, `human_approval.py`,
`human_approval_state.py`, y `kernel.py` (RE-KERNEL.1 — capa de
ensamblaje de solo lectura que centraliza los fragmentos anteriores en
un único módulo importable; no implementa K1/K2/K3/K5/K6, ver Sección
5).

**Loaders** (`loaders/`) — un loader por fuente de datos real:
`dry_powder_ledger_loader.py`, `human_approval_loader.py`,
`personal_capacity_facts_loader.py`, `shiller_loader.py`.

**Datos reales** (`data/raw/`):

| Archivo | Estado |
|---|---|
| `personal_capacity_facts.xlsx` | **Con datos reales cargados.** AMS resuelve `adequate` (nueve hechos verificables, cero rupturas); AML resuelve `constrained` (`liquidity_adequate` con ruptura confirmada, hallazgo real). Incluye dos pestañas adicionales, `Cajas` y `Proyecciones` (añadidas 2026-08-13): `Cajas` clasifica cada partida de AMS/AML en Seguridad/Motor/Rentas Pasivas por fórmula, con % de cada caja sobre el total (control de cuadre a 0€ frente al total patrimonial de cada hoja); `Proyecciones` congela una fecha e importe de referencia de Caja Motor (no enlazados por fórmula a `Cajas` — solo cambian con actualización explícita), calcula la trayectoria esperada a 5/10/15 años desde ese punto fijo bajo la hipótesis base v1, y añade una tabla de Seguimiento donde se registra el saldo real observado en fechas de control futuras frente a lo que la trayectoria esperaba — así se puede ver si se va por delante o por detrás, en vez de comparar el escenario contra sí mismo cada vez. Caja Motor no tiene objetivo numérico fijo (Sección 3) — esta hoja es el mecanismo de seguimiento, no un sustituto de una cifra objetivo. |
| `dry_powder_ledger.xlsx` | Vacío. Sin episodios de caída registrados todavía. |
| `human_approval_attestations.xlsx` | Ambos patrimonios con una atestación real (2026-08-13): AMS Deploy Aggressively (bajo cooling-off), AML Conserve (vigente). |
| `shiller.xlsx` | Serie histórica completa, fuente del Research Engine. |

**Scripts operativos:** `audit_posture.py` (dry-run de lectura, wrapper
fino sobre `engine/kernel.py::build_kernel_results()` desde
RE-KERNEL.1 — combina todos los gates y protocolos por patrimonio, no
ejecuta nada, ver Sección 5 sobre por qué no es el Kernel).

**Dashboards** (solo lectura, sin `<script>`, sin filtros ni
interactividad — deliberado, ver Sección 4):

- `generate_dashboard.py` → `outputs/dashboard.html` — dashboard
  operativo (RE-DASH.1 a RE-DASH.1.21): estado por patrimonio,
  liquidez, Dry Powder, Human Approval, alertas y datos de mercado.
- `generate_shiller_dashboard.py` → `outputs/shiller_dashboard.html`
  (RE-SHILLER-DASH.1 a RE-SHILLER-DASH.8) — panorama histórico
  diagnóstico sobre la serie completa de Shiller (1871-2026): resumen
  ejecutivo, indicadores con semáforo, gráficas de precio/CAPE/
  inflación/tipos con episodios de caída sombreados, resumen agregado
  de drawdowns con los peores episodios nombrados, y retornos reales
  posteriores según nivel de CAPE inicial. Explícitamente no dice si
  comprar o vender ni evalúa gates — esa lectura sigue viviendo solo en
  el dashboard operativo.

**Tests:** suite `tests/verify_*.py`, re-ejecutada en cada iteración.

**Documentación:**

- `docs/CONSTITUTION.md` — este documento.
- `docs/CONSTITUTION_RESEARCH_ENGINE.md` — los doce artículos que
  gobiernan el Research Engine (v1.1), guardada como archivo el
  2026-08-14 tras existir solo en conversación desde el inicio del
  proyecto. Auditada ese mismo día contra el código real: cinco
  violaciones encontradas y corregidas.
- `docs/GOVERNANCE/SOP_ENGINE_PROJECT_STATUS.md` — estado técnico del
  Research Engine, v2.32.
- `docs/MANUAL_OPERATIVO.md` / `.docx` — manual de uso diario (Dry
  Powder Protocol y Human Approval); Word e idéntico en contenido.

------------------------------------------------------------------------

## 10. Pendiente

Separado por qué tipo de espera es cada cosa — confundir estas
categorías es lo que convierte un "algún día" en una tarea inmediata
sin que nadie lo decida a propósito.

### Construible ya, sin bloqueo externo

- Nada en esta categoría ahora mismo. RE-DASH.1 (dashboard operativo,
  hasta RE-DASH.1.21) y su ampliación con el panorama histórico de
  Shiller (RE-SHILLER-DASH.1 a .8) se completaron en agosto 2026 — ver
  Sección 9. Próximo candidato real para esta categoría, si se decide
  priorizarlo: Portfolio Reallocation Protocol, una vez resueltas sus
  preguntas de diseño abiertas más abajo.

### Condicionado a un disparador real o una fecha concreta

- **Calculador de impacto temporal** para extracciones desde Caja
  Motor hacia Patrimonio de Uso, usando la hipótesis base v1 (Sección
  3). Se construye en el momento de una decisión real de extracción,
  no antes — ver Sección 8, Triggers.
- **Portfolio Reallocation Protocol** — todo pendiente. Preguntas
  abiertas: disparador (¿episodio de drawdown como Dry Powder, o
  revisión periódica/estructural?); universo de activos (¿solo
  rotación dentro de Caja Motor, o más amplio?); los tres invalidators
  del governance doc necesitan definición operativa —
  liquidez/riesgo del activo vendido, correlación entre vendido y
  comprado, coste de materializar la pérdida **o la ganancia** (el
  caso Motor→índice mundial es materializar ganancia, no pérdida);
  escala de agresividad propia o reutilizar las cuatro posturas
  existentes; si redirigir aportaciones nuevas (sin coste fiscal) y
  vender posición existente (con coste fiscal) son la misma regla o
  dos mecanismos distintos.
- **Congelado de `Proyecciones`** (fecha de referencia + importes de
  Caja Motor) fijado provisionalmente a 2026-08-13. Sustituirlo por el
  cierre a 31/12/2026 cuando esa fecha llegue, para anclar la
  trayectoria en año natural. Condicionado a fecha, no a evento.

### Baja prioridad, sin disparador definido, no urgente

Distinto del grupo anterior: aquí no hay un evento concreto que se
esté esperando, solo ausencia de necesidad real para priorizarlo hoy.

- **K1/K2/K3/K5/K6 del Kernel** (Sección 5) — la extracción de lo ya
  existente a `engine/kernel.py` se completó (RE-KERNEL.1); diseñar e
  implementar los cinco filtros que hoy no tienen ni spec es trabajo
  de política, no de ingeniería, y sigue sin disparador que lo haga
  urgente.
- **Dashboard** más allá del alcance actual (RE-DASH.1.21 operativo +
  RE-SHILLER-DASH.8 histórico — filtros, interactividad, nuevas
  vistas), y **Reporting** (Sección 4) — sin diseño todavía.
- **Rebalanceo** y **Protección** (Sección 6) — protocolos sin
  definir, ni siquiera como spec.
- **Similarity Engine v2** del Research Engine (duración, velocidad,
  tendencia previa, volatilidad, similitud multidimensional) — hito
  técnico identificado en `SOP_ENGINE_PROJECT_STATUS.md`, actualmente
  de baja prioridad.

### Fuera de alcance, deliberado, en todo el proyecto

- Wiring a `run.py` / `DecisionEngine`.
- Ejecución automática de cualquier operación.

------------------------------------------------------------------------

## 11. Forma de trabajo

- Una modificación conceptual por iteración. En documentación, un
  único archivo completo. En código, el cambio mínimo necesario:
  módulo, test y registro — nunca fragmentos sueltos.
- Proponer el diseño y sus acceptance checks antes de escribir código;
  confirmar con Armando antes de construir.
- Toda decisión de diseño no trivial queda registrada en
  `SOP_ENGINE_PROJECT_STATUS.md` (para el Research Engine) o en este
  documento (para el SOP) — nunca solo en el chat.
- Evitar refactorizaciones innecesarias; mantener compatibilidad con
  el resto del sistema.
- Fail-closed: la ausencia o incertidumbre de un dato nunca se lee
  como favorable. Un dato malformado se descarta con una explicación
  registrada, nunca se adivina.
- Priorizar claridad y estabilidad sobre velocidad.
- Backward compatibility: un cambio no rompe a quien ya dependía del
  comportamiento anterior sin decirlo explícitamente — mismo criterio
  que ya aplica el Research Engine (p. ej. `MIN_DRAWDOWN` re-exportado
  tras centralizarse, RE-044.2).

------------------------------------------------------------------------

## 12. Visión

El objetivo final del SOP es convertirse en un sistema operativo
patrimonial completo. El Research Engine y los protocolos ya
operativos representan solo una parte de las capacidades necesarias.

Con el tiempo, el SOP incorporará el Kernel unificado, el Dashboard,
Reporting, y los protocolos que hoy faltan (Rebalanceo, Protección,
Portfolio Reallocation completo) — siempre manteniendo la separación
entre principios, evidencia, decisión y ejecución, y siempre
construidos cuando exista una necesidad real (Sección 8), no antes.

Esta es una dirección, no un roadmap con fechas. La Sección 10
(Pendiente) es la fuente de verdad sobre qué está realmente activo en
cada momento — esta sección no se actualiza para reflejar plazos,
solo para reflejar si la dirección cambia.

> No buscamos predecir el futuro. Construimos un sistema capaz de
> tomar mejores decisiones durante toda una vida.

------------------------------------------------------------------------

## 13. Cómo retomar el proyecto

1. Leer este documento completo — es la autoridad.
2. Para el detalle técnico del Research Engine, leer
   `docs/GOVERNANCE/SOP_ENGINE_PROJECT_STATUS.md`, empezando por su
   "Honest Progress Snapshot".
3. Para operar el día a día (Dry Powder Protocol, Human Approval),
   usar `docs/MANUAL_OPERATIVO.md`.
4. Continuar desde la Sección 10 de este documento (Pendiente),
   respetando sus categorías — no todo lo pendiente es lo mismo.
