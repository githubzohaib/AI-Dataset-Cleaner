import uuid

import streamlit as st

from config.settings import (
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
    CSS_PATH,
)

from components.sidebar import sidebar
from components.home import show_home
from components.landing import show_landing

from utils.persistence import (
    CLEANING_OPTION_DEFAULTS,
    cleanup_stale_sessions,
    load_cleaning_options,
    load_session,
    save_cleaning_options,
    save_session,
)

# ----------------------------
# Session Identity (survives a browser refresh via the URL)
# ----------------------------

if "session_id" not in st.session_state:

    # Reuse the id already in the URL if this is a refresh of a session we've
    # seen before; otherwise mint a new one and stamp it into the URL so the
    # *next* refresh can find it too.
    st.session_state["session_id"] = st.query_params.get("sid") or uuid.uuid4().hex

    st.query_params["sid"] = st.session_state["session_id"]

    cleanup_stale_sessions()

# ----------------------------
# Session State Initialization
# ----------------------------

if "dataset" not in st.session_state:

    # Browser refresh = brand-new session_state, but the "sid" query param
    # above survives — use it to restore whatever dataset was last uploaded
    # instead of forcing the user to re-upload from scratch every refresh.
    restored = load_session(st.session_state["session_id"])

    st.session_state["dataset"] = restored["dataset"] if restored else None
    st.session_state["original_dataset"] = restored["original_dataset"] if restored else None
    st.session_state["cleaning_report"] = restored["cleaning_report"] if restored else []
    st.session_state["uploaded_file_name"] = restored["source_name"] if restored else None
    st.session_state["_persisted_dataset_ref"] = st.session_state["dataset"]

if "opt_numeric_strategy" not in st.session_state:

    # Same idea as the dataset restore above: a fresh session_state after a
    # refresh would otherwise silently reset every cleaning-tab widget
    # (strategy, checkboxes, threshold) back to its hardcoded default,
    # discarding choices the user already made. Seed session_state with the
    # cached values *before* views/cleaning.py creates the widgets — a
    # widget adopts whatever is already in st.session_state[key] instead of
    # its own `index`/`value` argument, so this is all that's needed to
    # restore them.
    for option_key, option_value in load_cleaning_options(
        st.session_state["session_id"]
    ).items():
        st.session_state[option_key] = option_value

if "show_landing" not in st.session_state:
    # A browser refresh starts a brand-new Streamlit session, wiping
    # session_state entirely — so this init would normally re-trigger the
    # landing gate every time. The "app" query param survives a refresh
    # (it's part of the URL), so we use it to remember that the user had
    # already entered the app and skip straight back to the dashboard shell.
    st.session_state["show_landing"] = st.query_params.get("app") != "1"

# ----------------------------
# Page Config
# ----------------------------

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
)

# ----------------------------
# Custom CSS (purple AI theme)
# ----------------------------

hide_streamlit_style = """
<style>
#MainMenu { visibility:hidden; }
footer { visibility:hidden; }
header { visibility:hidden; }
/* visibility (not display:none): stExpandSidebarButton — the only control
   that re-opens the sidebar once Streamlit's own native logic collapses it
   (its AUTO responsive behavior on narrow widths) — lives inside this
   toolbar. display:none would remove it from the tree entirely, with no way
   for a descendant to opt back in, permanently stranding a collapsed
   sidebar on desktop with no way to bring it back. */
[data-testid="stToolbar"]{ visibility:hidden; }
[data-testid="stExpandSidebarButton"] { visibility: visible !important; }
</style>
"""

try:
    with open(CSS_PATH) as css_file:
        custom_css = f"<style>{css_file.read()}</style>"
except FileNotFoundError:
    custom_css = ""

# Merged into a single st.markdown call: two separate calls would sit as two
# separate siblings in Streamlit's top-level vertical block, each pulling in
# its own flex "gap" — pure dead space above everything else on the page,
# including the landing page's sticky navbar.
st.markdown(hide_streamlit_style + custom_css, unsafe_allow_html=True)

# ----------------------------
# Landing Page Gate
# ----------------------------

if st.session_state["show_landing"]:

    show_landing()

else:

    # ----------------------------
    # Sidebar Navigation
    # ----------------------------

    page = sidebar()

    # ----------------------------
    # Route Pages
    # ----------------------------

    ROUTES = {
        "home": ("components.home", "show_home"),
        "overview": ("views.overview", "show_page"),
        "explorer": ("views.explorer", "show_page"),
        "missing": ("views.missing", "show_page"),
        "duplicates": ("views.duplicates", "show_page"),
        "outliers": ("views.outliers", "show_page"),
        "cleaning": ("views.cleaning", "show_page"),
        "visualization": ("views.visualization", "show_page"),
        "insights": ("views.insights", "show_page"),
        "export": ("views.export", "show_page"),
    }

    module_name, function_name = ROUTES[page]

    if page == "home":
        show_home()
    else:
        module = __import__(module_name, fromlist=[function_name])
        getattr(module, function_name)()

    # ----------------------------
    # Persist the dataset so it survives a browser refresh
    # ----------------------------
    # Every mutating action (upload, clean, reset, remove duplicates/outliers)
    # replaces st.session_state["dataset"] with a new DataFrame object and
    # then reruns — so comparing object identity here is a cheap, reliable
    # way to write to disk only when something actually changed, instead of
    # re-pickling on every single unrelated rerun (widget toggles, etc.).
    #
    # NOTE: this compares the object itself via `is`, not `id()`. `id()` is a
    # memory address, and once the old dataframe object is garbage-collected
    # (which can happen on any later rerun once nothing else references it),
    # CPython is free to reuse that exact address for a brand-new object —
    # causing `id(new_df) == id(old_df)` by coincidence and silently
    # skipping the save even though the dataset genuinely changed. Holding a
    # live reference in `_persisted_dataset_ref` prevents that object from
    # ever being collected in the first place, so `is` comparison is safe.
    current_dataset = st.session_state.get("dataset")

    if current_dataset is not None and (
        st.session_state.get("_persisted_dataset_ref") is not current_dataset
    ):

        save_session(
            st.session_state["session_id"],
            current_dataset,
            st.session_state.get("original_dataset"),
            st.session_state.get("cleaning_report", []),
            st.session_state.get("uploaded_file_name"),
        )

        st.session_state["_persisted_dataset_ref"] = current_dataset

    # ----------------------------
    # Persist cleaning options so they survive a browser refresh too
    # ----------------------------
    # Cheap dict-equality check against the last-saved snapshot, run on
    # every rerun (unlike the dataset save above, this file is small enough
    # that there's no need to be stingy about write frequency) — it just
    # avoids re-writing the settings file when nothing actually changed.
    current_options = {
        key: st.session_state.get(key, default)
        for key, default in CLEANING_OPTION_DEFAULTS.items()
    }

    if current_options != st.session_state.get("_persisted_options_snapshot"):

        save_cleaning_options(st.session_state["session_id"], current_options)

        st.session_state["_persisted_options_snapshot"] = current_options