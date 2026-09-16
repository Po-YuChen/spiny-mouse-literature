import html
import streamlit as st


def tags(items):
    return " · ".join(
        [
            str(x)
            for x in (items or [])
            if str(x).strip()
        ]
    )


def publication_card(row):

    signal_pathway = str(
        row.get(
            "Signal_Pathway",
            "",
        )
    ).strip()

    brief_focus = str(
        row.get(
            "Brief_Research_Focus",
            "",
        )
    ).strip()


    signal_html = ""

    if signal_pathway:

        signal_html = f"""
        <div style="margin-top:12px">
          <b>Signal Pathway:</b><br>
          <span style="line-height:1.5">
            {html.escape(signal_pathway)}
          </span>
        </div>
        """


    focus_html = ""

    if brief_focus:

        focus_html = f"""
        <div style="margin-top:12px">
          <b>Brief Research Focus:</b><br>
          <span style="line-height:1.5">
            {html.escape(brief_focus)}
          </span>
        </div>
        """


    st.markdown(
        f"""
        <div style="
            border:1px solid #E1E7E4;
            border-radius:14px;
            padding:18px 20px;
            margin-bottom:10px;
            background:#fff;
        ">

          <div style="
              font-size:.83rem;
              color:#66756F;
          ">
            {html.escape(str(row.get("Year", "")))}
            ·
            {html.escape(str(row.get("Article_Type", "")))}
          </div>

          <div style="
              font-size:1.08rem;
              font-weight:700;
              margin:6px 0;
          ">
            {html.escape(str(row.get("Title", "")))}
          </div>

          <div style="
              font-size:.9rem;
              color:#53625D;
              margin-bottom:10px;
          ">
            {html.escape(str(row.get("First_Author", "")))}
            ·
            {html.escape(str(row.get("Journal", "")))}
          </div>

          <div>
            <b>Species:</b>
            {html.escape(tags(row.get("_species", [])))}
          </div>

          <div>
            <b>Organ:</b>
            {html.escape(tags(row.get("_organs", [])))}
          </div>

          <div>
            <b>Model:</b>
            {html.escape(tags(row.get("_disease_models", [])))}
          </div>

          <div>
            <b>Omics:</b>
            {html.escape(tags(row.get("_omics", [])))}
          </div>

          {signal_html}

          {focus_html}

        </div>
        """,
        unsafe_allow_html=True,
    )


    c = st.columns(
        [1, 1, 1, 5]
    )


    if str(
        row.get(
            "PubMed_URL",
            "",
        )
    ).strip():

        c[0].link_button(
            "PubMed",
            row["PubMed_URL"],
            use_container_width=True,
        )


    doi = str(
        row.get(
            "DOI",
            "",
        )
    ).strip()

    if doi:

        c[1].link_button(
            "DOI",
            doi
            if doi.startswith("http")
            else f"https://doi.org/{doi}",
            use_container_width=True,
        )


    ds = (
        row.get(
            "_datasets",
            [],
        )
        or []
    )

    if (
        ds
        and str(
            ds[0].get(
                "Dataset_URL",
                "",
            )
        ).strip()
    ):

        c[2].link_button(
            f"Dataset{'s' if len(ds) > 1 else ''}",
            ds[0]["Dataset_URL"],
            use_container_width=True,
        )
