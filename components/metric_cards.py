import streamlit as st


def show_metrics(metrics: list[tuple[str, str | int | float]], columns: int = 4):
    """
    Display metrics in a responsive grid.

    Args:
        metrics: List of (label, value)
        columns: Number of columns per row
    """

    for i in range(0, len(metrics), columns):

        cols = st.columns(columns)

        row = metrics[i:i + columns]

        for col, (label, value) in zip(cols, row):
            col.metric(label, value)
