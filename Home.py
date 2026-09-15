import streamlit as st

from utils.google_sheets import load_google_sheets
from utils.database import enrich_literature


st.set_page_config(
    page_title="Spiny Mouse Literature Database",
    page_icon="🐭",
    layout="wide",
)

st.title("Spiny Mouse Literature Database")

st.caption(
    "A curated resource for Acomys research, disease models, "
    "regeneration, and public omics datasets."
)


try:
    data = load_google_sheets()
    lit = enrich_literature(data)

except Exception as e:
    st.error(
        "The website could not load the public literature database."
    )
    st.code(str(e))
    st.info(
        "Please check the public Google Sheet connection."
    )
    st.stop()


# -----------------------------
# Database overview
# -----------------------------

a, b, c, d = st.columns(4)

a.metric(
    "Publications",
    f"{len(lit):,}",
)

b.metric(
    "Research Topics",
    f"{len(set(sum(lit['_topics'].tolist(), []))):,}",
)

c.metric(
    "Omics Studies",
    f"{int(lit['_omics'].map(bool).sum()):,}",
)

d.metric(
    "Public Dataset Accessions",
    f"{len(data['Datasets']):,}",
)


st.divider()


# -----------------------------
# Quick literature search
# -----------------------------

st.subheader("Search the literature")

with st.form("home_search_form"):

    home_query = st.text_input(
        "Search literature",
        placeholder=(
            "e.g. kidney regeneration, macrophage, "
            "scRNA-seq, fibrosis"
        ),
        key="home_search",
        label_visibility="collapsed",
    )

    submitted = st.form_submit_button(
        "Search",
        type="primary",
    )

if submitted:

    if home_query.strip():

        st.session_state[
            "literature_query"
        ] = home_query.strip()

        st.switch_page(
            "pages/1_Literature.py"
        )

    else:

        st.warning(
            "Please enter a keyword before searching."
        )


st.divider()


# -----------------------------
# Navigation
# -----------------------------

st.subheader("Explore the database")

st.page_link(
    "pages/1_Literature.py",
    label="Browse literature",
    icon="🔎",
)

st.page_link(
    "pages/2_Omics_Datasets.py",
    label="Explore omics & datasets",
    icon="🧬",
)

st.page_link(
    "pages/3_Statistics.py",
    label="View statistics",
    icon="📊",
)
