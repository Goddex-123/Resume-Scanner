"""
Unit tests for the 3 Multi-Field Demo Resumes feature.
Tests file existence, ATS scoring, NLP skill extraction, and Job Matching across:
- Cybersecurity
- Web Development
- Data Science
"""

import os
from resume_scanner import NLPEngine, ATSScorer, JobMatcher
from app import DEMO_PROFILES, SAMPLES_DIR


def test_demo_files_exist():
    """Verify that all 3 demo resume files exist and have substantial content."""
    expected_files = [
        "sample_resume_cybersecurity.txt",
        "sample_resume_web_developer.txt",
        "sample_resume_data_science.txt",
    ]
    for filename in expected_files:
        filepath = os.path.join(SAMPLES_DIR, filename)
        assert os.path.isfile(filepath), f"Missing demo file: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            assert len(content) > 500, f"Demo file {filename} is suspiciously short: {len(content)} chars"


def test_demo_profiles_registry():
    """Verify that DEMO_PROFILES in app.py has entries for all 3 required fields."""
    assert "cybersecurity" in DEMO_PROFILES
    assert "web_dev" in DEMO_PROFILES
    assert "data_science" in DEMO_PROFILES

    for key, profile in DEMO_PROFILES.items():
        assert os.path.isfile(profile["file"]), f"Profile {key} points to non-existent file {profile['file']}"
        assert profile["candidate_name"]
        assert profile["title"]
        assert len(profile["skills"]) >= 4


def test_cybersecurity_resume_analysis():
    """Test full analysis pipeline for Alex Rivera (Cybersecurity)."""
    cyber_file = os.path.join(SAMPLES_DIR, "sample_resume_cybersecurity.txt")
    with open(cyber_file, "r", encoding="utf-8") as f:
        text = f.read()

    # 1. ATS Scoring
    scorer = ATSScorer()
    ats_res = scorer.calculate_score(text)
    assert ats_res["scores"]["total"] >= 65, f"ATS score too low: {ats_res['scores']['total']}"

    # 2. NLP Skill extraction
    nlp = NLPEngine(use_spacy=False)
    skills = nlp.extract_skills(text)
    flat_skills = [s.lower() for cat in skills.values() for s in cat]
    assert any("splunk" in s for s in flat_skills), "Splunk not extracted"
    assert any("wireshark" in s for s in flat_skills), "Wireshark not extracted"
    assert any("penetration testing" in s for s in flat_skills), "Penetration Testing not extracted"

    # 3. Job Matching
    matcher = JobMatcher()
    match_res = matcher.match(text)
    top_roles = [m["role"] for m in match_res["all_matches"][:3]]
    assert "Cybersecurity Analyst" in top_roles, f"Cybersecurity Analyst not in top matches: {top_roles}"


def test_web_developer_resume_analysis():
    """Test full analysis pipeline for David Kim (Web Developer)."""
    web_file = os.path.join(SAMPLES_DIR, "sample_resume_web_developer.txt")
    with open(web_file, "r", encoding="utf-8") as f:
        text = f.read()

    # 1. ATS Scoring
    scorer = ATSScorer()
    ats_res = scorer.calculate_score(text)
    assert ats_res["scores"]["total"] >= 65, f"ATS score too low: {ats_res['scores']['total']}"

    # 2. NLP Skill extraction
    nlp = NLPEngine(use_spacy=False)
    skills = nlp.extract_skills(text)
    flat_skills = [s.lower() for cat in skills.values() for s in cat]
    assert any("react" in s for s in flat_skills), "React not extracted"
    assert any("typescript" in s for s in flat_skills), "TypeScript not extracted"
    assert any("next.js" in s for s in flat_skills), "Next.js not extracted"

    # 3. Job Matching
    matcher = JobMatcher()
    match_res = matcher.match(text)
    top_roles = [m["role"] for m in match_res["all_matches"][:3]]
    assert "Web Developer" in top_roles, f"Web Developer not in top matches: {top_roles}"


def test_data_science_resume_analysis():
    """Test full analysis pipeline for Sarah Chen (Data Scientist)."""
    ds_file = os.path.join(SAMPLES_DIR, "sample_resume_data_science.txt")
    with open(ds_file, "r", encoding="utf-8") as f:
        text = f.read()

    # 1. ATS Scoring
    scorer = ATSScorer()
    ats_res = scorer.calculate_score(text)
    assert ats_res["scores"]["total"] >= 65, f"ATS score too low: {ats_res['scores']['total']}"

    # 2. Job Matching
    matcher = JobMatcher()
    match_res = matcher.match(text)
    top_roles = [m["role"] for m in match_res["all_matches"][:3]]
    has_match = any("Data Scientist" in r or "ML Engineer" in r for r in top_roles)
    assert has_match, f"Data roles not in top matches: {top_roles}"
