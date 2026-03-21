"""
ATS Scorer Module
Calculates ATS (Applicant Tracking System) compatibility scores.
"""

import re
from typing import Dict, List, Tuple, Optional
from collections import Counter


class ATSScorer:
    """
    Analyzes resume for ATS compatibility and provides scoring.
    """
    
    # Critical sections that ATS systems look for
    REQUIRED_SECTIONS = {
        'contact': ['email', 'phone', 'linkedin', 'address', 'contact'],
        'experience': ['experience', 'work history', 'employment', 'career', 'professional experience'],
        'education': ['education', 'academic', 'degree', 'university', 'college', 'qualification'],
        'skills': ['skills', 'technical skills', 'competencies', 'expertise', 'proficiencies']
    }
    
    OPTIONAL_SECTIONS = {
        'summary': ['summary', 'objective', 'profile', 'about me', 'career objective'],
        'projects': ['projects', 'portfolio', 'personal projects', 'academic projects'],
        'certifications': ['certifications', 'certificates', 'licenses', 'credentials'],
        'achievements': ['achievements', 'awards', 'honors', 'accomplishments'],
        'publications': ['publications', 'papers', 'research']
    }
    
    # Common ATS-friendly keywords by role
    ROLE_KEYWORDS = {
        'data_scientist': [
            'python', 'r', 'sql', 'machine learning', 'deep learning', 'statistics',
            'data analysis', 'visualization', 'tensorflow', 'pytorch', 'pandas',
            'numpy', 'scikit-learn', 'nlp', 'computer vision', 'a/b testing',
            'feature engineering', 'model deployment', 'aws', 'gcp', 'azure'
        ],
        'data_analyst': [
            'sql', 'excel', 'tableau', 'power bi', 'python', 'r', 'statistics',
            'data visualization', 'reporting', 'dashboards', 'etl', 'data cleaning',
            'business intelligence', 'analytics', 'kpi', 'metrics'
        ],
        'ml_engineer': [
            'python', 'tensorflow', 'pytorch', 'docker', 'kubernetes', 'mlops',
            'machine learning', 'deep learning', 'model deployment', 'aws', 'gcp',
            'ci/cd', 'feature store', 'model monitoring', 'api', 'microservices'
        ],
        'software_engineer': [
            'python', 'java', 'javascript', 'c++', 'git', 'agile', 'scrum',
            'api', 'rest', 'microservices', 'docker', 'kubernetes', 'ci/cd',
            'testing', 'debugging', 'sql', 'nosql', 'system design'
        ],
        'frontend_developer': [
            'javascript', 'typescript', 'react', 'vue', 'angular', 'html', 'css',
            'responsive design', 'ui/ux', 'webpack', 'npm', 'git', 'testing',
            'accessibility', 'performance optimization'
        ],
        'backend_developer': [
            'python', 'java', 'node.js', 'go', 'sql', 'nosql', 'api', 'rest',
            'microservices', 'docker', 'kubernetes', 'aws', 'database design',
            'caching', 'message queues', 'security'
        ]
    }
    
    def __init__(self):
        self.scores = {}
        self.feedback = []
    
    def calculate_score(self, text: str, target_role: Optional[str] = None) -> Dict:
        """
        Calculate comprehensive ATS score.
        
        Args:
            text: Resume text content
            target_role: Target job role for keyword matching
            
        Returns:
            Dictionary with scores and detailed feedback
        """
        self.feedback = []
        text_lower = text.lower()
        
        # Calculate individual scores
        section_score = self._score_sections(text_lower)
        format_score = self._score_formatting(text)
        keyword_score = self._score_keywords(text_lower, target_role)
        length_score = self._score_length(text)
        readability_score = self._score_readability(text)
        contact_score = self._score_contact_info(text)
        
        # Weight the scores
        weights = {
            'sections': 0.20,
            'formatting': 0.15,
            'keywords': 0.25,
            'length': 0.10,
            'readability': 0.15,
            'contact': 0.15
        }
        
        total_score = (
            section_score * weights['sections'] +
            format_score * weights['formatting'] +
            keyword_score * weights['keywords'] +
            length_score * weights['length'] +
            readability_score * weights['readability'] +
            contact_score * weights['contact']
        )
        
        self.scores = {
            'total': round(total_score, 1),
            'sections': round(section_score, 1),
            'formatting': round(format_score, 1),
            'keywords': round(keyword_score, 1),
            'length': round(length_score, 1),
            'readability': round(readability_score, 1),
            'contact': round(contact_score, 1)
        }
        
        return {
            'scores': self.scores,
            'feedback': self.feedback,
            'grade': self._get_grade(total_score),
            'pass_ats': total_score >= 60
        }
    
    def _score_sections(self, text: str) -> float:
        """Score based on presence of required and optional sections."""
        score = 0
        max_score = 100
        
        # Required sections (60 points total)
        required_found = 0
        for section, keywords in self.REQUIRED_SECTIONS.items():
            found = any(kw in text for kw in keywords)
            if found:
                required_found += 1
            else:
                self.feedback.append(f"⚠️ Missing required section: {section.title()}")
        
        score += (required_found / len(self.REQUIRED_SECTIONS)) * 60
        
        # Optional sections (40 points total)
        optional_found = 0
        for section, keywords in self.OPTIONAL_SECTIONS.items():
            found = any(kw in text for kw in keywords)
            if found:
                optional_found += 1
        
        score += (optional_found / len(self.OPTIONAL_SECTIONS)) * 40
        
        if required_found == len(self.REQUIRED_SECTIONS):
            self.feedback.append("✅ All required sections present")
        
        return min(score, max_score)
    
    def _score_formatting(self, text: str) -> float:
        """Score based on formatting quality."""
        score = 100
        
        # Check for problematic formatting
        issues = []
        
        # Too many special characters
        special_chars = len(re.findall(r'[^\w\s\.\,\;\:\-\+\@\#\(\)\/\&]', text))
        if special_chars > 50:
            score -= 15
            issues.append("Too many special characters")
        
        # Check for consistent use of bullet points
        bullet_patterns = [r'•', r'○', r'■', r'►', r'\*', r'-']
        bullet_types = sum(1 for p in bullet_patterns if re.search(p, text))
        if bullet_types > 3:
            score -= 10
            issues.append("Inconsistent bullet point styles")
        
        # Check for all caps abuse
        all_caps_words = len(re.findall(r'\b[A-Z]{5,}\b', text))
        if all_caps_words > 10:
            score -= 10
            issues.append("Excessive use of ALL CAPS")
        
        # Check for tables/graphics indicators (ATS struggle with these)
        if re.search(r'\|.*\|.*\|', text):
            score -= 15
            issues.append("Table-like formatting detected (may confuse ATS)")
        
        if not issues:
            self.feedback.append("✅ Good formatting for ATS compatibility")
        else:
            for issue in issues:
                self.feedback.append(f"⚠️ {issue}")
        
        return max(score, 0)
    
    def _score_keywords(self, text: str, target_role: Optional[str] = None) -> float:
        """Score based on relevant keyword density."""
        if not target_role:
            # Auto-detect role
            target_role = self._detect_role(text)
        
        target_role = target_role.lower().replace(' ', '_').replace('-', '_')
        
        if target_role not in self.ROLE_KEYWORDS:
            # Default to data scientist if role not found
            target_role = 'data_scientist'
        
        keywords = self.ROLE_KEYWORDS[target_role]
        found_keywords = []
        missing_keywords = []
        
        for keyword in keywords:
            if keyword.lower() in text:
                found_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        score = (len(found_keywords) / len(keywords)) * 100
        
        if found_keywords:
            self.feedback.append(f"✅ Found {len(found_keywords)}/{len(keywords)} role-relevant keywords")
        
        if missing_keywords[:5]:  # Show top 5 missing
            self.feedback.append(f"💡 Consider adding keywords: {', '.join(missing_keywords[:5])}")
        
        return score
    
    def _score_length(self, text: str) -> float:
        """Score based on resume length."""
        word_count = len(text.split())
        
        # Optimal range: 400-800 words (1-2 pages)
        if 400 <= word_count <= 800:
            score = 100
            self.feedback.append("✅ Resume length is optimal")
        elif 300 <= word_count < 400 or 800 < word_count <= 1000:
            score = 80
            self.feedback.append("⚠️ Resume length is acceptable but could be adjusted")
        elif 200 <= word_count < 300:
            score = 60
            self.feedback.append("⚠️ Resume might be too short - add more details")
        elif word_count > 1000:
            score = 60
            self.feedback.append("⚠️ Resume might be too long - consider condensing")
        else:
            score = 40
            self.feedback.append("❌ Resume length is problematic")
        
        return score
    
    def _score_readability(self, text: str) -> float:
        """Score based on text readability."""
        score = 100
        
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 50
        
        avg_sentence_length = len(words) / len(sentences)
        
        # Optimal sentence length: 15-25 words
        if avg_sentence_length > 30:
            score -= 20
            self.feedback.append("⚠️ Sentences are too long - break them up")
        elif avg_sentence_length < 10:
            score -= 10
            self.feedback.append("⚠️ Sentences might be too short")
        
        # Check for passive voice indicators
        passive_indicators = ['was', 'were', 'been', 'being', 'is', 'are']
        passive_count = sum(1 for w in words if w.lower() in passive_indicators)
        passive_ratio = passive_count / max(len(words), 1)
        
        if passive_ratio > 0.05:
            score -= 10
            self.feedback.append("💡 Consider using more active voice")
        
        return max(score, 0)
    
    def _score_contact_info(self, text: str) -> float:
        """Score based on contact information completeness."""
        score = 0
        
        # Email
        if re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text):
            score += 30
        else:
            self.feedback.append("❌ No email address found")
        
        # Phone
        if re.search(r'[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[0-9]{3,4}[-\s\.]?[0-9]{4,6}', text):
            score += 25
        else:
            self.feedback.append("⚠️ No phone number found")
        
        # LinkedIn
        if re.search(r'linkedin', text, re.IGNORECASE):
            score += 25
        else:
            self.feedback.append("💡 Consider adding LinkedIn profile")
        
        # GitHub/Portfolio (bonus for tech roles)
        if re.search(r'github|portfolio|website', text, re.IGNORECASE):
            score += 20
        else:
            self.feedback.append("💡 Consider adding GitHub or portfolio link")
        
        return min(score, 100)
    
    def _detect_role(self, text: str) -> str:
        """Auto-detect the target role from resume content."""
        role_scores = {}
        
        for role, keywords in self.ROLE_KEYWORDS.items():
            matches = sum(1 for kw in keywords if kw.lower() in text)
            role_scores[role] = matches
        
        if role_scores:
            detected = max(role_scores, key=role_scores.get)
            return detected
        
        return 'software_engineer'
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade."""
        if score >= 90:
            return 'A+'
        elif score >= 85:
            return 'A'
        elif score >= 80:
            return 'A-'
        elif score >= 75:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 65:
            return 'B-'
        elif score >= 60:
            return 'C+'
        elif score >= 55:
            return 'C'
        elif score >= 50:
            return 'C-'
        elif score >= 45:
            return 'D'
        else:
            return 'F'
    
    def get_improvement_suggestions(self) -> List[str]:
        """Get prioritized list of improvements."""
        suggestions = []
        
        if self.scores.get('contact', 0) < 70:
            suggestions.append("Add complete contact information (email, phone, LinkedIn)")
        
        if self.scores.get('sections', 0) < 70:
            suggestions.append("Include all required sections: Experience, Education, Skills")
        
        if self.scores.get('keywords', 0) < 60:
            suggestions.append("Add more role-relevant keywords and technical skills")
        
        if self.scores.get('formatting', 0) < 70:
            suggestions.append("Simplify formatting - avoid tables, graphics, and special characters")
        
        if self.scores.get('readability', 0) < 70:
            suggestions.append("Improve readability - use shorter sentences and active voice")
        
        return suggestions
