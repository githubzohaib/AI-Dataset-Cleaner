import streamlit as st
import pandas as pd


def dataframe_explorer(df: pd.DataFrame):

    working_df = df.copy()

    st.subheader("🔍 Dataset Explorer")

    search = st.text_input(
        "Search across all columns",
        placeholder="Type to search...",
    )

    if search:

        mask = working_df.astype(str).apply(
            lambda col: col.str.contains(
                search,
                case=False,
                na=False,
            )
        ).any(axis=1)

        working_df = working_df[mask]

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        filter_column = st.selectbox(
            "Filter Column",
            ["None"] + list(working_df.columns),
        )

    with col2:

        rows = st.selectbox(
            "Rows to display",
            [10, 20, 50, 100],
            index=1,
        )

    if filter_column != "None":

        values = sorted(
            working_df[filter_column]
            .dropna()
            .unique(),
            key=lambda x: str(x),
        )

        value = st.selectbox(
            "Value",
            values,
        )

        working_df = working_df[
            working_df[filter_column] == value
        ]

    st.divider()

    col3, col4 = st.columns(2)

    with col3:

        sort_column = st.selectbox(
            "Sort By",
            working_df.columns,
        )

    with col4:

        ascending = st.checkbox(
            "Ascending",
            value=True,
        )

    working_df = working_df.sort_values(
        sort_column,
        ascending=ascending,
    )

    st.dataframe(
        working_df.head(rows),
        width='stretch',
        hide_index=True,
    )

    st.caption(
        f"Showing {min(rows, len(working_df))} of {len(working_df)} rows "
        f"(filtered from {len(df)} total)."
    )

    return working_df
