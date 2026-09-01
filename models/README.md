# Machine Learning Models

This directory stores persisted ML models and their associated artifacts for the Resume Scanner's hybrid matching engine.

## Contents
When a model is trained using the `ModelTrainer` (via the `03_model_comparison.ipynb` notebook), it generates:

- `model.joblib`: The trained scikit-learn classifier (e.g., GradientBoostingClassifier).
- `scaler.joblib`: The fitted StandardScaler for feature normalization.
- `metadata.json`: Model versioning, evaluation metrics (F1, ROC-AUC), training timestamp, and embedding model name.
- `feature_schema.json`: Ordered list of the 26+ features expected by the model.

## Note on Version Control
Binary model files (`*.joblib`, `*.pkl`, `*.pt`, `*.bin`) are excluded from version control via `.gitignore` to keep the repository lightweight. 

To use the ML features, you must either:
1. Run the `03_model_comparison.ipynb` notebook to generate a local model.
2. Download pre-trained weights (if provided via a release).

If this directory is empty, the `HybridMatcher` will automatically degrade gracefully to Semantic-Only matching.
