# Reading Guide — Greener et al. (2022)

## What to focus on

Given the journal club's interests (AI in clinical microbiology, benchmarking
models), pay special attention to:

### 1. The taxonomy of ML methods
Look for the figure/table showing how methods relate to each other. This gives
you the mental map of "what types of models exist" — essential context for every
later session.

### 2. Evaluation metrics
Sections on accuracy, precision, recall, F1-score, AUC-ROC, and cross-validation
are directly relevant to **how to compare and benchmark models** (Session 2
topic). Understand what each measures and when to use which.

### 3. Overfitting and generalization
The #1 pitfall for beginners and central to understanding why benchmarking
matters. Ask yourself: how would I know if my model is overfitting?

### 4. Best practices
Data splitting, feature scaling, hyperparameter tuning. These are practical tips
you can apply directly.

### 5. When to use which method
The paper discusses how different data types (images, sequences, tabular data)
map to different methods. This is highly relevant for clinical microbiology where
data comes in many forms (MALDI-TOF spectra, genomic sequences, clinical
variables).

## Suggested discussion questions

1. What is the difference between a model that *memorizes* vs. one that
   *generalizes*?
2. When would you pick a simple model (e.g. random forest) over a deep neural
   network?
3. What evaluation metric would you use for a clinical microbiology
   classification task with rare positive cases (e.g. detecting a resistant
   strain)? Why not just accuracy?
4. How does the paper's advice on data splitting apply to biological datasets
   that are often small?
5. Which ML method category seems most relevant to your own work, and why?

## Connections to later sessions

- **Session 2** builds directly on the evaluation/benchmarking concepts here
- **Session 4** (MALDI-TOF + ML) is a concrete clinical application of the CNN
  and random forest methods described here
- **Session 5** (Deep Learning in Genomics) goes deeper on the neural network
  architectures introduced here
