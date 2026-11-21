"""
PathFinder — Design System & Styles
Centralized design constants, CSS styling, and UI helper functions.
"""

import streamlit as st
from typing import Optional, Dict, Any

# ---------------------------------------------------------------------------
# COLOR PALETTE
# ---------------------------------------------------------------------------
PRIMARY_PURPLE = "#6957E8"
SECONDARY_PURPLE = "#8B7CF6"
DEEP_NAVY = "#202747"
BG_LIGHT = "#F5F6FC"
CARD_BG = "#FFFFFF"
TEXT_MAIN = "#252C4B"
TEXT_MUTED = "#737D95"
BORDER_COLOR = "#E7EAF3"
COLOR_SUCCESS = "#20A67A"
COLOR_WARNING = "#E9A23B"
COLOR_DANGER = "#E56868"
COLOR_ACCENT = "#36A9D6"

# ---------------------------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

/* Base typography and background */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #252C4B;
}

.stApp {
    background-color: #F5F6FC;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1C223E 0%, #202747 60%, #171C33 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

[data-testid="stSidebar"] * {
    color: #E2E8F6 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 9px 12px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.15s ease-in-out;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255, 255, 255, 0.08);
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"] {
    background: linear-gradient(90deg, rgba(105, 87, 232, 0.35) 0%, rgba(139, 124, 246, 0.2) 100%);
    border-left: 3px solid #8B7CF6;
    color: #FFFFFF !important;
    font-weight: 600;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.12);
    margin: 1.2rem 0;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: #202747 !important;
    font-weight: 750 !important;
    letter-spacing: -0.4px;
}

/* Native Containers & Cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border: 1px solid #E7EAF3 !important;
    border-radius: 14px !important;
    padding: 1.25rem !important;
    box-shadow: 0 4px 16px rgba(32, 39, 71, 0.035) !important;
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #D4D8EC !important;
    box-shadow: 0 6px 20px rgba(32, 39, 71, 0.06) !important;
}

/* Native Metrics */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #E7EAF3 !important;
    padding: 16px 18px !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 10px rgba(32, 39, 71, 0.03) !important;
}

[data-testid="stMetricLabel"] {
    color: #737D95 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

[data-testid="stMetricValue"] {
    color: #202747 !important;
    font-size: 26px !important;
    font-weight: 800 !important;
}

/* Primary and Regular Buttons */
.stButton > button,
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #6957E8 0%, #8B7CF6 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 10px 22px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(105, 87, 232, 0.25) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(135deg, #5946DF 0%, #7A69EE 100%) !important;
    box-shadow: 0 6px 18px rgba(105, 87, 232, 0.35) !important;
    transform: translateY(-1px);
    color: #FFFFFF !important;
}

.stButton > button p,
.stButton > button span,
[data-testid="stFormSubmitButton"] > button p,
[data-testid="stFormSubmitButton"] > button span {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* Form Controls (Inputs, Selects, Multiselects) */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] div[data-baseweb="select"],
[data-testid="stMultiSelect"] div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    color: #252C4B !important;
    border: 1px solid #D9DEEC !important;
    border-radius: 8px !important;
    font-size: 14px !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: #6957E8 !important;
    box-shadow: 0 0 0 2px rgba(105, 87, 232, 0.15) !important;
}

/* Progress Bars */
[data-testid="stProgressBar"] {
    border-radius: 10px;
    height: 8px;
    overflow: hidden;
    background-color: #E8EBF5;
}

[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #6957E8 0%, #36A9D6 100%) !important;
}

/* Checkboxes */
[data-testid="stCheckbox"] label {
    font-weight: 500;
    color: #252C4B !important;
    font-size: 14px;
}

/* Alert Boxes */
[data-testid="stAlert"] {
    border-radius: 10px;
    border: 1px solid transparent;
}

/* Hero & Section Banners */
.pf-banner {
    background: linear-gradient(125deg, #202747 0%, #2A3460 50%, #3C2E75 100%);
    padding: 2rem 2.2rem;
    border-radius: 16px;
    color: #FFFFFF;
    box-shadow: 0 10px 28px rgba(32, 39, 71, 0.12);
    margin-bottom: 1.5rem;
}

.pf-banner h1 {
    color: #FFFFFF !important;
    font-size: 28px !important;
    margin: 6px 0 8px 0 !important;
    font-weight: 800 !important;
}

.pf-banner p {
    color: #D3DBF0 !important;
    font-size: 14.5px !important;
    margin: 0 !important;
    max-width: 720px;
    line-height: 1.5;
}

.pf-tagline-badge {
    display: inline-block;
    background: rgba(139, 124, 246, 0.2);
    border: 1px solid rgba(139, 124, 246, 0.4);
    color: #E2DEFF !important;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    padding: 3px 10px;
    border-radius: 6px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

/* Skill Tags & Badges */
.skill-badge {
    display: inline-block;
    padding: 4px 10px;
    margin: 3px 3px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    line-height: 1.3;
}

.skill-badge-matched {
    background-color: #E8F8F2;
    color: #17835E;
    border: 1px solid #B8EAD7;
}

.skill-badge-missing {
    background-color: #FFF4EC;
    color: #C26322;
    border: 1px solid #FEDAC2;
}

.skill-badge-neutral {
    background-color: #EEF1FA;
    color: #4A5578;
    border: 1px solid #DAE0F2;
}

/* Level Badges */
.level-badge {
    display: inline-block;
    padding: 3px 9px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.level-beginner {
    background-color: #E6F7F0;
    color: #1B8A64;
}

.level-intermediate {
    background-color: #EDEAFE;
    color: #5D4AD4;
}

.level-advanced {
    background-color: #FFF0E6;
    color: #B55219;
}

/* Sidebar mini user card */
.sidebar-user-card {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 12px 14px;
    border-radius: 10px;
    margin-bottom: 1rem;
}

.sidebar-user-card h4 {
    color: #FFFFFF !important;
    font-size: 13.5px !important;
    margin: 0 !important;
    font-weight: 700 !important;
}

.sidebar-user-card p {
    color: #B9C6E4 !important;
    font-size: 11.5px !important;
    margin: 2px 0 0 0 !important;
}

/* Clean spacing */
.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1200px;
}
</style>
"""


def inject_custom_css():
    """Injects the centralized application stylesheet."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_page_header(
    title: str,
    subtitle: str,
    badge: Optional[str] = "PATHFINDER"
):
    """Renders a consistent, polished hero banner at the top of a page."""
    badge_html = f'<div class="pf-tagline-badge">{badge}</div>' if badge else ""
    st.markdown(
        f"""
        <div class="pf-banner">
            {badge_html}
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_skill_badges(skills, kind="matched") -> str:
    """Returns HTML for inline colored skill tags."""
    if not skills:
        return "<span style='color:#737D95;font-size:12px;'>None</span>"

    cls = f"skill-badge skill-badge-{kind}"
    return " ".join(f'<span class="{cls}">{s}</span>' for s in skills)


def render_level_badge(level: str) -> str:
    """Returns HTML for a difficulty badge."""
    lvl = str(level).strip().lower()
    if "beginner" in lvl:
        cls = "level-badge level-beginner"
    elif "intermediate" in lvl:
        cls = "level-badge level-intermediate"
    else:
        cls = "level-badge level-advanced"
    return f'<span class="{cls}">{level}</span>'


def get_plotly_theme_defaults() -> Dict[str, Any]:
    """Returns standardized layout dictionary for consistent Plotly visual styling."""
    return {
        "template": "plotly_white",
        "font": {"family": "Plus Jakarta Sans, Inter, sans-serif", "color": TEXT_MAIN},
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "margin": dict(l=15, r=15, t=40, b=20),
    }
