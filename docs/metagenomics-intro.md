---
layout: page
title: "Metagenomics & Taxonomic Profiling — Introduction"
permalink: /metagenomics-intro/
---

# Metagenomics & Taxonomic Profiling

Background reading for the PLmicRO Journal Club — Series 3: Metagenomics & Microbiome.

---

## What is metagenomics?

Metagenomics is the study of genetic material recovered directly from environmental or clinical samples — without the need to culture individual organisms first. Instead of isolating a single species, you sequence **everything** in the sample: bacteria, archaea, viruses, fungi, and host DNA all mixed together. This "shotgun" approach gives an unbiased snapshot of the entire microbial community present.

The two main flavours:

| Approach | What it sequences | Resolution | Typical use |
|---|---|---|---|
| **Amplicon sequencing** (e.g. 16S rRNA) | One marker gene | Genus-level | Community surveys, microbiome studies |
| **Shotgun metagenomics** | All DNA in the sample | Species/strain-level | Pathogen detection, resistome, functional profiling |

Shotgun metagenomics is increasingly used in clinical microbiology for pathogen identification, antimicrobial resistance gene detection, and outbreak investigation — especially when culture fails or when you want to see the full picture.

---

## The taxonomic classification problem

Given millions of short (or long) sequencing reads from a metagenomic sample, **taxonomic classification** asks: *which organism does each read come from?*

This is harder than it sounds:

- **Databases are incomplete** — not all organisms have reference genomes.
- **Closely related species share sequence** — distinguishing *E. coli* from *Shigella* at read level is non-trivial.
- **Different tools have different biases** — some favour precision, some recall; some work well for bacteria but miss viruses.
- **Short reads carry less information** than long reads, but long reads have higher error rates.

A common strategy is to run the same data through **multiple classifiers and databases** and compare or merge the results. This helps reveal tool-specific biases and increases confidence in the findings — but it is tedious and error-prone to do manually.

---

## Enter nf-core/taxprofiler

**nf-core/taxprofiler** is a bioinformatics pipeline that automates exactly this multi-tool taxonomic profiling workflow. It takes raw shotgun metagenomic reads (short or long) and runs them through up to **11 different classification and profiling tools** — in parallel, against multiple databases — within a single reproducible pipeline run.

### Publication

> Stamouli S, Beber ME, Normark T, Christensen TA, Andersson-Li L, Borry M, Jamy M, nf-core community, Fellows Yates JA (2023). **nf-core/taxprofiler: highly parallelised and flexible pipeline for metagenomic taxonomic classification and profiling.** *bioRxiv* preprint. DOI: [10.1101/2023.10.20.563221](https://doi.org/10.1101/2023.10.20.563221)

### What the pipeline does

```
Raw reads
    │
    ▼
┌──────────────────────────┐
│  1. Quality control       │  FastQC / falco
│  2. Preprocessing         │  Adapter trimming (fastp, AdapterRemoval2, Porechop)
│     • Quality filtering   │  bbduk, PRINSEQ++, Filtlong
│     • Host removal        │  Bowtie2, Minimap2
│  3. Classification        │  Kraken2, KrakenUniq, Bracken,
│     (11 tools in parallel)│  MetaPhlAn, MALT, DIAMOND,
│                           │  Centrifuge, Kaiju, mOTUs
│  4. Standardisation       │  Taxpasta (unified output tables)
│  5. Visualisation         │  Krona, MultiQC
└──────────────────────────┘
    │
    ▼
Standardised taxonomic profiles + QC reports
```

### Why it matters

1. **Reproducibility** — Built with [Nextflow](https://www.nextflow.io/) and [nf-core](https://nf-co.re/) best practices. Every tool runs in its own container (Docker/Singularity), so results are identical regardless of where you run.
2. **Scalability** — Runs on a laptop or an HPC cluster with the same command. Designed for anything from a few samples to thousands.
3. **Multi-tool comparison** — Running multiple classifiers on the same preprocessed data, in parallel, lets you compare biases and build confidence. The pipeline standardises outputs with [Taxpasta](https://taxpasta.readthedocs.io/) so results are directly comparable.
4. **Both short and long reads** — Supports Illumina, Oxford Nanopore, and PacBio data within the same run.
5. **Clinical relevance** — Pathogen identification from complex clinical specimens (respiratory, CSF, tissue), antimicrobial resistance context, infection surveillance.

### Supported classifiers at a glance

| Tool | Approach | Strengths |
|---|---|---|
| **Kraken2** | k-mer matching | Very fast, widely used |
| **KrakenUniq** | Unique k-mer counting | Better precision than Kraken2 |
| **Bracken** | Bayesian re-estimation | Improves Kraken2 abundance estimates |
| **MetaPhlAn** | Clade-specific markers | High specificity, lower false positives |
| **Centrifuge** | FM-index classification | Memory-efficient, handles large DBs |
| **Kaiju** | Protein-level classification | Finds divergent organisms |
| **DIAMOND** | Translated alignment | Functional + taxonomic info |
| **MALT** | Alignment to references | Detailed alignment statistics |
| **mOTUs** | Marker gene profiling | Includes uncultured species |

---

## Key concepts to know

| Term | Definition |
|---|---|
| **Taxonomic classification** | Assigning each read to a taxon (species, genus, etc.) |
| **Taxonomic profiling** | Estimating the relative abundance of taxa in a sample |
| **k-mer** | A short DNA subsequence of length *k*; used by Kraken2 and others for fast lookup |
| **Lowest common ancestor (LCA)** | When a read matches multiple taxa, it is assigned to their shared ancestor |
| **Host depletion** | Removing human (or other host) reads before classification |
| **Precision vs. recall tradeoff** | Strict tools miss real organisms (↓ recall); lenient tools report false ones (↓ precision) |
| **Shotgun metagenomics** | Sequencing all DNA in a sample, not just a marker gene |
| **Nextflow** | A workflow language for scalable, reproducible bioinformatics pipelines |
| **nf-core** | A community effort providing curated, peer-reviewed Nextflow pipelines |

---

## Discussion questions for reading the paper

1. Why run multiple classifiers on the same data rather than picking "the best" tool?
2. What are the tradeoffs between k-mer-based (Kraken2) and alignment-based (MALT, DIAMOND) classification?
3. How does the pipeline handle the differences between short-read and long-read data?
4. What role does host depletion play, and when might you skip it?
5. How does Taxpasta standardise outputs — and why is this non-trivial?
6. Could nf-core/taxprofiler be useful in a clinical microbiology lab setting? What would be the barriers?

---

## Further reading

- [nf-core/taxprofiler documentation](https://nf-co.re/taxprofiler/1.0.1/) — Full pipeline docs, parameters, and output descriptions
- [Ye et al. (2019) — *Benchmarking Metagenomics Tools for Taxonomic Classification*](https://doi.org/10.1016/j.cell.2019.07.010), Cell — Comprehensive benchmark of classification tools (already on our reading list!)
- [Breitwieser et al. (2019) — *A review of methods and databases for metagenomic classification and assembly*](https://doi.org/10.1093/bib/bbx120), Briefings in Bioinformatics
- [Ewels et al. (2020) — *The nf-core framework for community-curated bioinformatics pipelines*](https://doi.org/10.1038/s41587-020-0439-x), Nature Biotechnology
