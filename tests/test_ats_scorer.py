"""
Unit tests for ATSScorer: explainable scoring, keyword stuffing detection,
quantifiable achievements, and ethical recommendations.
"""

from resume_scanner.ats_scorer import ATSScorer
from resume_scanner.config import ATSScoringConfig


def test_ats_scorer_components_and_config():
    custom_config = ATSScoringConfig(pass_threshold=65)
    scorer = ATSScorer(config=custom_config)

    resume = """
    Alex Rivera
    Email: alex@example.com | Phone: 555-123-4567 | LinkedIn: linkedin.com/in/alexrivera | GitHub: github.com/alexrivera
    SUMMARY
    Senior cybersecurity analyst with 5 years experience.
    WORK EXPERIENCE
    Lead SOC Analyst (2020 - Present)
    - Deployed Splunk SIEM rules across 500 servers reducing incident response time by 45%.
    - Conducted penetration tests with Wireshark and Metasploit, identifying 12 critical vulnerabilities.
    EDUCATION
    B.S. in Computer Science
    SKILLS
    Python, Splunk, Wireshark, Metasploit, Linux, Network Security
    """
    res = scorer.calculate_score(resume, target_role="cybersecurity_analyst")
    scores = res["scores"]

    assert scores["total"] >= 70
    assert scores["sections"] >= 60.0
    assert scores["contact"] == 100.0
    assert scores["achievements"] >= 70.0
    assert "disclaimer" in res


def test_keyword_stuffing_penalty_in_ats():
    scorer = ATSScorer()
    # Resume where 'python' is repeated excessively
    stuffed_resume = """
    John Doe
    Email: john@test.com | Phone: 555-111-2222
    Python Python Python Python Python Python Python Python Python Python
    Python Python Python Python Python Python Python Python Python Python
    EXPERIENCE
    Python developer
    EDUCATION
    BS Computer Science
    SKILLS
    Python
    """
    res = scorer.calculate_score(stuffed_resume, target_role="software_engineer")
    assert len(res["stuffing_warnings"]) > 0


def test_ethical_recommendations_wording():
    scorer = ATSScorer()
    # Resume missing some standard data science keywords
    resume = """
    Sarah Chen
    Email: sarah@data.org | Phone: 555-987-6543
    EXPERIENCE
    Data Analyst
    EDUCATION
    B.S. Statistics
    SKILLS
    SQL, Excel, Tableau
    """
    res = scorer.calculate_score(resume, target_role="data_scientist")
    feedback = res["feedback"]

    # Check for ethical phrasing rule: "If you genuinely have experience with X, consider highlighting it"
    ethical_found = any("If you genuinely have experience" in fb for fb in feedback)
    assert ethical_found
