"""
Local, session-scoped persistence for the uploaded dataset.

Streamlit wipes st.session_state on every browser refresh — it's a brand
new session with a blank slate. Without this module, refreshing the page
after uploading a file would silently drop it and force the user to
re-upload from scratch. Instead, the dataset is cached to disk keyed by a
session id carried in the URL's query string (?sid=...), which *does*
survive a refresh (it's part of the URL, not session_state), and restored
from there automatically on the next run. The dataset only goes away when
the user explicitly removes it, or a cache entry goes stale and gets swept.

This is a single-machine, local-disk cache — fine for a self-hosted or
single-instance deployment. A multi-instance production deployment would
need to swap this for a shared store (e.g. Redis, S3) keyed the same way.
"""

import pickle
import tempfile
import time
from pathlib import Path
from typing import Optional

CACHE_DIR = Path(tempfile.gettempdir()) / "raw2ready-ai-sessions"

MAX_AGE_SECONDS = 24 * 60 * 60


def _path_for(session_id: str) -> Path:

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    return CACHE_DIR / f"{session_id}.pkl"


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
    """Explicitly drop the cached dataset for this session id."""

    if not session_id:
        return

    _path_for(session_id).unlink(missing_ok=True)


def cleanup_stale_sessions(max_age_seconds: int = MAX_AGE_SECONDS):
    """Sweep cache entries older than `max_age_seconds` (default 24h) so
    abandoned browser tabs don't grow the cache directory forever."""

    if not CACHE_DIR.exists():
        return

    cutoff = time.time() - max_age_seconds

    for entry in CACHE_DIR.glob("*.pkl"):
        try:
            if entry.stat().st_mtime < cutoff:
                entry.unlink(missing_ok=True)
        except OSError:
            pass
