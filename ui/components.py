"""
Terra 2.0 — Reusable UI Components
Streamlit-based components using st.markdown with HTML/CSS.
"""

import streamlit as st

from config import XP_PER_LEVEL, LEVEL_NAMES


def page_header(title: str, subtitle: str, emoji: str) -> None:
    """Render a styled page header with glow effect."""
    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem 0 1rem 0;">
        <div style="font-size: 3rem; margin-bottom: 0.3rem;">{emoji}</div>
        <h1 class="glow-text" style="
            font-size: 2.2rem;
            font-weight: 700;
            margin: 0;
            background: linear-gradient(135deg, #2ECC71, #7EC8E3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">{title}</h1>
        <p style="
            color: #7EC8E3;
            font-size: 1rem;
            margin-top: 0.3rem;
            opacity: 0.8;
        ">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def terra_card(content_html: str, glow: bool = False) -> str:
    """Return HTML string for a glassmorphism card."""
    card_class = "terra-card-glow" if glow else "terra-card"
    return f'<div class="{card_class}">{content_html}</div>'


def render_terra_card(content_html: str, glow: bool = False) -> None:
    """Render a glassmorphism card directly."""
    st.markdown(terra_card(content_html, glow), unsafe_allow_html=True)


def xp_badge(xp: int, level: int, level_name: str) -> None:
    """Render XP badge with level info."""
    st.markdown(f"""
    <div class="terra-card" style="text-align: center; padding: 1rem;">
        <div style="
            font-size: 1.8rem;
            font-weight: 700;
            color: #F4C430;
            text-shadow: 0 0 15px rgba(244, 196, 48, 0.4);
        ">⭐ Level {level}</div>
        <div style="
            font-size: 1rem;
            color: #2ECC71;
            font-weight: 600;
            margin: 0.3rem 0;
        ">{level_name}</div>
        <div style="
            font-size: 0.85rem;
            color: #7EC8E3;
        ">{xp} XP</div>
    </div>
    """, unsafe_allow_html=True)


def metric_row(metrics: list) -> None:
    """
    Render a row of metric cards.
    metrics = [{"label": str, "value": str, "delta": str, "emoji": str}]
    """
    cols = st.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            delta_html = ""
            if metric.get("delta"):
                delta_color = "#2ECC71" if not metric["delta"].startswith("-") else "#EF4444"
                delta_html = f'<div style="font-size: 0.75rem; color: {delta_color};">{metric["delta"]}</div>'

            st.markdown(f"""
            <div class="terra-card" style="text-align: center; padding: 1rem;">
                <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">{metric.get("emoji", "📊")}</div>
                <div style="
                    font-size: 1.4rem;
                    font-weight: 700;
                    color: #F5F0E8;
                ">{metric.get("value", "0")}</div>
                <div style="
                    font-size: 0.8rem;
                    color: #7EC8E3;
                    margin-top: 0.2rem;
                ">{metric.get("label", "")}</div>
                {delta_html}
            </div>
            """, unsafe_allow_html=True)


def score_circle(score: float, max_score: float,
                 label: str, color: str) -> None:
    """Render CSS animated circular progress indicator using inline SVG."""
    percentage = min((score / max(max_score, 0.01)) * 100, 100)
    circumference = 2 * 3.14159 * 45
    dash_offset = circumference * (1 - percentage / 100)

    st.markdown(f"""
    <div class="score-circle" style="text-align: center; padding: 1rem;">
        <svg width="120" height="120" viewBox="0 0 120 120">
            <!-- Background circle -->
            <circle cx="60" cy="60" r="45"
                fill="none" stroke="rgba(45, 74, 62, 0.6)"
                stroke-width="8"/>
            <!-- Progress circle -->
            <circle cx="60" cy="60" r="45"
                fill="none" stroke="{color}"
                stroke-width="8"
                stroke-linecap="round"
                stroke-dasharray="{circumference}"
                stroke-dashoffset="{dash_offset}"
                transform="rotate(-90 60 60)"
                style="transition: stroke-dashoffset 1s ease;">
                <animate attributeName="stroke-dashoffset"
                    from="{circumference}" to="{dash_offset}"
                    dur="1.5s" fill="freeze"/>
            </circle>
            <!-- Score text -->
            <text x="60" y="55" text-anchor="middle"
                font-size="22" font-weight="700"
                fill="{color}"
                font-family="Plus Jakarta Sans, sans-serif">
                {score:.1f}
            </text>
            <text x="60" y="75" text-anchor="middle"
                font-size="10" fill="#7EC8E3"
                font-family="DM Sans, sans-serif">
                / {max_score:.0f}
            </text>
        </svg>
        <div style="
            font-size: 0.85rem;
            color: #F5F0E8;
            margin-top: 0.3rem;
            font-weight: 500;
        ">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def level_progress_bar(current_xp: int) -> None:
    """Render custom styled progress bar with level info."""
    level = min(current_xp // XP_PER_LEVEL + 1, 30)
    if level >= 30:
        progress = 100
        xp_to_next = 0
        next_name = "MAX"
    else:
        progress = (current_xp % XP_PER_LEVEL) / XP_PER_LEVEL * 100
        xp_to_next = XP_PER_LEVEL - (current_xp % XP_PER_LEVEL)
        next_name = LEVEL_NAMES[level] if level < 30 else "MAX"

    current_name = LEVEL_NAMES[level - 1]

    st.markdown(f"""
    <div style="margin: 0.5rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
            <span style="color: #2ECC71; font-size: 0.8rem; font-weight: 600;">
                Lv.{level} {current_name}
            </span>
            <span style="color: #7EC8E3; font-size: 0.8rem;">
                Lv.{min(level + 1, 30)} {next_name}
            </span>
        </div>
        <div style="
            background: rgba(45, 74, 62, 0.4);
            border-radius: 10px;
            height: 12px;
            overflow: hidden;
            border: 1px solid rgba(46, 204, 113, 0.2);
        ">
            <div style="
                background: linear-gradient(90deg, #2ECC71, #7EC8E3);
                height: 100%;
                width: {progress:.1f}%;
                border-radius: 10px;
                transition: width 0.5s ease;
            "></div>
        </div>
        <div style="text-align: center; margin-top: 0.2rem;">
            <span style="color: #F5F0E8; font-size: 0.75rem;">
                {current_xp} XP • {xp_to_next} XP to next level
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def toast_success(message: str) -> None:
    """Show a success toast notification."""
    st.toast(f"✅ {message}")


def toast_xp(xp_earned: int, action: str = "") -> None:
    """Show XP earned toast."""
    st.toast(f"⭐ +{xp_earned} XP{' — ' + action if action else ''}")


def eco_tip_card(tip: str) -> None:
    """Render a green eco tip card."""
    st.markdown(f"""
    <div class="terra-card" style="
        border-left: 4px solid #2ECC71;
        padding: 1rem 1.2rem;
    ">
        <div style="display: flex; align-items: flex-start; gap: 0.8rem;">
            <span style="font-size: 1.3rem;">💡</span>
            <span style="color: #F5F0E8; font-size: 0.9rem; line-height: 1.5;">
                {tip}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_particles() -> None:
    """Render 25 floating particle divs."""
    particles_html = "".join([f'<div class="particle"></div>' for _ in range(25)])
    st.markdown(f'<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0;">{particles_html}</div>', unsafe_allow_html=True)


def nav_button(emoji: str, label: str, page_key: str) -> bool:
    """Render a navigation card button. Returns True if clicked."""
    return st.button(f"{emoji} {label}", key=f"nav_{page_key}", use_container_width=True)
