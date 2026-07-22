import streamlit as st

from components.dataset_guard import get_dataset
from components.page_header import show_header
from components.metric_cards import show_metrics
from components.download import download_buttons


def show_page():

    show_header(
        "⬇️ Export Cleaned Dataset",
        "Review your changes and download the final dataset.",
    )

    df = get_dataset()

    original = st.session_state.get("original_dataset")

    st.subheader("Before vs After")

    if original is not None:

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("**Original Dataset**")

            show_metrics([
                ("Rows", len(original)),
                ("Columns", original.shape[1]),
                ("Missing", int(original.isnull().sum().sum())),
                ("Duplicates", int(original.duplicated().sum())),
            ], columns=2)

        with col2:

            st.markdown("**Current (Cleaned) Dataset**")

            show_metrics([
                ("Rows", len(df)),
                ("Columns", df.shape[1]),
                ("Missing", int(df.isnull().sum().sum())),
                ("Duplicates", int(df.duplicated().sum())),
            ], columns=2)

    st.divider()

    if st.session_state.get("cleaning_report"):

        st.subheader("Cleaning Steps Applied")

        for item in st.session_state["cleaning_report"]:

            st.write("✅", item)

        st.divider()

    else:

        st.info(
            "No cleaning steps have been applied yet. "
            "You can still download the dataset as-is, or visit the "
            "Cleaning page first."
        )

    st.subheader("Preview")

    st.dataframe(
        df.head(20),
        width='stretch',
        hide_index=True,
    )

    st.divider()

    st.subheader("⬇️ Download")

    download_buttons(df, file_stem="cleaned_dataset")
