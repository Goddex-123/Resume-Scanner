"""
Resume Scanner - AI-Powered Resume Analysis System
Main Streamlit Application — Premium UI Edition v2
"""

import os
import streamlit as st
from resume_scanner import ResumeParser, NLPEngine, ATSScorer, AIDetector, JobMatcher
from resume_scanner.ui.styles import CUSTOM_CSS
from resume_scanner.ui.charts import (
    create_gauge_chart,
    create_skill_radar,
    create_job_match_chart,
    create_score_breakdown_chart,
    create_keyword_density_chart,
    create_text_quality_chart,
    create_ai_breakdown_chart,
)

# Page Configuration
st.set_page_config(
    page_title="Resume Scanner | AI-Powered Analysis",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Premium CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ─── Path to the built-in demo resume ───────────────────────────────────────
DEMO_RESUME_PATH = os.path.join(os.path.dirname(__file__), "samples", "sample_resume.txt")


# ─────────────────────────────────────────────────────────────────────────────
# Helper: render a custom stat bar (CSS-driven)
# ─────────────────────────────────────────────────────────────────────────────
def _stat_bar(label: str, value: float, max_val: float = 100, color: str = "#8b5cf6"):
    pct = min(value / max_val * 100, 100)
    st.markdown(f"""
    <div class="stat-bar-container">
        <div class="stat-bar-label">
            <span>{label}</span>
            <span style="color:{color}; font-family:'JetBrains Mono',monospace; font-weight:600;">{value:.0f}</span>
        </div>
        <div class="stat-bar-track">
            <div class="stat-bar-fill" style="width:{pct}%; background:linear-gradient(90deg, {color}, {color}aa);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Main analysis pipeline
# ─────────────────────────────────────────────────────────────────────────────
def run_analysis(text: str, target_role: str, run_ats: bool, run_skills: bool,
                 run_ai: bool, run_jobs: bool):
    """Run the full analysis pipeline and render results."""

    progress = st.progress(0, text="🔍 Initializing analysis...")

    # ── Parse extra info ──────────────────────────────────────────────────
    parser = ResumeParser()
    parser.text = text            # set so helper methods work
    contact_info = parser.extract_contact_info()
    sections_found = parser.get_sections()

    # ── NLP Engine ────────────────────────────────────────────────────────
    try:
        progress.progress(20, text="🧠 Loading NLP engine...")
        nlp_engine = NLPEngine(use_spacy=False)
        skills = nlp_engine.extract_skills(text) if run_skills else {}
        text_quality = nlp_engine.analyze_text_quality(text)
        exp_years, exp_entries = nlp_engine.calculate_experience_years(text)
    except Exception as e:
        st.warning(f"⚠️ Skill extraction encountered an issue: {e}")
        skills, text_quality = {}, _empty_tq()
        exp_years, exp_entries = 0, []

    # ── ATS Scoring ───────────────────────────────────────────────────────
    try:
        progress.progress(45, text="📋 Calculating ATS score...")
        ats_scorer = ATSScorer()
        role = None if target_role == "Auto-Detect" else target_role.lower().replace(' ', '_')
        ats_results = ats_scorer.calculate_score(text, role) if run_ats else {}
    except Exception as e:
        st.warning(f"⚠️ ATS scoring encountered an issue: {e}")
        ats_results = {}

    # ── AI Detection ──────────────────────────────────────────────────────
    try:
        progress.progress(65, text="🤖 Analyzing content authenticity...")
        ai_detector = AIDetector()
        ai_results = ai_detector.analyze(text) if run_ai else {}
    except Exception as e:
        st.warning(f"⚠️ AI detection encountered an issue: {e}")
        ai_results = {}

    # ── Job Matching ──────────────────────────────────────────────────────
    try:
        progress.progress(85, text="💼 Matching job roles...")
        job_matcher = JobMatcher()
        job_results = job_matcher.match(text) if run_jobs else {}
    except Exception as e:
        st.warning(f"⚠️ Job matching encountered an issue: {e}")
        job_results = {}

    progress.progress(100, text="✨ Analysis complete!")

    st.markdown('<br>', unsafe_allow_html=True)
    st.success("✅ Analysis complete! Scroll down for your detailed results.")

    # ══════════════════════════════════════════════════════════════════════
    # TOP METRIC CARDS
    # ══════════════════════════════════════════════════════════════════════
    ats_score = ats_results.get('scores', {}).get('total', 0)
    total_skills = sum(len(v) for v in skills.values())
    ai_prob = ai_results.get('ai_probability', 0)
    best_match = job_results.get('best_match', {})
    match_pct = best_match.get('match', 0) if best_match else 0

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, val, label in [
        (c1, "📋", f"{ats_score:.0f}", "ATS Score"),
        (c2, "🧠", f"{total_skills}", "Skills Found"),
        (c3, "🤖", f"{ai_prob:.0f}%", "AI Probability"),
        (c4, "💼", f"{match_pct:.0f}%", "Best Match"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-icon">{icon}</span>
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════
    # QUICK INSIGHTS ROW (Contact + Sections + Experience)
    # ══════════════════════════════════════════════════════════════════════
    qi1, qi2, qi3 = st.columns(3)

    with qi1:
        st.markdown("""
        <div class="analysis-card">
            <div class="analysis-card-title">📇 Contact Information</div>
            <div class="contact-grid">
        """, unsafe_allow_html=True)

        items = [
            ("📧", "Email", contact_info.get('email', '—')),
            ("📱", "Phone", contact_info.get('phone', '—')),
            ("🔗", "LinkedIn", contact_info.get('linkedin', '—')),
            ("💻", "GitHub", contact_info.get('github', '—')),
        ]
        html_items = ""
        for ic, lbl, val in items:
            found_class = "" if val and val != '—' else 'style="opacity:0.4;"'
            html_items += f"""
                <div class="contact-item" {found_class}>
                    <span class="contact-icon">{ic}</span>
                    <div>
                        <div class="contact-label">{lbl}</div>
                        <div class="contact-value">{val or '—'}</div>
                    </div>
                </div>
            """
        st.markdown(html_items + "</div></div>", unsafe_allow_html=True)

    with qi2:
        st.markdown("""
        <div class="analysis-card">
            <div class="analysis-card-title">📑 Resume Sections</div>
        """, unsafe_allow_html=True)

        section_labels = {
            'contact': '📇 Contact',
            'summary': '📝 Summary',
            'experience': '💼 Experience',
            'education': '🎓 Education',
            'skills': '🛠️ Skills',
            'projects': '🚀 Projects',
            'certifications': '🏅 Certifications',
        }
        html_checks = ""
        for key, label in section_labels.items():
            found = sections_found.get(key, False)
            icon = '<span class="check-found">✓</span>' if found else '<span class="check-missing">✗</span>'
            html_checks += f'<div class="checklist-item">{icon}<span class="checklist-label">{label}</span></div>'

        st.markdown(html_checks + "</div>", unsafe_allow_html=True)

    with qi3:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-card-title">⏱️ Experience</div>
            <div style="text-align:center; margin:8px 0;">
                <div style="font-size:2.2rem; font-weight:700; font-family:'JetBrains Mono',monospace;
                    background:linear-gradient(135deg,#8b5cf6,#06b6d4);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">
                    {exp_years}+
                </div>
                <div style="color:#94a3b8; font-size:0.82rem; text-transform:uppercase; letter-spacing:1px;">Years Estimated</div>
            </div>
            <div class="exp-timeline">
        """, unsafe_allow_html=True)

        if exp_entries:
            for entry in exp_entries[:5]:
                end_label = "Present" if entry['end'] >= 2026 else str(entry['end'])
                st.markdown(f"""
                    <div class="exp-item">
                        <span class="exp-years">{entry['years']} yr{'s' if entry['years'] != 1 else ''}</span>
                        <span class="exp-range"> — {entry['start']} → {end_label}</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#64748b; font-size:0.85rem; padding:6px 0;">No date ranges detected</div>', unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════
    # DETAILED TABS
    # ══════════════════════════════════════════════════════════════════════
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 ATS Analysis", "🧠 Skills Map", "🤖 AI Detection", "💼 Job Fit", "📈 Deep Insights"
    ])

    # ── ATS Tab ───────────────────────────────────────────────────────────
    with tab1:
        if run_ats and ats_results:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.plotly_chart(create_gauge_chart(ats_score, "ATS Compatibility"),
                               use_container_width=True)
                sub_scores = ats_results.get('scores', {})
                if sub_scores:
                    st.plotly_chart(create_score_breakdown_chart(sub_scores),
                                   use_container_width=True)

            with col_b:
                st.markdown('<h3 class="section-header">📋 Feedback</h3>', unsafe_allow_html=True)
                for fb in ats_results.get('feedback', []):
                    if fb.startswith('✅'):
                        css = "feedback-positive"
                    elif fb.startswith('⚠️') or fb.startswith('💡'):
                        css = "feedback-warning"
                    else:
                        css = "feedback-negative"
                    st.markdown(f'<div class="feedback-item {css}">{fb}</div>', unsafe_allow_html=True)

                st.markdown(f"""
                <div class="grade-box">
                    <strong>Grade:</strong> {ats_results.get('grade', 'N/A')} &nbsp;&nbsp;|&nbsp;&nbsp;
                    <strong>ATS Pass:</strong> {'✅ Likely' if ats_results.get('pass_ats') else '❌ Unlikely'}
                </div>
                """, unsafe_allow_html=True)

                # Improvement Suggestions
                suggestions = ats_scorer.get_improvement_suggestions()
                if suggestions:
                    st.markdown('<h3 class="section-header">🎯 Improvement Suggestions</h3>', unsafe_allow_html=True)
                    for i, sug in enumerate(suggestions, 1):
                        st.markdown(f"""
                        <div class="suggestion-item">
                            <div class="suggestion-number">{i}</div>
                            <div class="suggestion-text">{sug}</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("ATS Analysis is disabled. Enable it in the sidebar.")

    # ── Skills Tab ────────────────────────────────────────────────────────
    with tab2:
        if run_skills and skills:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.plotly_chart(create_skill_radar(skills), use_container_width=True)
            with col_b:
                st.markdown('<h3 class="section-header">🎯 Detected Skills</h3>', unsafe_allow_html=True)
                for category, skill_list in skills.items():
                    if skill_list:
                        cat_name = category.replace('_', ' ').title()
                        st.markdown(
                            f'<div class="category-title">{cat_name} ({len(skill_list)})</div>',
                            unsafe_allow_html=True
                        )
                        badges = ''.join(
                            [f'<span class="skill-badge">{s}</span>' for s in skill_list[:15]]
                        )
                        st.markdown(badges, unsafe_allow_html=True)
                        st.markdown('<br>', unsafe_allow_html=True)

            # Skill summary stats
            st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)
            st.markdown('<h3 class="section-header">📊 Skill Distribution</h3>', unsafe_allow_html=True)
            sc1, sc2, sc3 = st.columns(3)
            non_empty = {k: v for k, v in skills.items() if v}
            sorted_cats = sorted(non_empty.items(), key=lambda x: len(x[1]), reverse=True)

            for i, (cat, slist) in enumerate(sorted_cats):
                target_col = [sc1, sc2, sc3][i % 3]
                with target_col:
                    color = "#8b5cf6" if i % 3 == 0 else "#06b6d4" if i % 3 == 1 else "#f472b6"
                    _stat_bar(cat.replace('_', ' ').title(), len(slist), max(len(s) for s in skills.values()) + 2, color)
        else:
            st.info("Skill extraction is disabled. Enable it in the sidebar.")

    # ── AI Detection Tab ──────────────────────────────────────────────────
    with tab3:
        if run_ai and ai_results:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.plotly_chart(create_gauge_chart(ai_prob, "AI Content Score"),
                               use_container_width=True)

                # AI sub-score breakdown radar
                detailed = ai_results.get('detailed_scores', {})
                if detailed:
                    st.plotly_chart(create_ai_breakdown_chart(detailed),
                                   use_container_width=True)

            with col_b:
                verdict = ai_results.get('verdict', 'Unknown')
                confidence = ai_results.get('confidence', 'N/A')

                if 'Human' in verdict:
                    verdict_color = '#10b981'
                elif 'Mixed' in verdict:
                    verdict_color = '#f59e0b'
                else:
                    verdict_color = '#ef4444'

                st.markdown(f"""
                <div class="verdict-card">
                    <h3 class="section-header" style="text-align:center;">🔍 Verdict</h3>
                    <div style="font-size:1.6rem; color:{verdict_color}; font-weight:700; margin:12px 0;">
                        {verdict}
                    </div>
                    <div style="color:#94a3b8;">Confidence: <strong>{confidence}</strong></div>
                </div>
                """, unsafe_allow_html=True)

                if ai_results.get('flags'):
                    st.markdown('<h4 style="color:#f59e0b; margin-top:18px;">⚠️ Flags Detected</h4>', unsafe_allow_html=True)
                    for flag in ai_results['flags']:
                        st.markdown(f'<div class="feedback-item feedback-warning">{flag}</div>', unsafe_allow_html=True)

                # Score breakdown details
                if detailed:
                    st.markdown('<h3 class="section-header">📊 Sub-Score Breakdown</h3>', unsafe_allow_html=True)
                    for key, val in detailed.items():
                        label = key.replace('_', ' ').title()
                        color = "#ef4444" if val >= 60 else "#f59e0b" if val >= 35 else "#10b981"
                        _stat_bar(label, val, 100, color)
        else:
            st.info("AI Detection is disabled. Enable it in the sidebar.")

    # ── Job Fit Tab ───────────────────────────────────────────────────────
    with tab4:
        if run_jobs and job_results:
            matches = job_results.get('all_matches', [])
            if matches:
                st.plotly_chart(create_job_match_chart(matches), use_container_width=True)

                best = job_results.get('best_match')
                if best:
                    match_color = '#10b981' if best['match'] >= 70 else '#f59e0b'
                    st.markdown(f"""
                    <div class="best-match-card">
                        <div style="font-size:0.95rem; color:#94a3b8;">Best Match</div>
                        <div style="font-size:2rem; font-weight:700; color:{match_color};">
                            {best['role']}
                        </div>
                        <div style="font-size:1.4rem; color:#8b5cf6; font-family:'JetBrains Mono',monospace;">
                            {best['match']:.1f}% Match
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Recommendations
                recs = job_results.get('recommendations', [])
                if recs:
                    st.markdown('<h3 class="section-header">💡 Recommendations</h3>', unsafe_allow_html=True)
                    for i, rec in enumerate(recs, 1):
                        st.markdown(f"""
                        <div class="suggestion-item">
                            <div class="suggestion-number">{i}</div>
                            <div class="suggestion-text">{rec}</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("Job Matching is disabled. Enable it in the sidebar.")

    # ── Deep Insights Tab ─────────────────────────────────────────────────
    with tab5:
        di1, di2 = st.columns([1, 1])

        with di1:
            # Text Quality Analysis
            st.markdown('<h3 class="section-header">📝 Writing Quality</h3>', unsafe_allow_html=True)
            st.plotly_chart(create_text_quality_chart(text_quality), use_container_width=True)

            # Raw stats
            st.markdown("""
            <div class="analysis-card">
                <div class="analysis-card-title">📊 Document Statistics</div>
            """, unsafe_allow_html=True)
            _stat_bar("Word Count", text_quality['word_count'], 1000, "#8b5cf6")
            _stat_bar("Sentences", text_quality['sentence_count'], 60, "#06b6d4")
            _stat_bar("Avg Sentence Length", text_quality['avg_sentence_length'], 30, "#f472b6")
            _stat_bar("Action Verbs", text_quality['action_verb_count'], 20, "#10b981")
            st.markdown("</div>", unsafe_allow_html=True)

        with di2:
            # Keyword Density
            if run_ats and ats_results:
                st.markdown('<h3 class="section-header">🔑 Keyword Coverage</h3>', unsafe_allow_html=True)

                # Reconstruct keyword lists
                scored_role = role or ats_scorer._detect_role(text.lower())
                scored_role = scored_role.lower().replace(' ', '_').replace('-', '_')
                if scored_role not in ats_scorer.ROLE_KEYWORDS:
                    scored_role = 'data_scientist'
                all_kw = ats_scorer.ROLE_KEYWORDS[scored_role]
                found_kw = [k for k in all_kw if k.lower() in text.lower()]
                missing_kw = [k for k in all_kw if k.lower() not in text.lower()]

                st.plotly_chart(create_keyword_density_chart(found_kw, missing_kw),
                               use_container_width=True)

                if found_kw:
                    st.markdown(f'<div class="category-title">✅ Found ({len(found_kw)})</div>', unsafe_allow_html=True)
                    badges = ''.join([f'<span class="skill-badge" style="border-color:rgba(16,185,129,0.3);">{k.title()}</span>' for k in found_kw])
                    st.markdown(badges, unsafe_allow_html=True)

                if missing_kw:
                    st.markdown(f'<br><div class="category-title">❌ Missing ({len(missing_kw)})</div>', unsafe_allow_html=True)
                    badges = ''.join([f'<span class="skill-badge" style="border-color:rgba(239,68,68,0.3); opacity:0.7;">{k.title()}</span>' for k in missing_kw])
                    st.markdown(badges, unsafe_allow_html=True)
            else:
                st.info("Enable ATS Scoring to see keyword analysis.")

            # Vocabulary Richness
            st.markdown("""
            <div class="analysis-card" style="margin-top:16px;">
                <div class="analysis-card-title">📖 Vocabulary Analysis</div>
            """, unsafe_allow_html=True)
            ttr = text_quality.get('vocabulary_richness', 0)
            ttr_pct = min(ttr * 100, 100)
            ttr_color = "#10b981" if ttr >= 0.5 else "#f59e0b" if ttr >= 0.35 else "#ef4444"
            _stat_bar("Type-Token Ratio", ttr, 1.0, ttr_color)

            avg_word = text_quality.get('avg_word_length', 0)
            _stat_bar("Avg Word Length", avg_word, 10, "#8b5cf6")

            verb_pct = text_quality.get('action_verb_percentage', 0)
            verb_color = "#10b981" if verb_pct >= 2.5 else "#f59e0b" if verb_pct >= 1.0 else "#ef4444"
            _stat_bar("Action Verb %", verb_pct, 5, verb_color)
            st.markdown("</div>", unsafe_allow_html=True)


def _empty_tq():
    """Returns empty text quality dict."""
    return {
        'word_count': 0, 'sentence_count': 0, 'avg_word_length': 0,
        'avg_sentence_length': 0, 'vocabulary_richness': 0,
        'action_verb_count': 0, 'action_verb_percentage': 0
    }


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    # ── Hero Section ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-container">
        <div class="hero-icon">🔬</div>
        <h1 class="hero-title">Resume Scanner</h1>
        <p class="hero-subtitle">AI-Powered Analysis • ATS Scoring • Skill Extraction</p>
        <div class="hero-badge">✦ v2.0 — Premium Edition</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown('<div class="sidebar-title">⚡ Quick Settings</div>', unsafe_allow_html=True)
        target_role = st.selectbox(
            "🎯 Target Role",
            ["Auto-Detect", "Data Scientist", "ML Engineer", "Data Analyst",
             "Software Engineer", "Data Engineer"],
            help="Select your target job role for better analysis"
        )

        st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">📊 Analysis Modules</div>', unsafe_allow_html=True)
        run_ats = st.checkbox("📋 ATS Scoring", value=True)
        run_skills = st.checkbox("🧠 Skill Extraction", value=True)
        run_ai = st.checkbox("🤖 AI Detection", value=True)
        run_jobs = st.checkbox("💼 Job Matching", value=True)

        st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">🔮 Powered By</div>', unsafe_allow_html=True)
        st.markdown("""
        <div>
            <span class="sidebar-tech-badge">NLP</span>
            <span class="sidebar-tech-badge">TF-IDF</span>
            <span class="sidebar-tech-badge">ML</span>
            <span class="sidebar-tech-badge">Heuristics</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; padding:8px 0;">
            <span class="pulse"></span>
            <span style="color:#94a3b8; font-size:0.78rem;">System Online</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Upload Section ────────────────────────────────────────────────────
    st.markdown("""
    <div class="upload-section">
        <div class="upload-section-inner">
            <div class="upload-title">📄 Upload Your Resume</div>
            <div class="upload-hint">Supports PDF and DOCX • Up to 1 GB</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drop your resume here",
        type=['pdf', 'docx'],
        help="Supports PDF and DOCX formats, up to 1 GB",
        label_visibility="collapsed"
    )

    # ── Demo Button ───────────────────────────────────────────────────────
    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

    _, demo_col, _ = st.columns([1, 2, 1])
    with demo_col:
        demo_clicked = st.button(
            "🚀  Try Demo Resume — See It In Action",
            use_container_width=True,
            type="secondary"
        )

    # ── Determine which source to analyse ─────────────────────────────────
    text = None

    if uploaded_file:
        parser = ResumeParser()
        try:
            file_type = uploaded_file.name.split('.')[-1]
            text = parser.parse(file_content=uploaded_file.read(), file_type=file_type)
        except Exception as e:
            st.error(f"❌ Failed to parse the uploaded file: {e}")
            st.info("💡 Make sure the file is a valid PDF or DOCX and is not corrupted.")
            return

    elif demo_clicked:
        try:
            with open(DEMO_RESUME_PATH, 'r', encoding='utf-8') as f:
                text = f.read()
            st.info("📄 Analyzing the built-in **demo resume** — upload your own to get personalized results!")
        except FileNotFoundError:
            st.error("❌ Demo resume file not found. Please ensure `samples/sample_resume.txt` exists.")
            return

    if text:
        run_analysis(text, target_role, run_ats, run_skills, run_ai, run_jobs)

    # ── Footer ────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="app-footer">
        <p>RESUME SCANNER v2.0 — Built with ❤️ by Soham</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
