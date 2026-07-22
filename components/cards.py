import streamlit as st


def card(title, value, icon: str = ""):
    """Render a glassmorphic stat card."""

    st.markdown(
        f"""
        <div class="glass-card">
            <h4>{icon} {title}</h4>
            <h2>{value}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
