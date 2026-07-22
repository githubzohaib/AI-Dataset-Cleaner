import streamlit as st

from components.dataset_guard import get_dataset
from components.page_header import show_header
from components.metric_cards import show_metrics
from components.tables import dataframe

from utils.analysis.overview import (
    dataset_summary,
    column_summary,
)


def show_page():

    show_header(
        "📊 Dataset Overview",
        "High-level summary of the uploaded dataset.",
    )

    df = get_dataset()

    summary = dataset_summary(df)

    show_metrics([
        ("Rows", summary["rows"]),
        ("Columns", summary["columns"]),
        ("Missing Values", summary["missing_values"]),
        ("Duplicates", summary["duplicate_rows"]),
    ])

    show_metrics([
        ("Numerical", summary["numerical_columns"]),
        ("Categorical", summary["categorical_columns"]),
        ("Memory (MB)", summary["memory_mb"]),
    ], columns=3)

    st.divider()

    with st.expander("Dataset Preview", expanded=True):

        dataframe(
            "First 20 Rows",
            df.head(20),
        )

    with st.expander("Column Information", expanded=True):

        dataframe(
            "Column Summary",
            column_summary(df),
        )

    with st.expander("Numerical Statistics"):

        dataframe(
            "Descriptive Statistics",
            df.describe(),
        )

    with st.expander("Categorical Statistics"):

        categorical_df = df.describe(include="object")

        if categorical_df.empty:
            st.info("No categorical columns found.")
        else:
            dataframe(
                "Categorical Summary",
                categorical_df,
            )
