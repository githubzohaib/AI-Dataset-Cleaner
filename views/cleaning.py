import streamlit as st

from components.dataset_guard import get_dataset
from components.page_header import show_header
from components.download import download_buttons
from components.feedback import action_status

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

            with action_status("🧹 Cleaning your dataset...") as status:

                status.write("Analyzing missing values, duplicates and outliers...")

                service = CleaningService()

                cleaned, report = service.clean(
                    df,
                    strategy,
                    remove_duplicates,
                    remove_outliers,
                    drop_columns,
                    threshold,
                )

                for step in report:
                    status.write(f"✅ {step}")

                status.update(
                    label="✅ Cleaning complete!",
                    state="complete",
                    expanded=False,
                )

            st.session_state["dataset"] = cleaned

            # Append rather than overwrite: the Duplicates/Outliers pages append
            # their own manual actions to this same list, so overwriting here
            # would silently erase any history built up on those pages.
            st.session_state["cleaning_report"] = (
                st.session_state.get("cleaning_report", []) + report
            )

            st.toast("Dataset cleaned successfully!", icon="✅")

            st.success("Dataset cleaned successfully! Scroll down to download.")

            st.rerun()

    with col2:

        if st.button(
            "♻ Reset Dataset",
            width='stretch',
        ):

            with action_status("♻️ Restoring original dataset...") as status:

                st.session_state["dataset"] = (
                    st.session_state["original_dataset"].copy()
                )

                st.session_state["cleaning_report"] = []

                status.update(
                    label="✅ Dataset restored!",
                    state="complete",
                    expanded=False,
                )

            st.toast("Dataset restored to its original state", icon="♻️")

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