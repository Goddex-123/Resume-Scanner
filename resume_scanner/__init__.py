"""
Resume Scanner - AI-Powered Resume Analysis System
A comprehensive toolkit for analyzing resumes using NLP and Machine Learning.
"""

from .parser import ResumeParser, ResumeDocument
from .nlp_engine import NLPEngine
from .ats_scorer import ATSScorer
from .ai_detector import AIDetector
from .job_matcher import JobMatcher
from .jd_analyzer import JobDescriptionAnalyzer, JobDescription
from .config import ParserConfig, ATSScoringConfig, JobMatchingConfig

__version__ = "2.0.0"
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
]
