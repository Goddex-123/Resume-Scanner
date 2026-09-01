"""
Configuration Module for Resume Scanner.
Centralizes operational constants, scoring weights, file constraints, and defaults.
"""

from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class ParserConfig:
    """Configuration for document parsing and file validation."""

    supported_extensions: List[str] = field(
        default_factory=lambda: [".pdf", ".docx", ".txt"]
    )
    unsupported_legacy_extensions: List[str] = field(
        default_factory=lambda: [".doc"]
    )
    max_file_size_mb: int = 15
    max_file_size_bytes: int = 15 * 1024 * 1024
    min_extracted_text_length: int = 30
    scanned_pdf_char_threshold_per_page: int = 40


@dataclass
class ATSScoringConfig:
    """Configurable weights and thresholds for ATS scoring."""

    weights: Dict[str, float] = field(
        default_factory=lambda: {
            "sections": 0.20,
            "formatting": 0.15,
            "keywords": 0.25,
            "achievements": 0.15,
            "readability": 0.10,
            "contact": 0.15,
        }
    )
    # Threshold above which a keyword repetition is penalized (keyword stuffing)
    keyword_stuffing_ratio_threshold: float = 0.04
    keyword_stuffing_count_threshold: int = 8
    optimal_word_count_min: int = 350
    optimal_word_count_max: int = 900
    pass_threshold: float = 60.0


@dataclass
class JobMatchingConfig:
    """Configurable weights for Resume-to-Job Description matching."""

    weights: Dict[str, float] = field(
        default_factory=lambda: {
            "required_skills": 0.40,
            "preferred_skills": 0.20,
            "semantic_similarity": 0.20,
            "experience_alignment": 0.10,
            "education_alignment": 0.10,
        }
    )


# Default shared instances
DEFAULT_PARSER_CONFIG = ParserConfig()
DEFAULT_ATS_CONFIG = ATSScoringConfig()
DEFAULT_JOB_MATCHING_CONFIG = JobMatchingConfig()
