"""
Model Training & Evaluation Module
Trains, compares, and persists ML models for resume-JD matching.

Implements a structured comparison pipeline across multiple classifiers
with proper evaluation metrics and data leakage prevention.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

import numpy as np
import joblib

logger = logging.getLogger(__name__)


def _safe_import_sklearn():
    """Import sklearn components with error handling."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import (
        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        roc_auc_score,
        average_precision_score,
        confusion_matrix,
    )
    from sklearn.model_selection import StratifiedKFold

    return {
        "LogisticRegression": LogisticRegression,
        "RandomForestClassifier": RandomForestClassifier,
        "GradientBoostingClassifier": GradientBoostingClassifier,
        "StandardScaler": StandardScaler,
        "accuracy_score": accuracy_score,
        "precision_score": precision_score,
        "recall_score": recall_score,
        "f1_score": f1_score,
        "roc_auc_score": roc_auc_score,
        "average_precision_score": average_precision_score,
        "confusion_matrix": confusion_matrix,
        "StratifiedKFold": StratifiedKFold,
    }


class ModelTrainer:
    """
    Trains and compares multiple classifiers for resume-JD matching.

    Evaluates: Logistic Regression, Random Forest, Gradient Boosting
    using stratified cross-validation and comprehensive metrics.
    """

    def __init__(self, feature_names: Optional[List[str]] = None):
        self.feature_names = feature_names
        self.sklearn = _safe_import_sklearn()
        self.scaler = self.sklearn["StandardScaler"]()
        self.best_model = None
        self.best_model_name = None
        self.best_metrics: Dict[str, float] = {}
        self.comparison_results: List[Dict[str, Any]] = []

    def _get_model_configs(self) -> Dict[str, Any]:
        """Define model configurations for comparison."""
        return {
            "logistic_regression": self.sklearn["LogisticRegression"](
                max_iter=1000,
                random_state=42,
                class_weight="balanced",
                C=1.0,
            ),
            "random_forest": self.sklearn["RandomForestClassifier"](
                n_estimators=100,
                max_depth=10,
                random_state=42,
                class_weight="balanced",
                n_jobs=-1,
            ),
            "gradient_boosting": self.sklearn["GradientBoostingClassifier"](
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42,
            ),
        }

    def train_and_compare(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
        n_cv_folds: int = 5,
    ) -> Dict[str, Any]:
        """
        Train multiple models and compare their performance.

        Args:
            X_train: Training feature matrix.
            y_train: Training labels.
            X_test: Test feature matrix.
            y_test: Test labels.
            n_cv_folds: Number of cross-validation folds.

        Returns:
            Comparison results dict with per-model metrics and best model selection.
        """
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        models = self._get_model_configs()
        results = []

        for name, model in models.items():
            logger.info("Training model: %s", name)

            try:
                # Train
                model.fit(X_train_scaled, y_train)

                # Predict
                y_pred = model.predict(X_test_scaled)
                y_prob = (
                    model.predict_proba(X_test_scaled)[:, 1]
                    if hasattr(model, "predict_proba")
                    else model.decision_function(X_test_scaled)
                )

                # Evaluate
                metrics = self._compute_metrics(y_test, y_pred, y_prob)
                metrics["model_name"] = name

                # Cross-validation F1
                cv_scores = self._cross_validate(
                    model, X_train_scaled, y_train, n_folds=n_cv_folds
                )
                metrics["cv_f1_mean"] = float(np.mean(cv_scores))
                metrics["cv_f1_std"] = float(np.std(cv_scores))

                # Feature importance (for tree models)
                if hasattr(model, "feature_importances_"):
                    importances = model.feature_importances_
                    if self.feature_names and len(self.feature_names) == len(importances):
                        top_features = sorted(
                            zip(self.feature_names, importances),
                            key=lambda x: x[1],
                            reverse=True,
                        )[:10]
                        metrics["top_features"] = [
                            {"name": n, "importance": round(float(v), 4)}
                            for n, v in top_features
                        ]

                # Confusion matrix
                cm = self.sklearn["confusion_matrix"](y_test, y_pred)
                metrics["confusion_matrix"] = cm.tolist()

                results.append({"name": name, "model": model, "metrics": metrics})
                logger.info("  %s — F1: %.3f, ROC-AUC: %.3f", name, metrics["f1"], metrics["roc_auc"])

            except Exception as e:
                logger.error("Failed to train %s: %s", name, e)
                results.append({
                    "name": name,
                    "model": None,
                    "metrics": {"error": str(e), "model_name": name},
                })

        # Select best model by F1
        valid_results = [r for r in results if r["model"] is not None]
        if valid_results:
            best = max(valid_results, key=lambda r: r["metrics"].get("f1", 0))
            self.best_model = best["model"]
            self.best_model_name = best["name"]
            self.best_metrics = best["metrics"]
            logger.info("Best model: %s (F1=%.3f)", best["name"], best["metrics"]["f1"])

        self.comparison_results = [r["metrics"] for r in results]

        return {
            "comparison": self.comparison_results,
            "best_model": self.best_model_name,
            "best_metrics": self.best_metrics,
            "dataset_stats": {
                "train_samples": len(y_train),
                "test_samples": len(y_test),
                "train_positive_ratio": float(np.mean(y_train)),
                "test_positive_ratio": float(np.mean(y_test)),
                "n_features": X_train.shape[1],
            },
        }

    def _compute_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_prob: np.ndarray,
    ) -> Dict[str, float]:
        """Compute classification metrics."""
        metrics = {
            "accuracy": float(self.sklearn["accuracy_score"](y_true, y_pred)),
            "precision": float(self.sklearn["precision_score"](y_true, y_pred, zero_division=0)),
            "recall": float(self.sklearn["recall_score"](y_true, y_pred, zero_division=0)),
            "f1": float(self.sklearn["f1_score"](y_true, y_pred, zero_division=0)),
        }

        try:
            metrics["roc_auc"] = float(self.sklearn["roc_auc_score"](y_true, y_prob))
        except ValueError:
            metrics["roc_auc"] = 0.0

        try:
            metrics["pr_auc"] = float(self.sklearn["average_precision_score"](y_true, y_prob))
        except ValueError:
            metrics["pr_auc"] = 0.0

        return metrics

    def _cross_validate(
        self, model, X: np.ndarray, y: np.ndarray, n_folds: int = 5
    ) -> List[float]:
        """Run stratified cross-validation and return F1 scores."""
        n_folds = min(n_folds, min(np.sum(y == 0), np.sum(y == 1)))
        if n_folds < 2:
            return [0.0]

        kfold = self.sklearn["StratifiedKFold"](
            n_splits=n_folds, shuffle=True, random_state=42
        )
        scores = []

        for train_idx, val_idx in kfold.split(X, y):
            clone = model.__class__(**model.get_params())
            clone.fit(X[train_idx], y[train_idx])
            y_pred = clone.predict(X[val_idx])
            score = self.sklearn["f1_score"](y[val_idx], y_pred, zero_division=0)
            scores.append(float(score))

        return scores


def save_model(
    model: Any,
    scaler: Any,
    metadata: Dict[str, Any],
    feature_names: List[str],
    output_dir: str = "models",
) -> str:
    """
    Persist a trained model with metadata and feature schema.

    Args:
        model: Trained sklearn model.
        scaler: Fitted StandardScaler.
        metadata: Model metadata (metrics, version, etc.).
        feature_names: Ordered list of feature names.
        output_dir: Directory to save model artifacts.

    Returns:
        Path to the saved model directory.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Save model
    model_path = os.path.join(output_dir, "model.joblib")
    joblib.dump(model, model_path)

    # Save scaler
    scaler_path = os.path.join(output_dir, "scaler.joblib")
    joblib.dump(scaler, scaler_path)

    # Save feature schema
    schema_path = os.path.join(output_dir, "feature_schema.json")
    with open(schema_path, "w", encoding="utf-8") as f:
        json.dump(feature_names, f, indent=2)

    # Save metadata
    metadata["saved_at"] = datetime.now().isoformat()
    metadata["model_path"] = model_path
    metadata["scaler_path"] = scaler_path
    meta_path = os.path.join(output_dir, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, default=str)

    logger.info("Model saved to %s", output_dir)
    return output_dir


def load_model(
    model_dir: str = "models",
) -> Tuple[Any, Any, Dict[str, Any], List[str]]:
    """
    Load a persisted model, scaler, metadata, and feature schema.

    Args:
        model_dir: Directory containing model artifacts.

    Returns:
        Tuple of (model, scaler, metadata, feature_names).

    Raises:
        FileNotFoundError: If model artifacts don't exist.
    """
    model_path = os.path.join(model_dir, "model.joblib")
    scaler_path = os.path.join(model_dir, "scaler.joblib")
    meta_path = os.path.join(model_dir, "metadata.json")
    schema_path = os.path.join(model_dir, "feature_schema.json")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"No trained model found at {model_path}")

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    with open(schema_path, "r", encoding="utf-8") as f:
        feature_names = json.load(f)

    logger.info("Model loaded from %s (type: %s)", model_dir, metadata.get("model_type", "unknown"))
    return model, scaler, metadata, feature_names
