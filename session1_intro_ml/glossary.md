# Glossary — ML Terms for Biologists

Quick-reference glossary of terms you will encounter in Greener et al. (2022)
and throughout the journal club.

## General concepts

- **Machine learning (ML):** Algorithms that learn patterns from data rather
  than being explicitly programmed with rules.
- **Artificial intelligence (AI):** Broad field; ML is a subset of AI.
- **Deep learning (DL):** ML using neural networks with many layers.
- **Model:** A mathematical function that maps inputs to outputs, learned from
  data.
- **Training:** The process of adjusting model parameters to minimize error on
  known data.
- **Inference/prediction:** Using a trained model on new, unseen data.

## Learning paradigms

- **Supervised learning:** Model learns from labeled data (e.g. "this spectrum
  belongs to species X").
- **Unsupervised learning:** Model finds structure without labels (e.g.
  clustering similar genomes).
- **Semi-supervised learning:** Mix of labeled and unlabeled data.
- **Self-supervised learning:** Model generates its own labels from the data
  (e.g. masking part of a DNA sequence and predicting it).
- **Transfer learning:** Using a model trained on one task as a starting point
  for another.

## Data handling

- **Features:** Input variables (e.g. peak intensities in a MALDI-TOF spectrum).
- **Labels:** Known correct outputs used for training (e.g. species identity).
- **Training set:** Data used to fit the model.
- **Validation set:** Data used to tune hyperparameters and prevent overfitting.
- **Test set:** Held-out data used only for final evaluation.
- **Cross-validation:** Repeatedly splitting data into train/test folds to get a
  robust performance estimate.
- **Overfitting:** Model performs well on training data but poorly on new data.
- **Underfitting:** Model is too simple to capture the patterns in the data.

## Evaluation metrics

- **Accuracy:** Fraction of correct predictions. Misleading with imbalanced
  classes.
- **Precision:** Of all positive predictions, how many were correct?
- **Recall (sensitivity):** Of all actual positives, how many were found?
- **F1-score:** Harmonic mean of precision and recall.
- **AUC-ROC:** Area Under the Receiver Operating Characteristic curve. Measures
  overall classifier quality across all thresholds.
- **Confusion matrix:** Table showing true positives, false positives, true
  negatives, false negatives.

## Model types

- **Linear regression:** Predicts a continuous value as a weighted sum of
  features.
- **Logistic regression:** Predicts a probability/class using a sigmoid
  function. Despite the name, it is a classifier.
- **Decision tree:** Splits data by asking yes/no questions about features.
- **Random forest:** Ensemble of many decision trees; robust and widely used.
- **Support vector machine (SVM):** Finds the optimal boundary between classes.
- **k-nearest neighbors (kNN):** Classifies based on the majority class of the
  k closest training examples.
- **Neural network:** Layers of interconnected nodes that learn hierarchical
  representations.
- **CNN (Convolutional Neural Network):** Specialized for grid-like data
  (images, spectra). Uses learnable filters.
- **RNN (Recurrent Neural Network):** Specialized for sequential data. Has
  memory of previous inputs.
- **Transformer:** Uses attention mechanisms to weigh the importance of
  different parts of the input. State-of-the-art for sequences.
- **Autoencoder:** Neural network that learns a compressed representation of the
  data (unsupervised).

## Dimensionality reduction

- **PCA (Principal Component Analysis):** Linear method to reduce dimensions
  while preserving variance.
- **t-SNE:** Non-linear method for visualizing high-dimensional data in 2D/3D.
- **UMAP:** Similar to t-SNE but faster and better at preserving global
  structure.
