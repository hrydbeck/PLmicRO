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

## Emergent Abilities: When Scale Creates Surprises

One of the most striking — and debated — findings in modern AI is that certain capabilities appear to **emerge** only when models reach a sufficient scale. They are absent in smaller models and then seem to switch on, sometimes abruptly, as models grow.

### When did researchers notice?

The story unfolded gradually, then all at once:

**2020 — GPT-3 and "few-shot learning."** When OpenAI scaled from GPT-2 (1.5B parameters) to GPT-3 (175B), they discovered something unexpected: GPT-3 could perform tasks it was never explicitly trained for, simply by being shown a few examples in the prompt. Translation, arithmetic, code generation — none of these were trained objectives, yet the model could do them. Smaller models in the same family could not. This was documented in Brown et al. (2020), *"Language Models are Few-Shot Learners"* ([arXiv:2005.14165](https://arxiv.org/abs/2005.14165)).

**2022 — The landmark survey.** Jason Wei and colleagues at Google systematically catalogued this phenomenon across 200+ tasks and multiple model families. Their paper, *"Emergent Abilities of Large Language Models"* ([arXiv:2206.07682](https://arxiv.org/abs/2206.07682)), showed a consistent pattern: on many benchmarks, performance stayed near random as models scaled up — until a critical size threshold, after which performance jumped sharply. They called these **emergent abilities** because they were "not present in smaller models but are present in larger models."

Key examples from the paper:

| Ability | Appears around | Absent below |
|---|---|---|
| Multi-step arithmetic | ~100B parameters | Random at 10B |
| Chain-of-thought reasoning | ~60–100B parameters | Fails at smaller scales |
| Word unscrambling | ~60B parameters | Near zero below |
| Following complex instructions | ~100B+ parameters | Unreliable below |

**2022–2023 — The ChatGPT moment.** When ChatGPT (based on GPT-3.5) launched in November 2022, the general public experienced emergent abilities firsthand — the model could hold coherent conversations, write essays, explain code, and reason through problems in ways that felt qualitatively different from any prior chatbot.

### What causes emergence?

This is still debated. The leading hypotheses:

1. **Sufficient internal representations** — Below a certain scale, the model simply doesn't have enough capacity to build the internal patterns needed for complex reasoning. Above it, those patterns form and compose in powerful ways.

2. **Composition of simpler skills** — Individual sub-skills (grammar, facts, logic) may each improve gradually, but the *combination* of multiple skills into a complex behavior only works when all sub-skills are above some minimum quality. One weak link breaks the chain.

3. **Phase transitions in learning** — Analogous to physical phase transitions (water suddenly freezing at 0°C), the model's internal organization may undergo qualitative shifts at certain scales.

### The counter-argument: Is emergence real?

Not everyone is convinced. In a provocative 2023 paper, Schaeffer et al. (*"Are Emergent Abilities of Large Language Models a Mirage?"*, [arXiv:2304.15004](https://arxiv.org/abs/2304.15004)) argued that apparent emergence may be an artifact of how we *measure* performance. When using metrics with sharp thresholds (like exact-match accuracy — either the answer is perfectly right or it scores zero), a gradually improving model's scores can look like a sudden jump. With smoother metrics, improvement appears more gradual.

This didn't settle the debate — some abilities still look genuinely emergent even with smooth metrics — but it added important nuance: **how you measure matters as much as what you measure** (a lesson that connects directly to our [detection performance]({{ '/primers/detection-performance/' | relative_url }}) primer).

### Why this matters for us

The emergence debate has practical consequences:

- **For clinical applications:** If your task only requires narrow classification (e.g. species ID from MALDI-TOF), a small specialized model will work. If you need flexible reasoning over complex evidence (e.g. RareCollab's variant interpretation), you may need a model large enough for emergent reasoning abilities.
- **For benchmarking:** When evaluating AI tools, the choice of metric can make a model look like it suddenly got better or like it gradually improved — echoing the Schaeffer critique.
- **For the future:** If emergence is real, we should expect further capability jumps as models scale. If it's partly a measurement artifact, we should invest more in better evaluation methods.

### Key references

| Year | Paper | Key contribution |
|---|---|---|
| 2020 | Brown et al. — *Language Models are Few-Shot Learners* ([arXiv:2005.14165](https://arxiv.org/abs/2005.14165)) | Discovered few-shot learning in GPT-3; first major evidence of emergent abilities |
| 2022 | Wei et al. — *Emergent Abilities of Large Language Models* ([arXiv:2206.07682](https://arxiv.org/abs/2206.07682)) | Systematic survey of 200+ tasks showing sharp capability transitions at scale |
| 2022 | Wei et al. — *Chain-of-Thought Prompting Elicits Reasoning* ([arXiv:2201.11903](https://arxiv.org/abs/2201.11903)) | Showed that step-by-step prompting unlocks reasoning — but only in sufficiently large models |
| 2023 | Schaeffer et al. — *Are Emergent Abilities a Mirage?* ([arXiv:2304.15004](https://arxiv.org/abs/2304.15004)) | Challenged emergence; argued metric choice creates the illusion of sudden jumps |

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

## Updating the Paper's Advice: What Has Changed?

Greener et al. (2022) remains an excellent introduction to ML fundamentals, but the field has moved fast since the paper was submitted (early 2021). Here are specific pieces of advice from the paper that need updating, with what we know now.

### 1. "When to use deep learning"

**Paper's advice:** Use deep learning primarily when you have a large dataset and raw unstructured input (images, sequences). For small tabular datasets, stick with classical ML (random forest, SVM).

**Update:** This is still *mostly* true for training models from scratch. But **transfer learning and foundation models** have changed the calculus. Today you can:

- Use a **pre-trained model** (e.g. a protein language model like ESM-2, or a vision model like BiomedCLIP) and fine-tune it on a small dataset — getting deep learning performance without needing thousands of training samples
- Use an **LLM with few-shot prompting** — no training data at all, just examples in the prompt
- Use **small language models** (Phi-3, Gemma) that run on a laptop

**New rule of thumb:** The question is no longer "do I have enough data for deep learning?" but "is there a pre-trained model close enough to my domain that I can adapt?"

### 2. "RNNs for sequence data"

**Paper's advice:** Recurrent neural networks (RNNs, LSTMs) are the natural choice for sequential data like protein sequences and genomic sequences.

**Update:** RNNs have been almost entirely replaced by **transformers** for sequence tasks. This happened rapidly after the paper was written:

| Year | Sequence modeling state-of-the-art |
|---|---|
| 2020 (paper written) | RNNs/LSTMs still common |
| 2021 | AlphaFold 2 (transformer-based) wins protein structure prediction |
| 2022–2023 | ESM-2, ProtTrans (protein language models) all transformer-based |
| 2024+ | Even DNA/RNA models (Evo, Nucleotide Transformer) are transformers |

**New advice:** For any sequence task (protein, DNA, RNA, clinical text), start with a **pre-trained transformer model** and fine-tune. RNNs are now largely historical.

### 3. "Transformers" — a brief mention

**Paper's advice:** Transformers get a brief mention as one architecture among many.

**Update:** Transformers are now the **dominant architecture** across nearly all domains — not just NLP but also computer vision (ViT), protein structure (AlphaFold 2), genomics (Evo), and multimodal tasks. The paper couldn't have predicted this: the transformer revolution was just beginning when the paper was written. See our [Transformer Architecture]({{ '/ai-intro/llms/#the-transformer-architecture' | relative_url }}) section for details.

### 4. "Self-supervised learning" — described as a niche technique

**Paper's advice:** Self-supervised learning is presented as one of several training approaches, used mainly for pre-training feature extractors.

**Update:** Self-supervised learning turned out to be the key that unlocked the entire LLM revolution. It's how GPT, Claude, LLaMA, and every modern LLM are trained: predict the next word from unlabeled text. This simple objective, applied at enormous scale, produces models with [emergent abilities]({{ '/ai-intro/llms/#emergent-abilities-when-scale-creates-surprises' | relative_url }}) that no one anticipated. Self-supervised learning is no longer niche — it's the foundation of modern AI.

### 5. Missing: prompt engineering as a new paradigm

**Not in the paper:** The concept of *using* a pre-trained model by writing natural language instructions (prompts) rather than training or fine-tuning.

**What's changed:** For many tasks, you no longer need to train a model at all. Instead:

```
Old workflow:  Collect data → Label data → Train model → Evaluate → Deploy
New workflow:  Write a prompt → Test → Iterate on prompt → Deploy
```

This doesn't replace all ML — you still need trained models for high-throughput tasks like variant calling or MALDI-TOF classification. But for reasoning tasks, literature review, report generation, and clinical decision support, prompt engineering is now a primary approach.

### 6. Missing: hallucination as a failure mode

**Not in the paper:** The paper covers overfitting, data leakage, and evaluation pitfalls — but not hallucination.

**What's changed:** For any AI system that *generates* text (LLMs, clinical report drafters, literature summarizers), **hallucination** — producing confident-sounding but factually wrong output — is now recognized as the most dangerous failure mode. This is especially critical in clinical microbiology where a hallucinated antibiotic resistance finding could affect patient care. Any deployment of generative AI in a clinical setting must include hallucination detection and human verification.

### 7. Missing: agentic AI

**Not in the paper:** The idea that AI systems can autonomously plan, use tools, and execute multi-step workflows.

**What's changed:** AI agents (like RareCollab from our reading list) represent a qualitative shift from "model as classifier" to "model as collaborator." This is covered in our [From language models to AI agents]({{ '/ai-intro/llms/#from-language-models-to-ai-agents' | relative_url }}) section.

### Summary

| Paper's advice (2022) | Updated advice (2025+) |
|---|---|
| Deep learning needs lots of data | Pre-trained models make small-data deep learning viable |
| RNNs for sequences | Transformers for everything sequential |
| Transformers are one option among many | Transformers dominate nearly all domains |
| Self-supervised learning is niche | Self-supervised learning is the foundation of modern AI |
| Train a model for each task | Prompt engineering can replace training for many tasks |
| Main risks: overfitting, data leakage | Add hallucination as a critical failure mode |
| AI classifies | AI reasons, plans, and uses tools (agents) |

> **Bottom line:** The paper's ML fundamentals (evaluation metrics, overfitting, data splitting) remain completely valid. What's changed is the *landscape of what's possible* — and the dominant architectures and workflows for getting there.

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
