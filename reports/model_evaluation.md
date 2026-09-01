# Model Evaluation Report

## Executive Summary
This report summarizes the performance of the Machine Learning classification layer added to the Resume Scanner. The ML layer supplements the existing rule-based system by providing a probability score indicating the likelihood of a candidate being a strong fit for a given Job Description.

## 1. Dataset Generation (Synthetic)
> [!IMPORTANT]
> The training dataset is explicitly **synthetic**. It is generated using template-based permutations across 5 professional domains to ensure a balanced, multi-class baseline for the model to learn from. 

- **Total Pairs**: 500+ generated
- **Domains**: Data Science, Software Engineering, Cybersecurity, Web Development, Data Engineering
- **Balance**: 1:1 Positive (matched domain and skills) to Negative (cross-domain or low skills)

## 2. Feature Engineering
The model operates on a 26-dimensional feature vector, integrating:
1. **Lexical Features**: TF-IDF cosine similarity, keyword overlap ratios.
2. **Semantic Features**: Sentence-BERT (all-MiniLM-L6-v2) cosine similarities between Resume sections and JD sections (e.g., Experience ↔ Responsibilities).
3. **Profile Features**: Parsed years of experience, education level, skill counts.
4. **Alignment Features**: Computed gaps in experience, education, and required skill coverage.

## 3. Model Comparison
Three algorithms were evaluated using stratified 5-fold cross-validation:

| Model | CV F1 Score | ROC-AUC | Notes |
|-------|-------------|---------|-------|
| **Logistic Regression** | 0.94 | 0.98 | Baseline linear model |
| **Random Forest** | 0.97 | 0.99 | Strong nonlinear baseline |
| **Gradient Boosting** | **0.98** | **0.99** | Selected as the final production model |

## 4. Error Analysis
- **False Positives**: Mostly occurred when a candidate had high keyword overlap but lacked the necessary years of experience (the model sometimes over-weighted TF-IDF).
- **False Negatives**: Occurred when a candidate used highly varied terminology not captured by the exact keyword matcher, though the Semantic Encoder helped mitigate this significantly.

## 5. Graceful Degradation
To ensure production stability:
- If `sentence-transformers` is unavailable, semantic features default to `0.0`.
- If the ML model file is missing, the system automatically falls back to rule-based + semantic matching (if available), or pure rule-based matching.

## 6. Future Work
- **Real-world Dataset**: Swap the synthetic data generation pipeline for an actual labeled dataset of historical hiring decisions.
- **Bias Mitigation**: While the current feature schema excludes demographic variables, real-world data would require strict bias audits.
