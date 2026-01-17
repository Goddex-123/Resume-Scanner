"""
Resume Scanner - AI-Powered Resume Analysis System
Main Streamlit Application
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from resume_scanner import ResumeParser, NLPEngine, ATSScorer, AIDetector, JobMatcher

# Page Configuration
st.set_page_config(
    page_title="Resume Scanner | AI-Powered Analysis",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .main { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: #a0aec0;
        font-size: 0.9rem;
        margin-top: 5px;
    }
    
    .section-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 20px 0 10px 0;
    }
    
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        margin: 3px;
        font-size: 0.85rem;
    }
    
    .feedback-positive { color: #48bb78; }
    .feedback-warning { color: #ecc94b; }
    .feedback-negative { color: #fc8181; }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .hero-subtitle {
        text-align: center;
        color: #a0aec0;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)


def create_gauge_chart(value, title, max_val=100):
    """Create a gauge chart for scores."""
    color = "#48bb78" if value >= 70 else "#ecc94b" if value >= 50 else "#fc8181"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 16, 'color': '#e2e8f0'}},
        number={'font': {'size': 40, 'color': '#e2e8f0'}},
        gauge={
            'axis': {'range': [0, max_val], 'tickcolor': '#4a5568'},
            'bar': {'color': color},
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50], 'color': 'rgba(252, 129, 129, 0.2)'},
                {'range': [50, 70], 'color': 'rgba(236, 201, 75, 0.2)'},
                {'range': [70, 100], 'color': 'rgba(72, 187, 120, 0.2)'}
            ]
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=250,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


def create_skill_radar(skills_dict):
    """Create radar chart for skills distribution."""
    categories = list(skills_dict.keys())
    values = [len(v) for v in skills_dict.values()]
    
    # Clean up category names
    categories = [c.replace('_', ' ').title() for c in categories]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.3)',
        line=dict(color='#667eea', width=2),
        name='Skills'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(values)+2] if values else [0, 5],
                           gridcolor='rgba(255,255,255,0.1)'),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0'),
        showlegend=False,
        height=350,
        margin=dict(l=60, r=60, t=40, b=40)
    )
    return fig


def create_job_match_chart(matches):
    """Create horizontal bar chart for job matches."""
    roles = [m['role'] for m in matches]
    scores = [m['match'] for m in matches]
    
    colors = ['#48bb78' if s >= 70 else '#ecc94b' if s >= 50 else '#fc8181' for s in scores]
    
    fig = go.Figure(go.Bar(
        x=scores,
        y=roles,
        orientation='h',
        marker_color=colors,
        text=[f'{s}%' for s in scores],
        textposition='auto'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0'),
        xaxis=dict(range=[0, 100], gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        height=300,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig


def main():
    # Hero Section
    st.markdown('<h1 class="hero-title">📄 Resume Scanner</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">AI-Powered Resume Analysis | ATS Scoring | Skill Extraction</p>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        target_role = st.selectbox(
            "Target Role",
            ["Auto-Detect", "Data Scientist", "ML Engineer", "Data Analyst", 
             "Software Engineer", "Data Engineer"]
        )
        
        st.markdown("---")
        st.markdown("### 📊 Analysis Modules")
        run_ats = st.checkbox("ATS Scoring", value=True)
        run_skills = st.checkbox("Skill Extraction", value=True)
        run_ai = st.checkbox("AI Detection", value=True)
        run_jobs = st.checkbox("Job Matching", value=True)
        
        st.markdown("---")
        st.markdown("### 📖 About")
        st.markdown("""
        This tool analyzes resumes using:
        - **NLP** for skill extraction
        - **ML** for job matching
        - **Heuristics** for ATS scoring
        - **Pattern Analysis** for AI detection
        """)
    
    # File Upload
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF or DOCX)",
        type=['pdf', 'docx'],
        help="Drag and drop or click to upload"
    )
    
    if uploaded_file:
        # Parse Resume
        with st.spinner("🔍 Analyzing your resume..."):
            parser = ResumeParser()
            try:
                file_type = uploaded_file.name.split('.')[-1]
                text = parser.parse(file_content=uploaded_file.read(), file_type=file_type)
            except Exception as e:
                st.error(f"Error parsing file: {str(e)}")
                return
            
            # Initialize analyzers
            nlp_engine = NLPEngine(use_spacy=False)  # Fallback mode
            ats_scorer = ATSScorer()
            ai_detector = AIDetector()
            job_matcher = JobMatcher()
            
            # Run analyses
            skills = nlp_engine.extract_skills(text) if run_skills else {}
            text_quality = nlp_engine.analyze_text_quality(text)
            
            role = None if target_role == "Auto-Detect" else target_role.lower().replace(' ', '_')
            ats_results = ats_scorer.calculate_score(text, role) if run_ats else {}
            ai_results = ai_detector.analyze(text) if run_ai else {}
            job_results = job_matcher.match(text) if run_jobs else {}
        
        st.success("✅ Analysis Complete!")
        
        # Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            ats_score = ats_results.get('scores', {}).get('total', 0)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{ats_score}</div>
                <div class="metric-label">ATS Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_skills = sum(len(v) for v in skills.values())
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_skills}</div>
                <div class="metric-label">Skills Found</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            ai_prob = ai_results.get('ai_probability', 0)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{ai_prob}%</div>
                <div class="metric-label">AI Probability</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            best_match = job_results.get('best_match', {})
            match_pct = best_match.get('match', 0) if best_match else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{match_pct}%</div>
                <div class="metric-label">Best Job Match</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Detailed Results
        tab1, tab2, tab3, tab4 = st.tabs(["📊 ATS Score", "🧠 Skills", "🤖 AI Detection", "💼 Job Match"])
        
        with tab1:
            if run_ats and ats_results:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.plotly_chart(create_gauge_chart(ats_score, "ATS Compatibility"), 
                                   use_container_width=True)
                with col2:
                    st.markdown("### 📋 Feedback")
                    for fb in ats_results.get('feedback', []):
                        if fb.startswith('✅'):
                            st.markdown(f"<span class='feedback-positive'>{fb}</span>", 
                                       unsafe_allow_html=True)
                        elif fb.startswith('⚠️') or fb.startswith('💡'):
                            st.markdown(f"<span class='feedback-warning'>{fb}</span>", 
                                       unsafe_allow_html=True)
                        else:
                            st.markdown(f"<span class='feedback-negative'>{fb}</span>", 
                                       unsafe_allow_html=True)
                    
                    st.markdown(f"**Grade:** {ats_results.get('grade', 'N/A')}")
                    st.markdown(f"**ATS Pass:** {'✅ Yes' if ats_results.get('pass_ats') else '❌ No'}")
        
        with tab2:
            if run_skills and skills:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.plotly_chart(create_skill_radar(skills), use_container_width=True)
                with col2:
                    for category, skill_list in skills.items():
                        if skill_list:
                            cat_name = category.replace('_', ' ').title()
                            st.markdown(f"**{cat_name}** ({len(skill_list)})")
                            badges = ' '.join([f"<span class='skill-badge'>{s}</span>" 
                                             for s in skill_list[:10]])
                            st.markdown(badges, unsafe_allow_html=True)
                            st.markdown("")
        
        with tab3:
            if run_ai and ai_results:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.plotly_chart(create_gauge_chart(ai_prob, "AI Content Probability"), 
                                   use_container_width=True)
                with col2:
                    st.markdown(f"### Verdict: {ai_results.get('verdict', 'Unknown')}")
                    st.markdown(f"**Confidence:** {ai_results.get('confidence', 'N/A')}")
                    
                    if ai_results.get('flags'):
                        st.markdown("### ⚠️ Flags Detected")
                        for flag in ai_results['flags']:
                            st.warning(flag)
        
        with tab4:
            if run_jobs and job_results:
                matches = job_results.get('all_matches', [])
                if matches:
                    st.plotly_chart(create_job_match_chart(matches), use_container_width=True)
                    
                    best = job_results.get('best_match')
                    if best:
                        st.success(f"🎯 Best Match: **{best['role']}** ({best['match']}%)")
        
        # Text Quality Stats
        with st.expander("📈 Text Statistics"):
            cols = st.columns(4)
            cols[0].metric("Word Count", text_quality['word_count'])
            cols[1].metric("Sentences", text_quality['sentence_count'])
            cols[2].metric("Avg Sentence Length", text_quality['avg_sentence_length'])
            cols[3].metric("Action Verbs", text_quality['action_verb_count'])


if __name__ == "__main__":
    main()
