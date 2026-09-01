"""
ATS Scorer Module - Production-Grade Edition
Calculates explainable ATS (Applicant Tracking System) compatibility scores
based on measurable formatting, section completeness, keyword alignment,
quantifiable achievements, and contact completeness.
"""

import re
from typing import Dict, List, Optional, Any

from .config import ATSScoringConfig, DEFAULT_ATS_CONFIG
from .nlp_engine import NLPEngine


class ATSScorer:
    """
    Analyzes resumes for ATS parseability, structure, and keyword relevance.
    Provides explainable scoring and ethical improvement recommendations.
    """

    # Critical sections that ATS systems parse
    REQUIRED_SECTIONS = {
        "contact": ["email", "phone", "linkedin", "address", "contact"],
        "experience": [
            "experience",
            "work history",
            "employment",
            "career",
            "professional experience",
        ],
        "education": [
            "education",
            "academic",
            "degree",
            "university",
            "college",
            "qualification",
        ],
        "skills": [
            "skills",
            "technical skills",
            "competencies",
            "expertise",
            "proficiencies",
        ],
    }

    OPTIONAL_SECTIONS = {
        "summary": ["summary", "objective", "profile", "about me", "career objective"],
        "projects": ["projects", "portfolio", "personal projects", "academic projects"],
        "certifications": ["certifications", "certificates", "licenses", "credentials"],
        "achievements": ["achievements", "awards", "honors", "accomplishments"],
        "publications": ["publications", "papers", "research"],
    }

    # Common ATS-friendly keywords by role
    ROLE_KEYWORDS = {
        "data_scientist": [
            "python",
            "r",
            "sql",
            "machine learning",
            "deep learning",
            "statistics",
            "data analysis",
            "visualization",
            "tensorflow",
            "pytorch",
            "pandas",
            "numpy",
            "scikit-learn",
            "nlp",
            "computer vision",
            "a/b testing",
            "feature engineering",
            "model deployment",
            "aws",
            "gcp",
            "azure",
        ],
        "data_analyst": [
            "sql",
            "excel",
            "tableau",
            "power bi",
            "python",
            "r",
            "statistics",
            "data visualization",
            "reporting",
            "dashboards",
            "etl",
            "data cleaning",
            "business intelligence",
            "analytics",
            "kpi",
            "metrics",
        ],
        "ml_engineer": [
            "python",
            "tensorflow",
            "pytorch",
            "docker",
            "kubernetes",
            "mlops",
            "machine learning",
            "deep learning",
            "model deployment",
            "aws",
            "gcp",
            "ci/cd",
            "feature store",
            "model monitoring",
            "api",
            "microservices",
        ],
        "software_engineer": [
            "python",
            "java",
            "javascript",
            "c++",
            "git",
            "agile",
            "scrum",
            "api",
            "rest",
            "microservices",
            "docker",
            "kubernetes",
            "ci/cd",
            "testing",
            "debugging",
            "sql",
            "nosql",
            "system design",
        ],
        "frontend_developer": [
            "javascript",
            "typescript",
            "react",
            "vue",
            "angular",
            "html",
            "css",
            "responsive design",
            "ui/ux",
            "webpack",
            "npm",
            "git",
            "testing",
            "accessibility",
            "performance optimization",
        ],
        "backend_developer": [
            "python",
            "java",
            "node.js",
            "go",
            "sql",
            "nosql",
            "api",
            "rest",
            "microservices",
            "docker",
            "kubernetes",
            "aws",
            "database design",
            "caching",
            "message queues",
            "security",
        ],
        "cybersecurity_analyst": [
            "cybersecurity",
            "network security",
            "penetration testing",
            "ethical hacking",
            "siem",
            "splunk",
            "wireshark",
            "metasploit",
            "burp suite",
            "firewall",
            "incident response",
            "vulnerability assessment",
            "cryptography",
            "owasp",
            "linux",
            "python",
            "bash",
            "zero trust",
            "threat intelligence",
            "soc",
            "cissp",
            "compliance",
        ],
        "cybersecurity": [
            "cybersecurity",
            "network security",
            "penetration testing",
            "ethical hacking",
            "siem",
            "splunk",
            "wireshark",
            "metasploit",
            "burp suite",
            "firewall",
            "incident response",
            "vulnerability assessment",
            "cryptography",
            "owasp",
            "linux",
            "python",
            "bash",
            "zero trust",
            "threat intelligence",
            "soc",
            "cissp",
            "compliance",
        ],
        "web_developer": [
            "javascript",
            "typescript",
            "html",
            "css",
            "react",
            "next.js",
            "node.js",
            "express",
            "rest",
            "api",
            "graphql",
            "tailwind",
            "git",
            "responsive design",
            "webpack",
            "frontend",
            "backend",
            "sql",
            "mongodb",
            "ui/ux",
        ],
    }

    def __init__(self, config: Optional[ATSScoringConfig] = None):
        self.config = config or DEFAULT_ATS_CONFIG
        self.scores: Dict[str, float] = {}
        self.feedback: List[str] = []
        self.stuffing_warnings: List[str] = []
        self.nlp = NLPEngine(use_spacy=False)

    def calculate_score(self, text: str, target_role: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculate comprehensive ATS score with explainable breakdown.
        """
        self.feedback = []
        self.stuffing_warnings = []
        text_lower = text.lower()

        # Calculate individual category scores
        section_score = self._score_sections(text_lower)
        format_score = self._score_formatting(text)
        keyword_score = self._score_keywords(text_lower, target_role)
        achievements_score = self._score_achievements(text)
        length_score = self._score_length(text)
        readability_score = self._score_readability(text)
        contact_score = self._score_contact_info(text)

        weights = self.config.weights
        w_sections = weights.get("sections", 0.20)
        w_formatting = weights.get("formatting", 0.15)
        w_keywords = weights.get("keywords", 0.25)
        w_achievements = weights.get("achievements", 0.15)
        w_readability = weights.get("readability", 0.10)
        w_contact = weights.get("contact", 0.15)

        total_weight = w_sections + w_formatting + w_keywords + w_achievements + w_readability + w_contact
        raw_total = (
            section_score * w_sections
            + format_score * w_formatting
            + keyword_score * w_keywords
            + achievements_score * w_achievements
            + readability_score * w_readability
            + contact_score * w_contact
        ) / max(total_weight, 0.01)

        total_score = max(0.0, min(100.0, raw_total))

        self.scores = {
            "total": round(total_score, 1),
            "sections": round(section_score, 1),
            "formatting": round(format_score, 1),
            "keywords": round(keyword_score, 1),
            "achievements": round(achievements_score, 1),
            "length": round(length_score, 1),
            "readability": round(readability_score, 1),
            "contact": round(contact_score, 1),
        }

        return {
            "scores": self.scores,
            "feedback": self.feedback,
            "grade": self._get_grade(total_score),
            "pass_ats": total_score >= self.config.pass_threshold,
            "stuffing_warnings": self.stuffing_warnings,
            "disclaimer": (
                "Analytical estimate based on ATS formatting and keyword alignment heuristics. "
                "Real employer ATS systems vary."
            ),
        }

    def _score_sections(self, text: str) -> float:
        """Score based on presence of required and optional sections."""
        score = 0.0
        max_score = 100.0

        required_found = 0
        for section, keywords in self.REQUIRED_SECTIONS.items():
            found = any(kw in text for kw in keywords)
            if found:
                required_found += 1
            else:
                self.feedback.append(f"⚠️ Missing required section: {section.title()}")

        score += (required_found / len(self.REQUIRED_SECTIONS)) * 60.0

        optional_found = 0
        for section, keywords in self.OPTIONAL_SECTIONS.items():
            found = any(kw in text for kw in keywords)
            if found:
                optional_found += 1

        score += (optional_found / len(self.OPTIONAL_SECTIONS)) * 40.0

        if required_found == len(self.REQUIRED_SECTIONS):
            self.feedback.append("✅ All essential resume sections present")

        return min(score, max_score)

    def _score_formatting(self, text: str) -> float:
        """Score based on formatting hygiene for ATS parsers."""
        score = 100.0
        issues = []

        # Excessive special characters
        special_chars = len(re.findall(r"[^\w\s\.\,\;\:\-\+\@\#\(\)\/\&]", text))
        if special_chars > 60:
            score -= 15.0
            issues.append("High density of non-standard symbols may confuse legacy parsers")

        # Bullet point consistency
        bullet_patterns = [r"•", r"○", r"■", r"►", r"\*", r"-"]
        bullet_types = sum(1 for p in bullet_patterns if re.search(p, text))
        if bullet_types > 3:
            score -= 10.0
            issues.append("Multiple conflicting bullet point symbols detected")

        # Excessive all-caps words
        all_caps_words = len(re.findall(r"\b[A-Z]{5,}\b", text))
        if all_caps_words > 12:
            score -= 10.0
            issues.append("Excessive use of ALL CAPS text")

        # Table-like ASCII markers
        if re.search(r"\|.*\|.*\|", text):
            score -= 10.0
            issues.append("Table-like formatting detected (some ATS parsers struggle to read table flow)")

        if not issues:
            self.feedback.append("✅ Clean formatting compatible with standard ATS parsers")
        else:
            for issue in issues:
                self.feedback.append(f"⚠️ {issue}")

        return max(score, 0.0)

    def _score_keywords(self, text: str, target_role: Optional[str] = None) -> float:
        """Score keyword relevance with keyword stuffing detection and diminishing returns."""
        if not target_role:
            target_role = self._detect_role(text)

        target_role = target_role.lower().replace(" ", "_").replace("-", "_")
        if target_role not in self.ROLE_KEYWORDS:
            target_role = "data_scientist"

        keywords = self.ROLE_KEYWORDS[target_role]
        words = text.split()
        total_words = max(len(words), 1)

        found_keywords = []
        missing_keywords = []

        # Count keyword occurrences to detect stuffing
        stuffing_found = False
        for keyword in keywords:
            kw_pattern = rf"\b{re.escape(keyword.lower())}\b"
            matches = len(re.findall(kw_pattern, text))
            if matches > 0:
                found_keywords.append(keyword)
                ratio = matches / total_words
                if matches >= self.config.keyword_stuffing_count_threshold and ratio >= self.config.keyword_stuffing_ratio_threshold:
                    stuffing_found = True
                    warn_msg = f"Keyword '{keyword}' appears {matches} times ({ratio*100:.1f}% of text). Repeated keywords offer diminishing ATS returns."
                    self.stuffing_warnings.append(warn_msg)
            else:
                missing_keywords.append(keyword)

        # Baseline coverage of unique role keywords (no points for repeating the same word)
        unique_coverage = (len(found_keywords) / len(keywords)) * 100.0

        # Apply stuffing penalty if detected
        if stuffing_found:
            unique_coverage = max(30.0, unique_coverage - 15.0)
            self.feedback.append("⚠️ Keyword repetition detected. Natural phrasing is preferred by recruiters and modern ATS.")
        else:
            if found_keywords:
                self.feedback.append(f"✅ Found {len(found_keywords)}/{len(keywords)} role-relevant keywords")

        # Ethical phrasing following Rule 17
        if missing_keywords[:4]:
            top_missing = ", ".join([k.title() for k in missing_keywords[:4]])
            self.feedback.append(
                f"💡 If you genuinely have experience with {top_missing}, consider highlighting them in your experience bullets."
            )

        return min(unique_coverage, 100.0)

    def _score_achievements(self, text: str) -> float:
        """Score based on quantifiable achievements and metrics in experience bullets."""
        analysis = self.nlp.analyze_bullet_points(text)
        total_bullets = analysis.get("total_bullets", 0)
        metric_pct = analysis.get("metric_percentage", 0.0)

        if total_bullets == 0:
            score = 60.0
            self.feedback.append("💡 Consider structuring work history with clear bullet points.")
        elif metric_pct >= 50.0:
            score = 100.0
            self.feedback.append(f"✅ Strong achievement metrics ({metric_pct:.0f}% of bullets contain measurable outcomes)")
        elif metric_pct >= 30.0:
            score = 80.0
            self.feedback.append(f"✅ Good presence of measurable metrics ({metric_pct:.0f}% of bullets)")
        elif metric_pct >= 15.0:
            score = 65.0
            self.feedback.append("💡 If available, consider adding measurable outcomes (e.g. scale, % gains, time saved) to more bullets.")
        else:
            score = 50.0
            self.feedback.append("💡 Most bullets lack quantifiable outcomes. Where possible, show measurable impact.")

        return score

    def _score_length(self, text: str) -> float:
        """Score based on resume word count."""
        word_count = len(text.split())
        min_opt = self.config.optimal_word_count_min
        max_opt = self.config.optimal_word_count_max

        if min_opt <= word_count <= max_opt:
            score = 100.0
            self.feedback.append("✅ Resume length is optimal (1-2 pages)")
        elif (min_opt - 100) <= word_count < min_opt or max_opt < word_count <= (max_opt + 200):
            score = 80.0
            self.feedback.append("⚠️ Resume length is acceptable but could be adjusted")
        elif word_count < (min_opt - 100):
            score = 60.0
            self.feedback.append("⚠️ Resume may be too brief — provide more depth on key projects")
        else:
            score = 65.0
            self.feedback.append("⚠️ Resume is quite long — consider condensing older roles")

        return score

    def _score_readability(self, text: str) -> float:
        """Score based on sentence length and active voice."""
        score = 100.0
        words = text.split()
        sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]

        if not sentences:
            return 60.0

        avg_len = len(words) / len(sentences)
        if avg_len > 28:
            score -= 15.0
            self.feedback.append("⚠️ Sentences are somewhat long — consider breaking them into concise bullets")
        elif avg_len < 8:
            score -= 10.0

        # Passive voice check
        passive_indicators = {"was", "were", "been", "being", "is", "are"}
        passive_count = sum(1 for w in words if w.lower() in passive_indicators)
        if (passive_count / max(len(words), 1)) > 0.07:
            score -= 10.0
            self.feedback.append("💡 Active voice: Begin bullets with strong action verbs rather than passive constructions")

        return max(score, 0.0)

    def _score_contact_info(self, text: str) -> float:
        """Score based on contact details completeness."""
        score = 0.0

        # Email
        if re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", text):
            score += 30.0
        else:
            self.feedback.append("❌ No email address found")

        # Phone
        if re.search(r"(?:\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b", text):
            score += 25.0
        else:
            self.feedback.append("⚠️ No phone number found")

        # LinkedIn
        if re.search(r"linkedin\.com/in/", text, re.IGNORECASE) or "linkedin" in text.lower():
            score += 25.0
        else:
            self.feedback.append("💡 Consider adding a LinkedIn profile link")

        # GitHub or Portfolio
        if re.search(r"github|portfolio|website|\.dev|\.io", text, re.IGNORECASE):
            score += 20.0
        else:
            self.feedback.append("💡 Consider adding a GitHub, portfolio, or personal website link")

        return min(score, 100.0)

    def _detect_role(self, text: str) -> str:
        """Auto-detect the target role from resume content."""
        role_scores = {}
        for role, keywords in self.ROLE_KEYWORDS.items():
            matches = sum(1 for kw in keywords if re.search(rf"\b{re.escape(kw.lower())}\b", text))
            role_scores[role] = matches

        if role_scores:
            return max(role_scores, key=role_scores.get)
        return "software_engineer"

    def _get_grade(self, score: float) -> str:
        """Convert numerical score to letter grade."""
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C+"
        elif score >= 55:
            return "C"
        elif score >= 50:
            return "C-"
        elif score >= 45:
            return "D"
        return "F"

    def get_improvement_suggestions(self) -> List[str]:
        """Get prioritized list of improvement recommendations."""
        suggestions = []

        if self.scores.get("contact", 0) < 75:
            suggestions.append(
                "High Priority: Ensure your contact header has an email, phone number, and LinkedIn URL."
            )
        if self.scores.get("sections", 0) < 75:
            suggestions.append(
                "High Priority: Include all core resume sections: Work Experience, Education, and Skills."
            )
        if self.scores.get("achievements", 0) < 70:
            suggestions.append(
                "Medium Priority: Quantify bullet points where possible with measurable outcomes (% increase, time saved, scale)."
            )
        if self.scores.get("keywords", 0) < 65:
            suggestions.append(
                "Medium Priority: If you have experience with industry-standard tools in your field, consider explicitly mentioning them."
            )
        if self.scores.get("formatting", 0) < 75:
            suggestions.append(
                "Low Priority: Keep formatting simple with standard bullet symbols and clean text hierarchies."
            )

        return suggestions
