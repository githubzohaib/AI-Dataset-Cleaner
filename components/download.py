import io

import pandas as pd
import streamlit as st


def to_csv_bytes(df: pd.DataFrame) -> bytes:

    return df.to_csv(index=False).encode("utf-8")


def to_excel_bytes(df: pd.DataFrame) -> bytes:

    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Cleaned Data")

    return buffer.getvalue()


def _toast_csv():
    st.toast("CSV download started", icon="⬇️")


def _toast_excel():
    st.toast("Excel download started", icon="⬇️")


def download_buttons(df: pd.DataFrame, file_stem: str = "cleaned_dataset"):
    """Render CSV + Excel download buttons side by side for a dataframe."""

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="⬇️ Download as CSV",
            # A callable defers the actual CSV encoding until the button is
            # clicked (and runs off the main script thread), instead of
            # re-encoding the whole dataframe on every single page rerun.
            data=lambda: to_csv_bytes(df),
            file_name=f"{file_stem}.csv",
            mime="text/csv",
            width='stretch',
            on_click=_toast_csv,
        )

    with col2:

        st.download_button(
            label="⬇️ Download as Excel",
            data=lambda: to_excel_bytes(df),
            file_name=f"{file_stem}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width='stretch',
            on_click=_toast_excel,
        )
