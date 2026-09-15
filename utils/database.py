from collections import defaultdict

import pandas as pd


def active_literature(df):
    out = df.copy()

    if "Record_Status" in out.columns:
        out = out[out["Record_Status"].eq("Active")].copy()

    out["Year_num"] = pd.to_numeric(
        out["Year"],
        errors="coerce",
    )

    return out


def relation_map(df, value_column):
    d = defaultdict(list)

    if df.empty:
        return {}

    for _, row in df.iterrows():
        literature_id = str(
            row.get("Literature_ID", "")
        ).strip()

        value = str(
            row.get(value_column, "")
        ).strip()

        if (
            literature_id
            and value
            and value not in d[literature_id]
        ):
            d[literature_id].append(value)

    return dict(d)


def dataset_map(df):
    d = defaultdict(list)

    if df.empty:
        return {}

    for _, row in df.iterrows():
        literature_id = str(
            row.get("Literature_ID", "")
        ).strip()

        if literature_id:
            d[literature_id].append(
                row.to_dict()
            )

    return dict(d)


def enrich_literature(data):
    lit = active_literature(
        data["Literature"]
    )

    mapping = {
        "_species": relation_map(
            data["Paper_Species"],
            "Species",
        ),
        "_organs": relation_map(
            data["Paper_Organs"],
            "Organ",
        ),
        "_omics": relation_map(
            data["Paper_Omics"],
            "Omics_Type",
        ),
        "_topics": relation_map(
            data["Paper_Topics"],
            "Topic",
        ),
        "_disease_models": relation_map(
            data["Paper_Disease_Models"],
            "Disease_Model_Category",
        ),
        "_keywords": relation_map(
            data["Paper_Keywords"],
            "Keyword",
        ),
    }

    datasets = dataset_map(
        data["Datasets"]
    )

    for column, relation in mapping.items():
        lit[column] = lit[
            "Literature_ID"
        ].map(
            lambda x: relation.get(x, [])
        )

    lit["_datasets"] = lit[
        "Literature_ID"
    ].map(
        lambda x: datasets.get(x, [])
    )

    lit["_has_dataset"] = lit[
        "_datasets"
    ].map(bool)

    return lit


def searchable_text(row):
    columns = [
        "Title",
        "Journal",
        "First_Author",
        "Affiliation",
        "Country",
        "PMID",
        "DOI",
        "Brief_Research_Focus",
        "Signal_Pathway",
        "Disease_Model_Display",
        "Keywords_Display",
        "Species_Display",
        "Organ_Display",
        "Omics_Display",
    ]

    parts = [
        str(row.get(column, ""))
        for column in columns
    ]

    for column in [
        "_species",
        "_organs",
        "_omics",
        "_topics",
        "_disease_models",
        "_keywords",
    ]:
        parts += row.get(column, []) or []

    return " ".join(parts).lower()


def filter_literature(
    df,
    query="",
    years=None,
    topics=None,
    species=None,
    organs=None,
    disease_models=None,
    omics=None,
    article_types=None,
    has_dataset=False,
):
    out = df.copy()

    if query.strip():
        q = query.strip().lower()

        out = out[
            out.apply(
                lambda row:
                q in searchable_text(row),
                axis=1,
            )
        ]

    def matches(values, selected):
        if not selected:
            return True

        return bool(
            set(values or [])
            & set(selected)
        )

    if years:
        out = out[
            out["Year"]
            .astype(str)
            .isin(years)
        ]

    if topics:
        out = out[
            out["_topics"].map(
                lambda x:
                matches(x, topics)
            )
        ]

    if species:
        out = out[
            out["_species"].map(
                lambda x:
                matches(x, species)
            )
        ]

    if organs:
        out = out[
            out["_organs"].map(
                lambda x:
                matches(x, organs)
            )
        ]

    if disease_models:
        out = out[
            out["_disease_models"].map(
                lambda x:
                matches(
                    x,
                    disease_models,
                )
            )
        ]

    if omics:
        out = out[
            out["_omics"].map(
                lambda x:
                matches(x, omics)
            )
        ]

    if article_types:
        out = out[
            out["Article_Type"]
            .isin(article_types)
        ]

    if has_dataset:
        out = out[
            out["_has_dataset"]
        ]

    return out.sort_values(
        ["Year_num", "Title"],
        ascending=[False, True],
        na_position="last",
    )
