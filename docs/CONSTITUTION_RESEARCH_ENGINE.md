# Constitución del Research Engine

**Versión:** 1.1\
**Guardada en el repositorio:** 2026-08-14

> **Relación con `docs/CONSTITUTION.md`.** En caso de conflicto,
> `docs/CONSTITUTION.md` gobierna el SOP completo; este documento
> gobierna únicamente el Research Engine. No compiten entre sí.

> **Política de versionado.** Cualquier cambio en estos artículos
> exige incrementar la versión constitucional (`core/version.py`'s
> `CONSTITUTION_VERSION`, mantenida en sincronía con la de arriba) y
> registrar la razón -- ver Historial de revisiones al final de este
> documento.

> Este documento existió únicamente en conversación desde el inicio
> del proyecto hasta hoy. `core/version.py` ya definía
> `CONSTITUTION_VERSION` en su referencia a él desde el principio, sin
> que el archivo mismo existiera nunca en el repositorio -- una
> auditoría contra estos doce artículos (`docs/GOVERNANCE/SOP_ENGINE_PROJECT_STATUS.md`,
> entradas RE-044.1 a RE-EXP.1, 2026-08-14) encontró y corrigió cinco
> violaciones reales antes de que este documento se guardara. No es un
> texto nuevo: es el mismo que gobernó esa auditoría, transcrito tal
> cual.

Me gusta llamarlo Constitución del Research Engine porque es exactamente eso: el documento que protege la coherencia del sistema. No es un README técnico ni una guía de uso. Es el conjunto de reglas que ningún módulo podrá romper.

## Artículo 1 · Finalidad

El Research Engine existe para transformar información histórica verificable en evidencia útil para la toma de decisiones patrimoniales.

El motor no promete predecir el futuro ni emite forecasts accionables por sí mismo. Puede medir resultados históricos posteriores para evaluar precedentes y validar hipótesis.

Su función es identificar precedentes históricos comparables, medir su similitud y presentar la evidencia de forma objetiva y reproducible.

## Artículo 2 · Primacía de los hechos

La base de datos únicamente podrá contener hechos observables o importados desde fuentes oficiales.

Nunca almacenará resultados derivados de dichos hechos.

Son hechos:

- Fechas
- Precios
- Índices
- Ratios
- Variables macroeconómicas
- Datos publicados por organismos oficiales

No son hechos:

- Drawdowns
- Duraciones
- Rentabilidades forward
- Similitudes
- Probabilidades
- Clasificaciones
- Inferencias

Toda magnitud derivada deberá calcularse en tiempo de ejecución.

## Artículo 3 · Separación de responsabilidades

El sistema estará dividido en cuatro capas independientes.

**Datos.** Almacena exclusivamente información original.

**Modelos.** Representa la estructura lógica de la información.

**Motor.** Realiza todos los cálculos.

**Presentación.** Comunica los resultados al usuario.

Ninguna capa podrá asumir responsabilidades pertenecientes a otra.

## Artículo 4 · Reproducibilidad

Toda respuesta producida por el motor deberá poder reproducirse utilizando exactamente la misma información disponible en la fecha analizada.

Queda prohibido utilizar información publicada con posterioridad al momento histórico objeto del análisis.

Esto incluye evitar look-ahead bias tanto en datos de mercado como en selección de episodios.

## Artículo 5 · Trazabilidad

Toda respuesta deberá poder reconstruirse completamente.

Será posible identificar:

- datos utilizados
- funciones ejecutadas
- parámetros empleados
- versión del motor
- fuentes consultadas

Ninguna conclusión podrá carecer de trazabilidad.

## Artículo 6 · Evidencia obligatoria

El motor nunca emitirá una conclusión sin mostrar la evidencia que la respalda.

Toda inferencia deberá acompañarse, como mínimo, de:

- episodios utilizados
- número de observaciones
- variables consideradas
- limitaciones relevantes

## Artículo 7 · Gestión de la incertidumbre

El motor nunca expresará una falsa precisión.

Siempre comunicará el tamaño efectivo de la evidencia utilizada.

El nivel de confianza será categórico.

```
Alta
Media
Baja
```

Los nombres exactos podrán expresarse en constantes de código, pero deberán mapearse a categorías discretas.

Los umbrales se definirán como constantes globales del sistema.

Nunca existirán números mágicos distribuidos por el código.

## Artículo 8 · Explicabilidad

Toda conclusión deberá responder inmediatamente a la pregunta: ¿Por qué?

El motor deberá identificar las variables y precedentes que sustentan cada resultado, y las variables o precedentes que lo contradicen.

La explicabilidad forma parte del resultado. No constituye documentación adicional.

## Artículo 9 · Parsimonia

El sistema favorecerá siempre el modelo más sencillo capaz de explicar adecuadamente los datos.

Toda nueva variable incorporada deberá demostrar que aporta información adicional.

Las variables redundantes serán eliminadas.

## Artículo 10 · Robustez

Toda conclusión importante deberá poder someterse a pruebas de sensibilidad.

El motor deberá permitir verificar cómo cambian los resultados al:

- excluir episodios individuales
- modificar parámetros
- ampliar o reducir la muestra
- cambiar criterios de similitud

Una conclusión que dependa de un único episodio deberá indicarlo explícitamente.

## Artículo 11 · Neutralidad

El motor no defenderá ninguna tesis de inversión.

No justificará decisiones previamente tomadas.

No buscará confirmar hipótesis.

Su única función consiste en medir la evidencia disponible.

## Artículo 12 · Conservadurismo epistemológico

Ante dos interpretaciones igualmente plausibles, el motor elegirá siempre la más prudente.

Cuando la evidencia sea insuficiente, la respuesta correcta será:

*No existe evidencia suficiente para concluir.*

Nunca se sustituirá la ausencia de evidencia por una estimación arbitraria.

## Axioma Fundamental

El Research Engine no genera certezas. Genera evidencia estructurada para tomar mejores decisiones.

## Adición de Armando

El valor del Research Engine no reside en acertar el futuro, sino en hacer explícito el razonamiento que conecta los datos históricos con cada decisión. Una respuesta sólo será tan sólida como la evidencia que pueda mostrar y tan fiable como la incertidumbre que sea capaz de reconocer.

---

Si dentro de dos años se incorpora IA, nuevas variables o nuevos módulos, la pregunta a hacerse antes de aceptar cualquier cambio es una sola: ¿viola alguno de estos doce artículos? Si la respuesta es sí, el cambio no entra. Esa disciplina mantiene el motor coherente a largo plazo.

---

## Historial de revisiones

**Versión 1.1 (2026-08-14)** -- primera revisión real desde que el documento se escribió. Cinco matices de Armando, ninguno cambia el espíritu de ningún artículo, todos precisan una redacción que la práctica de hoy ya había puesto a prueba:

- Relación con `docs/CONSTITUTION.md` añadida arriba -- las dos constituciones no competían, pero no estaba dicho por escrito.
- Artículo 1: distingue "prometer predecir" de "medir resultados históricos para evaluar precedentes y validar hipótesis" -- el motor sí calcula `future_return_5y`, MAE, hit-rate y rank correlation (`engine/validation_harness.py`, `engine/validation_metrics.py`); la redacción original podía leerse como que no lo hace.
- Artículo 4: nombra explícitamente el look-ahead bias, en datos de mercado y en selección de episodios.
- Artículo 7: aclara que Alta/Media/Baja es la categoría exigida, no el nombre literal en código (`LOW`, `NOT_DEMONSTRATED`, etc. ya conviven con esto hoy).
- Artículo 8: "variables" pasa a "variables y precedentes" -- RE-EXP.1 (2026-08-14) demostró que la contraevidencia real más útil no es una dimensión de similitud débil, es un episodio histórico disidente.

**Versión 1.0** -- texto original de Armando, sin fecha de commit propia (existió solo en conversación hasta guardarse el 2026-08-14, ver nota de procedencia arriba).
