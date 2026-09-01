"""
Resume Scanner ML Package
Provides semantic embeddings, feature engineering, model training, and hybrid inference.

All ML components are optional — the core resume_scanner package works without them.
If sentence-transformers or torch is not installed, ML_AVAILABLE is set to False
and all ML-dependent functionality gracefully degrades.
"""

import logging

logger = logging.getLogger(__name__)

# ── Availability flag ─────────────────────────────────────────────────────────
ML_AVAILABLE = False

try:
    from .embeddings import SemanticEncoder, get_encoder
    from .features import FeatureExtractor
    from .inference import HybridMatcher

    ML_AVAILABLE = True
except ImportError as e:
    logger.info(
        "ML components not available (missing dependency: %s). "
        "Rule-based analysis will continue to work normally.",
        e,
    )

    # Provide None stubs so downstream code can check without AttributeError
    SemanticEncoder = None  # type: ignore[assignment,misc]
    FeatureExtractor = None  # type: ignore[assignment,misc]
    HybridMatcher = None  # type: ignore[assignment,misc]
    get_encoder = None  # type: ignore[assignment,misc]

__all__ = [
    "ML_AVAILABLE",
    "SemanticEncoder",
    "FeatureExtractor",
    "HybridMatcher",
    "get_encoder",
]
