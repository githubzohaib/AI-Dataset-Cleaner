"""
Cleaning utility functions.
"""

import pandas as pd


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