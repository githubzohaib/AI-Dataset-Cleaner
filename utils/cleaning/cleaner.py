"""
Cleaning utility functions.
"""

import warnings

import pandas as pd

# pandas' own dict-based fillna() implementation raises a spurious
# "ChainedAssignmentError" FutureWarning on every call in pandas 2.2+ — it
# fires even when using the exact non-chained, column-by-column pattern the
# warning itself recommends as the fix, so it's a false positive in pandas'
# internals rather than something callers can avoid. Confirmed the fill
# still applies correctly either way; this just keeps it out of logs.
# https://github.com/pandas-dev/pandas/issues/57734
_FILLNA_WARNING = ".*ChainedAssignmentError.*"


def fill_numeric(df: pd.DataFrame, strategy: str):

    numeric = df.select_dtypes(include="number").columns

    fill_values = {}

    for col in numeric:

        if strategy == "Mean":
            value = df[col].mean()

        else:
            value = df[col].median()

        fill_values[col] = value

    if fill_values:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message=_FILLNA_WARNING, category=FutureWarning)
            df = df.fillna(value=fill_values)

    return df


def fill_categorical(df: pd.DataFrame):

    categorical = df.select_dtypes(exclude="number").columns

    fill_values = {}

    for col in categorical:

        mode = df[col].mode()

        if not mode.empty:
            fill_values[col] = mode[0]

    if fill_values:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message=_FILLNA_WARNING, category=FutureWarning)
            df = df.fillna(value=fill_values)

    return df


def remove_duplicates(df: pd.DataFrame):

    before = len(df)

    df = df.drop_duplicates()

    removed = before - len(df)

    return df, removed


def drop_missing_columns(
    df: pd.DataFrame,
    threshold: float,
):

    percentages = (
        df.isnull().mean() * 100
    )

    columns = percentages[
        percentages > threshold
    ].index.tolist()

    df = df.drop(columns=columns)

    return df, columns