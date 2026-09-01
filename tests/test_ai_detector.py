"""
Unit tests for AIDetector (Heuristic Writing Authenticity & Signal Analysis).
"""

from resume_scanner.ai_detector import AIDetector


def test_ai_detector_authentic_writing():
    detector = AIDetector()
    authentic_text = (
        "Engineered a distributed cache layer in Go and Redis reducing p99 latency from 180ms to 24ms. "
        "Configured PostgreSQL connection pooling and optimized database indexing. "
        "Mentored two junior engineers and conducted weekly production incident reviews."
    )
    result = detector.analyze(authentic_text)
    assert result["heuristic_score"] <= 40.0
    assert result["verdict"] in ["Authentic & Specific", "Balanced Phrasing"]
    assert "disclaimer" in result
    assert "NOT a scientifically validated AI detector" in result["disclaimer"]


def test_ai_detector_cliche_detection():
    detector = AIDetector()
    cliche_text = (
        "Results-driven and passionate about leveraging cutting-edge technology. "
        "Spearheaded initiatives to drive strategic growth and fostered collaborative synergy. "
        "Orchestrated seamless integration across cross-functional teams to pioneer innovative solutions."
    )
    result = detector.analyze(cliche_text)
    # Cliches should trigger higher heuristic signal score
    assert result["heuristic_score"] >= 50.0
    assert len(result["signals_detected"]["cliche_phrases"]) >= 3
    assert len(result["suggestions"]) > 0
