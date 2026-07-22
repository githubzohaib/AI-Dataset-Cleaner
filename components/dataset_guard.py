import streamlit as st


def get_dataset():
    """
    Return the uploaded dataset.

    Stops execution if no dataset exists.
    """

    if (
        "dataset" not in st.session_state
        or st.session_state["dataset"] is None
    ):

        st.warning(
            "⚠️ Please upload a dataset from the sidebar first."
        )

        st.stop()

    return st.session_state["dataset"]
