# Summary — Greener et al. (2022)

## What the paper covers

This is an **introductory review** aimed at biologists with little or no ML
background. It provides a gentle walkthrough of key techniques, from classical
methods to deep learning, with guidance on when and how to apply them to
biological data.

## Main sections

1. **Core ML concepts** — what it means to "fit a model to data," supervised vs.
   unsupervised learning, and the training/validation/test data split
2. **Traditional ML methods** — linear regression, logistic regression, support
   vector machines (SVMs), random forests, and dimensionality reduction (PCA,
   t-SNE)
3. **Neural networks & deep learning** — feedforward networks, convolutional
   neural networks (CNNs), recurrent neural networks (RNNs), autoencoders, and
   transformers
4. **Practical guidance** — evaluating model performance, avoiding overfitting,
   handling imbalanced datasets, choosing the right method for the data type
5. **Emerging directions** — generative models, transfer learning,
   interpretability/explainability

## Key vocabulary introduced

| Term | Meaning |
|------|---------|
| Supervised learning | Learning from labeled examples (input → known output) |
| Unsupervised learning | Finding structure in data without labels (e.g. clustering) |
| Features | The input variables the model uses to make predictions |
| Overfitting | Model memorizes training data instead of learning general patterns |
| Cross-validation | Repeatedly splitting data to estimate how well the model generalizes |
| Hyperparameters | Settings chosen before training (e.g. learning rate, number of layers) |
| AUC-ROC | Area Under the Receiver Operating Characteristic curve — a metric for classifier performance |
| CNN | Convolutional Neural Network — good for grid-structured data (images, spectra) |
| RNN | Recurrent Neural Network — good for sequential data (time series, sequences) |
| Transformer | Attention-based architecture — state-of-the-art for sequences (proteins, DNA) |
