---
layout: page
title: "Session 1 — ML Guide for Biologists"
permalink: /notes/session1/
---

# PLmicRO Journal Club — Session 1

📅 **Date:** TBD
📄 **Paper:**
- Greener JG, Kandathil SM, Moffat L, Jones DT (2022) — *A guide to machine learning for biologists*, Nature Reviews Molecular Cell Biology
  DOI: [10.1038/s41580-021-00407-0](https://doi.org/10.1038/s41580-021-00407-0)

👥 **Attendees:** (add your name)
-

---

## Pre-reading Questions

*What should we look for while reading?*

- How do the authors categorize the landscape of ML methods — what's the "taxonomy"?
- Which evaluation metrics matter most, and when is accuracy misleading?
- What is overfitting, and how do you detect and prevent it?
- Which ML methods map to which data types (images, sequences, tabular)?
- What practical best practices can we apply in our own work?
- In unsupervised learning, the paper says a cost function is still minimized even without ground truth — how is that possible? *(see [Glossary: Cost function](https://hrydbeck.github.io/PLmicRO/glossary/))*

---

## Key Concepts

*Core ideas, methods, and terminology from the paper*

### The ML taxonomy
- Supervised vs. unsupervised vs. self-supervised learning
- Classical ML (random forest, SVM, logistic regression) vs. deep learning (CNN, RNN, transformer)
- See [Glossary](https://hrydbeck.github.io/PLmicRO/glossary/) for definitions

### Overfitting vs. generalization
- A model that *memorizes* training data vs. one that *generalizes* to new data
- Key signs of overfitting: high training accuracy, low test accuracy
- Prevention: cross-validation, regularization, early stopping, more data

### Evaluation metrics
- **Accuracy** — misleading with imbalanced classes (e.g. 99% of samples are negative)
- **Precision / Recall / F1** — better for rare events (e.g. detecting resistant strains)
- **AUC-ROC** — threshold-independent measure of classifier quality
- **Confusion matrix** — the foundation for understanding all other metrics

### Where do LLMs fit?
- This paper predates the LLM revolution (ChatGPT launched Nov 2022, paper submitted earlier) — **LLMs are not explicitly covered**
- But the building blocks are all here:

| Paper's concept | How it connects to LLMs |
|---|---|
| Neural networks (deep learning section) | LLMs are neural networks — just very large ones |
| RNNs (recurrent neural networks) | The predecessor for sequence/language tasks — LLMs replaced these |
| Transformers (brief mention) | The architecture LLMs are built on (GPT = "Generative Pre-trained **Transformer**") |
| Self-supervised learning | Exactly how LLMs are trained: predict the next word from unlabeled text |
| Transfer learning | How LLMs work in practice: pre-train on general text, then fine-tune or prompt for specific tasks |

- The evolution: **RNN → Transformer → BERT (2018) → GPT-3 (2020) → ChatGPT (2022) → GPT-4 (2023) → agentic systems (2024–)**
- See [AI Primer](https://hrydbeck.github.io/PLmicRO/ai-intro/) for what happened after this paper was published

### Data handling best practices
- Train / validation / test split — why you need all three
- Cross-validation — robust performance estimation with limited data
- Feature scaling and preprocessing
- The danger of data leakage

---

## Methods Summary

*How the paper is structured*

- **Not a research paper** — this is a **review/tutorial** aimed at biologists entering ML
- Covers: supervised learning, unsupervised learning, deep learning, evaluation, best practices
- Uses biological examples throughout (protein structure, gene expression, microscopy)

---

## Main Results / Key Takeaways

*What are the most important messages?*

-

---

## Discussion Points

*Questions, critiques, connections to our work*

### From the reading guide
1. What is the difference between a model that *memorizes* vs. one that *generalizes*?
2. When would you pick a simple model (e.g. random forest) over a deep neural network?
3. What evaluation metric would you use for a clinical microbiology classification task with rare positive cases (e.g. detecting a resistant strain)? Why not just accuracy?
4. How does the paper's advice on data splitting apply to biological datasets that are often small?
5. Which ML method category seems most relevant to your own work, and why?

### Where are the LLMs?
6. The paper covers the foundations (neural networks, transformers, self-supervised learning, transfer learning) but was published before the LLM explosion. How does what we now know about LLMs change the paper's recommendations?
7. The paper advises matching method to data type. Where do LLMs fit — are they a new category, or a scaled-up version of existing methods?
8. What does the paper miss that the [AI Primer](https://hrydbeck.github.io/PLmicRO/ai-intro/) covers? (prompt engineering, RLHF, agentic AI, generalist vs. specialist tradeoff)

### Additional questions
- 💬
-

---

## Strengths & Limitations

| ✅ Strengths | ⚠️ Limitations |
|---|---|
| Broad accessible overview for biologists | Published pre-LLM era — misses the biggest shift in AI |
| Good coverage of practical pitfalls | Limited coverage of transformers, which now dominate |
| Strong biological examples throughout | Doesn't address prompt engineering, RLHF, or agentic AI |
| Provides foundational vocabulary for all later sessions | Some advice may need updating (e.g. "when to use deep learning") |

---

## Relevance to Our Work

*How does this connect to precision medicine, clinical microbiology, or our bioinformatics practice?*

- Provides the foundational vocabulary for all subsequent sessions
- Evaluation metrics are directly applicable to benchmarking clinical micro models
- The "which method for which data type" framework maps to our diverse data: MALDI-TOF spectra (→ CNN), genomic sequences (→ RNN/transformer), clinical variables (→ random forest)

### Connections to later sessions
- **Session 2** (Topçuoğlu et al.) builds directly on evaluation/benchmarking concepts
- **Session 4** (MALDI-TOF + ML) is a concrete clinical application of CNN and random forest
- **Session 5** (Deep Learning in Genomics) goes deeper on neural network architectures

---

## Action Items

- [ ]

---

## Resources & Links

- [Paper (DOI)](https://doi.org/10.1038/s41580-021-00407-0)
- [Glossary](https://hrydbeck.github.io/PLmicRO/glossary/)
- [AI Primer](https://hrydbeck.github.io/PLmicRO/ai-intro/)
- [Session 1 reading guide](https://github.com/hrydbeck/PLmicRO/blob/master/session1_intro_ml/reading_guide.md)
- [Session 1 glossary](https://github.com/hrydbeck/PLmicRO/blob/master/session1_intro_ml/glossary.md)

---

*Notes taken collaboratively in [HackMD](https://hackmd.io) — pushed to [PLmicRO GitHub Pages](https://hrydbeck.github.io/PLmicRO/notes/)*
