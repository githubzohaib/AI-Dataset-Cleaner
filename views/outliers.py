import streamlit as st

from components.dataset_guard import get_dataset
from components.page_header import show_header
from components.metric_cards import show_metrics
from components.feedback import action_status

from utils.analysis.outliers import (
    detect_outliers,
    remove_outliers,
)

SCAN_KEY = "outlier_scan_result"


def _run_scan(df):
    """
    Run Isolation Forest and cache the result in session_state.

    Detection is intentionally NOT re-run on every script rerun. Isolation
    Forest is configured with a fixed `contamination` quota, which forces it
    to flag ~5% of *whatever data it's given* as anomalous — always, no
    matter how clean the data already is. If detection reran live on every
    page load, clicking "Remove All" would remove the flagged rows, the page
    would rerun, detection would fire again on the now-smaller dataset, and
    a brand new ~5% batch would immediately appear — making removal look
    completely broken even though it worked. Scanning once and letting the
    user explicitly re-scan avoids that illusion.
    """

    with action_status("🤖 Scanning dataset for outliers (Isolation Forest)...") as status:

        result = detect_outliers(df)

        status.update(
            label=f"✅ Scan complete — {result['count']} outlier(s) found",
            state="complete",
            expanded=False,
        )

    st.session_state[SCAN_KEY] = result

    st.toast(f"Scan found {result['count']} outlier(s)", icon="🤖")


def show_page():

    show_header(
        "🤖 ML Outlier Detection",
        "Detect anomalies using Isolation Forest (unsupervised machine learning).",
    )

    df = get_dataset()

    if SCAN_KEY not in st.session_state:
        _run_scan(df)

    scan = st.session_state[SCAN_KEY]

    if not scan["features"]:

        st.info("No numerical columns available for outlier detection.")

        return

    # The scan is a snapshot from whenever it last ran — rows it flagged may
    # have since been removed (by this page or any other cleaning step).
    # Re-deriving against the *current* dataset keeps the numbers honest
    # without forcing a fresh (and inevitably non-empty) quota-based rescan.
    live_index = scan["rows"].index.intersection(df.index)
    live_rows = df.loc[live_index]
    live_mask = df.index.isin(live_index)
    live_count = len(live_rows)
    live_percentage = round(live_count / len(df) * 100, 2) if len(df) else 0

    show_metrics([
        ("Outliers (last scan)", live_count),
        ("Percentage", f"{live_percentage}%"),
    ], columns=2)

    st.caption(
        "Showing results from the last scan. The model won't re-flag data "
        "on its own after you remove something — click Re-scan if you want "
        "a fresh pass over what's left."
    )

    if st.button("🔄 Re-scan for Outliers", width='stretch'):

        _run_scan(df)

        st.rerun()

    st.divider()

    st.subheader("Features Used for Detection")

    st.write(scan["features"])

    st.divider()

    if live_count == 0:

        st.success(
            "✅ No outliers remaining from the last scan. Click Re-scan to "
            "check the current dataset again."
        )

        return

    st.subheader("🧹 Remove Outliers")

    tab_all, tab_individual = st.tabs(["⚡ Remove All", "🎯 Review Individually"])

    with tab_all:

        st.write(
            f"Remove all **{live_count}** outliers flagged by the last scan "
            "in one click."
        )

        if st.button(
            "🚮 Remove All Outliers",
            type="primary",
            width='stretch',
            key="remove_all_outliers",
        ):

            with action_status("🚮 Removing outliers...") as status:

                cleaned = remove_outliers(df, live_mask)

                removed = len(df) - len(cleaned)

                status.update(
                    label=f"✅ Removed {removed} outliers",
                    state="complete",
                    expanded=False,
                )

            st.session_state["dataset"] = cleaned

            st.session_state["cleaning_report"].append(
                f"Removed {removed} outliers using Isolation Forest"
            )

            st.toast(f"Removed {removed} outliers", icon="✅")

            st.success(f"{removed} outliers removed.")

            st.rerun()

    with tab_individual:

        st.caption(
            "Uncheck any rows you'd like to keep, then remove only the "
            "outliers still checked — handy when the model flags a point "
            "you know is legitimate."
        )

        editable = live_rows.copy()

        editable.insert(0, "Remove", True)

        edited = st.data_editor(
            editable,
            column_config={
                "Remove": st.column_config.CheckboxColumn("Remove?", default=True),
            },
            disabled=[c for c in editable.columns if c != "Remove"],
            hide_index=True,
            width='stretch',
        )

        selected_index = edited.index[edited["Remove"]]

        if st.button(
            f"🗑 Remove Selected ({len(selected_index)})",
            type="primary",
            width='stretch',
            disabled=len(selected_index) == 0,
            key="remove_selected_outliers",
        ):

            with action_status("🚮 Removing selected outliers...") as status:

                cleaned = df.drop(index=selected_index)

                removed = len(selected_index)

                status.update(
                    label=f"✅ Removed {removed} outlier(s)",
                    state="complete",
                    expanded=False,
                )

            st.session_state["dataset"] = cleaned

            st.session_state["cleaning_report"].append(
                f"Removed {removed} manually selected outlier(s) using Isolation Forest"
            )

            st.toast(f"Removed {removed} selected outlier(s)", icon="✅")

            st.success(f"Removed {removed} selected outlier(s).")

            st.rerun()
