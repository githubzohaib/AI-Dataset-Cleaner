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
        <p style="color:#F4A8CB; font-size:13px; margin-top:-4px;">
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

    if uploaded is not None:

        # Streamlit's file_uploader keeps returning the SAME file object on every
        # rerun (button clicks, checkbox toggles, st.rerun() after cleaning, etc.),
        # not just the moment it's uploaded. Without this guard, every rerun would
        # silently reload the original file and wipe out any cleaning that was
        # just applied. We only (re)load when the file is actually new.
        file_fingerprint = f"{uploaded.name}_{uploaded.size}"

        if st.session_state.get("uploaded_file_fingerprint") != file_fingerprint:

            df = load_dataset(uploaded)

            st.session_state["dataset"] = df

            st.session_state["original_dataset"] = df.copy()

            st.session_state["cleaning_report"] = []

            st.session_state["uploaded_file_fingerprint"] = file_fingerprint

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
            <span class="chip chip-pink">Rows: {len(df):,}</span>
            <span class="chip chip-pink">Cols: {df.shape[1]}</span>
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