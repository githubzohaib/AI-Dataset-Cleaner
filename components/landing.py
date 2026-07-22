import streamlit as st


FEATURES = [
    ("🕳️", "Smart Missing Values", "Detect gaps instantly and auto-fill with Mean, Median or Mode."),
    ("📋", "Duplicate Detection", "Find and remove duplicate rows in a single click."),
    ("🤖", "ML Outlier Detection", "Isolation Forest spots anomalies your eyes would miss."),
    ("📈", "Rich Visual Analytics", "Histograms, box plots, bar charts and correlation heatmaps."),
    ("💡", "AI Insights & Grading", "Get a quality score, letter grade, and plain-English recommendations."),
    ("⬇️", "One-Click Export", "Download your cleaned dataset as CSV or Excel, ready to use."),
]


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
            background: rgba(168, 85, 247, 0.12);
            border: 1px solid rgba(168, 85, 247, 0.4);
            color: #D8B4FE;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-bottom: 18px;
        }
        .landing-title {
            font-size: 56px;
            font-weight: 800;
            line-height: 1.1;
            background: linear-gradient(90deg, #F3F0FF 0%, #C084FC 45%, #7C3AED 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }
        .landing-subtitle {
            font-size: 19px;
            color: #C4B5FD;
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
            background: radial-gradient(circle, rgba(168,85,247,0.35) 0%, rgba(168,85,247,0) 70%);
            z-index: -1;
            pointer-events: none;
        }
        .feature-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(168, 85, 247, 0.22);
            border-radius: 18px;
            padding: 26px 22px;
            height: 100%;
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }
        .feature-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 14px 34px rgba(168, 85, 247, 0.3);
            border-color: rgba(196, 132, 252, 0.6);
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
            color: #D8B4FE;
            font-size: 14px;
            font-weight: 600;
        }
        .step-num {
            width: 26px;
            height: 26px;
            border-radius: 50%;
            background: linear-gradient(135deg, #7C3AED, #C084FC);
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
                Upload any CSV and let AI detect missing values, duplicates and outliers —
                then clean, visualize and export your dataset in minutes.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Centered CTA button ----
    _, mid, _ = st.columns([1, 1, 1])

    with mid:

        if st.button("🚀 Launch App", width='stretch', type="primary"):

            st.session_state["show_landing"] = False

            st.rerun()

    st.markdown(
        """
        <div class="landing-steps">
            <div class="step-chip"><span class="step-num">1</span> Upload your CSV</div>
            <div class="step-chip"><span class="step-num">2</span> Let AI analyze &amp; clean it</div>
            <div class="step-chip"><span class="step-num">3</span> Download the clean version</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

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