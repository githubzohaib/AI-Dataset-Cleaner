import streamlit as st

from components.brand import logo_svg
from components.cards import card
from components.dataset_guard import get_dataset


def show_home():

    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:12px;">
            {logo_svg('home', size=40)}
            <h1 class="gradient-text" style="margin:0;">Raw2Ready AI</h1>
        </div>
        <p style="color:#F4A8CB; font-size:16px; margin-top:6px;">
            AI-Powered Dataset Cleaning &amp; Preprocessing Platform
        </p>
        """,
        unsafe_allow_html=True,
    )

    if (
        "dataset" not in st.session_state
        or st.session_state["dataset"] is None
    ):
        st.info("📂 Upload a dataset (CSV, Excel, JSON, Parquet...) from the sidebar to begin.")
        return

    df = get_dataset()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        card("Rows", f"{len(df):,}", icon="📄")

    with col2:
        card("Columns", df.shape[1], icon="📊")

    with col3:
        card("Missing", f"{int(df.isnull().sum().sum()):,}", icon="🕳️")

    with col4:
        card("Duplicates", f"{int(df.duplicated().sum()):,}", icon="📎")

    st.divider()

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(),
        width='stretch',
    )