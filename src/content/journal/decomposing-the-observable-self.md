---
title: "Decomposing the Observable Self"
date: 2025-01-18
description: "A framework for understanding what signals from images and video can tell us about human identity—and what they cannot."
---

How much of a person can be understood from what is visible? This question sits at the intersection of philosophy, psychology, and computer vision. As we build systems that extract signals from images and video, we need a framework for what these signals represent—and the epistemic limits of observation.

## The Inner-Outer Distinction

William James (1890) distinguished between the "I" (the knowing self) and the "Me" (the known self—the self as object). The "Me" includes the material self (body, possessions), the social self (recognition from others), and the spiritual self (inner thoughts, dispositions). Only portions of the "Me" are externally observable.

Goffman (1959) extended this with dramaturgy: we perform versions of ourselves for different audiences. The "front stage" self—what others see—is curated, contextual, and strategic. The "back stage" self remains hidden. Any system that observes humans captures only front-stage performances.

**Implication for taocore-human**: Signals extracted from images represent *performed* identity, not essential identity. A face in a photograph is a moment of presentation, not a window to character.

## What Can Be Extracted from Images and Video

Computer vision has made significant progress in extracting human-related signals. Following the taxonomy from Vinciarelli et al. (2009) on social signal processing, we can categorize observable attributes:

### Geometric and Spatial Signals

| Signal Type | What It Measures | Reliability |
|------------|------------------|-------------|
| Face detection | Presence and location of faces | High (>95% in good conditions) |
| Facial landmarks | 68+ points defining face geometry | High |
| Body pose | Joint positions (skeleton estimation) | Moderate-High |
| Gaze direction | Where someone is looking | Moderate |
| Proximity | Physical distance between people | High (with calibration) |
| Gesture | Hand and body movements | Moderate |

### Temporal Signals (Video)

| Signal Type | What It Measures | Reliability |
|------------|------------------|-------------|
| Co-occurrence | Who appears together over time | High |
| Turn-taking | Patterns of interaction timing | Moderate |
| Synchrony | Movement coordination between people | Moderate |
| Trajectory | Movement patterns through space | High |

### Expression and Affect Signals

This is where reliability degrades and interpretation becomes fraught.

| Signal Type | What It Claims | Actual Reliability |
|------------|----------------|-------------------|
| Facial Action Units (AUs) | Muscle movements in face | Moderate |
| Emotion classification | Categorical emotion labels | **Low-Contested** |
| Valence-Arousal | Dimensional affect | Moderate for extremes |

Barrett et al. (2019) demonstrated that the mapping from facial configuration to emotional state is far weaker than commonly assumed. Facial expressions are culturally variable, context-dependent, and individually different. A "smile" detected by a classifier may indicate joy, politeness, discomfort, or nothing at all.

**Implication for taocore-human**: We extract Action Units and valence-arousal as *signals*, but refuse to label emotions. The system should say "elevated AU12 (lip corner puller)" not "happy."

## Demographic and Physical Attributes

Beyond expression, images reveal (or seem to reveal) demographic characteristics:

### Race and Ethnicity

Automated race classification is technically possible but ethically contested (Buolamwini & Gebru, 2018). Key concerns:

- Race is socially constructed, not a stable biological category
- Classification systems embed historical biases
- Accuracy varies dramatically across groups
- The act of classification can reinforce harmful categorization

**Position for taocore-human**: We do not extract race. If skin tone is relevant for technical reasons (e.g., lighting normalization), it is treated as a continuous signal, not a categorical identity.

### Gender

Similar concerns apply. West et al. (2019) documented the harms of automated gender classification:

- Conflates sex, gender identity, and gender expression
- Binary classification erases non-binary identities
- High error rates for transgender individuals
- Reinforces surveillance of gender non-conformity

**Position for taocore-human**: We do not classify gender. Presentation features (clothing, hair, makeup) can be described without inferring identity categories.

### Age

Age estimation is less ethically fraught but still unreliable:

- Mean absolute error of 5-8 years in best systems
- Accuracy varies by actual age and demographics
- "Apparent age" differs from chronological age

**Position for taocore-human**: If age is extracted, it is presented as a range with uncertainty, labeled as "apparent age" not actual age.

### Physical Attributes

Some physical characteristics can be measured with reasonable reliability:

- Height (with reference objects or calibration)
- Body proportions
- Clothing and accessories
- Hair characteristics

These remain *descriptions*, not *inferences*. Describing what is visible is different from inferring what it means.

## The Signal-to-Meaning Gap

The fundamental challenge is the gap between extractable signals and meaningful interpretation. Consider this hierarchy:

```
Level 1: Pixels (raw data)
   ↓
Level 2: Geometric features (faces, poses, positions)
   ↓
Level 3: Behavioral signals (expressions, movements, co-occurrence)
   ↓
Level 4: Psychological inference (emotions, intentions, personality)
   ↓
Level 5: Identity claims (who someone "is")
```

Each transition loses reliability. Levels 1-2 are largely objective. Level 3 is measurable but context-dependent. Levels 4-5 are interpretive and often unjustified.

**Principle**: taocore-human operates at Levels 2-3. It extracts and reports signals. It does not infer psychology or claim identity.

## What Else Helps Us Understand Ourselves?

Beyond image/video signals, other modalities contribute to self-understanding:

### Voice and Speech

- Prosody (pitch, rhythm, intensity) carries affective information
- Speech content reveals thought patterns
- Voice quality is relatively stable across time

Schuller & Batliner (2013) provide a comprehensive review of computational paralinguistics.

### Physiological Signals

- Heart rate variability
- Skin conductance
- Respiration patterns

These are less accessible in typical image/video scenarios but offer more direct windows to autonomic states (Kreibig, 2010).

### Digital Traces

- Social media activity
- Communication patterns
- Location history

Kosinski et al. (2013) controversially demonstrated personality prediction from Facebook likes—raising significant privacy concerns.

### Self-Report

The most direct but not always accurate:

- Questionnaires (Big Five, etc.)
- Experience sampling
- Interviews

## A Framework for Ethical Signal Extraction

Drawing from the above, we propose constraints for systems that observe humans:

1. **Signal, not inference**: Report what is measured, not what it supposedly means
2. **Uncertainty quantification**: Every signal carries confidence; present it
3. **Refusal capability**: Decline to interpret when data quality is insufficient
4. **No identity categories**: Avoid race, gender, emotion labels
5. **Aggregation over individuals**: Prefer group patterns to individual profiles
6. **Temporal stability**: Trust convergent signals over momentary observations
7. **Transparency**: Document what is extracted and what is not

## Toward Equilibrium-Based Understanding

The equilibrium concept from TaoCore offers a principled approach: rather than trusting any single observation, we ask what state the signals converge toward over time. Non-convergence indicates ambiguity—and ambiguity should be reported, not hidden.

This connects to Bayesian approaches in perception (Knill & Pouget, 2004): the brain integrates uncertain signals over time, weighting by reliability. A computational system for understanding humans should do the same.

---

## References

Barrett, L. F., Adolphs, R., Marsella, S., Martinez, A. M., & Pollak, S. D. (2019). Emotional expressions reconsidered: Challenges to inferring emotion from human facial movements. *Psychological Science in the Public Interest*, 20(1), 1-68.

Buolamwini, J., & Gebru, T. (2018). Gender shades: Intersectional accuracy disparities in commercial gender classification. *Proceedings of the Conference on Fairness, Accountability and Transparency*, 77-91.

Goffman, E. (1959). *The Presentation of Self in Everyday Life*. Anchor Books.

James, W. (1890). *The Principles of Psychology*. Henry Holt and Company.

Knill, D. C., & Pouget, A. (2004). The Bayesian brain: The role of uncertainty in neural coding and computation. *Trends in Neurosciences*, 27(12), 712-719.

Kosinski, M., Stillwell, D., & Graepel, T. (2013). Private traits and attributes are predictable from digital records of human behavior. *Proceedings of the National Academy of Sciences*, 110(15), 5802-5805.

Kreibig, S. D. (2010). Autonomic nervous system activity in emotion: A review. *Biological Psychology*, 84(3), 394-421.

Schuller, B., & Batliner, A. (2013). *Computational Paralinguistics: Emotion, Affect and Personality in Speech and Language Processing*. John Wiley & Sons.

Vinciarelli, A., Pantic, M., & Bourlard, H. (2009). Social signal processing: Survey of an emerging domain. *Image and Vision Computing*, 27(12), 1743-1759.

West, S. M., Whittaker, M., & Crawford, K. (2019). *Discriminating Systems: Gender, Race and Power in AI*. AI Now Institute.
