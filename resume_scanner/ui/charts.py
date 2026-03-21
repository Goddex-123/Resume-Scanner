"""
Chart generation functions for Resume Scanner — Premium Edition
"""

import plotly.graph_objects as go


def create_gauge_chart(value, title, max_val=100):
    """Create a premium gauge chart with neon glow styling."""
    if value >= 70:
        bar_color = "#10b981"
    elif value >= 50:
        bar_color = "#f59e0b"
    else:
        bar_color = "#ef4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': title,
            'font': {'size': 16, 'color': '#94a3b8', 'family': 'Inter'}
        },
        number={
            'font': {'size': 52, 'color': '#f1f5f9', 'family': 'JetBrains Mono'}
        },
        gauge={
            'axis': {
                'range': [0, max_val],
                'tickcolor': '#334155',
                'tickwidth': 1,
                'tickfont': {'color': '#64748b', 'size': 10}
            },
            'bar': {'color': bar_color, 'thickness': 0.7},
            'bgcolor': 'rgba(15,15,30,0.5)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 40], 'color': 'rgba(239,68,68,0.07)'},
                {'range': [40, 70], 'color': 'rgba(245,158,11,0.07)'},
                {'range': [70, 100], 'color': 'rgba(16,185,129,0.07)'}
            ],
            'threshold': {
                'line': {'color': '#8b5cf6', 'width': 3},
                'thickness': 0.85,
                'value': value
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=280,
        margin=dict(l=30, r=30, t=55, b=25),
        font={'family': 'Inter'}
    )
    return fig


def create_skill_radar(skills_dict):
    """Create a modern radar chart for skills."""
    if not skills_dict:
        return go.Figure()

    categories = [c.replace('_', ' ').title() for c in skills_dict.keys()]
    values = [len(v) for v in skills_dict.values()]

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
        fillcolor='rgba(139,92,246,0.12)',
        line=dict(color='#8b5cf6', width=2.5),
        marker=dict(
            size=7,
            color='#06b6d4',
            line=dict(color='#0a0a1a', width=2)
        ),
        hovertemplate='%{theta}: %{r} skills<extra></extra>'
    ))

    max_val = max(values) if values else 5

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_val + 2],
                gridcolor='rgba(139,92,246,0.06)',
                linecolor='rgba(139,92,246,0.06)',
                tickfont=dict(color='#475569', size=10)
            ),
            angularaxis=dict(
                gridcolor='rgba(139,92,246,0.06)',
                linecolor='rgba(139,92,246,0.06)',
                tickfont=dict(color='#94a3b8', size=11)
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Inter'),
        showlegend=False,
        height=380,
        margin=dict(l=80, r=80, t=30, b=30)
    )
    return fig


def create_job_match_chart(matches):
    """Create a modern horizontal bar chart for job matches."""
    if not matches:
        return go.Figure()

    roles = [m['role'] for m in matches]
    scores = [m['match'] for m in matches]

    colors = []
    for s in scores:
        if s >= 70:
            colors.append('rgba(16,185,129,0.85)')
        elif s >= 50:
            colors.append('rgba(245,158,11,0.85)')
        else:
            colors.append('rgba(239,68,68,0.75)')

    fig = go.Figure(go.Bar(
        x=scores,
        y=roles,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.08)', width=1),
            cornerradius=6
        ),
        text=[f'{s:.1f}%' for s in scores],
        textposition='inside',
        textfont=dict(color='white', size=13, family='JetBrains Mono'),
        hovertemplate='%{y}: %{x:.1f}%<extra></extra>'
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Inter'),
        xaxis=dict(
            range=[0, 100],
            gridcolor='rgba(139,92,246,0.06)',
            showgrid=True,
            zeroline=False,
            tickfont=dict(color='#64748b')
        ),
        yaxis=dict(
            gridcolor='rgba(139,92,246,0.06)',
            tickfont=dict(color='#94a3b8', size=12)
        ),
        height=320,
        margin=dict(l=20, r=30, t=15, b=25),
        bargap=0.3
    )
    return fig


def create_score_breakdown_chart(scores_dict):
    """Create horizontal bar chart showing ATS sub-score breakdown."""
    if not scores_dict:
        return go.Figure()

    labels = []
    values = []
    for key, val in scores_dict.items():
        if key == 'total':
            continue
        labels.append(key.replace('_', ' ').title())
        values.append(val)

    colors = []
    for v in values:
        if v >= 70:
            colors.append('rgba(16,185,129,0.8)')
        elif v >= 50:
            colors.append('rgba(245,158,11,0.8)')
        else:
            colors.append('rgba(239,68,68,0.7)')

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.06)', width=1),
            cornerradius=5
        ),
        text=[f'{v:.0f}' for v in values],
        textposition='inside',
        textfont=dict(color='white', size=12, family='JetBrains Mono'),
        hovertemplate='%{y}: %{x:.1f}/100<extra></extra>'
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Inter'),
        xaxis=dict(
            range=[0, 100],
            gridcolor='rgba(139,92,246,0.06)',
            showgrid=True,
            zeroline=False,
            title=dict(text='Score', font=dict(color='#64748b', size=11)),
            tickfont=dict(color='#64748b')
        ),
        yaxis=dict(
            tickfont=dict(color='#94a3b8', size=11),
            automargin=True
        ),
        height=250,
        margin=dict(l=10, r=20, t=10, b=30),
        bargap=0.35
    )
    return fig


def create_keyword_density_chart(found_keywords, missing_keywords):
    """Create a donut chart showing keyword coverage."""
    found = len(found_keywords)
    missing = len(missing_keywords)
    total = found + missing

    if total == 0:
        return go.Figure()

    fig = go.Figure(go.Pie(
        values=[found, missing],
        labels=['Found', 'Missing'],
        hole=0.65,
        marker=dict(
            colors=['rgba(16,185,129,0.8)', 'rgba(239,68,68,0.4)'],
            line=dict(color='rgba(0,0,0,0.3)', width=2)
        ),
        textinfo='label+percent',
        textfont=dict(color='#e2e8f0', size=13, family='Inter'),
        hovertemplate='%{label}: %{value} keywords (%{percent})<extra></extra>'
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Inter'),
        showlegend=False,
        height=240,
        margin=dict(l=20, r=20, t=10, b=10),
        annotations=[dict(
            text=f'<b>{found}/{total}</b>',
            x=0.5, y=0.5,
            font=dict(size=22, color='#8b5cf6', family='JetBrains Mono'),
            showarrow=False
        )]
    )
    return fig


def create_text_quality_chart(quality_metrics):
    """Create a horizontal bar chart for text quality metrics."""
    if not quality_metrics:
        return go.Figure()

    # Normalize to 0-100 scale for visual comparison
    metrics = {
        'Vocabulary Richness': min(quality_metrics.get('vocabulary_richness', 0) * 200, 100),
        'Action Verb Usage': min(quality_metrics.get('action_verb_percentage', 0) * 10, 100),
        'Sentence Clarity': max(0, 100 - abs(quality_metrics.get('avg_sentence_length', 20) - 20) * 3),
        'Content Depth': min(quality_metrics.get('word_count', 0) / 8, 100),
    }

    labels = list(metrics.keys())
    values = list(metrics.values())

    colors = []
    for v in values:
        if v >= 70:
            colors.append('rgba(16,185,129,0.75)')
        elif v >= 45:
            colors.append('rgba(245,158,11,0.75)')
        else:
            colors.append('rgba(239,68,68,0.65)')

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.06)', width=1),
            cornerradius=5
        ),
        text=[f'{v:.0f}%' for v in values],
        textposition='inside',
        textfont=dict(color='white', size=12, family='JetBrains Mono'),
        hovertemplate='%{y}: %{x:.0f}/100<extra></extra>'
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Inter'),
        xaxis=dict(
            range=[0, 100],
            gridcolor='rgba(139,92,246,0.06)',
            showgrid=True,
            zeroline=False,
            tickfont=dict(color='#64748b')
        ),
        yaxis=dict(
            tickfont=dict(color='#94a3b8', size=11),
            automargin=True
        ),
        height=200,
        margin=dict(l=10, r=20, t=10, b=20),
        bargap=0.35
    )
    return fig


def create_ai_breakdown_chart(detailed_scores):
    """Create a radar chart for AI detection breakdown."""
    if not detailed_scores:
        return go.Figure()

    categories = [k.replace('_', ' ').title() for k in detailed_scores.keys()]
    values = list(detailed_scores.values())

    values_closed = values + [values[0]]
    categories_closed = categories + [categories[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(239,68,68,0.1)',
        line=dict(color='#ef4444', width=2),
        marker=dict(size=6, color='#f59e0b', line=dict(color='#0a0a1a', width=2)),
        hovertemplate='%{theta}: %{r:.1f}/100<extra></extra>'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(239,68,68,0.06)',
                linecolor='rgba(239,68,68,0.06)',
                tickfont=dict(color='#475569', size=10)
            ),
            angularaxis=dict(
                gridcolor='rgba(239,68,68,0.06)',
                linecolor='rgba(239,68,68,0.06)',
                tickfont=dict(color='#94a3b8', size=11)
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Inter'),
        showlegend=False,
        height=280,
        margin=dict(l=60, r=60, t=20, b=20)
    )
    return fig
