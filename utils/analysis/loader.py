"""
Handles loading datasets.
"""

from typing import Optional

import pandas as pd


def load_dataset(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a pandas DataFrame.

    Args:
        uploaded_file: Uploaded file from Streamlit.

    Returns:
        DataFrame if successful, otherwise None.
    """

    if uploaded_file is None:
        return None

    return pd.read_csv(uploaded_file)
