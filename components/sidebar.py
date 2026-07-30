import uuid

import streamlit as st
import streamlit.components.v1 as components

from utils.analysis.loader import load_dataset, SUPPORTED_EXTENSIONS
from utils.persistence import delete_session


PAGES = {
    "  Dashboard": "home",
    "  Overview": "overview",
    "  Explorer": "explorer",
    "  Missing Values": "missing",
    "  Duplicates": "duplicates",
    "  Outliers": "outliers",
    "  Cleaning": "cleaning",
    "  Analytics": "visualization",
    "  AI Insights": "insights",
    "  Export": "export",
}


def _inject_mobile_sidebar_css():
    """Responsive CSS: hamburger on mobile, normal sidebar on desktop."""

    st.markdown(
        """
        <style>
        /* ── MOBILE: hide sidebar off-screen, show hamburger ── */
        @media (max-width: 768px) {

            [data-testid="stSidebar"] {
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                bottom: 0 !important;
                z-index: 9999 !important;
                display: flex !important;
                flex-direction: column !important;
                width: 290px !important;
                min-width: 290px !important;
                max-width: 290px !important;
                transform: translateX(-100%) !important;
                transition: transform 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
                overflow-y: auto !important;
                -webkit-overflow-scrolling: touch !important;
                background: #0D0A1A !important;
                padding-top: 16px !important;
                box-shadow: none !important;
            }
            [data-testid="stSidebar"].mobile-open {
                transform: translateX(0) !important;
                box-shadow: 8px 0 40px rgba(0,0,0,0.55) !important;
            }

            /* dark backdrop behind sidebar */
            .sb-backdrop {
                display: none;
                position: fixed;
                inset: 0;
                background: rgba(0, 0, 0, 0.6);
                z-index: 9998;
                backdrop-filter: blur(4px);
                -webkit-backdrop-filter: blur(4px);
            }
            .sb-backdrop.active { display: block; }

            /* hamburger button */
            .sb-hamburger {
                display: flex !important;
                position: fixed;
                top: 12px;
                left: 12px;
                z-index: 10000;
                width: 44px;
                height: 44px;
                border-radius: 11px;
                background: rgba(236, 72, 153, 0.14);
                border: 1px solid rgba(236, 72, 153, 0.35);
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: background 0.15s ease, transform 0.1s ease;
                -webkit-tap-highlight-color: transparent;
            }
            .sb-hamburger:active {
                background: rgba(236, 72, 153, 0.32);
                transform: scale(0.93);
            }
            .sb-hamburger svg {
                width: 20px; height: 20px;
                pointer-events: none;
            }

            /* close X inside sidebar — shown only once openSidebar() has
               moved it inside .mobile-open, driven by the class alone (see
               rule below) rather than the JS inline style that used to try
               to flip this: an inline style can never win against this
               !important rule, so the X was never actually visible. */
            .sb-close {
                display: none !important;
                position: absolute;
                top: 14px;
                right: 14px;
                width: 32px;
                height: 32px;
                border-radius: 8px;
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.1);
                align-items: center;
                justify-content: center;
                cursor: pointer;
                z-index: 10001;
                color: #D8CFEF;
                font-size: 15px;
                line-height: 1;
                -webkit-tap-highlight-color: transparent;
                transition: background 0.12s ease;
            }
            .sb-close:active {
                background: rgba(255,255,255,0.14);
            }
            [data-testid="stSidebar"].mobile-open .sb-close {
                display: flex !important;
            }

            /* full-width main content */
            [data-testid="stMain"] {
                margin-left: 0 !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
        }

        /* ── DESKTOP: hide mobile-only elements ── */
        @media (min-width: 769px) {
            .sb-hamburger,
            .sb-backdrop,
            .sb-close {
                display: none !important;
            }
        }
        </style>

        <!-- hamburger icon -->
        <div class="sb-hamburger" id="sbHamburger">
            <svg viewBox="0 0 24 24" fill="none" stroke="#F9A8D4"
                 stroke-width="2.2" stroke-linecap="round">
                <line x1="4" y1="6" x2="20" y2="6"/>
                <line x1="4" y1="12" x2="20" y2="12"/>
                <line x1="4" y1="18" x2="20" y2="18"/>
            </svg>
        </div>

        <!-- backdrop overlay -->
        <div class="sb-backdrop" id="sbBackdrop"></div>

        <!-- close button (will be moved into sidebar by JS) -->
        <div class="sb-close" id="sbClose">✕</div>
        """,
        unsafe_allow_html=True,
    )


def _inject_mobile_sidebar_js():
    """Zero-height iframe script that controls the parent DOM."""

    components.html(
        """
        <script>
        (function () {
            try {
                var doc = window.parent.document;
            } catch(e) {
                return; // Cross-origin blocked, abort gracefully
            }

            // Use a flag on the parent window so we only attach delegation listeners ONCE.
            // This survives Streamlit iframe destruction/recreation on re-runs.
            if (window.parent._sbMobileBound) return;
            window.parent._sbMobileBound = true;

            function openSidebar() {
                var sb = doc.querySelector('[data-testid="stSidebar"]');
                var bd = doc.getElementById('sbBackdrop');
                var cl = doc.getElementById('sbClose');
                if (!sb) return;
                sb.classList.add('mobile-open');
                if (bd) bd.classList.add('active');
                if (cl && !sb.contains(cl)) {
                    sb.insertBefore(cl, sb.firstChild);
                }
            }

            function closeSidebar() {
                var sb = doc.querySelector('[data-testid="stSidebar"]');
                var bd = doc.getElementById('sbBackdrop');
                if (sb) sb.classList.remove('mobile-open');
                if (bd) bd.classList.remove('active');
            }

            // EVENT DELEGATION on document (capture phase)
            // This ensures clicks work perfectly even if Streamlit completely 
            // destroys and recreates the HTML elements on re-renders.
            doc.addEventListener('click', function (e) {
                if (e.target.closest('#sbHamburger')) {
                    e.stopPropagation();
                    var sb = doc.querySelector('[data-testid="stSidebar"]');
                    if (sb && sb.classList.contains('mobile-open')) {
                        closeSidebar();
                    } else {
                        openSidebar();
                    }
                    return;
                }
                if (e.target.closest('#sbBackdrop')) {
                    closeSidebar();
                    return;
                }
                if (e.target.closest('#sbClose')) {
                    e.stopPropagation();
                    closeSidebar();
                    return;
                }
            }, true);

            // Auto-close sidebar when user taps a nav radio on mobile
            doc.addEventListener('change', function (e) {
                if (e.target.matches('[data-testid="stSidebar"] input[type="radio"]')) {
                    if (window.parent.innerWidth <= 768) {
                        setTimeout(closeSidebar, 150);
                    }
                }
            }, true);

            // Close on rotate / resize past breakpoint
            window.parent.addEventListener('resize', function () {
                if (window.parent.innerWidth > 768) closeSidebar();
            });

        })();
        </script>
        """,
        height=0,
        width=0,
    )


def sidebar():

    _inject_mobile_sidebar_css()
    _inject_mobile_sidebar_js()

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

                    st.session_state.pop("outlier_scan_result", None)

                    st.toast(
                        f"Loaded {len(df):,} rows × {df.shape[1]} columns",
                        icon="✅",
                    )

    st.sidebar.divider()

    page_labels = list(PAGES.keys())

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
            st.session_state["_persisted_dataset_ref"] = None

            st.session_state.pop("outlier_scan_result", None)

            st.session_state["uploader_version"] = uploader_version + 1

            st.toast("Dataset removed", icon="🗑️")

            st.rerun()

    else:

        st.sidebar.info("No dataset loaded yet.")

    if st.sidebar.button(
        "🔄 Start New Session",
        width='stretch',
        help="Clears the uploaded dataset, cleaning history and cleaning "
             "options, and starts over with a completely fresh session.",
    ):

        # Wipe this session's disk cache (dataset blob + cleaning-options
        # file) before minting a new session id — otherwise the old id's
        # cache entries would just sit there until the 24h sweep.
        delete_session(st.session_state.get("session_id"))

        # Bump forward (never reuse/reset to 0) so the file_uploader widget
        # gets a key it has genuinely never had before — matches the same
        # reasoning as "Remove Dataset" below, needed because
        # st.session_state.clear() below would otherwise make this default
        # back to 0, which the browser's widget state may already know.
        next_uploader_version = st.session_state.get("uploader_version", 0) + 1

        # A full reset, not just the dataset fields: session_state.clear()
        # also drops cleaning options, scan results, and every other
        # transient key, so "Start New Session" genuinely means starting
        # over rather than a partial reset.
        st.session_state.clear()

        st.session_state["session_id"] = uuid.uuid4().hex
        st.session_state["uploader_version"] = next_uploader_version

        # Reset the URL too: a fresh sid, dropped page (back to the
        # dashboard home), and "app=1" so the user stays inside the app
        # instead of bouncing back to the landing gate.
        st.query_params.clear()
        st.query_params["sid"] = st.session_state["session_id"]
        st.query_params["app"] = "1"

        st.toast("Started a new session", icon="🔄")

        st.rerun()

    st.sidebar.divider()

    if st.sidebar.button("← Back to Landing", width='stretch'):

        st.session_state["show_landing"] = True

        st.query_params.pop("app", None)

        st.toast("Back to landing page", icon="👋")

        st.rerun()

    return PAGES[page]