"""
Dataset Quality Score.
"""

import pandas as pd
import streamlit as st


# A pure function of the dataframe's content — caching means a browser
# refresh (which restores the same dataset from disk) or navigating back to
# this page recomputes nothing; Streamlit hits the cache instead of
# re-scanning every cell.
@st.cache_data(show_spinner=False)
def calculate_quality_score(df: pd.DataFrame):

    score = 100

    total_missing = (
        df.isnull()
        .sum()
        .sum()
    )

    duplicate_rows = df.duplicated().sum()

    total_cells = df.shape[0] * df.shape[1]

    missing_ratio = (
        total_missing / total_cells * 100
    ) if total_cells else 0

    score -= missing_ratio

    score -= duplicate_rows * 0.5

    score = max(0, round(score, 2))

    if score >= 90:

        grade = "A"

    elif score >= 80:

        grade = "B"

    elif score >= 70:

        grade = "C"

    elif score >= 60:

        grade = "D"

    else:

        grade = "F"

    return score, grade
