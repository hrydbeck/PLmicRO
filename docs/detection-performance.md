---
layout: page
title: "Detection & Classification Performance"
permalink: /primers/detection-performance/
---

A practical guide to evaluating how well a classifier or detection algorithm performs — whether it's calling genomic variants, identifying resistant strains, or classifying MALDI-TOF spectra.

---

## Why Not Just Use Accuracy?

The most intuitive performance metric is **accuracy** — the fraction of all predictions that are correct:

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

It sounds reasonable: out of everything the model classified, how many did it get right? The problem is that accuracy **hides critical failures** when classes are imbalanced — which they almost always are in clinical and genomic applications.

### A concrete example

Imagine a variant caller processing 1,000,000 genomic positions, where only 1,000 are true variants (0.1%):

| Classifier | Strategy | TP | FP | FN | TN | Accuracy |
|---|---|---|---|---|---|---|
| **Model A** | Always says "wildtype" | 0 | 0 | 1,000 | 999,000 | **99.9%** |
| **Model B** | Actually detects variants | 950 | 200 | 50 | 998,800 | **99.97%** |

Model A achieves 99.9% accuracy by doing **absolutely nothing useful** — it misses every single variant. A clinician relying on accuracy alone might think this tool works brilliantly.

This is why we need metrics that separately measure **how well we find positives** (recall) and **how trustworthy our positive calls are** (precision). The rest of this page covers those metrics.

---

## The Setup: Binary Classification

Many real-life tasks boil down to sorting things into two groups:

- Is this email **spam** or **not spam**?
- Does this patient have **cancer** or **not**?
- Is this genomic position a **variant** or **wildtype**?

We want our algorithm to call mutations as mutations and wildtype as wildtype. To measure how well it does, we need a **facit** (ground truth) — cases where the true answer is already known.

---

## The Four Outcomes

For each prediction, there are four possible results:

| | **Predicted Positive** | **Predicted Negative** |
|---|---|---|
| **Actually Positive** | ✅ True Positive (TP) | ❌ False Negative (FN) |
| **Actually Negative** | ❌ False Positive (FP) | ✅ True Negative (TN) |

And the fundamental relationships:

```
N Actual negatives  = TN + FP
N Actual positives  = TP + FN
N Predicted negatives = TN + FN
N Predicted positives = TP + FP
```

<img src="{{ '/assets/img/detection/classification_performance.png' | relative_url }}" alt="Classification performance overview" width="500">

---

## Key Metrics

### Precision

<img src="{{ '/assets/img/detection/precision.png' | relative_url }}" alt="Precision" width="80" style="float:right; margin-left:1em;">

**Question:** Among the called mutations, how many are true?

$$\text{Precision} = \frac{TP}{TP + FP}$$

- A high number means the algorithm calls far more TPs than FPs
- **Use when** false positives are unacceptable — you want to be confident that your predicted mutations are real
- *Example: You don't want to report a resistance mutation to a clinician if it's likely to be noise*

---

### Sensitivity / Recall

<img src="{{ '/assets/img/detection/recall_sensitivity.png' | relative_url }}" alt="Recall / Sensitivity" width="80" style="float:right; margin-left:1em;">

**Question:** Among the true mutations, how many were found?

$$\text{Recall} = \text{Sensitivity} = \frac{TP}{TP + FN}$$

- A high number means most existing positives ended up as TP
- **Use when** false negatives are unacceptable — missing a real mutation is dangerous
- *Example: A screening test for MRSA where you must catch every case*

---

### Specificity

<img src="{{ '/assets/img/detection/specificity.png' | relative_url }}" alt="Specificity" width="80" style="float:right; margin-left:1em;">

**Question:** Among the true negatives, how many were correctly ignored?

$$\text{Specificity} = \frac{TN}{FP + TN}$$

- A high number means very few negatives are falsely called as positives
- **Use when** you don't want to frighten people with misleading information
- *Example: Confirming that a patient does NOT carry a pathogenic variant*

---

### The Precision–Recall Tradeoff

<img src="{{ '/assets/img/detection/precision_recall.png' | relative_url }}" alt="Precision vs Recall" width="300">

There is almost always a tension between precision and recall:

- **Increase sensitivity** (catch more true positives) → you typically also catch more false positives → **precision drops**
- **Increase precision** (be stricter about what you call) → you miss some true positives → **recall drops**

The right balance depends on the clinical context: Is it worse to miss a variant (→ prioritize recall) or to report a false one (→ prioritize precision)?

---

### F1 Score

The **harmonic mean** of precision and recall — a single number that balances both:

$$F_1 = 2 \cdot \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

Useful when you need one metric to compare models, especially with imbalanced classes.

---

## The Confusion Matrix

All the metrics above come from the same 2×2 table:

| | **Predicted +** | **Predicted −** | |
|---|---|---|---|
| **Actual +** | TP | FN | ← Recall = TP/(TP+FN) |
| **Actual −** | FP | TN | ← Specificity = TN/(FP+TN) |
| | ↑ Precision = TP/(TP+FP) | | |

---

## ROC Curve

**ROC** stands for Receiver Operating Characteristic — not the most intuitive name. A better description: **TP-rate vs FP-rate plot**.

<img src="{{ '/assets/img/detection/fp_rate.png' | relative_url }}" alt="FP rate" width="80" style="float:right; margin-left:1em;">

- **Y-axis:** True Positive Rate (= Recall/Sensitivity) = TP / (TP + FN)
- **X-axis:** False Positive Rate (= 1 − Specificity) = FP / (FP + TN)

### How it works

Each classifier produces a **confidence score** (e.g. genotype quality, GQ). By sweeping a threshold from strict to lenient:

1. **Threshold = 1.0** (very strict): almost nothing is called → TPR ≈ 0, FPR ≈ 0 (bottom-left corner)
2. **Lower the threshold**: more calls are made → TPR increases; if the model is good, FPR stays low
3. **Threshold = 0.0** (accept everything): TPR = 1, FPR = 1 (top-right corner)

Connect the dots and you get the ROC curve.

### Reading the curve

- **Perfect classifier:** hugs the top-left corner (high TPR, low FPR)
- **Random guessing:** diagonal line from bottom-left to top-right
- **Worse than random:** below the diagonal

---

## AUC (Area Under the Curve)

The **AUC-ROC** collapses the entire ROC curve into a single number:

| AUC | Interpretation |
|---|---|
| 1.0 | Perfect classifier |
| 0.9–1.0 | Excellent |
| 0.8–0.9 | Good |
| 0.7–0.8 | Fair |
| 0.5 | Random guessing |
| < 0.5 | Worse than random |

---

## Variant Calling Example: GQ Thresholds

In genomic variant calling, each variant comes with a **GQ (Genotype Quality)** value — an estimate of how confident we are that the genotype is correct.

- Low GQ → higher risk of being a false positive
- Including low-GQ variants might add a few TPs but will likely also add many FPs

**Practical approach:** Calculate confusion matrices at various GQ thresholds, then pick the threshold that gives the best balance of TP and FP for your use case.

### RTG Tools ROC Plot

Tools like `rtg vcfeval` and `rtg rocplot` can evaluate variant calling performance against a ground truth. Their plot uses **absolute counts** (TP vs FP) rather than rates, because:

- Truth sets (VCF) don't always define the full set of negatives
- It's hard to count "possible negative calls" when variants span multiple bases
- Insertions can occupy zero reference bases

The resulting plot is not a true ROC curve but is still informative for choosing a GQ threshold.

---

## Quick Reference

| Metric | Formula | When to prioritize |
|---|---|---|
| **Precision** | TP / (TP + FP) | False positives are costly (e.g. reporting fake mutations) |
| **Recall / Sensitivity** | TP / (TP + FN) | False negatives are dangerous (e.g. missing MRSA) |
| **Specificity** | TN / (FP + TN) | Confirming absence is important |
| **F1** | 2·(Prec·Rec)/(Prec+Rec) | Need a single balanced metric |
| **AUC-ROC** | Area under ROC curve | Comparing classifiers across all thresholds |

---

*Content adapted from PLmicRO internal notes on detection performance evaluation. [Edit on GitHub](https://github.com/hrydbeck/PLmicRO/edit/master/docs/detection-performance.md).*
