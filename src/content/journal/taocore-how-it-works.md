---
title: "How TaoCore Works (Math and Logic for Engineers)"
date: 2026-04-05
description: "A plain-English deep dive into TaoCore’s primitives, metrics, and equilibrium solver."
---

This is a deep dive into TaoCore’s math and logic, written for software engineers who haven’t studied data science. The goal is not to impress you with formulas; it’s to make the system understandable, auditable, and predictable.

## 1. The core idea

TaoCore models a system as:

- **A graph** of entities and relationships
- **A state vector** of numeric signals
- **Metrics** that measure structure and dynamics
- **An equilibrium solver** that finds stable states

If you can understand “data structures + iteration + error checking,” you can understand TaoCore.

## 2. Primitives (the data model)

### Node

A node represents an entity with numeric features and optional time decay.

- `features` is just a dict of numbers (e.g., `{"energy": 0.7}`)
- `timestamp` + `decay_rate` let you compute freshness

The decay rule is exponential:

```text
strength(t) = exp(-decay_rate * age)
```

That gives a smooth, monotonic “freshness” factor.

### Edge

An edge connects two nodes and has a weight. It can be **directed** or **undirected**. If it’s undirected, we add adjacency in both directions. This matters because centrality and clustering depend on connectivity.

Implementation note: in the code, `directed=False` is a first‑class flag on `Edge`, and `Graph.add_edge` mirrors adjacency when it’s false.

### Graph

The graph stores:

- Nodes (by id)
- Edges
- Adjacency (neighbors)

Most graph operations are BFS-style traversal: “What’s connected?” “How far?” “Which path?”

### StateVector

A `StateVector` is just a numeric array. It can be built from a dict or a NumPy array. Distances use Euclidean norm:

```text
distance(a, b) = ||a - b||_2
```

If you build from dicts, TaoCore aligns keys deterministically so distances are valid. If keys or shapes mismatch, it raises instead of silently computing a wrong distance.

## 3. Equilibrium solver (fixed-point iteration)

The solver repeatedly applies an update rule until the system stabilizes. This is the classic fixed‑point iteration:

```text
x_{t+1} = f(x_t)
```

If it converges, you have a fixed point `x*` where:

```text
f(x*) = x*
```

Why this matters: Many real systems “settle” into stable patterns. The fixed‑point method gives a principled way to find that stable state or detect that one doesn’t exist. If the sequence oscillates, TaoCore surfaces that as a failure mode instead of hiding it.

Implementation details:
- Residuals are tracked at every step.
- Convergence can require a stability window (N consecutive steps).
- Oscillation detection checks 2‑cycle and 3‑cycle patterns.

Reference: fixed‑point iteration is standard numerical analysis.  
See: https://en.wikipedia.org/wiki/Fixed-point_iteration

## 4. Metrics: what TaoCore measures

### BalanceMetric (bounds compliance)

Given acceptable ranges, it penalizes out‑of‑bounds values:

```text
score = 1.0                       if min <= value <= max
score = max(0, 1 - dist / range)  otherwise
```

This makes the logic explicit: you can see exactly why a score drops.

### FlowMetric (dynamics)

Given a sequence of states, we compute deltas:

```text
delta_t = x_{t+1} - x_t
```

Modes:

- **Coherence**: are step sizes consistent?
- **Volatility**: how big are the steps?
- **Directionality**: are step directions aligned?

Directionality uses cosine similarity (range -1 to 1).  
Reference: https://www.ibm.com/think/topics/cosine-similarity

### ClusterMetric (structure)

Three clustering strategies:

- **Connected components** (graph connectivity)
- **Modularity** (community structure)
- **Distance-based** (feature similarity)

Reference: https://www.baeldung.com/cs/graph-connected-components

### HubMetric (centrality)

Centrality measures capture influence in the graph:

- Degree
- Betweenness
- Eigenvector
- PageRank

References:
- Degree: https://en.wikipedia.org/wiki/Centrality
- Betweenness: https://en.wikipedia.org/wiki/Betweenness_centrality
- Eigenvector: https://en.wikipedia.org/wiki/Eigenvector_centrality
- PageRank (random surfer + dangling nodes): https://en.wikipedia.org/wiki/PageRank

### AttentionMetric (relevance)

Two modes:

- **Similarity**: cosine or Euclidean similarity between feature vectors
- **Composite**: weighted mix of similarity, recency, and strength

This makes the logic inspectable and tunable.

Implementation details worth noting:

- PageRank handles “dangling nodes” (no outgoing edges) by redistributing rank across all nodes.
- Attention can blend similarity, recency, and decay‑based strength into one score.

## 5. Why this is engineering‑friendly

TaoCore is designed for **bounded claims**:

- Deterministic metrics
- Explicit weights
- Diagnosable convergence
- Clear failure modes (oscillation, non‑convergence)

It doesn’t guess. It measures and reports.

## 6. Evidence in the codebase

The tests in `tests/` verify:

- Graph traversal and edge cases
- Metric correctness
- Equilibrium convergence and oscillation detection
- Attention scoring and temporal decay

If you want to validate behavior, the tests are the first place to look:

- `tests/test_solvers.py` (convergence + oscillation)
- `tests/test_metrics.py` (balance/flow/cluster/hub/composite)
- `tests/test_attention.py` (similarity + composite attention)

## 7. What to read next

If you want to go deeper:

- `src/taocore/primitives/` for data structures
- `src/taocore/metrics/` for measurable logic
- `src/taocore/solvers/equilibrium.py` for fixed‑point iteration

I can also add a walkthrough with concrete inputs if that would help.
