"""
Job Matcher Module
Matches resumes to job roles using TF-IDF and cosine similarity.
"""

import re
from typing import Dict, List, Tuple
from collections import Counter
import math


class JobMatcher:
    """Matches resumes to suitable job roles using text similarity."""
    
    JOB_DESCRIPTIONS = {
        'Data Scientist': '''
            machine learning deep learning python r sql statistics data analysis 
            tensorflow pytorch pandas numpy scikit-learn visualization modeling
            feature engineering model deployment nlp computer vision a/b testing
            jupyter notebook kaggle research algorithms neural networks
        ''',
        'ML Engineer': '''
            machine learning python tensorflow pytorch docker kubernetes mlops
            model deployment aws gcp azure ci/cd pipeline api microservices
            feature store model monitoring production engineering scalability
            deep learning infrastructure optimization performance
        ''',
        'Data Analyst': '''
            sql excel tableau power bi python r data visualization reporting
            dashboards analytics business intelligence kpi metrics etl
            data cleaning statistical analysis presentation stakeholders
        ''',
        'Software Engineer': '''
            python java javascript typescript c++ git agile scrum api rest
            microservices docker kubernetes ci/cd testing debugging sql nosql
            system design architecture backend frontend full stack development
        ''',
        'Data Engineer': '''
            python sql spark hadoop airflow etl pipeline data warehouse
            aws gcp azure bigquery snowflake redshift kafka streaming
            data modeling schema design optimization performance scalability
        ''',
        'AI/ML Research': '''
            research publications neural networks deep learning transformers
            nlp computer vision reinforcement learning pytorch tensorflow
            mathematics statistics algorithms optimization papers conference
        '''
    }
    
    def __init__(self):
        self.vocabulary = set()
        self.idf_scores = {}
        self._build_vocabulary()
    
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
        words = re.findall(r'\b[a-z]+\b', text)
        return [w for w in words if len(w) > 2]
    
    def _calculate_tf(self, words: List[str]) -> Dict[str, float]:
        """Calculate term frequency."""
        word_counts = Counter(words)
        total = len(words)
        return {w: c/total for w, c in word_counts.items()}
    
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
    
    def match(self, resume_text: str) -> Dict:
        """
        Match resume to job roles.
        
        Returns:
            Dictionary with matches and recommendations
        """
        resume_tfidf = self._calculate_tfidf(resume_text)
        
        matches = []
        for role, description in self.JOB_DESCRIPTIONS.items():
            job_tfidf = self._calculate_tfidf(description)
            similarity = self._cosine_similarity(resume_tfidf, job_tfidf)
            match_pct = round(similarity * 100, 1)
            matches.append({'role': role, 'match': match_pct})
        
        matches.sort(key=lambda x: x['match'], reverse=True)
        
        best_match = matches[0] if matches else None
        
        return {
            'best_match': best_match,
            'all_matches': matches,
            'recommendations': self._get_recommendations(matches, resume_text)
        }
    
    def _get_recommendations(self, matches: List, resume_text: str) -> List[str]:
        """Get recommendations based on matches."""
        recs = []
        if matches:
            top = matches[0]
            if top['match'] >= 70:
                recs.append(f"Strong fit for {top['role']} roles")
            elif top['match'] >= 50:
                recs.append(f"Good potential for {top['role']} - consider adding more relevant skills")
            else:
                recs.append("Resume could benefit from more targeted keywords")
        return recs
