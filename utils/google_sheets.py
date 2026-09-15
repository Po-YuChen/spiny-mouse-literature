from io import StringIO

import pandas as pd
import requests
import streamlit as st


SPREADSHEET_ID = "13DkKqRnnBgLVad7uRsFQXTNCrUT46lP69A5w777tvBc"

TABLES_TO_LOAD = [
    "Literature",
    "Datasets",
    "Paper_Keywords",
    "Paper_Species",
    "Paper_Organs",
    "Paper_Omics",
    "Paper_Topics",
    "Paper_Disease_Models",
]


def _csv_url(sheet_name: str) -> str:
    return (
        f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq"
        f"?tqx=out:csv&sheet={sheet_name}"
    )


def _fetch_table(sheet_name: str) -> pd.DataFrame:

    response = requests.get(
        _csv_url(sheet_name),
        timeout=60,
    )

    response.raise_for_status()

    return pd.read_csv(
        StringIO(response.text),
        dtype=str,
        keep_default_na=False,
    )


@st.cache_data(
    ttl=300,
    show_spinner="Loading literature database…",
)
def load_google_sheets():

    data = {}

    for sheet_name in TABLES_TO_LOAD:
        data[sheet_name] = _fetch_table(sheet_name)

    return data


def api_healthcheck():

    literature = _fetch_table("Literature")

    return {
        "ok": True,
        "table": "Literature",
        "count": len(literature),
    }
