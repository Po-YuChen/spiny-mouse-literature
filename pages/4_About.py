import streamlit as st
st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")
st.title("About this database")
st.markdown("""
The **Spiny Mouse Literature Database** is a curated resource for publications involving *Acomys* / spiny mice.

### Data model
One primary record per publication (`Literature_ID`) plus normalized relation tables for species, organs, omics, disease models, keywords, topics, and public datasets.

### Curation
Display fields are for human-readable presentation. Website filters and statistics use normalized relation tables.

### Update workflow
Google Sheets is the editing backend. Only `Record_Status = Active` records appear publicly. The website is read-only and refreshes cached data every 5 minutes.
""")
