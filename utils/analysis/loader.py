"""
Handles loading datasets from the common tabular file formats used in the
real world — not just CSV.
"""

import json
from typing import Optional

import pandas as pd

# Keep in sync with the `type=` list passed to st.file_uploader in
# components/sidebar.py.
SUPPORTED_EXTENSIONS = ["csv", "tsv", "txt", "xlsx", "xls", "xlsm", "json", "parquet"]


def _read_delimited(uploaded_file, sep) -> pd.DataFrame:
    """CSV/TSV/TXT share the same reader; `sep=None` auto-sniffs the
    delimiter (needed for .txt, which could be comma, tab, semicolon...)."""

    uploaded_file.seek(0)

    engine = "python" if sep is None else "c"

    try:
        return pd.read_csv(uploaded_file, sep=sep, engine=engine)

    except UnicodeDecodeError:

        uploaded_file.seek(0)

        return pd.read_csv(uploaded_file, sep=sep, engine=engine, encoding="latin-1")


def _read_excel(uploaded_file) -> pd.DataFrame:

    uploaded_file.seek(0)

    return pd.read_excel(uploaded_file)


def _read_json(uploaded_file) -> pd.DataFrame:

    uploaded_file.seek(0)

    try:
        return pd.read_json(uploaded_file)

    except ValueError:
        # Not a flat records/columns table pandas can parse directly (e.g.
        # a nested object) — fall back to a generic JSON-to-table flattener.
        uploaded_file.seek(0)

        try:
            payload = json.load(uploaded_file)
        except json.JSONDecodeError as exc:
            raise ValueError(f"This isn't valid JSON: {exc}") from exc

        return pd.json_normalize(payload)


def _read_parquet(uploaded_file) -> pd.DataFrame:

    uploaded_file.seek(0)

    return pd.read_parquet(uploaded_file)


_READERS = {
    "csv": lambda f: _read_delimited(f, sep=","),
    "tsv": lambda f: _read_delimited(f, sep="\t"),
    "txt": lambda f: _read_delimited(f, sep=None),
    "xlsx": _read_excel,
    "xls": _read_excel,
    "xlsm": _read_excel,
    "json": _read_json,
    "parquet": _read_parquet,
}


def load_dataset(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Load an uploaded file into a pandas DataFrame, auto-dispatching on its
    extension (csv, tsv, txt, xlsx, xls, xlsm, json, parquet).

    Args:
        uploaded_file: Uploaded file from Streamlit.

    Returns:
        DataFrame if successful, otherwise None.

    Raises:
        ValueError: If the file type is unsupported, or the file is empty,
            unreadable, or parses to zero columns/rows (e.g. wrong
            encoding, or a file mislabeled with the wrong extension).
    """

    if uploaded_file is None:
        return None

    name = uploaded_file.name.lower()

    extension = name.rsplit(".", 1)[-1] if "." in name else ""

    reader = _READERS.get(extension)

    if reader is None:
        raise ValueError(
            f"Unsupported file type '.{extension}'. Supported formats: "
            + ", ".join(SUPPORTED_EXTENSIONS)
        )

    try:
        df = reader(uploaded_file)

    except pd.errors.EmptyDataError as exc:
        raise ValueError("The uploaded file is empty.") from exc

    except UnicodeDecodeError as exc:
        raise ValueError(
            "Could not decode this file. Please upload a UTF-8 or "
            "Latin-1 encoded file."
        ) from exc

    except pd.errors.ParserError as exc:
        raise ValueError(
            f"This file doesn't look like a valid .{extension} file — it "
            "may be corrupted or mislabeled."
        ) from exc

    except ValueError:
        raise

    except Exception as exc:
        raise ValueError(f"Couldn't read this .{extension} file: {exc}") from exc

    if df.shape[1] == 0:
        raise ValueError("No columns could be parsed from this file.")

    if df.shape[0] == 0:
        raise ValueError("The uploaded file has no data rows.")

    return df
