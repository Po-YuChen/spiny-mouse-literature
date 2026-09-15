import html
import json

import pandas as pd
import requests
import streamlit as st


API_BASE_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbwsEhpib0ZP7PaNXv6oucfYCqQN1HlgorIN2BIxF633_-SGVJ14ht8902tvQm_y3fGn"
    "/exec"
)


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


def _parse_response(response):

    # First try normal JSON
    try:
        return response.json()
    except Exception:
        pass

    # HtmlService may encode JSON as HTML text
    text = html.unescape(response.text)

    # Look specifically for our API JSON object
    start = text.find('{"ok":')

    if start == -1:
        raise RuntimeError(
            "Apps Script returned content, but the API JSON "
            "could not be located. "
            f"First 500 characters: {response.text[:500]}"
        )

    # Parse exactly one JSON object.
    # This safely ignores any HTML / JavaScript after it.
    decoder = json.JSONDecoder()

    try:
        payload, _ = decoder.raw_decode(text[start:])
        return payload

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Apps Script response contained API JSON, "
            f"but it could not be decoded: {exc}. "
            f"Response around JSON: {text[start:start+500]}"
        )


def _fetch_table(table_name: str) -> pd.DataFrame:

    response = requests.get(
        API_BASE_URL,
        params={"table": table_name},
        timeout=60,
    )

    response.raise_for_status()

    payload = _parse_response(response)

    if not payload.get("ok"):
        raise RuntimeError(
            f"Apps Script API error for {table_name}: "
            f"{payload.get('error', 'unknown error')}"
        )

    rows = payload.get("data", [])

    return pd.DataFrame(rows)


@st.cache_data(
    ttl=300,
    show_spinner="Loading literature database…",
)
def load_google_sheets():

    data = {}

    for table in TABLES_TO_LOAD:
        data[table] = _fetch_table(table)

    return data


def api_healthcheck():

    response = requests.get(
        API_BASE_URL,
        params={"table": "Literature"},
        timeout=60,
    )

    response.raise_for_status()

    return _parse_response(response)
