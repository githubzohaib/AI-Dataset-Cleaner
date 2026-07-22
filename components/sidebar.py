import streamlit as st

from utils.analysis.loader import load_dataset


PAGES = {
    "🏠 Dashboard": "home",
    "📊 Overview": "overview",
    "🔍 Explorer": "explorer",
    "🕳️ Missing Values": "missing",
    "📋 Duplicates": "duplicates",
    "🤖 ML Outliers": "outliers",
    "🧹 Cleaning": "cleaning",
    "📈 Analytics": "visualization",
    "💡 AI Insights": "insights",
    "⬇️ Export": "export",
}


def sidebar():

    st.sidebar.markdown(
        """
        <h2 class="gradient-text" style="margin-bottom:0;">🧠 AI Cleaner</h2>
        <p style="color:#A78BFA; font-size:13px; margin-top:-4px;">
            AI Powered Data Cleaning Platform
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.divider()

    uploaded = st.sidebar.file_uploader(
        "📂 Upload Dataset",
        type=["csv"],
    )

    if uploaded:

        df = load_dataset(uploaded)

        st.session_state["dataset"] = df

        if st.session_state["original_dataset"] is None:

            st.session_state["original_dataset"] = df.copy()

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        list(PAGES.keys()),
        label_visibility="collapsed",
    )

    st.sidebar.divider()

    if st.session_state.get("dataset") is not None:

        df = st.session_state["dataset"]

        st.sidebar.success("✅ Dataset Loaded")

        st.sidebar.markdown(
            f"""
            <span class="chip chip-purple">Rows: {len(df):,}</span>
            <span class="chip chip-purple">Cols: {df.shape[1]}</span>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.sidebar.info("No dataset loaded yet.")

    st.sidebar.divider()

    if st.sidebar.button("← Back to Landing", width='stretch'):

        st.session_state["show_landing"] = True

        st.rerun()

    st.sidebar.divider()

    st.sidebar.caption("Version 2.0 · Purple AI Edition")

    st.sidebar.caption("Made with 💜 using Streamlit")

    return PAGES[page]