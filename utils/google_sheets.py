import html
import json
import re

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
    text = response.text.strip()

    # Case 1: normal JSON
    try:
        return response.json()
    except Exception:
        pass

    # Case 2: HtmlService wraps JSON inside HTML
    body_match = re.search(
        r"<body[^>]*>(.*?)</body>",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if body_match:
        text = body_match.group(1)

    # Remove remaining HTML tags if present
    text = re.sub(r"<[^>]+>", "", text)

    # Decode HTML entities
    text = html.unescape(text).strip()

    # Find JSON object boundaries
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise RuntimeError(
            "Apps Script returned a response, but no JSON object was found. "
            f"First 300 characters: {response.text[:300]}"
        )

    json_text = text[start:end + 1]

    return json.loads(json_text)


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
