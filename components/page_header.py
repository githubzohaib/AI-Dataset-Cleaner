import streamlit as st


def show_header(title, subtitle):

    st.markdown(
        f"""
        <h1 class="gradient-text" style="margin-bottom:0;">{title}</h1>
        <p style="color:#F4A8CB; font-size:15px; margin-top:2px;">{subtitle}</p>
        <hr style="margin-top:10px;">
        """,
        unsafe_allow_html=True,
    )