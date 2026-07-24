import time

import streamlit as st


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


def _inject_landing_css():

    st.markdown(
        """
        <style>
        .landing-hero {
            text-align: center;
            padding: 70px 20px 30px 20px;
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
            background: linear-gradient(90deg, #F3F0FF 0%, #F472B6 45%, #DB2777 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }
        .landing-subtitle {
            font-size: 19px;
            color: #F4A8CB;
            max-width: 650px;
            margin: 0 auto 10px auto;
            font-weight: 400;
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
        .feature-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(236, 72, 153, 0.22);
            border-radius: 18px;
            padding: 26px 22px;
            height: 100%;
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
        .landing-steps {
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
            margin: 10px 0 40px 0;
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
        .landing-footer {
            text-align: center;
            color: #7C6BA8;
            font-size: 13px;
            margin-top: 50px;
        }
        </style>
        <div class="landing-glow"></div>
        """,
        unsafe_allow_html=True,
    )


def show_landing():
    """Render the landing page. Sets session flag and reruns when user clicks Launch."""

    _inject_landing_css()

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

    # ---- Centered CTA button ----
    _, mid, _ = st.columns([1, 1, 1])

    with mid:

        if st.button("🚀 Launch App", width='stretch', type="primary"):

            with st.spinner("🚀 Launching your workspace..."):
                time.sleep(0.4)

            st.session_state["show_landing"] = False

            st.query_params["app"] = "1"

            st.toast("Welcome to AI Dataset Cleaner!", icon="🚀")

            st.rerun()

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

    # ---- Why Choose section: numbered offset cards + orb illustration ----
    left_col, mid_col, right_col = st.columns([1, 1, 1])

    with left_col:

        for num, title, desc in [WHY_ITEMS[0]]:
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

        st.markdown('<div class="why-col-offset">', unsafe_allow_html=True)

        for num, title, desc in [WHY_ITEMS[2]]:
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

        st.markdown("</div>", unsafe_allow_html=True)

    with mid_col:

        st.markdown(
            f"""
            <div class="orb-wrap">
                <div class="orb-float" style="width:220px;">{ORB_SVG}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right_col:

        st.markdown(
            """
            <div class="why-heading-wrap">
                <div class="why-heading">Why Choose<br>AI Dataset<br>Cleaner?</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for num, title, desc in [WHY_ITEMS[1]]:
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

        for num, title, desc in [WHY_ITEMS[3]]:
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

    # ---- Feature grid ----
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

    st.markdown(
        """
        <p class="landing-footer">🧠 AI Dataset Cleaner · Purple AI Edition · Made with 💜 using Streamlit</p>
        """,
        unsafe_allow_html=True,
    )