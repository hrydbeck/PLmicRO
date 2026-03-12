---
layout: page
title: "AI, LLMs & Agentic Systems"
permalink: /ai-intro/llms/
---

*Background reading for the PLmicRO Journal Club AI sessions. This primer covers the key concepts you need before diving into papers on AI in medicine and microbiology.*

**← [Back to Primer overview]({{ '/ai-intro/' | relative_url }})**

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

Certain **emergent abilities** — complex reasoning, following nuanced instructions, chain-of-thought problem solving — tend to appear only above certain scale thresholds.

### But size isn't everything

Three things matter as much as (or more than) parameter count:

1. **Data quality** — A smaller model trained on curated, high-quality data can outperform a larger one trained on noisy internet text.
2. **Architecture innovations** — Techniques like mixture-of-experts (MoE) activate only a fraction of the parameters per query, making models effectively "big but efficient."
3. **Training compute** — How long and on how much data you train determines what the model actually learns.

### Mixture-of-Experts (MoE)

One of the most important architecture innovations is **Mixture-of-Experts (MoE)**. The idea is simple but powerful:

Instead of one monolithic neural network where every parameter is used for every input, an MoE model contains many **specialist sub-networks ("experts")** and a **router** that decides which experts to activate for each input.

```
Input token
    ↓
[Router] — "Which experts should handle this?"
    ↓
Activates 2 of 8 experts (for example)
    ↓
Output (combined from selected experts)
```

**Why it matters:**

- A model can have **hundreds of billions of total parameters** but only activate a small fraction per query — making it fast and efficient
- Different experts can specialize in different types of knowledge (one might be good at code, another at biology)
- It's how models can be "big" in knowledge capacity but "small" in compute cost per query

**Real examples:**

| Model | Total parameters | Active per query | Architecture |
|---|---|---|---|
| GPT-4 (rumored) | ~1.8 trillion | ~280B | 16 experts, activate 2 |
| Mixtral 8x7B | 46.7B | 12.9B | 8 experts, activate 2 |
| DeepSeek-V2 | 236B | 21B | 160 experts, activate 6 |

This is why the parameter count alone doesn't tell you how fast or expensive a model is to run — an MoE model with 200B total parameters can be faster than a dense model with 70B.

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

## The Transformer Architecture

Every modern LLM is built on the **transformer** — an architecture introduced in 2017 that revolutionized AI. Understanding it helps explain why LLMs work the way they do.

### The problem transformers solved

Before transformers, language models used **Recurrent Neural Networks (RNNs)** that processed text one word at a time, left to right. This had two big limitations:

1. **Slow** — you can't parallelize; each word depends on the previous one
2. **Forgetful** — by the time the model reaches word 500, it has largely forgotten word 1

### The key idea: Attention

The transformer's breakthrough is the **attention mechanism** — instead of reading sequentially, it looks at **all words simultaneously** and learns which ones are relevant to each other.

When processing the sentence *"The antibiotic resistance gene was found on a plasmid that transferred between species"*, the model can directly connect "gene" to "transferred" even though they're far apart — without having to remember through all the words in between.

### How it works (simplified)

```
Input text
    ↓
[Tokenize] — split into tokens
    ↓
[Embedding] — convert each token to a numeric vector
    ↓
[Self-attention × N layers] — each token "looks at" all others,
    learns which are relevant, updates its representation
    ↓
[Output] — predict next token (or classification, etc.)
```

The "self-attention" step is where the magic happens. For each token, the model computes:

- **Query**: "What am I looking for?"
- **Key**: "What do I contain?"
- **Value**: "What information do I provide?"

Every token's query is matched against every other token's key to produce attention weights — a score for how much each token should influence the current one. This is computed in parallel for all tokens, making transformers much faster than RNNs.

### Why this matters

| Property | RNN (old) | Transformer (new) |
|---|---|---|
| Processing | Sequential (slow) | Parallel (fast) |
| Long-range connections | Weak (forgets) | Strong (attention) |
| Training speed | Slow | Fast (GPU-friendly) |
| Scalability | Limited | Scales to billions of parameters |

This scalability is why transformers enabled the jump from models with millions of parameters to models with hundreds of billions — and why the LLM revolution happened.

### The family tree

The transformer spawned two major families:

- **Encoder models** (e.g. BERT) — read the whole input at once, good for **understanding** tasks (classification, named entity recognition)
- **Decoder models** (e.g. GPT) — generate text one token at a time, good for **generation** tasks (chatbots, text completion, code generation)
- **Encoder-decoder models** (e.g. T5) — combine both, used for translation and summarization

Most modern LLMs (GPT-4, Claude, LLaMA) are **decoder-only** transformers — optimized for generating text.

### Timeline

| Year | Milestone |
|---|---|
| 2017 | Transformer introduced ("Attention Is All You Need") |
| 2018 | BERT (encoder) — first big pre-trained language model |
| 2018 | GPT-1 (decoder) — OpenAI's first generative model |
| 2020 | GPT-3 — 175B parameters, few-shot learning emerges |
| 2022 | ChatGPT — transformers go mainstream |
| 2023+ | GPT-4, Claude, LLaMA, Gemini — rapid scaling and specialization |

---

## From language models to AI agents

A standard LLM just generates text — it reads a prompt and writes a response. An **AI agent** goes further:

```
LLM alone:    Question → Answer (single step)
AI agent:     Goal → Plan → Use tools → Observe → Reason → Act → ... → Final answer
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

- [Glossary]({{ '/glossary/' | relative_url }}) — Quick-reference definitions for terms used across our sessions
- Session 1 reading guide — Greener et al. (2022), *A guide to machine learning for biologists*
- [Detection & Classification Performance]({{ '/primers/detection-performance/' | relative_url }}) — Precision, recall, ROC curves

---

**← [Back to Primer overview]({{ '/ai-intro/' | relative_url }})**

*This primer was developed from discussions within the PLmicRO Journal Club. [Edit on GitHub](https://github.com/hrydbeck/PLmicRO/edit/master/docs/ai-intro-llms.md).*
