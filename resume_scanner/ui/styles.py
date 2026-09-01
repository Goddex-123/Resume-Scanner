"""
Premium CSS styles for Resume Scanner — Ultra Modern Edition
Packed with animations while staying GPU-accelerated & performant.
"""

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --primary: #8b5cf6;
        --primary-glow: rgba(139, 92, 246, 0.4);
        --secondary: #06b6d4;
        --secondary-glow: rgba(6, 182, 212, 0.3);
        --accent: #f472b6;
        --accent-glow: rgba(244, 114, 182, 0.3);
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --dark-1: #06060f;
        --dark-2: #0a0a1a;
        --dark-3: #12122a;
        --card-bg: rgba(18, 18, 42, 0.65);
        --card-border: rgba(139, 92, 246, 0.15);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
    }

    /* ============== BASE ============== */
    .main { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    html, body, [data-testid="stAppViewContainer"] { scroll-behavior: smooth; }

    /* ============== ANIMATED BACKGROUND ============== */
    .stApp {
        background: var(--dark-1);
        background-image:
            radial-gradient(ellipse 80% 60% at 50% -20%, rgba(139,92,246,0.15), transparent),
            radial-gradient(ellipse 60% 50% at 80% 50%, rgba(6,182,212,0.08), transparent),
            radial-gradient(ellipse 60% 50% at 20% 80%, rgba(244,114,182,0.06), transparent);
        background-attachment: fixed;
    }

    /* Safe dot-grid overlay via container background instead of pseudo-elements */
    [data-testid="stAppViewContainer"] {
        background-image: radial-gradient(rgba(139,92,246,0.08) 1px, transparent 1px);
        background-size: 32px 32px;
        animation: dotDrift 20s linear infinite;
    }

    @keyframes dotDrift {
        from { background-position: 0 0; }
        to { background-position: 32px 32px; }
    }

    /* Hide Streamlit defaults safely */
    [data-testid="stHeader"], footer { visibility: hidden !important; }

    /* ============== GLOBAL ENTRANCE ANIMATION ============== */
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translate3d(0, 24px, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }

    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translate3d(-16px, 0, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }

    /* ============== HERO SECTION ============== */
    .hero-container {
        text-align: center;
        padding: 50px 20px 35px;
        margin-bottom: 10px;
        position: relative;
        animation: fadeSlideUp 0.8s ease-out both;
    }

    .hero-icon {
        font-size: 4.5rem;
        margin-bottom: 18px;
        display: inline-block;
        animation: heroFloat 4s ease-in-out infinite;
        filter: drop-shadow(0 0 25px var(--primary-glow));
        position: relative;
    }

    /* Neon ring behind hero icon */
    .hero-icon::after {
        content: '';
        position: absolute;
        top: 50%; left: 50%;
        width: 90px; height: 90px;
        transform: translate(-50%, -50%);
        border-radius: 50%;
        border: 2px solid rgba(139,92,246,0.2);
        animation: neonRing 3s ease-in-out infinite alternate;
    }

    @keyframes neonRing {
        0% {
            box-shadow: 0 0 5px rgba(139, 92, 246, 0.2), 0 0 20px rgba(139, 92, 246, 0.05);
            transform: translate(-50%, -50%) scale(1);
        }
        100% {
            box-shadow: 0 0 15px rgba(139, 92, 246, 0.4), 0 0 40px rgba(6, 182, 212, 0.1);
            transform: translate(-50%, -50%) scale(1.12);
        }
    }

    @keyframes heroFloat {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-14px) scale(1.06); }
    }

    .hero-title {
        font-size: 3.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 40%, #f472b6 70%, #8b5cf6 100%);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientText 5s ease infinite;
        margin-bottom: 14px;
        letter-spacing: -1.5px;
        line-height: 1.1;
        position: relative;
    }

    @keyframes gradientText {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    /* Shimmer overlay on title */
    .hero-title::after {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 60%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent);
        animation: shimmer 4s ease-in-out infinite;
    }

    @keyframes shimmer {
        0% { left: -60%; }
        100% { left: 160%; }
    }

    .hero-subtitle {
        color: var(--text-secondary);
        font-size: 1.05rem;
        font-weight: 400;
        letter-spacing: 3px;
        text-transform: uppercase;
        animation: fadeSlideUp 1s ease-out 0.3s both;
    }

    .hero-badge {
        display: inline-block;
        margin-top: 18px;
        padding: 6px 18px;
        border-radius: 50px;
        background: rgba(139,92,246,0.1);
        border: 1px solid rgba(139,92,246,0.25);
        color: var(--primary);
        font-size: 0.8rem;
        font-weight: 500;
        letter-spacing: 1px;
        animation: fadeSlideUp 1s ease-out 0.5s both;
    }

    /* ============== GLASSMORPHISM CARDS ============== */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid var(--card-border);
        border-radius: 20px;
        padding: 28px;
        box-shadow:
            0 8px 32px rgba(0,0,0,0.4),
            0 0 0 1px rgba(255,255,255,0.03) inset;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: fadeSlideUp 0.6s ease-out both;
    }

    /* Animated gradient top border */
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--primary), var(--secondary), var(--accent), transparent);
        background-size: 200% 100%;
        animation: borderFlow 3s linear infinite;
    }

    @keyframes borderFlow {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(139,92,246,0.3);
        box-shadow:
            0 20px 40px rgba(0,0,0,0.4),
            0 0 30px rgba(139,92,246,0.08);
    }

    /* ============== REDESIGNED UPLOAD DROPZONE ============== */
    [data-testid="stFileUploader"] {
        background: rgba(14, 14, 34, 0.6) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 2px dashed rgba(139, 92, 246, 0.4) !important;
        border-radius: 20px !important;
        padding: 24px !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: rgba(139, 92, 246, 0.8) !important;
        box-shadow: 0 0 35px rgba(139, 92, 246, 0.22), 0 12px 35px rgba(0, 0, 0, 0.45) !important;
        transform: translateY(-2px) !important;
    }

    [data-testid="stFileUploader"] section {
        background: transparent !important;
        padding: 8px 0 !important;
    }

    [data-testid="stFileUploader"] section > div {
        color: var(--text-secondary) !important;
    }

    /* ============== UNIVERSAL TRANSLUCENT BUTTON SYSTEM ============== */
    /* Base styling for all buttons across the application */
    button,
    div.stButton > button,
    [data-testid="stFileUploader"] button,
    div.stDownloadButton > button {
        background: rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(14px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(14px) saturate(180%) !important;
        border: 1px solid rgba(139, 92, 246, 0.32) !important;
        color: #f1f5f9 !important;
        border-radius: 14px !important;
        padding: 10px 24px !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.4px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    /* Universal Shimmer Reflection Sweep on Hover */
    button::before,
    div.stButton > button::before,
    [data-testid="stFileUploader"] button::before,
    div.stDownloadButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: -50% !important;
        left: -50% !important;
        width: 200% !important;
        height: 200% !important;
        background: linear-gradient(45deg, transparent 40%, rgba(255, 255, 255, 0.12) 50%, transparent 60%) !important;
        transform: translateX(-100%) !important;
        transition: transform 0.65s ease !important;
        pointer-events: none !important;
    }

    button:hover::before,
    div.stButton > button:hover::before,
    [data-testid="stFileUploader"] button:hover::before,
    div.stDownloadButton > button:hover::before {
        transform: translateX(100%) !important;
    }

    /* Universal Hover State */
    button:hover,
    div.stButton > button:hover,
    [data-testid="stFileUploader"] button:hover,
    div.stDownloadButton > button:hover {
        background: rgba(139, 92, 246, 0.22) !important;
        border-color: rgba(139, 92, 246, 0.65) !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 0 25px rgba(139, 92, 246, 0.28), 0 8px 24px rgba(0, 0, 0, 0.35),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }

    /* Universal Active / Click State */
    button:active,
    div.stButton > button:active,
    [data-testid="stFileUploader"] button:active,
    div.stDownloadButton > button:active {
        transform: translateY(1px) scale(0.98) !important;
        background: rgba(139, 92, 246, 0.35) !important;
        box-shadow: 0 2px 10px rgba(139, 92, 246, 0.2) !important;
    }

    /* Primary Translucent Glowing Neon Glass Button */
    div.stButton > button[kind="primary"],
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.38), rgba(6, 182, 212, 0.28)) !important;
        backdrop-filter: blur(16px) saturate(190%) !important;
        -webkit-backdrop-filter: blur(16px) saturate(190%) !important;
        border: 1px solid rgba(139, 92, 246, 0.6) !important;
        color: #ffffff !important;
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.35), 0 6px 20px rgba(0, 0, 0, 0.3),
                    inset 0 1px 1px rgba(255, 255, 255, 0.25) !important;
    }

    div.stButton > button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.55), rgba(6, 182, 212, 0.42)) !important;
        border-color: rgba(139, 92, 246, 0.9) !important;
        box-shadow: 0 0 40px rgba(139, 92, 246, 0.5), 0 10px 30px rgba(0, 0, 0, 0.4),
                    inset 0 1px 1px rgba(255, 255, 255, 0.4) !important;
        transform: translateY(-2px) !important;
    }

    /* Secondary Frosted Glass Button */
    div.stButton > button[kind="secondary"],
    button[data-testid="baseButton-secondary"] {
        background: rgba(18, 18, 42, 0.5) !important;
        backdrop-filter: blur(14px) saturate(160%) !important;
        -webkit-backdrop-filter: blur(14px) saturate(160%) !important;
        border: 1px solid rgba(139, 92, 246, 0.28) !important;
        color: #e2e8f0 !important;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.1) !important;
    }

    div.stButton > button[kind="secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover {
        background: rgba(139, 92, 246, 0.22) !important;
        border-color: rgba(139, 92, 246, 0.65) !important;
        color: #ffffff !important;
        box-shadow: 0 0 25px rgba(139, 92, 246, 0.25), 0 8px 24px rgba(0, 0, 0, 0.35),
                    inset 0 1px 1px rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px) !important;
    }

    /* ============== FLOATING DOCK PILL TABS ============== */
    [data-testid="stTabs"] {
        margin-top: 24px;
        margin-bottom: 28px;
    }

    div[data-baseweb="tab-list"] {
        background: rgba(10, 10, 26, 0.65) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(139, 92, 246, 0.22) !important;
        border-radius: 20px !important;
        padding: 6px 8px !important;
        gap: 8px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
    }

    button[data-baseweb="tab"] {
        border-radius: 14px !important;
        padding: 10px 22px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.3px !important;
        border: 1px solid transparent !important;
        background: transparent !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #f1f5f9 !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(139, 92, 246, 0.25) !important;
        transform: translateY(-1px) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.35), rgba(6, 182, 212, 0.22)) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(139, 92, 246, 0.5) !important;
        box-shadow: 0 0 25px rgba(139, 92, 246, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.2) !important;
    }

    div[data-baseweb="tab-highlight"],
    div[data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ============== METRIC CARDS ============== */
    .metric-card {
        background: linear-gradient(145deg, rgba(18,18,42,0.8), rgba(30,27,75,0.4));
        border: 1px solid rgba(139,92,246,0.18);
        border-radius: 20px;
        padding: 26px 20px;
        text-align: center;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    /* Staggered entrance for metric cards */
    .stColumn:nth-child(1) .metric-card { animation: fadeSlideUp 0.5s ease-out 0.1s both; }
    .stColumn:nth-child(2) .metric-card { animation: fadeSlideUp 0.5s ease-out 0.2s both; }
    .stColumn:nth-child(3) .metric-card { animation: fadeSlideUp 0.5s ease-out 0.3s both; }
    .stColumn:nth-child(4) .metric-card { animation: fadeSlideUp 0.5s ease-out 0.4s both; }

    /* Animated top-glow on metric cards */
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--primary), var(--secondary), transparent);
        background-size: 200% 100%;
        opacity: 0;
        transition: opacity 0.3s ease;
        animation: borderFlow 3s linear infinite;
    }

    .metric-card:hover::before { opacity: 1; }

    .metric-card::after {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(139,92,246,0.06) 0%, transparent 60%);
        opacity: 0;
        transition: opacity 0.4s ease;
        pointer-events: none;
    }

    .metric-card:hover::after { opacity: 1; }

    .metric-card:hover {
        transform: translateY(-6px) scale(1.02);
        border-color: rgba(139,92,246,0.35);
        box-shadow: 0 18px 40px rgba(139,92,246,0.12), 0 0 20px rgba(139,92,246,0.05);
    }

    .metric-icon {
        font-size: 1.6rem;
        margin-bottom: 8px;
        display: block;
        transition: transform 0.3s ease;
    }

    .metric-card:hover .metric-icon { transform: scale(1.2); }

    .metric-value {
        font-size: 2.6rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        background: linear-gradient(135deg, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }

    .metric-label {
        color: var(--text-secondary);
        font-size: 0.82rem;
        margin-top: 6px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }

    /* ============== SKILL BADGES ============== */
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(6,182,212,0.12));
        border: 1px solid rgba(139,92,246,0.25);
        color: #e2e8f0;
        padding: 7px 16px;
        border-radius: 50px;
        margin: 4px;
        font-size: 0.82rem;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: default;
        position: relative;
        overflow: hidden;
        animation: fadeSlideUp 0.4s ease-out both;
    }

    /* Holographic shimmer sweep */
    .skill-badge::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.1) 50%, transparent 60%);
        transform: translateX(-100%);
        transition: transform 0.6s ease;
    }

    .skill-badge:hover::before { transform: translateX(100%); }

    .skill-badge:hover {
        background: linear-gradient(135deg, rgba(139,92,246,0.4), rgba(6,182,212,0.25));
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 20px rgba(139,92,246,0.25);
        border-color: rgba(139,92,246,0.5);
    }

    /* ============== FEEDBACK ITEMS ============== */
    .feedback-item {
        padding: 14px 18px;
        border-radius: 14px;
        margin: 8px 0;
        font-size: 0.92rem;
        line-height: 1.5;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeSlideIn 0.4s ease-out both;
    }

    .feedback-item:hover {
        transform: translateX(6px);
        box-shadow: 4px 0 15px rgba(0,0,0,0.1);
    }

    .feedback-positive {
        background: rgba(16, 185, 129, 0.08);
        border-left: 3px solid #10b981;
        color: #6ee7b7;
    }

    .feedback-warning {
        background: rgba(245, 158, 11, 0.08);
        border-left: 3px solid #f59e0b;
        color: #fcd34d;
    }

    .feedback-negative {
        background: rgba(239, 68, 68, 0.08);
        border-left: 3px solid #ef4444;
        color: #fca5a5;
    }

    /* ============== ANALYSIS CARD ============== */
    .analysis-card {
        background: rgba(18,18,42,0.5);
        border: 1px solid rgba(139,92,246,0.12);
        border-radius: 18px;
        padding: 22px 24px;
        margin: 12px 0;
        transition: all 0.3s ease;
        animation: fadeSlideUp 0.5s ease-out both;
    }

    .analysis-card:hover {
        border-color: rgba(139,92,246,0.25);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }

    .analysis-card-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* ============== CONTACT INFO GRID ============== */
    .contact-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
    }

    .contact-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 14px;
        background: rgba(139,92,246,0.06);
        border-radius: 12px;
        border: 1px solid rgba(139,92,246,0.1);
        transition: all 0.3s ease;
    }

    .contact-item:hover {
        border-color: rgba(139,92,246,0.25);
        transform: translateY(-2px);
    }

    .contact-icon { font-size: 1.1rem; }
    .contact-label { color: var(--text-muted); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px; }
    .contact-value { color: var(--text-primary); font-size: 0.85rem; font-weight: 500; }

    /* ============== SECTION CHECKLIST ============== */
    .checklist-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 0;
        border-bottom: 1px solid rgba(139,92,246,0.06);
        animation: fadeSlideIn 0.3s ease-out both;
    }

    .checklist-item:last-child { border-bottom: none; }

    .check-found { color: #10b981; font-size: 1.1rem; }
    .check-missing { color: #ef4444; font-size: 1.1rem; }
    .checklist-label { color: var(--text-secondary); font-size: 0.88rem; font-weight: 500; }

    /* ============== STAT BAR ============== */
    .stat-bar-container {
        margin: 10px 0;
    }

    .stat-bar-label {
        display: flex;
        justify-content: space-between;
        color: var(--text-secondary);
        font-size: 0.82rem;
        margin-bottom: 6px;
    }

    .stat-bar-track {
        width: 100%;
        height: 8px;
        background: rgba(139,92,246,0.08);
        border-radius: 10px;
        overflow: hidden;
    }

    .stat-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }

    .stat-bar-fill::after {
        content: '';
        position: absolute;
        top: 0; right: 0; bottom: 0; left: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
        animation: shimmer 2s ease-in-out infinite;
    }

    /* ============== SIDEBAR ============== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10,10,26,0.97), rgba(18,18,42,0.97));
        border-right: 1px solid rgba(139,92,246,0.1);
    }

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stCheckbox label {
        color: #e2e8f0 !important;
    }

    .sidebar-title {
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }

    .sidebar-tech-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        background: rgba(139,92,246,0.1);
        border: 1px solid rgba(139,92,246,0.15);
        color: var(--text-secondary);
        font-size: 0.72rem;
        margin: 3px 2px;
        transition: all 0.3s ease;
    }

    .sidebar-tech-badge:hover {
        background: rgba(139,92,246,0.2);
        border-color: rgba(139,92,246,0.3);
    }

    /* ============== TABS ============== */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(18,18,42,0.6);
        border-radius: 14px;
        padding: 5px;
        gap: 4px;
        border: 1px solid rgba(139,92,246,0.1);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: var(--text-secondary);
        font-weight: 500;
        font-size: 0.9rem;
        padding: 10px 16px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-primary);
        background: rgba(139,92,246,0.06);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(139,92,246,0.25), rgba(6,182,212,0.15)) !important;
        color: #f1f5f9 !important;
        box-shadow: 0 2px 12px rgba(139,92,246,0.15);
    }

    /* Tab content fade-in */
    .stTabs [data-baseweb="tab-panel"] {
        animation: fadeSlideUp 0.4s ease-out both;
    }

    /* ============== MESSAGES ============== */
    .stSuccess {
        background: rgba(16, 185, 129, 0.08) !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-radius: 14px !important;
        animation: fadeSlideUp 0.5s ease-out both;
    }

    .stWarning {
        background: rgba(245, 158, 11, 0.08) !important;
        border: 1px solid rgba(245, 158, 11, 0.2) !important;
        border-radius: 14px !important;
    }

    .stError {
        background: rgba(239, 68, 68, 0.08) !important;
        border: 1px solid rgba(239, 68, 68, 0.2) !important;
        border-radius: 14px !important;
    }

    .stInfo {
        background: rgba(6, 182, 212, 0.08) !important;
        border: 1px solid rgba(6, 182, 212, 0.2) !important;
        border-radius: 14px !important;
    }

    /* ============== EXPANDER ============== */
    .streamlit-expanderHeader {
        background: rgba(18,18,42,0.5) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(139,92,246,0.08) !important;
        transition: all 0.3s ease !important;
    }

    .streamlit-expanderHeader:hover {
        border-color: rgba(139,92,246,0.2) !important;
    }

    /* ============== PROGRESS BAR ============== */
    .stProgress > div > div {
        background: linear-gradient(90deg, #8b5cf6, #06b6d4, #f472b6, #8b5cf6) !important;
        background-size: 300% 100% !important;
        animation: progressShimmer 2s ease infinite !important;
        border-radius: 10px !important;
    }

    @keyframes progressShimmer {
        0% { background-position: 300% 0; }
        100% { background-position: -300% 0; }
    }

    /* ============== SECTION HEADERS ============== */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 24px 0 16px 0;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(139,92,246,0.15);
        position: relative;
    }

    .section-header::after {
        content: '';
        position: absolute;
        bottom: -1px; left: 0;
        width: 60px; height: 2px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        border-radius: 2px;
    }

    /* ============== CATEGORY TITLE ============== */
    .category-title {
        color: var(--primary);
        font-weight: 600;
        font-size: 0.88rem;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }

    /* ============== GRADE & VERDICT ============== */
    .grade-box {
        padding: 18px 24px;
        background: rgba(139,92,246,0.06);
        border: 1px solid rgba(139,92,246,0.15);
        border-radius: 16px;
        margin-top: 16px;
        animation: fadeSlideUp 0.5s ease-out both;
    }

    .grade-box strong { color: var(--text-primary); }

    .verdict-card {
        padding: 24px;
        background: rgba(18,18,42,0.5);
        border: 1px solid rgba(139,92,246,0.12);
        border-radius: 18px;
        text-align: center;
        margin: 10px 0;
        animation: fadeSlideUp 0.5s ease-out both;
    }

    .best-match-card {
        text-align: center;
        padding: 24px;
        background: linear-gradient(135deg, rgba(139,92,246,0.08), rgba(6,182,212,0.05));
        border: 1px solid rgba(139,92,246,0.15);
        border-radius: 18px;
        margin-top: 20px;
        animation: fadeSlideUp 0.5s ease-out both;
    }

    /* ============== IMPROVEMENT SUGGESTIONS ============== */
    .suggestion-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 14px 16px;
        background: rgba(139,92,246,0.04);
        border: 1px solid rgba(139,92,246,0.1);
        border-radius: 14px;
        margin: 8px 0;
        transition: all 0.3s ease;
        animation: fadeSlideIn 0.4s ease-out both;
    }

    .suggestion-item:hover {
        border-color: rgba(139,92,246,0.25);
        transform: translateX(4px);
        box-shadow: 4px 0 15px rgba(139,92,246,0.05);
    }

    .suggestion-number {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        width: 26px; height: 26px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
        flex-shrink: 0;
    }

    .suggestion-text {
        color: var(--text-secondary);
        font-size: 0.88rem;
        line-height: 1.5;
    }

    /* ============== EXPERIENCE TIMELINE ============== */
    .exp-timeline {
        border-left: 2px solid rgba(139,92,246,0.2);
        padding-left: 20px;
        margin: 10px 0;
    }

    .exp-item {
        position: relative;
        padding: 8px 0;
        animation: fadeSlideIn 0.4s ease-out both;
    }

    .exp-item::before {
        content: '';
        position: absolute;
        left: -25px; top: 14px;
        width: 8px; height: 8px;
        border-radius: 50%;
        background: var(--primary);
        box-shadow: 0 0 8px var(--primary-glow);
    }

    .exp-years { color: var(--primary); font-family: 'JetBrains Mono', monospace; font-weight: 600; font-size: 0.9rem; }
    .exp-range { color: var(--text-muted); font-size: 0.78rem; }

    /* ============== FOOTER ============== */
    .app-footer {
        text-align: center;
        padding: 30px 20px;
        margin-top: 40px;
        border-top: 1px solid rgba(139,92,246,0.08);
        animation: fadeSlideUp 0.6s ease-out both;
    }

    .app-footer p {
        color: var(--text-muted);
        font-size: 0.78rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    /* ============== PULSE INDICATOR ============== */
    .pulse {
        display: inline-block;
        width: 8px; height: 8px;
        background: #10b981;
        border-radius: 50%;
        animation: pulse 2s infinite;
        margin-right: 8px;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); }
        70% { box-shadow: 0 0 0 10px rgba(16,185,129,0); }
        100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); }
    }

    /* ============== DIVIDER ============== */
    .styled-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139,92,246,0.2), transparent);
        margin: 20px 0;
        border: none;
    }

    /* ============== MULTI-FIELD DEMO PROFILES ============== */
    .demo-selector-wrapper {
        background: linear-gradient(135deg, rgba(18,18,42,0.85), rgba(30,27,75,0.6));
        border: 1px solid rgba(139,92,246,0.3);
        border-radius: 20px;
        padding: 24px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35), 0 0 25px rgba(139,92,246,0.1);
        animation: fadeSlideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
    }

    .demo-selector-header {
        text-align: center;
        margin-bottom: 20px;
    }

    .demo-selector-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #f1f5f9;
        letter-spacing: -0.3px;
        margin-bottom: 6px;
    }

    .demo-selector-subtitle {
        font-size: 0.85rem;
        color: #94a3b8;
    }

    .demo-card {
        background: rgba(14, 14, 34, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 18px;
        padding: 22px;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
    }

    .demo-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.55);
    }

    .demo-card.cybersecurity:hover {
        border-color: rgba(239, 68, 68, 0.6);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.55), 0 0 30px rgba(239, 68, 68, 0.25);
    }

    .demo-card.web_dev:hover {
        border-color: rgba(6, 182, 212, 0.6);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.55), 0 0 30px rgba(6, 182, 212, 0.25);
    }

    .demo-card.data_science:hover {
        border-color: rgba(139, 92, 246, 0.6);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.55), 0 0 30px rgba(139, 92, 246, 0.25);
    }

    .demo-card-top {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }

    .demo-card-icon {
        font-size: 2rem;
        line-height: 1;
    }

    .demo-card-field {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }

    .demo-card-name {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 2px 0;
    }

    .demo-card-role {
        font-size: 0.8rem;
        color: #94a3b8;
        line-height: 1.3;
        margin-bottom: 14px;
    }

    .demo-tags-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 16px;
    }

    .demo-tag {
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 8px;
        background: rgba(139, 92, 246, 0.12);
        color: #e2e8f0;
        border: 1px solid rgba(139, 92, 246, 0.25);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .demo-tag:hover {
        background: rgba(139, 92, 246, 0.22);
        border-color: rgba(139, 92, 246, 0.45);
        color: #ffffff;
    }

    /* ============== SIDEBAR STYLING ============== */
    .sidebar-title {
        color: #f1f5f9;
        font-weight: 700;
        font-size: 0.92rem;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin: 16px 0 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .sidebar-tech-badge {
        display: inline-block;
        background: rgba(139, 92, 246, 0.15);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        color: #cbd5e1;
        padding: 5px 12px;
        border-radius: 50px;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 3px 2px;
        transition: all 0.25s ease;
    }

    .sidebar-tech-badge:hover {
        background: rgba(139, 92, 246, 0.3);
        border-color: rgba(139, 92, 246, 0.6);
        color: #ffffff;
        transform: translateY(-1px);
    }

    .demo-active-banner {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(6, 182, 212, 0.1));
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-radius: 14px;
        padding: 14px 20px;
        margin: 18px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        animation: fadeSlideUp 0.5s ease-out both;
    }

    .demo-active-info {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .demo-active-text {
        font-size: 0.95rem;
        color: #f1f5f9;
    }

    .demo-switch-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 6px;
    }

    /* ============== JOB DESCRIPTION DIRECT MATCHING ============== */
    .jd-card {
        background: linear-gradient(135deg, rgba(20, 20, 48, 0.9), rgba(30, 27, 75, 0.7));
        border: 1px solid rgba(139, 92, 246, 0.35);
        border-radius: 16px;
        padding: 20px 24px;
        margin: 16px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .jd-role-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 6px;
    }

    .skill-badge-req-match {
        display: inline-block;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.45);
        color: #6ee7b7;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 3px 4px;
    }

    .skill-badge-req-miss {
        display: inline-block;
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.45);
        color: #fcd34d;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 3px 4px;
    }

    .skill-badge-pref-match {
        display: inline-block;
        background: rgba(6, 182, 212, 0.15);
        border: 1px solid rgba(6, 182, 212, 0.45);
        color: #67e8f9;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 3px 4px;
    }

    /* ============== PRIORITY PILLS ============== */
    .priority-pill-high {
        background: rgba(239, 68, 68, 0.2);
        border: 1px solid rgba(239, 68, 68, 0.5);
        color: #fca5a5;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-right: 8px;
    }

    .priority-pill-med {
        background: rgba(245, 158, 11, 0.2);
        border: 1px solid rgba(245, 158, 11, 0.5);
        color: #fcd34d;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-right: 8px;
    }

    .priority-pill-low {
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid rgba(16, 185, 129, 0.5);
        color: #6ee7b7;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-right: 8px;
    }

    /* ============== DISCLAIMER BOX ============== */
    .disclaimer-box {
        background: rgba(15, 23, 42, 0.7);
        border-left: 3px solid #8b5cf6;
        border-radius: 0 8px 8px 0;
        padding: 10px 14px;
        margin-top: 14px;
        font-size: 0.78rem;
        color: #94a3b8;
        line-height: 1.4;
    }

    /* ============== RESPONSIVE ============== */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.4rem; }
        .hero-subtitle { font-size: 0.85rem; letter-spacing: 1.5px; }
        .metric-value { font-size: 2rem; }
        .contact-grid { grid-template-columns: 1fr; }
    }
</style>
"""
