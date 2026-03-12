---
layout: page
title: AI Primer
permalink: /ai-intro/
---

Background reading for the PLmicRO Journal Club. Click any section to expand a summary, then follow the link for the full page.

---

<details open>
<summary><h2 style="display:inline">🤖 AI, LLMs & Agentic Systems</h2></summary>

<br>

A primer on the key concepts behind modern AI — from language models to autonomous agents.

### What's covered

- **What is a language model?** Tokens, parameters, context windows, hallucinations
- **The size spectrum** — When you need GPT-4 vs. a small fine-tuned model vs. classical ML
- **How LLMs work** — Training → fine-tuning (RLHF) → inference
- **From LLMs to agents** — Planning, tool use, memory, multi-agent systems
- **Why it matters for microbiology** — Variant interpretation, lab automation, clinical decision support

### Key takeaway

> The field is moving from **AI as a classifier** (give it data, get a label) to **AI as a collaborator** (give it a goal, let it reason and use tools).

| Scale | Parameters | Examples |
|---|---|---|
| Small language models | ~1M–100M | BERT-base (110M), DistilBERT (66M) |
| Large language models | ~1B–100B+ | GPT-4, Claude, LLaMA 3 (70B) |
| Efficient LMs (recent) | ~1B–7B | Phi-3 Mini (3.8B), Gemma 2B |

**→ [Read the full AI Primer]({{ '/ai-intro/llms/' | relative_url }})**

</details>

---

<details>
<summary><h2 style="display:inline">📊 Detection & Classification Performance</h2></summary>

<br>

How to evaluate whether a classifier or detection algorithm actually works — essential for benchmarking variant callers, ML models, and diagnostic tools.

### What's covered

- **The four outcomes** — TP, TN, FP, FN and the confusion matrix
- **Precision** — Among predicted positives, how many are real?
- **Recall / Sensitivity** — Among actual positives, how many did we find?
- **Specificity** — Among actual negatives, how many were correctly ignored?
- **The precision–recall tradeoff** — You usually can't maximize both
- **F1 score** — A single balanced metric
- **ROC curve & AUC** — Threshold-independent classifier evaluation
- **Variant calling example** — GQ thresholds and RTG tools

### Quick reference

| Metric | Formula | Prioritize when... |
|---|---|---|
| **Precision** | TP / (TP + FP) | False positives are costly |
| **Recall** | TP / (TP + FN) | False negatives are dangerous |
| **Specificity** | TN / (FP + TN) | Confirming absence matters |
| **F1** | 2·(P·R)/(P+R) | Need one balanced number |
| **AUC** | Area under ROC | Comparing classifiers overall |

**→ [Read the full Detection Performance guide]({{ '/primers/detection-performance/' | relative_url }})**

</details>

---

<details>
<summary><h2 style="display:inline">📚 More Topics (Coming Soon)</h2></summary>

<br>

Future primer sections may include:

- **Genomic epidemiology concepts** — SNP distances, phylogenetics, outbreak detection
- **Metagenomics fundamentals** — Taxonomic profiling, assembly, binning
- **Data handling & reproducibility** — FAIR principles, version control for data
- **Statistical foundations** — Bayesian vs. frequentist, multiple testing, p-values

*Suggest a topic on the [Suggest a Paper]({{ '/suggest/' | relative_url }}) page.*

</details>

---

*[Edit this page on GitHub](https://github.com/hrydbeck/PLmicRO/edit/master/docs/ai-intro.md)*
