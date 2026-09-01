"""
Semantic Encoder Module
Provides sentence-level embeddings using a lightweight local Sentence-Transformer model.

Uses all-MiniLM-L6-v2 (384-dimensional embeddings, ~80MB model) for:
  - Full-document similarity
  - Section-aware resume ↔ JD matching
  - Feature inputs to the ML classifier

The model runs locally on CPU without any API key or internet access after first download.
"""

import logging
from typing import Dict, List, Optional, Union

import numpy as np

logger = logging.getLogger(__name__)

# ── Lazy singleton ────────────────────────────────────────────────────────────
_ENCODER_INSTANCE: Optional["SemanticEncoder"] = None

DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# Section mapping: resume section name → JD section it should be compared against
SECTION_ALIGNMENT = {
    "experience": "responsibilities",
    "skills": "required_skills",
    "projects": "responsibilities",
    "summary": "job_summary",
    "education": "education_requirements",
}


def get_encoder(model_name: str = DEFAULT_MODEL_NAME) -> "SemanticEncoder":
    """Return the singleton SemanticEncoder instance, creating it on first call."""
    global _ENCODER_INSTANCE
    if _ENCODER_INSTANCE is None or _ENCODER_INSTANCE.model_name != model_name:
        _ENCODER_INSTANCE = SemanticEncoder(model_name=model_name)
    return _ENCODER_INSTANCE


class SemanticEncoder:
    """
    Wraps a SentenceTransformer model for generating text embeddings.

    Features:
      - Singleton access via get_encoder() for efficient reuse
      - Section-aware encoding for structured resume ↔ JD comparison
      - CPU-only execution, no GPU required
      - Graceful error handling throughout
    """

    def __init__(self, model_name: str = DEFAULT_MODEL_NAME):
        from sentence_transformers import SentenceTransformer

        self.model_name = model_name
        logger.info("Loading SentenceTransformer model: %s", model_name)
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        logger.info(
            "Model loaded successfully (embedding dim: %d)", self.embedding_dim
        )

    def encode_text(self, text: str) -> np.ndarray:
        """
        Encode a single text string into a dense embedding vector.

        Args:
            text: Input text to encode.

        Returns:
            1-D numpy array of shape (embedding_dim,).
        """
        if not text or not text.strip():
            return np.zeros(self.embedding_dim, dtype=np.float32)

        # Truncate very long text to avoid OOM (model max is ~512 tokens ≈ ~2000 chars)
        truncated = text[:8000]
        embedding = self.model.encode(truncated, show_progress_bar=False)
        return np.asarray(embedding, dtype=np.float32)

    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """
        Encode a batch of text strings.

        Args:
            texts: List of text strings.

        Returns:
            2-D numpy array of shape (len(texts), embedding_dim).
        """
        if not texts:
            return np.zeros((0, self.embedding_dim), dtype=np.float32)

        clean_texts = [t[:8000] if t else "" for t in texts]
        embeddings = self.model.encode(clean_texts, show_progress_bar=False)
        return np.asarray(embeddings, dtype=np.float32)

    def encode_sections(
        self, sections: Dict[str, str]
    ) -> Dict[str, np.ndarray]:
        """
        Encode multiple named text sections.

        Args:
            sections: Dict mapping section names to their text content.
                      e.g. {"experience": "...", "skills": "...", ...}

        Returns:
            Dict mapping section names to their embedding vectors.
        """
        result = {}
        for name, text in sections.items():
            result[name] = self.encode_text(text)
        return result

    def similarity(self, text_a: str, text_b: str) -> float:
        """
        Compute cosine similarity between two texts.

        Args:
            text_a: First text.
            text_b: Second text.

        Returns:
            Cosine similarity score in range [-1, 1], typically [0, 1] for
            positive text embeddings.
        """
        if not text_a or not text_b:
            return 0.0

        emb_a = self.encode_text(text_a)
        emb_b = self.encode_text(text_b)
        return float(self._cosine_similarity(emb_a, emb_b))

    def section_similarity(
        self,
        resume_sections: Dict[str, str],
        jd_sections: Dict[str, str],
    ) -> Dict[str, float]:
        """
        Compute section-aware semantic similarity between resume and JD.

        Maps resume sections to their JD counterparts using SECTION_ALIGNMENT
        and computes pairwise cosine similarities.

        Args:
            resume_sections: Dict of resume section texts.
                             Keys: "experience", "skills", "projects", "summary", "education"
            jd_sections: Dict of JD section texts.
                         Keys: "responsibilities", "required_skills", "job_summary",
                               "education_requirements"

        Returns:
            Dict mapping alignment pair names to similarity scores.
            e.g. {"experience_responsibilities": 0.72, ...}
        """
        results = {}

        # Encode all sections
        resume_embeddings = self.encode_sections(resume_sections)
        jd_embeddings = self.encode_sections(jd_sections)

        for resume_key, jd_key in SECTION_ALIGNMENT.items():
            if resume_key in resume_embeddings and jd_key in jd_embeddings:
                sim = self._cosine_similarity(
                    resume_embeddings[resume_key],
                    jd_embeddings[jd_key],
                )
                pair_name = f"{resume_key}_{jd_key}"
                results[pair_name] = float(max(0.0, sim))  # Clamp to [0, 1]

        # Also compute full-document similarity if both have content
        all_resume_text = " ".join(
            t for t in resume_sections.values() if t
        )
        all_jd_text = " ".join(t for t in jd_sections.values() if t)
        if all_resume_text and all_jd_text:
            results["full_document"] = float(
                max(0.0, self.similarity(all_resume_text, all_jd_text))
            )

        return results

    @staticmethod
    def _cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        """Compute cosine similarity between two vectors."""
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))
