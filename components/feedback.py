"""
Shared UI feedback helper for buttons that mutate the dataset.
"""

import time
from contextlib import contextmanager

import streamlit as st


@contextmanager
def action_status(working_label: str, min_duration: float = 0.45):
    """
    Wrap a mutating button action in a themed st.status block.

    Guarantees the spinner stays visible for at least `min_duration` seconds
    even if the underlying pandas operation finishes instantly, so fast
    actions (e.g. dropping a handful of rows) still visibly register as
    "work happened" instead of flashing by unnoticed. The caller is
    responsible for calling `status.update(label=..., state="complete", ...)`
    on the yielded status before the block ends.
    """

    start = time.time()

    with st.status(working_label, expanded=True) as status:

        yield status

        elapsed = time.time() - start

        if elapsed < min_duration:
            time.sleep(min_duration - elapsed)
