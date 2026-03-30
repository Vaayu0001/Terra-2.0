"""
Terra 2.0 — Global CSS Styles
Includes Google Fonts, animated mesh background, particles,
glassmorphism cards, custom scrollbar, and all component overrides.
"""


def get_global_css() -> str:
    """Return the complete CSS string for Terra 2.0."""

    # Generate particle CSS for 25 particles
    particle_css_items = []
    for i in range(1, 26):
        left = (i * 4) % 100
        delay = (i * 0.7) % 15
        duration = 12 + (i % 8) * 2
        size = 3 + (i % 6)
        color = "#2ECC71" if i % 2 == 0 else "#7EC8E3"
        opacity = 0.3 + (i % 4) * 0.1

        particle_css_items.append(f"""
        .particle:nth-child({i}) {{
            left: {left}%;
            width: {size}px;
            height: {size}px;
            background: {color};
            animation-delay: {delay:.1f}s;
            animation-duration: {duration}s;
            opacity: {opacity};
        }}""")

    particles_css = "\n".join(particle_css_items)

    return f"""
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=DM+Sans:wght@300;400;500&display=swap');

    :root {{
        --terra-green:   #2ECC71;
        --terra-dark:    #0D1F1A;
        --terra-beige:   #F5F0E8;
        --terra-sky:     #7EC8E3;
        --terra-yellow:  #F4C430;
        --terra-accent:  #FF6B35;
        --terra-muted:   #2D4A3E;
        --terra-card:    rgba(45, 74, 62, 0.55);
    }}

    /* ═══════ Animated Gradient Mesh Background ═══════ */
    @keyframes meshMove {{
        0%, 100% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
    }}

    .stApp {{
        background: linear-gradient(135deg, #0D1F1A 0%, #0a2e20 30%, #0f1a2e 60%, #0D1F1A 100%) !important;
        background-size: 400% 400% !important;
        animation: meshMove 18s ease infinite !important;
    }}

    /* ═══════ Floating Particles ═══════ */
    @keyframes float {{
        0% {{ transform: translateY(100vh); opacity: 0; }}
        10% {{ opacity: 0.6; }}
        90% {{ opacity: 0.3; }}
        100% {{ transform: translateY(-10vh); opacity: 0; }}
    }}

    .particle {{
        position: fixed;
        border-radius: 50%;
        pointer-events: none;
        z-index: 0;
        animation: float linear infinite;
    }}

    {particles_css}

    /* ═══════ Hide Streamlit Chrome ═══════ */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header {{ visibility: hidden; }}
    .stDeployButton {{ display: none; }}

    /* ═══════ Custom Sidebar ═══════ */
    [data-testid="stSidebar"] {{
        background: rgba(13, 31, 26, 0.95) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(46, 204, 113, 0.2) !important;
    }}

    [data-testid="stSidebar"] .stMarkdown {{
        color: #F5F0E8 !important;
    }}

    [data-testid="stSidebar"] .stRadio label {{
        color: #F5F0E8 !important;
    }}

    [data-testid="stSidebar"] .stRadio label:hover {{
        color: #2ECC71 !important;
    }}

    /* ═══════ Button Overrides ═══════ */
    .stButton button {{
        background: linear-gradient(135deg, #2ECC71, #7EC8E3) !important;
        color: #0D1F1A !important;
        font-weight: 600 !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: 0.5px;
    }}

    .stButton button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(46, 204, 113, 0.4) !important;
    }}

    .stButton button:active {{
        transform: translateY(0) !important;
    }}

    /* ═══════ Metric Cards ═══════ */
    [data-testid="metric-container"] {{
        background: rgba(45, 74, 62, 0.5) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(46, 204, 113, 0.2) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
    }}

    [data-testid="metric-container"] label {{
        color: #7EC8E3 !important;
    }}

    [data-testid="metric-container"] [data-testid="stMetricValue"] {{
        color: #F5F0E8 !important;
    }}

    /* ═══════ Progress Bar ═══════ */
    .stProgress > div > div {{
        background: linear-gradient(90deg, #2ECC71, #7EC8E3) !important;
        border-radius: 10px !important;
    }}

    .stProgress > div {{
        background: rgba(45, 74, 62, 0.4) !important;
        border-radius: 10px !important;
    }}

    /* ═══════ Input Fields ═══════ */
    .stTextInput input {{
        background: rgba(45, 74, 62, 0.4) !important;
        border: 1px solid rgba(46, 204, 113, 0.3) !important;
        border-radius: 12px !important;
        color: #F5F0E8 !important;
        font-family: 'DM Sans', sans-serif !important;
    }}

    .stTextInput input:focus {{
        border-color: var(--terra-green) !important;
        box-shadow: 0 0 15px rgba(46, 204, 113, 0.2) !important;
    }}

    .stSelectbox > div > div {{
        background: rgba(45, 74, 62, 0.4) !important;
        border: 1px solid rgba(46, 204, 113, 0.3) !important;
        border-radius: 12px !important;
        color: #F5F0E8 !important;
    }}

    .stNumberInput input {{
        background: rgba(45, 74, 62, 0.4) !important;
        border: 1px solid rgba(46, 204, 113, 0.3) !important;
        border-radius: 12px !important;
        color: #F5F0E8 !important;
    }}

    .stTextArea textarea {{
        background: rgba(45, 74, 62, 0.4) !important;
        border: 1px solid rgba(46, 204, 113, 0.3) !important;
        border-radius: 12px !important;
        color: #F5F0E8 !important;
    }}

    /* ═══════ Radio Buttons ═══════ */
    .stRadio label {{
        color: #F5F0E8 !important;
    }}

    /* ═══════ Checkbox ═══════ */
    .stCheckbox label {{
        color: #F5F0E8 !important;
    }}

    /* ═══════ Slider ═══════ */
    .stSlider label {{
        color: #F5F0E8 !important;
    }}

    /* ═══════ Terra Card (Glassmorphism) ═══════ */
    .terra-card {{
        background: rgba(45, 74, 62, 0.55);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(46, 204, 113, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }}

    .terra-card:hover {{
        border-color: rgba(46, 204, 113, 0.5);
        transform: translateY(-3px);
    }}

    .terra-card-glow {{
        background: rgba(45, 74, 62, 0.55);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(46, 204, 113, 0.4);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),
                    0 0 30px rgba(46, 204, 113, 0.15);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }}

    .terra-card-glow:hover {{
        border-color: rgba(46, 204, 113, 0.7);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),
                    0 0 50px rgba(46, 204, 113, 0.25);
    }}

    /* ═══════ Typography ═══════ */
    h1, h2, h3 {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #F5F0E8 !important;
    }}

    p, span, div, label {{
        font-family: 'DM Sans', sans-serif;
    }}

    .stMarkdown p, .stMarkdown span {{
        color: #F5F0E8;
    }}

    /* ═══════ Custom Scrollbar ═══════ */
    ::-webkit-scrollbar {{
        width: 5px;
    }}

    ::-webkit-scrollbar-track {{
        background: #0D1F1A;
    }}

    ::-webkit-scrollbar-thumb {{
        background: #2ECC71;
        border-radius: 5px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: #27ae60;
    }}

    /* ═══════ Glow Text Animation ═══════ */
    @keyframes glow {{
        0%, 100% {{ text-shadow: 0 0 10px rgba(46, 204, 113, 0.5); }}
        50% {{ text-shadow: 0 0 25px rgba(46, 204, 113, 0.9),
                             0 0 50px rgba(46, 204, 113, 0.4); }}
    }}

    .glow-text {{
        animation: glow 3s ease infinite;
    }}

    /* ═══════ Page Fade In ═══════ */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .main .block-container {{
        animation: fadeIn 0.6s ease forwards;
    }}

    /* ═══════ Tabs Override ═══════ */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}

    .stTabs [data-baseweb="tab"] {{
        background: rgba(45, 74, 62, 0.4) !important;
        border-radius: 12px !important;
        color: #F5F0E8 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        border: 1px solid rgba(46, 204, 113, 0.2) !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: rgba(46, 204, 113, 0.3) !important;
        border-color: rgba(46, 204, 113, 0.6) !important;
    }}

    /* ═══════ Expander ═══════ */
    .streamlit-expanderHeader {{
        background: rgba(45, 74, 62, 0.4) !important;
        border-radius: 12px !important;
        color: #F5F0E8 !important;
    }}

    /* ═══════ Download Button ═══════ */
    .stDownloadButton button {{
        background: linear-gradient(135deg, #F4C430, #FF6B35) !important;
        color: #0D1F1A !important;
        font-weight: 600 !important;
        border-radius: 50px !important;
        border: none !important;
    }}

    .stDownloadButton button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(244, 196, 48, 0.4) !important;
    }}

    /* ═══════ Divider ═══════ */
    hr {{
        border-color: rgba(46, 204, 113, 0.2) !important;
    }}

    /* ═══════ Alert / Warning ═══════ */
    .stAlert {{
        background: rgba(45, 74, 62, 0.5) !important;
        border: 1px solid rgba(46, 204, 113, 0.3) !important;
        border-radius: 12px !important;
        color: #F5F0E8 !important;
    }}

    /* ═══════ Score Circle ═══════ */
    .score-circle {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }}

    /* ═══════ Navigation Grid ═══════ */
    .nav-card {{
        background: rgba(45, 74, 62, 0.45);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(46, 204, 113, 0.15);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }}

    .nav-card:hover {{
        border-color: rgba(46, 204, 113, 0.5);
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
    }}

    /* ═══════ Badge Grid ═══════ */
    .badge-item {{
        background: rgba(45, 74, 62, 0.4);
        border: 1px solid rgba(46, 204, 113, 0.2);
        border-radius: 12px;
        padding: 0.8rem;
        text-align: center;
        transition: all 0.3s ease;
    }}

    .badge-item:hover {{
        transform: scale(1.05);
        border-color: rgba(46, 204, 113, 0.5);
    }}

    /* ═══════ Multiselect ═══════ */
    .stMultiSelect > div {{
        background: rgba(45, 74, 62, 0.4) !important;
        border: 1px solid rgba(46, 204, 113, 0.3) !important;
        border-radius: 12px !important;
    }}

    /* ═══════ Toast Override ═══════ */
    [data-testid="stToast"] {{
        background: rgba(13, 31, 26, 0.95) !important;
        border: 1px solid rgba(46, 204, 113, 0.3) !important;
        border-radius: 12px !important;
        color: #F5F0E8 !important;
    }}

    /* ═══════ Pulse Animation ═══════ */
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}

    .pulse {{
        animation: pulse 2s ease infinite;
    }}
    """
