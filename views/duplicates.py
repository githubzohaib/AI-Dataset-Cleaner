import streamlit as st

from components.dataset_guard import get_dataset
from components.page_header import show_header
from components.metric_cards import show_metrics
from components.tables import dataframe

from utils.analysis.duplicates import (
    duplicate_summary,
    remove_duplicates,
)


def show_page():

    show_header(
        "📋 Duplicate Analysis",
        "Detect and remove duplicate rows from the dataset.",
    )

    df = get_dataset()

    result = duplicate_summary(df)

    show_metrics([
        ("Duplicate Rows", result["count"]),
        ("Duplicate %", f"{result['percentage']}%"),
    ], columns=2)

    st.divider()

    if result["count"] == 0:

        st.success("✅ No duplicate rows found.")

        return

    dataframe(
        "Duplicate Rows",
        result["rows"],
    )

    if st.button(
        "🗑 Remove Duplicates",
        type="primary",
    ):

        cleaned_df = remove_duplicates(df)

        removed = len(df) - len(cleaned_df)

        st.session_state["dataset"] = cleaned_df

        st.session_state["cleaning_report"].append(
            f"Removed {removed} duplicate rows"
        )

        st.success(
            f"Removed {removed} duplicate rows."
        )

        st.rerun()
