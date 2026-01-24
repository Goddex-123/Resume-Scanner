"""
Resume Scanner - AI-Powered Resume Analysis System
Main Streamlit Application - Premium UI Edition
"""

import streamlit as st
import plotly.express as px
from resume_scanner import ResumeParser, NLPEngine, ATSScorer, AIDetector, JobMatcher
from resume_scanner.ui.styles import CUSTOM_CSS
from resume_scanner.ui.charts import (
    create_gauge_chart, 
    create_skill_radar, 
    create_job_match_chart
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

def main():
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-icon">🔬</div>
        <h1 class="hero-title">Resume Scanner</h1>
        <p class="hero-subtitle">AI-Powered Analysis • ATS Scoring • Skill Extraction</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚡ Quick Settings")
        target_role = st.selectbox(
            "🎯 Target Role",
            ["Auto-Detect", "Data Scientist", "ML Engineer", "Data Analyst", 
             "Software Engineer", "Data Engineer"],
            help="Select your target job role for better analysis"
        )
        
        st.markdown("---")
        st.markdown("### 📊 Analysis Modules")
        run_ats = st.checkbox("📋 ATS Scoring", value=True)
        run_skills = st.checkbox("🧠 Skill Extraction", value=True)
        run_ai = st.checkbox("🤖 AI Detection", value=True)
        run_jobs = st.checkbox("💼 Job Matching", value=True)
        
        st.markdown("---")
        st.markdown("### 🔮 Powered By")
        st.markdown("""
        <div style="color: #94a3b8; font-size: 0.85rem;">
        • NLP & Pattern Matching<br>
        • TF-IDF Vectorization<br>
        • Machine Learning<br>
        • Advanced Heuristics
        </div>
        """, unsafe_allow_html=True)
    
    # File Upload with custom styling
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "📄 Drop your resume here (PDF or DOCX)",
        type=['pdf', 'docx'],
        help="Supports PDF and DOCX formats"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file:
        # Analysis Progress
        progress = st.progress(0, text="🔍 Initializing analysis...")
        
        # Parse Resume
        parser = ResumeParser()
        try:
            progress.progress(20, text="📄 Parsing document...")
            file_type = uploaded_file.name.split('.')[-1]
            text = parser.parse(file_content=uploaded_file.read(), file_type=file_type)
        except Exception as e:
            st.error(f"❌ Error parsing file: {str(e)}")
            return
        
        # Initialize analyzers
        progress.progress(40, text="🧠 Loading NLP engine...")
        nlp_engine = NLPEngine(use_spacy=False)
        ats_scorer = ATSScorer()
        ai_detector = AIDetector()
        job_matcher = JobMatcher()
        
        # Run analyses
        progress.progress(60, text="📊 Extracting skills...")
        skills = nlp_engine.extract_skills(text) if run_skills else {}
        text_quality = nlp_engine.analyze_text_quality(text)
        
        progress.progress(75, text="🎯 Calculating scores...")
        role = None if target_role == "Auto-Detect" else target_role.lower().replace(' ', '_')
        ats_results = ats_scorer.calculate_score(text, role) if run_ats else {}
        
        progress.progress(85, text="🤖 Analyzing content...")
        ai_results = ai_detector.analyze(text) if run_ai else {}
        
        progress.progress(95, text="💼 Matching jobs...")
        job_results = job_matcher.match(text) if run_jobs else {}
        
        progress.progress(100, text="✨ Analysis complete!")
        
        st.markdown('<br>', unsafe_allow_html=True)
        st.success("✅ Analysis Complete! Scroll down for detailed results.")
        
        # Metrics Row with Custom Cards
        ats_score = ats_results.get('scores', {}).get('total', 0)
        total_skills = sum(len(v) for v in skills.values())
        ai_prob = ai_results.get('ai_probability', 0)
        best_match = job_results.get('best_match', {})
        match_pct = best_match.get('match', 0) if best_match else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{ats_score:.0f}</div>
                <div class="metric-label">ATS Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_skills}</div>
                <div class="metric-label">Skills Found</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{ai_prob:.0f}%</div>
                <div class="metric-label">AI Probability</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{match_pct:.0f}%</div>
                <div class="metric-label">Best Match</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<br>', unsafe_allow_html=True)
        
        # Detailed Results Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 ATS Analysis", "🧠 Skills Map", "🤖 AI Detection", "💼 Job Fit"])
        
        with tab1:
            if run_ats and ats_results:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.plotly_chart(create_gauge_chart(ats_score, "ATS Compatibility"), 
                                   use_container_width=True)
                with col2:
                    st.markdown('<h3 class="section-header">📋 Feedback</h3>', unsafe_allow_html=True)
                    for fb in ats_results.get('feedback', []):
                        if fb.startswith('✅'):
                            st.markdown(f'<div class="feedback-item feedback-positive">{fb}</div>', 
                                       unsafe_allow_html=True)
                        elif fb.startswith('⚠️') or fb.startswith('💡'):
                            st.markdown(f'<div class="feedback-item feedback-warning">{fb}</div>', 
                                       unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="feedback-item feedback-negative">{fb}</div>', 
                                       unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="margin-top: 20px; padding: 15px; background: rgba(139,92,246,0.1); border-radius: 12px;">
                        <strong>Grade:</strong> {ats_results.get('grade', 'N/A')} &nbsp;&nbsp;|&nbsp;&nbsp;
                        <strong>ATS Pass:</strong> {'✅ Likely' if ats_results.get('pass_ats') else '❌ Unlikely'}
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab2:
            if run_skills and skills:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.plotly_chart(create_skill_radar(skills), use_container_width=True)
                with col2:
                    st.markdown('<h3 class="section-header">🎯 Detected Skills</h3>', unsafe_allow_html=True)
                    for category, skill_list in skills.items():
                        if skill_list:
                            cat_name = category.replace('_', ' ').title()
                            st.markdown(f'<div class="category-title">{cat_name} ({len(skill_list)})</div>', 
                                       unsafe_allow_html=True)
                            badges = ''.join([f'<span class="skill-badge">{s}</span>' for s in skill_list[:12]])
                            st.markdown(badges, unsafe_allow_html=True)
                            st.markdown('<br>', unsafe_allow_html=True)
        
        with tab3:
            if run_ai and ai_results:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.plotly_chart(create_gauge_chart(ai_prob, "AI Content Score"), 
                                   use_container_width=True)
                with col2:
                    verdict = ai_results.get('verdict', 'Unknown')
                    confidence = ai_results.get('confidence', 'N/A')
                    
                    verdict_color = '#10b981' if 'Human' in verdict else '#f59e0b' if 'Mixed' in verdict else '#ef4444'
                    
                    st.markdown(f"""
                    <h3 class="section-header">🔍 Verdict</h3>
                    <div style="font-size: 1.5rem; color: {verdict_color}; font-weight: 600; margin: 15px 0;">
                        {verdict}
                    </div>
                    <div style="color: #94a3b8;">Confidence: <strong>{confidence}</strong></div>
                    """, unsafe_allow_html=True)
                    
                    if ai_results.get('flags'):
                        st.markdown('<h4 style="color: #f59e0b; margin-top: 20px;">⚠️ Flags Detected</h4>', 
                                   unsafe_allow_html=True)
                        for flag in ai_results['flags']:
                            st.markdown(f'<div class="feedback-item feedback-warning">{flag}</div>', 
                                       unsafe_allow_html=True)
        
        with tab4:
            if run_jobs and job_results:
                matches = job_results.get('all_matches', [])
                if matches:
                    st.plotly_chart(create_job_match_chart(matches), use_container_width=True)
                    
                    best = job_results.get('best_match')
                    if best:
                        match_color = '#10b981' if best['match'] >= 70 else '#f59e0b'
                        st.markdown(f"""
                        <div style="text-align: center; padding: 20px; background: rgba(139,92,246,0.1); border-radius: 16px; margin-top: 20px;">
                            <div style="font-size: 1.1rem; color: #94a3b8;">Best Match</div>
                            <div style="font-size: 2rem; font-weight: 700; color: {match_color};">
                                {best['role']}
                            </div>
                            <div style="font-size: 1.5rem; color: #8b5cf6;">{best['match']:.1f}% Match</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Text Stats Expander
        with st.expander("📈 Document Statistics"):
            cols = st.columns(5)
            cols[0].metric("📝 Words", text_quality['word_count'])
            cols[1].metric("📄 Sentences", text_quality['sentence_count'])
            cols[2].metric("📏 Avg Length", f"{text_quality['avg_sentence_length']:.1f}")
            cols[3].metric("💪 Action Verbs", text_quality['action_verb_count'])
            cols[4].metric("📊 Vocab Richness", f"{text_quality['vocabulary_richness']:.2f}")


if __name__ == "__main__":
    main()
