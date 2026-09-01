"""
Resume Scanner - AI-Powered Resume Analysis System
A comprehensive toolkit for analyzing resumes using NLP, Semantic Embeddings, and Machine Learning.
"""

from .parser import ResumeParser, ResumeDocument
from .nlp_engine import NLPEngine
from .ats_scorer import ATSScorer
from .ai_detector import AIDetector
from .job_matcher import JobMatcher
from .jd_analyzer import JobDescriptionAnalyzer, JobDescription
from .config import ParserConfig, ATSScoringConfig, JobMatchingConfig, HybridMatchingConfig

__version__ = "3.0.0"
__author__ = "Soham"

__all__ = [
    "ResumeParser",
    "ResumeDocument",
    "NLPEngine",
    "ATSScorer",
    "AIDetector",
    "JobMatcher",
    "JobDescriptionAnalyzer",
    "JobDescription",
    "ParserConfig",
    "ATSScoringConfig",
    "JobMatchingConfig",
    "HybridMatchingConfig",
]

# ── Conditional ML exports ────────────────────────────────────────────────────
# These are only available when sentence-transformers and torch are installed.
try:
    from .ml import ML_AVAILABLE, SemanticEncoder, FeatureExtractor, HybridMatcher, get_encoder

    if ML_AVAILABLE:
        __all__.extend([
            "ML_AVAILABLE",
            "SemanticEncoder",
            "FeatureExtractor",
            "HybridMatcher",
            "get_encoder",
        ])
except ImportError:
    ML_AVAILABLE = False
