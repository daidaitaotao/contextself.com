---
title: "Decomposing the Observable Self"
date: 2025-01-18
description: "A framework for understanding what signals from images and video can tell us about human identity—and what they cannot."
---

How much of a person can be understood from what is visible? This question has occupied me as I work on systems that extract signals from images and video. The technology is advancing rapidly, but I find myself more interested in its limits than its capabilities.

## The Inner-Outer Distinction

William James (1890) distinguished between the "I" (the knowing self) and the "Me" (the known self—the self as object). The "Me" includes the material self (body, possessions), the social self (recognition from others), and the spiritual self (inner thoughts, dispositions). Only portions of the "Me" are externally observable.

Goffman (1959) extended this with dramaturgy: we perform versions of ourselves for different audiences. The "front stage" self—what others see—is curated, contextual, and strategic. The "back stage" self remains hidden.

**What this means to me**: Any system that observes humans captures only performances, not essences. When I look at a photograph of someone, I'm seeing a moment they chose to present (or had presented for them). This isn't a limitation to overcome—it's a fundamental truth about what observation can access. I think we forget this too easily when building technology.

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

**What this means**: The 91-95% accuracy numbers are misleading for real-world use. They come from benchmark conditions that don't reflect how people actually appear in photos and videos—partially obscured, badly lit, at odd angles. I've learned to mentally discount benchmark performance by 20-30% when thinking about practical applications.

### Facial Landmark Detection

68-point landmark models achieve:

| Model | Dataset | NME (Normalized Mean Error) |
|-------|---------|----------------------------|
| HRNet (Sun et al., 2019) | 300W | 2.87% |
| AWing (Wang et al., 2019) | WFLW | 4.36% |
| Human inter-rater | 300W | ~3.0% |

**What this means**: Landmark detection is genuinely good—approaching human-level agreement. This is the kind of geometric signal I trust. It's measuring shape, not meaning.

### Body Pose Estimation

Skeleton estimation accuracy (PCK @ 0.5 threshold—correct if within 50% of head size):

| Model | Dataset | PCK@0.5 |
|-------|---------|---------|
| HRNet (Sun et al., 2019) | COCO | 76.3% |
| OpenPose (Cao et al., 2019) | COCO | 65.3% |
| AlphaPose (Fang et al., 2017) | COCO | 72.3% |

Multi-person scenarios show 10-15% degradation due to occlusion and association errors.

**What this means**: Pose estimation is useful but imperfect. 76% means roughly 1 in 4 joint positions is noticeably wrong. For measuring gross body position—standing, sitting, facing toward/away—it's adequate. For fine-grained gesture analysis, I'd be cautious.

### The Problem with Emotion Recognition

This is where I become skeptical of the entire enterprise.

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

**What this means to me**: This data changed how I think about the field. If humans only agree 48% of the time on what "fear" looks like across cultures, then any algorithm trained on Western-labeled data is encoding one culture's interpretation as universal truth. The 71% accuracy of a commercial API isn't measuring "emotion detection"—it's measuring agreement with Western labelers' interpretations of posed expressions.

I find this troubling because these systems are being deployed as if they measure something real. But they're measuring agreement with a training set, not ground truth about human experience.

### Facial Action Units: A More Honest Alternative

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

Data from BP4D-Spontaneous dataset (Zhang et al., 2014).

**What this means**: AUs are more honest because they describe what's actually observable—muscle movements—without claiming to know what they mean. AU12 (lip corner puller) is reliably detectable at 0.86 F1. Whether that "smile" indicates joy, politeness, nervousness, or a photographer's instruction is a separate question entirely.

This is the approach I want to take with taocore-human: describe the signal, not the interpretation.

## Demographic Attributes: Where Accuracy Meets Ethics

### Gender Classification Bias

Buolamwini & Gebru (2018) tested three commercial systems on the Pilot Parliaments Benchmark:

| Demographic Group | System A | System B | System C |
|------------------|----------|----------|----------|
| Lighter-skinned males | 0.8% error | 0.0% error | 0.0% error |
| Lighter-skinned females | 6.0% error | 1.7% error | 7.1% error |
| Darker-skinned males | 12.0% error | 0.7% error | 6.0% error |
| Darker-skinned females | 34.7% error | 21.3% error | 34.5% error |

**What this means**: Error rates for darker-skinned females were up to 43× higher than for lighter-skinned males. This isn't a bug to be fixed with more data—it reflects whose faces were considered worth including in training sets. The bias is structural.

**My position**: I don't think we should build systems that classify gender from appearance. It conflates sex, gender identity, and gender expression. It fails for people who don't fit binary categories. And even when it "works," it reinforces the idea that gender is something readable from the surface.

### Age Estimation

State-of-the-art mean absolute error (MAE) in years:

| Model | MORPH II | FG-NET | UTKFace |
|-------|----------|--------|---------|
| DEX (Rothe et al., 2018) | 2.68 | 4.63 | - |
| SSR-Net (Yang et al., 2018) | 3.16 | 4.48 | 5.21 |

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

**What this means**: Age estimation is less politically charged than gender, but still unreliable. ±8 years for someone over 60 means the system might guess 55 or 70 for someone who is 63. If taocore-human ever reports age, it should be as a wide range with explicit uncertainty—"apparent age: 55-70"—not a point estimate.

### Race Classification: Why I Won't Build It

Accuracy seems high in benchmarks:

| Study | Dataset | Accuracy |
|-------|---------|----------|
| Fu et al. (2014) | MORPH II (3 classes) | 99.1% |
| Guo & Mu (2014) | PCSO (2 classes) | 98.3% |

But these benchmarks are fundamentally flawed:
1. **Limited categories**: Most use 2-4 racial categories, erasing mixed-race and many ethnic groups
2. **Labeling inconsistency**: Inter-rater agreement on race labels is only 85-90% (Albiero et al., 2020)
3. **Downstream harm**: These systems have led to wrongful arrests (Hill, 2020)

**My position**: Race is a social construct, not a biological category that can be read from faces. The high "accuracy" of these systems means they're good at reproducing the racial categories their training data encoded—not that race is something objectively measurable.

I will not build race classification into taocore-human. Some capabilities shouldn't exist.

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

**What this means**: The gap between benchmark and reality is enormous. A system that's 95% accurate in the lab might be 50% accurate on your actual photos. This is why taocore-human needs to report confidence and refuse to interpret when conditions are poor. Silence is more honest than false confidence.

## The Signal-to-Meaning Gap

I think of this as a hierarchy where reliability degrades at each level:

```
Level 1: Pixels (raw data)
   ↓ [~5% information loss - compression, noise]
Level 2: Geometric features (faces, poses, positions)
   ↓ [10-20% error - detection/estimation]
Level 3: Behavioral signals (AUs, pose configurations)
   ↓ [30-50% error - context-dependent mapping]
Level 4: Psychological inference (emotions, intentions)
   ↓ [50-70% error - weak construct validity]
Level 5: Identity claims (who someone "is")
   ↓ [undefined - philosophical category error]
```

**My principle for taocore-human**: Operate at Levels 2-3. Report geometric features and behavioral signals with confidence intervals. Do not attempt Levels 4-5.

The temptation is always to climb higher—to say something more meaningful. But meaning without validity is noise dressed up as signal.

## What Else Helps Us Understand Ourselves?

### Voice and Speech

Paralinguistic features show moderate reliability:

| Feature | Task | Accuracy/Correlation |
|---------|------|---------------------|
| Pitch variation | Arousal detection | r = 0.45-0.65 |
| Speech rate | Stress detection | r = 0.35-0.50 |
| Voice quality | Depression screening | AUC = 0.70-0.80 |

Data from Schuller & Batliner (2013).

**What this means**: Voice carries real signal—more than I initially expected. The correlations with arousal and stress are moderate but meaningful. This might be a future direction for taocore-human, though audio raises its own privacy concerns.

### Physiological Signals

| Signal | What It Measures | Reliability (r with self-report) |
|--------|-----------------|--------------------------------|
| Heart rate variability | Arousal/stress | 0.40-0.60 |
| Skin conductance | Emotional activation | 0.50-0.70 |
| Pupil dilation | Cognitive load, arousal | 0.35-0.55 |

Data from Kreibig (2010) meta-analysis.

**What this means**: Physiological signals correlate with self-reported states better than facial expressions do. This makes sense—they're measuring the body's actual response, not a culturally mediated display. But they require sensors, which limits practical application.

## Framework for Ethical Signal Extraction

Based on the data above, here's how I think about what taocore-human should and shouldn't do:

| Signal Type | Reliability | Should Extract? | How to Report |
|------------|-------------|-----------------|---------------|
| Face presence/location | High (>90%) | Yes | Bounding box + confidence |
| Facial landmarks | Moderate-High (85-95%) | Yes | Points + NME estimate |
| Body pose | Moderate (65-80%) | Yes | Skeleton + PCK confidence |
| Facial AUs | Variable (38-92%) | Selective | Only high-reliability AUs |
| Emotion labels | Low (<60%) | **No** | - |
| Gender | Biased (65-99%) | **No** | - |
| Race | Invalid construct | **No** | - |
| Age | Moderate (±5-8 years) | With uncertainty | Range, not point estimate |

## Conclusion: What I've Learned

Working through this literature has clarified my thinking:

1. **Geometric signals are trustworthy.** Where faces are, how bodies are positioned—these are measurable with reasonable accuracy.

2. **Behavioral signals require humility.** AUs and pose configurations can be detected, but what they mean depends on context we often don't have.

3. **Psychological inferences are overreach.** The emotion recognition industry is built on shaky foundations. I don't want to contribute to it.

4. **Identity categorizations are harmful.** Race and gender classification encode social constructs as biological facts. They should not be built.

The goal of taocore-human is not to understand people. It's to describe observable patterns while being honest about what remains unknown. The data tells us clearly: most of what matters about a person is not visible on the surface.

---

## References

Albiero, V., et al. (2020). Analysis of gender inequality in face recognition accuracy. *IEEE/CVF WACV Workshops*, 81-89.

Barrett, L. F., et al. (2019). Emotional expressions reconsidered. *Psychological Science in the Public Interest*, 20(1), 1-68.

Buolamwini, J., & Gebru, T. (2018). Gender shades. *FAT*, 77-91.

Cao, Z., et al. (2019). OpenPose. *IEEE TPAMI*, 43(1), 172-186.

Deng, J., et al. (2020). RetinaFace. *IEEE/CVF CVPR*, 5203-5212.

Ekman, P., & Friesen, W. V. (1978). *Facial Action Coding System*. Consulting Psychologists Press.

Goffman, E. (1959). *The Presentation of Self in Everyday Life*. Anchor Books.

Hill, K. (2020). Wrongfully accused by an algorithm. *The New York Times*, June 24.

James, W. (1890). *The Principles of Psychology*. Henry Holt.

Kreibig, S. D. (2010). Autonomic nervous system activity in emotion. *Biological Psychology*, 84(3), 394-421.

Ricanek, K., & Tesafaye, T. (2006). MORPH. *FG*, 341-345.

Rothe, R., et al. (2018). Deep expectation of real and apparent age. *IJCV*, 126(2-4), 144-157.

Schuller, B., & Batliner, A. (2013). *Computational Paralinguistics*. Wiley.

Sun, K., et al. (2019). Deep high-resolution representation learning. *IEEE/CVF CVPR*, 5693-5703.

Zhang, K., et al. (2016). MTCNN. *IEEE SPL*, 23(10), 1499-1503.

Zhang, X., et al. (2014). BP4D-Spontaneous. *Image and Vision Computing*, 32(10), 692-706.
