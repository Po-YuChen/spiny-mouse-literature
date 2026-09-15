
import pandas as pd
import requests
import streamlit as st

API_BASE_URL = "https://script.google.com/macros/s/AKfycbwsEhpib0ZP7PaNXv6oucfYCqQN1HlgorIN2BIxF633_-SGVJ14ht8902tvQm_y3fGn/exec"

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

def _fetch_table(table_name: str) -> pd.DataFrame:
    response = requests.get(
        API_BASE_URL,
        params={"table": table_name},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    if not payload.get("ok"):
        raise RuntimeError(
            f"Apps Script API error for {table_name}: "
            f"{payload.get('error', 'unknown error')}"
        )

    rows = payload.get("data", [])
    return pd.DataFrame(rows)

@st.cache_data(ttl=300, show_spinner="Loading literature database…")
def load_google_sheets():
    data = {}
    for table in TABLES_TO_LOAD:
        data[table] = _fetch_table(table)
    return data

def api_healthcheck():
    """Return a lightweight status payload from the Literature endpoint."""
    response = requests.get(
        API_BASE_URL,
        params={"table": "Literature"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
