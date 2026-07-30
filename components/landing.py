import time

import streamlit as st
import streamlit.components.v1 as components


FEATURES = [
    ("🕳️", "Smart Missing Values", "Detect gaps instantly and auto-fill with Mean, Median or Mode."),
    ("📋", "Duplicate Detection", "Find and remove duplicate rows in a single click."),
    ("🤖", "ML Outlier Detection", "Isolation Forest spots anomalies your eyes would miss."),
    ("📈", "Rich Visual Analytics", "Histograms, box plots, bar charts and correlation heatmaps."),
    ("💡", "AI Insights & Grading", "Get a quality score, letter grade, and plain-English recommendations."),
    ("⬇️", "One-Click Export", "Download your cleaned dataset as CSV or Excel, ready to use."),
]

WHY_ITEMS = [
    ("01", "Your Data Stays Yours", "Everything runs in your session — nothing is stored or shared."),
    ("02", "Enterprise-Grade Cleaning", "Isolation Forest and statistical imputation, not just find-and-replace."),
    ("03", "See Before You Trust", "Full before/after comparison so you know exactly what changed."),
    ("04", "Export Anywhere", "One click to CSV or Excel — ready for your next tool."),
]

NAV_LINKS = [
    ("Home", "#top"),
    ("Why Us", "#why-choose"),
    ("Features", "#features"),
]

ORB_SVG = """
<svg viewBox="0 0 320 320" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="orbGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#EC4899" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#EC4899" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="orbBody" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3B2E63"/>
      <stop offset="55%" stop-color="#221B3D"/>
      <stop offset="100%" stop-color="#120E22"/>
    </linearGradient>
    <radialGradient id="eyeGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="35%" stop-color="#F9A8D4"/>
      <stop offset="100%" stop-color="#EC4899"/>
    </radialGradient>
    <filter id="blurSoft" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>
  <circle cx="160" cy="170" r="140" fill="url(#orbGlow)" filter="url(#blurSoft)"/>
  <rect x="70" y="90" width="180" height="160" rx="46" fill="url(#orbBody)" stroke="#EC4899" stroke-opacity="0.35"/>
  <circle cx="120" cy="165" r="20" fill="url(#eyeGlow)"/>
  <circle cx="200" cy="165" r="20" fill="url(#eyeGlow)"/>
  <path d="M120 210 Q160 230 200 210" stroke="#EC4899" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.6"/>
  <line x1="160" y1="90" x2="160" y2="65" stroke="#EC4899" stroke-width="3" stroke-linecap="round"/>
  <circle cx="160" cy="58" r="7" fill="#EC4899"/>
  <rect x="55" y="150" width="14" height="34" rx="7" fill="#3B2E63" stroke="#EC4899" stroke-opacity="0.35"/>
  <rect x="251" y="150" width="14" height="34" rx="7" fill="#3B2E63" stroke="#EC4899" stroke-opacity="0.35"/>
</svg>
"""

LOGO_SVG = """
<svg width="30" height="30" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F472B6"/>
      <stop offset="100%" stop-color="#DB2777"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="28" height="28" rx="9" fill="url(#logoGrad)" opacity="0.18"/>
  <rect x="1" y="1" width="28" height="28" rx="9" fill="none" stroke="url(#logoGrad)" stroke-width="1.4"/>
  <circle cx="15" cy="15" r="6.5" fill="none" stroke="url(#logoGrad)" stroke-width="1.6"/>
  <circle cx="15" cy="15" r="2.2" fill="url(#logoGrad)"/>
</svg>
"""


def _inject_landing_css():

    st.markdown(
        """
        <style>
        /* hide every bit of Streamlit's default top chrome */
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        header {
            display: none !important;
            height: 0 !important;
            visibility: hidden !important;
        }
        .stApp {
            margin-top: 0 !important;
            padding-top: 0 !important;
            background: transparent !important;
        }
        [data-testid="stAppViewContainer"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
            background: transparent !important;
        }
        [data-testid="stMain"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 2rem !important;
            max-width: 100% !important;
            margin-top: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            border: none !important;
        }

        /* ── NAVBAR ── */
        .navbar-wrap {
            position: sticky;
            top: 0;
            z-index: 999;
            margin: 0 !important;
            padding: 14px 34px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: transparent;
            backdrop-filter: none;
            -webkit-backdrop-filter: none;
            border-bottom: none;
        }
        .navbar-logo {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 16px;
            font-weight: 800;
            color: #F3F0FF;
            white-space: nowrap;
        }
        .navbar-logo span {
            background: linear-gradient(90deg, #F472B6, #DB2777);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .navbar-links {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 34px;
            flex: 1;
        }
        .navbar-links a {
            color: #D8CFEF;
            font-size: 14px;
            font-weight: 600;
            text-decoration: none;
            opacity: 0.85;
            transition: opacity 0.15s ease, color 0.15s ease;
        }
        .navbar-links a:hover {
            opacity: 1;
            color: #F9A8D4;
        }
        div[data-testid="stButton"] button[kind="primary"] {
            border-radius: 999px !important;
        }

        /* ── MOBILE COMPACT BAR (logo + hamburger, hidden on desktop) ──
           These are rendered as one raw-HTML block so they are real DOM
           siblings, unlike the desktop row below (see .st-key-navbar_desktop_row). */
        .navbar-mobile-bar {
            display: none;
            align-items: center;
            justify-content: space-between;
            width: 100%;
        }

        /* ── MOBILE HAMBURGER (inside navbar-mobile-bar, hidden on desktop) ── */
        .nav-hamburger {
            display: none;
            width: 40px;
            height: 40px;
            border-radius: 10px;
            background: rgba(236, 72, 153, 0.12);
            border: 1px solid rgba(236, 72, 153, 0.3);
            align-items: center;
            justify-content: center;
            cursor: pointer;
            flex-shrink: 0;
            -webkit-tap-highlight-color: transparent;
            transition: background 0.15s ease;
        }
        .nav-hamburger:active {
            background: rgba(236, 72, 153, 0.3);
        }
        .nav-hamburger svg {
            width: 18px;
            height: 18px;
            pointer-events: none;
        }

        /* ── MOBILE DROPDOWN MENU ── */
        .nav-mobile-menu {
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: rgba(13, 10, 26, 0.97);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(236, 72, 153, 0.2);
            padding: 18px 24px 22px 24px;
            flex-direction: column;
            gap: 4px;
            z-index: 1000;
        }
        .nav-mobile-menu.open {
            display: flex;
        }
        .nav-mobile-menu a {
            color: #D8CFEF;
            font-size: 15px;
            font-weight: 600;
            text-decoration: none;
            padding: 10px 14px;
            border-radius: 10px;
            transition: background 0.12s ease, color 0.12s ease;
        }
        .nav-mobile-menu a:hover,
        .nav-mobile-menu a:active {
            background: rgba(236, 72, 153, 0.1);
            color: #F9A8D4;
        }
        .nav-mobile-divider {
            height: 1px;
            background: rgba(236, 72, 153, 0.15);
            margin: 8px 0;
        }

        /* ── HERO ── */
        .landing-hero {
            text-align: center;
            padding: 28px 20px 20px 20px;
        }
        .landing-badge {
            display: inline-block;
            padding: 6px 18px;
            border-radius: 999px;
            background: rgba(236, 72, 153, 0.12);
            border: 1px solid rgba(236, 72, 153, 0.4);
            color: #F9A8D4;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-bottom: 18px;
        }
        .landing-title {
            font-size: 56px;
            font-weight: 800;
            line-height: 1.1;
            text-align: center;
            background: linear-gradient(90deg, #F3F0FF 0%, #F472B6 45%, #DB2777 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }
        .landing-hero p.landing-subtitle {
            font-size: 19px;
            color: #F4A8CB;
            max-width: 650px;
            width: 100%;
            margin: 0 auto 10px auto !important;
            font-weight: 400;
            text-align: center !important;
        }
        .landing-hero div[data-testid="stMarkdownContainer"] {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .landing-glow {
            position: fixed;
            top: -180px;
            left: 50%;
            transform: translateX(-50%);
            width: 700px;
            height: 700px;
            background: radial-gradient(circle, rgba(236,72,153,0.35) 0%, rgba(236,72,153,0) 70%);
            z-index: -1;
            pointer-events: none;
        }

        /* ── FEATURE CARDS ── */
        .feature-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(236, 72, 153, 0.22);
            border-radius: 18px;
            padding: 26px 22px;
            height: 100%;
            text-align: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }
        .feature-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 14px 34px rgba(236, 72, 153, 0.3);
            border-color: rgba(244, 114, 182, 0.6);
        }
        .feature-icon {
            font-size: 30px;
            margin-bottom: 10px;
        }
        .feature-title {
            font-size: 17px;
            font-weight: 700;
            color: #F3F0FF;
            margin-bottom: 6px;
        }
        .feature-desc {
            font-size: 14px;
            color: #B9AEDD;
            line-height: 1.5;
        }

        /* ── SECTION HEADINGS ── */
        .section-heading {
            text-align: center;
            font-size: 30px;
            font-weight: 800;
            color: #F3F0FF;
            margin: 10px 0 28px 0;
        }

        /* ── STEPS ── */
        .landing-steps {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 40px;
            flex-wrap: wrap;
            margin: 18px 0 40px 0;
            text-align: center;
        }
        .step-chip {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #F9A8D4;
            font-size: 14px;
            font-weight: 600;
        }
        .step-num {
            width: 26px;
            height: 26px;
            border-radius: 50%;
            background: linear-gradient(135deg, #DB2777, #F472B6);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
        }

        /* ── WHY CARDS ── */
        .why-card {
            text-align: center;
        }
        .why-heading {
            text-align: center;
        }

        /* ── FOOTER ── */
        .footer-wrap {
            margin-top: 60px;
            padding: 28px 34px 22px 34px;
            border-top: 1px solid rgba(236, 72, 153, 0.15);
        }
        .footer-inner {
            max-width: 1100px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }
        .footer-brand-name {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 15px;
            font-weight: 800;
            color: #F3F0FF;
        }
        .footer-brand-name span {
            background: linear-gradient(90deg, #F472B6, #DB2777);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .footer-links {
            display: flex;
            align-items: center;
            gap: 24px;
            flex-wrap: wrap;
        }
        .footer-links a {
            color: #9A8FC2;
            font-size: 13px;
            text-decoration: none;
            transition: color 0.15s ease;
        }
        .footer-links a:hover {
            color: #F9A8D4;
        }
        .footer-divider {
            width: 1px;
            height: 14px;
            background: rgba(236, 72, 153, 0.25);
        }

        /* ══════════════════════════════════════════════
           RESPONSIVE — MOBILE BREAKPOINTS
           ══════════════════════════════════════════════ */
        @media (max-width: 768px) {

            /* Hide the desktop logo/links/button row. Streamlit's raw-HTML
               `.navbar-wrap` open/close tags are separate sibling elements,
               NOT real DOM parents of the st.columns() row rendered between
               them — so a `.navbar-wrap > [data-testid="stHorizontalBlock"]`
               selector never matches anything. Target the keyed container's
               real, stable class instead (see _render_navbar()). */
            .st-key-navbar_desktop_row {
                display: none !important;
            }

            /* show the compact logo + hamburger bar */
            .navbar-mobile-bar {
                display: flex;
            }

            .nav-hamburger {
                display: flex;
            }

            .navbar-wrap {
                padding: 12px 16px;
            }

            /* Hero scales down */
            .landing-title {
                font-size: 32px;
                line-height: 1.15;
            }
            .landing-hero p.landing-subtitle {
                font-size: 15px;
            }
            .landing-badge {
                font-size: 11px;
                padding: 5px 14px;
            }
            .landing-hero {
                padding: 20px 16px 14px 16px;
            }

            /* Steps stack vertically */
            .landing-steps {
                flex-direction: column;
                gap: 16px;
                margin: 14px 0 28px 0;
            }

            /* Section headings */
            .section-heading {
                font-size: 22px;
                margin: 6px 0 20px 0;
            }

            /* Feature cards */
            .feature-card {
                padding: 20px 16px;
            }
            .feature-icon {
                font-size: 26px;
            }
            .feature-title {
                font-size: 15px;
            }
            .feature-desc {
                font-size: 13px;
            }

            /* Footer stacks vertically, centered */
            .footer-wrap {
                padding: 24px 16px 18px 16px;
                margin-top: 40px;
            }
            .footer-inner {
                flex-direction: column;
                align-items: center;
                text-align: center;
                gap: 18px;
            }
            .footer-brand-name {
                justify-content: center;
                font-size: 14px;
            }
            .footer-links {
                justify-content: center;
                gap: 6px;
                flex-wrap: wrap;
            }
            .footer-links a {
                font-size: 12.5px;
            }
            .footer-divider {
                display: none;
            }
            .footer-links a:not(:last-child)::after {
                content: " · ";
                color: rgba(236, 72, 153, 0.35);
                margin-left: 6px;
            }
        }

        @media (max-width: 400px) {
            .landing-title {
                font-size: 26px;
            }
            .landing-hero p.landing-subtitle {
                font-size: 14px;
            }
            .navbar-logo {
                font-size: 14px;
            }
        }
        </style>
        <div class="landing-glow"></div>
        <div id="top"></div>
        """,
        unsafe_allow_html=True,
    )


def _inject_landing_nav_js():
    """Hamburger toggle via event delegation — survives Streamlit re-renders."""

    components.html(
        """
        <script>
        (function () {
            try { var doc = window.parent.document; } catch(e) { return; }

            if (window.parent._navMobileBound) return;
            window.parent._navMobileBound = true;

            doc.addEventListener('click', function (e) {
                var hamburger = e.target.closest('.nav-hamburger');
                var menu = doc.querySelector('.nav-mobile-menu');

                if (hamburger) {
                    e.stopPropagation();
                    if (menu) menu.classList.toggle('open');
                    return;
                }

                if (e.target.closest('.nav-mobile-menu a')) {
                    if (menu) menu.classList.remove('open');
                    return;
                }

                if (menu && menu.classList.contains('open')) {
                    if (!e.target.closest('.nav-mobile-menu') && !e.target.closest('.nav-hamburger')) {
                        menu.classList.remove('open');
                    }
                }
            }, true);

            window.parent.addEventListener('resize', function () {
                if (window.parent.innerWidth > 768) {
                    var menu = doc.querySelector('.nav-mobile-menu');
                    if (menu) menu.classList.remove('open');
                }
            });
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def _launch_app():
    with st.spinner("🚀 Launching your workspace..."):
        time.sleep(0.4)

    st.session_state["show_landing"] = False
    st.query_params["app"] = "1"
    st.toast("Welcome to Raw2Ready AI!", icon="🚀")
    st.rerun()


def _render_navbar():
    """Desktop: Streamlit columns. Mobile: columns hidden, hamburger + dropdown shown."""

    nav_links_html = "".join(
        f'<a href="{href}">{label}</a>' for label, href in NAV_LINKS
    )

    mobile_links_html = "".join(
        f'<a href="{href}">{label}</a>' for label, href in NAV_LINKS
    )

    st.markdown('<div class="navbar-wrap">', unsafe_allow_html=True)

    # Compact mobile bar: logo + hamburger, hidden on desktop via CSS.
    # Rendered as a single raw-HTML block so the logo and hamburger are real
    # DOM siblings (unlike the desktop row below, which is built from
    # separate st.columns/st.button calls — see the CSS note on
    # .st-key-navbar_desktop_row for why that distinction matters here).
    st.markdown(
        f"""
        <div class="navbar-mobile-bar">
            <div class="navbar-logo">{LOGO_SVG}<span>Raw2Ready AI</span></div>
            <div class="nav-hamburger" id="navHamburger">
                <svg viewBox="0 0 24 24" fill="none" stroke="#F9A8D4"
                     stroke-width="2.2" stroke-linecap="round">
                    <line x1="4" y1="6" x2="20" y2="6"/>
                    <line x1="4" y1="12" x2="20" y2="12"/>
                    <line x1="4" y1="18" x2="20" y2="18"/>
                </svg>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Mobile dropdown menu (hidden on desktop via CSS, toggled by JS on mobile).
    # No CTA button here on purpose — the mobile Launch button lives only in
    # the hero section, not duplicated into this nav dropdown.
    st.markdown(
        f"""
        <div class="nav-mobile-menu" id="navMobileMenu">
            {mobile_links_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Desktop layout using Streamlit columns. Wrapped in a keyed container so
    # it gets a stable, real CSS class (`st-key-navbar_desktop_row`) that the
    # mobile media query can reliably target — st.markdown's raw
    # `.navbar-wrap` div does NOT actually become this row's DOM parent, so a
    # selector assuming that nesting silently matches nothing.
    with st.container(key="navbar_desktop_row"):
        left, center, right = st.columns([1.2, 3, 1], vertical_alignment="center")

        with left:
            st.markdown(
                f'<div class="navbar-logo">{LOGO_SVG}<span>Raw2Ready AI</span></div>',
                unsafe_allow_html=True,
            )

        with center:
            st.markdown(
                f'<div class="navbar-links">{nav_links_html}</div>',
                unsafe_allow_html=True,
            )

        with right:
            if st.button("🚀 Start Cleaning", key="navbar_launch", width="stretch", type="primary"):
                _launch_app()

    st.markdown("</div>", unsafe_allow_html=True)


def show_landing():
    """Render the fully responsive landing page."""

    # The CSS injection, the (invisible, height=0) nav-JS iframe, and the
    # navbar markup are each separate top-level elements in Streamlit's eyes,
    # so by default they'd each get its own flex "gap" from the surrounding
    # vertical block — dead space stacking up above the sticky navbar even
    # though none of them render a visible box. gap=None removes it.
    with st.container(gap=None):
        _inject_landing_css()
        _inject_landing_nav_js()
        _render_navbar()

    # ── HERO ──
    st.markdown(
        """
        <div class="landing-hero">
            <div class="landing-badge">✨ AI-POWERED DATA CLEANING</div>
            <div class="landing-title">Turn Messy Data into<br>Clean, Trusted Insights</div>
            <p class="landing-subtitle">
                Upload CSV, Excel, JSON or Parquet and let AI detect missing values,
                duplicates and outliers — then clean, visualize and export your dataset in minutes.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── CTA BUTTON ──
    st.markdown('<div id="get-started"></div>', unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1, 1])

    with mid:
        if st.button("🚀 Start Cleaning", key="hero_launch", width="stretch", type="primary"):
            _launch_app()

    st.markdown(
        """
        <div class="landing-steps">
            <div class="step-chip"><span class="step-num">1</span> Upload your dataset</div>
            <div class="step-chip"><span class="step-num">2</span> Let AI analyze &amp; clean it</div>
            <div class="step-chip"><span class="step-num">3</span> Download the clean version</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── WHY CHOOSE ──
    st.markdown('<div id="why-choose"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Why Choose Raw2Ready AI?</div>', unsafe_allow_html=True)

    left_col, mid_col, right_col = st.columns([1, 1, 1])

    with left_col:
        for num, title, desc in [WHY_ITEMS[0], WHY_ITEMS[2]]:
            st.markdown(
                f"""
                <div class="why-card">
                    <span class="why-num">{num}</span>
                    <div class="why-title">{title}</div>
                    <div class="why-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with mid_col:
        st.markdown(
            f'<div class="orb-wrap"><div class="orb-float" style="width:220px;">{ORB_SVG}</div></div>',
            unsafe_allow_html=True,
        )

    with right_col:
        for num, title, desc in [WHY_ITEMS[1], WHY_ITEMS[3]]:
            st.markdown(
                f"""
                <div class="why-card">
                    <span class="why-num">{num}</span>
                    <div class="why-title">{title}</div>
                    <div class="why-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ── FEATURE GRID ──
    st.markdown('<div id="features"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Everything You Need</div>', unsafe_allow_html=True)

    cols = st.columns(3)

    for i, (icon, title, desc) in enumerate(FEATURES):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)

    # ── MINIMAL FOOTER ──
    st.markdown(
        f"""
        <div class="footer-wrap">
            <div class="footer-inner">
                <div class="footer-brand-name">{LOGO_SVG}<span>Raw2Ready AI</span></div>
                <div class="footer-links">
                    <a href="#">Terms</a>
                    <div class="footer-divider"></div>
                    <a href="#">Privacy Policy</a>
                    <div class="footer-divider"></div>
                    <a href="#">Security</a>
                    <div class="footer-divider"></div>
                    <a href="#">General</a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )