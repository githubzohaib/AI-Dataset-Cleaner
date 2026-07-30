"""
Local, session-scoped persistence for the uploaded dataset and the user's
cleaning preferences.

Streamlit wipes st.session_state on every browser refresh — it's a brand
new session with a blank slate. Without this module, refreshing the page
after uploading a file would silently drop it and force the user to
re-upload from scratch. Instead, state is cached to disk keyed by a
session id carried in the URL's query string (?sid=...), which *does*
survive a refresh (it's part of the URL, not session_state), and restored
from there automatically on the next run. The cache only goes away when
the user explicitly removes it, or a cache entry goes stale and gets swept.

Two separate files are used per session, not one combined blob:

- ``{sid}.pkl``          — the dataset(s) + cleaning report. Pickled because
  it holds DataFrames. Written only when the dataset itself changes (it can
  be tens of MB, so re-writing it on every widget tweak would be wasteful).
- ``{sid}.settings.json`` — small, JSON-serializable cleaning options
  (selectbox/checkbox/slider choices). Cheap enough to re-write on every
  rerun that changes them, independently of the dataset file.

AI insights, the quality score, and derived charts are deliberately NOT
stored here. They're pure functions of the dataset, so they're wrapped in
`st.cache_data` at their definition instead (see quality_score.py,
recommendation.py, outliers.py, etc.) — restoring the dataset after a
refresh and recomputing them is instant on a cache hit, and correct even on
a cache miss, without doubling up on serialized storage.

This is a single-machine, local-disk cache — fine for a self-hosted or
single-instance deployment. A multi-instance production deployment would
need to swap this for a shared store (e.g. Redis, S3) keyed the same way.
"""

import json
import pickle
import tempfile
import time
from pathlib import Path
from typing import Optional

CACHE_DIR = Path(tempfile.gettempdir()) / "raw2ready-ai-sessions"

MAX_AGE_SECONDS = 24 * 60 * 60

# Every user-selectable cleaning option that should survive a browser
# refresh, keyed by the exact `key=` each widget is given in
# views/cleaning.py, mapped to its default value. Centralized here so
# app.py (which restores them) and cleaning.py (which owns the widgets)
# never drift out of sync about which keys exist or what "fresh" means.
CLEANING_OPTION_DEFAULTS = {
    "opt_numeric_strategy": "Mean",
    "opt_remove_duplicates": True,
    "opt_remove_outliers": True,
    "opt_drop_columns": False,
    "opt_missing_threshold": 60,
}


def _path_for(session_id: str) -> Path:

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    return CACHE_DIR / f"{session_id}.pkl"


def _settings_path_for(session_id: str) -> Path:

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    return CACHE_DIR / f"{session_id}.settings.json"


def save_session(session_id, dataset, original_dataset, cleaning_report, source_name):
    """Persist the current dataset state to disk. Best-effort — a failed
    write shouldn't crash the app, it just means the refresh-persistence
    convenience won't work for this save."""

    if not session_id or dataset is None:
        return

    payload = {
        "dataset": dataset,
        "original_dataset": original_dataset,
        "cleaning_report": cleaning_report,
        "source_name": source_name,
        "saved_at": time.time(),
    }

    try:
        with open(_path_for(session_id), "wb") as f:
            pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)
    except OSError:
        pass


def load_session(session_id: str) -> Optional[dict]:
    """Return the cached {dataset, original_dataset, cleaning_report,
    source_name} dict for this session id, or None if nothing is cached."""

    if not session_id:
        return None

    path = _path_for(session_id)

    if not path.exists():
        return None

    try:
        with open(path, "rb") as f:
            return pickle.load(f)

    except Exception:
        # Corrupt or incompatible cache entry (e.g. pickled under a
        # different pandas version) — don't let it crash the app, just
        # treat it as if nothing was cached.
        path.unlink(missing_ok=True)
        return None


def delete_session(session_id: str):
    """Explicitly drop everything cached for this session id (dataset and
    cleaning options alike) — used by both "Remove Dataset" and "Start New
    Session"."""

    if not session_id:
        return

    _path_for(session_id).unlink(missing_ok=True)
    _settings_path_for(session_id).unlink(missing_ok=True)


def save_cleaning_options(session_id: str, options: dict):
    """Persist the user's cleaning-tab widget choices. Deliberately a tiny
    JSON file, separate from the (potentially large) dataset pickle, so it's
    cheap to rewrite on every rerun that changes a checkbox or slider."""

    if not session_id:
        return

    try:
        with open(_settings_path_for(session_id), "w", encoding="utf-8") as f:
            json.dump(options, f)
    except OSError:
        pass


def load_cleaning_options(session_id: str) -> dict:
    """Return the cached cleaning options for this session id, falling back
    to CLEANING_OPTION_DEFAULTS for any key that's missing or was never
    saved (fresh session, corrupt file, or an option added in a later
    release)."""

    options = dict(CLEANING_OPTION_DEFAULTS)

    if not session_id:
        return options

    path = _settings_path_for(session_id)

    if not path.exists():
        return options

    try:
        with open(path, "r", encoding="utf-8") as f:
            saved = json.load(f)

        options.update(
            {k: v for k, v in saved.items() if k in CLEANING_OPTION_DEFAULTS}
        )

    except Exception:
        # Corrupt or unreadable settings file — treat as if nothing was
        # cached rather than crashing the app.
        path.unlink(missing_ok=True)

    return options


def cleanup_stale_sessions(max_age_seconds: int = MAX_AGE_SECONDS):
    """Sweep cache entries older than `max_age_seconds` (default 24h) so
    abandoned browser tabs don't grow the cache directory forever."""

    if not CACHE_DIR.exists():
        return

    cutoff = time.time() - max_age_seconds

    for pattern in ("*.pkl", "*.settings.json"):
        for entry in CACHE_DIR.glob(pattern):
            try:
                if entry.stat().st_mtime < cutoff:
                    entry.unlink(missing_ok=True)
            except OSError:
                pass
