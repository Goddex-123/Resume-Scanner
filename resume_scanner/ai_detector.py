"""
AI Writing Signals & Authenticity Analysis Module
Evaluates resumes for generic buzzwords, repetitive structures, corporate clichés,
and lack of specificity using transparent, explainable heuristics.
NOTE: This is a writing-style heuristic indicator, NOT a scientifically validated AI detector.
"""

import re
from typing import Dict, List, Any
from collections import Counter


class AIDetector:
    """
    Analyzes resume text for AI-style writing clichés, corporate buzzwords,
    and structural uniformity to help candidates write more authentic, impactful resumes.
    """

    AI_PHRASES = [
        "leveraging cutting-edge",
        "cutting-edge technology",
        "spearheaded initiatives",
        "drove strategic",
        "fostered collaborative",
        "orchestrated seamless",
        "catalyzed growth",
        "synergized efforts",
        "pioneered innovative",
        "championed digital",
        "cultivated relationships",
        "streamlined operations",
        "optimized workflows",
        "passionate about",
        "dedicated professional",
        "results-driven professional",
        "results-driven",
        "detail-oriented",
        "highly motivated",
        "proven track record",
        "dynamic and visionary",
        "game-changing solutions",
        "seamless integration",
        "cross-functional synergy",
        "strategic vision",
        "holistic approach",
    ]

    OVERUSED_VERBS = [
        "leveraged",
        "spearheaded",
        "orchestrated",
        "synergized",
        "catalyzed",
        "pioneered",
        "championed",
        "cultivated",
        "revolutionized",
        "transformed",
        "fostered",
        "amplified",
    ]

    def __init__(self):
        self.analysis_results: Dict[str, Any] = {}

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for AI-style writing clichés, repetitive sentence structures,
        and specificity.
        """
        text_lower = text.lower()

        phrase_score, found_phrases = self._check_ai_phrases(text_lower)
        verb_score, found_verbs = self._check_overused_verbs(text_lower)
        ttr_score = self._calculate_ttr(text)
        repetition_score = self._check_repetition(text)
        specificity_score, generic_signals = self._check_specificity(text)

        # Composite heuristic score (0 - 100)
        # Higher score = higher density of AI-style corporate writing and repetitive patterns
        heuristic_score = (
            phrase_score * 0.30
            + verb_score * 0.20
            + (100.0 - ttr_score) * 0.20
            + repetition_score * 0.15
            + (100.0 - specificity_score) * 0.15
        )
        heuristic_score = max(0.0, min(100.0, round(heuristic_score, 1)))

        confidence = self._get_confidence(heuristic_score)
        verdict = self._get_verdict(heuristic_score)
        flags = self._get_flags(found_phrases, found_verbs, repetition_score, specificity_score)
        suggestions = self._get_suggestions(found_phrases, found_verbs, repetition_score, specificity_score)

        self.analysis_results = {
            # Backward-compatible keys
            "ai_probability": heuristic_score,
            "confidence": confidence,
            "verdict": verdict,
            "detailed_scores": {
                "ai_phrases": round(phrase_score, 1),
                "overused_verbs": round(verb_score, 1),
                "vocabulary_diversity": round(ttr_score, 1),
                "repetition": round(repetition_score, 1),
                "specificity": round(specificity_score, 1),
            },
            "flags": flags,
            # Enhanced transparent reporting
            "heuristic_score": heuristic_score,
            "signals_detected": {
                "cliche_phrases": found_phrases,
                "buzzword_verbs": found_verbs,
                "generic_signals": generic_signals,
            },
            "suggestions": suggestions,
            "disclaimer": (
                "Heuristic writing-style indicator analyzing buzzwords and phrasing patterns. "
                "This is NOT a scientifically validated AI detector and should not be treated as proof of authorship."
            ),
        }
        return self.analysis_results

    def _check_ai_phrases(self, text: str) -> tuple[float, List[str]]:
        found = [p for p in self.AI_PHRASES if p in text]
        count = len(found)
        if count >= 6:
            score = 90.0
        elif count >= 4:
            score = 70.0
        elif count >= 2:
            score = 45.0
        elif count >= 1:
            score = 25.0
        else:
            score = 10.0
        return score, found

    def _check_overused_verbs(self, text: str) -> tuple[float, List[str]]:
        found = [v for v in self.OVERUSED_VERBS if re.search(rf"\b{re.escape(v)}\b", text)]
        count = len(found)
        if count >= 5:
            score = 85.0
        elif count >= 3:
            score = 60.0
        elif count >= 1:
            score = 30.0
        else:
            score = 10.0
        return score, found

    def _calculate_ttr(self, text: str) -> float:
        words = re.findall(r"\b[a-z]+\b", text.lower())
        if len(words) < 50:
            return 50.0
        ttr = len(set(words)) / len(words)
        # Normalize into a 0 - 100 scale (healthy TTR for resumes is ~0.40 to 0.65)
        return max(0.0, min(100.0, (ttr - 0.25) / 0.40 * 100.0))

    def _check_repetition(self, text: str) -> float:
        sentences = [
            s.strip() for s in re.split(r"[.!?\n]+", text) if len(s.strip().split()) >= 4
        ]
        if len(sentences) < 5:
            return 25.0

        starts = [s.split()[0].lower().strip(",.;:") for s in sentences if s.split()]
        counts = Counter(starts)
        max_same = max(counts.values()) if counts else 0
        ratio = max_same / len(sentences)

        if ratio > 0.35:
            return min(100.0, ratio * 120.0)
        return min(100.0, ratio * 60.0)

    def _check_specificity(self, text: str) -> tuple[float, List[str]]:
        """Evaluate whether descriptions provide concrete metrics and technical nouns."""
        words = text.split()
        total_words = max(len(words), 1)

        # Numbers, percentages, scale indicators
        metrics_found = len(re.findall(r"(?:\d+(?:\.\d+)?%|\$\d+|\b\d+\+?\b)", text))
        density = (metrics_found / total_words) * 100.0

        generic_signals = []
        if density < 0.8:
            generic_signals.append("Low density of numerical metrics or concrete outcome figures")
        if re.search(r"(?i)\bresponsible for\b", text):
            generic_signals.append("Uses passive 'responsible for' instead of direct action verbs")

        score = min(100.0, max(20.0, density * 40.0 + 30.0))
        return score, generic_signals

    def _get_confidence(self, score: float) -> str:
        if score >= 70 or score <= 25:
            return "High"
        elif score >= 45:
            return "Medium"
        return "Moderate"

    def _get_verdict(self, score: float) -> str:
        if score >= 70:
            return "High AI Cliché Density"
        elif score >= 50:
            return "Moderate AI-Style Signals"
        elif score >= 30:
            return "Balanced Phrasing"
        return "Authentic & Specific"

    def _get_flags(
        self,
        found_phrases: List[str],
        found_verbs: List[str],
        repetition_score: float,
        specificity_score: float,
    ) -> List[str]:
        flags = []
        if found_phrases:
            top_p = ", ".join([f"'{p}'" for p in found_phrases[:3]])
            flags.append(f"Contains {len(found_phrases)} corporate clichés ({top_p})")
        if len(found_verbs) >= 3:
            flags.append(f"Overuses buzzword verbs: {', '.join(found_verbs[:3])}")
        if repetition_score > 50:
            flags.append("Multiple sentences begin with identical sentence starters")
        if specificity_score < 45:
            flags.append("Lacks quantifiable outcomes and concrete technical specifics")
        return flags

    def _get_suggestions(
        self,
        found_phrases: List[str],
        found_verbs: List[str],
        repetition_score: float,
        specificity_score: float,
    ) -> List[str]:
        suggestions = []
        if found_phrases:
            suggestions.append(
                "Replace generic buzzwords (e.g. 'results-driven', 'spearheaded initiatives') "
                "with the actual problem solved and tools utilized."
            )
        if len(found_verbs) >= 2:
            suggestions.append(
                "Vary your action verbs. Instead of 'leveraged' or 'orchestrated', use domain-specific "
                "verbs like 'Engineered', 'Architected', or 'Configured'."
            )
        if repetition_score > 40:
            suggestions.append(
                "Vary your sentence structure so consecutive bullet points do not all open with the "
                "exact same grammatical pattern."
            )
        if specificity_score < 50:
            suggestions.append(
                "Ground high-level claims with specific details (e.g., system scale, team size, tools, "
                "or percentage improvements achieved)."
            )
        return suggestions
