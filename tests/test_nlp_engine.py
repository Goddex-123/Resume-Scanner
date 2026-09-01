"""
Unit tests for NLPEngine: skill normalization, experience interval merging,
and achievement/bullet analysis.
"""

from resume_scanner.nlp_engine import NLPEngine


def test_boundary_safe_skill_extraction():
    nlp = NLPEngine(use_spacy=False)
    text = "Proficient in C++, C#, .NET, and Python. Experience with C programming."
    skills = nlp.extract_skills(text)
    langs = skills.get("programming_languages", [])

    assert "C++" in langs
    assert "C#" in langs
    assert "Python" in langs
    assert "C" in langs


def test_skill_alias_normalization():
    nlp = NLPEngine(use_spacy=False)
    text = "Hands-on experience with sklearn, k8s, postgres, and nodejs."
    skills_flat = nlp.get_all_skills_flat(text)

    # Aliases should be mapped to canonical titles
    assert "Scikit-Learn" in skills_flat
    assert "Kubernetes" in skills_flat
    assert "PostgreSQL" in skills_flat
    assert "Node.js" in skills_flat


def test_overlapping_experience_interval_merging():
    nlp = NLPEngine(use_spacy=False)
    # Two overlapping roles:
    # Role A: 2020 to 2023 (3 years)
    # Role B: 2021 to 2024 (3 years)
    # Without merging: 3 + 3 = 6 years (wrong)
    # With merging: 2020 to 2024 = 4.0 years (correct)
    text = """
    EXPERIENCE
    Lead Security Architect
    2020 - 2023
    Cyber Consultant (Concurrent)
    2021 - 2024
    """
    total_years, entries = nlp.calculate_experience_years(text)
    assert total_years == 4.0
    assert len(entries) == 2


def test_bullet_points_and_achievement_analysis():
    nlp = NLPEngine(use_spacy=False)
    text = """
    - Architected a distributed streaming pipeline processing 250,000 requests/sec with 99.99% uptime.
    - Led cross-functional engineering sprints and conducted weekly code reviews.
    - Responsible for general system maintenance and tasks.
    """
    result = nlp.analyze_bullet_points(text)
    assert result["total_bullets"] == 3
    assert result["bullets_with_metrics"] == 1
    assert len(result["strong_bullets"]) == 1
    assert "Architected" in result["strong_bullets"][0]
    assert len(result["moderate_bullets"]) == 1
    assert len(result["weak_bullets"]) == 1


def test_keyword_stuffing_detection():
    nlp = NLPEngine(use_spacy=False)
    # Repeat the keyword 'python' unnaturally many times
    stuffed_text = "Python Python Python Python Python Python Python Python Python Python developer building web applications."
    quality = nlp.analyze_text_quality(stuffed_text)
    warnings = quality.get("keyword_stuffing_warnings", [])
    assert len(warnings) > 0
    assert "python" in warnings[0].lower()
