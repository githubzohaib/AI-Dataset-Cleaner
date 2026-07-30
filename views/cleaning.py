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

    # Each widget below is given a `key=` that matches an entry in
    # CLEANING_OPTION_DEFAULTS (utils/persistence.py), AND an explicit
    # `value=`/`index=` read from st.session_state (seeded by app.py before
    # this page ever runs). The explicit value isn't redundant: Streamlit
    # only pushes a session_state-restored value down to the *browser* when
    # it was assigned in the exact same script run that creates the widget.
    # Our seeding happens once, on the session's very first run — long
    # before the user ever navigates to this page — so by the time these
    # widgets are actually created for the first time in a real browser,
    # that "just changed" signal is gone and Streamlit would otherwise fall
    # back to each widget's hardcoded default (unchecked / slider minimum),
    # even though st.session_state already holds the restored value
    # internally. Passing the value explicitly closes that gap.
    strategy_options = ["Mean", "Median"]

    strategy = st.selectbox(
        "Numerical Missing Value Strategy",
        strategy_options,
        index=strategy_options.index(st.session_state["opt_numeric_strategy"]),
        key="opt_numeric_strategy",
    )

    remove_duplicates = st.checkbox(
        "Remove Duplicate Rows",
        value=st.session_state["opt_remove_duplicates"],
        key="opt_remove_duplicates",
    )

    remove_outliers = st.checkbox(
        "Remove ML Outliers",
        value=st.session_state["opt_remove_outliers"],
        key="opt_remove_outliers",
    )

    drop_columns = st.checkbox(
        "Drop Columns With Too Many Missing Values",
        value=st.session_state["opt_drop_columns"],
        key="opt_drop_columns",
    )

    threshold = st.slider(
        "Missing Value Threshold (%)",
        10,
        90,
        value=st.session_state["opt_missing_threshold"],
        key="opt_missing_threshold",
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