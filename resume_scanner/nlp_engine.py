"""
NLP Engine Module
Handles skill extraction, entity recognition, and text analysis using NLP.
"""

import re
from typing import List, Dict, Set, Tuple
from collections import Counter


class NLPEngine:
    """
    NLP-powered engine for extracting skills, entities, and analyzing resume content.
    """
    
    # Comprehensive skill databases
    PROGRAMMING_LANGUAGES = {
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c', 'ruby', 'go', 'golang',
        'rust', 'kotlin', 'swift', 'scala', 'php', 'perl', 'r', 'matlab', 'julia', 'dart',
        'objective-c', 'assembly', 'bash', 'shell', 'powershell', 'sql', 'html', 'css', 'sass',
        'less', 'lua', 'haskell', 'clojure', 'elixir', 'erlang', 'fortran', 'cobol', 'vba',
        'groovy', 'f#', 'ocaml', 'scheme', 'lisp', 'prolog', 'solidity'
    }
    
    FRAMEWORKS_LIBRARIES = {
        # Python
        'django', 'flask', 'fastapi', 'streamlit', 'pandas', 'numpy', 'scipy', 'matplotlib',
        'seaborn', 'plotly', 'bokeh', 'scikit-learn', 'sklearn', 'tensorflow', 'keras', 'pytorch',
        'torch', 'xgboost', 'lightgbm', 'catboost', 'nltk', 'spacy', 'gensim', 'transformers',
        'huggingface', 'opencv', 'pillow', 'beautifulsoup', 'scrapy', 'selenium', 'requests',
        'asyncio', 'celery', 'airflow', 'prefect', 'dask', 'pyspark', 'polars',
        # JavaScript
        'react', 'reactjs', 'angular', 'vue', 'vuejs', 'svelte', 'next.js', 'nextjs', 'nuxt',
        'express', 'expressjs', 'node', 'nodejs', 'nest', 'nestjs', 'gatsby', 'remix',
        'jquery', 'redux', 'mobx', 'webpack', 'vite', 'rollup', 'babel', 'eslint',
        # Java
        'spring', 'spring boot', 'springboot', 'hibernate', 'maven', 'gradle', 'junit',
        # Other
        'rails', 'ruby on rails', '.net', 'asp.net', 'entity framework', 'blazor',
        'flutter', 'react native', 'ionic', 'electron', 'qt', 'gtk'
    }
    
    DATA_SCIENCE_TOOLS = {
        'jupyter', 'jupyter notebook', 'anaconda', 'colab', 'google colab', 'kaggle',
        'databricks', 'mlflow', 'wandb', 'weights and biases', 'tensorboard', 'optuna',
        'hyperopt', 'ray', 'dvc', 'great expectations', 'evidently', 'whylabs',
        'feature store', 'feast', 'sagemaker', 'vertex ai', 'azure ml', 'datarobot',
        'h2o', 'dataiku', 'rapidminer', 'knime', 'alteryx', 'tableau', 'power bi',
        'looker', 'metabase', 'superset', 'grafana', 'kibana', 'splunk', 'excel',
        'google sheets', 'stata', 'spss', 'sas', 'minitab', 'eviews'
    }
    
    DATABASES = {
        'mysql', 'postgresql', 'postgres', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
        'sqlite', 'oracle', 'sql server', 'mssql', 'mariadb', 'dynamodb', 'firestore',
        'firebase', 'couchdb', 'neo4j', 'graphql', 'influxdb', 'timescaledb', 'clickhouse',
        'snowflake', 'redshift', 'bigquery', 'hive', 'presto', 'trino', 'dremio',
        'cockroachdb', 'supabase', 'planetscale', 'fauna', 'airtable'
    }
    
    CLOUD_DEVOPS = {
        'aws', 'amazon web services', 'ec2', 's3', 'lambda', 'rds', 'ecs', 'eks', 'fargate',
        'azure', 'microsoft azure', 'gcp', 'google cloud', 'google cloud platform',
        'docker', 'kubernetes', 'k8s', 'helm', 'terraform', 'ansible', 'puppet', 'chef',
        'jenkins', 'github actions', 'gitlab ci', 'circleci', 'travis ci', 'argocd',
        'prometheus', 'grafana', 'datadog', 'new relic', 'pagerduty', 'opsgenie',
        'nginx', 'apache', 'caddy', 'traefik', 'kong', 'istio', 'envoy', 'linkerd',
        'vagrant', 'virtualbox', 'vmware', 'openstack', 'cloudflare', 'vercel', 'netlify',
        'heroku', 'digitalocean', 'linode', 'vultr', 'render', 'railway', 'fly.io'
    }
    
    SOFT_SKILLS = {
        'leadership', 'communication', 'teamwork', 'collaboration', 'problem solving',
        'problem-solving', 'critical thinking', 'analytical', 'creativity', 'innovation',
        'time management', 'project management', 'agile', 'scrum', 'kanban', 'waterfall',
        'stakeholder management', 'negotiation', 'presentation', 'public speaking',
        'mentoring', 'coaching', 'conflict resolution', 'decision making', 'adaptability',
        'flexibility', 'attention to detail', 'organization', 'planning', 'prioritization',
        'multitasking', 'self-motivated', 'proactive', 'initiative', 'work ethic',
        'interpersonal', 'customer service', 'client relations', 'cross-functional'
    }
    
    ML_AI_CONCEPTS = {
        'machine learning', 'deep learning', 'neural network', 'neural networks',
        'natural language processing', 'nlp', 'computer vision', 'cv', 'reinforcement learning',
        'supervised learning', 'unsupervised learning', 'semi-supervised', 'transfer learning',
        'fine-tuning', 'feature engineering', 'feature selection', 'dimensionality reduction',
        'clustering', 'classification', 'regression', 'time series', 'forecasting',
        'anomaly detection', 'recommendation system', 'recommender system', 'collaborative filtering',
        'cnn', 'rnn', 'lstm', 'gru', 'transformer', 'bert', 'gpt', 'attention mechanism',
        'generative ai', 'gan', 'vae', 'diffusion', 'llm', 'large language model',
        'rag', 'retrieval augmented', 'langchain', 'llamaindex', 'vector database',
        'embedding', 'word2vec', 'glove', 'fasttext', 'sentiment analysis', 'ner',
        'named entity recognition', 'pos tagging', 'topic modeling', 'text classification',
        'object detection', 'image segmentation', 'image classification', 'ocr',
        'speech recognition', 'speech synthesis', 'tts', 'asr'
    }
    
    def __init__(self, use_spacy: bool = True):
        """
        Initialize NLP Engine.
        
        Args:
            use_spacy: Whether to use spaCy for advanced NLP (requires spacy to be installed)
        """
        self.use_spacy = use_spacy
        self.nlp = None
        
        if use_spacy:
            try:
                import spacy
                try:
                    self.nlp = spacy.load("en_core_web_sm")
                except OSError:
                    print("Warning: spaCy model 'en_core_web_sm' not found. Using pattern matching only.")
                    self.use_spacy = False
            except ImportError:
                print("Warning: spaCy not installed. Using pattern matching only.")
                self.use_spacy = False
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """
        Extract categorized skills from resume text.
        
        Args:
            text: Resume text content
            
        Returns:
            Dictionary with skill categories and found skills
        """
        text_lower = text.lower()
        
        skills = {
            'programming_languages': [],
            'frameworks_libraries': [],
            'data_science_tools': [],
            'databases': [],
            'cloud_devops': [],
            'ml_ai_concepts': [],
            'soft_skills': []
        }
        
        # Extract skills by category
        skills['programming_languages'] = self._find_skills(text_lower, self.PROGRAMMING_LANGUAGES)
        skills['frameworks_libraries'] = self._find_skills(text_lower, self.FRAMEWORKS_LIBRARIES)
        skills['data_science_tools'] = self._find_skills(text_lower, self.DATA_SCIENCE_TOOLS)
        skills['databases'] = self._find_skills(text_lower, self.DATABASES)
        skills['cloud_devops'] = self._find_skills(text_lower, self.CLOUD_DEVOPS)
        skills['ml_ai_concepts'] = self._find_skills(text_lower, self.ML_AI_CONCEPTS)
        skills['soft_skills'] = self._find_skills(text_lower, self.SOFT_SKILLS)
        
        return skills
    
    def _find_skills(self, text: str, skill_set: Set[str]) -> List[str]:
        """Find skills from a skill set in text."""
        found = []
        for skill in skill_set:
            # Use word boundary matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                found.append(skill.title())
        return sorted(list(set(found)))
    
    def get_all_skills_flat(self, text: str) -> List[str]:
        """Get all extracted skills as a flat list."""
        skills = self.extract_skills(text)
        all_skills = []
        for category in skills.values():
            all_skills.extend(category)
        return sorted(list(set(all_skills)))
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities using spaCy.
        
        Args:
            text: Resume text content
            
        Returns:
            Dictionary with entity types and found entities
        """
        entities = {
            'organizations': [],
            'locations': [],
            'dates': [],
            'education': [],
            'persons': []
        }
        
        if self.nlp:
            doc = self.nlp(text[:100000])  # Limit text length for performance
            
            for ent in doc.ents:
                if ent.label_ == 'ORG':
                    entities['organizations'].append(ent.text)
                elif ent.label_ in ['GPE', 'LOC']:
                    entities['locations'].append(ent.text)
                elif ent.label_ == 'DATE':
                    entities['dates'].append(ent.text)
                elif ent.label_ == 'PERSON':
                    entities['persons'].append(ent.text)
            
            # Deduplicate
            for key in entities:
                entities[key] = list(set(entities[key]))
        
        # Pattern-based extraction for education
        education_patterns = [
            r'\b(B\.?S\.?|B\.?A\.?|M\.?S\.?|M\.?A\.?|Ph\.?D\.?|MBA|Bachelor|Master|Doctorate)\b',
            r'\b(University|College|Institute|School)\s+of\s+\w+',
            r'\b(Computer Science|Data Science|Mathematics|Statistics|Engineering|Physics|Chemistry|Biology)\b'
        ]
        
        for pattern in education_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities['education'].extend(matches)
        
        entities['education'] = list(set(entities['education']))
        
        return entities
    
    def calculate_experience_years(self, text: str) -> Tuple[float, List[Dict]]:
        """
        Estimate years of experience from resume.
        
        Args:
            text: Resume text content
            
        Returns:
            Tuple of (estimated years, list of date ranges found)
        """
        # Find date patterns
        date_patterns = [
            r'(\d{4})\s*[-–—]\s*(present|current|\d{4})',
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*(\d{4})\s*[-–—]\s*(present|current|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{4})',
        ]
        
        experiences = []
        current_year = 2026  # Current year
        
        # Simple year-to-year pattern
        year_pattern = r'(\d{4})\s*[-–—]\s*(present|current|\d{4})'
        matches = re.findall(year_pattern, text, re.IGNORECASE)
        
        total_years = 0
        for start, end in matches:
            start_year = int(start)
            if end.lower() in ['present', 'current']:
                end_year = current_year
            else:
                end_year = int(end)
            
            if 1990 <= start_year <= current_year and start_year <= end_year <= current_year:
                years = end_year - start_year
                total_years += years
                experiences.append({
                    'start': start_year,
                    'end': end_year,
                    'years': years
                })
        
        return total_years, experiences
    
    def analyze_text_quality(self, text: str) -> Dict[str, float]:
        """
        Analyze text quality metrics.
        
        Args:
            text: Resume text content
            
        Returns:
            Dictionary with quality metrics
        """
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Calculate metrics
        word_count = len(words)
        sentence_count = len(sentences)
        avg_word_length = sum(len(w) for w in words) / max(word_count, 1)
        avg_sentence_length = word_count / max(sentence_count, 1)
        
        # Vocabulary richness (Type-Token Ratio)
        unique_words = set(w.lower() for w in words)
        ttr = len(unique_words) / max(word_count, 1)
        
        # Count action verbs
        action_verbs = {
            'achieved', 'built', 'created', 'designed', 'developed', 'established',
            'implemented', 'improved', 'increased', 'launched', 'led', 'managed',
            'optimized', 'reduced', 'streamlined', 'transformed', 'delivered',
            'executed', 'generated', 'initiated', 'maintained', 'produced',
            'resolved', 'spearheaded', 'supervised', 'trained', 'analyzed',
            'collaborated', 'coordinated', 'demonstrated', 'engineered', 'enhanced'
        }
        
        action_verb_count = sum(1 for w in words if w.lower() in action_verbs)
        action_verb_ratio = action_verb_count / max(word_count, 1) * 100
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_word_length': round(avg_word_length, 2),
            'avg_sentence_length': round(avg_sentence_length, 2),
            'vocabulary_richness': round(ttr, 3),
            'action_verb_count': action_verb_count,
            'action_verb_percentage': round(action_verb_ratio, 2)
        }
    
    def get_skill_summary(self, text: str) -> Dict[str, any]:
        """
        Get comprehensive skill summary.
        
        Args:
            text: Resume text content
            
        Returns:
            Summary with skill counts and top skills
        """
        skills = self.extract_skills(text)
        
        total_skills = sum(len(v) for v in skills.values())
        
        category_counts = {k: len(v) for k, v in skills.items()}
        
        # Get top skills by category
        top_by_category = {}
        for category, skill_list in skills.items():
            top_by_category[category] = skill_list[:5]
        
        return {
            'total_skills': total_skills,
            'category_counts': category_counts,
            'skills_by_category': skills,
            'top_by_category': top_by_category
        }
