# Research Engine — Domain Model Architecture

## Philosophy

The Research Engine produces objective, reproducible and explainable historical evidence.

Each model has a single responsibility.

The dependency graph must always remain acyclic.

---

# Snapshot

Represents the current market state.

Responsible for describing the present.

Produces:

- Event
- Context

Never contains historical information.

---

# Similarity

Represents the comparison between:

Current Snapshot

and

One Historical Episode.

Responsible only for measuring similarity.

Contains:

- global score
- event scores
- context scores
- outcome scores

Never contains decisions.

Never contains portfolio logic.

---

# SimilarityExplanation

Explains why one historical episode is considered similar.

Local explanation.

Used only inside Similarity.

Contains:

- Event explanation
- Context explanation
- Outcome explanation

---

# Evidence

Aggregates all similar episodes.

Responsible for statistical evidence.

Contains:

- historical sample
- probabilities
- return statistics
- recovery statistics

Never explains itself.

Never makes recommendations.

---

# ResearchExplanation

Explains how the Evidence was produced.

Global explanation.

Contains:

- sample size
- strongest dimensions
- weakest dimensions
- top historical matches
- observations

Never computes statistics.

---

# ResearchResult

Official output of the Research Engine.

Contains:

- Evidence
- ResearchExplanation

Future versions may include:

- Quality
- Metadata

---

# Assessment

Transforms evidence into standardized assessments.

Consumes:

ResearchResult

Produces:

Assessment

Never allocates capital.

---

# Inference

Transforms assessments into objective conclusions.

Consumes:

Assessment

Produces:

Inference

Never executes portfolio decisions.

---

# Constitution

Highest authority.

Consumes:

Inference

Produces:

Rules.

The Constitution is the only component allowed to govern portfolio decisions.