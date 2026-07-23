import pandas as pd
from typing import List, Tuple

from utils.analysis.outliers import detect_outliers

# Configurable thresholds
MISSING_VALUE_ERROR_THRESHOLD = 70      # percent missing to trigger error
MISSING_VALUE_WARNING_THRESHOLD = 20    # percent missing to trigger warning
DUPLICATE_ROWS_WARNING_THRESHOLD = 0    # any duplicate rows trigger warning
CORRELATION_THRESHOLD = 0.8             # high correlation threshold
IMBALANCE_THRESHOLD = 0.90              # feature imbalance threshold
DATETIME_PARSE_SUCCESS_THRESHOLD = 0.8  # % of values that must parse as dates to flag a column


def generate_ai_insights(
    df: pd.DataFrame,
    missing_error_threshold: int = MISSING_VALUE_ERROR_THRESHOLD,
    missing_warning_threshold: int = MISSING_VALUE_WARNING_THRESHOLD,
    duplicate_warning_threshold: int = DUPLICATE_ROWS_WARNING_THRESHOLD,
    correlation_threshold: float = CORRELATION_THRESHOLD,
    imbalance_threshold: float = IMBALANCE_THRESHOLD,
) -> List[Tuple[str, str]]:
    """
    Generate AI-powered insights and recommendations for dataset cleaning.

    Args:
        df: Input DataFrame to analyze.
        missing_error_threshold: Percent missing values that triggers an error.
        missing_warning_threshold: Percent missing values that triggers a warning.
        duplicate_warning_threshold: Number of duplicate rows that triggers a warning.
        correlation_threshold: Correlation strength to trigger a correlation note.
        imbalance_threshold: Imbalance ratio to trigger a warning.

    Returns:
        List of (level, message) tuples where level is "error", "warning", "info", or "success".
    """

    insights: List[Tuple[str, str]] = []

    # -------------------------
    # 1. Missing Value Analysis
    # -------------------------
    missing_percentages = df.isnull().mean() * 100

    for column in df.columns:

        missing_pct = missing_percentages[column]

        if missing_pct > missing_error_threshold:

            insights.append((
                "error",
                f"'{column}' has {missing_pct:.1f}% missing values. Consider removing this column."
            ))

        elif missing_pct > missing_warning_threshold:

            insights.append((
                "warning",
                f"'{column}' has {missing_pct:.1f}% missing values. Median/Mode imputation recommended."
            ))

        if missing_pct > 0:

            if pd.api.types.is_numeric_dtype(df[column]):
                suggested_impute = "Mean/Median imputation for numeric column"
            else:
                suggested_impute = "Mode imputation for categorical column"

            insights.append((
                "info",
                f"'{column}' has missing data. Consider {suggested_impute}."
            ))

    # -------------------------
    # 2. Duplicate Row Detection
    # -------------------------
    duplicate_count = int(df.duplicated().sum())

    if duplicate_count > duplicate_warning_threshold:

        insights.append((
            "warning",
            f"{duplicate_count} duplicate rows detected."
        ))

    else:

        insights.append((
            "success",
            "No duplicate rows detected."
        ))

    # -------------------------
    # 3. Outlier Detection
    # -------------------------
    outlier_result = detect_outliers(df)
    outlier_count = outlier_result["count"]
    outlier_percentage = outlier_result["percentage"]

    if outlier_count > 0:

        insights.append((
            "warning",
            f"{outlier_count} ML outliers detected."
        ))

        insights.append((
            "info",
            f"Outliers represent {outlier_percentage:.1f}% of the dataset. Verify if removal is appropriate."
        ))

    # -------------------------
    # 4. Correlation Analysis
    # -------------------------
    numeric_df = df.select_dtypes(include="number")

    if len(numeric_df.columns) > 1:

        corr_matrix = numeric_df.corr().abs()

        # Mask the diagonal (self-correlation == 1) and exact-zero entries
        masked = corr_matrix.where((corr_matrix < 1) & (corr_matrix > 0))

        highest_corr = masked.max().max()

        if pd.notna(highest_corr) and highest_corr > correlation_threshold:

            # Find one representative pair that hits the highest correlation
            pair = None

            for row in masked.index:
                for col in masked.columns:
                    if row != col and masked.loc[row, col] == highest_corr:
                        pair = (row, col)
                        break
                if pair:
                    break

            col_names = ", ".join(pair) if pair else "some pair of columns"

            insights.append((
                "info",
                f"Strong correlation ({highest_corr:.2f}) detected between {col_names}. "
                "Consider feature redundancy analysis."
            ))

    # -------------------------
    # 5. Categorical Imbalance Check
    # -------------------------
    categorical_df = df.select_dtypes(exclude="number")

    for col in categorical_df.columns:

        value_counts = categorical_df[col].value_counts(normalize=True)

        if value_counts.empty:
            continue

        max_imbalance = value_counts.max()

        if max_imbalance > imbalance_threshold:

            insights.append((
                "warning",
                f"'{col}' is highly imbalanced (top category = {max_imbalance:.1%} of total). "
                "Consider recoding or feature engineering."
            ))

    # -------------------------
    # 6. Temporal Data Check (optional)
    # -------------------------
    datetime_candidates = [
        col for col in df.columns
        if "date" in col.lower() or "time" in col.lower()
    ]

    for col in datetime_candidates:

        if pd.api.types.is_datetime64_any_dtype(df[col]):

            insights.append((
                "info",
                f"Column '{col}' appears to contain date/time data. "
                "Consider extracting year/month/day features."
            ))

            continue

        # Object / string columns: try parsing and only flag if it's mostly real dates.
        # (Avoids the ambiguous-truth-value crash of calling bool() on a Series,
        # and avoids false positives on columns that just happen to have "date"/"time"
        # in the name but aren't actually date-like.)
        if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col]):

            non_null = df[col].dropna()

            if len(non_null) == 0:
                continue

            try:
                parsed = pd.to_datetime(non_null, errors="coerce", format="mixed")
            except TypeError:
                # older pandas versions (<2.0) don't support format="mixed"
                parsed = pd.to_datetime(non_null, errors="coerce")

            parse_success_rate = parsed.notna().mean()

            if parse_success_rate > DATETIME_PARSE_SUCCESS_THRESHOLD:

                insights.append((
                    "info",
                    f"Column '{col}' appears to contain date/time data. "
                    "Consider proper datetime parsing and extraction (year/season/month)."
                ))

    # -------------------------
    # 7. Final Assessment
    # -------------------------
    insights.append((
        "success",
        "Dataset is ready for machine learning after cleaning."
    ))

    return insights