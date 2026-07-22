import streamlit as st

from components.dataset_guard import get_dataset
from components.metric_cards import show_metrics
from components.page_header import show_header

from utils.recommendation.quality_score import (
    calculate_quality_score,
)

from utils.recommendation.recommendation import (
    generate_ai_insights,
)


def show_page():

    show_header(
        "💡 AI Dataset Insights",
        "AI-powered interpretation of dataset quality.",
    )

    df = get_dataset()

    score, grade = calculate_quality_score(df)

    show_metrics([
        ("Quality Score", f"{score}%"),
        ("Grade", grade),
    ], columns=2)

    st.divider()

    st.subheader("AI Recommendations")

    insights = generate_ai_insights(df)

    for level, message in insights:

        if level == "success":

            st.success(message)

        elif level == "warning":

            st.warning(message)

        elif level == "error":

            st.error(message)

        else:

            st.info(message)

    if st.session_state["cleaning_report"]:

        st.divider()

        st.subheader("Cleaning History")

        for item in st.session_state["cleaning_report"]:

            st.write("✅", item)
