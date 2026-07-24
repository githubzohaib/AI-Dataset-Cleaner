import streamlit as st

from components.dataset_guard import get_dataset
from components.page_header import show_header
from components.metric_cards import show_metrics
from components.feedback import action_status

from utils.analysis.duplicates import (
    duplicate_summary,
    remove_duplicates,
)


def show_page():

    show_header(
        "📋 Duplicate Analysis",
        "Detect and remove duplicate rows from the dataset.",
    )

    df = get_dataset()

    result = duplicate_summary(df)

    show_metrics([
        ("Duplicate Rows", result["count"]),
        ("Duplicate %", f"{result['percentage']}%"),
    ], columns=2)

    st.divider()

    if result["count"] == 0:

        st.success("✅ No duplicate rows found.")

        return

    st.subheader("🧹 Remove Duplicates")

    tab_all, tab_individual = st.tabs(["⚡ Remove All", "🎯 Review Individually"])

    with tab_all:

        st.write(
            f"Remove all **{result['count']}** detected duplicate rows in one click."
        )

        if st.button(
            "🗑 Remove All Duplicates",
            type="primary",
            width='stretch',
            key="remove_all_duplicates",
        ):

            with action_status("🗑️ Removing duplicate rows...") as status:

                cleaned_df = remove_duplicates(df)

                removed = len(df) - len(cleaned_df)

                status.update(
                    label=f"✅ Removed {removed} duplicate rows",
                    state="complete",
                    expanded=False,
                )

            st.session_state["dataset"] = cleaned_df

            st.session_state["cleaning_report"].append(
                f"Removed {removed} duplicate rows"
            )

            st.toast(f"Removed {removed} duplicate rows", icon="✅")

            st.success(f"Removed {removed} duplicate rows.")

            st.rerun()

    with tab_individual:

        st.caption(
            "Uncheck any rows you'd like to keep, then remove only the ones "
            "still checked."
        )

        editable = result["rows"].copy()

        editable.insert(0, "Remove", True)

        edited = st.data_editor(
            editable,
            column_config={
                "Remove": st.column_config.CheckboxColumn("Remove?", default=True),
            },
            disabled=[c for c in editable.columns if c != "Remove"],
            hide_index=True,
            width='stretch',
            key="duplicates_editor",
        )

        selected_index = edited.index[edited["Remove"]]

        if st.button(
            f"🗑 Remove Selected ({len(selected_index)})",
            type="primary",
            width='stretch',
            disabled=len(selected_index) == 0,
            key="remove_selected_duplicates",
        ):

            with action_status("🗑️ Removing selected rows...") as status:

                cleaned_df = df.drop(index=selected_index)

                removed = len(selected_index)

                status.update(
                    label=f"✅ Removed {removed} duplicate row(s)",
                    state="complete",
                    expanded=False,
                )

            st.session_state["dataset"] = cleaned_df

            st.session_state["cleaning_report"].append(
                f"Removed {removed} manually selected duplicate row(s)"
            )

            st.toast(f"Removed {removed} selected row(s)", icon="✅")

            st.success(f"Removed {removed} selected duplicate row(s).")

            st.rerun()
