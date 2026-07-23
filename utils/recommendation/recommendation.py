import pandas as pd
from typing import List, Tuple, Dict, Optional
from utils.analysis.outliers import detect_outliers

# Define configurable thresholds
MISSING_VALUE_ERROR_THRESHOLD = 70  # percent missing to trigger error
MISSING_VALUE_WARNING_THRESHOLD = 20  # percent missing to trigger warning
DUPLICATE_ROWS_WARNING_THRESHOLD = 0  # any duplicate rows trigger warning
CORRELATION_THRESHOLD = 0.8  # high correlation threshold
IMBALANCE_THRESHOLD = 0.90  # feature imbalance threshold
TEMPORAL_DATA_MARKER = "date"
CATEGORICAL_DATA_MARKER = "category"

def generate_ai_insights(
    df: pd.DataFrame,
    missing_error_threshold: int = MISSING_VALUE_ERROR_THRESHOLD,
    missing_warning_threshold: int = MISSING_VALUE_WARNING_THRESHOLD,
    duplicate_warning_threshold: int = DUPLICATE_ROWS_WARNING_THRESHOLD,
    correlation_threshold: float = CORRELATION_THRESHOLD,
    imbalance_threshold: float = IMBALANCE_THRESHOLD
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
        List of (level, message) tuples where level can be "error", "warning", or "success".
    """

    insights: List[Tuple[str, str]] = []

    # -------------------------
    # 1. Missing Value Analysis
    # -------------------------
    missing_percentages = df.isnull().mean() * 100

    for column in df.columns:
        missing_pct = missing_percentages[column]

        # Error-level recommendation for high missingness
        if missing_pct > missing_error_threshold:
            insights.append((
                "error",
                f"'{column}' has {missing_pct:.1f}% missing values. Consider removing this column."
            ))

        # Warning-level recommendation for moderate missingness
        elif missing_pct > missing_warning_threshold:
            insights.append((
                "warning",
                f"'{column}' has {missing_pct:.1f}% missing values. Median/Mode imputation recommended."
            ))

        # Suggest appropriate imputation strategy
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
    duplicate_rows = df[df.duplicated()]
    duplicate_count = len(duplicate_rows)

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
    outlier_mask = outlier_result["mask"]
    outlier_features = outlier_result["features"]

    if outlier_count > 0:
        insights.append((
            "warning",
            f"{outlier_count} ML outliers detected."
        ))

        # Suggest impact assessment
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
        # Find the highest correlation between any two distinct features
        highest_corr = corr_matrix.where(
            lambda x: (x < 1) & (x > 0)
        ).max().max()
        if highest_corr > correlation_threshold:
            highly_corr_cols = [
                col for col in corr_matrix.columns
                if any(
                    (corr_matrix[col].loc[row] == highest_corr) and
                    (row != col) and
                    (corr_matrix.loc[row][col] == highest_corr)
                    for row in corr_matrix.index
                )
            ]
            col_names = ", ".join(highly_corr_cols) if highly_corr_cols else "some pair"
            insights.append((
                "info",
                f"Strong correlation ({highest_corr:.2f}) detected among {col_names}. "
                "Consider feature redundancy analysis."
            ))

    # -------------------------
    # 5. Categorical Imbalance Check
    # -------------------------
    categorical_df = df.select_dtypes(exclude="number")
    for col in categorical_df.columns:
        value_counts = categorical_df[col].value_counts(normalize=True)
        if len(value_counts) > 0:
            max_imbalance = value_counts.max()
            if max_imbalance > imbalance_threshold:
                insights.append((
                    "warning",
                    f"'{col}' is highly imbalanced (max category = {max_imbalance:.1%} of total). "
                    "Consider recoding or feature engineering."
                ))

    # -------------------------
    # 6. Temporal Data Check (optional)
    # -------------------------
    # Detect if any column looks like a date/time field
    datetime_candidates = [
        col for col in df.columns
        if "date" in col.lower() or "time" in col.lower()
    ]
    for col in datetime_candidates:
        if pd.api.types.is_datetime64_any_dtype(df[col]) or (
            pd.api.types.is_object_dtype(df[col]) and
            df[col].apply(lambda x: isinstance(x, (str, int, float))) and
            len(df[col].dropna()) > 0
        ):
            # Try to parse as datetime to validate
            try:
                pd.to_datetime(df[col], errors="coerce")
                insights.append((
                    "info",
                    f"Column '{col}' appears to contain date/time data. "
                    "Consider proper datetime parsing and extraction (year/season/month)."
                ))
            except Exception:
                pass  # Not parseable, but we still note the potential

    # -------------------------
    # 7. Final Assessment
    # -------------------------
    # Overall dataset readiness message
    insights.append((
        "success",
        "Dataset is ready for machine learning after cleaning."
    ))

    return insights