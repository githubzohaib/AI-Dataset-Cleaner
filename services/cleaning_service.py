from utils.cleaning.cleaner import (
    fill_numeric,
    fill_categorical,
    remove_duplicates,
    drop_missing_columns,
)

from utils.analysis.outliers import (
    detect_outliers,
    remove_outliers,
)


class CleaningService:

    def clean(
        self,
        df,
        numeric_strategy,
        remove_duplicate_rows,
        remove_ml_outliers,
        drop_columns,
        threshold,
    ):

        report = []

        cleaned = df.copy()

        cleaned = fill_numeric(
            cleaned,
            numeric_strategy,
        )

        report.append(
            f"Filled numerical values using {numeric_strategy}"
        )

        cleaned = fill_categorical(cleaned)

        report.append(
            "Filled categorical values using Mode"
        )

        if remove_duplicate_rows:

            cleaned, removed = remove_duplicates(cleaned)

            report.append(
                f"Removed {removed} duplicate rows"
            )

        if remove_ml_outliers:

            result = detect_outliers(cleaned)

            if result["mask"] is not None:

                cleaned = remove_outliers(
                    cleaned,
                    result["mask"],
                )

                report.append(
                    f"Removed {result['count']} outliers"
                )

        if drop_columns:

            cleaned, columns = drop_missing_columns(
                cleaned,
                threshold,
            )

            report.append(
                f"Dropped columns: {columns}"
            )

        return cleaned, report
