# MANUAL OPERATIVO — SOP Research Engine

> **¿Qué es esto?** La guía de qué hacer en tu día a día, bloque a
> bloque. Para el "por qué" de cada regla, o para ver el código,
> consulta `docs/GOVERNANCE/SOP_ENGINE_PROJECT_STATUS.md`.

Se escribe bloque a bloque, en el orden en que cada pieza queda cerrada.
Hoy: Dry Powder Protocol.

------------------------------------------------------------------------

## 1. Dry Powder Protocol

### 1.1 De qué va, en 30 segundos

- **El problema que evita:** que te quedes paralizado esperando el
  "suelo perfecto", o que te gastes toda la pólvora seca en la primera
  caída y no te quede nada si el mercado tiene una segunda pierna peor.
- **Qué hace:** convierte una postura (ej. `Deploy Partially`) en una
  cifra concreta de euros a desplegar, tramo a tramo.
- **Dónde encaja:** este protocolo no decide si hoy es buen momento —
  eso ya lo deciden antes las otras piezas del SOP (Evidence Quality,
  Regime Comparability, Personal Capacity), que combinadas producen la
  postura del día. Dry Powder Protocol arranca **después**: dado que
  la postura de hoy ya autoriza desplegar algo, ¿cuánto exactamente?
- **Importante:** es una calculadora de riesgo. No ejecuta nada, no
  mueve dinero, no se conecta a ningún bróker. La decisión y la
  ejecución son siempre tuyas.

**Las 4 reglas clave:**

1.  **Porcentaje sobre lo que queda, no sobre el total inicial.** Cada
    tramo usa un % de la pólvora seca *restante* (12% en `Deploy
    Partially`, 22% en `Deploy Aggressively`). Esto por sí solo no te
    deja nunca a cero, pero tampoco basta: si el episodio dura mucho,
    tramo a tramo puedes acabar desplegando casi todo sin que ninguna
    decisión concreta haya autorizado ese total — para eso está la
    regla 3.
2.  **Cadencia dual (espaciado obligatorio).** Entre un tramo y otro
    deben pasar días mínimos (30 en `Partially`, 14 en `Aggressively`)
    **o** una caída adicional del mercado de 5 puntos porcentuales.
    Basta con que se cumpla una de las dos, no las dos a la vez.
3.  **Techo de seguridad por episodio, cortafuegos, no control diario.**
    No puedes desplegar en total más del 40% de la pólvora inicial en
    `Partially` ni más del 80% en `Aggressively`. Si lo alcanzas, se
    frena — **y aquí hay un matiz importante que se pierde fácil:**
    solo el techo del 80% (`Deploy Aggressively`) tiene una vía de
    excepción, y solo con una atestación de Human Approval vigente que
    lo autorice explícitamente. El techo del 40% en `Partially` **no
    tiene excepción por atestación** — una vez alcanzado, no se
    desplegará más bajo esa postura hasta que el episodio se cierre o
    la postura escale a `Aggressively` (que tiene su propio techo,
    independiente).
4.  **Ratchet: el techo no retrocede dentro del mismo episodio.** Si el
    mercado empeora y subes a `Aggressively`, ese techo se mantiene
    como referencia aunque luego la postura se relaje a `Partially` —
    no se "recarga" capacidad de tramo por bajar y volver a subir. Solo
    se resetea cuando el episodio se cierra de verdad (recuperación
    completa, ver 1.5).

Ninguno de estos números (12%, 22%, 30 días, 14 días, 5 pp, 40%, 80%)
está ajustado contra el histórico de mercado — son parámetros de
estructura de riesgo, versión 1, explícitamente revisables.

### 1.2 Flujo de trabajo

```
       [ 1. Ejecutar script en la terminal ]
                         │
                         ▼
          ¿has_active_episode == True?
            ├── NO  ──> No hacer nada. Fin.
            └── SÍ  ──> [ 2. Abrir Excel y registrar ]
```

**Paso 1 — Comprobar el mercado.** Desde la raíz del repo:

```bash
python3 audit_posture.py
```

Cadencia sugerida (no es una regla del sistema, es recomendación): una
vez por semana en mercado tranquilo, más a menudo si sospechas una
caída relevante. No hay nada automático que te avise — si no lo corres,
no te enteras.

Busca en la salida `Dry Powder Ledger state (AMS)` / `(AML)`:

- `has_active_episode = False` → todo en orden, no toques el Excel.
- `has_active_episode = True` → hay una caída activa, pasa al Paso 2.

**Paso 2 — Rellenar el Excel** (`data/raw/dry_powder_ledger.xlsx`,
pestaña de tu patrimonio, AMS o AML).

**A. Si el episodio ACABA DE EMPEZAR (Sección 1 "EPISODIO ACTUAL"),
solo la primera vez que aparece:**

1.  **Fecha inicio episodio** — copia el `peak_date` exacto que te
    imprime la pantalla (ej. `2026.07`). Tiene que ser exacto al
    decimal: el sistema compara esta celda contra el valor detectado,
    y si no coincide trata la Sección 1 como si no estuviera rellena
    aunque la celda no esté en blanco.
2.  **Pólvora seca inicial (€)** — el total de liquidez que tenías
    disponible para invertir el día que empezó la caída. Esto es
    tuyo, nadie más lo sabe.

Si el episodio sigue abierto en la siguiente revisión, no tocas la
Sección 1 otra vez — se queda como está hasta el cierre (ver 1.5).

> **Regla de oro:** si no sabes qué poner en una celda, escribe
> literalmente `Pendiente`. El sistema lo lee como "no lo sé todavía"
> — nunca como cero, nunca como un valor a adivinar. Nunca dejes una
> celda a medias ni te inventes un número.

**B. Si vas a EJECUTAR UN TRAMO (Sección 2 "REGISTRO DE TRAMOS
DESPLEGADOS"), añade una fila NUEVA cada vez que muevas dinero real —
nunca se borran ni se sobrescriben filas pasadas:**

| Columna | Qué escribir | Ejemplo |
|---|---|---|
| **Fecha** | Fecha real de la transferencia/compra (`AAAA-MM-DD`), no el mes Shiller. | `2026-08-15` |
| **Importe desplegado (€)** | Los euros reales ejecutados. | `15000` |
| **Postura vigente** | La postura que `audit_posture.py` reportó como techo combinado (`COMBINED posture ceiling`) el día del tramo — no la que crees que "debería" ser. | `Deploy Partially` |
| **Nota** | Comentario libre para tu contexto futuro. | Primera compra, caída del 10% |
| **Activo / Instrumento** | Qué compraste. Puramente informativo, no entra en ningún cálculo. | S&P 500 ETF |

> ⚠️ **Atención a la postura:** úsala siempre exacta, tal como
> aparece en el desplegable. Si la dejas vacía, en `Pendiente`, o con
> un texto que no coincide con ninguna de las cinco postura del
> sistema, el importe se sigue contando igual (el dinero se desplegó
> de verdad), pero esa fila deja de contar para el ratchet — el
> sistema no sabrá que ese tramo llegó a una postura más alta, y el
> techo de la próxima recomendación puede salir más bajo de lo que
> debería. El sistema te avisa de esto en su salida si ocurre, pero
> mejor evitarlo desde el origen.

### 1.3 Guía de respuestas del script

`audit_posture.py` te da, por patrimonio, uno de estos cinco estados
exactos:

| Mensaje del script | Qué significa | Qué hacer |
|---|---|---|
| `posture no deployment` | La postura de hoy (`Conserve`/`Prepare`/`Blocked`) no autoriza desplegar nada. | No desplegar. |
| `cadence not met` | Aún no toca: no han pasado ni los días mínimos ni los puntos de caída adicional desde el último tramo. | Esperar. |
| `ceiling reached` | Techo acumulado alcanzado para la postura vigente. En `Partially` (40%) es definitivo hasta cierre o escalada. En `Aggressively` (80%) admite excepción vía Human Approval. | Frenar, salvo excepción en `Aggressively`. |
| `ceiling reached, approved beyond ceiling` | Solo puede pasar en `Deploy Aggressively`, con una atestación de Human Approval vigente que lo autorice. El sistema **no calcula** el importe por fórmula aquí. | Fijar tú a mano la cifra, según lo atestiguado. |
| `authorized` | Luz verde: el sistema te da una cifra concreta (`authorized_amount`). | Recomendación de compra — decides si la ejecutas. |

### 1.4 Cuándo se borra el historial

**Nunca.** Un episodio se cierra cuando el mercado recupera del todo su
máximo anterior (Drawdown vuelve a 0). Cuando eso pase, en el próximo
episodio la Sección 1 vuelve a pedir fecha y pólvora seca inicial
nuevas — el ratchet y el acumulado se calculan solo sobre las filas de
la Sección 2 cuya fecha caiga dentro del episodio actual. Las filas del
episodio anterior se quedan en el histórico, sin tocar.

------------------------------------------------------------------------

*Próxima sección de este manual: Human Approval — pendiente.*
