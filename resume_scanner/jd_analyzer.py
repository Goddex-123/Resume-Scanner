"""
Job Description Analyzer Module
Parses and structures job descriptions into required skills, preferred qualifications,
experience thresholds, and education expectations.
"""

import re
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field

from .nlp_engine import NLPEngine


@dataclass
class JobDescription:
    """Structured representation of a parsed job description."""

    title: str = ""
    raw_text: str = ""
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    all_skills: List[str] = field(default_factory=list)
    experience_years_required: Optional[float] = None
    education_required: List[str] = field(default_factory=list)
    responsibilities: List[str] = field(default_factory=list)
    domain_keywords: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class JobDescriptionAnalyzer:
    """
    Analyzes job descriptions to extract actionable hiring criteria.
    Differentiates between mandatory (Required) and optional (Preferred) qualifications.
    """

    def __init__(self, nlp_engine: Optional[NLPEngine] = None):
        self.nlp = nlp_engine or NLPEngine(use_spacy=False)

    def analyze(self, jd_text: str, title: str = "") -> JobDescription:
        """
        Parse raw job description text into structured JobDescription model.
        """
        clean_text = jd_text.strip()
        if not clean_text:
            return JobDescription(title=title, raw_text="")

        # 1. Section segregation
        sections = self._split_jd_sections(clean_text)

        # 2. Skill extraction across full text and specific sections
        full_skills_flat = self.nlp.get_all_skills_flat(clean_text)

        # Skills found in Required section vs Preferred section
        req_text = sections.get("required", "")
        pref_text = sections.get("preferred", "")

        required_skills: List[str] = []
        preferred_skills: List[str] = []

        if req_text or pref_text:
            if req_text:
                required_skills = self.nlp.get_all_skills_flat(req_text)
            if pref_text:
                preferred_skills = self.nlp.get_all_skills_flat(pref_text)

            # Avoid overlap: if a skill is in required, don't duplicate in preferred
            preferred_skills = [s for s in preferred_skills if s not in required_skills]

            # Any skills in the rest of the text that weren't assigned
            assigned = set(required_skills + preferred_skills)
            unassigned = [s for s in full_skills_flat if s not in assigned]

            # Contextual keyword tagging for unassigned skills
            for s in unassigned:
                if self._is_preferred_context(clean_text, s):
                    preferred_skills.append(s)
                else:
                    required_skills.append(s)
        else:
            # No explicit headings: use contextual cues
            for s in full_skills_flat:
                if self._is_preferred_context(clean_text, s):
                    preferred_skills.append(s)
                else:
                    required_skills.append(s)

        # 3. Experience requirements extraction
        exp_years = self._extract_experience_years(clean_text)

        # 4. Education requirements extraction
        education = self._extract_education_requirements(clean_text)

        # 5. Responsibilities
        responsibilities = self._extract_responsibilities(sections.get("responsibilities", clean_text))

        return JobDescription(
            title=title or self._infer_title(clean_text),
            raw_text=clean_text,
            required_skills=sorted(list(set(required_skills))),
            preferred_skills=sorted(list(set(preferred_skills))),
            all_skills=sorted(list(set(full_skills_flat))),
            experience_years_required=exp_years,
            education_required=education,
            responsibilities=responsibilities,
            domain_keywords=full_skills_flat[:10],
            metadata={"sections_detected": list(sections.keys())},
        )

    def _split_jd_sections(self, text: str) -> Dict[str, str]:
        """Split JD into required, preferred, and responsibilities sections."""
        lines = text.split("\n")
        sections: Dict[str, List[str]] = {"general": []}
        current_section = "general"

        header_patterns = {
            "required": r"(?i)^\s*(?:#+\s*)?(?:requirements?|required\s+qualifications?|minimum\s+qualifications?|basic\s+qualifications?|what\s+you\s+need|what\s+you['’]?ll\s+bring|must\s+haves?|qualifications?)\s*:?\s*$",
            "preferred": r"(?i)^\s*(?:#+\s*)?(?:preferred\s+qualifications?|nice\s+to\s+have|bonus\s+points?|plus|desired\s+qualifications?|preferred\s+skills?|what\s+would\s+be\s+great|preferred\s+experience)\s*:?\s*$",
            "responsibilities": r"(?i)^\s*(?:#+\s*)?(?:responsibilities|duties|what\s+you['’]?ll\s+do|key\s+responsibilities|role\s+overview|deliverables)\s*:?\s*$",
        }

        for line in lines:
            clean = line.strip()
            matched_header = False
            for sec_name, pattern in header_patterns.items():
                if re.match(pattern, clean):
                    current_section = sec_name
                    sections.setdefault(current_section, [])
                    matched_header = True
                    break

            if not matched_header:
                sections.setdefault(current_section, []).append(line)

        return {k: "\n".join(v).strip() for k, v in sections.items() if "\n".join(v).strip()}

    def _is_preferred_context(self, text: str, skill: str) -> bool:
        """Check if a skill appears in the vicinity of bonus/preferred modal words."""
        pattern = rf"(?i)(?:preferred|plus|bonus|nice to have|ideal|optional)[^.\n]{{0,60}}\b{re.escape(skill)}\b"
        return bool(re.search(pattern, text))

    def _extract_experience_years(self, text: str) -> Optional[float]:
        """Extract minimum years of required experience from JD text."""
        # e.g., "5+ years of experience", "minimum 3 years", "3-5 years"
        patterns = [
            r"(?i)\b(\d+)\+?\s*(?:to\s*\d+\+?)?\s*years?(?:\s+of)?(?:\s+(?:relevant|professional|hands-on|industry|software))?\s+experience",
            r"(?i)minimum\s+of\s+(\d+)\+?\s*years?",
            r"(?i)(\d+)\s*\+\s*years?",
        ]
        for pat in patterns:
            match = re.search(pat, text)
            if match:
                try:
                    return float(match.group(1))
                except (ValueError, IndexError):
                    continue
        return None

    def _extract_education_requirements(self, text: str) -> List[str]:
        """Identify degree and education expectations."""
        edu_patterns = [
            (r"(?i)\b(?:ph\.?d|doctorate)\b", "PhD"),
            (r"(?i)\b(?:master'?s?|m\.?s\.?|m\.?a\.?|mba)\b", "Master's Degree"),
            (r"(?i)\b(?:bachelor'?s?|b\.?s\.?|b\.?a\.?|undergraduate)\b", "Bachelor's Degree"),
            (r"(?i)\b(?:associate'?s?)\b", "Associate's Degree"),
        ]
        found = []
        for pat, label in edu_patterns:
            if re.search(pat, text):
                found.append(label)
        return found

    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract main duty bullets from responsibilities section."""
        bullets = []
        for line in text.split("\n"):
            clean = line.strip()
            if clean.startswith(("-", "*", "•", "–", "—")) or re.match(r"^\d+\.", clean):
                b = re.sub(r"^[-*•–—\d\.]+\s*", "", clean).strip()
                if len(b) > 15:
                    bullets.append(b)
        return bullets[:8]

    def _infer_title(self, text: str) -> str:
        """Infer target role title from the first lines of the JD."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        if lines:
            first = lines[0]
            if len(first) < 60 and not first.lower().startswith(("http", "about", "company", "we are")):
                return first
        return "Target Role"
