import streamlit as st

from components.dataset_guard import get_dataset
from components.page_header import show_header
from components.metric_cards import show_metrics
from components.tables import dataframe
from components.charts import plot

from utils.analysis.missing import (
    missing_summary,
    dataset_health_score,
    generate_recommendations,
    missing_bar_chart,
    missing_heatmap,
)


def show_page():

    show_header(
        "🕳️ Missing Value Analysis",
        "Analyze missing data patterns and receive AI-powered cleaning recommendations.",
    )

    df = get_dataset()

    summary = missing_summary(df)

    health = dataset_health_score(df)

    show_metrics([
        ("Dataset Health", f"{health}%"),
        ("Columns with Missing Data", int((summary["Missing Values"] > 0).sum())),
        ("Total Missing Values", int(summary["Missing Values"].sum())),
    ], columns=3)

    st.divider()

    dataframe(
        "Missing Value Summary",
        summary,
    )

    if summary["Missing Values"].sum() == 0:

        st.success("✅ No missing values detected in this dataset.")

        return

    st.subheader("📊 Missing Percentage by Column")

    plot(
        missing_bar_chart(summary)
    )

    st.subheader("🔥 Missing Value Heatmap")

    plot(
        missing_heatmap(df)
    )

    st.subheader("🤖 AI Cleaning Recommendations")

    recommendations = generate_recommendations(summary)

    if recommendations:

        for recommendation in recommendations:
            st.info(recommendation)

    else:

        st.success(
            "No missing values detected."
        )
