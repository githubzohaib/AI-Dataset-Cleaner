import streamlit as st


def plot(fig):

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F3F0FF", family="Poppins, sans-serif"),
        colorway=[
            "#A855F7", "#C084FC", "#7C3AED", "#D8B4FE",
            "#6D28D9", "#E9D5FF", "#8B5CF6",
        ],
        margin=dict(t=50, l=10, r=10, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )

    fig.update_xaxes(gridcolor="rgba(168,85,247,0.12)")
    fig.update_yaxes(gridcolor="rgba(168,85,247,0.12)")

    st.plotly_chart(
        fig,
        width='stretch',
    )
