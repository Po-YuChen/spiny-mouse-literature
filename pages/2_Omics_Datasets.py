import pandas as pd
import streamlit as st

from utils.google_sheets import load_google_sheets
from utils.database import enrich_literature


st.set_page_config(
    page_title="Omics & Datasets",
    page_icon="🧬",
    layout="wide",
)

st.title("Omics & Public Datasets")


# -----------------------------
# Load database
# -----------------------------

data = load_google_sheets()

lit = enrich_literature(data)

ds = data["Datasets"].copy()


# -----------------------------
# Merge publication information
# -----------------------------

small = lit[
    [
        "Literature_ID",
        "Title",
        "Year",
        "Journal",
        "_species",
        "_organs",
    ]
]

m = ds.merge(
    small,
    on="Literature_ID",
    how="left",
)


# -----------------------------
# Prepare filter options
# -----------------------------

repository_options = sorted(
    [
        x
        for x in m["Database"]
        .dropna()
        .astype(str)
        .unique()
        if x.strip()
    ]
)

omics_options = sorted(
    [
        x
        for x in m["Omics_Type"]
        .dropna()
        .astype(str)
        .unique()
        if x.strip()
    ]
)


# -----------------------------
# Helper: Select all / none
# -----------------------------

def set_dataset_filter_state(
    options,
    key_prefix,
    value,
):
    for i in range(len(options)):

        st.session_state[
            f"dataset_filter_{key_prefix}_{i}"
        ] = value


# -----------------------------
# Helper: popover checkbox filter
# -----------------------------

def dataset_popover_filter(
    label,
    options,
    key_prefix,
):

    # Default = Select all
    for i in range(len(options)):

        checkbox_key = (
            f"dataset_filter_{key_prefix}_{i}"
        )

        if checkbox_key not in st.session_state:

            st.session_state[
                checkbox_key
            ] = True


    # Count current selections
    selected_count = sum(
        1
        for i in range(len(options))
        if st.session_state.get(
            f"dataset_filter_{key_prefix}_{i}",
            True,
        )
    )


    button_label = (
        f"{label} ({selected_count})"
    )


    selected = []


    with st.popover(
        button_label,
        use_container_width=True,
    ):

        action_cols = st.columns(2)

        action_cols[0].button(
            "Select all",
            key=f"dataset_filter_{key_prefix}_select_all",
            use_container_width=True,
            on_click=set_dataset_filter_state,
            args=(
                options,
                key_prefix,
                True,
            ),
        )

        action_cols[1].button(
            "Select none",
            key=f"dataset_filter_{key_prefix}_select_none",
            use_container_width=True,
            on_click=set_dataset_filter_state,
            args=(
                options,
                key_prefix,
                False,
            ),
        )

        st.divider()


        for i, option in enumerate(options):

            checked = st.checkbox(
                option,
                key=f"dataset_filter_{key_prefix}_{i}",
            )

            if checked:
                selected.append(option)


    # Show selected options directly
    if selected:

        st.caption(
            ", ".join(selected)
        )

    else:

        st.caption(
            "None"
        )


    return selected


# -----------------------------
# Filters
# -----------------------------

c1, c2, c3 = st.columns(3)


with c1:

    dbs = dataset_popover_filter(
        "Repository",
        repository_options,
        "repository",
    )


with c2:

    oms = dataset_popover_filter(
        "Omics type",
        omics_options,
        "omics",
    )


with c3:

    q = st.text_input(
        "Search accession or publication",
        placeholder="e.g. GSE71761, kidney, regeneration",
    )


# -----------------------------
# Apply filters
# -----------------------------

mask = pd.Series(
    True,
    index=m.index,
)


# Repository
if len(dbs) == 0:

    mask &= False

elif len(dbs) < len(repository_options):

    mask &= m["Database"].isin(dbs)


# Omics type
if len(oms) == 0:

    mask &= False

elif len(oms) < len(omics_options):

    mask &= m["Omics_Type"].isin(oms)


# Keyword search
if q.strip():

    search_query = (
        q.lower()
        .strip()
    )

    mask &= m.apply(
        lambda r:
        search_query
        in " ".join(
            [
                str(
                    r.get(
                        "Accession",
                        "",
                    )
                ),
                str(
                    r.get(
                        "Title",
                        "",
                    )
                ),
                str(
                    r.get(
                        "PMID",
                        "",
                    )
                ),
                str(
                    r.get(
                        "Database",
                        "",
                    )
                ),
                str(
                    r.get(
                        "Omics_Type",
                        "",
                    )
                ),
            ]
        ).lower(),
        axis=1,
    )


res = m[mask].copy()


# -----------------------------
# Result count
# -----------------------------

st.write(
    f"**{len(res):,} dataset records found**"
)


# -----------------------------
# Dataset cards
# -----------------------------

for _, r in res.iterrows():

    st.markdown(
        f"### {r.get('Accession', '')}"
    )

    st.write(
        f"**{r.get('Omics_Type', '')}**"
        f" · {r.get('Database', '')}"
    )

    st.write(
        "Associated publication: "
        f"**{r.get('Title', '')}**"
    )


    species = (
        r.get(
            "_species",
            [],
        )
        or []
    )

    organs = (
        r.get(
            "_organs",
            [],
        )
        or []
    )


    st.caption(
        f"{r.get('Year', '')}"
        f" · {r.get('Journal', '')}"
        f" · Species: {', '.join(species)}"
        f" · Organ: {', '.join(organs)}"
    )


    dataset_url = str(
        r.get(
            "Dataset_URL",
            "",
        )
    ).strip()


    if dataset_url:

        st.link_button(
            "Open public dataset",
            dataset_url,
        )


    st.divider()
