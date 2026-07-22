from components.dataset_guard import get_dataset
from components.page_header import show_header
from components.explorer import dataframe_explorer


def show_page():

    show_header(
        "🔍 Dataset Explorer",
        "Search, filter and sort your dataset.",
    )

    df = get_dataset()

    dataframe_explorer(df)
