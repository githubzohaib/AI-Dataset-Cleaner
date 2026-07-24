import streamlit as st

from utils.analysis.loader import load_dataset, SUPPORTED_EXTENSIONS
from utils.persistence import delete_session


PAGES = {
    "🏠 Dashboard": "home",
    "📊 Overview": "overview",
    "🔍 Explorer": "explorer",
    "🕳️ Missing Values": "missing",
    "📋 Duplicates": "duplicates",
    "🤖 ML Outliers": "outliers",
    "🧹 Cleaning": "cleaning",
    "📈 Analytics": "visualization",
    "💡 AI Insights": "insights",
    "⬇️ Export": "export",
}


def sidebar():

    st.sidebar.markdown(
        """
        <h2 class="gradient-text" style="margin-bottom:0;">🧠 AI Cleaner</h2>
        <p style="color:#F4A8CB; font-size:13px; margin-top:-4px;">
            AI Powered Data Cleaning Platform
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.divider()

    # A dynamic key lets the "Remove Dataset" button force this widget back
    # to its empty state (bumping the version makes Streamlit treat it as a
    # brand-new widget) — otherwise the picker would keep showing the old
    # filename even after the dataset behind it was cleared.
    uploader_version = st.session_state.get("uploader_version", 0)

    uploaded = st.sidebar.file_uploader(
        "📂 Upload Dataset",
        type=SUPPORTED_EXTENSIONS,
        help="Supports CSV, TSV, TXT, Excel (.xlsx/.xls/.xlsm), JSON and Parquet.",
        key=f"file_uploader_{uploader_version}",
    )

    if uploaded is not None:

        # Streamlit's file_uploader keeps returning the SAME file object on every
        # rerun (button clicks, checkbox toggles, st.rerun() after cleaning, etc.),
        # not just the moment it's uploaded. Without this guard, every rerun would
        # silently reload the original file and wipe out any cleaning that was
        # just applied. We only (re)load when the file is actually new — `file_id`
        # is assigned per upload action, so it changes even if the user re-uploads
        # a same-named, same-sized file after editing it (name+size would miss that).
        file_fingerprint = uploaded.file_id

        if st.session_state.get("uploaded_file_fingerprint") != file_fingerprint:

            with st.sidebar.status("📂 Loading dataset...", expanded=True) as status:

                status.write(f"Reading `{uploaded.name}`...")

                try:
                    df = load_dataset(uploaded)

                except ValueError as exc:

                    status.update(
                        label="❌ Upload failed",
                        state="error",
                        expanded=True,
                    )

                    st.sidebar.error(f"⚠️ Couldn't load this file: {exc}")

                    # Don't retry-load this same broken file on every rerun.
                    st.session_state["uploaded_file_fingerprint"] = file_fingerprint

                else:

                    status.write(f"Parsed {len(df):,} rows × {df.shape[1]} columns.")

                    status.update(
                        label="✅ Dataset loaded!",
                        state="complete",
                        expanded=False,
                    )

                    st.session_state["dataset"] = df

                    st.session_state["original_dataset"] = df.copy()

                    st.session_state["cleaning_report"] = []

                    st.session_state["uploaded_file_fingerprint"] = file_fingerprint

                    st.session_state["uploaded_file_name"] = uploaded.name

                    # A brand-new file can coincidentally reuse the same row
                    # labels (e.g. both start at 0..N-1) as whatever was
                    # scanned before, which would otherwise make stale
                    # flagged-outlier indices appear to "match" unrelated
                    # rows in the new dataset.
                    st.session_state.pop("outlier_scan_result", None)

                    st.toast(
                        f"Loaded {len(df):,} rows × {df.shape[1]} columns",
                        icon="✅",
                    )

    st.sidebar.divider()

    page_labels = list(PAGES.keys())

    # Restore the last-visited page from the URL so a browser refresh keeps
    # the user where they were instead of snapping back to the Dashboard.
    # (Only affects the widget's initial value — once the radio has been
    # interacted with in this session, Streamlit's own widget state takes
    # over and this index is ignored, which is what we want.)
    remembered_page = st.query_params.get("page", "home")

    default_index = next(
        (i for i, label in enumerate(page_labels) if PAGES[label] == remembered_page),
        0,
    )

    page = st.sidebar.radio(
        "Navigation",
        page_labels,
        index=default_index,
        label_visibility="collapsed",
    )

    st.query_params["page"] = PAGES[page]

    st.sidebar.divider()

    if st.session_state.get("dataset") is not None:

        df = st.session_state["dataset"]

        source_name = st.session_state.get("uploaded_file_name")

        st.sidebar.success(f"✅ Dataset Loaded{f' — {source_name}' if source_name else ''}")

        st.sidebar.markdown(
            f"""
            <span class="chip chip-pink">Rows: {len(df):,}</span>
            <span class="chip chip-pink">Cols: {df.shape[1]}</span>
            """,
            unsafe_allow_html=True,
        )

        st.sidebar.caption(
            "Stays loaded across refreshes — use Remove Dataset below to clear it."
        )

        if st.sidebar.button("🗑️ Remove Dataset", width='stretch'):

            delete_session(st.session_state.get("session_id"))

            st.session_state["dataset"] = None
            st.session_state["original_dataset"] = None
            st.session_state["cleaning_report"] = []
            st.session_state["uploaded_file_fingerprint"] = None
            st.session_state["uploaded_file_name"] = None
            st.session_state["_persisted_dataset_id"] = None

            st.session_state.pop("outlier_scan_result", None)

            # Force the file_uploader widget to reset visually too, instead
            # of continuing to display the now-cleared file's name.
            st.session_state["uploader_version"] = uploader_version + 1

            st.toast("Dataset removed", icon="🗑️")

            st.rerun()

    else:

        st.sidebar.info("No dataset loaded yet.")

    st.sidebar.divider()

    if st.sidebar.button("← Back to Landing", width='stretch'):

        st.session_state["show_landing"] = True

        st.query_params.pop("app", None)

        st.toast("Back to landing page", icon="👋")

        st.rerun()

    st.sidebar.divider()

    st.sidebar.caption("Version 2.0 · Purple AI Edition")

    st.sidebar.caption("Made with 💜 using Streamlit")

    return PAGES[page]