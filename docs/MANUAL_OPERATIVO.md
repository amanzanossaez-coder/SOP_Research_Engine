# MANUAL OPERATIVO — SOP Research Engine

Este manual sirve para operar el SOP en la práctica.

No explica por qué existen las reglas ni cómo está diseñado el sistema.
Eso vive en `docs/GOVERNANCE/SOP_ENGINE_PROJECT_STATUS.md`.

Aquí solo se explica:

- qué revisar;
- qué rellenar;
- cuándo actuar;
- cuándo no hacer nada.

Se escribe bloque a bloque, en el orden en que cada pieza queda cerrada.
Hoy: Dry Powder Protocol y Human Approval.

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
- **Importante:** este protocolo no ejecuta nada. No mueve dinero, no
  conecta con ningún bróker. Solo te dice si, según las reglas, hoy se
  puede desplegar un tramo y cuál sería el importe — la decisión de
  ejecutarlo es siempre tuya.

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
    frena. El techo del 40% y el del 80% no funcionan igual — ver el
    aviso justo debajo de esta lista.
4.  **Ratchet: el techo no retrocede dentro del mismo episodio.** Si el
    mercado empeora y subes a `Aggressively`, ese techo se mantiene
    como referencia aunque luego la postura se relaje a `Partially` —
    no se "recarga" capacidad de tramo por bajar y volver a subir. Solo
    se resetea cuando el episodio se cierra de verdad (recuperación
    completa, ver 1.4).

> **El matiz que más se pierde: el 40% y el 80% no son la misma regla.**
> El techo del 40% en `Deploy Partially` **no tiene excepción.** Si se
> alcanza, no se despliega más bajo esa postura — punto. El techo del
> 80% en `Deploy Aggressively` **sí puede superarse**, pero solo con
> una atestación de Human Approval vigente y explícita. El sistema no
> calcula automáticamente cuánto desplegar más allá de ese techo —
> esa cifra la fijas tú a mano, según lo atestiguado.

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
Sección 1 otra vez — se queda como está hasta el cierre (ver 1.4).

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

### 1.4 Qué pasa cuando termina un episodio

El historial no se borra nunca. Un episodio se cierra cuando el mercado
recupera del todo su máximo anterior (Drawdown vuelve a 0). Cuando eso
pase, en el próximo episodio la Sección 1 vuelve a pedir fecha y
pólvora seca inicial nuevas — el ratchet y el acumulado se calculan
solo sobre las filas de la Sección 2 cuya fecha caiga dentro del
episodio actual. Las filas del episodio anterior se quedan en el
histórico, sin tocar.

### Checklist rápido

Antes de actuar:

- Ejecuta `python3 audit_posture.py`.
- Comprueba si hay episodio activo.
- Si no hay episodio activo, no hagas nada.
- Si hay episodio activo, revisa la pestaña AMS o AML.
- Si es la primera vez que aparece este episodio, rellena antes la
  Sección 1 (fecha inicio + pólvora seca inicial) — sin eso, el
  sistema no calcula ningún tramo.
- Si el sistema autoriza un tramo, decide si lo ejecutas.
- Si lo ejecutas, registra una fila nueva en la Sección 2 del Excel.
- No borres ni sobrescribas filas anteriores.

------------------------------------------------------------------------

## 2. Human Approval

### 2.1 Para qué sirve

Human Approval sirve para evitar que cambies tus propias reglas en
caliente.

En una caída fuerte, o en un momento de euforia, puede ser tentador
subir tu tolerancia al riesgo justo cuando menos deberías fiarte de
esa decisión.

Este protocolo no te impide cambiar tu tolerancia. Lo que hace es
poner una pausa obligatoria antes de que una subida empiece a contar.

La pregunta que responde es:

> ¿Tengo una autorización vigente de mi "yo en frío" para actuar hasta
> esta postura?

Human Approval no decide si el mercado es atractivo. Tampoco mueve
dinero. Solo dice si tienes permiso personal vigente para actuar.

Para ejecutar una decisión hacen falta las dos cosas:

- que la postura combinada del SOP lo permita;
- que Human Approval esté vigente.

Una no compensa la otra.

### 2.2 Reglas principales

#### 1. Subir tolerancia nunca aplica al instante

Si autorizas una postura más agresiva que la vigente, entra en
cooling-off. Plazos actuales:

- 14 días en condiciones normales;
- 30 días si hay crisis de mercado o crisis personal.

Mientras dura el cooling-off, esa subida todavía no cuenta.

#### 2. La autorización anterior sigue mandando

Si ya tenías una autorización válida, no quedas bloqueado mientras
esperas. Durante el cooling-off sigue vigente la autorización
anterior.

Ejemplo:

- tenías `Prepare`;
- registras subida a `Deploy Partially`;
- durante 14 días sigues teniendo `Prepare`;
- al terminar el plazo, pasa a `Deploy Partially`.

#### 3. Bajar tolerancia aplica inmediatamente

Si reduces tu postura autorizada, el cambio aplica en el momento. No
hay cooling-off para ser más conservador. También aplica
inmediatamente si repites la misma postura.

#### 4. Toda autorización caduca

Cada autorización dura 90 días desde su fecha de registro. Si no hay
ninguna autorización vigente, Human Approval queda bloqueado hasta que
registres una nueva.

Renovar la misma postura (regla 3) reinicia este plazo de inmediato,
sin esperar cooling-off — es la forma de evitar quedarte bloqueado si
se acerca la caducidad y sigues de acuerdo con tu techo actual.

#### 5. Las crisis solo alargan el cooling-off

Hay dos tipos de crisis: crisis de mercado y crisis personal.

La crisis de mercado la calcula el sistema. Tú no la escribes. La
crisis personal la declaras tú en el Excel.

Ninguna de las dos autoriza ni bloquea por sí sola. Solo hacen una
cosa: si estás subiendo tolerancia, el cooling-off pasa de 14 a 30
días. Nunca lo acortan.

#### 6. El sistema mira toda la historia

El sistema no compara solo la última fila contra la anterior.
Reconstruye qué autorización estaba realmente vigente en cada momento.

Esto evita saltarse el cooling-off encadenando revisiones. Si una
subida todavía no había entrado en vigor, no cuenta como punto de
partida para la siguiente.

### 2.3 Cómo revisar el estado

Ejecuta:

```bash
python3 audit_posture.py
```

Busca:

```text
Human Approval state (AMS)
Human Approval state (AML)
```

Recomendación práctica:

- revísalo cada vez que ejecutes `audit_posture.py`;
- como mínimo, una vez al trimestre;
- no esperes a que caduque.

No hay aviso automático. Si no lo revisas, puede caducar sin que te
enteres.

### 2.4 Excel de Human Approval

Archivo:

```text
data/raw/human_approval_attestations.xlsx
```

Hay una pestaña por patrimonio: `AMS`, `AML`.

Añade una fila nueva cada vez que registres o revises formalmente tu
autorización. No borres filas antiguas. No sobrescribas filas pasadas.

### 2.5 Qué rellenar

| Columna | Qué escribir |
|---|---|
| `Fecha (calendario real, AAAA-MM-DD)` | Fecha del día en que haces la atestación — **no** la fecha en la que esperas que termine el cooling-off. Esa la calcula el sistema solo (`effective_date`). |
| `Postura aprobada` | Techo máximo que te autorizas. No es la postura del mercado de hoy. |
| `Crisis personal declarada` | `Sí` o `No`. Sé honesto. Solo afecta al cooling-off si estás subiendo tolerancia. |
| `Nota` | Contexto para tu futuro yo. |

> A diferencia de la Sección 1 de Dry Powder Protocol (que usa el mes
> Shiller en formato decimal, ej. `2026.07`), aquí la fecha es siempre
> calendario real. No mezcles los dos formatos.

No hay columna de crisis de mercado. El sistema la calcula solo
usando la fecha de la atestación y el drawdown de mercado de ese día.

> **Sobre superar el techo del 80% de Dry Powder Protocol:** RE-041.1
> prevé que Human Approval pueda autorizar excepcionalmente ampliar
> ese techo hasta el 90% en `Deploy Aggressively`. El diseño de esa
> pieza ya está cerrado y la lógica interna existe (`engine/human_approval.py`),
> pero **todavía no es utilizable**: no hay columna en este Excel para
> registrarla, y `audit_posture.py` sigue sin conectarla a Dry Powder
> Protocol. Esta sección se actualizará cuando esté construida de
> punta a punta — hasta entonces, esa vía de excepción no existe en la
> práctica, aunque el protocolo la contemple.

### 2.6 Qué significa cada estado

| Estado | Significado | Qué hacer |
|---|---|---|
| `missing` | Nunca has registrado autorización. | Bloqueado. Registra una primera fila. |
| `expired` | No queda autorización vigente. | Bloqueado. Registra una nueva. |
| `under_cooling_off` | Hay una subida esperando y no hay autorización anterior válida que cubra mientras tanto. | Esperar hasta la fecha efectiva. |
| `valid` | Hay autorización vigente. | Mira `effective_posture_ceiling`. Ese es tu techo personal actual. |

Si el estado es `valid`, puede existir además una subida pendiente. En
ese caso:

- `effective_posture_ceiling` = lo que manda hoy;
- `pending_increase` = subida futura que todavía no aplica.

### 2.7 Checklist rápido

Antes de actuar:

- Ejecuta `python3 audit_posture.py`.
- Revisa el bloque Human Approval.
- Comprueba que el estado sea `valid`.
- Mira `effective_posture_ceiling`.
- Si hay `pending_increase`, no la uses todavía.
- Si quieres subir tolerancia, registra una fila nueva y espera el
  cooling-off.
- Si quieres bajar tolerancia, registra una fila nueva; aplica
  inmediatamente.
- Declara crisis personal si existe.
- No borres ni edites filas anteriores.
- No intentes forzar la excepción del techo del 80% en Dry Powder
  Protocol: el diseño ya existe en el código, pero todavía no es
  utilizable (ver 2.5). Trátalo como límite absoluto, hoy.

Recuerda:

> Human Approval vigente no basta para actuar. También hace falta que
> la postura combinada del SOP y el Dry Powder Protocol lo permitan.

------------------------------------------------------------------------

*Manual completo por ahora. Superar el techo del 80% de Dry Powder
(ver nota en 2.5) y Portfolio Reallocation Protocol quedan pendientes
de que el propio sistema los tenga construidos.*
