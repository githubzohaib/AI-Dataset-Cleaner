"""
Dataset overview utilities.
"""

import pandas as pd


def dataset_summary(df: pd.DataFrame) -> dict:
    """Return high-level dataset statistics."""

    numerical_cols = df.select_dtypes(include=["number"]).columns
    categorical_cols = df.select_dtypes(exclude=["number"]).columns

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1024**2, 2),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "numerical_columns": len(numerical_cols),
        "categorical_columns": len(categorical_cols),
    }


def column_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return information about every column."""

    summary = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values,
        "Missing %": (
            df.isnull().mean() * 100
        ).round(2).values,
        "Unique Values": df.nunique().values,
    })

    return summary
