"""
Missing value analysis utilities.
"""

import pandas as pd
import plotly.express as px


def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a summary of missing values.
    """

    summary = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values,
        "Missing Percentage":
            (df.isnull().mean() * 100).round(2).values
    })

    summary = summary.sort_values(
        by="Missing Percentage",
        ascending=False
    )

    return summary


def dataset_health_score(df: pd.DataFrame) -> float:
    """
    Calculate dataset health score.
    """

    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        return 100.0

    missing = df.isnull().sum().sum()

    score = ((total_cells - missing) / total_cells) * 100

    return round(score, 2)


def generate_recommendations(summary: pd.DataFrame):

    recommendations = []

    for _, row in summary.iterrows():

        percentage = row["Missing Percentage"]

        column = row["Column"]

        if percentage == 0:
            continue

        elif percentage > 70:

            recommendations.append(
                f"🔴 '{column}' has {percentage}% missing values. Consider dropping this column."
            )

        elif percentage > 30:

            recommendations.append(
                f"🟠 '{column}' has {percentage}% missing values. Consider advanced imputation."
            )

        else:

            recommendations.append(
                f"🟢 '{column}' has {percentage}% missing values. Mean/Mode imputation should work."
            )

    return recommendations


def missing_bar_chart(summary: pd.DataFrame):

    fig = px.bar(
        summary,
        x="Column",
        y="Missing Percentage",
        color="Missing Percentage",
        title="Missing Values (%)",
        text="Missing Percentage",
        color_continuous_scale=["#3B1D6E", "#A855F7", "#F0ABFC"],
    )

    fig.update_layout(
        xaxis_title="Columns",
        yaxis_title="Missing %",
    )

    return fig


def missing_heatmap(df: pd.DataFrame):

    fig = px.imshow(
        df.isnull(),
        aspect="auto",
        color_continuous_scale=["#171233", "#A855F7"],
        title="Missing Value Heatmap",
    )

    return fig
