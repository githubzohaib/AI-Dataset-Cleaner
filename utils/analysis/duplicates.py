"""
Duplicate detection utilities.
"""

import pandas as pd


def duplicate_summary(df: pd.DataFrame):

    duplicate_rows = df[df.duplicated()]

    return {
        "count": duplicate_rows.shape[0],
        "percentage": round(
            duplicate_rows.shape[0] / len(df) * 100,
            2,
        ) if len(df) else 0,
        "rows": duplicate_rows,
    }


def remove_duplicates(df: pd.DataFrame):

    return df.drop_duplicates()
