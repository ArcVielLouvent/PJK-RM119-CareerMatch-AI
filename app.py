"""
CareerMatch AI — Streamlit Application
AI-Powered Career Matching System by Team PJK-RM119

UI/UX Design: Dark Premium Theme — Inspired by Verdant Concept
Designed by: Islahul Hadi (UI/UX & Documentation Specialist)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Page Configuration (MUST be first Streamlit call)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="CareerMatch AI - Smart Career Matching",
    page_icon="CM",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS — Dark Premium Theme (Verdant-Inspired)
# ---------------------------------------------------------------------------
# Palet warna:
#   --accent     : Lime Green (#c5f467)   → CTA, highlight, badge
#   --accent-dim : Dim Lime (#8fb848)     → Accent sekunder
#   --bg         : Deep Dark (#0a0f0a)    → Background utama
#   --bg-card    : Glass Dark (#141a14)   → Background kartu
#   --bg-glass   : rgba(20,26,20,0.6)     → Glassmorphism
#   --text       : Off-White (#e8e8e8)    → Teks utama
#   --text-sec   : Muted (#8a9a8a)        → Teks sekunder
#   --border     : (#1f2e1f)              → Border kartu
#   --green      : (#4ade80)              → Skor tinggi (>80%)
#   --amber      : (#fbbf24)              → Skor sedang (50-79%)
#   --red        : (#f87171)              → Skor rendah (<50%)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* ── Import Google Font: Outfit + Inter ── */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── CSS Variables ── */
    :root {
        --accent: #c5f467;
        --accent-dim: #8fb848;
        --accent-glow: rgba(197, 244, 103, 0.15);
        --bg: #0a0f0a;
        --bg-card: #111811;
        --bg-glass: rgba(20, 26, 20, 0.65);
        --text: #e8e8e8;
        --text-sec: #8a9a8a;
        --border: #1f2e1f;
        --border-glow: rgba(197, 244, 103, 0.12);
    }

    /* ── Global Typography ── */
    *, html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    h1, h2, h3, h4, h5, h6,
    .hero-title, .stat-value {
        font-family: 'Outfit', sans-serif !important;
    }

    /* ── Smooth Scroll ── */
    html {
        scroll-behavior: smooth;
    }

    /* ── Sembunyikan elemen bawaan Streamlit ── */
    #MainMenu, footer, header {visibility: hidden;}

    /* ── Background with floating orbs ── */
    .stApp {
        background: var(--bg);
        background-image:
            radial-gradient(ellipse 80% 50% at 50% 0%, rgba(197,244,103,0.06) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 100%, rgba(40,80,20,0.08) 0%, transparent 50%);
    }

    .stApp > [data-testid="stAppViewContainer"]::before,
    .stApp > [data-testid="stAppViewContainer"]::after {
        content: '';
        position: fixed;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.4;
        pointer-events: none;
        z-index: 0;
    }

    .stApp > [data-testid="stAppViewContainer"]::before {
        width: 400px;
        height: 400px;
        background: rgba(197,244,103,0.04);
        top: -100px;
        right: -100px;
        animation: orbFloat1 20s ease-in-out infinite;
    }

    .stApp > [data-testid="stAppViewContainer"]::after {
        width: 300px;
        height: 300px;
        background: rgba(40,80,20,0.06);
        bottom: 10%;
        left: -80px;
        animation: orbFloat2 25s ease-in-out infinite;
    }

    /* ── Scrollbar Styling ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-dim); }

    /* ────────────────────────────────────────────────────────────
       ANIMATED GLOW KEYFRAMES
    ──────────────────────────────────────────────────────────── */
    @keyframes subtleGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(197,244,103,0.05); }
        50% { box-shadow: 0 0 40px rgba(197,244,103,0.1); }
    }

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
    }

    @keyframes pulseRing {
        0% { box-shadow: 0 0 0 0 rgba(197,244,103,0.3); }
        70% { box-shadow: 0 0 0 8px rgba(197,244,103,0); }
        100% { box-shadow: 0 0 0 0 rgba(197,244,103,0); }
    }

    @keyframes orbFloat1 {
        0%, 100% { transform: translate(0, 0) scale(1); }
        33% { transform: translate(-60px, 80px) scale(1.1); }
        66% { transform: translate(40px, -40px) scale(0.95); }
    }

    @keyframes orbFloat2 {
        0%, 100% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(80px, -60px) scale(1.15); }
    }

    /* ────────────────────────────────────────────────────────────
       HERO SECTION
    ──────────────────────────────────────────────────────────── */
    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 3.5rem 1rem 2rem 1rem;
        animation: fadeInUp 0.8s ease-out;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(197, 244, 103, 0.08);
        border: 1px solid rgba(197, 244, 103, 0.2);
        color: var(--accent);
        font-size: 0.75rem;
        font-weight: 600;
        padding: 6px 18px;
        border-radius: 50px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
    }

    .hero-badge::before {
        content: '';
        display: inline-block;
        width: 8px;
        height: 8px;
        background: var(--accent);
        border-radius: 50%;
        animation: pulseRing 2s ease-out infinite;
    }

    .hero-title {
        font-size: 3.4rem;
        font-weight: 800;
        color: var(--text);
        margin: 0;
        letter-spacing: -0.035em;
        line-height: 1.15;
    }

    .hero-title .accent {
        color: var(--accent);
        font-style: italic;
        font-weight: 900;
        background: linear-gradient(135deg, #c5f467 0%, #a8e040 50%, #8fb848 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        display: inline-block;
        padding-right: 0.15em;
        padding-bottom: 0.05em;
        overflow: visible;
    }

    .hero-title .accent::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #c5f467, transparent);
        border-radius: 2px;
        opacity: 0.4;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: var(--text-sec);
        font-weight: 400;
        margin-top: 1rem;
        line-height: 1.6;
        max-width: 560px;
        width: 100%;
        text-align: center;
        margin-left: auto;
        margin-right: auto;
    }

    .hero-features {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1.5rem;
        flex-wrap: wrap;
    }

    .hero-feature-item {
        display: flex;
        align-items: center;
        gap: 6px;
        color: var(--text-sec);
        font-size: 0.8rem;
        font-weight: 400;
    }

    .hero-feature-item::before {
        content: '◆';
        color: var(--accent);
        font-size: 0.5rem;
    }

    /* ────────────────────────────────────────────────────────────
       CARDS — Glassmorphism
    ──────────────────────────────────────────────────────────── */
    .card {
        background: var(--bg-glass);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease-out;
    }

    .card:hover {
        border-color: var(--border-glow);
        box-shadow: 0 8px 32px rgba(197, 244, 103, 0.06);
        transform: translateY(-3px);
    }

    /* ────────────────────────────────────────────────────────────
       RESULT CARD — Job Recommendation
    ──────────────────────────────────────────────────────────── */
    .result-card-header {
        display: flex;
        align-items: flex-start;
        gap: 14px;
    }

    .rank-badge {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 42px;
        height: 42px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.85rem;
        flex-shrink: 0;
    }

    .rank-1 {
        background: linear-gradient(135deg, rgba(197,244,103,0.2), rgba(197,244,103,0.05));
        border: 1px solid rgba(197,244,103,0.3);
        color: var(--accent);
    }
    .rank-2 {
        background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(139,92,246,0.05));
        border: 1px solid rgba(139,92,246,0.25);
        color: #a78bfa;
    }
    .rank-3 {
        background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(59,130,246,0.05));
        border: 1px solid rgba(59,130,246,0.25);
        color: #60a5fa;
    }
    .rank-default {
        background: rgba(138,154,138,0.1);
        border: 1px solid var(--border);
        color: var(--text-sec);
    }

    .job-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text);
        margin: 0 0 2px 0;
        line-height: 1.3;
    }

    .job-meta {
        font-size: 0.8rem;
        color: var(--text-sec);
    }

    /* ── Score Progress Bar ── */
    .score-section {
        margin-top: 1rem;
    }

    .score-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }

    .score-label {
        font-size: 0.72rem;
        color: var(--text-sec);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .score-value {
        font-size: 1.05rem;
        font-weight: 700;
        font-family: 'Outfit', sans-serif !important;
    }

    .score-high { color: #4ade80; }
    .score-mid  { color: #fbbf24; }
    .score-low  { color: #f87171; }

    .progress-bg {
        width: 100%;
        height: 6px;
        background: rgba(138,154,138,0.15);
        border-radius: 99px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        border-radius: 99px;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .progress-high { background: linear-gradient(90deg, #22c55e, #4ade80); }
    .progress-mid  { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .progress-low  { background: linear-gradient(90deg, #ef4444, #f87171); }

    /* ── Skills Tags ── */
    .skills-container {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 14px;
    }

    .skill-tag {
        display: inline-block;
        background: rgba(197, 244, 103, 0.08);
        color: var(--accent);
        font-size: 0.72rem;
        font-weight: 500;
        padding: 4px 12px;
        border-radius: 8px;
        border: 1px solid rgba(197, 244, 103, 0.15);
        letter-spacing: 0.01em;
    }

    /* ────────────────────────────────────────────────────────────
       SUMMARY STATS — Glass Cards
    ──────────────────────────────────────────────────────────── */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
        animation: fadeInUp 0.6s ease-out;
    }

    @media (max-width: 768px) {
        .stats-container { grid-template-columns: repeat(2, 1fr); }
    }

    .stat-card {
        background: var(--bg-glass);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem 1rem;
        text-align: center;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        transition: all 0.3s ease;
    }

    .stat-card:hover {
        border-color: var(--border-glow);
        animation: subtleGlow 3s ease-in-out infinite;
    }

    .stat-icon {
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .stat-icon svg {
        width: 24px;
        height: 24px;
    }

    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--accent);
        line-height: 1;
    }

    .stat-label {
        font-size: 0.68rem;
        color: var(--text-sec);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 6px;
        font-weight: 500;
    }

    /* ────────────────────────────────────────────────────────────
       SECTION LABEL
    ──────────────────────────────────────────────────────────── */
    .section-label {
        font-size: 0.72rem;
        color: var(--text-sec);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-weight: 600;
        margin-bottom: 1.2rem;
        margin-top: 0.5rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .section-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, var(--border), transparent);
    }

    /* ── Divider ── */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 2.5rem 0;
        border: none;
    }

    /* ────────────────────────────────────────────────────────────
       UPLOAD ZONE
    ──────────────────────────────────────────────────────────── */
    .upload-zone {
        border: 1.5px dashed var(--border);
        border-radius: 16px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        background: var(--bg-glass);
        backdrop-filter: blur(20px);
        transition: all 0.35s ease;
    }

    .upload-zone:hover {
        border-color: var(--accent);
        background: rgba(197, 244, 103, 0.03);
        box-shadow: 0 0 30px rgba(197, 244, 103, 0.05);
    }

    .upload-icon {
        margin-bottom: 0.5rem;
        animation: float 4s ease-in-out infinite;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .upload-icon svg {
        width: 48px;
        height: 48px;
    }

    .upload-text {
        color: var(--text-sec);
        font-size: 0.9rem;
    }

    .upload-text strong {
        color: var(--accent);
    }

    /* ────────────────────────────────────────────────────────────
       TABS
    ──────────────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: var(--bg-card);
        border-radius: 14px;
        padding: 5px;
        border: 1px solid var(--border);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 500;
        font-size: 0.85rem;
        color: var(--text-sec);
    }

    .stTabs [aria-selected="true"] {
        background: rgba(197, 244, 103, 0.1) !important;
        color: var(--accent) !important;
        font-weight: 600 !important;
        border: 1px solid rgba(197, 244, 103, 0.2) !important;
    }

    /* ────────────────────────────────────────────────────────────
       FORM INPUTS
    ──────────────────────────────────────────────────────────── */
    .stFileUploader > div {
        border: none !important;
        padding: 0 !important;
    }

    .stTextArea textarea {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 1rem !important;
    }

    .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(197, 244, 103, 0.1) !important;
    }

    .stTextArea textarea::placeholder {
        color: var(--text-sec) !important;
        opacity: 0.6 !important;
    }

    /* ── Primary CTA Button ── */
    .stButton > button {
        background: linear-gradient(135deg, #c5f467, #a8e040) !important;
        color: #0a0f0a !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 2rem !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.01em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        box-shadow: 0 2px 15px rgba(197, 244, 103, 0.2) !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #d4ff7a, #c5f467) !important;
        box-shadow: 0 4px 25px rgba(197, 244, 103, 0.35) !important;
        transform: translateY(-2px) !important;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* ────────────────────────────────────────────────────────────
       SIDEBAR
    ──────────────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: var(--bg-card) !important;
        border-right: 1px solid var(--border) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdown"] {
        color: var(--text-sec);
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.5rem 0 1.5rem 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1rem;
    }

    .sidebar-brand-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        background: rgba(197, 244, 103, 0.12);
        border: 1px solid rgba(197, 244, 103, 0.25);
        border-radius: 10px;
    }

    .sidebar-brand-icon svg {
        width: 18px;
        height: 18px;
    }

    .sidebar-brand-text {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        color: var(--text);
        letter-spacing: -0.02em;
    }

    .sidebar-brand-text span {
        color: var(--accent);
    }

    .sidebar-section {
        font-size: 0.68rem;
        font-weight: 600;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.75rem;
        margin-top: 1.8rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .sidebar-section::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
    }

    .team-item {
        padding: 10px 0;
        border-bottom: 1px solid rgba(31, 46, 31, 0.5);
        transition: all 0.2s ease;
    }

    .team-item:hover {
        padding-left: 6px;
    }

    .team-name {
        font-weight: 600;
        font-size: 0.85rem;
        color: var(--text);
    }

    .team-role {
        font-size: 0.73rem;
        color: var(--text-sec);
    }

    /* ── Step Indicator ── */
    .how-it-works-step {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 12px;
    }

    .step-number {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        min-width: 24px;
        border-radius: 8px;
        background: rgba(197, 244, 103, 0.1);
        border: 1px solid rgba(197, 244, 103, 0.2);
        color: var(--accent);
        font-size: 0.7rem;
        font-weight: 700;
        font-family: 'Outfit', sans-serif;
    }

    .step-text {
        font-size: 0.82rem;
        color: var(--text-sec);
        line-height: 1.45;
    }

    .step-text strong {
        color: var(--text);
    }

    /* ── Tech Stack Tags ── */
    .tech-tag-container {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
    }

    .tech-tag {
        display: inline-block;
        background: rgba(197, 244, 103, 0.06);
        color: var(--text-sec);
        font-size: 0.7rem;
        font-weight: 500;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid var(--border);
    }

    /* ── Kualifikasi Panel — Structured Layout ── */
    .qual-panel {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.25rem 1.25rem 1.5rem 1.25rem;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .qual-panel-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border);
    }

    .qual-panel-header svg {
        width: 18px;
        height: 18px;
        flex-shrink: 0;
    }

    .qual-panel-title {
        font-family: 'Outfit', sans-serif;
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--text);
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .qual-section {
        margin-bottom: 1rem;
    }

    .qual-section:last-child {
        margin-bottom: 0;
    }

    .qual-section-label {
        font-size: 0.65rem;
        font-weight: 600;
        color: var(--accent-dim);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }

    .qual-items {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
    }

    .qual-item {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(197, 244, 103, 0.06);
        color: var(--text);
        font-size: 0.75rem;
        font-weight: 400;
        padding: 5px 12px;
        border-radius: 8px;
        border: 1px solid var(--border);
        line-height: 1.4;
    }

    .qual-item-accent {
        background: rgba(197, 244, 103, 0.1);
        border-color: rgba(197, 244, 103, 0.2);
        color: var(--accent);
        font-weight: 500;
    }

    .qual-body-text {
        font-size: 0.82rem;
        color: var(--text-sec);
        line-height: 1.7;
        padding: 0.5rem 0 0.25rem 0;
        word-break: break-word;
    }

    .qual-body-text strong {
        color: var(--text);
    }

    /* Ensure expander content is not clipped */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        overflow: visible !important;
        padding-bottom: 0.5rem !important;
    }

    /* ── Expander Styling ── */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        color: var(--text-sec) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
    }

    /* ────────────────────────────────────────────────────────────
       ANALYTICS DASHBOARD — Verdant-Inspired
    ──────────────────────────────────────────────────────────── */
    .analytics-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0 1.5rem 0;
        animation: fadeInUp 0.7s ease-out;
    }

    @media (max-width: 768px) {
        .analytics-grid { grid-template-columns: 1fr; }
    }

    .analytics-card {
        background: var(--bg-glass);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.5rem;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .analytics-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(197,244,103,0.2), transparent);
    }

    .analytics-card:hover {
        border-color: var(--border-glow);
        box-shadow: 0 8px 40px rgba(197, 244, 103, 0.06);
        transform: translateY(-2px);
    }

    .analytics-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }

    .analytics-card-title {
        font-family: 'Outfit', sans-serif;
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--text);
    }

    .analytics-card-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(197, 244, 103, 0.08);
        border: 1px solid rgba(197, 244, 103, 0.15);
        color: var(--accent);
        font-size: 0.65rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 50px;
        letter-spacing: 0.04em;
    }

    .analytics-card-badge::before {
        content: '';
        display: inline-block;
        width: 5px;
        height: 5px;
        background: var(--accent);
        border-radius: 50%;
    }

    /* ── Gauge Chart ── */
    .gauge-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem 0;
    }

    .gauge-ring {
        position: relative;
        width: 140px;
        height: 140px;
    }

    .gauge-ring svg {
        width: 140px;
        height: 140px;
        transform: rotate(-90deg);
    }

    .gauge-ring circle {
        fill: none;
        stroke-width: 8;
        stroke-linecap: round;
    }

    .gauge-bg {
        stroke: rgba(138,154,138,0.12);
    }

    .gauge-fill {
        transition: stroke-dashoffset 1.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .gauge-label {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
    }

    .gauge-value {
        font-family: 'Outfit', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: var(--accent);
        line-height: 1;
    }

    .gauge-sub {
        font-size: 0.65rem;
        color: var(--text-sec);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 4px;
    }

    /* ── Score Breakdown List ── */
    .score-breakdown {
        margin-top: 1rem;
    }

    .score-breakdown-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid rgba(31,46,31,0.4);
    }

    .score-breakdown-item:last-child {
        border-bottom: none;
    }

    .score-breakdown-name {
        font-size: 0.78rem;
        color: var(--text-sec);
        flex: 1;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        padding-right: 12px;
    }

    .score-breakdown-bar {
        width: 80px;
        height: 4px;
        background: rgba(138,154,138,0.15);
        border-radius: 99px;
        overflow: hidden;
        margin-right: 10px;
        flex-shrink: 0;
    }

    .score-breakdown-fill {
        height: 100%;
        border-radius: 99px;
        transition: width 1s ease;
    }

    .score-breakdown-val {
        font-family: 'Outfit', sans-serif;
        font-size: 0.78rem;
        font-weight: 600;
        min-width: 36px;
        text-align: right;
    }

    /* ── YoE Comparison ── */
    .yoe-compare {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-top: 0.75rem;
    }

    .yoe-block {
        flex: 1;
        text-align: center;
        padding: 0.75rem;
        background: rgba(20,26,20,0.5);
        border-radius: 12px;
        border: 1px solid var(--border);
    }

    .yoe-block-value {
        font-family: 'Outfit', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--accent);
        line-height: 1;
    }

    .yoe-block-label {
        font-size: 0.6rem;
        color: var(--text-sec);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 4px;
    }

    .yoe-vs {
        font-size: 0.7rem;
        color: var(--text-sec);
        font-weight: 600;
    }

    /* ── Empty State ── */
    .empty-state {
        text-align: center;
        padding: 3.5rem 1rem;
        color: var(--text-sec);
    }

    .empty-icon {
        margin-bottom: 1rem;
        opacity: 0.3;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .empty-icon svg {
        width: 56px;
        height: 56px;
    }

    /* ────────────────────────────────────────────────────────────
       FEATURE CARDS — Landing / "How it works" inline
    ──────────────────────────────────────────────────────────── */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 1.5rem 0 2rem 0;
        animation: fadeInUp 0.8s ease-out 0.3s both;
    }

    @media (max-width: 768px) {
        .feature-grid { grid-template-columns: 1fr; }
    }

    .feature-card {
        background: var(--bg-glass);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        transition: all 0.35s ease;
    }

    .feature-card:hover {
        border-color: rgba(197, 244, 103, 0.2);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(197, 244, 103, 0.06);
    }

    .feature-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: rgba(197, 244, 103, 0.1);
        border: 1px solid rgba(197, 244, 103, 0.2);
        margin-bottom: 1rem;
    }

    .feature-icon svg {
        width: 20px;
        height: 20px;
    }

    .feature-title {
        font-family: 'Outfit', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 6px;
    }

    .feature-desc {
        font-size: 0.8rem;
        color: var(--text-sec);
        line-height: 1.5;
    }

    /* ────────────────────────────────────────────────────────────
       FOOTER
    ──────────────────────────────────────────────────────────── */
    .app-footer {
        text-align: center;
        padding: 2.5rem 1rem;
        margin-top: 2rem;
        border-top: 1px solid var(--border);
    }

    .footer-label {
        font-size: 0.65rem;
        color: var(--text-sec);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-weight: 500;
        margin-bottom: 1rem;
    }

    .footer-brand {
        font-family: 'Outfit', sans-serif;
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--text-sec);
    }

    .footer-brand span {
        color: var(--accent);
        font-weight: 700;
    }

    /* ────────────────────────────────────────────────────────────
       ALERT / NOTIFICATION OVERRIDES
    ──────────────────────────────────────────────────────────── */
    .stAlert {
        border-radius: 12px !important;
    }

    /* ── Chart Overrides ── */
    .stBarChart, .stLineChart {
        border-radius: 14px;
        overflow: hidden;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Model Loading — di-cache agar hanya dijalankan 1x
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def init_model():
    """Load model dari cache (.joblib) atau training baru jika belum ada."""
    from core.pipeline import load_or_train_model
    return load_or_train_model()


# ---------------------------------------------------------------------------
# Helper — Tentukan warna skor berdasarkan nilai
# ---------------------------------------------------------------------------
def _score_class(score: float) -> str:
    """Return CSS class suffix berdasarkan threshold skor."""
    if score >= 80:
        return "high"   # Hijau
    elif score >= 50:
        return "mid"    # Kuning/Oranye
    else:
        return "low"    # Merah


def _extract_skills_from_quals(qual_text: str) -> list[str]:
    """
    Ekstrak keyword skills sederhana dari teks kualifikasi
    untuk ditampilkan sebagai tags di kartu hasil.
    """
    import re
    if not qual_text or qual_text == "nan":
        return []

    # Pattern untuk mendeteksi skill-like keywords
    skill_patterns = [
        r'\b(?:Python|Java|JavaScript|SQL|HTML|CSS|React|Node\.js|C\+\+|PHP|Ruby)\b',
        r'\b(?:Excel|Word|PowerPoint|SAP|Oracle|AutoCAD|Photoshop|Figma)\b',
        r'\b(?:Machine Learning|Data Analysis|NLP|Deep Learning|AI|TensorFlow)\b',
        r'\b(?:Project Management|Communication|Leadership|Teamwork|Problem Solving)\b',
        r'\b(?:Marketing|Sales|Accounting|Finance|Engineering|Design)\b',
        r'\b(?:Bachelor|Master|MBA|PhD|Degree)\b',
    ]

    found = set()
    for pattern in skill_patterns:
        matches = re.findall(pattern, qual_text, re.IGNORECASE)
        for m in matches:
            found.add(m.strip().title())

    # Juga ambil kata kunci pendek dari RequiredQual
    words = qual_text.split()
    for w in words:
        clean_w = re.sub(r'[^a-zA-Z+#.]', '', w)
        if len(clean_w) > 2 and clean_w[0].isupper() and clean_w not in {
            'The', 'And', 'For', 'With', 'Must', 'Have', 'Will', 'Should',
            'This', 'That', 'From', 'Been', 'Has', 'Had', 'Are', 'Not',
            'But', 'Also', 'Can', 'May', 'All', 'Any', 'Other', 'Years',
            'Experience', 'Required', 'Preferred', 'Knowledge', 'Skills',
            'Ability', 'Minimum', 'Work', 'Working', 'Strong', 'Good',
        }:
            if clean_w not in found and len(found) < 8:
                found.add(clean_w)

    return list(found)[:8]


# ---------------------------------------------------------------------------
# Sidebar — Info, How It Works, Team
# ---------------------------------------------------------------------------
def render_sidebar():
    with st.sidebar:
        # ── Brand ──
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-brand-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#c5f467"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"/></svg></div>
                <div class="sidebar-brand-text">Career<span>Match</span> AI</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sidebar-section">About</div>', unsafe_allow_html=True)
        st.markdown(
            """
            **CareerMatch AI** automates the matching of CV skills
            against job postings using NLP & Machine Learning.

            Upload your ATS-friendly CV and get instant
            job recommendations ranked by compatibility.
            """
        )

        st.markdown('<div class="sidebar-section">How It Works</div>', unsafe_allow_html=True)

        steps = [
            ("1", "<strong>Extract</strong> — Text is parsed from your PDF"),
            ("2", "<strong>Process</strong> — NLP cleans & lemmatizes skills"),
            ("3", "<strong>Align</strong> — Terms mapped to job vocabulary"),
            ("4", "<strong>Match</strong> — TF-IDF + Cosine Similarity"),
            ("5", "<strong>Rank</strong> — Business rules filter & boost"),
        ]
        for num, text in steps:
            st.markdown(
                f'<div class="how-it-works-step">'
                f'<div class="step-number">{num}</div>'
                f'<div class="step-text">{text}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="sidebar-section">Tech Stack</div>', unsafe_allow_html=True)

        techs = ["Python", "spaCy", "NLTK", "Scikit-Learn", "TF-IDF", "Cosine Sim", "Streamlit"]
        tags_html = "".join(f'<span class="tech-tag">{t}</span>' for t in techs)
        st.markdown(f'<div class="tech-tag-container">{tags_html}</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">Team PJK-RM119</div>', unsafe_allow_html=True)

        team = [
            ("Armand Al-Farizy", "Project Manager & Lead AI/ML Engineer"),
            ("Aisyah Ridhalillah Putri", "Data Analyst & Researcher"),
            ("Islahul Hadi", "UI/UX & Documentation Specialist"),
            ("Faber Dui Nababan", "QA Tester"),
        ]
        for name, role in team:
            st.markdown(
                f'<div class="team-item">'
                f'<div class="team-name">{name}</div>'
                f'<div class="team-role">{role}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("Pijak × IBM SkillsBuild 2026 — Capstone Project")


# ---------------------------------------------------------------------------
# Result Card Component — Kartu rekomendasi pekerjaan
# ---------------------------------------------------------------------------
def _parse_qualifications(qual_text: str) -> dict:
    """Parse qualification text into structured categories."""
    import re
    result = {"skills": [], "education": [], "experience": [], "other": []}
    if not qual_text or qual_text == "nan":
        return result

    # Education patterns
    edu_patterns = re.findall(
        r"(?:Bachelor|Master|MBA|PhD|Degree|Diploma|B\.?S\.?|M\.?S\.?|B\.?A\.?|M\.?A\.?)"
        r"(?:[^.;,]*(?:in|of)[^.;,]*)?",
        qual_text, re.IGNORECASE
    )
    for e in edu_patterns:
        cleaned = e.strip().rstrip('.,;')
        if cleaned and len(cleaned) > 2:
            result["education"].append(cleaned.title())

    # Experience patterns
    exp_patterns = re.findall(
        r'\d+\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience\s*)?(?:in\s+[^.;,]{3,40})?',
        qual_text, re.IGNORECASE
    )
    for e in exp_patterns:
        cleaned = e.strip().rstrip('.,;')
        if cleaned:
            result["experience"].append(cleaned.title())

    # Technical skills
    tech_skills = re.findall(
        r'\b(?:Python|Java|JavaScript|TypeScript|SQL|HTML|CSS|React|Angular|Vue|'
        r'Node\.js|C\+\+|C#|PHP|Ruby|Go|Rust|Swift|Kotlin|R|Scala|'
        r'Excel|Word|PowerPoint|SAP|Oracle|AutoCAD|Photoshop|Figma|Sketch|'
        r'Machine Learning|Data Analysis|NLP|Deep Learning|AI|TensorFlow|PyTorch|'
        r'Docker|Kubernetes|AWS|Azure|GCP|Git|Linux|REST|API|Agile|Scrum|'
        r'Project Management|Communication|Leadership|Teamwork|Problem Solving|'
        r'Marketing|Accounting|Finance|Engineering|Design|DevOps|CI/CD)\b',
        qual_text, re.IGNORECASE
    )
    seen = set()
    for s in tech_skills:
        title = s.strip().title()
        if title not in seen:
            seen.add(title)
            result["skills"].append(title)

    # Remaining meaningful sentences as "other"
    sentences = re.split(r'[.;]', qual_text)
    for sent in sentences:
        sent = sent.strip()
        if len(sent) > 15 and not any(kw.lower() in sent.lower() for kw in
            [p.strip() for p in result["education"] + result["experience"] + result["skills"] if p]):
            if len(result["other"]) < 3:
                result["other"].append(sent)

    return result


def render_result_card(rec: dict, rank: int):
    """Render satu kartu rekomendasi dengan score bar berwarna."""
    # Badge ranking
    rank_map = {1: ("#1", "rank-1"), 2: ("#2", "rank-2"), 3: ("#3", "rank-3")}
    icon, cls = rank_map.get(rank, (f"#{rank}", "rank-default"))
    badge_html = f'<div class="rank-badge {cls}">{icon}</div>'

    score = rec["Match Score"]
    sc = _score_class(score)

    yoe = rec["Required YoE"]
    yoe_text = f"{yoe} year{'s' if yoe != 1 else ''}" if yoe > 0 else "Not specified"

    # Skills tags
    qual_text = str(rec.get("Required Qualifications", ""))
    skills = _extract_skills_from_quals(qual_text)
    skills_html = ""
    if skills:
        tags = "".join(f'<span class="skill-tag">{s}</span>' for s in skills)
        skills_html = f'<div class="skills-container">{tags}</div>'

    card_html = (
        f'<div class="card">'
        f'<div class="result-card-header">'
        f'{badge_html}'
        f'<div>'
        f'<p class="job-title">{rec["Job Title"]}</p>'
        f'<p class="job-meta">Experience Required: {yoe_text}</p>'
        f'</div>'
        f'</div>'
        f'<div class="score-section">'
        f'<div class="score-row">'
        f'<span class="score-label">Match Score</span>'
        f'<span class="score-value score-{sc}">{score}%</span>'
        f'</div>'
        f'<div class="progress-bg">'
        f'<div class="progress-fill progress-{sc}" style="width: {score}%;"></div>'
        f'</div>'
        f'</div>'
        f'{skills_html}'
        f'</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

    # Structured qualifications panel
    if qual_text and qual_text != "nan":
        with st.expander("View Full Qualifications", expanded=False):
            parsed = _parse_qualifications(qual_text)

            svg_qual = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#c5f467"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z"/></svg>'

            panel_html = f'<div class="qual-panel"><div class="qual-panel-header">{svg_qual}<span class="qual-panel-title">Required Qualifications</span></div>'

            # Skills section
            if parsed["skills"]:
                items = ''.join(f'<span class="qual-item qual-item-accent">{s}</span>' for s in parsed["skills"])
                panel_html += f'<div class="qual-section"><div class="qual-section-label">Technical Skills</div><div class="qual-items">{items}</div></div>'

            # Education section
            if parsed["education"]:
                items = ''.join(f'<span class="qual-item">{e}</span>' for e in parsed["education"])
                panel_html += f'<div class="qual-section"><div class="qual-section-label">Education</div><div class="qual-items">{items}</div></div>'

            # Experience section
            if parsed["experience"]:
                items = ''.join(f'<span class="qual-item">{e}</span>' for e in parsed["experience"])
                panel_html += f'<div class="qual-section"><div class="qual-section-label">Experience</div><div class="qual-items">{items}</div></div>'

            # Full text as fallback / additional info
            panel_html += f'<div class="qual-section"><div class="qual-section-label">Full Description</div><div class="qual-body-text">{qual_text}</div></div>'

            panel_html += '</div>'
            st.markdown(panel_html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------
def main():
    render_sidebar()

    # ── Hero Header ──
    hero_html = (
        '<div class="hero-container">'
        '<div class="hero-badge">AI-Powered Career Matching</div>'
        '<h1 class="hero-title">Intelligence that<br>'
        '<span class="accent">matches</span> your career.</h1>'
        '<p class="hero-subtitle">'
        'Upload your CV and let our AI analyze your skills against '
        '12,000+ job postings to find your perfect career match.'
        '</p>'
        '<div class="hero-features">'
        '<span class="hero-feature-item">NLP-Powered Analysis</span>'
        '<span class="hero-feature-item">12,000+ Job Postings</span>'
        '<span class="hero-feature-item">Instant Results</span>'
        '</div>'
        '</div>'
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    # ── Feature Cards ──
    # SVG icon definitions for feature cards
    svg_upload = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#c5f467"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m6.75 12l-3-3m0 0l-3 3m3-3v6m-1.5-15H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"/></svg>'
    svg_brain = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#c5f467"><path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z"/></svg>'
    svg_target = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#c5f467"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"/></svg>'

    feature_html = (
        '<div class="feature-grid">'
        '<div class="feature-card">'
        f'<div class="feature-icon">{svg_upload}</div>'
        '<div class="feature-title">Upload your CV</div>'
        '<div class="feature-desc">Simply upload your PDF CV and our system will extract &amp; analyze your skills automatically.</div>'
        '</div>'
        '<div class="feature-card">'
        f'<div class="feature-icon">{svg_brain}</div>'
        '<div class="feature-title">AI-Powered Matching</div>'
        '<div class="feature-desc">NLP cleans and aligns your skills, then TF-IDF + Cosine Similarity finds the best matches.</div>'
        '</div>'
        '<div class="feature-card">'
        f'<div class="feature-icon">{svg_target}</div>'
        '<div class="feature-title">Get Recommendations</div>'
        '<div class="feature-desc">Receive ranked job recommendations with match scores, required experience &amp; qualifications.</div>'
        '</div>'
        '</div>'
    )
    st.markdown(feature_html, unsafe_allow_html=True)

    # ── Load Model ──
    with st.spinner("Initializing AI engine..."):
        try:
            vectorizer, job_matrix, clean_df = init_model()
        except Exception as e:
            st.error(f"Failed to initialize model: {e}")
            st.markdown(
                """
                **How to fix this:**

                **Option A — Setup Kaggle API:**
                1. Go to [kaggle.com/settings](https://www.kaggle.com/settings) → API → **Create New Token**
                2. Save `kaggle.json` to `C:\\Users\\<YourName>\\.kaggle\\kaggle.json`
                3. Restart this app

                **Option B — Download manually:**
                1. Download from [kaggle.com/datasets/madhab/jobposts](https://www.kaggle.com/datasets/madhab/jobposts)
                2. Place `data job posts.csv` in the `data/` folder
                3. Restart this app
                """
            )
            st.stop()

    # ── Divider ──
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Input Section — 2 Tabs ──
    tab_upload, tab_manual = st.tabs(["Upload CV (PDF)", "Manual Skills Input"])

    cv_text = None
    source_label = None

    # -- Tab 1: Upload CV --
    with tab_upload:
        svg_doc_upload = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#c5f467"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5"/></svg>'
        upload_zone_html = (
            '<div class="upload-zone">'
            f'<div class="upload-icon">{svg_doc_upload}</div>'
            '<div class="upload-text">'
            'Drag and drop your <strong>PDF CV</strong> here<br>'
            '<span style="font-size: 0.8rem; opacity: 0.5;">'
            'ATS-friendly format   English or Indonesian   Max 10 MB'
            '</span>'
            '</div>'
            '</div>'
        )
        st.markdown(upload_zone_html, unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload your CV",
            type=["pdf"],
            label_visibility="collapsed",
            key="pdf_uploader",
        )

        if uploaded_file is not None:
            from core.pdf_extractor import extract_pdf_text

            with st.spinner("Extracting text from PDF..."):
                raw_text, status = extract_pdf_text(uploaded_file)

            if raw_text:
                cv_text = raw_text
                source_label = f"{uploaded_file.name}"
                st.success(f"Successfully extracted text from **{uploaded_file.name}**")
            else:
                st.error(f"{status}")
                st.info("Try the **Manual Skills Input** tab to enter your skills directly.")

    # -- Tab 2: Manual Input (Fallback) --
    with tab_manual:
        manual_desc_html = (
            '<p style="color: var(--text-sec); font-size: 0.85rem; margin-bottom: 1rem;">'
            'Paste your CV content or type your skills, qualifications, and experience below. '
            'This is useful as a <strong style="color: var(--accent);">fallback</strong> when PDF extraction is not possible.'
            '</p>'
        )
        st.markdown(manual_desc_html, unsafe_allow_html=True)
        manual_text = st.text_area(
            "Enter your skills and experience",
            height=200,
            placeholder=(
                "e.g., Python, Machine Learning, 3 years of experience in data analysis, "
                "SQL, TensorFlow, Bachelor's degree in Computer Science..."
            ),
            label_visibility="collapsed",
            key="manual_input",
        )

        if st.button("Analisis Kecocokan Karier", key="analyze_btn"):
            if manual_text and manual_text.strip():
                cv_text = manual_text.strip()
                source_label = "Manual Input"
            else:
                st.warning("Please enter your skills and experience first.")

    # ── Results Section ──
    if cv_text:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        from core.inference import get_job_recommendations, extract_yoe

        with st.spinner("Analyzing your profile and matching against 12,000+ job postings..."):
            results = get_job_recommendations(
                cv_text=cv_text,
                tfidf_model=vectorizer,
                job_matrix=job_matrix,
                clean_df=clean_df,
                top_k=5,
            )
            detected_yoe = extract_yoe(cv_text)

        if results:
            # ── Summary Stats ──
            best_score = results[0]["Match Score"]
            avg_score = round(sum(r["Match Score"] for r in results) / len(results), 1)

            # SVG icons for stat cards
            svg_calendar = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#c5f467"><path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5"/></svg>'
            svg_trophy = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#c5f467"><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 18.75h-9m9 0a3 3 0 013 3h-15a3 3 0 013-3m9 0v-3.375c0-.621-.503-1.125-1.125-1.125h-.871M7.5 18.75v-3.375c0-.621.504-1.125 1.125-1.125h.872m5.007 0H9.497m5.007 0a7.454 7.454 0 01-.982-3.172M9.497 14.25a7.454 7.454 0 00.981-3.172M5.25 4.236c-.982.143-1.954.317-2.916.52A6.003 6.003 0 007.73 9.728M5.25 4.236V4.5c0 2.108.966 3.99 2.48 5.228M5.25 4.236V2.721C7.456 2.41 9.71 2.25 12 2.25c2.291 0 4.545.16 6.75.47v1.516M18.75 4.236c.982.143 1.954.317 2.916.52A6.003 6.003 0 0016.27 9.728M18.75 4.236V4.5c0 2.108-.966 3.99-2.48 5.228M18.75 4.236V2.721M12 12.75a2.25 2.25 0 01-2.248-2.354M12 12.75a2.25 2.25 0 002.248-2.354M12 12.75V14.25"/></svg>'
            svg_chart = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#c5f467"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941"/></svg>'
            svg_briefcase = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#c5f467"><path stroke-linecap="round" stroke-linejoin="round" d="M20.25 14.15v4.25c0 1.094-.787 2.036-1.872 2.18-2.087.277-4.216.42-6.378.42s-4.291-.143-6.378-.42c-1.085-.144-1.872-1.086-1.872-2.18v-4.25m16.5 0a2.18 2.18 0 00.75-1.661V8.706c0-1.081-.768-2.015-1.837-2.175a48.114 48.114 0 00-3.413-.387m4.5 8.006c-.194.165-.42.295-.673.38A23.978 23.978 0 0112 15.75c-2.648 0-5.195-.429-7.577-1.22a2.016 2.016 0 01-.673-.38m0 0A2.18 2.18 0 013 12.489V8.706c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 013.413-.387m7.5 0V5.25A2.25 2.25 0 0013.5 3h-3a2.25 2.25 0 00-2.25 2.25v.894m7.5 0a48.667 48.667 0 00-7.5 0M12 12.75h.008v.008H12v-.008z"/></svg>'

            stats_html = (
                f'<div class="stats-container">'
                f'<div class="stat-card"><span class="stat-icon">{svg_calendar}</span>'
                f'<div class="stat-value">{detected_yoe}</div>'
                f'<div class="stat-label">Years Detected</div></div>'
                f'<div class="stat-card"><span class="stat-icon">{svg_trophy}</span>'
                f'<div class="stat-value">{best_score}%</div>'
                f'<div class="stat-label">Best Match</div></div>'
                f'<div class="stat-card"><span class="stat-icon">{svg_chart}</span>'
                f'<div class="stat-value">{avg_score}%</div>'
                f'<div class="stat-label">Avg Score</div></div>'
                f'<div class="stat-card"><span class="stat-icon">{svg_briefcase}</span>'
                f'<div class="stat-value">{len(results)}</div>'
                f'<div class="stat-label">Jobs Found</div></div>'
                f'</div>'
            )
            st.markdown(stats_html, unsafe_allow_html=True)

            # ── Recommendation Cards ──
            st.markdown(
                '<p class="section-label">Top Recommendations</p>',
                unsafe_allow_html=True,
            )

            for idx, rec in enumerate(results, 1):
                render_result_card(rec, idx)

            # ── Analytics Dashboard ──
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown(
                '<p class="section-label">Analytics Dashboard</p>',
                unsafe_allow_html=True,
            )

            # Prepare data
            chart_titles = [r["Job Title"][:40] for r in reversed(results)]
            chart_scores = [r["Match Score"] for r in reversed(results)]
            all_scores = [r["Match Score"] for r in results]
            avg_yoe = round(sum(r["Required YoE"] for r in results) / len(results), 1)

            # ── Analytics Grid: Gauge + Breakdown ──
            # Build SVG gauge for best match score
            circumference = 2 * 3.14159 * 54  # radius = 54
            offset = circumference * (1 - best_score / 100)
            gauge_color = '#4ade80' if best_score >= 80 else ('#c5f467' if best_score >= 50 else '#f87171')

            gauge_html = (
                '<div class="gauge-container">'
                '<div class="gauge-ring">'
                f'<svg viewBox="0 0 120 120">'
                f'<circle class="gauge-bg" cx="60" cy="60" r="54"/>'
                f'<circle class="gauge-fill" cx="60" cy="60" r="54" '
                f'stroke="{gauge_color}" '
                f'stroke-dasharray="{circumference}" '
                f'stroke-dashoffset="{offset}"/>'
                f'</svg>'
                '<div class="gauge-label">'
                f'<div class="gauge-value">{best_score}%</div>'
                '<div class="gauge-sub">Best Match</div>'
                '</div>'
                '</div>'
                '</div>'
            )

            # Score breakdown list
            breakdown_html = '<div class="score-breakdown">'
            for r in results:
                s = r["Match Score"]
                sc_cls = _score_class(s)
                color_map = {'high': '#4ade80', 'mid': '#fbbf24', 'low': '#f87171'}
                fill_color = color_map[sc_cls]
                breakdown_html += (
                    '<div class="score-breakdown-item">'
                    f'<span class="score-breakdown-name">{r["Job Title"][:35]}</span>'
                    f'<div class="score-breakdown-bar"><div class="score-breakdown-fill" style="width:{s}%;background:{fill_color}"></div></div>'
                    f'<span class="score-breakdown-val" style="color:{fill_color}">{s}%</span>'
                    '</div>'
                )
            breakdown_html += '</div>'

            # YoE comparison
            yoe_html = (
                '<div class="yoe-compare">'
                f'<div class="yoe-block"><div class="yoe-block-value">{detected_yoe}</div>'
                '<div class="yoe-block-label">Your Experience</div></div>'
                '<div class="yoe-vs">vs</div>'
                f'<div class="yoe-block"><div class="yoe-block-value">{avg_yoe}</div>'
                '<div class="yoe-block-label">Avg Required</div></div>'
                '</div>'
            )

            analytics_html = (
                '<div class="analytics-grid">'
                # Card 1: Match Score Gauge
                '<div class="analytics-card">'
                '<div class="analytics-card-header">'
                '<span class="analytics-card-title">Match Score Overview</span>'
                f'<span class="analytics-card-badge">Top {len(results)} Results</span>'
                '</div>'
                f'{gauge_html}'
                f'{yoe_html}'
                '</div>'
                # Card 2: Score Breakdown
                '<div class="analytics-card">'
                '<div class="analytics-card-header">'
                '<span class="analytics-card-title">Score Breakdown</span>'
                f'<span class="analytics-card-badge">Avg {avg_score}%</span>'
                '</div>'
                f'{breakdown_html}'
                '</div>'
                '</div>'
            )
            st.markdown(analytics_html, unsafe_allow_html=True)

            # ── Score Distribution Chart (Plotly) ──
            st.markdown(
                '<p class="section-label">Score Distribution</p>',
                unsafe_allow_html=True,
            )

            bar_colors = []
            for s in chart_scores:
                if s >= 80:
                    bar_colors.append('#4ade80')
                elif s >= 50:
                    bar_colors.append('#c5f467')
                else:
                    bar_colors.append('#f87171')

            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=chart_titles,
                x=chart_scores,
                orientation='h',
                marker=dict(
                    color=bar_colors,
                    line=dict(color='rgba(197,244,103,0.3)', width=1),
                ),
                text=[f'{s}%' for s in chart_scores],
                textposition='outside',
                textfont=dict(color='#e8e8e8', size=12, family='Outfit'),
                hovertemplate=(
                    '<b>%{y}</b><br>'
                    'Match Score: <b>%{x:.1f}%</b>'
                    '<extra></extra>'
                ),
            ))

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(20,26,20,0.6)',
                font=dict(family='Inter', color='#8a9a8a', size=11),
                xaxis=dict(
                    title=dict(
                        text='Match Score (%)',
                        font=dict(color='#8a9a8a', size=11),
                    ),
                    range=[0, 105],
                    gridcolor='rgba(31,46,31,0.5)',
                    gridwidth=1,
                    zeroline=False,
                    tickfont=dict(color='#8a9a8a'),
                    ticksuffix='%',
                ),
                yaxis=dict(
                    tickfont=dict(color='#e8e8e8', size=12),
                    gridcolor='rgba(0,0,0,0)',
                ),
                margin=dict(l=10, r=40, t=20, b=40),
                height=max(200, len(results) * 60 + 60),
                bargap=0.3,
                hoverlabel=dict(
                    bgcolor='#141a14',
                    bordercolor='rgba(197,244,103,0.3)',
                    font=dict(color='#e8e8e8', family='Inter'),
                ),
            )

            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        else:
            svg_search = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#8a9a8a"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/></svg>'
            empty_html = (
                '<div class="empty-state">'
                f'<div class="empty-icon">{svg_search}</div>'
                '<p><strong>No matching jobs found for your profile.</strong></p>'
                '<p style="font-size: 0.85rem;">Try adding more specific skills or using different keywords.</p>'
                '</div>'
            )
            st.markdown(empty_html, unsafe_allow_html=True)

    # ── Footer ──
    footer_html = (
        '<div class="app-footer">'
        '<div class="footer-label">Built by Team PJK-RM119</div>'
        '<div class="footer-brand">'
        'Career<span>Match</span> AI · Pijak × IBM SkillsBuild 2026'
        '</div>'
        '</div>'
    )
    st.markdown(footer_html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
