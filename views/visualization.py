import streamlit as st

from components.dataset_guard import get_dataset
from components.page_header import show_header

from components.charts import plot

from utils.visualization.charts import (
    histogram,
    box_plot,
    bar_chart,
    correlation_heatmap,
)


def show_page():

    show_header(
        "📈 Data Visualization",
        "Explore your dataset visually.",
    )

    df = get_dataset()

    tabs = st.tabs(
        [
            "Dataset",
            "Numerical",
            "Categorical",
            "Correlation",
        ]
    )

    # -----------------------------------

    with tabs[0]:

        st.subheader("Dataset Preview")

        st.dataframe(
            df.head(20),
            width='stretch',
        )

    # -----------------------------------

    with tabs[1]:

        numeric = list(
            df.select_dtypes(include="number").columns
        )

        if numeric:

            column = st.selectbox(
                "Select Numerical Column",
                numeric,
            )

            plot(histogram(df, column))

            plot(box_plot(df, column))

        else:

            st.info("No numerical columns found.")

    # -----------------------------------

    with tabs[2]:

        categorical = list(
            df.select_dtypes(exclude="number").columns
        )

        if categorical:

            column = st.selectbox(
                "Select Category",
                categorical,
            )

            plot(bar_chart(df, column))

        else:

            st.info("No categorical columns found.")

    # -----------------------------------

    with tabs[3]:

        numeric = df.select_dtypes(include="number")

        if numeric.shape[1] >= 2:

            plot(correlation_heatmap(df))

        else:

            st.info("Need at least two numerical columns for a correlation heatmap.")
