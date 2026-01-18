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

### Face Detection: The Foundation

Modern face detection has achieved near-human performance under good conditions:

| System/Study | Dataset | Accuracy | Notes |
|-------------|---------|----------|-------|
| RetinaFace (Deng et al., 2020) | WIDER FACE (hard) | 91.4% AP | State-of-the-art |
| MTCNN (Zhang et al., 2016) | FDDB | 95.1% recall | Widely deployed |
| Human performance | FDDB | ~94% | Baseline comparison |

However, accuracy degrades significantly with:
- **Occlusion**: 30-40% drop with partial face coverage (Ge et al., 2017)
- **Pose variation**: 15-25% drop at extreme angles >60° (Zhu & Ramanan, 2012)
- **Low resolution**: Below 20×20 pixels, detection drops to <50% (Yang et al., 2016)
- **Lighting**: Low-light conditions reduce accuracy by 20-35% (Li et al., 2019)

### Facial Landmark Detection

68-point landmark models achieve:

| Model | Dataset | NME (Normalized Mean Error) |
|-------|---------|----------------------------|
| HRNet (Sun et al., 2019) | 300W | 2.87% |
| AWing (Wang et al., 2019) | WFLW | 4.36% |
| Human inter-rater | 300W | ~3.0% |

NME below 4% is considered reliable for downstream tasks. Above 8%, geometric measurements become unreliable.

### Body Pose Estimation

Skeleton estimation accuracy (PCK @ 0.5 threshold—correct if within 50% of head size):

| Model | Dataset | PCK@0.5 |
|-------|---------|---------|
| HRNet (Sun et al., 2019) | COCO | 76.3% |
| OpenPose (Cao et al., 2019) | COCO | 65.3% |
| AlphaPose (Fang et al., 2017) | COCO | 72.3% |

Multi-person scenarios show 10-15% degradation due to occlusion and association errors.

### The Problem with Emotion Recognition

This is where the data most clearly shows the limits of observation.

**Claimed accuracy in controlled conditions:**

| System | Dataset | Reported Accuracy |
|--------|---------|-------------------|
| Commercial API A | FER2013 | 71% |
| Commercial API B | AffectNet | 65% |
| Academic SOTA | RAF-DB | 88% |

**But these numbers are misleading.** Barrett et al. (2019) conducted a meta-analysis of 1,000+ studies and found:

- **Within-culture agreement** on facial expressions: r = 0.39 to 0.58
- **Cross-cultural agreement**: drops to r = 0.20 to 0.45
- **Reliability of "basic emotion" categories**: challenged by 25%+ disagreement even in posed expressions

Key findings from their meta-analysis:

| Expression | % Agreement (Western) | % Agreement (Cross-cultural) |
|-----------|----------------------|------------------------------|
| Happiness | 90% | 69% |
| Sadness | 75% | 56% |
| Anger | 74% | 59% |
| Fear | 65% | 48% |
| Disgust | 65% | 45% |
| Surprise | 83% | 67% |

**Critical insight**: If humans only agree 48-69% cross-culturally on "fear" faces, any algorithm trained on Western-labeled data will embed cultural bias as ground truth.

### Facial Action Units: A More Reliable Alternative

The Facial Action Coding System (FACS; Ekman & Friesen, 1978) describes muscle movements, not emotions:

| AU | Description | Detection Accuracy (F1) |
|----|-------------|------------------------|
| AU1 | Inner brow raiser | 0.51 |
| AU2 | Outer brow raiser | 0.45 |
| AU4 | Brow lowerer | 0.55 |
| AU6 | Cheek raiser | 0.76 |
| AU12 | Lip corner puller | 0.86 |
| AU15 | Lip corner depressor | 0.38 |
| AU25 | Lips part | 0.92 |

Data from BP4D-Spontaneous dataset (Zhang et al., 2014). Note the wide variance—some AUs are detectable, others are not.

**Implication for taocore-human**: We can reliably detect AU12 (lip corner pull). We should not claim "happiness."

## Demographic Attributes: Accuracy and Bias

### Gender Classification Bias

Buolamwini & Gebru (2018) tested three commercial systems on the Pilot Parliaments Benchmark:

| Demographic Group | System A | System B | System C |
|------------------|----------|----------|----------|
| Lighter-skinned males | 0.8% error | 0.0% error | 0.0% error |
| Lighter-skinned females | 6.0% error | 1.7% error | 7.1% error |
| Darker-skinned males | 12.0% error | 0.7% error | 6.0% error |
| Darker-skinned females | 34.7% error | 21.3% error | 34.5% error |

**Error rates for darker-skinned females were up to 43× higher than for lighter-skinned males.**

### Age Estimation

State-of-the-art mean absolute error (MAE) in years:

| Model | MORPH II | FG-NET | UTKFace |
|-------|----------|--------|---------|
| DEX (Rothe et al., 2018) | 2.68 | 4.63 | - |
| SSR-Net (Yang et al., 2018) | 3.16 | 4.48 | 5.21 |
| MV-CNN (Shen et al., 2018) | 2.87 | 4.10 | - |

But MAE varies significantly by actual age:

| Age Group | Typical MAE |
|-----------|-------------|
| 0-20 | 3-5 years |
| 20-40 | 4-6 years |
| 40-60 | 5-8 years |
| 60+ | 8-12 years |

And by demographics (Ricanek & Tesafaye, 2006):
- African American faces: +1.5 years MAE vs. Caucasian
- Female faces: +0.8 years MAE vs. male (on Western-trained models)

**Implication for taocore-human**: If age is reported, it must include uncertainty ranges and acknowledge demographic variation.

### Race Classification: The Data Against It

Accuracy seems high in benchmarks:

| Study | Dataset | Accuracy |
|-------|---------|----------|
| Fu et al. (2014) | MORPH II (3 classes) | 99.1% |
| Guo & Mu (2014) | PCSO (2 classes) | 98.3% |

But these benchmarks are flawed:
1. **Limited categories**: Most use 2-4 racial categories, erasing mixed-race and many ethnic groups
2. **Labeling inconsistency**: Inter-rater agreement on race labels is only 85-90% (Albiero et al., 2020)
3. **Downstream harm**: Identified individuals have been misclassified leading to wrongful arrests (Hill, 2020)

**Position for taocore-human**: We do not extract race. The construct validity is too low and the potential for harm too high.

## Reliability Across Conditions

Real-world performance differs dramatically from benchmark performance:

| Condition | Face Detection | Landmark | Pose | Expression |
|-----------|---------------|----------|------|------------|
| Lab conditions | 95%+ | 97%+ | 85%+ | 70%+ |
| Good natural light | 90%+ | 92%+ | 75%+ | 55%+ |
| Indoor variable | 80%+ | 85%+ | 65%+ | 45%+ |
| Low light | 60%+ | 70%+ | 50%+ | 30%+ |
| Motion blur | 55%+ | 60%+ | 45%+ | 25%+ |
| Occlusion (>30%) | 50%+ | 55%+ | 40%+ | 20%+ |

Data synthesized from multiple studies including WIDER FACE, 300W-LP, and COCO-WholeBody benchmarks.

## The Signal-to-Meaning Gap: Quantified

We can now quantify the degradation at each level:

```
Level 1: Pixels
   ↓ [~5% information loss - compression, noise]
Level 2: Geometric features
   ↓ [10-20% error - detection/estimation]
Level 3: Behavioral signals (AUs, pose)
   ↓ [30-50% error - context-dependent mapping]
Level 4: Psychological inference
   ↓ [50-70% error - weak construct validity]
Level 5: Identity claims
   ↓ [undefined - philosophical category error]
```

**Principle**: taocore-human operates at Levels 2-3, reporting confidence intervals. Levels 4-5 are out of scope.

## What Else Helps Us Understand Ourselves?

### Voice and Speech

Paralinguistic features show moderate reliability:

| Feature | Task | Accuracy/Correlation |
|---------|------|---------------------|
| Pitch variation | Arousal detection | r = 0.45-0.65 |
| Speech rate | Stress detection | r = 0.35-0.50 |
| Voice quality | Depression screening | AUC = 0.70-0.80 |

Data from Schuller & Batliner (2013) computational paralinguistics review.

### Physiological Signals

| Signal | What It Measures | Reliability (r with self-report) |
|--------|-----------------|--------------------------------|
| Heart rate variability | Arousal/stress | 0.40-0.60 |
| Skin conductance | Emotional activation | 0.50-0.70 |
| Pupil dilation | Cognitive load, arousal | 0.35-0.55 |

Data from Kreibig (2010) meta-analysis.

### Digital Behavior

Kosinski et al. (2013) Facebook likes study:

| Trait | AUC (prediction from likes) |
|-------|----------------------------|
| Sexual orientation (male) | 0.88 |
| Sexual orientation (female) | 0.75 |
| Democrat vs. Republican | 0.85 |
| Christian vs. Muslim | 0.82 |
| Openness | 0.73 |
| Conscientiousness | 0.68 |
| Extraversion | 0.70 |

These correlations are strong—and deeply concerning for privacy.

## Framework for Ethical Signal Extraction

Based on the empirical data above:

| Signal Type | Reliability | Should Extract? | How to Report |
|------------|-------------|-----------------|---------------|
| Face presence/location | High (>90%) | Yes | Bounding box + confidence |
| Facial landmarks | Moderate-High (85-95%) | Yes | Points + NME estimate |
| Body pose | Moderate (65-80%) | Yes | Skeleton + PCK confidence |
| Facial AUs | Variable (38-92%) | Selective | Only high-reliability AUs |
| Emotion labels | Low (<60%) | No | - |
| Gender | Biased (65-99%) | No | - |
| Race | Invalid construct | No | - |
| Age | Moderate (±5-8 years) | With uncertainty | Range, not point estimate |

## Conclusion: What the Data Tells Us

The empirical literature supports a position of principled restraint:

1. **Geometric signals** are reliable enough to extract
2. **Behavioral signals** are context-dependent and require uncertainty quantification
3. **Psychological inferences** are unreliable and culturally biased
4. **Identity categorizations** are ethically and empirically unjustified

The data does not support confident claims about who people are. It supports cautious descriptions of what can be observed.

---

## References

Albiero, V., KS, K., Vangara, K., Zhang, H., King, M. C., & Bowyer, K. W. (2020). Analysis of gender inequality in face recognition accuracy. *Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision Workshops*, 81-89.

Barrett, L. F., Adolphs, R., Marsella, S., Martinez, A. M., & Pollak, S. D. (2019). Emotional expressions reconsidered: Challenges to inferring emotion from human facial movements. *Psychological Science in the Public Interest*, 20(1), 1-68.

Buolamwini, J., & Gebru, T. (2018). Gender shades: Intersectional accuracy disparities in commercial gender classification. *Proceedings of the Conference on Fairness, Accountability and Transparency*, 77-91.

Cao, Z., Hidalgo, G., Simon, T., Wei, S. E., & Sheikh, Y. (2019). OpenPose: Realtime multi-person 2D pose estimation using Part Affinity Fields. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 43(1), 172-186.

Deng, J., Guo, J., Ververas, E., Kotsia, I., & Zafeiriou, S. (2020). RetinaFace: Single-shot multi-level face localisation in the wild. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 5203-5212.

Ekman, P., & Friesen, W. V. (1978). *Facial Action Coding System: A Technique for the Measurement of Facial Movement*. Consulting Psychologists Press.

Goffman, E. (1959). *The Presentation of Self in Everyday Life*. Anchor Books.

Hill, K. (2020). Wrongfully accused by an algorithm. *The New York Times*, June 24, 2020.

James, W. (1890). *The Principles of Psychology*. Henry Holt and Company.

Kosinski, M., Stillwell, D., & Graepel, T. (2013). Private traits and attributes are predictable from digital records of human behavior. *Proceedings of the National Academy of Sciences*, 110(15), 5802-5805.

Kreibig, S. D. (2010). Autonomic nervous system activity in emotion: A review. *Biological Psychology*, 84(3), 394-421.

Ricanek, K., & Tesafaye, T. (2006). MORPH: A longitudinal image database of normal adult age-progression. *Proceedings of the International Conference on Automatic Face and Gesture Recognition*, 341-345.

Rothe, R., Timofte, R., & Van Gool, L. (2018). Deep expectation of real and apparent age from a single image without facial landmarks. *International Journal of Computer Vision*, 126(2-4), 144-157.

Schuller, B., & Batliner, A. (2013). *Computational Paralinguistics: Emotion, Affect and Personality in Speech and Language Processing*. John Wiley & Sons.

Sun, K., Xiao, B., Liu, D., & Wang, J. (2019). Deep high-resolution representation learning for visual recognition. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 5693-5703.

Zhang, K., Zhang, Z., Li, Z., & Qiao, Y. (2016). Joint face detection and alignment using multitask cascaded convolutional networks. *IEEE Signal Processing Letters*, 23(10), 1499-1503.

Zhang, X., Yin, L., Cohn, J. F., Canavan, S., Reale, M., Horber, A., ... & Girard, J. M. (2014). BP4D-Spontaneous: A high-resolution spontaneous 3D dynamic facial expression database. *Image and Vision Computing*, 32(10), 692-706.
