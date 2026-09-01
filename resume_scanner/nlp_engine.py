"""
NLP Engine Module
Handles skill extraction, entity recognition, and text analysis using NLP.
"""

import re
import logging
from datetime import datetime
from typing import List, Dict, Set, Tuple, Any

logger = logging.getLogger(__name__)


class NLPEngine:
    """
    NLP-powered engine for extracting skills, entities, and analyzing resume content.
    """

    # Action verbs for achievement and bullet strength analysis
    ACTION_VERBS = {
        "accelerated", "achieved", "acquired", "administered", "advised", "allocated",
        "amplified", "analyzed", "architected", "authored", "automated", "boosted",
        "budgeted", "built", "calculated", "centralized", "championed", "coached",
        "collaborated", "compiled", "composed", "conceptualized", "conducted",
        "configured", "consolidated", "constructed", "consulted", "controlled",
        "converted", "coordinated", "created", "customized", "debugged", "decreased",
        "defined", "delivered", "deployed", "designed", "developed", "devised",
        "diagnosed", "directed", "discovered", "dispatched", "diversified", "documented",
        "doubled", "drafted", "drove", "eliminated", "enabled", "enforced",
        "engineered", "enhanced", "established", "estimated", "evaluated", "executed",
        "expanded", "expedited", "fabricated", "facilitated", "forecasted", "formulated",
        "fostered", "founded", "generated", "guided", "halted", "headed", "identified",
        "implemented", "improved", "increased", "initiated", "innovated", "inspected",
        "installed", "instituted", "instructed", "integrated", "intensified", "interfaced",
        "interpreted", "interviewed", "introduced", "invented", "investigated", "launched",
        "lead", "led", "leveraged", "maintained", "managed", "maximized", "mentored",
        "merged", "migrated", "minimized", "modeled", "moderated", "modernized",
        "monitored", "motivated", "negotiated", "obtained", "operated", "optimized",
        "orchestrated", "organized", "originated", "overhauled", "oversaw", "partnered",
        "performed", "pioneered", "planned", "prepared", "presented", "prevented",
        "produced", "programmed", "promoted", "proposed", "published", "quantified",
        "re-engineered", "rebuilt", "reconciled", "recruited", "redesigned", "reduced",
        "refined", "reformed", "regulated", "remodeled", "reorganized", "repaired",
        "replaced", "represented", "researched", "resolved", "restructured", "retrieved",
        "revamped", "reviewed", "revitalized", "revolutionized", "saved", "scaled",
        "scheduled", "secured", "selected", "separated", "simplified", "simulated",
        "slashed", "solidified", "solved", "spearheaded", "standardized", "stimulated",
        "streamlined", "structured", "succeeded", "supervised", "supplied", "supported",
        "surpassed", "synthesized", "systematized", "tabulated", "targeted", "taught",
        "terminated", "tested", "tracked", "trained", "transcribed", "transformed",
        "transitioned", "translated", "tripled", "troubleshot", "unified", "unlocked",
        "updated", "upgraded", "utilized", "validated", "verified", "yielded"
    }

    # Canonical skill aliases for normalization
    SKILL_ALIASES = {
        "sklearn": "Scikit-Learn",
        "scikit-learn": "Scikit-Learn",
        "scikit learn": "Scikit-Learn",
        "node": "Node.js",
        "nodejs": "Node.js",
        "node.js": "Node.js",
        "k8s": "Kubernetes",
        "kubernetes": "Kubernetes",
        "postgres": "PostgreSQL",
        "postgresql": "PostgreSQL",
        "golang": "Go",
        "go": "Go",
        "react": "React",
        "reactjs": "React",
        "react.js": "React",
        "vue": "Vue.js",
        "vuejs": "Vue.js",
        "vue.js": "Vue.js",
        "next.js": "Next.js",
        "nextjs": "Next.js",
        "aws": "AWS",
        "amazon web services": "AWS",
        "gcp": "GCP",
        "google cloud": "GCP",
        "google cloud platform": "GCP",
        "azure": "Azure",
        "microsoft azure": "Azure",
        "tf": "TensorFlow",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
        "torch": "PyTorch",
        "mongo": "MongoDB",
        "mongodb": "MongoDB",
        "ci/cd": "CI/CD",
        "cicd": "CI/CD",
        "mlops": "MLOps",
        "nlp": "NLP",
        "cv": "Computer Vision",
        "computer vision": "Computer Vision",
        "tailwind": "Tailwind CSS",
        "tailwindcss": "Tailwind CSS",
        "c++": "C++",
        "c#": "C#",
        ".net": ".NET",
        "asp.net": "ASP.NET",
        "sql": "SQL",
        "html": "HTML5",
        "html5": "HTML5",
        "css": "CSS3",
        "css3": "CSS3",
        "js": "JavaScript",
        "javascript": "JavaScript",
        "ts": "TypeScript",
        "typescript": "TypeScript",
        "power bi": "Power BI",
        "powerbi": "Power BI",
        "docker": "Docker",
        "graphql": "GraphQL",
        "rest api": "REST APIs",
        "rest": "REST APIs",
        "api": "REST APIs",
        "splunk": "Splunk",
        "wireshark": "Wireshark",
        "metasploit": "Metasploit",
        "burp suite": "Burp Suite",
        "nmap": "Nmap",
        "nessus": "Nessus",
        "snort": "Snort",
        "suricata": "Suricata",
        "crowdstrike": "CrowdStrike",
        "qualys": "Qualys",
        "kali linux": "Kali Linux",
        "cissp": "CISSP",
        "ceh": "CEH",
        "security+": "CompTIA Security+",
        "comptia security+": "CompTIA Security+",
    }

    MONTH_MAP = {
        "jan": 1, "january": 1,
        "feb": 2, "february": 2,
        "mar": 3, "march": 3,
        "apr": 4, "april": 4,
        "may": 5,
        "jun": 6, "june": 6,
        "jul": 7, "july": 7,
        "aug": 8, "august": 8,
        "sep": 9, "september": 9, "sept": 9,
        "oct": 10, "october": 10,
        "nov": 11, "november": 11,
        "dec": 12, "december": 12,
    }

    # Comprehensive skill databases
    PROGRAMMING_LANGUAGES = {
        "python",
        "java",
        "javascript",
        "typescript",
        "c++",
        "c#",
        "c",
        "ruby",
        "go",
        "golang",
        "rust",
        "kotlin",
        "swift",
        "scala",
        "php",
        "perl",
        "r",
        "matlab",
        "julia",
        "dart",
        "objective-c",
        "assembly",
        "bash",
        "shell",
        "powershell",
        "sql",
        "html",
        "css",
        "sass",
        "less",
        "lua",
        "haskell",
        "clojure",
        "elixir",
        "erlang",
        "fortran",
        "cobol",
        "vba",
        "groovy",
        "f#",
        "ocaml",
        "scheme",
        "lisp",
        "prolog",
        "solidity",
    }

    FRAMEWORKS_LIBRARIES = {
        # Python
        "django",
        "flask",
        "fastapi",
        "streamlit",
        "pandas",
        "numpy",
        "scipy",
        "matplotlib",
        "seaborn",
        "plotly",
        "bokeh",
        "scikit-learn",
        "sklearn",
        "tensorflow",
        "keras",
        "pytorch",
        "torch",
        "xgboost",
        "lightgbm",
        "catboost",
        "nltk",
        "spacy",
        "gensim",
        "transformers",
        "huggingface",
        "opencv",
        "pillow",
        "beautifulsoup",
        "scrapy",
        "selenium",
        "requests",
        "asyncio",
        "celery",
        "airflow",
        "prefect",
        "dask",
        "pyspark",
        "polars",
        # JavaScript
        "react",
        "reactjs",
        "angular",
        "vue",
        "vuejs",
        "svelte",
        "next.js",
        "nextjs",
        "nuxt",
        "express",
        "expressjs",
        "node",
        "nodejs",
        "nest",
        "nestjs",
        "gatsby",
        "remix",
        "jquery",
        "redux",
        "mobx",
        "webpack",
        "vite",
        "rollup",
        "babel",
        "eslint",
        "tailwind",
        "tailwindcss",
        "zustand",
        "graphql",
        "rest api",
        "prisma",
        "sequelize",
        "mongoose",
        "fastify",
        "jest",
        "cypress",
        "playwright",
        # Java
        "spring",
        "spring boot",
        "springboot",
        "hibernate",
        "maven",
        "gradle",
        "junit",
        # Other
        "rails",
        "ruby on rails",
        ".net",
        "asp.net",
        "entity framework",
        "blazor",
        "flutter",
        "react native",
        "ionic",
        "electron",
        "qt",
        "gtk",
    }

    CYBERSECURITY_TOOLS = {
        "wireshark",
        "splunk",
        "metasploit",
        "burp suite",
        "nmap",
        "nessus",
        "snort",
        "suricata",
        "kali linux",
        "crowdstrike",
        "qualys",
        "owasp",
        "owasp zap",
        "penetration testing",
        "vulnerability assessment",
        "incident response",
        "threat hunting",
        "threat intelligence",
        "zero trust",
        "siem",
        "soc",
        "firewall",
        "firewalls",
        "cryptography",
        "malware analysis",
        "network security",
        "ids/ips",
        "cissp",
        "ceh",
        "security+",
    }

    DATA_SCIENCE_TOOLS = {
        "jupyter",
        "jupyter notebook",
        "anaconda",
        "colab",
        "google colab",
        "kaggle",
        "databricks",
        "mlflow",
        "wandb",
        "weights and biases",
        "tensorboard",
        "optuna",
        "hyperopt",
        "ray",
        "dvc",
        "great expectations",
        "evidently",
        "whylabs",
        "feature store",
        "feast",
        "sagemaker",
        "vertex ai",
        "azure ml",
        "datarobot",
        "h2o",
        "dataiku",
        "rapidminer",
        "knime",
        "alteryx",
        "tableau",
        "power bi",
        "looker",
        "metabase",
        "superset",
        "grafana",
        "kibana",
        "splunk",
        "excel",
        "google sheets",
        "stata",
        "spss",
        "sas",
        "minitab",
        "eviews",
    }

    DATABASES = {
        "mysql",
        "postgresql",
        "postgres",
        "mongodb",
        "redis",
        "elasticsearch",
        "cassandra",
        "sqlite",
        "oracle",
        "sql server",
        "mssql",
        "mariadb",
        "dynamodb",
        "firestore",
        "firebase",
        "couchdb",
        "neo4j",
        "graphql",
        "influxdb",
        "timescaledb",
        "clickhouse",
        "snowflake",
        "redshift",
        "bigquery",
        "hive",
        "presto",
        "trino",
        "dremio",
        "cockroachdb",
        "supabase",
        "planetscale",
        "fauna",
        "airtable",
    }

    CLOUD_DEVOPS = {
        "aws",
        "amazon web services",
        "ec2",
        "s3",
        "lambda",
        "rds",
        "ecs",
        "eks",
        "fargate",
        "azure",
        "microsoft azure",
        "gcp",
        "google cloud",
        "google cloud platform",
        "docker",
        "kubernetes",
        "k8s",
        "helm",
        "terraform",
        "ansible",
        "puppet",
        "chef",
        "jenkins",
        "github actions",
        "gitlab ci",
        "circleci",
        "travis ci",
        "argocd",
        "prometheus",
        "grafana",
        "datadog",
        "new relic",
        "pagerduty",
        "opsgenie",
        "nginx",
        "apache",
        "caddy",
        "traefik",
        "kong",
        "istio",
        "envoy",
        "linkerd",
        "vagrant",
        "virtualbox",
        "vmware",
        "openstack",
        "cloudflare",
        "vercel",
        "netlify",
        "heroku",
        "digitalocean",
        "linode",
        "vultr",
        "render",
        "railway",
        "fly.io",
    }

    SOFT_SKILLS = {
        "leadership",
        "communication",
        "teamwork",
        "collaboration",
        "problem solving",
        "problem-solving",
        "critical thinking",
        "analytical",
        "creativity",
        "innovation",
        "time management",
        "project management",
        "agile",
        "scrum",
        "kanban",
        "waterfall",
        "stakeholder management",
        "negotiation",
        "presentation",
        "public speaking",
        "mentoring",
        "coaching",
        "conflict resolution",
        "decision making",
        "adaptability",
        "flexibility",
        "attention to detail",
        "organization",
        "planning",
        "prioritization",
        "multitasking",
        "self-motivated",
        "proactive",
        "initiative",
        "work ethic",
        "interpersonal",
        "customer service",
        "client relations",
        "cross-functional",
    }

    ML_AI_CONCEPTS = {
        "machine learning",
        "deep learning",
        "neural network",
        "neural networks",
        "natural language processing",
        "nlp",
        "computer vision",
        "cv",
        "reinforcement learning",
        "supervised learning",
        "unsupervised learning",
        "semi-supervised",
        "transfer learning",
        "fine-tuning",
        "feature engineering",
        "feature selection",
        "dimensionality reduction",
        "clustering",
        "classification",
        "regression",
        "time series",
        "forecasting",
        "anomaly detection",
        "recommendation system",
        "recommender system",
        "collaborative filtering",
        "cnn",
        "rnn",
        "lstm",
        "gru",
        "transformer",
        "bert",
        "gpt",
        "attention mechanism",
        "generative ai",
        "gan",
        "vae",
        "diffusion",
        "llm",
        "large language model",
        "rag",
        "retrieval augmented",
        "langchain",
        "llamaindex",
        "vector database",
        "embedding",
        "word2vec",
        "glove",
        "fasttext",
        "sentiment analysis",
        "ner",
        "named entity recognition",
        "pos tagging",
        "topic modeling",
        "text classification",
        "object detection",
        "image segmentation",
        "image classification",
        "ocr",
        "speech recognition",
        "speech synthesis",
        "tts",
        "asr",
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
                    logger.warning(
                        "spaCy model 'en_core_web_sm' not found. Using pattern matching only."
                    )
                    self.use_spacy = False
            except ImportError:
                logger.warning("spaCy not installed. Using pattern matching only.")
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
            "programming_languages": [],
            "frameworks_libraries": [],
            "data_science_tools": [],
            "cybersecurity_tools": [],
            "databases": [],
            "cloud_devops": [],
            "ml_ai_concepts": [],
            "soft_skills": [],
        }

        # Extract skills by category
        skills["programming_languages"] = self._find_skills(
            text_lower, self.PROGRAMMING_LANGUAGES
        )
        skills["frameworks_libraries"] = self._find_skills(
            text_lower, self.FRAMEWORKS_LIBRARIES
        )
        skills["data_science_tools"] = self._find_skills(
            text_lower, self.DATA_SCIENCE_TOOLS
        )
        skills["cybersecurity_tools"] = self._find_skills(
            text_lower, self.CYBERSECURITY_TOOLS
        )
        skills["databases"] = self._find_skills(text_lower, self.DATABASES)
        skills["cloud_devops"] = self._find_skills(text_lower, self.CLOUD_DEVOPS)
        skills["ml_ai_concepts"] = self._find_skills(text_lower, self.ML_AI_CONCEPTS)
        skills["soft_skills"] = self._find_skills(text_lower, self.SOFT_SKILLS)

        return skills

    def _find_skills(self, text: str, skill_set: Set[str]) -> List[str]:
        """
        Find skills using boundary-safe regex matching and alias normalization.
        Handles C++, C#, .NET, and single-character languages (C, R) without false positives.
        """
        found: Set[str] = set()
        for skill in skill_set:
            skill_lower = skill.lower()

            # Punctuation-safe boundary handling
            if skill_lower == "c++":
                pattern = r"(?<!\w)c\+\+(?!\w)"
            elif skill_lower == "c#":
                pattern = r"(?<!\w)c#(?!\w)"
            elif skill_lower == ".net":
                pattern = r"(?<!\w)\.net(?!\w)"
            elif skill_lower == "c":
                # Single character 'c' should not match in 'c++' or inside words
                pattern = r"\b[Cc]\b(?!\s*[\+#])"
            elif skill_lower == "r":
                # Single character 'r' should not match in date numbers or arbitrary terms
                pattern = r"\b[Rr]\b(?!\s*[\d\.\-])"
            elif "/" in skill_lower or "-" in skill_lower:
                pattern = r"(?<!\w)" + re.escape(skill_lower) + r"(?!\w)"
            else:
                pattern = r"\b" + re.escape(skill_lower) + r"\b"

            if re.search(pattern, text, re.IGNORECASE):
                canonical = self.SKILL_ALIASES.get(skill_lower, skill.title())
                found.add(canonical)

        return sorted(list(found))

    def get_all_skills_flat(self, text: str) -> List[str]:
        """Get all extracted skills as a flat list."""
        skills = self.extract_skills(text)
        all_skills = []
        for category in skills.values():
            all_skills.extend(category)
        return sorted(list(set(all_skills)))

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities using spaCy or pattern matching fallback.
        """
        entities = {
            "organizations": [],
            "locations": [],
            "dates": [],
            "education": [],
            "persons": [],
        }

        if self.nlp:
            doc = self.nlp(text[:100000])  # Limit text length for performance

            for ent in doc.ents:
                if ent.label_ == "ORG":
                    entities["organizations"].append(ent.text)
                elif ent.label_ in ["GPE", "LOC"]:
                    entities["locations"].append(ent.text)
                elif ent.label_ == "DATE":
                    entities["dates"].append(ent.text)
                elif ent.label_ == "PERSON":
                    entities["persons"].append(ent.text)

            # Deduplicate
            for key in entities:
                entities[key] = list(set(entities[key]))

        # Pattern-based extraction for education
        education_patterns = [
            r"\b(B\.?S\.?|B\.?A\.?|M\.?S\.?|M\.?A\.?|Ph\.?D\.?|MBA|Bachelor|Master|Doctorate)\b",
            r"\b(University|College|Institute|School)\s+of\s+\w+",
            r"\b(Computer Science|Data Science|Mathematics|Statistics|Engineering|Physics|Chemistry|Biology|Cybersecurity)\b",
        ]

        for pattern in education_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["education"].extend(matches)

        entities["education"] = list(set(entities["education"]))

        return entities

    def calculate_experience_years(self, text: str) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Calculate total professional experience by MERGING OVERLAPPING EMPLOYMENT PERIODS.
        Uses dynamic system date (never a hard-coded year).
        """
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        current_decimal = current_year + current_month / 12.0

        raw_ranges: List[Tuple[float, float, str]] = []

        # 1. Month-Year to Month-Year or Present
        # e.g., "March 2021 - Present", "Jun 2018 - Feb 2021"
        month_names = "jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|sept|oct|october|nov|november|dec|december"
        p_month = re.compile(
            rf"(?i)\b({month_names})\.?,?\s*(\d{{4}})\s*[-–—/to]+\s*(?:({month_names})\.?,?\s*(\d{{4}})|(present|current|now))\b"
        )
        for m in p_month.finditer(text):
            s_month_str, s_year_str, e_month_str, e_year_str, pres_str = m.groups()
            s_year = int(s_year_str)
            s_month = self.MONTH_MAP.get(s_month_str.lower(), 1)
            start_val = s_year + (s_month - 1) / 12.0

            if pres_str:
                end_val = current_decimal
                end_label = "Present"
            else:
                e_year = int(e_year_str)
                e_month = self.MONTH_MAP.get(e_month_str.lower(), 12)
                end_val = e_year + e_month / 12.0
                end_label = f"{e_month_str.capitalize()} {e_year}"

            if 1980 <= s_year <= current_year and start_val <= end_val:
                raw_ranges.append((start_val, end_val, f"{s_month_str.capitalize()} {s_year} – {end_label}"))

        # 2. Year to Year or Present (when month wasn't matched)
        p_year = re.compile(
            r"\b(19\d{2}|20\d{2})\s*[-–—/to]+\s*(19\d{2}|20\d{2}|present|current|now)\b",
            re.IGNORECASE,
        )
        for m in p_year.finditer(text):
            s_year_str, e_year_str = m.groups()
            s_year = int(s_year_str)
            start_val = float(s_year)

            if e_year_str.lower() in ["present", "current", "now"]:
                end_val = current_decimal
                end_label = "Present"
            else:
                e_year = int(e_year_str)
                end_val = float(e_year)
                end_label = str(e_year)

            # Avoid adding if an existing month-precision range already covers roughly this same window
            already_covered = any(abs(r[0] - start_val) < 1.0 and abs(r[1] - end_val) < 1.0 for r in raw_ranges)
            if not already_covered and 1980 <= s_year <= current_year and start_val <= end_val:
                raw_ranges.append((start_val, end_val, f"{s_year} – {end_label}"))

        if not raw_ranges:
            return 0.0, []

        # Sort and MERGE OVERLAPPING INTERVALS
        sorted_intervals = sorted(raw_ranges, key=lambda x: x[0])
        merged_intervals: List[Tuple[float, float]] = []

        for start_val, end_val, _ in sorted_intervals:
            if not merged_intervals:
                merged_intervals.append((start_val, end_val))
            else:
                prev_start, prev_end = merged_intervals[-1]
                # If current interval overlaps or is immediately adjacent (within 2 months)
                if start_val <= prev_end + (2.0 / 12.0):
                    merged_intervals[-1] = (prev_start, max(prev_end, end_val))
                else:
                    merged_intervals.append((start_val, end_val))

        total_years = sum(end - start for start, end in merged_intervals)
        total_years = round(min(total_years, 45.0), 1)

        experiences_list = [
            {
                "start": int(r[0]),
                "end": int(r[1]) if r[1] < current_year else current_year,
                "years": round(r[1] - r[0], 1),
                "label": r[2],
            }
            for r in raw_ranges
        ]

        return total_years, experiences_list

    def analyze_bullet_points(self, text_or_bullets: Any) -> Dict[str, Any]:
        """
        Analyze bullet points for action verbs, measurable metrics, and quality.
        Does NOT fabricate accomplishments or metrics.
        """
        if isinstance(text_or_bullets, list):
            bullets = text_or_bullets
        else:
            bullets = []
            for line in str(text_or_bullets).split("\n"):
                clean = line.strip()
                if clean.startswith(("-", "*", "•", "–", "—")) or re.match(r"^\d+\.", clean):
                    bullet_text = re.sub(r"^[-*•–—\d\.]+\s*", "", clean).strip()
                    if len(bullet_text) > 10:
                        bullets.append(bullet_text)

        if not bullets:
            return {
                "total_bullets": 0,
                "bullets_with_metrics": 0,
                "metric_percentage": 0.0,
                "strong_bullets": [],
                "moderate_bullets": [],
                "weak_bullets": [],
                "recommendations": ["Consider organizing your work history with clear bullet points."],
            }

        # Metric patterns: %, $, scale numbers, latencies, time savings
        metric_pattern = re.compile(
            r"(?:\d+(?:\.\d+)?%|\$\d+(?:\.\d+)?[kKmMbB]?|\b\d{1,3}(?:,\d{3})+\b|\b\d+\+?\s*(?:users|clients|teams|projects|engineers|services|endpoints|servers|requests|transactions|cves|tickets|hours|days|weeks|months|minutes|ms|seconds)\b|\b(?:increased|reduced|boosted|saved|decreased|cut)\b[^\.\n]*?\b\d+)",
            re.IGNORECASE,
        )

        strong = []
        moderate = []
        weak = []

        for b in bullets:
            has_metric = bool(metric_pattern.search(b))
            first_word = b.split()[0].lower().strip(",.;:") if b.split() else ""
            has_action_verb = first_word in self.ACTION_VERBS or any(b.lower().startswith(v + " ") for v in self.ACTION_VERBS)

            if has_action_verb and has_metric:
                strong.append(b)
            elif has_action_verb or has_metric:
                moderate.append(b)
            else:
                weak.append(b)

        with_metrics_count = len(strong) + sum(1 for b in moderate if metric_pattern.search(b))
        metric_pct = round((with_metrics_count / max(len(bullets), 1)) * 100, 1)

        recommendations = []
        if metric_pct < 40:
            recommendations.append(
                "If you have quantifiable results available (e.g. % performance increase, revenue impact, time saved), consider adding them to your experience bullets."
            )
        if len(weak) > len(strong):
            recommendations.append(
                "Begin each bullet with a strong past-tense action verb (e.g. 'Architected', 'Spearheaded', 'Engineered') to highlight direct contributions."
            )

        return {
            "total_bullets": len(bullets),
            "bullets_with_metrics": with_metrics_count,
            "metric_percentage": metric_pct,
            "strong_bullets": strong,
            "moderate_bullets": moderate,
            "weak_bullets": weak,
            "recommendations": recommendations,
        }

    def analyze_text_quality(self, text: str) -> Dict[str, Any]:
        """
        Analyze text quality metrics including keyword repetition and stuffing signals.
        """
        words = text.split()
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        word_count = len(words)
        sentence_count = len(sentences)
        avg_word_length = sum(len(w) for w in words) / max(word_count, 1)
        avg_sentence_length = word_count / max(sentence_count, 1)

        unique_words = set(w.lower() for w in words)
        ttr = len(unique_words) / max(word_count, 1)

        found_action_verbs = list(
            set([w.lower().strip(",.;:") for w in words if w.lower().strip(",.;:") in self.ACTION_VERBS])
        )
        action_verb_count = len(found_action_verbs)
        action_verb_ratio = action_verb_count / max(word_count, 1) * 100

        # Check for repetitive keywords / keyword stuffing
        word_counts: Dict[str, int] = {}
        stop_words = {
            "the", "and", "to", "of", "a", "in", "for", "is", "on", "that", "by",
            "this", "with", "i", "you", "it", "not", "or", "be", "are", "from",
            "at", "as", "your", "all", "have", "new", "more", "an", "was", "we",
            "will", "my", "our", "their", "so", "if"
        }
        for w in words:
            wl = w.lower().strip(",.;:()[]{}'\"")
            if len(wl) > 2 and wl not in stop_words:
                word_counts[wl] = word_counts.get(wl, 0) + 1

        stuffing_warnings = []
        for word, count in word_counts.items():
            ratio = count / max(word_count, 1)
            if count >= 8 and ratio >= 0.035:
                stuffing_warnings.append(
                    f"Word '{word}' is repeated {count} times ({ratio*100:.1f}% of text). "
                    "Suspicious repetition may trigger ATS keyword-stuffing penalties."
                )

        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_word_length": round(avg_word_length, 2),
            "avg_sentence_length": round(avg_sentence_length, 2),
            "vocabulary_richness": round(ttr, 3),
            "action_verb_count": action_verb_count,
            "action_verb_percentage": round(action_verb_ratio, 2),
            "found_action_verbs": sorted(found_action_verbs),
            "keyword_stuffing_warnings": stuffing_warnings,
        }

    def get_skill_summary(self, text: str) -> Dict[str, Any]:
        """
        Get comprehensive skill summary.
        """
        skills = self.extract_skills(text)
        total_skills = sum(len(v) for v in skills.values())
        category_counts = {k: len(v) for k, v in skills.items()}

        top_by_category = {}
        for category, skill_list in skills.items():
            top_by_category[category] = skill_list[:5]

        return {
            "total_skills": total_skills,
            "category_counts": category_counts,
            "skills_by_category": skills,
            "top_by_category": top_by_category,
        }
