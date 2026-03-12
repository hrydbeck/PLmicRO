---
layout: page
title: Glossary
permalink: /glossary/
---


Quick-reference glossary of terms that come up in our journal club papers. Organized by topic — use Ctrl+F to search.

*Contributions welcome — [edit on GitHub](https://github.com/hrydbeck/PLmicRO/edit/master/docs/glossary.md).*

---

## AI & Machine Learning — General

| Term | Definition |
|---|---|
| **Artificial intelligence (AI)** | Broad field of computer science aiming to build systems that perform tasks normally requiring human intelligence. ML is a subset of AI. |
| **Machine learning (ML)** | Algorithms that learn patterns from data rather than being explicitly programmed with rules. |
| **Deep learning (DL)** | ML using neural networks with many layers, capable of learning hierarchical representations. |
| **Model** | A mathematical function that maps inputs to outputs, learned from data. |
| **Training** | The process of adjusting model parameters to minimize error on known data. |
| **Inference / prediction** | Using a trained model on new, unseen data. |
| **Hyperparameter** | A setting chosen before training (e.g. learning rate, number of layers) — not learned from data. |
| **Epoch** | One complete pass through the entire training dataset. |
| **Batch size** | Number of samples processed before updating model parameters. |

---

## Large Language Models & Generative AI

| Term | Definition |
|---|---|
| **Large language model (LLM)** | A deep learning model trained on massive text data to understand and generate human language (e.g. GPT-4, Claude, LLaMA). |
| **Transformer** | Architecture behind modern LLMs — uses attention mechanisms to weigh the importance of different parts of the input. |
| **Mixture-of-Experts (MoE)** | Architecture where a model contains many specialist sub-networks ("experts") and a router that selects which to activate per input — allows models to be very large in total parameters but efficient per query. |
| **Attention mechanism** | Lets the model focus on the most relevant parts of the input when producing each output. |
| **Token** | The basic unit an LLM processes — roughly a word or subword (e.g. "microbiology" might be split into "micro" + "biology"). |
| **Prompt** | The input text/instructions given to an LLM. |
| **Cost function (loss function)** | The function a model minimizes during training. In **supervised** learning, it measures the gap between predictions and known correct answers (ground truth). In **unsupervised** learning, there are no labels — instead the cost function measures an internal consistency criterion: how well the model reconstructs its own input (autoencoders), how tight and separated its clusters are (k-means), or how well it predicts the probability of the data it sees (generative models). The data itself provides the signal, just not as human-provided labels. |
| **Fine-tuning** | Adapting a pre-trained model to a specific task or domain using additional training data. |
| **RAG (Retrieval-Augmented Generation)** | Combining an LLM with a knowledge retrieval step — the model looks up relevant documents before generating an answer. |
| **Foundation model** | A large model pre-trained on broad data that can be adapted to many downstream tasks (e.g. GPT-4, ESM-2). |
| **Hallucination** | When an LLM generates plausible-sounding but factually incorrect output. |
| **Context window** | The maximum amount of text an LLM can process at once (measured in tokens). |

---

## Agentic AI

| Term | Definition |
|---|---|
| **Agentic AI / AI agent** | An AI system that can autonomously plan, use tools, and take multi-step actions to accomplish a goal — beyond simple question-answer. |
| **Tool use** | When an AI agent calls external tools (databases, APIs, calculators) to gather information or perform actions. |
| **Chain-of-thought (CoT)** | Prompting an LLM to reason step by step, improving accuracy on complex tasks. |
| **Multi-agent system** | Multiple specialized AI agents collaborating on a task, each with different expertise (e.g. RareCollab's phenotype and molecular agents). |
| **Orchestrator** | A central agent that coordinates the actions of other agents in a multi-agent system. |
| **ReAct (Reasoning + Acting)** | A framework where an LLM alternates between reasoning about what to do and taking actions. |

---

## Learning Paradigms

| Term | Definition |
|---|---|
| **Supervised learning** | Model learns from labeled data (e.g. "this spectrum belongs to species X"). |
| **Unsupervised learning** | Model finds structure without labels (e.g. clustering similar genomes). |
| **Semi-supervised learning** | Mix of labeled and unlabeled data. |
| **Self-supervised learning** | Model generates its own labels from the data (e.g. masking part of a DNA sequence and predicting it). |
| **Transfer learning** | Using a model trained on one task as a starting point for another. |
| **Reinforcement learning (RL)** | Model learns by interacting with an environment, receiving rewards or penalties. |
| **RLHF (RL from Human Feedback)** | Training technique for LLMs — humans rank outputs and the model learns to produce preferred responses. |
| **Few-shot / zero-shot learning** | Making predictions with very few (or no) labeled training examples, typically by providing examples in the prompt. |

---

## Data Handling & Evaluation

| Term | Definition |
|---|---|
| **Features** | Input variables (e.g. peak intensities in a MALDI-TOF spectrum). |
| **Labels** | Known correct outputs used for training (e.g. species identity). |
| **Training / validation / test set** | Data splits for fitting the model, tuning hyperparameters, and final evaluation. |
| **Cross-validation** | Repeatedly splitting data into train/test folds for a robust performance estimate. |
| **Overfitting** | Model performs well on training data but poorly on new data. |
| **Underfitting** | Model is too simple to capture the patterns. |
| **Accuracy** | Fraction of correct predictions. Misleading with imbalanced classes. |
| **Precision** | Of all positive predictions, how many were correct? |
| **Recall (sensitivity)** | Of all actual positives, how many were found? |
| **F1-score** | Harmonic mean of precision and recall. |
| **AUC-ROC** | Area Under the ROC curve — measures classifier quality across all thresholds. |
| **Confusion matrix** | Table showing TP, FP, TN, FN. |
| **Benchmark** | A standardized dataset or task used to compare model performance. |

---

## Model Types

| Term | Definition |
|---|---|
| **Logistic regression** | Predicts class probabilities using a sigmoid function. Despite the name, it's a classifier. |
| **Random forest** | Ensemble of decision trees — robust and widely used. |
| **SVM (Support Vector Machine)** | Finds the optimal boundary between classes. |
| **CNN (Convolutional Neural Network)** | Specialized for grid-like data (images, spectra). Uses learnable filters. |
| **RNN (Recurrent Neural Network)** | Specialized for sequential data; has memory of previous inputs. |
| **GNN (Graph Neural Network)** | Operates on graph-structured data (e.g. protein interaction networks). |
| **Autoencoder** | Neural network that learns a compressed representation (unsupervised). |
| **VAE (Variational Autoencoder)** | Autoencoder that learns a probabilistic latent space — can generate new data. |
| **GAN (Generative Adversarial Network)** | Two networks (generator + discriminator) trained against each other to produce realistic data. |
| **Diffusion model** | Generates data by learning to reverse a gradual noising process. |

---

## Dimensionality Reduction & Clustering

| Term | Definition |
|---|---|
| **PCA (Principal Component Analysis)** | Linear method to reduce dimensions while preserving variance. |
| **t-SNE** | Non-linear method for visualizing high-dimensional data in 2D/3D. |
| **UMAP** | Similar to t-SNE but faster and better at preserving global structure. |
| **k-means** | Partitions data into k clusters by minimizing within-cluster distances. |
| **Hierarchical clustering** | Builds a tree of nested clusters (dendrogram). |

---

## Genomics & Molecular Biology

| Term | Definition |
|---|---|
| **WGS (Whole Genome Sequencing)** | Sequencing the complete DNA of an organism. |
| **WES (Whole Exome Sequencing)** | Sequencing only the protein-coding regions (~1-2% of the genome). |
| **RNA-seq** | Sequencing RNA to measure gene expression levels. |
| **Variant** | A difference in DNA sequence compared to a reference genome (e.g. SNP, indel). |
| **SNP (Single Nucleotide Polymorphism)** | A single base-pair change in the genome. |
| **Indel** | Insertion or deletion of one or more nucleotides. |
| **VCF (Variant Call Format)** | Standard file format for storing variant data. |
| **Pathogenic variant** | A genetic variant that causes or contributes to disease. |
| **VUS (Variant of Uncertain Significance)** | A variant whose clinical impact is not yet established. |
| **HPO (Human Phenotype Ontology)** | Standardized vocabulary for describing clinical features/phenotypes in human disease. |
| **Mendelian disorder** | A disease caused by a mutation in a single gene, following classical inheritance patterns. |
| **Exome** | The part of the genome formed by exons — the protein-coding sequences. |
| **Transcriptome** | The complete set of RNA transcripts in a cell or tissue at a given time. |

---

## Clinical Microbiology

| Term | Definition |
|---|---|
| **MALDI-TOF MS** | Matrix-Assisted Laser Desorption/Ionization Time-of-Flight Mass Spectrometry — rapid microbial identification from protein profiles. |
| **AST (Antimicrobial Susceptibility Testing)** | Testing which antibiotics a pathogen is susceptible or resistant to. |
| **MIC (Minimum Inhibitory Concentration)** | The lowest concentration of an antibiotic that prevents visible bacterial growth. |
| **AMR (Antimicrobial Resistance)** | The ability of microorganisms to resist antimicrobial treatments. |
| **Resistome** | The collection of all antibiotic resistance genes in a sample or organism. |
| **MLST (Multi-Locus Sequence Typing)** | Typing scheme using sequences of ~7 housekeeping genes to categorize bacterial strains. |
| **cgMLST / wgMLST** | Core-genome or whole-genome MLST — higher resolution typing using hundreds to thousands of loci. |

---

## Metagenomics & Microbiome

| Term | Definition |
|---|---|
| **Metagenomics** | Sequencing all DNA in an environmental or clinical sample to study the community of organisms present. |
| **16S rRNA sequencing** | Targeted sequencing of the 16S ribosomal RNA gene for bacterial identification and profiling. |
| **Taxonomic profiling** | Determining which species (and their relative abundances) are present in a sample. |
| **OTU (Operational Taxonomic Unit)** | A cluster of similar sequences used as a proxy for a species (typically 97% identity). |
| **ASV (Amplicon Sequence Variant)** | Exact sequence variants resolved from amplicon data — higher resolution than OTUs. |
| **Alpha diversity** | Diversity within a single sample (e.g. Shannon index, species richness). |
| **Beta diversity** | Diversity between samples — how different are two communities? |

---

## Genomic Epidemiology

| Term | Definition |
|---|---|
| **Phylogenetics** | Study of evolutionary relationships, typically visualized as trees. |
| **SNP distance** | Number of single nucleotide differences between two genomes — used to assess relatedness. |
| **Outbreak detection** | Identifying clusters of closely related isolates suggesting a common source. |
| **Transmission tracking** | Using genomic data to reconstruct how a pathogen spreads between patients or settings. |
| **Core genome** | The set of genes shared by all (or nearly all) strains of a species. |
| **Accessory genome** | Genes present in some but not all strains — often includes virulence and resistance genes. |
| **Pangenome** | The full set of genes across all strains of a species (core + accessory). |

---

*Last updated: 2026-03-05 · [Edit on GitHub](https://github.com/hrydbeck/PLmicRO/edit/master/docs/glossary.md)*
