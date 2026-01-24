"""
Chart generation functions for Resume Scanner
"""

import plotly.graph_objects as go

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
    if not skills_dict:
        return go.Figure()

    categories = [c.replace('_', ' ').title() for c in skills_dict.keys()]
    values = [len(v) for v in skills_dict.values()]
    
    # Close the polygon
    if len(values) > 0:
        values_closed = values + [values[0]]
        categories_closed = categories + [categories[0]]
    else:
        values_closed = []
        categories_closed = []
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(139, 92, 246, 0.25)',
        line=dict(color='#8b5cf6', width=3),
        marker=dict(size=8, color='#06b6d4')
    ))
    
    max_val = max(values) if values else 5
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, max_val + 3],
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
    if not matches:
        return go.Figure()

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
