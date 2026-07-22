"""
Visualization utilities.
"""

import pandas as pd
import plotly.express as px

PURPLE_SCALE = ["#3B1D6E", "#6D28D9", "#A855F7", "#D8B4FE", "#F5D0FE"]


def histogram(df, column):

    return px.histogram(
        df,
        x=column,
        title=f"{column} Distribution",
        marginal="box",
        color_discrete_sequence=["#A855F7"],
    )


def box_plot(df, column):

    return px.box(
        df,
        y=column,
        title=f"{column} Box Plot",
        color_discrete_sequence=["#C084FC"],
    )


def bar_chart(df, column):

    counts = (
        df[column]
        .value_counts()
        .reset_index()
    )

    counts.columns = [column, "Count"]

    return px.bar(
        counts,
        x=column,
        y="Count",
        title=f"{column} Distribution",
        color="Count",
        color_continuous_scale=PURPLE_SCALE,
    )


def correlation_heatmap(df):

    numeric = df.select_dtypes(include="number")

    corr = numeric.corr()

    return px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap",
        color_continuous_scale=PURPLE_SCALE,
    )
