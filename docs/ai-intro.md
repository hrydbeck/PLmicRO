---
layout: page
title: AI Primer
permalink: /ai-intro/
---

# A Brief Introduction to AI, LLMs, and Agentic Systems

*Background reading for the PLmicRO Journal Club AI sessions. This primer covers the key concepts you need before diving into papers on AI in medicine and microbiology.*

---

## What is a language model, and why "large"?

A **language model** is a system trained to predict and generate human language. At its core, it learns statistical patterns — which words tend to follow which — from enormous amounts of text.

The "**large**" in Large Language Model (LLM) refers to the number of **parameters**: the internal weights the model adjusts during training. More parameters mean more capacity to encode patterns.

| Scale | Parameters | Examples |
|---|---|---|
| Small language models | ~1M–100M | BERT-base (110M), DistilBERT (66M) |
| Large language models | ~1B–100B+ | GPT-4, Claude, LLaMA 3 (70B) |
| Small/efficient LMs (recent trend) | ~1B–7B | Phi-3 Mini (3.8B), Gemma 2B |

### Why does size matter?

A model like GPT-4 or Claude needs to be large because the goal is **general capability** — it should be able to discuss Mendelian genetics, write Python code, or explain MALDI-TOF spectra. Encoding that breadth of knowledge requires enormous capacity.

Certain **emergent abilities** — complex reasoning, following nuanced instructions, chain-of-thought problem solving — tend to appear only above certain scale thresholds. Researchers don't fully understand why, but it's one of the most striking findings in recent AI research.

### But size isn't everything

Three things matter as much as (or more than) parameter count:

1. **Data quality** — A smaller model trained on curated, high-quality data can outperform a larger one trained on noisy internet text.
2. **Architecture innovations** — Techniques like mixture-of-experts (MoE) activate only a fraction of the parameters per query, making models effectively "big but efficient."
3. **Training compute** — How long and on how much data you train determines what the model actually learns.

---

## The spectrum: from small to large

Not every problem needs a massive model. The right choice depends on the task:

| Goal | Approach | Example |
|---|---|---|
| General-purpose reasoning across any topic | Very large model | GPT-4, Claude |
| Expert in one specific domain | Smaller model fine-tuned on domain data | BioGPT (biomedical text), Med-PaLM (clinical Q&A) |
| Run locally on a phone or laptop | Small distilled model | Phi-3 Mini, Gemma 2B |
| Classify MALDI-TOF spectra | Classical ML or small neural network | Random forest, CNN with ~1M parameters |

**Key insight:** A model that only needs to classify bacterial species from mass spectra can be *millions of times smaller* than a general-purpose LLM — and often more accurate for that specific task.

This is a central question for our journal club: **When is a massive general model the right tool vs. a small, specialized one?**

---

## How LLMs work (simplified)

1. **Training:** The model reads billions of text documents and learns to predict the next word. Through this simple objective, it develops internal representations of language, facts, and reasoning patterns.

2. **Fine-tuning:** The base model is further trained on curated instruction-response pairs to make it helpful and safe (this is where techniques like RLHF — Reinforcement Learning from Human Feedback — come in).

3. **Inference:** When you give the model a prompt, it generates a response one token at a time, each time predicting the most likely next token given everything before it.

### Key terminology

- **Token** — The basic unit an LLM processes, roughly a word or subword. "Microbiology" might become "micro" + "biology."
- **Context window** — The maximum amount of text the model can consider at once (measured in tokens). Larger windows let the model work with longer documents.
- **Hallucination** — When the model generates plausible-sounding but factually incorrect output. A critical limitation for medical and scientific applications.
- **Prompt** — The input text or instructions you give the model.

---

## From language models to AI agents

A standard LLM just generates text — it reads a prompt and writes a response. An **AI agent** goes further:

```
LLM alone:           Question → Answer (single step)
AI agent:             Goal → Plan → Use tools → Observe → Reason → Act → ... → Final answer
```

### What makes an AI agent?

1. **Planning** — Breaking a complex goal into steps
2. **Tool use** — Calling external tools: databases, web search, calculators, code execution
3. **Memory** — Keeping track of what it has learned and done
4. **Reasoning** — Deciding what to do next based on observations

### Multi-agent systems

Some systems use **multiple specialized agents** working together, each with different expertise. An **orchestrator** agent coordinates them.

This is exactly what **RareCollab** does: separate agents handle phenotype analysis and molecular evidence, coordinated by an orchestrator that integrates their findings into a diagnosis.

---

## Why this matters for microbiology and precision medicine

| Application | How AI fits |
|---|---|
| **Variant interpretation** | LLMs reason over genomic + phenotypic evidence (RareCollab) |
| **Literature review** | LLMs summarize and synthesize papers at scale |
| **Clinical decision support** | Domain-specific models assist with diagnosis and treatment |
| **Lab automation** | Agents orchestrate multi-step analytical workflows |
| **MALDI-TOF identification** | Small specialized models classify spectra |
| **Outbreak detection** | ML models identify clusters in genomic surveillance data |

The field is moving from **AI as a classifier** (give it data, get a label) to **AI as a collaborator** (give it a goal, let it reason and use tools). Understanding this shift helps frame every paper we read.

---

## Questions to keep in mind

As you read papers in our journal club, consider:

1. **What type of model is being used?** General LLM, fine-tuned domain model, or classical ML?
2. **Why that size?** Could a smaller/larger model work? What's the tradeoff?
3. **Is it a tool or an agent?** Does it just classify, or does it plan, reason, and use tools?
4. **What are the failure modes?** Hallucination? Overfitting? Data leakage?
5. **Could we use this in our setting?** What would it take to deploy in a clinical microbiology lab?

---

## Further reading

- [Glossary](glossary) — Quick-reference definitions for terms used across our sessions
- Session 1 reading guide — Greener et al. (2022), *A guide to machine learning for biologists*
- [RareCollab reading notes](https://github.com/hrydbeck/PLmicRO/tree/master/notes/ai_ml/rarecollab_notes.md) — Our first agentic AI paper

---

*This primer was developed from discussions within the PLmicRO Journal Club. [Edit on GitHub](https://github.com/hrydbeck/PLmicRO/edit/master/docs/ai-intro.md).*
