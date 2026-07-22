"""
Cleaning utility functions.
"""

import pandas as pd


def fill_numeric(df: pd.DataFrame, strategy: str):

    numeric = df.select_dtypes(include="number").columns

    for col in numeric:

        if strategy == "Mean":
            value = df[col].mean()

        else:
            value = df[col].median()

        df[col] = df[col].fillna(value)

    return df


def fill_categorical(df: pd.DataFrame):

    categorical = df.select_dtypes(exclude="number").columns

    for col in categorical:

        if not df[col].mode().empty:

            df[col] = df[col].fillna(
                df[col].mode()[0]
            )

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
