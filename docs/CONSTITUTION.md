# SOP — Sistema Operativo Patrimonial

**Versión:** 1.5\
**Última actualización:** 2026-08-13

> Este documento es la autoridad máxima del SOP. Sustituye a las
> versiones anteriores de `CONSTITUTION.md`, `PROJECT_STATE.md`,
> `ROADMAP.md` y `MODEL_ARCHITECTURE.md`, que quedaban marcadas como
> "no autoritativas, pendientes de consolidación" desde RE-DOC-001
> (governance doc v1.2) sin que esa consolidación llegara a hacerse.
> Este documento la cierra.

Para el detalle técnico del Research Engine (motores, gates, tests,
cada iteración con su justificación) sigue rigiendo
`docs/GOVERNANCE/SOP_ENGINE_PROJECT_STATUS.md` como fuente única de
verdad de ese subsistema. Este documento no lo duplica — lo resume y
enlaza.

------------------------------------------------------------------------

## 1. Qué es el SOP

El SOP es el producto. No el Research Engine, no un protocolo
individual — el sistema completo de gobierno patrimonial que debe
funcionar durante décadas mediante reglas objetivas, no mediante
juicio ad-hoc en el momento de decidir.

El Research Engine es un subsistema. Su única función es transformar
datos históricos en evidencia objetiva y explicable. No decide la
asignación patrimonial por sí mismo — produce información; la
Constitución y los protocolos del SOP determinan cómo se utiliza esa
información.

### Filosofía

- Pensar en décadas, no en meses.
- Separar evidencia de opinión.
- Mantener una arquitectura patrimonial estable.
- Utilizar reglas verificables — cada restricción real acaba siendo un
  número, un estado discreto, un veto o una atestación explícita, no
  una intención bien redactada.
- Minimizar la influencia emocional en la toma de decisiones.
- Robustez antes que sofisticación: preferimos un sistema
  comprensible, reproducible y mantenible a uno más complejo pero
  difícil de gobernar.
- Generar evidencia explicable, nunca una caja negra.

### Jerarquía de objetivos primaria

1. Evitar el error irreversible.
2. Preservar el capital en términos reales.
3. Maximizar el retorno a largo plazo, solo una vez respetadas las dos
   restricciones anteriores.

Esta jerarquía es una decisión de gobierno, no un resultado del
modelo. Si el orden cambia, cambia el resto del SOP con él.

------------------------------------------------------------------------

## 2. Arquitectura patrimonial

Concepto cerrado el 2026-08-13, todavía sin traducción a código ni a
Excel — ver Sección 6, Pendiente.

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
   │      Objetivo cuantificado de Caja Motor:
   │      X€ a 5 años / Y€ a 10 años / Z€ a 15 años
   │      (pendiente: cifras concretas)
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
la libertad futura. Los objetivos cuantificados a 5, 10 y 15 años se
fijan sobre Caja Motor, no sobre el Patrimonio Financiero completo —
ver más abajo.

**Patrimonio de Uso.** Su propósito es la utilidad vital y la calidad
de vida. No se mide por rentabilidad financiera y el SOP no impone
puertas automáticas sobre él.

**Patrimonio de Consumo — eliminado como categoría.** Coches, relojes,
vacaciones u otros gastos de disfrute son consumo. No son asignación
patrimonial y quedan fuera del balance gobernado por el SOP.

### El puente: extracción de Patrimonio Financiero hacia Patrimonio de Uso

El SOP no bloquea automáticamente una extracción de capital desde
Patrimonio Financiero hacia Patrimonio de Uso.

Lo que sí exige es transparencia sobre el coste de oportunidad.

Antes de extraer capital, el sistema debe estimar el impacto temporal
de esa decisión:

> ¿Cuántos meses o años retrasa esta extracción la consecución de los
> objetivos financieros a 5, 10 y 15 años?

Este cálculo es un **warning informativo**, no una puerta de bloqueo.

La decisión final pertenece a Armando. El SOP informa del coste
financiero; no decide si la utilidad vital compensa ese coste.

El cálculo usará una hipótesis de rentabilidad explícita y revisable.
Puede tomar como referencia información del Research Engine, pero no
queda gobernado automáticamente por la expectativa del Assessment
Engine.

### Objetivo de Caja Motor e hipótesis de rentabilidad

Los objetivos cuantificados X/Y/Z se fijan por necesidad patrimonial:
cuánto capital exige sostener la vida elegida y la libertad futura.

No se fijan proyectando el mercado hacia delante. La proyección solo
sirve para evaluar si la trayectoria actual va camino de cumplir esos
objetivos.

En esta versión, X/Y/Z se definen como objetivos de Caja Motor, no como
objetivos del Patrimonio Financiero completo. Caja Seguridad y Caja
Rentas Pasivas cumplen funciones distintas y se gobiernan por sus
propias reglas.

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

### Nivel 4 — Estrategias de inversión dentro de cada caja

P. ej., dentro de Caja Motor: concentración actual en S&P 500 frente a
diversificación gradual hacia un índice mundial. Sin reglas todavía —
es exactamente el terreno de Portfolio Reallocation Protocol (Sección
3).

### Nivel 5 — Productos concretos

Vanguard S&P 500, fondos monetarios, JGPI, etc.

### Por qué esta jerarquía importa

Puedes cambiar cualquier elemento de un nivel inferior sin reescribir
los superiores — cambiar un producto en el Nivel 5 no debería obligar
a tocar el Nivel 1. Es la misma disciplina de responsabilidad única y
estabilidad arquitectónica que ya rige el código del Research Engine,
aplicada al patrimonio completo.

------------------------------------------------------------------------

## 3. Protocolos del SOP

| Protocolo | Gobierna | Estado |
|---|---|---|
| **Dry Powder Protocol** | Convertir liquidez ociosa (Caja Seguridad) en capital invertido durante un episodio de caída | 85-90% aislado. Cuatro reglas completas, techo extraordinario del 90% vía Human Approval ya calculado por fórmula (RE-032.10). Sin wiring a `run.py`/`DecisionEngine`, deliberado. |
| **Human Approval** | Consentimiento humano vigente, independiente de si los datos permiten actuar | 75-80% operativo real. Chain-resolution completa, cooling-off 14/30 días, validez 90 días, extensión propia de 30 días para el techo del 90%. Demostrado end-to-end en `audit_posture.py`. Sin atestaciones reales cargadas todavía. |
| **Portfolio Reallocation Protocol** | Vender un activo de riesgo del Patrimonio Financiero para comprar otro (rotación **dentro** del Patrimonio Financiero, nunca hacia Patrimonio de Uso) | 0-5%. Sin reglas, sin código, sin Excel. Ver Sección 6. |

Los protocolos son prerrequisitos independientes entre sí — ninguno
compensa a otro. Para actuar hacen falta todos los que apliquen a la
vez: la postura combinada de evidencia, Human Approval vigente, y las
reglas propias del protocolo en cuestión (Dry Powder o Reallocation).

Frontera importante fijada el 2026-08-13: mover capital de Patrimonio
Financiero hacia Patrimonio de Uso (p. ej., vender S&P 500 para
financiar Santoña) **no es** una decisión de Portfolio Reallocation
Protocol — es una decisión personal, informada por "El puente"
(Sección 2), no gobernada por ningún protocolo del SOP.

------------------------------------------------------------------------

## 4. Research Engine (resumen)

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
alcance en todo el proyecto.

Estado técnico completo, motor a motor, con cada iteración justificada
y cada test verificado: `docs/GOVERNANCE/SOP_ENGINE_PROJECT_STATUS.md`
(v1.90 a fecha de este documento).

------------------------------------------------------------------------

## 5. Entregables existentes

Lo que hoy existe de verdad en el repositorio, no lo que está previsto:

**Motores y gates** (`engine/`) — módulos principales, incluyendo el
núcleo del Research Engine, `evidence_quality_gate.py`,
`regime_comparability_gate.py`, `personal_capacity_facts_gate.py`,
`gate_combination.py`, `posture_mapper.py`, `dry_powder_protocol.py`,
`dry_powder_ledger_state.py`, `human_approval.py`,
`human_approval_state.py`.

**Loaders** (`loaders/`) — un loader por fuente de datos real:
`dry_powder_ledger_loader.py`, `human_approval_loader.py`,
`personal_capacity_facts_loader.py`, `shiller_loader.py`.

**Datos reales** (`data/raw/`):

| Archivo | Estado |
|---|---|
| `personal_capacity_facts.xlsx` | **Con datos reales cargados.** AMS resuelve `adequate` (nueve hechos verificables, cero rupturas); AML resuelve `constrained` (`liquidity_adequate` con ruptura confirmada, hallazgo real). Incluye dos pestañas adicionales, `Cajas` y `Proyecciones` (añadidas 2026-08-13): `Cajas` clasifica cada partida de AMS/AML en Seguridad/Motor/Rentas Pasivas por fórmula, con % de cada caja sobre el total (control de cuadre a 0€ frente al total patrimonial de cada hoja); `Proyecciones` congela una fecha e importe de referencia de Caja Motor (no enlazados por fórmula a `Cajas` — solo cambian con actualización explícita), calcula la trayectoria esperada a 5/10/15 años desde ese punto fijo bajo la hipótesis base v1, y añade una tabla de Seguimiento donde se registra el saldo real observado en fechas de control futuras frente a lo que la trayectoria esperaba — así se puede ver si se va por delante o por detrás, en vez de comparar el escenario contra sí mismo cada vez. Ilustrativo; no sustituye a los objetivos X/Y/Z todavía pendientes. |
| `dry_powder_ledger.xlsx` | Vacío. Sin episodios de caída registrados todavía. |
| `human_approval_attestations.xlsx` | Vacío. Sin atestaciones registradas todavía. |
| `shiller.xlsx` | Serie histórica completa, fuente del Research Engine. |

**Scripts operativos:** `audit_posture.py` (dry-run de lectura,
combina todos los gates y protocolos por patrimonio, no ejecuta nada).

**Tests:** suite `tests/verify_*.py`, re-ejecutada en cada iteración.

**Documentación:**

- `docs/CONSTITUTION.md` — este documento.
- `docs/GOVERNANCE/SOP_ENGINE_PROJECT_STATUS.md` — estado técnico del
  Research Engine, v1.90.
- `docs/MANUAL_OPERATIVO.md` / `.docx` — manual de uso diario (Dry
  Powder Protocol y Human Approval); Word e idéntico en contenido.

------------------------------------------------------------------------

## 6. Pendiente

**Arquitectura patrimonial (Sección 2):**

- Definir los objetivos cuantificados X/Y/Z de Caja Motor a 5, 10 y 15
  años, por necesidad patrimonial.
- Construir el calculador de impacto temporal para extracciones desde
  Caja Motor hacia Patrimonio de Uso, usando la hipótesis base v1
  fijada en esta Constitución.
- Si `personal_capacity_facts.xlsx` ya considera la vivienda habitual
  en algún cálculo existente — sin verificar todavía, para no dar por
  hecho una respuesta.
- El congelado de `Proyecciones` (fecha de referencia + importes de
  Caja Motor) está fijado provisionalmente a 2026-08-13. Sustituirlo
  por el cierre a 31/12/2026 cuando esté disponible, para anclar la
  trayectoria en año natural.

**Portfolio Reallocation Protocol — todo, ver preguntas abiertas
detalladas en la conversación del 2026-08-13:**

- Disparador (¿episodio de drawdown como Dry Powder, o revisión
  periódica/estructural?).
- Universo de activos (¿solo rotación dentro de Caja Motor, o más
  amplio?).
- Los tres invalidators nombrados en el governance doc necesitan
  definición operativa: liquidez/riesgo del activo vendido,
  correlación entre vendido y comprado, coste de materializar la
  pérdida **o la ganancia** (el caso Motor→índice mundial es
  materializar ganancia, no pérdida — matiz encontrado el 2026-08-13,
  el texto original solo contemplaba pérdida).
- Escala de agresividad propia, o reutilizar las cuatro posturas ya
  existentes.
- Mecanismo: ¿redirigir aportaciones nuevas (sin coste fiscal) y
  vender posición existente (con coste fiscal) son la misma regla o
  dos mecanismos distintos?

**Fuera de alcance, deliberado, en todo el proyecto:**

- Wiring a `run.py` / `DecisionEngine`.
- Ejecución automática de cualquier operación.

**Investigación futura del Research Engine** (menor prioridad que lo
anterior): Similarity Engine v2 (duración, velocidad, tendencia
previa, volatilidad, similitud multidimensional) — siguiente hito
técnico según `SOP_ENGINE_PROJECT_STATUS.md`.

------------------------------------------------------------------------

## 7. Forma de trabajo

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

------------------------------------------------------------------------

## 8. Cómo retomar el proyecto

1. Leer este documento completo — es la autoridad.
2. Para el detalle técnico del Research Engine, leer
   `docs/GOVERNANCE/SOP_ENGINE_PROJECT_STATUS.md`, empezando por su
   "Honest Progress Snapshot".
3. Para operar el día a día (Dry Powder Protocol, Human Approval),
   usar `docs/MANUAL_OPERATIVO.md`.
4. Continuar desde la Sección 6 de este documento (Pendiente).
