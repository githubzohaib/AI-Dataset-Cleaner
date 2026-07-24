"""
Machine Learning based outlier detection.
"""

import warnings

import pandas as pd

from sklearn.ensemble import IsolationForest


def detect_outliers(df: pd.DataFrame):
    """
    Detect outliers using Isolation Forest.
    """

    numeric_df = df.select_dtypes(include="number").copy()

    if numeric_df.empty or len(numeric_df) < 2:

        return {
            "count": 0,
            "percentage": 0,
            "rows": pd.DataFrame(),
            "mask": None,
            "features": [],
        }

    # See utils/cleaning/cleaner.py::_FILLNA_WARNING — pandas raises a
    # spurious ChainedAssignmentError FutureWarning on this call regardless
    # of assignment style; suppressing the known-benign warning only.
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message=".*ChainedAssignmentError.*", category=FutureWarning)
        for col in numeric_df.columns:
            numeric_df[col] = numeric_df[col].fillna(numeric_df[col].median())

    model = IsolationForest(

        contamination=0.05,

        random_state=42,
    )

    predictions = model.fit_predict(
        numeric_df
    )

    mask = predictions == -1

    outliers = df.loc[mask]

    return {

        "count": len(outliers),

        "percentage": round(

            len(outliers) / len(df) * 100,

            2,
        ) if len(df) else 0,

        "rows": outliers,

        "mask": mask,

        "features": numeric_df.columns.tolist(),
    }


def remove_outliers(
    df: pd.DataFrame,
    mask,
):

    if mask is None:
        return df

    return df.loc[~mask]
