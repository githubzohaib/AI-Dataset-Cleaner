import streamlit as st

from config.settings import (
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
    CSS_PATH,
)

from components.sidebar import sidebar
from components.home import show_home

# ----------------------------
# Session State Initialization
# ----------------------------

if "dataset" not in st.session_state:
    st.session_state["dataset"] = None

if "original_dataset" not in st.session_state:
    st.session_state["original_dataset"] = None

if "cleaning_report" not in st.session_state:
    st.session_state["cleaning_report"] = []

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
[data-testid="stToolbar"]{ display:none; }
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

try:
    with open(CSS_PATH) as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

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
