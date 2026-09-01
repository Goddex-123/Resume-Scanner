"""
Feature Engineering Module
Extracts structured feature vectors from resume + JD pairs for ML classification.

Produces 25+ features across 5 categories:
  - Lexical (TF-IDF, keyword overlap)
  - Semantic (embedding similarities)
  - Resume profile (experience, skills, education)
  - JD profile (requirements, preferences)
  - Alignment (gaps, coverage ratios)
"""

import re
import math
import logging
from typing import Dict, List, Any, Optional
from collections import Counter

logger = logging.getLogger(__name__)

# Feature schema — ordered list of all feature names produced by this extractor
FEATURE_SCHEMA = [
    # Lexical features
    "tfidf_cosine_similarity",
    "keyword_overlap_ratio",
    "required_keyword_coverage",
    "preferred_keyword_coverage",
    # Semantic features (0.0 when unavailable)
    "full_doc_embedding_similarity",
    "experience_responsibilities_sim",
    "skills_requirements_sim",
    "projects_responsibilities_sim",
    "summary_job_summary_sim",
    # Resume profile features
    "years_of_experience",
    "num_skills",
    "num_relevant_skills",
    "num_projects",
    "num_experience_entries",
    "education_level",
    "certification_count",
    "achievement_density",
    # JD profile features
    "required_skill_count",
    "preferred_skill_count",
    "required_experience_years",
    "education_requirement_level",
    # Alignment features
    "experience_gap",
    "skill_gap",
    "education_match",
    "required_skill_coverage",
    "preferred_skill_coverage",
]


def _tokenize(text: str) -> List[str]:
    """Simple word tokenizer matching the existing JobMatcher approach."""
    words = re.findall(r"\b[a-z][a-z0-9+#.-]*\b", text.lower())
    return [w for w in words if len(w) > 2]


def _tfidf_cosine(text_a: str, text_b: str) -> float:
    """Compute TF-IDF cosine similarity between two texts."""
    words_a = _tokenize(text_a)
    words_b = _tokenize(text_b)
    if not words_a or not words_b:
        return 0.0

    # Build vocabulary from both documents
    vocab = set(words_a) | set(words_b)

    # Term frequency
    tf_a = Counter(words_a)
    tf_b = Counter(words_b)

    # IDF across the 2-document corpus
    doc_freq = {}
    for w in vocab:
        df = (1 if w in tf_a else 0) + (1 if w in tf_b else 0)
        doc_freq[w] = math.log(2.0 / (df + 1)) + 1  # smoothed IDF

    # TF-IDF vectors
    tfidf_a = {w: (tf_a[w] / len(words_a)) * doc_freq[w] for w in vocab if w in tf_a}
    tfidf_b = {w: (tf_b[w] / len(words_b)) * doc_freq[w] for w in vocab if w in tf_b}

    # Cosine similarity
    common = set(tfidf_a.keys()) & set(tfidf_b.keys())
    if not common:
        return 0.0

    dot = sum(tfidf_a[w] * tfidf_b[w] for w in common)
    mag_a = math.sqrt(sum(v ** 2 for v in tfidf_a.values()))
    mag_b = math.sqrt(sum(v ** 2 for v in tfidf_b.values()))

    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def _keyword_overlap(text_a: str, text_b: str) -> float:
    """Jaccard-style keyword overlap ratio."""
    set_a = set(_tokenize(text_a))
    set_b = set(_tokenize(text_b))
    if not set_a or not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union) if union else 0.0


def _encode_education_level(text: str) -> int:
    """Convert education text to ordinal level (0-4)."""
    text_lower = text.lower()
    if re.search(r"\bph\.?d|doctorate\b", text_lower):
        return 4
    if re.search(r"\bmaster|m\.s\.|m\.a\.|mba\b", text_lower):
        return 3
    if re.search(r"\bbachelor|b\.s\.|b\.a\.\b", text_lower):
        return 2
    if re.search(r"\bassociate\b", text_lower):
        return 1
    return 0


def _count_projects(text: str) -> int:
    """Estimate number of project entries in resume text."""
    project_patterns = [
        r"(?im)^[\s•\-\*]*project\s*[:\-]",
        r"(?im)^[\s•\-\*]*(?:personal|side|academic|capstone)\s+project",
    ]
    count = 0
    for pat in project_patterns:
        count += len(re.findall(pat, text))
    # Also count section-style entries
    if re.search(r"(?i)\bprojects?\b", text):
        # Count bullet points after a "Projects" heading
        match = re.search(r"(?i)(?:^|\n)\s*projects?\s*[:\n](.+?)(?:\n\s*\n|\Z)", text, re.DOTALL)
        if match:
            bullets = re.findall(r"(?m)^\s*[•\-\*]\s+.{15,}", match.group(1))
            count = max(count, len(bullets))
    return max(count, 0)


def _count_certifications(text: str) -> int:
    """Count certification mentions in resume text."""
    cert_patterns = [
        r"(?i)\b(?:certified|certification|certificate)\b",
        r"(?i)\b(?:aws|azure|gcp|google|cisco|comptia|pmp|cissp|ceh|cisa)\s+(?:certified|cert\.?)\b",
        r"(?i)\b(?:CISSP|CEH|CCNA|CCNP|CISA|PMP|AWS\s+SAA|CKA|CKAD|CompTIA\s+Security\+)\b",
    ]
    total = 0
    for pat in cert_patterns:
        total += len(re.findall(pat, text))
    # Deduplicate roughly
    return min(total, 15)


class FeatureExtractor:
    """
    Extracts a structured feature vector from a resume + JD pair.

    Can optionally use SemanticEncoder for embedding-based features.
    When encoder is not available, semantic features default to 0.0.
    """

    def __init__(self, encoder=None, nlp_engine=None):
        """
        Args:
            encoder: Optional SemanticEncoder instance for embedding features.
            nlp_engine: Optional NLPEngine instance for skill/experience extraction.
        """
        self.encoder = encoder
        self.nlp_engine = nlp_engine

    def _get_nlp_engine(self):
        """Lazily initialize NLPEngine if not provided."""
        if self.nlp_engine is None:
            from resume_scanner.nlp_engine import NLPEngine
            self.nlp_engine = NLPEngine(use_spacy=False)
        return self.nlp_engine

    def extract(
        self,
        resume_text: str,
        jd_text: str,
        jd_required_skills: Optional[List[str]] = None,
        jd_preferred_skills: Optional[List[str]] = None,
        jd_experience_years: Optional[float] = None,
        jd_education_required: Optional[List[str]] = None,
        resume_sections: Optional[Dict[str, str]] = None,
        jd_sections: Optional[Dict[str, str]] = None,
    ) -> Dict[str, float]:
        """
        Extract a complete feature vector from a resume + JD pair.

        Args:
            resume_text: Full resume text.
            jd_text: Full job description text.
            jd_required_skills: List of required skills from JD analysis.
            jd_preferred_skills: List of preferred skills from JD analysis.
            jd_experience_years: Required experience years from JD.
            jd_education_required: Education requirements from JD.
            resume_sections: Optional pre-extracted resume sections.
            jd_sections: Optional pre-extracted JD sections.

        Returns:
            Dict with all feature names from FEATURE_SCHEMA mapped to float values.
        """
        features: Dict[str, float] = {}
        nlp = self._get_nlp_engine()

        # ── Lexical features ──────────────────────────────────────────────
        features["tfidf_cosine_similarity"] = _tfidf_cosine(resume_text, jd_text)
        features["keyword_overlap_ratio"] = _keyword_overlap(resume_text, jd_text)

        # Skill-based keyword coverage
        resume_skills_dict = nlp.extract_skills(resume_text)
        resume_skills_flat = set(
            s.lower() for cat in resume_skills_dict.values() for s in cat
        )
        resume_lower = resume_text.lower()

        def _has_skill(skill_name: str) -> bool:
            s_low = skill_name.lower()
            return s_low in resume_skills_flat or bool(
                re.search(rf"\b{re.escape(s_low)}\b", resume_lower)
            )

        jd_required = jd_required_skills or []
        jd_preferred = jd_preferred_skills or []

        matched_req = [s for s in jd_required if _has_skill(s)]
        matched_pref = [s for s in jd_preferred if _has_skill(s)]

        features["required_keyword_coverage"] = (
            len(matched_req) / len(jd_required) if jd_required else 0.5
        )
        features["preferred_keyword_coverage"] = (
            len(matched_pref) / len(jd_preferred) if jd_preferred else 0.5
        )

        # ── Semantic features ─────────────────────────────────────────────
        if self.encoder is not None and resume_sections and jd_sections:
            try:
                section_sims = self.encoder.section_similarity(
                    resume_sections, jd_sections
                )
                features["full_doc_embedding_similarity"] = section_sims.get(
                    "full_document", 0.0
                )
                features["experience_responsibilities_sim"] = section_sims.get(
                    "experience_responsibilities", 0.0
                )
                features["skills_requirements_sim"] = section_sims.get(
                    "skills_required_skills", 0.0
                )
                features["projects_responsibilities_sim"] = section_sims.get(
                    "projects_responsibilities", 0.0
                )
                features["summary_job_summary_sim"] = section_sims.get(
                    "summary_job_summary", 0.0
                )
            except Exception as e:
                logger.warning("Semantic feature extraction failed: %s", e)
                for key in [
                    "full_doc_embedding_similarity",
                    "experience_responsibilities_sim",
                    "skills_requirements_sim",
                    "projects_responsibilities_sim",
                    "summary_job_summary_sim",
                ]:
                    features[key] = 0.0
        elif self.encoder is not None:
            # No sections provided — compute full-document similarity only
            try:
                features["full_doc_embedding_similarity"] = max(
                    0.0, self.encoder.similarity(resume_text, jd_text)
                )
            except Exception:
                features["full_doc_embedding_similarity"] = 0.0
            for key in [
                "experience_responsibilities_sim",
                "skills_requirements_sim",
                "projects_responsibilities_sim",
                "summary_job_summary_sim",
            ]:
                features[key] = 0.0
        else:
            # No encoder available
            for key in [
                "full_doc_embedding_similarity",
                "experience_responsibilities_sim",
                "skills_requirements_sim",
                "projects_responsibilities_sim",
                "summary_job_summary_sim",
            ]:
                features[key] = 0.0

        # ── Resume profile features ───────────────────────────────────────
        exp_years, exp_entries = nlp.calculate_experience_years(resume_text)
        features["years_of_experience"] = float(exp_years)
        features["num_skills"] = float(
            sum(len(v) for v in resume_skills_dict.values())
        )
        features["num_relevant_skills"] = float(len(matched_req) + len(matched_pref))
        features["num_projects"] = float(_count_projects(resume_text))
        features["num_experience_entries"] = float(len(exp_entries))
        features["education_level"] = float(_encode_education_level(resume_text))
        features["certification_count"] = float(_count_certifications(resume_text))

        # Achievement density from bullet analysis
        try:
            bullet_analysis = nlp.analyze_bullet_points(resume_text)
            total_bullets = bullet_analysis.get("total_bullets", 0)
            metric_bullets = bullet_analysis.get("bullets_with_metrics", 0)
            features["achievement_density"] = (
                metric_bullets / total_bullets if total_bullets > 0 else 0.0
            )
        except Exception:
            features["achievement_density"] = 0.0

        # ── JD profile features ───────────────────────────────────────────
        features["required_skill_count"] = float(len(jd_required))
        features["preferred_skill_count"] = float(len(jd_preferred))
        features["required_experience_years"] = float(
            jd_experience_years if jd_experience_years is not None else 0.0
        )
        features["education_requirement_level"] = float(
            _encode_education_level(
                " ".join(jd_education_required) if jd_education_required else ""
            )
        )

        # ── Alignment features ────────────────────────────────────────────
        features["experience_gap"] = (
            features["years_of_experience"] - features["required_experience_years"]
        )
        features["skill_gap"] = float(len(jd_required) - len(matched_req))
        features["education_match"] = float(
            1.0
            if features["education_level"] >= features["education_requirement_level"]
            else 0.0
        )
        features["required_skill_coverage"] = features["required_keyword_coverage"]
        features["preferred_skill_coverage"] = features["preferred_keyword_coverage"]

        # Validate schema
        for key in FEATURE_SCHEMA:
            if key not in features:
                features[key] = 0.0

        return features

    def extract_vector(
        self,
        resume_text: str,
        jd_text: str,
        **kwargs,
    ) -> List[float]:
        """
        Extract features and return as an ordered list matching FEATURE_SCHEMA.

        Returns:
            List of float values in FEATURE_SCHEMA order.
        """
        feat_dict = self.extract(resume_text, jd_text, **kwargs)
        return [feat_dict.get(key, 0.0) for key in FEATURE_SCHEMA]
