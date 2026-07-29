# SOP — Project State

Última actualización: Julio 2026

---

# Visión

El Sistema Operativo Patrimonial (SOP) es un sistema completo de gobierno patrimonial.

El objetivo no es construir un modelo predictivo, sino un sistema de decisión objetivo, reproducible y basado en evidencia.

El Research Engine es únicamente uno de los módulos del SOP.

---

# Arquitectura general

SOP

├── Constitución
├── Arquitectura Patrimonial
├── Kernel
├── Dashboard
├── Triggers
├── Protocolos
├── Research Engine
├── Reporting
└── Simulaciones

---

# Estado del Research Engine

## Implementado

✔ Drawdown Engine

✔ Snapshot Engine

✔ Probability Engine

✔ Similarity Engine (v1)

✔ Inference Engine

✔ Assessment Engine

✔ Decision Engine

---

## Refactorizaciones realizadas

Episode ahora almacena:

- peak_index
- bottom_index
- recovery_index

Snapshot ahora almacena:

- index

Snapshot Engine calcula:

- duration_months

El motor continúa funcionando correctamente tras la refactorización.

---

# Estado actual

Motor estable.

Toda modificación futura deberá mantener compatibilidad con:

- Decision Engine
- Assessment Engine
- Similarity Engine

---

# Principios de diseño

- Arquitectura modular.
- Objetos simples.
- Cada Engine tiene una única responsabilidad.
- Ningún cálculo duplicado.
- Todo dato se calcula una sola vez.
- Todo módulo debe poder reutilizarse.

---

# Forma de trabajo

- Un único archivo por iteración.
- Siempre archivo completo.
- Nunca fragmentos.
- Explicaciones cortas.
- Nunca modificar arquitectura sin justificarlo.
- Priorizar estabilidad sobre velocidad.

---

# Objetivo actual

Construir Similarity Engine v2.
