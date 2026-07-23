import streamlit as st


def plot(fig):

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F3F0FF", family="Poppins, sans-serif"),
        colorway=[
            "#EC4899", "#F472B6", "#DB2777", "#F9A8D4",
            "#BE185D", "#FBCFE8", "#F43F5E",
        ],
        margin=dict(t=50, l=10, r=10, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )

    fig.update_xaxes(gridcolor="rgba(236,72,153,0.12)")
    fig.update_yaxes(gridcolor="rgba(236,72,153,0.12)")

    st.plotly_chart(
        fig,
        width='stretch',
    )