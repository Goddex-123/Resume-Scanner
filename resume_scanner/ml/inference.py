"""
Hybrid Inference Engine
Combines rule-based NLP analysis with ML predictions and semantic embeddings
into an explainable resume-JD matching system.

Three tiers of analysis (each works independently):
  1. Rule-based: existing JobMatcher (always available)
  2. Semantic: embedding similarity (when sentence-transformers installed)
  3. ML Model: trained classifier prediction (when model exists)
"""

import logging
import os
from typing import Dict, List, Any, Optional

import numpy as np

logger = logging.getLogger(__name__)


class HybridMatcher:
    """
    Integrates rule-based, semantic, and ML-based resume matching.

    Graceful degradation:
      - If encoder unavailable → returns rule-based results only
      - If trained model unavailable → returns rule-based + semantic results
      - If both available → returns full hybrid analysis with explainability
    """

    def __init__(
        self,
        encoder=None,
        model=None,
        scaler=None,
        feature_names: Optional[List[str]] = None,
        model_metadata: Optional[Dict[str, Any]] = None,
        weights: Optional[Dict[str, float]] = None,
    ):
        """
        Args:
            encoder: Optional SemanticEncoder instance.
            model: Optional trained sklearn model.
            scaler: Optional fitted StandardScaler.
            feature_names: Ordered feature names matching the model's expectations.
            model_metadata: Model version, metrics, etc.
            weights: Hybrid scoring weights. Defaults to balanced weights.
        """
        self.encoder = encoder
        self.model = model
        self.scaler = scaler
        self.feature_names = feature_names
        self.model_metadata = model_metadata or {}
        self.weights = weights or {
            "semantic_similarity": 0.35,
            "required_skills": 0.30,
            "preferred_skills": 0.10,
            "experience_alignment": 0.10,
            "education_alignment": 0.05,
            "lexical_similarity": 0.10,
        }

    @property
    def has_encoder(self) -> bool:
        return self.encoder is not None

    @property
    def has_model(self) -> bool:
        return self.model is not None and self.scaler is not None

    def match(
        self,
        resume_text: str,
        jd_text: str,
        rule_based_results: Optional[Dict[str, Any]] = None,
        resume_sections: Optional[Dict[str, str]] = None,
        jd_sections: Optional[Dict[str, str]] = None,
        jd_required_skills: Optional[List[str]] = None,
        jd_preferred_skills: Optional[List[str]] = None,
        jd_experience_years: Optional[float] = None,
        jd_education_required: Optional[List[str]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Perform hybrid matching analysis.

        Args:
            resume_text: Full resume text.
            jd_text: Full JD text.
            rule_based_results: Optional pre-computed results from JobMatcher.
            resume_sections: Optional structured resume sections.
            jd_sections: Optional structured JD sections.
            jd_required_skills: Required skills from JD analysis.
            jd_preferred_skills: Preferred skills from JD analysis.
            jd_experience_years: Required experience from JD.
            jd_education_required: Education requirements from JD.

        Returns:
            Dict with ML and semantic analysis results, or None if no ML
            capabilities are available.
        """
        if not self.has_encoder and not self.has_model:
            return None

        result: Dict[str, Any] = {
            "ml_available": True,
            "has_semantic": self.has_encoder,
            "has_trained_model": self.has_model,
        }

        # ── Semantic similarity ───────────────────────────────────────────
        if self.has_encoder:
            try:
                semantic_results = self._compute_semantic(
                    resume_text, jd_text, resume_sections, jd_sections
                )
                result["semantic_similarity"] = semantic_results
            except Exception as e:
                logger.warning("Semantic analysis failed: %s", e)
                result["semantic_similarity"] = {"full_document": 0.0}

        # ── ML model prediction ───────────────────────────────────────────
        if self.has_model:
            try:
                ml_results = self._compute_ml_prediction(
                    resume_text=resume_text,
                    jd_text=jd_text,
                    resume_sections=resume_sections,
                    jd_sections=jd_sections,
                    jd_required_skills=jd_required_skills,
                    jd_preferred_skills=jd_preferred_skills,
                    jd_experience_years=jd_experience_years,
                    jd_education_required=jd_education_required,
                )
                result["ml_prediction"] = ml_results
            except Exception as e:
                logger.warning("ML prediction failed: %s", e)
                result["ml_prediction"] = None

        # ── Feature contributions (explainability) ────────────────────────
        if rule_based_results and self.has_encoder:
            result["feature_contributions"] = self._explain(
                rule_based_results,
                result.get("semantic_similarity", {}),
            )

        # ── Model info ────────────────────────────────────────────────────
        result["model_info"] = self._get_model_info()

        return result

    def _compute_semantic(
        self,
        resume_text: str,
        jd_text: str,
        resume_sections: Optional[Dict[str, str]] = None,
        jd_sections: Optional[Dict[str, str]] = None,
    ) -> Dict[str, float]:
        """Compute semantic similarity scores."""
        result: Dict[str, float] = {}

        # Full document similarity
        result["full_document"] = max(
            0.0, self.encoder.similarity(resume_text, jd_text)
        )

        # Section-level similarity
        if resume_sections and jd_sections:
            section_sims = self.encoder.section_similarity(
                resume_sections, jd_sections
            )
            result.update(section_sims)

        return result

    def _compute_ml_prediction(
        self,
        resume_text: str,
        jd_text: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """Compute ML model prediction with probability."""
        from .features import FeatureExtractor, FEATURE_SCHEMA

        extractor = FeatureExtractor(encoder=self.encoder)
        features = extractor.extract(resume_text, jd_text, **kwargs)

        # Build feature vector in the correct order
        if self.feature_names:
            feature_vector = [features.get(name, 0.0) for name in self.feature_names]
        else:
            feature_vector = [features.get(name, 0.0) for name in FEATURE_SCHEMA]

        X = np.array([feature_vector])
        X_scaled = self.scaler.transform(X)

        # Predict
        prediction = int(self.model.predict(X_scaled)[0])
        probability = 0.0
        if hasattr(self.model, "predict_proba"):
            probability = float(self.model.predict_proba(X_scaled)[0, 1])

        # Feature importances for this prediction
        top_features = []
        if hasattr(self.model, "feature_importances_"):
            importances = self.model.feature_importances_
            names = self.feature_names or FEATURE_SCHEMA
            paired = list(zip(names, importances, feature_vector))
            paired.sort(key=lambda x: abs(x[1]), reverse=True)
            for name, importance, value in paired[:8]:
                top_features.append({
                    "feature": name,
                    "importance": round(float(importance), 4),
                    "value": round(float(value), 4),
                })

        return {
            "prediction": prediction,
            "match_probability": round(probability, 4),
            "top_features": top_features,
            "disclaimer": (
                "Estimated probability of a positive match under the trained model. "
                "This is NOT a prediction of hiring outcome."
            ),
        }

    def _explain(
        self,
        rule_results: Dict[str, Any],
        semantic_results: Dict[str, float],
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate explainable positive/negative signal breakdown.

        Combines rule-based coverage with semantic similarity to
        produce human-readable contribution explanations.
        """
        positive = []
        negative = []

        breakdown = rule_results.get("breakdown", {})

        # Required skills
        req_match = breakdown.get("required_skills_match", 0)
        if req_match >= 80:
            positive.append({
                "signal": "Strong required skill coverage",
                "value": f"{req_match:.0f}%",
                "weight": self.weights.get("required_skills", 0.30),
            })
        elif req_match < 50:
            negative.append({
                "signal": "Low required skill coverage",
                "value": f"{req_match:.0f}%",
                "weight": self.weights.get("required_skills", 0.30),
            })

        # Preferred skills
        pref_match = breakdown.get("preferred_skills_match", 0)
        if pref_match >= 60:
            positive.append({
                "signal": "Good preferred skill coverage",
                "value": f"{pref_match:.0f}%",
                "weight": self.weights.get("preferred_skills", 0.10),
            })

        # Experience
        exp_align = breakdown.get("experience_alignment", 0)
        if exp_align >= 80:
            positive.append({
                "signal": "Strong experience alignment",
                "value": f"{exp_align:.0f}%",
                "weight": self.weights.get("experience_alignment", 0.10),
            })
        elif exp_align < 60:
            negative.append({
                "signal": "Experience gap detected",
                "value": f"{exp_align:.0f}%",
                "weight": self.weights.get("experience_alignment", 0.10),
            })

        # Education
        edu_align = breakdown.get("education_alignment", 0)
        if edu_align >= 80:
            positive.append({
                "signal": "Education requirement met",
                "value": f"{edu_align:.0f}%",
                "weight": self.weights.get("education_alignment", 0.05),
            })

        # Semantic similarity
        full_doc_sim = semantic_results.get("full_document", 0)
        if full_doc_sim >= 0.6:
            positive.append({
                "signal": "Strong semantic alignment with job description",
                "value": f"{full_doc_sim:.0%}",
                "weight": self.weights.get("semantic_similarity", 0.35),
            })
        elif full_doc_sim < 0.3:
            negative.append({
                "signal": "Weak semantic alignment — resume language differs from JD",
                "value": f"{full_doc_sim:.0%}",
                "weight": self.weights.get("semantic_similarity", 0.35),
            })

        # Missing skills
        missing_req = rule_results.get("missing_required_skills", [])
        if missing_req:
            negative.append({
                "signal": f"Missing required skills: {', '.join(missing_req[:5])}",
                "value": f"{len(missing_req)} skills",
                "weight": 0.0,
            })

        return {"positive": positive, "negative": negative}

    def _get_model_info(self) -> Dict[str, Any]:
        """Return model metadata for display."""
        info: Dict[str, Any] = {
            "semantic_model": (
                self.encoder.model_name if self.has_encoder else "unavailable"
            ),
        }

        if self.has_model:
            info["classifier_type"] = self.model_metadata.get(
                "model_type", type(self.model).__name__
            )
            info["model_version"] = self.model_metadata.get("model_version", "1.0.0")
            info["training_f1"] = self.model_metadata.get("f1", "N/A")
            info["training_roc_auc"] = self.model_metadata.get("roc_auc", "N/A")
        else:
            info["classifier_type"] = "none (semantic-only mode)"
            info["model_version"] = "N/A"

        info["weights"] = self.weights

        return info


def create_hybrid_matcher(
    encoder=None,
    model_dir: str = "models",
) -> HybridMatcher:
    """
    Factory function to create a HybridMatcher with optional trained model.

    Loads model from disk if available, otherwise returns semantic-only matcher.

    Args:
        encoder: Optional SemanticEncoder instance.
        model_dir: Path to model directory.

    Returns:
        Configured HybridMatcher instance.
    """
    model = None
    scaler = None
    feature_names = None
    metadata = None

    model_path = os.path.join(model_dir, "model.joblib")
    if os.path.exists(model_path):
        try:
            from .model import load_model
            model, scaler, metadata, feature_names = load_model(model_dir)
            logger.info("Loaded trained model from %s", model_dir)
        except Exception as e:
            logger.warning("Failed to load trained model: %s", e)

    return HybridMatcher(
        encoder=encoder,
        model=model,
        scaler=scaler,
        feature_names=feature_names,
        model_metadata=metadata,
    )
