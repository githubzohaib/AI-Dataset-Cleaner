import streamlit as st

from components.dataset_guard import get_dataset
from components.page_header import show_header
from components.download import download_buttons

from services.cleaning_service import CleaningService


def show_page():

    show_header(
        "⚙️ Cleaning Engine",
        "Automatically clean your dataset.",
    )

    df = get_dataset()

    strategy = st.selectbox(
        "Numerical Missing Value Strategy",
        ["Mean", "Median"],
    )

    remove_duplicates = st.checkbox(
        "Remove Duplicate Rows",
        value=True,
    )

    remove_outliers = st.checkbox(
        "Remove ML Outliers",
        value=True,
    )

    drop_columns = st.checkbox(
        "Drop Columns With Too Many Missing Values",
        value=False,
    )

    threshold = st.slider(
        "Missing Value Threshold (%)",
        10,
        90,
        60,
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🚀 Clean Dataset",
            width='stretch',
            type="primary",
        ):

            service = CleaningService()

            cleaned, report = service.clean(
                df,
                strategy,
                remove_duplicates,
                remove_outliers,
                drop_columns,
                threshold,
            )

            st.session_state["dataset"] = cleaned

            st.session_state["cleaning_report"] = report

            st.success("Dataset cleaned successfully!")

            st.rerun()

    with col2:

        if st.button(
            "♻ Reset Dataset",
            width='stretch',
        ):

            st.session_state["dataset"] = (
                st.session_state["original_dataset"].copy()
            )

            st.session_state["cleaning_report"] = []

            st.success("Dataset restored.")

            st.rerun()

    st.divider()

    st.subheader("Current Dataset")

    st.write(f"Rows : {df.shape[0]}")

    st.write(f"Columns : {df.shape[1]}")

    st.dataframe(
        df.head(),
        width='stretch',
    )

    if st.session_state["cleaning_report"]:

        st.divider()

        st.subheader("Cleaning Report")

        for item in st.session_state["cleaning_report"]:

            st.success(item)

        st.divider()

        st.subheader("⬇️ Download Cleaned Dataset")

        download_buttons(df, file_stem="cleaned_dataset")
