"""
Resume Scanner - AI-Powered Resume Analysis System
Main Streamlit Application - Premium UI Edition
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from resume_scanner import ResumeParser, NLPEngine, ATSScorer, AIDetector, JobMatcher

# Page Configuration
st.set_page_config(
    page_title="Resume Scanner | AI-Powered Analysis",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS with Glassmorphism, Animations & Modern Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --primary: #8b5cf6;
        --secondary: #06b6d4;
        --accent: #f472b6;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --dark: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.7);
    }
    
    .main { font-family: 'Space Grotesk', sans-serif; }
    
    /* Animated Background */
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #172554, #0c4a6e, #134e4a);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15);
        border-color: rgba(139, 92, 246, 0.4);
    }
    
    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 40px 20px;
        margin-bottom: 30px;
    }
    
    .hero-icon {
        font-size: 4rem;
        margin-bottom: 15px;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 12px;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.2rem;
        font-weight: 400;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* Metric Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin: 30px 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(6, 182, 212, 0.1));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: scale(1.03);
        border-color: rgba(139, 92, 246, 0.5);
    }
    
    .metric-value {
        font-size: 2.8rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        background: linear-gradient(135deg, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 8px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Skill Badges */
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(6, 182, 212, 0.2));
        border: 1px solid rgba(139, 92, 246, 0.4);
        color: #e2e8f0;
        padding: 8px 16px;
        border-radius: 25px;
        margin: 4px;
        font-size: 0.85rem;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: default;
    }
    
    .skill-badge:hover {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.5), rgba(6, 182, 212, 0.4));
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(139, 92, 246, 0.3);
    }
    
    /* Feedback Items */
    .feedback-item {
        padding: 12px 16px;
        border-radius: 12px;
        margin: 8px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .feedback-positive {
        background: rgba(16, 185, 129, 0.15);
        border-left: 3px solid #10b981;
        color: #6ee7b7;
    }
    
    .feedback-warning {
        background: rgba(245, 158, 11, 0.15);
        border-left: 3px solid #f59e0b;
        color: #fcd34d;
    }
    
    .feedback-negative {
        background: rgba(239, 68, 68, 0.15);
        border-left: 3px solid #ef4444;
        color: #fca5a5;
    }
    
    /* Upload Area */
    .uploadedFile {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px dashed rgba(139, 92, 246, 0.4) !important;
        border-radius: 16px !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95), rgba(30, 27, 75, 0.95));
        border-right: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stCheckbox label {
        color: #e2e8f0 !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        padding: 5px;
        gap: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(6, 182, 212, 0.2)) !important;
        color: #f1f5f9 !important;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: rgba(16, 185, 129, 0.15) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 12px !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.15) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 12px !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.6) !important;
        border-radius: 12px !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #8b5cf6, #06b6d4) !important;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #f1f5f9;
        margin: 25px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(139, 92, 246, 0.3);
    }
    
    /* Category Title */
    .category-title {
        color: #8b5cf6;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Animated pulse for live indicator */
    .pulse {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        animation: pulse 2s infinite;
        margin-right: 8px;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
</style>
""", unsafe_allow_html=True)


def create_gauge_chart(value, title, max_val=100):
    """Create a premium gauge chart."""
    if value >= 70:
        color = "#10b981"
    elif value >= 50:
        color = "#f59e0b"
    else:
        color = "#ef4444"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 18, 'color': '#f1f5f9', 'family': 'Space Grotesk'}},
        number={'font': {'size': 48, 'color': '#f1f5f9', 'family': 'JetBrains Mono'}},
        gauge={
            'axis': {'range': [0, max_val], 'tickcolor': '#475569', 'tickwidth': 2},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': 'rgba(30,41,59,0.5)',
            'borderwidth': 2,
            'bordercolor': 'rgba(139,92,246,0.3)',
            'steps': [
                {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.15)'},
                {'range': [40, 70], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
            ],
            'threshold': {
                'line': {'color': '#8b5cf6', 'width': 3},
                'thickness': 0.8,
                'value': value
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=280,
        margin=dict(l=30, r=30, t=60, b=30),
        font={'family': 'Space Grotesk'}
    )
    return fig


def create_skill_radar(skills_dict):
    """Create radar chart for skills."""
    categories = [c.replace('_', ' ').title() for c in skills_dict.keys()]
    values = [len(v) for v in skills_dict.values()]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(139, 92, 246, 0.25)',
        line=dict(color='#8b5cf6', width=3),
        marker=dict(size=8, color='#06b6d4')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, max(values)+3] if values else [0, 5],
                gridcolor='rgba(148, 163, 184, 0.15)',
                linecolor='rgba(148, 163, 184, 0.15)'
            ),
            angularaxis=dict(
                gridcolor='rgba(148, 163, 184, 0.15)',
                linecolor='rgba(148, 163, 184, 0.15)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Space Grotesk'),
        showlegend=False,
        height=380,
        margin=dict(l=80, r=80, t=40, b=40)
    )
    return fig


def create_job_match_chart(matches):
    """Create horizontal bar chart for job matches."""
    roles = [m['role'] for m in matches]
    scores = [m['match'] for m in matches]
    
    colors = ['#10b981' if s >= 70 else '#f59e0b' if s >= 50 else '#ef4444' for s in scores]
    
    fig = go.Figure(go.Bar(
        x=scores,
        y=roles,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.2)', width=1)
        ),
        text=[f'{s:.1f}%' for s in scores],
        textposition='inside',
        textfont=dict(color='white', size=14, family='JetBrains Mono')
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Space Grotesk'),
        xaxis=dict(
            range=[0, 100], 
            gridcolor='rgba(148, 163, 184, 0.1)',
            showgrid=True
        ),
        yaxis=dict(gridcolor='rgba(148, 163, 184, 0.1)'),
        height=320,
        margin=dict(l=20, r=30, t=20, b=30),
        bargap=0.3
    )
    return fig


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
