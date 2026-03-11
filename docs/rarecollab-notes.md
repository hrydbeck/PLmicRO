]633;E;{ echo '---'\x3b   echo 'layout: page'\x3b   echo 'title: "RareCollab — Agentic Diagnostics"'\x3b   echo 'permalink: /notes/rarecollab/'\x3b   echo '---'\x3b   echo ''\x3b   cat notes/ai_ml/rarecollab_notes.md\x3b } > docs/rarecollab-notes.md;af9fd577-405a-4917-817b-c4ddab6b31f9]633;C---
layout: page
title: "RareCollab — Agentic Diagnostics"
permalink: /notes/rarecollab/
---

# PLmicRO Journal Club — RareCollab

📅 **Date:**  
📄 **Paper:**  
- Qi G, Wang J, Chong ML, Shaik Z, Li S et al. (2026) — *RareCollab — An Agentic System Diagnosing Mendelian Disorders with Integrated Phenotypic and Molecular Evidence*, arXiv preprint  
  DOI/Link: [arXiv:2602.04058](https://arxiv.org/abs/2602.04058)

👥 **Attendees:** (add your name)  
-  

---

## Pre-reading Questions

*What should we look for while reading?*

- How does the agentic architecture differ from traditional variant prioritization pipelines?
- What role does phenotype information (HPO terms) play vs. molecular evidence?
- How is RNA-seq data integrated into the diagnostic reasoning?
- What are the implications for clinical microbiology / precision medicine?

---

## Key Concepts

*Core ideas, methods, and terminology from the paper — first-pass understanding, to be refined when reading the Methods section.*

### RareCollab Architecture Components

| Component | Role | Analogy |
|---|---|---|
| **Diagnostic Engine** | Stable, quantitative core that does numerical variant scoring and prioritization. Deterministic and reproducible. | The lab's bioinformatics pipeline |
| **LLM Specialist Labs** | LLM-powered modules, each handling a specific evidence type: transcriptomic (RNA-seq) signals, phenotype matching (HPO terms), variant databases (ClinVar, OMIM), literature review. They produce interpretable text-based assessments. | Individual domain experts (molecular geneticist, phenotype specialist, literature reviewer) |
| **Integration Engine** | Merges outputs from the Specialist Labs and the Diagnostic Engine into a unified ranking — combines "gene expression is aberrant" + "phenotype matches" + "variant is rare" into one coherent score. | The team meeting where findings are combined |
| **Confidence Reviewer** | Evaluates how confident the system is in each diagnosis — flags cases where evidence is contradictory or insufficient. Quality-control agent. | The senior reviewer who asks "are we sure enough to report this?" |

### Key terms
- **Agentic framework** — AI system that plans, uses tools, and takes multi-step actions autonomously (see [AI Primer](https://hrydbeck.github.io/PLmicRO/ai-intro/))
- **Multi-modal diagnostic reasoning** — combining genomic + transcriptomic + phenotype data (vs. traditional DNA-only interpretation)
- **Diagnostic odyssey** — the often years-long journey families face before receiving a rare disease diagnosis
- **UDN (Undiagnosed Diseases Network)** — NIH-funded network of clinical sites investigating undiagnosed patients; used as the benchmark dataset

---

## Methods Summary

*Study design, data, analytical approach*

- **Data:** UDN patients with paired genomic (exome/genome) and transcriptomic (RNA-seq) data
- **Methods:** Agentic framework with Diagnostic Engine (quantitative) + LLM Specialist Labs (interpretive) + Integration Engine (fusion) + Confidence Reviewer (QC)
- **Evaluation:** Top-1 and top-5 diagnostic accuracy compared against widely used variant-prioritization tools
- **Key result from abstract:** 77% top-5 accuracy, ~20% improvement over existing approaches

---

## Main Results

*Key findings and figures worth discussing*

-  

---

## Discussion Points

*Questions, critiques, connections to our work*

### Top-k accuracy
- **Top-1 accuracy** = correct causal variant ranked #1. **Top-5** = correct variant anywhere in the top 5 candidates.
- Clinicians review a ranked shortlist anyway, so top-5 is practically meaningful — like having the right diagnosis in your differential.
- Common metric in variant prioritization and information retrieval (cf. ImageNet top-5).

### Benchmark design & selection bias
- UDN patients were *originally* undiagnosed but many have **since been solved** through expert review, functional studies, etc. These solved cases provide the ground truth.
- **Not all UDN cases are solved** — the diagnostic rate is ~30–35%. The benchmark uses only the subset with (a) a confirmed diagnosis AND (b) paired genomic + RNA-seq data.
- This creates **selection bias**: solved cases may be systematically easier; the hardest cases remain unsolved and untested.
- 💬 **Key question for discussion:** Does the 77% top-5 accuracy on the solvable subset tell us anything about performance on truly unsolved cases?
- 💬 Could RareCollab help solve cases that humans couldn't, or does it only replicate what experts already achieved?

---

## Strengths & Limitations

| ✅ Strengths | ⚠️ Limitations |
|---|---|
| Multi-modal integration (genomic + transcriptomic + phenotype) | Benchmark limited to solved UDN cases — selection bias toward "easier" cases |
| Modular architecture — components can be updated independently | Requires paired RNA-seq data, which isn't always available |
| ~20% improvement over existing variant prioritization tools | ~65–70% of UDN cases remain unsolved and untested |
| Interpretable assessments from LLM Specialist Labs | Real-world performance on truly unsolved cases unknown |

---

## Relevance to Our Work

*How does this connect to precision medicine, clinical microbiology, or our bioinformatics practice?*

- Agentic AI systems — could similar approaches work for microbial diagnostics?
- Multi-modal integration (genomic + phenotypic) — parallels to clinical micro workflows?

---

## Action Items

- [ ]  

---

## Resources & Links

- [arXiv paper](https://arxiv.org/abs/2602.04058)
- [PDF](https://arxiv.org/pdf/2602.04058)
- [Zotero entry]()

---

*Notes taken collaboratively — see [PLmicRO GitHub Pages](https://hrydbeck.github.io/PLmicRO/notes/)*
