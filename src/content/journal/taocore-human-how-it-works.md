---
title: "How TaoCore-Human Works (Math and Logic for Engineers)"
date: 2026-04-05
description: "A practical explanation of the photo/video pipelines and conservative decision rules."
---

This entry explains how `taocore-human` uses TaoCore’s math to analyze photos and videos. It’s meant to be understandable to engineers without data science background.

## 1. The pipeline in one sentence

`taocore-human` turns media into measurable signals, builds a graph, runs stability metrics, then **refuses to interpret** when data quality is poor.

## 2. Inputs and adapters

### Photo folders

- Input: a folder of images.
- The adapter yields frames.
- Extractors produce signals per frame (faces, expressions, scene quality).

### Video

- Input: a video file.
- The adapter splits the video into time windows.
- Each window becomes a mini “photo set.”

## 3. Signals (extractors)

Extractors produce structured numeric signals:

- Face detection confidence
- Arousal/valence (as proxies, not ground truth)
- Scene illumination and blur (data quality)

By default the pipeline can use **stub extractors** to test without ML dependencies.

## 4. Graph construction

### Photo pipeline

- Each tracked person becomes a `PersonNode`.
- Edges connect people who co‑occur.
- The graph is a snapshot of “who appears with whom.”

### Video pipeline

Two graph layers:

1. **Per‑window graphs** (temporal)
2. **Aggregated graph** (global)

This lets us measure interaction stability over time, not just overall co‑occurrence.

## 5. Metrics applied

`taocore-human` reuses TaoCore metrics:

- **BalanceMetric**: are signals in plausible bounds?
- **ClusterMetric**: are there sub‑groups?
- **HubMetric**: who is structurally central?
- **FlowMetric** (video): are interactions coherent or volatile?

Metrics are descriptive. They don’t “label” people; they measure structure and dynamics.

## 6. Equilibrium solver

After metrics, the pipeline runs the fixed‑point iteration solver:

```text
x_{t+1} = f(x_t)
```

If the system doesn’t stabilize, the pipeline flags it as unreliable.

## 7. Conservative decision rules (safety)

The decider is intentionally strict:

- If no person has enough coverage/confidence → reject
- If equilibrium doesn’t converge → reject
- If temporal volatility is too high (video) → reject

This makes “no interpretation” the default when data is weak.

## 8. Why this matters

The design is about **bounded claims**:

- Explicit uncertainty
- Structured failure modes
- No hidden inference steps

That’s what makes it safe enough to experiment with in real systems.

## 9. Evidence in the codebase

Tests and pipelines live here:

- `taocore_human/pipeline/` for the main logic
- `tests/` for edge cases and correctness

If you want, I can add a tutorial with example inputs/outputs.
