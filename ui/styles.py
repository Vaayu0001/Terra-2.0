"""
Terra 2.0 — Global CSS Styles (Light, Warm Theme)
Warm beige/earth-tone light theme with forest green accents.
Includes modern cards, smooth transitions, and accessibility features.
"""


def get_global_css() -> str:
    """Return the complete CSS string for Terra 2.0 with warm light theme."""
    return """
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

    :root {
        --bg-primary: #FAF7F2;
        --bg-secondary: #F2EDE4;
        --bg-card: #FFFFFF;
        --accent-green: #3D7A5E;
        --accent-light: #6BAF8A;
        --accent-warm: #C8794A;
        --accent-gold: #D4A853;
        --text-primary: #2C2C2C;
        --text-secondary: #5C5C5C;
        --text-muted: #9A9A9A;
        --border: #E8E0D5;
        --shadow: rgba(60, 40, 20, 0.08);
    }

    /* ═══════ Hide Streamlit Default Chrome ═══════ */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* ═══════ Root Background ═══════ */
    .stApp {
        background-color: var(--bg-primary) !important;
        font-family: 'Inter', 'Plus Jakarta Sans', sans-serif !important;
    }

    /* ═══════ Main Content Area ═══════ */
    .main, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-primary) !important;
    }

    /* ═══════ Cards Base Style ═══════ */
    .terra-card {
        background: var(--bg-card) !important;
        border-radius: 16px !important;
        border: 1px solid var(--border) !important;
        box-shadow: 0 2px 12px var(--shadow) !important;
        padding: 24px !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    .terra-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px var(--shadow) !important;
    }

    /* ═══════ Cards with Glow ═══════ */
    .terra-card-glow {
        background: var(--bg-card) !important;
        border-radius: 16px !important;
        border: 1.5px solid var(--accent-green) !important;
        box-shadow: 0 4px 20px rgba(61, 122, 94, 0.12) !important;
        padding: 24px !important;
        transition: all 0.3s ease !important;
    }
    .terra-card-glow:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 32px rgba(61, 122, 94, 0.2) !important;
    }

    /* ═══════ Sidebar ═══════ */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border) !important;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary) !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        color: var(--accent-green) !important;
    }

    /* ═══════ Buttons ═══════ */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-green), var(--accent-light)) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(61, 122, 94, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(61, 122, 94, 0.4) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ═══════ Primary Button Variant ═══════ */
    .btn-primary {
        background: linear-gradient(135deg, var(--accent-green), var(--accent-light)) !important;
        color: white !important;
    }

    /* ═══════ Secondary Button Variant ═══════ */
    .btn-secondary {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1.5px solid var(--border) !important;
    }

    /* ═══════ Warning/Danger Buttons ═══════ */
    .btn-danger {
        background: linear-gradient(135deg, #E74C3C, #C0392B) !important;
        color: white !important;
    }

    /* ═══════ Input Fields ═══════ */
    .stTextInput > div > div > input,
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input,
    .stNumberInput > div > div > input:focus {
        background: var(--bg-primary) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--accent-green) !important;
        box-shadow: 0 0 0 3px rgba(61, 122, 94, 0.12) !important;
    }

    .stTextArea textarea {
        background: var(--bg-primary) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
    }
    .stTextArea textarea:focus {
        border-color: var(--accent-green) !important;
        box-shadow: 0 0 0 3px rgba(61, 122, 94, 0.12) !important;
    }

    /* ═══════ Select/Dropdown ═══════ */
    .stSelectbox > div > div {
        background: var(--bg-primary) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        transition: all 0.2s ease !important;
    }
    
    /* Target all nested text in selectbox */
    .stSelectbox > div > div > div {
        color: var(--text-primary) !important;
    }
    
    .stSelectbox > div > div > div > div {
        color: var(--text-primary) !important;
    }
    
    .stSelectbox > div > div > div span {
        color: var(--text-primary) !important;
    }
    
    .stSelectbox > div > div > div > div span {
        color: var(--text-primary) !important;
    }
    
    .stSelectbox input {
        color: var(--text-primary) !important;
    }
    
    .stSelectbox input::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Hover state - dark background with white text */
    .stSelectbox > div > div:hover {
        background: var(--accent-green) !important;
        color: white !important;
    }
    
    .stSelectbox > div > div:hover > div {
        color: white !important;
    }
    
    .stSelectbox > div > div:hover div {
        color: white !important;
    }
    
    .stSelectbox > div > div:hover span {
        color: white !important;
    }
    
    .stSelectbox > div > div:focus {
        border-color: var(--accent-green) !important;
        background: var(--accent-green) !important;
        color: white !important;
    }
    
    .stSelectbox > div > div:focus > div,
    .stSelectbox > div > div:focus div,
    .stSelectbox > div > div:focus span {
        color: white !important;
    }
    
    /* Handle open/expanded state */
    .stSelectbox [role="listbox"] {
        background: var(--bg-primary) !important;
    }
    
    .stSelectbox [role="listbox"] * {
        color: var(--text-primary) !important;
    }
    
    .stSelectbox [role="option"] {
        color: var(--text-primary) !important;
    }
    
    .stSelectbox [role="option"]:hover {
        color: white !important;
        background: var(--accent-green) !important;
    }

    /* ═══════ Checkbox & Radio ═══════ */
    .stCheckbox label, .stRadio label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    .stCheckbox label:hover, .stRadio label:hover {
        color: var(--text-primary) !important;
    }
    
    /* ═══════ Form Labels ═══════ */
    label {
        color: var(--text-primary) !important;
    }
    .stTextInput label, .stNumberInput label, .stTextArea label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }

    /* ═══════ Slider ═══════ */
    .stSlider label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }

    /* ═══════ Progress Bar ═══════ */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--accent-green), var(--accent-light)) !important;
        border-radius: 999px !important;
    }
    .stProgress > div {
        background: var(--bg-secondary) !important;
        border-radius: 999px !important;
    }

    /* ═══════ Metrics ═══════ */
    [data-testid="stMetric"] {
        background: var(--bg-card) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        border: 1px solid var(--border) !important;
    }
    [data-testid="stMetric"] label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--accent-green) !important;
    }

    /* ═══════ Tabs ═══════ */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
        border-bottom: none !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: var(--text-secondary);
        font-weight: 500;
        padding: 8px 16px !important;
    }
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: var(--accent-green) !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 4px var(--shadow) !important;
    }

    /* ═══════ Expander ═══════ */
    .streamlit-expanderHeader {
        background: var(--bg-secondary) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
    }

    /* ═══════ Alerts & Messages ═══════ */
    .stAlert {
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
    }

    /* ═══════ Error Alert ═══════ */
    [data-testid="stAlert"] {
        background: #FEF3F2 !important;
        border: 1px solid #FECBCB !important;
        border-radius: 12px !important;
        color: #B42318 !important;
    }

    /* ═══════ Success Alert ═══════ */
    .element-container [data-testid="stAlert"] {
        background: #F0FDF4 !important;
        border: 1px solid #DCFCE7 !important;
        color: #166534 !important;
    }

    /* ═══════ Info Alert ═══════ */
    .stInfo {
        background: #F0F9FF !important;
        border: 1px solid #BFDBFE !important;
        color: #0C4A6E !important;
    }

    /* ═══════ Loading Spinner ═══════ */
    .terra-loader {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 20px;
        color: var(--text-secondary);
        font-size: 15px;
        font-weight: 500;
    }
    .terra-loader::before {
        content: '';
        width: 20px;
        height: 20px;
        border: 2.5px solid var(--border);
        border-top-color: var(--accent-green);
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
        flex-shrink: 0;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* ═══════ Badge Pills ═══════ */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #EEF7F2;
        color: var(--accent-green);
        border: 1px solid #C8E6D5;
        border-radius: 999px;
        padding: 6px 14px;
        font-size: 13px;
        font-weight: 600;
    }

    /* ═══════ Badge Variants ═══════ */
    .badge-warm {
        background: #FDF3E8;
        color: var(--accent-warm);
        border-color: #FDDBB0;
    }
    .badge-gold {
        background: #FEF9E7;
        color: var(--accent-gold);
        border-color: #F5D89C;
    }

    /* ═══════ XP Bar ═══════ */
    .xp-bar-container {
        background: var(--bg-secondary);
        border-radius: 999px;
        height: 8px;
        overflow: hidden;
        border: 1px solid var(--border);
    }
    .xp-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--accent-green), var(--accent-light));
        border-radius: 999px;
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ═══════ Score Circle ═══════ */
    .score-circle {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        width: 120px;
        height: 120px;
        background: linear-gradient(135deg, rgba(61, 122, 94, 0.1), rgba(107, 175, 138, 0.1));
        border: 2px solid var(--accent-green);
        border-radius: 50%;
        font-weight: 700;
        font-size: 32px;
        color: var(--accent-green);
    }

    /* ═══════ Navigation Grid Cards ═══════ */
    .nav-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .nav-card:hover {
        border-color: var(--accent-green);
        transform: translateY(-6px);
        box-shadow: 0 12px 32px var(--shadow);
    }

    /* ═══════ Divider ═══════ */
    hr {
        border-color: var(--border) !important;
        margin: 24px 0 !important;
    }

    /* ═══════ Typography ═══════ */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }

    p, span, label, div {
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }

    .stMarkdown {
        color: var(--text-primary);
    }

    /* ═══════ Links ═══════ */
    a {
        color: var(--accent-green) !important;
        text-decoration: none !important;
        font-weight: 600 !important;
    }
    a:hover {
        color: var(--accent-light) !important;
    }

    /* ═══════ Scrollbar ═══════ */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-green);
    }

    /* ═══════ Code Blocks ═══════ */
    pre, code {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
        border: 1px solid var(--border) !important;
    }

    /* ═══════ Animations ═══════ */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.4s ease forwards;
    }

    @keyframes slideInFromLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .slide-in-left {
        animation: slideInFromLeft 0.3s ease forwards;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    .pulse {
        animation: pulse 2s ease infinite;
    }

    /* ═══════ Responsive ═══════ */
    @media (max-width: 768px) {
        .terra-card {
            padding: 16px !important;
        }
        .stButton > button {
            padding: 10px 20px !important;
            font-size: 14px !important;
        }
    }

    /* ═══════ ACCENT COLORS — Streak, Badges, Medals ═══════ */
    
    /* Streak counter — Terracotta accent */
    .streak-badge {
        background: linear-gradient(135deg, var(--accent-warm), #D97A5C) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 8px 16px !important;
        font-weight: 700 !important;
        display: inline-block !important;
        box-shadow: 0 4px 12px rgba(200, 121, 74, 0.3) !important;
    }

    /* Level badge — Gold border */
    .level-badge {
        border: 2.5px solid var(--accent-gold) !important;
        background: linear-gradient(135deg, #FFF9E6 0%, #FFFBF0 100%) !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        text-align: center !important;
        box-shadow: 0 4px 16px rgba(212, 168, 83, 0.2) !important;
    }

    .level-badge-text {
        color: var(--accent-gold) !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
    }

    /* Leaderboard medals */
    .medal-gold {
        color: var(--accent-gold) !important;
        font-size: 1.8rem !important;
    }

    .medal-silver {
        color: #B0B0B0 !important;
        font-size: 1.8rem !important;
    }

    .medal-bronze {
        color: var(--accent-warm) !important;
        font-size: 1.8rem !important;
    }

    /* Feature card accent on hover */
    .nav-card {
        border-left: 3px solid transparent !important;
        transition: all 0.3s ease !important;
    }

    .nav-card:hover {
        border-left-color: var(--accent-green) !important;
    }

    /* XP Progress Bar — Green to sage gradient */
    .xp-progress {
        background: linear-gradient(90deg, var(--accent-green) 0%, var(--accent-light) 100%) !important;
        border-radius: 999px !important;
        height: 8px !important;
        transition: width 0.4s ease !important;
    }

    /* Badge item — Gold border accent */
    .badge-item:hover {
        border-color: var(--accent-gold) !important;
        transform: scale(1.05) !important;
        box-shadow: 0 8px 20px rgba(212, 168, 83, 0.25) !important;
    }

    /* Trophy/Leaderboard row accent colors */
    .trophy-first {
        border-left: 4px solid var(--accent-gold) !important;
        background: linear-gradient(90deg, rgba(212, 168, 83, 0.1), transparent) !important;
    }

    .trophy-second {
        border-left: 4px solid #B0B0B0 !important;
        background: linear-gradient(90deg, rgba(176, 176, 176, 0.08), transparent) !important;
    }

    .trophy-third {
        border-left: 4px solid var(--accent-warm) !important;
        background: linear-gradient(90deg, rgba(200, 121, 74, 0.08), transparent) !important;
    }

    /* Eco score rating colors */
    .eco-rating-good {
        color: var(--accent-green) !important;
    }

    .eco-rating-okay {
        color: var(--accent-gold) !important;
    }

    .eco-rating-poor {
        color: var(--accent-warm) !important;
    }
    """


def get_loading_html(message: str = "Loading...") -> str:
    """Return HTML for a loading spinner with message."""
    return f"""
    <div class="terra-loader">{message}</div>
    """


def get_success_toast(message: str) -> str:
    """Return styled success toast HTML."""
    return f"""
    <div style="
        background: #F0FDF4;
        border: 1.5px solid #86EFAC;
        border-radius: 12px;
        padding: 16px 20px;
        color: #15803D;
        font-weight: 500;
        font-size: 15px;
        display: flex;
        align-items: center;
        gap: 12px;
    ">
        <span style="font-size: 20px;">✅</span>
        <span>{message}</span>
    </div>
    """


def get_error_toast(message: str) -> str:
    """Return styled error toast HTML."""
    return f"""
    <div style="
        background: #FEF3F2;
        border: 1.5px solid #FCCAB1;
        border-radius: 12px;
        padding: 16px 20px;
        color: #B42318;
        font-weight: 500;
        font-size: 15px;
        display: flex;
        align-items: center;
        gap: 12px;
    ">
        <span style="font-size: 20px;">❌</span>
        <span>{message}</span>
    </div>
    """
