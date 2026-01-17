"""
AI Content Detection Module
Analyzes text to detect AI-generated content in resumes.
"""

import re
import math
from typing import Dict, List
from collections import Counter


class AIDetector:
    """Detects potential AI-generated content in resumes."""
    
    AI_PHRASES = [
        'leveraging cutting-edge', 'spearheaded initiatives', 'drove strategic',
        'fostered collaborative', 'orchestrated seamless', 'catalyzed growth',
        'synergized efforts', 'pioneered innovative', 'championed digital',
        'cultivated relationships', 'streamlined operations', 'optimized workflows',
        'passionate about', 'dedicated professional', 'results-driven',
        'detail-oriented', 'highly motivated', 'proven track record'
    ]
    
    OVERUSED_VERBS = [
        'leveraged', 'spearheaded', 'orchestrated', 'synergized', 'catalyzed',
        'pioneered', 'championed', 'cultivated', 'revolutionized', 'transformed'
    ]
    
    def __init__(self):
        self.analysis_results = {}
    
    def analyze(self, text: str) -> Dict:
        """Analyze text for AI-generated content."""
        text_lower = text.lower()
        
        phrase_score = self._check_ai_phrases(text_lower)
        verb_score = self._check_overused_verbs(text_lower)
        ttr_score = self._calculate_ttr(text)
        repetition_score = self._check_repetition(text)
        
        ai_probability = (phrase_score * 0.3 + verb_score * 0.2 + 
                         (100 - ttr_score) * 0.25 + repetition_score * 0.25)
        ai_probability = max(0, min(100, ai_probability))
        
        self.analysis_results = {
            'ai_probability': round(ai_probability, 1),
            'confidence': self._get_confidence(ai_probability),
            'verdict': self._get_verdict(ai_probability),
            'detailed_scores': {
                'ai_phrases': round(phrase_score, 1),
                'overused_verbs': round(verb_score, 1),
                'vocabulary_diversity': round(ttr_score, 1),
                'repetition': round(repetition_score, 1)
            },
            'flags': self._get_flags(text_lower)
        }
        return self.analysis_results
    
    def _check_ai_phrases(self, text: str) -> float:
        found = sum(1 for p in self.AI_PHRASES if p in text)
        if found >= 6: return 90
        elif found >= 4: return 70
        elif found >= 2: return 45
        elif found >= 1: return 25
        return 10
    
    def _check_overused_verbs(self, text: str) -> float:
        found = sum(1 for v in self.OVERUSED_VERBS if v in text)
        if found >= 5: return 85
        elif found >= 3: return 60
        elif found >= 1: return 30
        return 10
    
    def _calculate_ttr(self, text: str) -> float:
        words = re.findall(r'\b[a-z]+\b', text.lower())
        if len(words) < 50: return 50
        ttr = len(set(words)) / len(words)
        return max(0, min(100, (ttr - 0.3) / 0.4 * 100))
    
    def _check_repetition(self, text: str) -> float:
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 20]
        if len(sentences) < 5: return 30
        starts = [s.split()[0].lower() for s in sentences if s.split()]
        max_same = max(Counter(starts).values()) if starts else 0
        return min(100, (max_same / len(sentences)) * 100)
    
    def _get_confidence(self, prob: float) -> str:
        if prob >= 70: return "High"
        elif prob >= 45: return "Medium"
        return "Low"
    
    def _get_verdict(self, prob: float) -> str:
        if prob >= 70: return "Likely AI-Generated"
        elif prob >= 45: return "Possibly AI-Assisted"
        elif prob >= 25: return "Mixed Human/AI"
        return "Likely Human-Written"
    
    def _get_flags(self, text: str) -> List[str]:
        flags = []
        ai_found = [p for p in self.AI_PHRASES if p in text]
        if ai_found:
            flags.append(f"Found {len(ai_found)} AI-style phrases")
        verb_found = [v for v in self.OVERUSED_VERBS if v in text]
        if len(verb_found) >= 3:
            flags.append(f"Overused buzzwords: {', '.join(verb_found[:3])}")
        return flags
