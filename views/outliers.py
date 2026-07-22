import streamlit as st

from components.dataset_guard import get_dataset
from components.page_header import show_header
from components.metric_cards import show_metrics
from components.tables import dataframe

from utils.analysis.outliers import (
    detect_outliers,
    remove_outliers,
)


def show_page():

    show_header(
        "🤖 ML Outlier Detection",
        "Detect anomalies using Isolation Forest (unsupervised machine learning).",
    )

    df = get_dataset()

    result = detect_outliers(df)

    show_metrics([
        ("Outliers", result["count"]),
        ("Percentage", f"{result['percentage']}%"),
    ], columns=2)

    st.divider()

    if not result["features"]:

        st.info("No numerical columns available for outlier detection.")

        return

    st.subheader("Features Used for Detection")

    st.write(result["features"])

    st.divider()

    if result["count"] == 0:

        st.success("✅ No outliers detected.")

        return

    dataframe(
        "Detected Outliers",
        result["rows"],
    )

    if st.button(
        "🚮 Remove Outliers",
        type="primary",
    ):

        cleaned = remove_outliers(
            df,
            result["mask"],
        )

        removed = len(df) - len(cleaned)

        st.session_state["dataset"] = cleaned

        st.session_state["cleaning_report"].append(
            f"Removed {removed} outliers using Isolation Forest"
        )

        st.success(
            f"{removed} outliers removed."
        )

        st.rerun()
