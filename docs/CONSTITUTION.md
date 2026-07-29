# SOP — Sistema Operativo Patrimonial

> Un sistema de decisión patrimonial basado en evidencia, no en predicciones.

---

# ¿Qué es el SOP?

El Sistema Operativo Patrimonial (SOP) es un framework diseñado para ayudar a tomar decisiones patrimoniales de forma objetiva, consistente y reproducible.

Su objetivo no es predecir el futuro de los mercados.

Su objetivo es construir un proceso de decisión robusto apoyado en datos, principios y evidencia histórica.

El Research Engine constituye el núcleo analítico del sistema.

---

# Filosofía

El SOP se fundamenta en cinco principios:

- Pensar en décadas, no en meses.
- Separar evidencia de opinión.
- Mantener una arquitectura patrimonial estable.
- Utilizar reglas objetivas.
- Minimizar la influencia emocional en la toma de decisiones.

---

# Arquitectura del proyecto

```
SOP_RESEARCH_ENGINE/

├── core/
├── data/
│   ├── raw/
│   ├── processed/
│   └── outputs/
│
├── docs/
│   ├── CONSTITUTION.md
│   ├── PROJECT_STATE.md
│   └── ROADMAP.md
│
├── engine/
├── loaders/
├── models/
├── notebooks/
├── reports/
├── tests/
│
├── README.md
├── requirements.txt
└── run.py
```

---

# Módulos

## core

Infraestructura común del sistema.

Contiene constantes, contratos, excepciones y componentes compartidos.

---

## data

Datos utilizados por el motor.

raw
: datos originales

processed
: datos transformados

outputs
: resultados generados

---

## engine

Implementación de todos los motores de análisis.

Ejemplos:

- Drawdown Engine
- Snapshot Engine
- Similarity Engine
- Probability Engine
- Inference Engine
- Assessment Engine
- Decision Engine

---

## models

Modelos de datos utilizados por el sistema.

---

## loaders

Carga y preparación de datasets.

---

## docs

Documentación funcional del proyecto.

### CONSTITUTION

Principios del SOP.

### PROJECT_STATE

Estado actual del desarrollo.

### ROADMAP

Hoja de ruta del proyecto.

---

# Estado actual

El proyecto se encuentra en desarrollo activo.

El núcleo funcional del Research Engine ya está operativo y continúa evolucionando mediante iteraciones incrementales.

---

# Forma de trabajo

Durante el desarrollo seguimos las siguientes reglas:

- Una modificación por iteración.
- Un único archivo por paso.
- Siempre archivos completos.
- Evitar refactorizaciones innecesarias.
- Mantener compatibilidad con el resto del sistema.
- Priorizar claridad y estabilidad.

---

# Objetivo del Research Engine

El Research Engine analiza el contexto histórico del mercado para producir evidencia objetiva.

Actualmente incorpora motores para:

- detección de drawdowns;
- comparación con episodios históricos;
- estimación probabilística;
- inferencia;
- evaluación del contexto;
- generación de decisiones.

No ejecuta operaciones de inversión.

Produce evidencia para que el SOP pueda tomar decisiones consistentes.

---

# Visión a largo plazo

El Research Engine será uno de los módulos del Sistema Operativo Patrimonial.

En el futuro el SOP incorporará, entre otros:

- simulaciones;
- reporting;
- dashboard;
- gestión de triggers;
- gobierno del sistema;
- protocolos patrimoniales.

---

# Cómo ejecutar

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar:

```bash
python3 run.py
```

---

# Inicio de una nueva conversación con ChatGPT

Para retomar el proyecto en un nuevo chat:

1. Adjuntar el repositorio completo (preferiblemente en formato ZIP).
2. Indicar que primero se revisen:
   - `docs/CONSTITUTION.md`
   - `docs/PROJECT_STATE.md`
   - `docs/ROADMAP.md`
3. Continuar desde el estado descrito en `PROJECT_STATE.md`.

Esto permite mantener el contexto técnico y funcional del proyecto sin depender del historial de conversaciones.

---

# Estado del proyecto

En evolución continua.