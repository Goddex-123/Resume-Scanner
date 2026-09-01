"""
Resume Scanner - AI-Powered Resume Analysis System
Main Streamlit Application — Production-Grade UI Edition v2
"""

import os
from typing import Optional
import streamlit as st

from resume_scanner import ResumeParser, NLPEngine, ATSScorer, AIDetector, JobMatcher
try:
    from resume_scanner import ML_AVAILABLE, SemanticEncoder, HybridMatcher, get_encoder
except ImportError:
    ML_AVAILABLE = False
from resume_scanner.ui.styles import CUSTOM_CSS
from resume_scanner.ui.charts import (
    create_gauge_chart,
    create_skill_radar,
    create_job_match_chart,
    create_score_breakdown_chart,
    create_keyword_density_chart,
    create_text_quality_chart,
    create_ai_breakdown_chart,
    create_direct_jd_match_chart,
)

# Page Configuration
st.set_page_config(
    page_title="Resume Scanner | AI-Powered Analysis",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_resource
def load_ml_components():
    """Load the ML embeddings model and hybrid matcher once."""
    if ML_AVAILABLE:
        try:
            encoder = get_encoder()
            from resume_scanner.ml.inference import create_hybrid_matcher
            matcher = create_hybrid_matcher(encoder=encoder, model_dir="models")
            return encoder, matcher
        except Exception as e:
            return None, None
    return None, None

# Apply Premium CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ─── Path to the built-in demo resumes ───────────────────────────────────────
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")
DEMO_RESUME_PATH = os.path.join(SAMPLES_DIR, "sample_resume.txt")

DEMO_PROFILES = {
    "cybersecurity": {
        "key": "cybersecurity",
        "title": "Cybersecurity Analyst",
        "field_name": "Cyber Security",
        "candidate_name": "Alex Rivera",
        "role_desc": "Lead Cybersecurity Analyst • SOC & Pen-Testing",
        "icon": "🛡️",
        "accent": "#ef4444",
        "badge_border": "rgba(239, 68, 68, 0.4)",
        "file": os.path.join(SAMPLES_DIR, "sample_resume_cybersecurity.txt"),
        "target_role": "Cybersecurity Analyst",
        "skills": ["Splunk", "Wireshark", "Metasploit", "Python", "CISSP", "Zero Trust"],
    },
    "web_dev": {
        "key": "web_dev",
        "title": "Web Developer",
        "field_name": "Web Development",
        "candidate_name": "David Kim",
        "role_desc": "Senior Full-Stack Developer • React & Node.js",
        "icon": "🌐",
        "accent": "#06b6d4",
        "badge_border": "rgba(6, 182, 212, 0.4)",
        "file": os.path.join(SAMPLES_DIR, "sample_resume_web_developer.txt"),
        "target_role": "Web Developer",
        "skills": ["TypeScript", "React", "Next.js", "Node.js", "PostgreSQL", "Tailwind"],
    },
    "data_science": {
        "key": "data_science",
        "title": "Data Scientist",
        "field_name": "Data Science & AI",
        "candidate_name": "Sarah Chen",
        "role_desc": "Senior Data Scientist • ML & Production MLOps",
        "icon": "🔬",
        "accent": "#8b5cf6",
        "badge_border": "rgba(139, 92, 246, 0.4)",
        "file": os.path.join(SAMPLES_DIR, "sample_resume_data_science.txt"),
        "target_role": "Data Scientist",
        "skills": ["Python", "PyTorch", "TensorFlow", "NLP", "MLOps", "AWS"],
    },
}

# ─── Built-in Realistic Sample Job Descriptions ──────────────────────────────
SAMPLE_CYBER_JD = """Job Title: Cybersecurity Analyst (SOC)
Company: Sentinel Cyber Defense
Experience Required: 3+ years of relevant security operations experience.

Requirements:
- Proven experience working in a Security Operations Center (SOC) monitoring and triaging incidents.
- Hands-on experience with SIEM platforms, specifically Splunk, QRadar, or Microsoft Sentinel.
- Solid understanding of network protocols, TCP/IP, and packet analysis using Wireshark or tcpdump.
- Experience with vulnerability scanning and penetration testing tools (Nmap, Metasploit, Burp Suite).
- Understanding of MITRE ATT&CK and OWASP Top 10 frameworks.
- Bachelor's degree in Computer Science, Cybersecurity, or equivalent practical experience.

Preferred Qualifications:
- Industry certifications such as CompTIA Security+, CEH, or CISSP.
- Scripting ability in Python or Bash for log analysis and automation.
- Familiarity with cloud security controls in AWS or Azure.
- Experience writing custom detection rules (YARA, Sigma, or Snort).

Responsibilities:
- Monitor and triage real-time alerts across enterprise endpoints, firewalls, and cloud infrastructure.
- Perform root cause investigations for malware infections, phishing campaigns, and unauthorized access attempts.
- Coordinate incident response workflows with infrastructure and engineering teams.
- Conduct regular vulnerability assessments and collaborate on remediation plans.
"""

SAMPLE_WEB_JD = """Job Title: Full-Stack Web Developer
Company: Nexa Digital Platforms
Experience Required: 3+ years of web engineering experience.

Requirements:
- Strong proficiency in JavaScript, TypeScript, and modern React.
- Solid experience building server-side applications using Node.js and Express.
- Experience designing and querying relational databases (PostgreSQL or MySQL).
- Deep knowledge of modern CSS, responsive layouts, and Tailwind CSS.
- Familiarity with RESTful APIs, HTTP protocols, and state management (Redux or Zustand).
- Bachelor's degree in Computer Science or equivalent hands-on experience.

Preferred Qualifications:
- Experience with Next.js, server-side rendering (SSR), and GraphQL.
- Working knowledge of containerization with Docker and CI/CD pipelines.
- Experience writing automated unit and integration tests using Jest or Cypress.
- Passion for web accessibility (WCAG) and web performance optimization (Core Web Vitals).

Responsibilities:
- Architect and develop customer-facing web applications with responsive, accessible UI components.
- Build scalable backend microservices and RESTful API endpoints.
- Collaborate with product designers and backend engineers in an agile team.
- Profile and optimize frontend bundle sizes, rendering speeds, and database queries.
"""

SAMPLE_DS_JD = """Job Title: Data Scientist (Machine Learning & NLP)
Company: Cognition AI Labs
Experience Required: 4+ years of hands-on data science experience.

Requirements:
- Advanced proficiency in Python, pandas, numpy, and SQL.
- Strong practical experience building machine learning models using Scikit-Learn, PyTorch, or TensorFlow.
- Solid foundation in applied statistics, regression, hypothesis testing, and A/B testing methodology.
- Experience developing Natural Language Processing (NLP) solutions or text classification pipelines.
- Master's degree or Bachelor's degree in Data Science, Computer Science, Statistics, or related field.

Preferred Qualifications:
- Experience with MLOps frameworks, model tracking (MLflow, Weights & Biases), and Docker deployment.
- Familiarity with modern Transformer architectures, HuggingFace, and LLM fine-tuning.
- Experience with cloud platforms (AWS S3/SageMaker or GCP BigQuery/Vertex AI).
- Publications in ML conferences or competitive data science profile (Kaggle).

Responsibilities:
- Formulate business challenges into statistical and predictive machine learning models.
- Clean, preprocess, and engineer features from massive unstructured and structured datasets.
- Train, validate, benchmark, and deploy machine learning models into production services.
- Present data-driven findings and model evaluations to technical leaders and business stakeholders.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Helper: render a custom stat bar (CSS-driven)
# ─────────────────────────────────────────────────────────────────────────────
def _stat_bar(label: str, value: float, max_val: float = 100, color: str = "#8b5cf6"):
    pct = min(value / max_val * 100, 100)
    st.markdown(
        f"""
<div class="stat-bar-container">
<div class="stat-bar-label">
<span>{label}</span>
<span style="color:{color}; font-family:'JetBrains Mono',monospace; font-weight:600;">{value:.0f}</span>
</div>
<div class="stat-bar-track">
<div class="stat-bar-fill" style="width:{pct}%; background:linear-gradient(90deg, {color}, {color}aa);"></div>
</div>
</div>
    """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Main analysis pipeline
# ─────────────────────────────────────────────────────────────────────────────
def run_analysis(
    text: str,
    target_role: str,
    run_ats: bool,
    run_skills: bool,
    run_ai: bool,
    run_jobs: bool,
    job_description_text: Optional[str] = None,
    job_title_input: str = "",
):
    """Run the full analysis pipeline and render results."""

    progress = st.progress(0, text="🔍 Initializing analysis...")

    # ── Parse extra info ──────────────────────────────────────────────────
    parser = ResumeParser()
    parser.text = text
    contact_info = parser.extract_contact_info()
    sections_found = parser.get_sections()

    # ── NLP Engine ────────────────────────────────────────────────────────
    try:
        progress.progress(20, text="🧠 Extracting skills & analyzing experience...")
        nlp_engine = NLPEngine(use_spacy=False)
        skills = nlp_engine.extract_skills(text) if run_skills else {}
        text_quality = nlp_engine.analyze_text_quality(text)
        exp_years, exp_entries = nlp_engine.calculate_experience_years(text)
        bullet_analysis = nlp_engine.analyze_bullet_points(text)
    except Exception as e:
        st.warning(f"⚠️ Skill extraction encountered an issue: {e}")
        skills, text_quality = {}, _empty_tq()
        exp_years, exp_entries = 0, []
        bullet_analysis = {}

    # ── ATS Scoring ───────────────────────────────────────────────────────
    try:
        progress.progress(45, text="📋 Calculating ATS score...")
        ats_scorer = ATSScorer()
        role = (
            None
            if target_role == "Auto-Detect"
            else target_role.lower().replace(" ", "_")
        )
        ats_results = ats_scorer.calculate_score(text, role) if run_ats else {}
    except Exception as e:
        st.warning(f"⚠️ ATS scoring encountered an issue: {e}")
        ats_results = {}

    # ── AI Writing Signals ────────────────────────────────────────────────
    try:
        progress.progress(65, text="✍️ Analyzing writing authenticity & style signals...")
        ai_detector = AIDetector()
        ai_results = ai_detector.analyze(text) if run_ai else {}
    except Exception as e:
        st.warning(f"⚠️ Writing style analysis encountered an issue: {e}")
        ai_results = {}

    # ── Job Matching (Direct JD or Benchmark Roles) ────────────────────────
    try:
        progress.progress(85, text="💼 Evaluating job alignment...")
        job_matcher = JobMatcher()
        if run_jobs:
            if job_description_text and job_description_text.strip():
                job_results = job_matcher.match_resume_to_jd(
                    text, job_description_text, job_title_input
                )
                job_results["direct_match"] = True

                # Hybrid ML Matching
                encoder, hybrid_matcher = load_ml_components()
                if hybrid_matcher:
                    progress.progress(90, text="🔬 Computing semantic embeddings & ML predictions...")
                    ml_results = hybrid_matcher.match(
                        resume_text=text,
                        jd_text=job_description_text,
                        rule_based_results=job_results,
                        resume_sections=sections_found,
                    )
                    if ml_results:
                        job_results["ml_results"] = ml_results
            else:
                job_results = job_matcher.match(text)
                job_results["direct_match"] = False
        else:
            job_results = {}
    except Exception as e:
        st.warning(f"⚠️ Job matching encountered an issue: {e}")
        job_results = {}

    progress.progress(100, text="✨ Analysis complete!")

    st.markdown("<br>", unsafe_allow_html=True)
    st.success("✅ Analysis complete! Scroll down for your detailed results.")

    # ══════════════════════════════════════════════════════════════════════
    # TOP METRIC CARDS
    # ══════════════════════════════════════════════════════════════════════
    ats_score = ats_results.get("scores", {}).get("total", 0)
    total_skills = sum(len(v) for v in skills.values())
    ai_prob = ai_results.get("heuristic_score", ai_results.get("ai_probability", 0))

    if job_results.get("direct_match"):
        match_val = f"{job_results.get('overall_match', 0):.0f}%"
        match_label = "Target JD Match"
        match_icon = "🎯"
    else:
        best_match = job_results.get("best_match", {})
        match_pct = best_match.get("match", 0) if best_match else 0
        match_val = f"{match_pct:.0f}%"
        match_label = "Best Role Fit"
        match_icon = "💼"

    c1, c2, c3, c4, c5 = st.columns(5)
    
    metrics = [
        (c1, "📋", f"{ats_score:.0f}", "ATS Score"),
        (c2, "🧠", f"{total_skills}", "Skills Found"),
        (c3, "✍️", f"{ai_prob:.0f}%", "AI Phrasing Score"),
        (c4, match_icon, match_val, match_label),
    ]
    
    ml_results = job_results.get("ml_results", {}) if job_results.get("direct_match") else {}
    if ml_results and ml_results.get("has_trained_model"):
        prob = ml_results.get("ml_prediction", {}).get("match_probability", 0.0)
        metrics.append((c5, "🤖", f"{prob*100:.0f}%", "ML Match Prob"))
    elif ml_results and ml_results.get("has_semantic"):
        sem = ml_results.get("semantic_similarity", {}).get("full_document", 0.0)
        metrics.append((c5, "🌐", f"{sem*100:.0f}%", "Semantic Sim"))
    else:
        metrics.append((c5, "🤖", "N/A", "ML Disabled"))

    for col, icon, val, label in metrics:
        with col:
            st.markdown(
                f"""
<div class="metric-card">
<span class="metric-icon">{icon}</span>
<div class="metric-value">{val}</div>
<div class="metric-label">{label}</div>
</div>
            """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════
    # QUICK INSIGHTS ROW (Contact + Sections + Experience)
    # ══════════════════════════════════════════════════════════════════════
    qi1, qi2, qi3 = st.columns(3)

    with qi1:
        st.markdown(
            """
<div class="analysis-card">
<div class="analysis-card-title">📇 Contact Information</div>
<div class="contact-grid">
        """,
            unsafe_allow_html=True,
        )

        items = [
            ("📧", "Email", contact_info.get("email", "—")),
            ("📱", "Phone", contact_info.get("phone", "—")),
            ("🔗", "LinkedIn", contact_info.get("linkedin", "—")),
            ("💻", "GitHub", contact_info.get("github", "—")),
        ]
        html_items = ""
        for icon, label, val in items:
            is_present = val != "—" and val is not None
            val_display = str(val)[:28] + ("…" if len(str(val)) > 28 else "")
            color = "#f1f5f9" if is_present else "#64748b"
            html_items += f"""
<div class="contact-item">
<span class="contact-icon">{icon}</span>
<div class="contact-details">
<div class="contact-label">{label}</div>
<div class="contact-value" style="color:{color};">{val_display}</div>
</div>
</div>
            """
        st.markdown(html_items + "</div></div>", unsafe_allow_html=True)

    with qi2:
        st.markdown(
            """
<div class="analysis-card">
<div class="analysis-card-title">📑 Detected Sections</div>
<div class="section-list">
        """,
            unsafe_allow_html=True,
        )

        core_sections = [
            "experience",
            "education",
            "skills",
            "summary",
            "projects",
            "certifications",
        ]
        sec_html = ""
        for sec in core_sections:
            found = sections_found.get(sec, False)
            icon = "✅" if found else "❌"
            css = "section-found" if found else "section-missing"
            sec_html += f"""
<div class="section-tag {css}">
<span class="section-tag-icon">{icon}</span>
<span>{sec.title()}</span>
</div>
            """
        st.markdown(sec_html + "</div></div>", unsafe_allow_html=True)

    with qi3:
        st.markdown(
            f"""
<div class="analysis-card">
<div class="analysis-card-title">⏳ Professional Experience</div>
<div style="font-size:2.2rem; font-weight:700; color:#8b5cf6; font-family:'JetBrains Mono',monospace;">
    {exp_years:.1f} <span style="font-size:1rem; color:#94a3b8; font-weight:400;">years (merged)</span>
</div>
<div style="color:#94a3b8; font-size:0.8rem; margin:4px 0 10px;">Overlapping employment intervals deduplicated</div>
<div class="exp-timeline">
        """,
            unsafe_allow_html=True,
        )

        if exp_entries:
            for entry in exp_entries[:4]:
                label_text = entry.get("label", f"{entry.get('start')} – {entry.get('end')}")
                years_text = f"{entry.get('years', 0)} yr"
                st.markdown(
                    f"""
<div class="exp-item">
<span class="exp-years">{years_text}</span>
<span class="exp-range"> — {label_text}</span>
</div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div style="color:#64748b; font-size:0.85rem; padding:6px 0;">No date ranges detected</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════
    # DETAILED TABS
    # ══════════════════════════════════════════════════════════════════════
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📊 ATS Analysis",
            "🧠 Skills Map",
            "✍️ Writing Signals",
            "🎯 Job Match",
            "📈 Deep Insights",
        ]
    )

    # ── Tab 1: ATS Tab ────────────────────────────────────────────────────
    with tab1:
        if run_ats and ats_results:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.plotly_chart(
                    create_gauge_chart(ats_score, "ATS Compatibility"),
                    use_container_width=True,
                    config={"displayModeBar": False},
                )
                sub_scores = ats_results.get("scores", {})
                if sub_scores:
                    st.plotly_chart(
                        create_score_breakdown_chart(sub_scores),
                        use_container_width=True,
                        config={"displayModeBar": False},
                    )

            with col_b:
                st.markdown(
                    '<h3 class="section-header">📋 Parser Feedback</h3>',
                    unsafe_allow_html=True,
                )
                for fb in ats_results.get("feedback", []):
                    if fb.startswith("✅"):
                        css = "feedback-positive"
                    elif fb.startswith("⚠️") or fb.startswith("💡"):
                        css = "feedback-warning"
                    else:
                        css = "feedback-negative"
                    st.markdown(
                        f'<div class="feedback-item {css}">{fb}</div>',
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"""
<div class="grade-box">
<strong>Estimated Grade:</strong> {ats_results.get('grade', 'N/A')} &nbsp;&nbsp;|&nbsp;&nbsp;
<strong>ATS Baseline:</strong> {'✅ Meets Pass Baseline' if ats_results.get('pass_ats') else '⚠️ Needs Attention'}
</div>
                """,
                    unsafe_allow_html=True,
                )

                # Prioritized Improvement Suggestions
                suggestions = ats_scorer.get_improvement_suggestions()
                if suggestions:
                    st.markdown(
                        '<h3 class="section-header" style="margin-top:16px;">🎯 Prioritized Action Plan</h3>',
                        unsafe_allow_html=True,
                    )
                    for sug in suggestions:
                        if sug.startswith("High"):
                            pill = '<span class="priority-pill-high">High Priority</span>'
                            text_body = sug.replace("High Priority: ", "")
                        elif sug.startswith("Medium"):
                            pill = '<span class="priority-pill-med">Medium Priority</span>'
                            text_body = sug.replace("Medium Priority: ", "")
                        else:
                            pill = '<span class="priority-pill-low">Low Priority</span>'
                            text_body = sug.replace("Low Priority: ", "")

                        st.markdown(
                            f"""
<div class="suggestion-item">
<div>{pill}</div>
<div class="suggestion-text">{text_body}</div>
</div>
                            """,
                            unsafe_allow_html=True,
                        )

                # Honest Disclaimer
                st.markdown(
                    f'<div class="disclaimer-box">ℹ️ {ats_results.get("disclaimer", "")}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("ATS Analysis is disabled. Enable it in the sidebar.")

    # ── Tab 2: Skills Tab ─────────────────────────────────────────────────
    with tab2:
        if run_skills and skills:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.plotly_chart(
                    create_skill_radar(skills),
                    use_container_width=True,
                    config={"displayModeBar": False},
                )
            with col_b:
                st.markdown(
                    '<h3 class="section-header">🎯 Detected Skills</h3>',
                    unsafe_allow_html=True,
                )
                for category, skill_list in skills.items():
                    if skill_list:
                        cat_name = category.replace("_", " ").title()
                        st.markdown(
                            f'<div class="category-title">{cat_name} ({len(skill_list)})</div>',
                            unsafe_allow_html=True,
                        )
                        badges = "".join(
                            [
                                f'<span class="skill-badge">{s}</span>'
                                for s in skill_list[:15]
                            ]
                        )
                        st.markdown(badges, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)

            st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)
            st.markdown(
                '<h3 class="section-header">📊 Skill Distribution</h3>',
                unsafe_allow_html=True,
            )
            sc1, sc2, sc3 = st.columns(3)
            non_empty = {k: v for k, v in skills.items() if v}
            sorted_cats = sorted(
                non_empty.items(), key=lambda x: len(x[1]), reverse=True
            )

            for i, (cat, slist) in enumerate(sorted_cats):
                target_col = [sc1, sc2, sc3][i % 3]
                with target_col:
                    color = (
                        "#8b5cf6"
                        if i % 3 == 0
                        else "#06b6d4" if i % 3 == 1 else "#f472b6"
                    )
                    _stat_bar(
                        cat.replace("_", " ").title(),
                        len(slist),
                        max(len(s) for s in skills.values()) + 2,
                        color,
                    )
        else:
            st.info("Skill extraction is disabled. Enable it in the sidebar.")

    # ── Tab 3: Writing Style & Authenticity Signals (formerly AI Detection) ──
    with tab3:
        if run_ai and ai_results:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.plotly_chart(
                    create_gauge_chart(ai_prob, "AI Writing Signals (Heuristic)"),
                    use_container_width=True,
                    config={"displayModeBar": False},
                )
                detailed = ai_results.get("detailed_scores", {})
                if detailed:
                    st.plotly_chart(
                        create_ai_breakdown_chart(detailed),
                        use_container_width=True,
                        config={"displayModeBar": False},
                    )

            with col_b:
                verdict = ai_results.get("verdict", "Unknown")
                confidence = ai_results.get("confidence", "Moderate")

                if "Authentic" in verdict:
                    verdict_color = "#10b981"
                elif "Balanced" in verdict:
                    verdict_color = "#06b6d4"
                elif "Moderate" in verdict:
                    verdict_color = "#f59e0b"
                else:
                    verdict_color = "#ef4444"

                st.markdown(
                    f"""
<div class="verdict-card">
<h3 class="section-header" style="text-align:center;">✍️ Phrasing Style Assessment</h3>
<div style="font-size:1.6rem; color:{verdict_color}; font-weight:700; margin:12px 0;">
    {verdict}
</div>
<div style="color:#94a3b8;">Signal Strength: <strong>{confidence}</strong></div>
</div>
                """,
                    unsafe_allow_html=True,
                )

                # Signals & Clichés detected
                detected_signals = ai_results.get("signals_detected", {})
                cliches = detected_signals.get("cliche_phrases", [])
                buzzverbs = detected_signals.get("buzzword_verbs", [])

                if cliches or buzzverbs:
                    st.markdown(
                        '<h4 style="color:#f59e0b; margin-top:18px;">⚠️ Overused Corporate Buzzwords Detected</h4>',
                        unsafe_allow_html=True,
                    )
                    cliche_badges = "".join(
                        [
                            f'<span class="skill-badge" style="border-color:rgba(245,158,11,0.5); '
                            f'color:#fcd34d;">{c}</span>'
                            for c in cliches
                        ]
                    )
                    verb_badges = "".join(
                        [
                            f'<span class="skill-badge" style="border-color:rgba(239,68,68,0.5); '
                            f'color:#fca5a5;">{v}</span>'
                            for v in buzzverbs
                        ]
                    )
                    st.markdown(cliche_badges + verb_badges, unsafe_allow_html=True)

                # Constructive authentic suggestions
                suggestions = ai_results.get("suggestions", [])
                if suggestions:
                    st.markdown(
                        '<h4 style="color:#60a5fa; margin-top:18px;">💡 Recommendations for Authentic Phrasing</h4>',
                        unsafe_allow_html=True,
                    )
                    for sug in suggestions:
                        st.markdown(
                            f'<div class="feedback-item feedback-warning">💡 {sug}</div>',
                            unsafe_allow_html=True,
                        )

                # Explicit honest disclaimer
                st.markdown(
                    f'<div class="disclaimer-box">ℹ️ {ai_results.get("disclaimer", "")}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("Writing style analysis is disabled. Enable it in the sidebar.")

    # ── Tab 4: Job Fit & Direct JD Match ──────────────────────────────────
    with tab4:
        if run_jobs and job_results:
            if job_results.get("direct_match"):
                # Direct Resume ↔ Target Job Description Match Mode
                st.markdown(
                    f"""
<div class="jd-card">
    <div style="font-size:0.9rem; color:#94a3b8; text-transform:uppercase; letter-spacing:0.8px;">
        Target Job Match Analysis
    </div>
    <div class="jd-role-header">🎯 {job_results.get('job_title', 'Target Role')}</div>
    <div style="font-size:1.8rem; font-weight:700; color:#8b5cf6; font-family:'JetBrains Mono',monospace;">
        {job_results.get('overall_match', 0):.1f}%
        <span style="font-size:1rem; color:#94a3b8; font-weight:400;">Composite Alignment</span>
    </div>
</div>
                    """,
                    unsafe_allow_html=True,
                )

                jd_col1, jd_col2 = st.columns([1, 1])

                with jd_col1:
                    st.markdown('<h3 class="section-header">📊 Alignment Breakdown</h3>', unsafe_allow_html=True)
                    breakdown = job_results.get("breakdown", {})
                    st.plotly_chart(
                        create_direct_jd_match_chart(breakdown),
                        use_container_width=True,
                        config={"displayModeBar": False},
                    )

                    # Experience & Education Comparison
                    req_exp = job_results.get("required_experience_years")
                    cand_exp = job_results.get("candidate_experience_years", 0)
                    exp_disp = f"~{req_exp:.0f} years" if req_exp else "Not specified"

                    st.markdown(
                        f"""
<div class="analysis-card" style="margin-top:12px;">
    <div class="analysis-card-title">⏳ Experience & Education Comparison</div>
    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
        <span style="color:#94a3b8;">Job Requirement:</span>
        <strong style="color:#e2e8f0;">{exp_disp}</strong>
    </div>
    <div style="display:flex; justify-content:space-between;">
        <span style="color:#94a3b8;">Candidate Experience:</span>
        <strong style="color:#8b5cf6;">{cand_exp:.1f} years (merged)</strong>
    </div>
</div>
                        """,
                        unsafe_allow_html=True,
                    )

                with jd_col2:
                    st.markdown('<h3 class="section-header">🔑 Qualifications Coverage</h3>', unsafe_allow_html=True)

                    # Required Skills Matched
                    req_matched = job_results.get("matched_required_skills", [])
                    if req_matched:
                        st.markdown(
                            f'<div style="font-size:0.88rem; font-weight:600; color:#10b981; margin-bottom:4px;">'
                            f'✅ Matched Required Skills ({len(req_matched)})</div>',
                            unsafe_allow_html=True,
                        )
                        badges_matched = "".join(
                            [f'<span class="skill-badge-req-match">{s}</span>' for s in req_matched]
                        )
                        st.markdown(badges_matched, unsafe_allow_html=True)

                    # Missing Required Skills
                    req_missing = job_results.get("missing_required_skills", [])
                    if req_missing:
                        st.markdown(
                            f'<div style="font-size:0.88rem; font-weight:600; color:#f59e0b; margin:12px 0 4px;">'
                            f'⚠️ Gaps in Required Skills ({len(req_missing)})</div>',
                            unsafe_allow_html=True,
                        )
                        badges_missing = "".join(
                            [f'<span class="skill-badge-req-miss">{s}</span>' for s in req_missing]
                        )
                        st.markdown(badges_missing, unsafe_allow_html=True)

                    # Preferred Skills Matched
                    pref_matched = job_results.get("matched_preferred_skills", [])
                    if pref_matched:
                        st.markdown(
                            f'<div style="font-size:0.88rem; font-weight:600; color:#06b6d4; margin:12px 0 4px;">'
                            f'🌟 Matched Preferred / Bonus Skills ({len(pref_matched)})</div>',
                            unsafe_allow_html=True,
                        )
                        badges_pref = "".join(
                            [f'<span class="skill-badge-pref-match">{s}</span>' for s in pref_matched]
                        )
                        st.markdown(badges_pref, unsafe_allow_html=True)

                # Tailored Recommendations for this JD
                jd_recs = job_results.get("recommendations", [])
                if jd_recs:
                    st.markdown(
                        '<h3 class="section-header" style="margin-top:18px;">'
                        '💡 Targeted Guidance for this Role</h3>',
                        unsafe_allow_html=True,
                    )
                    for rec in jd_recs:
                        st.markdown(
                            f'<div class="feedback-item feedback-warning">{rec}</div>',
                            unsafe_allow_html=True,
                        )

                st.markdown(
                    f'<div class="disclaimer-box">ℹ️ {job_results.get("disclaimer", "")}</div>',
                    unsafe_allow_html=True,
                )

                ml_res = job_results.get("ml_results", {})
                if ml_res and ml_res.get("has_semantic"):
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown('<h3 class="section-header">🔬 ML & Semantic Analysis</h3>', unsafe_allow_html=True)
                    
                    if ml_res.get("has_trained_model"):
                        pred = ml_res["ml_prediction"]
                        prob = pred["match_probability"]
                        st.markdown(
                            f'<div style="font-size:1.1rem; font-weight:700; color:#8b5cf6; margin-bottom:12px;">' 
                            f'ML Match Probability: {prob*100:.1f}%</div>',
                            unsafe_allow_html=True,
                        )
                    
                    fc = ml_res.get("feature_contributions", {})
                    if fc.get("positive") or fc.get("negative"):
                        st.markdown('<div style="font-size:0.95rem; font-weight:600; margin-bottom:8px;">Explainability Breakdown</div>', unsafe_allow_html=True)
                        for p in fc.get("positive", []):
                            st.markdown(f'<div class="feedback-item feedback-good">✅ <strong>{p["signal"]}</strong>: {p["value"]}</div>', unsafe_allow_html=True)
                        for n in fc.get("negative", []):
                            st.markdown(f'<div class="feedback-item feedback-danger">⚠️ <strong>{n["signal"]}</strong>: {n["value"]}</div>', unsafe_allow_html=True)
                    
                    with st.expander("🔧 Technical Details (ML)"):
                        st.json(ml_res.get("model_info", {}))
                        if ml_res.get("has_trained_model"):
                            st.json(ml_res["ml_prediction"].get("top_features", []))

            else:
                # Benchmark Roles Mode
                matches = job_results.get("all_matches", [])
                if matches:
                    st.plotly_chart(
                        create_job_match_chart(matches),
                        use_container_width=True,
                        config={"displayModeBar": False},
                    )

                    best = job_results.get("best_match")
                    if best:
                        match_color = "#10b981" if best["match"] >= 70 else "#f59e0b"
                        st.markdown(
                            f"""
<div class="best-match-card">
<div style="font-size:0.95rem; color:#94a3b8;">Top Benchmark Match</div>
<div style="font-size:2rem; font-weight:700; color:{match_color};">
    {best['role']}
</div>
<div style="font-size:1.4rem; color:#8b5cf6; font-family:'JetBrains Mono',monospace;">
    {best['match']:.1f}% Similarity
</div>
</div>
                        """,
                            unsafe_allow_html=True,
                        )

                    recs = job_results.get("recommendations", [])
                    if recs:
                        st.markdown(
                            '<h3 class="section-header">💡 Benchmark Role Recommendations</h3>',
                            unsafe_allow_html=True,
                        )
                        for i, rec in enumerate(recs, 1):
                            st.markdown(
                                f"""
<div class="suggestion-item">
<div class="suggestion-number">{i}</div>
<div class="suggestion-text">{rec}</div>
</div>
                            """,
                                unsafe_allow_html=True,
                            )
        else:
            st.info("Job Matching is disabled. Enable it in the sidebar.")

    # ── Tab 5: Deep Insights & Bullet Analysis ────────────────────────────
    with tab5:
        di1, di2 = st.columns([1, 1])

        with di1:
            st.markdown(
                '<h3 class="section-header">📝 Writing Quality</h3>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(
                create_text_quality_chart(text_quality),
                use_container_width=True,
                config={"displayModeBar": False},
            )

            st.markdown(
                """
<div class="analysis-card">
<div class="analysis-card-title">📊 Document Statistics</div>
            """,
                unsafe_allow_html=True,
            )
            _stat_bar("Word Count", text_quality["word_count"], 1000, "#8b5cf6")
            _stat_bar("Sentences", text_quality["sentence_count"], 60, "#06b6d4")
            _stat_bar(
                "Avg Sentence Length",
                text_quality["avg_sentence_length"],
                30,
                "#f472b6",
            )
            _stat_bar("Action Verbs", text_quality["action_verb_count"], 20, "#10b981")

            found_verbs = text_quality.get("found_action_verbs", [])
            if found_verbs:
                st.markdown(
                    '<div style="margin-top: 12px; font-size: 0.85rem; color: #94a3b8;">Action Verbs Found:</div>',
                    unsafe_allow_html=True,
                )
                badges = "".join(
                    [
                        f'<span class="skill-badge" style="border-color:rgba(16,185,129,0.3); '
                        f'font-size:0.75rem; padding:2px 6px; margin:2px;">{v.title()}</span>'
                        for v in found_verbs
                    ]
                )
                st.markdown(
                    f'<div style="margin-top: 4px; display: flex; flex-wrap: wrap;">{badges}</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)

            # Repetition / Keyword Stuffing Warnings
            stuffing_warnings = text_quality.get("keyword_stuffing_warnings", [])
            if stuffing_warnings:
                st.markdown(
                    """
<div class="analysis-card" style="margin-top:16px; border-color:rgba(239,68,68,0.4);">
<div class="analysis-card-title" style="color:#f87171;">⚠️ Repetition & Stuffing Warnings</div>
                    """,
                    unsafe_allow_html=True,
                )
                for w in stuffing_warnings:
                    st.markdown(f'<div class="feedback-item feedback-negative">{w}</div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        with di2:
            # Bullet Point Strength & Achievement Analysis
            st.markdown(
                '<h3 class="section-header">🎯 Bullet Point & Metrics Impact</h3>',
                unsafe_allow_html=True,
            )

            total_bullets = bullet_analysis.get("total_bullets", 0)
            metrics_count = bullet_analysis.get("bullets_with_metrics", 0)
            metric_pct = bullet_analysis.get("metric_percentage", 0.0)
            strong_bullets = bullet_analysis.get("strong_bullets", [])
            moderate_bullets = bullet_analysis.get("moderate_bullets", [])
            weak_bullets = bullet_analysis.get("weak_bullets", [])

            st.markdown(
                f"""
<div class="analysis-card">
    <div class="analysis-card-title">📈 Quantifiable Achievement Density</div>
    <div style="font-size:2.2rem; font-weight:700; color:#10b981; font-family:'JetBrains Mono',monospace;">
        {metric_pct:.0f}% <span style="font-size:0.95rem; color:#94a3b8; font-weight:400;">
        ({metrics_count}/{total_bullets} bullets have metrics)</span>
    </div>
    <div style="margin: 12px 0 6px;">
        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
            <span style="color:#10b981;">● Strong (Action + Measurable Outcome):</span>
            <strong>{len(strong_bullets)}</strong>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
            <span style="color:#06b6d4;">● Moderate (Action Verb only):</span>
            <strong>{len(moderate_bullets)}</strong>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.85rem;">
            <span style="color:#f59e0b;">● Weak / Passive construction:</span>
            <strong>{len(weak_bullets)}</strong>
        </div>
    </div>
</div>
                """,
                unsafe_allow_html=True,
            )

            bullet_recs = bullet_analysis.get("recommendations", [])
            if bullet_recs:
                st.markdown('<div style="margin-top:12px;"></div>', unsafe_allow_html=True)
                for br in bullet_recs:
                    st.markdown(f'<div class="feedback-item feedback-warning">💡 {br}</div>', unsafe_allow_html=True)

            # Keyword Coverage
            if run_ats and ats_results:
                st.markdown(
                    '<h3 class="section-header" style="margin-top:20px;">🔑 Role Keyword Coverage</h3>',
                    unsafe_allow_html=True,
                )
                scored_role = role or ats_scorer._detect_role(text.lower())
                scored_role = scored_role.lower().replace(" ", "_").replace("-", "_")
                if scored_role not in ats_scorer.ROLE_KEYWORDS:
                    scored_role = "data_scientist"
                all_kw = ats_scorer.ROLE_KEYWORDS[scored_role]
                found_kw = [k for k in all_kw if k.lower() in text.lower()]
                missing_kw = [k for k in all_kw if k.lower() not in text.lower()]

                st.plotly_chart(
                    create_keyword_density_chart(found_kw, missing_kw),
                    use_container_width=True,
                    config={"displayModeBar": False},
                )


def _empty_tq():
    """Returns empty text quality dict."""
    return {
        "word_count": 0,
        "sentence_count": 0,
        "avg_word_length": 0,
        "avg_sentence_length": 0,
        "vocabulary_richness": 0,
        "action_verb_count": 0,
        "action_verb_percentage": 0,
        "found_action_verbs": [],
        "keyword_stuffing_warnings": [],
    }


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    # ── Hero Section ──────────────────────────────────────────────────────
    st.markdown(
        """
<div class="hero-container">
<div class="hero-icon">🔬</div>
<h1 class="hero-title">Resume Scanner</h1>
<p class="hero-subtitle">Production NLP Analysis • ATS Compatibility • Target JD Matching</p>
<div class="hero-badge">✦ v2.0 — Production-Grade Engineering Edition</div>
</div>
    """,
        unsafe_allow_html=True,
    )

    # ── Sidebar ───────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-title">⚡ Quick Settings</div>', unsafe_allow_html=True
        )
        target_role = st.selectbox(
            "🎯 Target Role Benchmark",
            [
                "Auto-Detect",
                "Cybersecurity Analyst",
                "Web Developer",
                "Data Scientist",
                "ML Engineer",
                "Data Analyst",
                "Software Engineer",
                "Data Engineer",
            ],
            help="Used for role-specific keyword benchmarking when no custom Job Description is provided",
        )

        st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sidebar-title">📊 Analysis Modules</div>',
            unsafe_allow_html=True,
        )
        run_ats = st.checkbox("📋 ATS Scoring", value=True)
        run_skills = st.checkbox("🧠 Skill Extraction", value=True)
        run_ai = st.checkbox("✍️ Writing Style Signals", value=True)
        run_jobs = st.checkbox("💼 Job Matching", value=True)

        st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sidebar-title">🔮 Technology Stack</div>', unsafe_allow_html=True
        )
        st.markdown(
            """
<div>
<span class="sidebar-tech-badge">PyMuPDF</span>
<span class="sidebar-tech-badge">python-docx</span>
<span class="sidebar-tech-badge">NLP / TF-IDF</span>
<span class="sidebar-tech-badge">Interval Merging</span>
"""
+ (f'<span class="sidebar-tech-badge" style="background:rgba(139,92,246,0.15); color:#c4b5fd; border-color:rgba(139,92,246,0.3);">Sentence-BERT</span>' if ML_AVAILABLE else '')
+ """
</div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            """
<div style="text-align:center; padding:8px 0;">
<span class="pulse"></span>
<span style="color:#94a3b8; font-size:0.78rem;">Analyzer Online</span>
</div>
        """,
            unsafe_allow_html=True,
        )

    # ── Optional Custom Job Description Input ─────────────────────────────
    with st.expander("🎯 Target Job Description Matching (Optional — Click to Expand)", expanded=False):
        st.markdown(
            """
<div style="font-size:0.85rem; color:#94a3b8; margin-bottom:10px;">
    Provide a specific job posting to extract <strong>Required vs. Preferred qualifications</strong>,
    measure semantic similarity, and detect skill gaps tailored to that role.
</div>
            """,
            unsafe_allow_html=True,
        )

        col_jd_t, col_samples = st.columns([1, 1])
        with col_jd_t:
            jd_title_in = st.text_input(
                "Target Job Title",
                value=st.session_state.get("jd_title_val", ""),
                placeholder="e.g. SOC Analyst or Senior Web Developer",
            )
        with col_samples:
            st.markdown(
                "<div style='font-size:0.8rem; color:#94a3b8; margin-bottom:4px;'>"
                "Load a pre-configured sample JD:</div>",
                unsafe_allow_html=True,
            )
            sc1, sc2, sc3 = st.columns(3)
            if sc1.button("🛡️ Cyber JD", key="sample_jd_cyber"):
                st.session_state["jd_title_val"] = "Cybersecurity Analyst (SOC)"
                st.session_state["jd_text_val"] = SAMPLE_CYBER_JD
                st.rerun()
            if sc2.button("🌐 Web Dev JD", key="sample_jd_web"):
                st.session_state["jd_title_val"] = "Full-Stack Web Developer"
                st.session_state["jd_text_val"] = SAMPLE_WEB_JD
                st.rerun()
            if sc3.button("🔬 Data Sci JD", key="sample_jd_ds"):
                st.session_state["jd_title_val"] = "Data Scientist (ML & NLP)"
                st.session_state["jd_text_val"] = SAMPLE_DS_JD
                st.rerun()

        jd_text_in = st.text_area(
            "Job Description Text",
            value=st.session_state.get("jd_text_val", ""),
            height=130,
            placeholder="Paste full job posting here (including Requirements, Qualifications, and Responsibilities)...",
        )

    # ── Upload Section ────────────────────────────────────────────────────
    st.markdown(
        """
<div style="text-align:center; margin: 16px 0 12px;">
    <div style="font-size:1.25rem; font-weight:700; color:#f1f5f9; letter-spacing:-0.3px;">
        📄 Upload Your Resume
    </div>
    <div style="font-size:0.85rem; color:#94a3b8; margin-top:4px;">
        Supports PDF, DOCX, and TXT formats • Multi-page & layout preserved
    </div>
</div>
    """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"],
        help="Supports PDF, DOCX, and TXT formats",
        label_visibility="collapsed",
    )

    # ── Demo Selection State ──────────────────────────────────────────────
    if "show_demo_selector" not in st.session_state:
        st.session_state["show_demo_selector"] = False
    if "active_demo_key" not in st.session_state:
        st.session_state["active_demo_key"] = None

    # ── Demo Button ───────────────────────────────────────────────────────
    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

    _, demo_col, _ = st.columns([1, 2, 1])
    with demo_col:
        demo_clicked = st.button(
            "🚀  Try Demo Resume — See It In Action",
            use_container_width=True,
            type="secondary",
        )

    if demo_clicked:
        st.session_state["show_demo_selector"] = True
        if not st.session_state.get("active_demo_key"):
            st.session_state["active_demo_key"] = "cybersecurity"

    # ── Render 3 Demo Candidate Profiles ──────────────────────────────────
    if st.session_state.get("show_demo_selector") and not uploaded_file:
        st.markdown(
            """
<div class="demo-selector-wrapper">
    <div class="demo-selector-header">
        <div class="demo-selector-title">🎯 Select a Demo Profile to Test-Drive Resume Scanner</div>
        <div class="demo-selector-subtitle">Choose from 3 specialized industry resumes across distinct fields:</div>
    </div>
</div>
            """,
            unsafe_allow_html=True,
        )

        c_cyber, c_web, c_ds = st.columns(3)
        cols_map = {
            "cybersecurity": c_cyber,
            "web_dev": c_web,
            "data_science": c_ds,
        }

        for pkey, pinfo in DEMO_PROFILES.items():
            col = cols_map[pkey]
            with col:
                is_active = st.session_state.get("active_demo_key") == pkey
                active_status = (
                    '<span style="color:#10b981; font-weight:700; font-size:0.75rem; margin-left:6px;">● ACTIVE</span>'
                    if is_active
                    else ""
                )
                skills_tags = "".join(
                    [
                        f'<span class="demo-tag">{skill}</span>'
                        for skill in pinfo["skills"][:4]
                    ]
                )
                card_border = (
                    f"border: 2px solid {pinfo['accent']}; box-shadow: 0 0 20px {pinfo['badge_border']};"
                    if is_active
                    else f"border-top: 3px solid {pinfo['accent']};"
                )

                st.markdown(
                    f"""
<div class="demo-card {pkey}" style="{card_border}">
    <div class="demo-card-top">
        <span class="demo-card-icon">{pinfo['icon']}</span>
        <div>
            <div class="demo-card-field" style="color:{pinfo['accent']};">{pinfo['field_name']}{active_status}</div>
            <div class="demo-card-name">{pinfo['candidate_name']}</div>
        </div>
    </div>
    <div class="demo-card-role">{pinfo['role_desc']}</div>
    <div class="demo-tags-wrap">{skills_tags}</div>
</div>
                    """,
                    unsafe_allow_html=True,
                )

                btn_label = (
                    f"✓ Scanning {pinfo['candidate_name'].split()[0]}"
                    if is_active
                    else f"👉 Scan {pinfo['candidate_name'].split()[0]} ({pinfo['title']})"
                )
                btn_type = "primary" if is_active else "secondary"
                if st.button(
                    btn_label,
                    key=f"btn_demo_{pkey}",
                    use_container_width=True,
                    type=btn_type,
                ):
                    st.session_state["active_demo_key"] = pkey
                    st.session_state["show_demo_selector"] = True
                    st.rerun()

    # ── Determine which source to analyse ─────────────────────────────────
    text = None

    if uploaded_file:
        st.session_state["active_demo_key"] = None
        parser = ResumeParser()
        try:
            file_type = uploaded_file.name.split(".")[-1]
            text = parser.parse(file_content=uploaded_file.read(), file_type=file_type)
        except Exception as e:
            st.error(f"❌ Failed to parse the uploaded file: {e}")
            st.info("💡 Make sure the file is a valid PDF, DOCX, or TXT file and is not corrupted.")
            return

    elif st.session_state.get("active_demo_key"):
        active_key = st.session_state["active_demo_key"]
        curr_profile = DEMO_PROFILES.get(active_key, DEMO_PROFILES["data_science"])
        try:
            with open(curr_profile["file"], "r", encoding="utf-8") as f:
                text = f.read()

            # Active demo status banner with reset
            b1, b2 = st.columns([4, 1])
            with b1:
                st.markdown(
                    f"""
<div class="demo-active-banner">
    <div class="demo-active-info">
        <span style="font-size:1.8rem;">{curr_profile['icon']}</span>
        <div>
            <div class="demo-active-text">Active Demo Candidate: <strong>{curr_profile['candidate_name']}</strong>
            — <span style="color:{curr_profile['accent']}; font-weight:600;">{curr_profile['title']}</span></div>
            <div style="font-size:0.8rem; color:#94a3b8;">Analyzing {curr_profile['field_name']} profile •
            Click another card above to switch fields anytime.</div>
        </div>
    </div>
</div>
                    """,
                    unsafe_allow_html=True,
                )
            with b2:
                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.button(
                    "✖️ Clear Demo",
                    use_container_width=True,
                    help="Clear demo mode to upload your own resume",
                ):
                    st.session_state["active_demo_key"] = None
                    st.session_state["show_demo_selector"] = False
                    st.rerun()

            with st.expander(f"📄 View {curr_profile['candidate_name']}'s Full Resume Source"):
                st.code(text, language="text")

        except FileNotFoundError:
            st.error(
                f"❌ Demo resume file not found: `{curr_profile['file']}`. Please ensure samples exist."
            )
            return

    if text:
        custom_jd = jd_text_in if jd_text_in and jd_text_in.strip() else None
        custom_jd_title = jd_title_in if jd_title_in else ""
        run_analysis(
            text,
            target_role,
            run_ats,
            run_skills,
            run_ai,
            run_jobs,
            job_description_text=custom_jd,
            job_title_input=custom_jd_title,
        )

    # ── Footer ────────────────────────────────────────────────────────────
    st.markdown(
        """
<div class="app-footer">
<p>RESUME SCANNER v2.0 — Production-Grade Engineering Edition • Built by Soham</p>
</div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
