import pandas as pd

from utils.analysis.outliers import (
    detect_outliers,
)


def generate_ai_insights(df: pd.DataFrame):

    insights = []

    # -------------------------

    missing = (
        df.isnull().mean() * 100
    )

    for column, percentage in missing.items():

        if percentage > 70:

            insights.append(

                (
                    "error",

                    f"'{column}' has {percentage:.1f}% missing values. Consider removing it."
                )

            )

        elif percentage > 20:

            insights.append(

                (
                    "warning",

                    f"'{column}' has {percentage:.1f}% missing values. Median/Mode imputation is recommended."
                )

            )

    # -------------------------

    duplicates = df.duplicated().sum()

    if duplicates:

        insights.append(

            (
                "warning",

                f"{duplicates} duplicate rows detected."
            )

        )

    else:

        insights.append(

            (
                "success",

                "No duplicate rows detected."
            )

        )

    # -------------------------

    outliers = detect_outliers(df)

    if outliers["count"]:

        insights.append(

            (
                "warning",

                f"{outliers['count']} ML outliers detected."
            )

        )

    # -------------------------

    numeric = df.select_dtypes(
        include="number"
    )

    if len(numeric.columns) > 1:

        corr = numeric.corr().abs()

        highest = corr.where(
            corr < 1
        ).max().max()

        if pd.notna(highest) and highest > 0.8:

            insights.append(

                (
                    "info",

                    "Strong correlation detected between numerical variables."
                )

            )

    # -------------------------

    for column in df.select_dtypes(
        exclude="number"
    ).columns:

        value_counts = df[column].value_counts(normalize=True)

        if value_counts.empty:
            continue

        imbalance = value_counts.max()

        if imbalance > 0.90:

            insights.append(

                (
                    "warning",

                    f"'{column}' is highly imbalanced."
                )

            )

    insights.append(

        (
            "success",

            "Dataset is ready for machine learning after cleaning."
        )

    )

    return insights
