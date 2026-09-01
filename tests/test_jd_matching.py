"""
Unit tests for JobDescriptionAnalyzer and direct JobMatcher matching.
"""

from resume_scanner.jd_analyzer import JobDescriptionAnalyzer
from resume_scanner.job_matcher import JobMatcher


def test_job_description_analyzer_sections():
    analyzer = JobDescriptionAnalyzer()
    sample_jd = """
    Job Title: Senior Data Scientist
    Experience: 4+ years of professional experience.

    Requirements:
    - Python, SQL, and Pandas
    - Deep learning experience with PyTorch or TensorFlow

    Preferred Qualifications:
    - Experience with Docker and AWS
    - Knowledge of Kubernetes and MLOps

    Responsibilities:
    - Build production ML pipelines
    - Lead predictive modeling initiatives
    """
    jd = analyzer.analyze(sample_jd, title="Senior Data Scientist")
    assert jd.title == "Senior Data Scientist"
    assert jd.experience_years_required == 4.0

    # Required skills
    req_lower = [s.lower() for s in jd.required_skills]
    assert "python" in req_lower
    assert "sql" in req_lower
    assert any("pytorch" in s.lower() or "tensorflow" in s.lower() for s in req_lower)

    # Preferred skills
    pref_lower = [s.lower() for s in jd.preferred_skills]
    assert any("docker" in s.lower() or "aws" in s.lower() for s in pref_lower)


def test_direct_resume_to_jd_matching():
    matcher = JobMatcher()
    resume = """
    Sarah Chen
    Data Scientist with 5 years experience.
    Skills: Python, SQL, Pandas, PyTorch, Scikit-Learn.
    Experience:
    2019 - 2024: Built deep learning models with PyTorch.
    Education:
    Master of Science in Computer Science
    """
    sample_jd = """
    Requirements:
    - Python and PyTorch
    - SQL database querying
    - Kubernetes and Docker
    Preferred:
    - Scikit-Learn and AWS
    Experience: 3+ years
    """
    result = matcher.match_resume_to_jd(resume, sample_jd, "Data Scientist")
    assert result["overall_match"] > 50.0

    matched_req = [s.lower() for s in result["matched_required_skills"]]
    assert "python" in matched_req
    assert "pytorch" in matched_req
    assert "sql" in matched_req

    missing_req = [s.lower() for s in result["missing_required_skills"]]
    assert any("kubernetes" in s or "docker" in s for s in missing_req)

    # Verify disclaimer is present
    assert "disclaimer" in result
    assert "NOT a prediction" in result["disclaimer"]
