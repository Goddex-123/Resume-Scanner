"""
Dataset Generation & Validation Module
Generates synthetic resume-JD matching datasets for ML training and evaluation.

IMPORTANT: The generated dataset is SYNTHETIC — it uses template-based variation
to create diverse resume-JD pairs across 5 domains. This is explicitly documented
and NOT presented as real-world labeled data. The infrastructure supports swapping
in a real labeled dataset with the same schema.
"""

import random
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

import numpy as np

logger = logging.getLogger(__name__)

# ── Domain Templates ──────────────────────────────────────────────────────────

DOMAIN_TEMPLATES = {
    "data_science": {
        "title_variations": [
            "Data Scientist", "Senior Data Scientist", "ML Engineer",
            "Applied Data Scientist", "Data Scientist (NLP)",
        ],
        "core_skills": [
            "Python", "pandas", "numpy", "scikit-learn", "SQL",
            "TensorFlow", "PyTorch", "statistics", "machine learning",
            "data visualization", "Jupyter", "deep learning",
        ],
        "extended_skills": [
            "NLP", "computer vision", "MLflow", "Docker", "AWS",
            "Spark", "A/B testing", "feature engineering", "Keras",
            "XGBoost", "LightGBM", "Hugging Face", "NLTK", "spaCy",
        ],
        "experience_templates": [
            "Built predictive ML models achieving {metric}% accuracy on production data",
            "Developed NLP pipeline processing {volume}K+ documents daily",
            "Designed A/B testing framework reducing decision time by {metric}%",
            "Implemented feature engineering pipeline increasing model F1 by {metric} points",
            "Deployed ML models to production serving {volume}K+ predictions/day",
        ],
        "jd_responsibilities": [
            "Develop and deploy machine learning models for business optimization",
            "Analyze large datasets to extract actionable insights",
            "Collaborate with engineering teams to productionize ML pipelines",
            "Design experiments and A/B tests to validate hypotheses",
            "Present data-driven findings to stakeholders",
        ],
    },
    "software_engineering": {
        "title_variations": [
            "Software Engineer", "Senior Software Engineer", "Backend Engineer",
            "Full-Stack Developer", "Software Developer",
        ],
        "core_skills": [
            "Python", "Java", "JavaScript", "Git", "SQL",
            "REST API", "Docker", "CI/CD", "agile", "testing",
            "microservices", "system design",
        ],
        "extended_skills": [
            "Kubernetes", "AWS", "TypeScript", "React", "Node.js",
            "PostgreSQL", "Redis", "GraphQL", "Go", "C++",
            "Kafka", "gRPC", "Terraform", "Linux",
        ],
        "experience_templates": [
            "Designed microservices architecture handling {volume}K+ requests/second",
            "Reduced API latency by {metric}% through query optimization",
            "Implemented CI/CD pipeline cutting deployment time by {metric}%",
            "Led migration of monolith to {volume} microservices",
            "Built automated testing framework achieving {metric}% code coverage",
        ],
        "jd_responsibilities": [
            "Design and implement scalable backend services",
            "Write clean, maintainable code with comprehensive test coverage",
            "Participate in code reviews and architectural discussions",
            "Debug and resolve production issues under tight deadlines",
            "Collaborate with product and design teams in agile sprints",
        ],
    },
    "cybersecurity": {
        "title_variations": [
            "Cybersecurity Analyst", "Security Engineer", "SOC Analyst",
            "Penetration Tester", "Information Security Analyst",
        ],
        "core_skills": [
            "SIEM", "Splunk", "Wireshark", "Python", "Linux",
            "network security", "incident response", "vulnerability assessment",
            "firewalls", "penetration testing", "OWASP", "TCP/IP",
        ],
        "extended_skills": [
            "Metasploit", "Burp Suite", "Nmap", "MITRE ATT&CK",
            "CISSP", "CompTIA Security+", "cloud security", "AWS",
            "threat intelligence", "malware analysis", "IDS/IPS",
            "YARA", "Sigma", "digital forensics", "SOC operations",
        ],
        "experience_templates": [
            "Monitored and triaged {volume}+ security alerts daily in enterprise SOC",
            "Conducted {volume}+ penetration tests identifying critical vulnerabilities",
            "Reduced incident response time by {metric}% through automated playbooks",
            "Developed custom SIEM detection rules catching {metric}% more threats",
            "Led security audit achieving {metric}% compliance across infrastructure",
        ],
        "jd_responsibilities": [
            "Monitor security alerts and triage potential incidents",
            "Conduct vulnerability assessments and penetration testing",
            "Develop and maintain security monitoring and detection rules",
            "Coordinate incident response and post-mortem analysis",
            "Ensure compliance with security frameworks and regulations",
        ],
    },
    "web_development": {
        "title_variations": [
            "Web Developer", "Frontend Developer", "Full-Stack Developer",
            "React Developer", "Senior Web Engineer",
        ],
        "core_skills": [
            "JavaScript", "TypeScript", "React", "HTML", "CSS",
            "Node.js", "Git", "REST API", "responsive design",
            "webpack", "PostgreSQL", "agile",
        ],
        "extended_skills": [
            "Next.js", "Vue.js", "Redux", "GraphQL", "Tailwind CSS",
            "Docker", "Jest", "Cypress", "MongoDB", "Express",
            "Web accessibility", "performance optimization", "PWA",
            "Figma", "Storybook",
        ],
        "experience_templates": [
            "Built responsive web application serving {volume}K+ monthly active users",
            "Improved Core Web Vitals scores by {metric}% through bundle optimization",
            "Developed component library used across {volume} product teams",
            "Reduced page load time by {metric}% through code splitting and lazy loading",
            "Implemented real-time features handling {volume}K+ concurrent WebSocket connections",
        ],
        "jd_responsibilities": [
            "Build responsive, accessible web applications with modern frameworks",
            "Develop reusable UI components and front-end libraries",
            "Optimize application performance and bundle sizes",
            "Collaborate with designers to translate mockups into pixel-perfect interfaces",
            "Write unit and integration tests for frontend and backend code",
        ],
    },
    "data_engineering": {
        "title_variations": [
            "Data Engineer", "Senior Data Engineer", "ETL Developer",
            "Data Platform Engineer", "Analytics Engineer",
        ],
        "core_skills": [
            "Python", "SQL", "Spark", "Airflow", "ETL",
            "data warehouse", "AWS", "data modeling",
            "Kafka", "pipeline", "BigQuery", "Snowflake",
        ],
        "extended_skills": [
            "Redshift", "dbt", "Terraform", "Docker", "Kubernetes",
            "Hadoop", "Hive", "streaming", "Delta Lake", "GCP",
            "Azure", "Databricks", "data governance", "Presto",
        ],
        "experience_templates": [
            "Designed ETL pipelines processing {volume}TB+ data daily",
            "Reduced data pipeline latency by {metric}% through Spark optimization",
            "Built real-time streaming platform processing {volume}M+ events/hour",
            "Migrated legacy warehouse to cloud achieving {metric}% cost reduction",
            "Implemented data quality framework catching {metric}% of anomalies before production",
        ],
        "jd_responsibilities": [
            "Design and maintain scalable data pipelines and ETL processes",
            "Build and optimize data warehouse solutions",
            "Implement data quality monitoring and governance frameworks",
            "Collaborate with data scientists to enable ML workflows",
            "Manage cloud data infrastructure and cost optimization",
        ],
    },
}


def _generate_resume_text(
    domain: str,
    skill_subset_ratio: float = 0.8,
    experience_years: int = 4,
    education: str = "Bachelor's",
    seed: Optional[int] = None,
) -> str:
    """Generate a synthetic resume text from domain templates."""
    if seed is not None:
        random.seed(seed)

    template = DOMAIN_TEMPLATES[domain]
    title = random.choice(template["title_variations"])

    # Select skill subset
    n_core = max(3, int(len(template["core_skills"]) * skill_subset_ratio))
    n_ext = max(1, int(len(template["extended_skills"]) * skill_subset_ratio * 0.6))
    skills = random.sample(template["core_skills"], min(n_core, len(template["core_skills"])))
    skills += random.sample(template["extended_skills"], min(n_ext, len(template["extended_skills"])))

    # Generate experience bullets
    n_bullets = random.randint(3, 5)
    bullets = []
    for tmpl in random.sample(template["experience_templates"], min(n_bullets, len(template["experience_templates"]))):
        metric = random.randint(15, 95)
        volume = random.choice([10, 50, 100, 500])
        bullets.append(tmpl.format(metric=metric, volume=volume))

    sections = [
        f"PROFESSIONAL SUMMARY",
        f"Experienced {title} with {experience_years}+ years of hands-on experience in "
        f"{', '.join(skills[:3])} and related technologies.",
        "",
        f"SKILLS",
        f"{', '.join(skills)}",
        "",
        f"EXPERIENCE",
        f"{title} | Tech Company | 20{max(10, 24 - experience_years)}-Present",
    ]
    for b in bullets:
        sections.append(f"• {b}")

    sections.extend([
        "",
        "EDUCATION",
        f"{education} Degree in Computer Science",
        "University | Graduated 2020",
    ])

    # Add certifications for some resumes
    if random.random() > 0.5:
        sections.extend([
            "",
            "CERTIFICATIONS",
            random.choice([
                "AWS Certified Solutions Architect",
                "Google Cloud Professional Data Engineer",
                "Certified Kubernetes Administrator (CKA)",
                "CompTIA Security+ Certified",
                "PMP Certified",
            ]),
        ])

    return "\n".join(sections)


def _generate_jd_text(
    domain: str,
    experience_required: int = 3,
    education: str = "Bachelor's",
    skill_subset_ratio: float = 0.8,
    seed: Optional[int] = None,
) -> str:
    """Generate a synthetic job description from domain templates."""
    if seed is not None:
        random.seed(seed)

    template = DOMAIN_TEMPLATES[domain]
    title = random.choice(template["title_variations"])

    n_req = max(3, int(len(template["core_skills"]) * skill_subset_ratio))
    n_pref = max(2, int(len(template["extended_skills"]) * skill_subset_ratio * 0.5))
    required = random.sample(template["core_skills"], min(n_req, len(template["core_skills"])))
    preferred = random.sample(template["extended_skills"], min(n_pref, len(template["extended_skills"])))

    responsibilities = random.sample(
        template["jd_responsibilities"],
        min(4, len(template["jd_responsibilities"])),
    )

    jd = [
        f"Job Title: {title}",
        f"Company: Tech Corp",
        f"Experience Required: {experience_required}+ years",
        "",
        "Requirements:",
    ]
    for skill in required:
        jd.append(f"- Proficiency in {skill}")
    jd.append(f"- {education} degree in Computer Science or related field")
    jd.append("")
    jd.append("Preferred Qualifications:")
    for skill in preferred:
        jd.append(f"- Experience with {skill}")
    jd.append("")
    jd.append("Responsibilities:")
    for resp in responsibilities:
        jd.append(f"- {resp}")

    return "\n".join(jd)


@dataclass
class DatasetEntry:
    """A single resume-JD pair with metadata."""
    resume_id: str
    job_id: str
    resume_text: str
    job_description: str
    match_label: int  # 1 = good match, 0 = poor match
    domain: str
    job_title: str = ""


class ResumeJDDatasetGenerator:
    """
    Generates synthetic resume-JD matching datasets for ML training.

    Creates positive (matching domain) and negative (cross-domain) pairs
    across 5 career domains with controlled variation.

    IMPORTANT: This generates SYNTHETIC data for model development.
    Results and metrics are honestly reported as synthetic-data performance.
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.domains = list(DOMAIN_TEMPLATES.keys())

    def generate(
        self,
        pairs_per_domain: int = 40,
        negative_ratio: float = 1.0,
    ) -> List[DatasetEntry]:
        """
        Generate a balanced dataset of resume-JD pairs.

        Args:
            pairs_per_domain: Number of positive pairs per domain.
            negative_ratio: Ratio of negative to positive pairs (1.0 = balanced).

        Returns:
            List of DatasetEntry objects.
        """
        random.seed(self.seed)
        np.random.seed(self.seed)

        entries: List[DatasetEntry] = []
        resume_counter = 0
        jd_counter = 0

        for domain in self.domains:
            # Generate positive pairs (same domain, varying skill overlap)
            for i in range(pairs_per_domain):
                resume_counter += 1
                jd_counter += 1

                skill_ratio = random.uniform(0.5, 1.0)
                exp_years = random.randint(2, 10)
                exp_required = random.randint(1, max(1, exp_years - 1))
                education = random.choice(["Bachelor's", "Master's"])

                resume = _generate_resume_text(
                    domain,
                    skill_subset_ratio=skill_ratio,
                    experience_years=exp_years,
                    education=education,
                    seed=self.seed + resume_counter,
                )
                jd = _generate_jd_text(
                    domain,
                    experience_required=exp_required,
                    education=education,
                    skill_subset_ratio=skill_ratio,
                    seed=self.seed + jd_counter + 10000,
                )

                entries.append(DatasetEntry(
                    resume_id=f"resume_{resume_counter:04d}",
                    job_id=f"jd_{jd_counter:04d}",
                    resume_text=resume,
                    job_description=jd,
                    match_label=1,
                    domain=domain,
                    job_title=DOMAIN_TEMPLATES[domain]["title_variations"][0],
                ))

            # Generate negative pairs (cross-domain)
            n_negative = int(pairs_per_domain * negative_ratio)
            other_domains = [d for d in self.domains if d != domain]

            for i in range(n_negative):
                resume_counter += 1
                jd_counter += 1

                other_domain = random.choice(other_domains)
                skill_ratio = random.uniform(0.4, 0.9)
                exp_years = random.randint(1, 8)

                resume = _generate_resume_text(
                    domain,
                    skill_subset_ratio=skill_ratio,
                    experience_years=exp_years,
                    seed=self.seed + resume_counter,
                )
                jd = _generate_jd_text(
                    other_domain,
                    experience_required=random.randint(2, 6),
                    seed=self.seed + jd_counter + 10000,
                )

                entries.append(DatasetEntry(
                    resume_id=f"resume_{resume_counter:04d}",
                    job_id=f"jd_{jd_counter:04d}",
                    resume_text=resume,
                    job_description=jd,
                    match_label=0,
                    domain=domain,
                    job_title=DOMAIN_TEMPLATES[other_domain]["title_variations"][0],
                ))

        random.shuffle(entries)
        logger.info(
            "Generated %d resume-JD pairs (%d positive, %d negative)",
            len(entries),
            sum(1 for e in entries if e.match_label == 1),
            sum(1 for e in entries if e.match_label == 0),
        )
        return entries


class DatasetValidator:
    """
    Validates a resume-JD matching dataset for quality and integrity.
    """

    def validate(self, entries: List[DatasetEntry]) -> Dict[str, Any]:
        """
        Run all validation checks and return a quality report.

        Returns:
            Dict with validation results and statistics.
        """
        report: Dict[str, Any] = {
            "total_pairs": len(entries),
            "positive_pairs": sum(1 for e in entries if e.match_label == 1),
            "negative_pairs": sum(1 for e in entries if e.match_label == 0),
            "unique_resumes": len(set(e.resume_id for e in entries)),
            "unique_jds": len(set(e.job_id for e in entries)),
            "domains": sorted(set(e.domain for e in entries)),
            "issues": [],
        }

        # Class distribution
        total = report["total_pairs"]
        if total == 0:
            report["issues"].append("Dataset is empty")
            return report

        pos_ratio = report["positive_pairs"] / total
        report["positive_ratio"] = round(pos_ratio, 3)
        if pos_ratio < 0.3 or pos_ratio > 0.7:
            report["issues"].append(
                f"Class imbalance detected: {pos_ratio:.1%} positive"
            )

        # Check for missing text
        missing_resume = sum(
            1 for e in entries if not e.resume_text or len(e.resume_text.strip()) < 50
        )
        missing_jd = sum(
            1 for e in entries if not e.job_description or len(e.job_description.strip()) < 50
        )
        if missing_resume:
            report["issues"].append(f"{missing_resume} entries have missing/short resume text")
        if missing_jd:
            report["issues"].append(f"{missing_jd} entries have missing/short JD text")

        # Check for invalid labels
        invalid_labels = sum(
            1 for e in entries if e.match_label not in (0, 1)
        )
        if invalid_labels:
            report["issues"].append(f"{invalid_labels} entries have invalid labels")

        # Check for duplicate resume-JD pairs
        pair_keys = [(e.resume_id, e.job_id) for e in entries]
        n_unique_pairs = len(set(pair_keys))
        if n_unique_pairs < len(entries):
            report["issues"].append(
                f"{len(entries) - n_unique_pairs} duplicate resume-JD pairs found"
            )

        # Domain distribution
        domain_counts: Dict[str, int] = {}
        for e in entries:
            domain_counts[e.domain] = domain_counts.get(e.domain, 0) + 1
        report["domain_distribution"] = domain_counts

        report["is_valid"] = len(report["issues"]) == 0

        return report


def create_train_test_split(
    entries: List[DatasetEntry],
    test_size: float = 0.2,
    seed: int = 42,
) -> Tuple[List[DatasetEntry], List[DatasetEntry]]:
    """
    Split dataset into train and test sets with data leakage prevention.

    Uses resume_id grouping to ensure the same resume never appears in
    both train and test sets, preventing information leakage.

    Args:
        entries: List of DatasetEntry objects.
        test_size: Fraction of data for testing.
        seed: Random seed for reproducibility.

    Returns:
        Tuple of (train_entries, test_entries).
    """
    random.seed(seed)

    # Group entries by resume_id
    resume_groups: Dict[str, List[DatasetEntry]] = {}
    for entry in entries:
        resume_groups.setdefault(entry.resume_id, []).append(entry)

    # Shuffle groups and split
    group_ids = list(resume_groups.keys())
    random.shuffle(group_ids)

    n_test_groups = max(1, int(len(group_ids) * test_size))
    test_group_ids = set(group_ids[:n_test_groups])

    train_entries = []
    test_entries = []

    for gid, group_entries in resume_groups.items():
        if gid in test_group_ids:
            test_entries.extend(group_entries)
        else:
            train_entries.extend(group_entries)

    logger.info(
        "Split: %d train (%d groups), %d test (%d groups)",
        len(train_entries),
        len(group_ids) - n_test_groups,
        len(test_entries),
        n_test_groups,
    )

    return train_entries, test_entries
