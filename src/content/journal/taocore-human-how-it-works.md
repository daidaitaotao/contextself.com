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
- The adapter enumerates supported image files, loads each with PIL or OpenCV, and yields `ImageFrame` objects.
- Extractors produce signals per frame (faces, expressions, scene quality).

Implementation note: the adapter sorts paths deterministically so results are reproducible.

### Video

- Input: a video file.
- The adapter uses OpenCV to read frames, converts BGR→RGB, and yields `VideoFrame`.
- `get_windows()` slices the video into overlapping windows with `window_duration` and `window_overlap`.

## 3. Signals (extractors)

Extractors produce structured numeric signals:

- Face detection confidence
- Arousal/valence (as proxies, not ground truth)
- Scene illumination and blur (data quality)

By default the pipeline can use **stub extractors** to test without ML dependencies.

Implementation note: stub extractors are seeded, so runs are deterministic given the same seed.

## 4. Graph construction

### Photo pipeline

- Each tracked person becomes a `PersonNode` with aggregated features like coverage ratio and confidence.
- Edges connect people who co‑occur; weight is based on co‑occurrence frequency.
- The graph is a snapshot of “who appears with whom.”

### Video pipeline

Two graph layers:

1. **Per‑window graphs** (temporal)
2. **Aggregated graph** (global)

Window nodes track temporal statistics like arousal/valence trends and group volatility. These signals feed the video report and rejection rules.

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

If the system doesn’t stabilize, the pipeline flags it as unreliable. This is intentionally conservative.

## 7. Conservative decision rules (safety)

The decider is intentionally strict:

- If no person has enough coverage/confidence → reject
- If equilibrium doesn’t converge → reject
- If temporal volatility is too high (video) → reject

Concrete thresholds (defaults):
- Photo: `min_images=3`, `min_coverage=0.3`, `min_confidence=0.5`
- Video: `min_duration=10s`, `window_duration=5s`, `window_overlap=1s`

This makes “no interpretation” the default when data is weak.

## 8. Why this matters

The design is about **bounded claims**:

- Explicit uncertainty
- Structured failure modes
- No hidden inference steps

That’s what makes it safe enough to experiment with in real systems.

The report generator enforces careful language: it uses “signals” and “patterns,” and always attaches limitations and recommendations. Even when interpretation is allowed, it avoids definitive claims.

## 9. Evidence in the codebase

Tests and pipelines live here:

- `taocore_human/pipeline/` for the main logic
- `taocore_human/reports/generator.py` for safety‑focused language
- `taocore_human/nodes/` for feature definitions
- `tests/` for edge cases and correctness

If you want, I can add a tutorial with example inputs/outputs.
