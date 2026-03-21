"""
Resume Scanner - AI-Powered Resume Analysis System
A comprehensive toolkit for analyzing resumes using NLP and Machine Learning.
"""

from .parser import ResumeParser
from .nlp_engine import NLPEngine
from .ats_scorer import ATSScorer
from .ai_detector import AIDetector
from .job_matcher import JobMatcher

__version__ = "1.0.0"
__author__ = "Soham"

__all__ = [
    "ResumeParser",
    "NLPEngine", 
    "ATSScorer",
    "AIDetector",
    "JobMatcher"
]
