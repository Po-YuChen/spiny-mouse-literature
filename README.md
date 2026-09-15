
# Spiny Mouse Literature Database — Apps Script API MVP

This Streamlit MVP reads the public, read-only Apps Script API connected to
`Spiny_Mouse_Literature_Database_MASTER`.

## API endpoint

`https://script.google.com/macros/s/AKfycbwsEhpib0ZP7PaNXv6oucfYCqQN1HlgorIN2BIxF633_-SGVJ14ht8902tvQm_y3fGn/exec`

## Architecture

Google Sheets MASTER
→ Google Apps Script read-only JSON API
→ Streamlit website

No service-account JSON key is required.

## Public tables

The API is expected to expose only:

- Literature
- Datasets
- Paper_Keywords
- Paper_Species
- Paper_Organs
- Paper_Omics
- Paper_Topics
- Paper_Disease_Models

`Literature` should expose only `Record_Status = Active`.
Relation tables should expose only rows linked to Active publications.

## Local run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

macOS/Linux activation:

```bash
source .venv/bin/activate
```

## Deploy to Streamlit Community Cloud

1. Push this project folder to GitHub.
2. Create a new Streamlit Community Cloud app.
3. Select the repository and `app.py`.
4. Deploy.

No Streamlit Secrets are needed for the current public read-only API design.

## Caching

Streamlit caches API responses for 5 minutes:

```python
@st.cache_data(ttl=300)
```

The Apps Script side also caches results for 5 minutes.

## If the Apps Script deployment changes

Replace `API_BASE_URL` in:

`utils/google_sheets.py`

with the new `/exec` URL.
