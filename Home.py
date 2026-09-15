# -----------------------------
# Quick literature search
# -----------------------------

st.subheader("Search the literature")


# Initialize search state
if "home_search" not in st.session_state:
    st.session_state["home_search"] = ""


def clear_home_search():
    st.session_state["home_search"] = ""


with st.form("home_search_form"):

    search_row = st.columns(
        [12, 0.45],
        gap="small",
    )

    # Search input
    with search_row[0]:

        home_query = st.text_input(
            "Search literature",
            placeholder=(
                "e.g. kidney regeneration, macrophage, "
                "scRNA-seq, fibrosis"
            ),
            key="home_search",
            label_visibility="collapsed",
        )

    # Clear button
    with search_row[1]:

        clear_clicked = st.form_submit_button(
            "×",
            help="Clear search",
        )

    submitted = st.form_submit_button(
        "Search",
        type="primary",
    )


# Clear search
if clear_clicked:

    st.session_state["home_search"] = ""

    st.rerun()


# Run search
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
