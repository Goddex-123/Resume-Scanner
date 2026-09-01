# 📄 AI-Powered Resume Scanner & ATS Compatibility Analyzer

![Python 3.9+](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Tests](https://img.shields.io/badge/pytest-22%20passed-brightgreen)
![CI Status](https://github.com/Goddex-123/Resume-Scanner/actions/workflows/ci.yml/badge.svg)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Click%20Here-brightgreen?style=for-the-badge&logo=streamlit)](https://resume-scanner-sohambarate.streamlit.app)

> **A production-grade Applicant Tracking System (ATS) analyzer and resume optimization engine built with modern NLP, structured document decomposition, interval-merging experience analysis, and direct Job Description qualification matching.**

---

## 📋 Executive Summary

The **Resume Scanner** provides candidates and career engineers with transparent, explainable feedback on resume structure, domain skill coverage, and formatting hygiene. Rather than treating ATS systems as an opaque black box, the scanner uses deterministic parsing heuristics, canonical skill normalization, and TF-IDF cosine similarity to identify genuine qualification alignment.

### Key Capabilities

- **Robust Multi-Format Parsing**:
  - High-fidelity PDF extraction via **PyMuPDF (`fitz`)**, preserving paragraph flows, multi-page structures, and detecting scanned/image-only PDFs.
  - Structure-aware Word extraction via **`python-docx`**, reading body paragraphs and structured tables in natural document order.
  - Resilient TXT extraction with multi-encoding fallback (`utf-8`, `utf-8-sig`, `latin-1`, `cp1252`).
  - Graceful rejection of legacy binary `.doc` files with clear conversion instructions.
- **Overlapping Employment Interval Merging**:
  - Employment periods across roles are parsed and merged into continuous timelines, preventing inflated experience counts from concurrent or overlapping roles.
  - Dynamically calculates experience from the system date rather than hard-coded years.
- **Direct Job Description (JD) Alignment**:
  - Differentiates **Required (mandatory)** from **Preferred (bonus)** qualifications.
  - Measures candidate skill coverage, experience alignment, and semantic text similarity against specific target postings.
  - Pre-loaded with realistic sample JDs across Cybersecurity, Web Development, and Data Science.
- **Explainable ATS Scoring & Ethical Guidance**:
  - Transparent weighted categories: Section Completeness, Formatting Hygiene, Role Keywords, Quantifiable Achievements, Readability, and Contact Info.
  - Detects keyword stuffing and penalties for artificial keyword spamming.
  - Recommendations follow ethical phrasing: *"If you genuinely have experience with X, consider highlighting it."*
- **Authentic Writing Style & Buzzword Signals**:
  - Transparent heuristic analysis of overused corporate clichés, buzzword verbs, and sentence uniformity.
  - Explicitly non-punitive, providing concrete rewording suggestions to make writing more grounded and specific.
- **Interactive Multi-Field Demo Suite**:
  - Test-drive the application instantly with realistic candidates in **Cybersecurity**, **Web Development**, and **Data Science**.

---

## 🏗️ Technical Architecture

```mermaid
graph TD
    subgraph Input_Layer [Document & Criteria Input]
        ResumeFile[Resume File (PDF, DOCX, TXT)]
        TargetJD[Target Job Description (Optional)]
        DemoSuite[3-Field Demo Profiles]
    end

    subgraph Parsing_Engine [Robust Extraction Layer]
        ResumeFile --> Parser[ResumeParser Engine]
        DemoSuite --> Parser
        Parser --> DocModel[ResumeDocument Dataclass]
        DocModel --> CleanText[Layout-Preserving Text Normalizer]
        DocModel --> SectionDecomp[Context-Aware Section Parser]
        DocModel --> ContactExtract[International Contact & Link Normalizer]
    end

    subgraph NLP_Analysis [NLP & Semantic Engine]
        CleanText --> SkillNorm[Skill Normalizer & Alias Canonicalizer]
        CleanText --> DateMerge[Date Range & Interval Merging Calculator]
        CleanText --> BulletMetrics[Achievement & Metric Density Classifier]
        CleanText --> AIStyle[Writing Authenticity & Cliché Analyzer]
    end

    subgraph Matching_Engine [ATS & Matching Core]
        TargetJD --> JDAnalyzer[JobDescriptionAnalyzer]
        JDAnalyzer --> ReqPrefSplit[Required vs Preferred Skill Matrix]
        CleanText --> JobMatcher[JobMatcher: TF-IDF Cosine Similarity]
        ReqPrefSplit --> JobMatcher
        CleanText --> ATSScorer[ATSScorer: Explainable Scoring & Quality Heuristics]
    end

    subgraph Presentation_Layer [UI / UX Dashboard]
        JobMatcher --> StreamlitApp[Streamlit v2.0 Dashboard]
        ATSScorer --> StreamlitApp
        SkillNorm --> StreamlitApp
        BulletMetrics --> StreamlitApp
        AIStyle --> StreamlitApp
    end
```

---

## 🔬 Explainable Methodology & Disclaimers

1. **ATS Score Disclaimer**:
   - ATS score outputs represent an analytical estimate based on common commercial ATS parsing heuristics (such as section completeness, standard font/formatting readability, and role-relevant terminology).
   - Commercial employer ATS configurations vary across vendors; this tool provides best-practice optimization guidance rather than guaranteed hiring outcomes.
2. **AI Writing Style Disclaimer**:
   - The writing signals module uses heuristic detection of corporate clichés, buzzwords, and sentence structure uniformity.
   - It is **not** a scientifically validated authorship detector and is designed solely to help candidates write more concrete, authentic bullet points.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9, 3.10, or 3.11
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Goddex-123/Resume-Scanner.git
   cd Resume-Scanner
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Launch the Streamlit dashboard**
   ```bash
   streamlit run app.py
   ```
   Open `http://localhost:8501` in your browser.

---

## 🐳 Docker Deployment

Run the scanner in an isolated, secure container with non-root user execution:

```bash
# Build the production image
docker build -t resume-scanner:v2 .

# Run container on port 8501
docker run -p 8501:8501 --rm resume-scanner:v2
```

Access the application at `http://localhost:8501`.

---

## 🧪 Testing & Quality Assurance

The test suite contains 22 automated tests covering parser integrity, interval merging, skill alias normalization, target JD qualification extraction, and explainable ATS scoring:

```bash
# Run the complete test suite
pytest -v

# Run with test coverage reporting
pytest --cov=resume_scanner tests/
```

---

## 📁 Repository Structure

```
Resume-Scanner/
├── app.py                     # Streamlit application entrypoint with multi-field demo & JD match
├── Dockerfile                 # Hardened Dockerfile with non-root appuser
├── requirements.txt           # Verified pinned dependencies
├── data/
│   └── job_keywords.json      # Curated domain keyword dictionaries
├── samples/
│   ├── sample_resume_cybersecurity.txt  # Alex Rivera (SOC & Pen-Testing)
│   ├── sample_resume_web_developer.txt  # David Kim (Full-Stack TypeScript & React)
│   └── sample_resume_data_science.txt   # Sarah Chen (Machine Learning & MLOps)
├── resume_scanner/
│   ├── __init__.py            # Package exports
│   ├── config.py              # Centralized dataclass configurations
│   ├── parser.py              # Multi-format parser, scanned PDF detection & section extractor
│   ├── nlp_engine.py          # Skill canonicalizer, interval merging & metric analyzer
│   ├── jd_analyzer.py         # Required vs. Preferred qualification analyzer
│   ├── job_matcher.py         # Direct JD matcher & benchmark role matcher
│   ├── ats_scorer.py          # ATS compatibility scorer with keyword stuffing safeguards
│   ├── ai_detector.py         # Heuristic writing authenticity & buzzword signal analyzer
│   └── ui/
│       ├── charts.py          # Plotly neon & dark-mode visualizers
│       └── styles.py          # Responsive custom CSS design tokens
└── tests/
    ├── test_basic.py          # Baseline structure & import tests
    ├── test_demo_resumes.py   # Multi-field demo profiles test suite
    ├── test_parser.py         # Parser, docx, txt, and contact extraction tests
    ├── test_nlp_engine.py     # Skill normalization, interval merging & bullet analysis
    ├── test_jd_matching.py    # Target JD parsing & direct matching tests
    └── test_ats_scorer.py     # ATS scoring, stuffing penalty & ethical phrasing tests
```

---

## 👨‍💻 Author

**Soham Barate (Goddex-123)**  
*AI Engineer & Full-Stack Developer*  

[LinkedIn](https://linkedin.com/in/soham-barate-7429181a9) | [GitHub](https://github.com/Goddex-123)
