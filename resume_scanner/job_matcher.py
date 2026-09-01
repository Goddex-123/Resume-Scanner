"""
Job Matcher Module - Production-Grade Edition
Provides role benchmark matching and direct Resume ↔ Job Description analysis
using TF-IDF semantic similarity, required/preferred skill coverage, and experience alignment.
"""

import re
import math
from typing import Dict, List, Any, Optional
from collections import Counter

from .nlp_engine import NLPEngine
from .jd_analyzer import JobDescriptionAnalyzer
from .config import JobMatchingConfig, DEFAULT_JOB_MATCHING_CONFIG


class JobMatcher:
    """
    Matches resumes to suitable job roles and target job descriptions.
    Supports both benchmark role comparison and direct 1-to-1 Job Description evaluation.
    """

    JOB_DESCRIPTIONS = {
        "Data Scientist": """
            machine learning deep learning python r sql statistics data analysis
            tensorflow pytorch pandas numpy scikit-learn visualization modeling
            feature engineering model deployment nlp computer vision a/b testing
            jupyter notebook kaggle research algorithms neural networks
        """,
        "ML Engineer": """
            machine learning python tensorflow pytorch docker kubernetes mlops
            model deployment aws gcp azure ci/cd pipeline api microservices
            feature store model monitoring production engineering scalability
            deep learning infrastructure optimization performance
        """,
        "Data Analyst": """
            sql excel tableau power bi python r data visualization reporting
            dashboards analytics business intelligence kpi metrics etl
            data cleaning statistical analysis presentation stakeholders
        """,
        "Software Engineer": """
            python java javascript typescript c++ git agile scrum api rest
            microservices docker kubernetes ci/cd testing debugging sql nosql
            system design architecture backend frontend full stack development
        """,
        "Data Engineer": """
            python sql spark hadoop airflow etl pipeline data warehouse
            aws gcp azure bigquery snowflake redshift kafka streaming
            data modeling schema design optimization performance scalability
        """,
        "AI/ML Research": """
            research publications neural networks deep learning transformers
            nlp computer vision reinforcement learning pytorch tensorflow
            mathematics statistics algorithms optimization papers conference
        """,
        "Cybersecurity Analyst": """
            cybersecurity network security penetration testing ethical hacking
            firewalls siem incident response vulnerability assessment soc wireshark
            cryptography owasp compliance cissp comptia linux python bash
            threat intelligence zero trust vulnerability management intrusion detection
            splunk metasploit burp suite threat hunting security operations
        """,
        "Web Developer": """
            web development frontend backend javascript typescript html css react
            node.js express responsive design ui/ux rest api webpack tailwind git
            full stack next.js redux web performance accessibility graphql state management
            docker postgresql mongodb jest cypress agile component library
        """,
    }

    def __init__(self, config: Optional[JobMatchingConfig] = None):
        self.config = config or DEFAULT_JOB_MATCHING_CONFIG
        self.vocabulary = set()
        self.idf_scores = {}
        self._build_vocabulary()
        self.nlp = NLPEngine(use_spacy=False)
        self.jd_analyzer = JobDescriptionAnalyzer(self.nlp)

    def _build_vocabulary(self):
        """Build vocabulary from job descriptions."""
        all_words = []
        for desc in self.JOB_DESCRIPTIONS.values():
            words = self._tokenize(desc)
            all_words.extend(words)
            self.vocabulary.update(words)

        # Calculate IDF
        doc_count = len(self.JOB_DESCRIPTIONS)
        word_doc_freq = Counter()
        for desc in self.JOB_DESCRIPTIONS.values():
            words = set(self._tokenize(desc))
            for word in words:
                word_doc_freq[word] += 1

        for word in self.vocabulary:
            self.idf_scores[word] = math.log(doc_count / (1 + word_doc_freq[word]))

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        text = text.lower()
        words = re.findall(r"\b[a-z]+\b", text)
        return [w for w in words if len(w) > 2]

    def _calculate_tf(self, words: List[str]) -> Dict[str, float]:
        """Calculate term frequency."""
        word_counts = Counter(words)
        total = len(words)
        return {w: c / total for w, c in word_counts.items()}

    def _calculate_tfidf(self, text: str) -> Dict[str, float]:
        """Calculate TF-IDF vector for text."""
        words = self._tokenize(text)
        tf = self._calculate_tf(words)
        tfidf = {}
        for word, freq in tf.items():
            idf = self.idf_scores.get(word, 0)
            tfidf[word] = freq * idf
        return tfidf

    def _cosine_similarity(self, vec1: Dict, vec2: Dict) -> float:
        """Calculate cosine similarity between two vectors."""
        common_words = set(vec1.keys()) & set(vec2.keys())
        if not common_words:
            return 0.0

        dot_product = sum(vec1[w] * vec2[w] for w in common_words)
        mag1 = math.sqrt(sum(v**2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v**2 for v in vec2.values()))

        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot_product / (mag1 * mag2)

    # ─────────────────────────────────────────────────────────────────────────
    # Public API 1: Benchmark Role Matching (Backward Compatible)
    # ─────────────────────────────────────────────────────────────────────────
    def match(self, resume_text: str) -> Dict[str, Any]:
        """
        Match resume to standard benchmark roles.
        Maintains backward compatibility with the existing public interface.
        """
        resume_tfidf = self._calculate_tfidf(resume_text)

        matches = []
        for role, description in self.JOB_DESCRIPTIONS.items():
            job_tfidf = self._calculate_tfidf(description)
            similarity = self._cosine_similarity(resume_tfidf, job_tfidf)
            match_pct = round(similarity * 100, 1)
            matches.append({"role": role, "match": match_pct})

        matches.sort(key=lambda x: x["match"], reverse=True)
        best_match = matches[0] if matches else None

        return {
            "best_match": best_match,
            "all_matches": matches,
            "recommendations": self._get_recommendations(matches, resume_text),
        }

    def _get_recommendations(self, matches: List, resume_text: str) -> List[str]:
        """Get recommendations based on benchmark role matches."""
        recs = []
        if matches:
            top = matches[0]
            if top["match"] >= 70:
                recs.append(f"Strong overall alignment with standard {top['role']} role requirements.")
            elif top["match"] >= 50:
                recs.append(
                    f"Moderate alignment with {top['role']} — consider highlighting relevant core tools and skills if you possess them."
                )
            else:
                recs.append("Resume could benefit from more targeted domain keywords and project details.")
        return recs

    # ─────────────────────────────────────────────────────────────────────────
    # Public API 2: Direct Resume ↔ Target Job Description Matching
    # ─────────────────────────────────────────────────────────────────────────
    def match_resume_to_jd(
        self,
        resume_text: str,
        jd_text: str,
        jd_title: str = "",
    ) -> Dict[str, Any]:
        """
        Directly match a resume against a target Job Description.
        Calculates explainable coverage of required skills, preferred skills,
        experience alignment, and semantic text similarity.
        """
        if not jd_text or not jd_text.strip():
            return {
                "overall_match": 0.0,
                "breakdown": {},
                "matched_required_skills": [],
                "missing_required_skills": [],
                "matched_preferred_skills": [],
                "missing_preferred_skills": [],
                "recommendations": ["Please provide a target job description to evaluate matching."],
                "disclaimer": "Analytical estimate based on content similarity.",
            }

        # 1. Parse Job Description
        jd = self.jd_analyzer.analyze(jd_text, title=jd_title)

        # 2. Extract skills from Resume
        resume_skills_dict = self.nlp.extract_skills(resume_text)
        resume_skills_flat = set(
            [s.lower() for cat in resume_skills_dict.values() for s in cat]
        )
        resume_lower = resume_text.lower()

        # Skill matching predicate
        def has_skill(skill_name: str) -> bool:
            s_low = skill_name.lower()
            return s_low in resume_skills_flat or bool(
                re.search(rf"\b{re.escape(s_low)}\b", resume_lower)
            )

        # Required skills coverage
        matched_required = [s for s in jd.required_skills if has_skill(s)]
        missing_required = [s for s in jd.required_skills if s not in matched_required]
        if jd.required_skills:
            req_coverage = (len(matched_required) / len(jd.required_skills)) * 100.0
        else:
            req_coverage = 80.0

        # Preferred skills coverage
        matched_preferred = [s for s in jd.preferred_skills if has_skill(s)]
        missing_preferred = [s for s in jd.preferred_skills if s not in matched_preferred]
        if jd.preferred_skills:
            pref_coverage = (len(matched_preferred) / len(jd.preferred_skills)) * 100.0
        else:
            pref_coverage = 70.0

        # Semantic TF-IDF Similarity
        semantic_sim = self._compute_direct_similarity(resume_text, jd_text)
        semantic_score = round(semantic_sim * 100, 1)

        # Experience alignment
        exp_years, _ = self.nlp.calculate_experience_years(resume_text)
        if jd.experience_years_required is not None and jd.experience_years_required > 0:
            exp_ratio = exp_years / jd.experience_years_required
            exp_score = min(100.0, exp_ratio * 100.0)
        else:
            exp_score = 85.0

        # Education alignment
        edu_entities = self.nlp.extract_entities(resume_text).get("education", [])
        resume_edu_text = " ".join(edu_entities).lower() + " " + resume_lower[:600]
        if jd.education_required:
            edu_matches = 0
            for req_deg in jd.education_required:
                first_deg_word = req_deg.lower().split()[0]
                if (
                    first_deg_word in resume_edu_text
                    or "bachelor" in resume_edu_text
                    or "master" in resume_edu_text
                    or "degree" in resume_edu_text
                ):
                    edu_matches += 1
            edu_score = (edu_matches / len(jd.education_required)) * 100.0 if jd.education_required else 90.0
        else:
            edu_score = 90.0

        # Composite overall match score
        weights = self.config.weights
        overall = (
            req_coverage * weights.get("required_skills", 0.40)
            + pref_coverage * weights.get("preferred_skills", 0.20)
            + semantic_score * weights.get("semantic_similarity", 0.20)
            + exp_score * weights.get("experience_alignment", 0.10)
            + edu_score * weights.get("education_alignment", 0.10)
        )
        overall = max(0.0, min(100.0, overall))

        # Ethical recommendations
        recs: List[str] = []
        if missing_required:
            top_missing = missing_required[:5]
            recs.append(
                f"Core Required Skills: If you genuinely have experience with {', '.join(top_missing)}, consider highlighting them in your experience and skills sections."
            )
        if missing_preferred and len(missing_preferred) > 1:
            top_pref = missing_preferred[:3]
            recs.append(
                f"Preferred Qualifications: Mentioning any genuine background with {', '.join(top_pref)} can strengthen your application."
            )
        if jd.experience_years_required and exp_years < jd.experience_years_required:
            recs.append(
                f"The job specifies ~{jd.experience_years_required:.0f} years of experience. Highlight relevant freelance, academic, or project work to demonstrate equivalent depth."
            )
        if semantic_score < 40:
            recs.append(
                "Align your summary and project descriptions more closely with the domain terminology used in this job posting."
            )

        return {
            "job_title": jd.title,
            "overall_match": round(overall, 1),
            "breakdown": {
                "required_skills_match": round(req_coverage, 1),
                "preferred_skills_match": round(pref_coverage, 1),
                "semantic_similarity": semantic_score,
                "experience_alignment": round(exp_score, 1),
                "education_alignment": round(edu_score, 1),
            },
            "matched_required_skills": matched_required,
            "missing_required_skills": missing_required,
            "matched_preferred_skills": matched_preferred,
            "missing_preferred_skills": missing_preferred,
            "required_experience_years": jd.experience_years_required,
            "candidate_experience_years": exp_years,
            "recommendations": recs,
            "disclaimer": "Analytical estimate based on content similarity and skill alignment. This is NOT a prediction of whether an Applicant Tracking System will accept or reject a resume.",
        }

    def _compute_direct_similarity(self, text1: str, text2: str) -> float:
        """Compute cosine similarity between two dynamic texts using word frequencies."""
        words1 = self._tokenize(text1)
        words2 = self._tokenize(text2)
        if not words1 or not words2:
            return 0.0

        vocab = set(words1) | set(words2)
        tf1 = Counter(words1)
        tf2 = Counter(words2)

        dot = sum(tf1.get(w, 0) * tf2.get(w, 0) for w in vocab)
        mag1 = math.sqrt(sum(v**2 for v in tf1.values()))
        mag2 = math.sqrt(sum(v**2 for v in tf2.values()))
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot / (mag1 * mag2)
