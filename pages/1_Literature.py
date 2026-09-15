import streamlit as st

from utils.google_sheets import load_google_sheets
from utils.database import enrich_literature, filter_literature
from utils.ui import publication_card


st.set_page_config(
    page_title="Literature | Spiny Mouse Database",
    page_icon="🔎",
    layout="wide",
)

st.title("Literature Search")


# -----------------------------
# Load database
# -----------------------------

data = load_google_sheets()
lit = enrich_literature(data)


# -----------------------------
# Search
# -----------------------------

q = st.text_input(
    "Search literature",
    placeholder="e.g. kidney regeneration, macrophage, scRNA-seq",
    key="literature_query",
)


# -----------------------------
# Prepare year range
# -----------------------------

year_values = sorted(
    [
        int(y)
        for y in lit["Year"]
        .dropna()
        .astype(str)
        .unique()
        if str(y).isdigit()
    ]
)


# -----------------------------
# Helper: popover checkbox filter
# -----------------------------

def popover_filter(label, options, key_prefix):
    selected = []

    # Count selected options from session state
    selected_count = sum(
        1
        for i in range(len(options))
        if st.session_state.get(
            f"{key_prefix}_{i}",
            False,
        )
    )

    # Show selection count in button label
    button_label = (
        f"{label} ({selected_count})"
        if selected_count > 0
        else label
    )

    # Popover
    with st.popover(
        button_label,
        use_container_width=True,
    ):

        st.markdown(f"**Select {label}**")

        for i, option in enumerate(options):

            checked = st.checkbox(
                option,
                key=f"{key_prefix}_{i}",
            )

            if checked:
                selected.append(option)

    return selected


# -----------------------------
# Filters
# -----------------------------

with st.expander(
    "Filters",
    expanded=True,
):

    # -----------------------------
    # Year
    # -----------------------------

    st.markdown("**Year**")

    year_row = st.columns([1, 1, 4])

    year_from = year_row[0].selectbox(
        "From",
        year_values,
        index=0,
    )

    year_to = year_row[1].selectbox(
        "To",
        year_values,
        index=len(year_values) - 1,
    )


    # -----------------------------
    # Topic / Species / Organ
    # -----------------------------

    r1 = st.columns(3)

    with r1[0]:

        topics = popover_filter(
            "Topic",
            sorted(
                set(
                    sum(
                        lit["_topics"].tolist(),
                        [],
                    )
                )
            ),
            "topic",
        )

    with r1[1]:

        species = popover_filter(
            "Species",
            sorted(
                set(
                    sum(
                        lit["_species"].tolist(),
                        [],
                    )
                )
            ),
            "species",
        )

    with r1[2]:

        organs = popover_filter(
            "Organ",
            sorted(
                set(
                    sum(
                        lit["_organs"].tolist(),
                        [],
                    )
                )
            ),
            "organ",
        )


    # -----------------------------
    # Disease / Omics / Article type / Dataset
    # -----------------------------

    r2 = st.columns(4)

    with r2[0]:

        disease = popover_filter(
            "Disease model",
            sorted(
                set(
                    sum(
                        lit["_disease_models"].tolist(),
                        [],
                    )
                )
            ),
            "disease",
        )

    with r2[1]:

        omics = popover_filter(
            "Omics",
            sorted(
                set(
                    sum(
                        lit["_omics"].tolist(),
                        [],
                    )
                )
            ),
            "omics",
        )

    with r2[2]:

        article_types = popover_filter(
            "Article type",
            sorted(
                lit["Article_Type"]
                .dropna()
                .unique()
            ),
            "article_type",
        )

    with r2[3]:

        st.markdown(
            "<div style='height: 8px;'></div>",
            unsafe_allow_html=True,
        )

        has_dataset = st.toggle(
            "Has public dataset"
        )


# -----------------------------
# Convert year range to year list
# -----------------------------

if year_from <= year_to:

    years = [
        str(y)
        for y in year_values
        if year_from <= y <= year_to
    ]

else:

    years = []


# -----------------------------
# Apply search + filters
# -----------------------------

res = filter_literature(
    lit,
    q,
    years,
    topics,
    species,
    organs,
    disease,
    omics,
    article_types,
    has_dataset,
)


st.write(
    f"**{len(res):,} publications found**"
)


# -----------------------------
# Pagination
# -----------------------------

page_size = st.selectbox(
    "Results per page",
    [10, 20, 50],
    index=1,
)

pages = max(
    1,
    (len(res) + page_size - 1)
    // page_size,
)

page = st.number_input(
    "Page",
    min_value=1,
    max_value=pages,
    value=1,
)


# -----------------------------
# Publication cards
# -----------------------------

start = (
    (page - 1)
    * page_size
)

end = (
    page
    * page_size
)

for _, row in res.iloc[
    start:end
].iterrows():

    publication_card(row)

    st.divider()
