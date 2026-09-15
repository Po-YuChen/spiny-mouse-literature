import streamlit as st
from utils.google_sheets import load_google_sheets
from utils.database import enrich_literature

st.set_page_config(page_title="Spiny Mouse Literature Database", page_icon="🐭", layout="wide")
st.title("Spiny Mouse Literature Database")
st.caption("A curated resource for Acomys research, disease models, regeneration, and public omics datasets.")

try:
    data=load_google_sheets()
    lit=enrich_literature(data)
except Exception as e:
    st.error("The website could not read the Apps Script API.")
    st.code(str(e))
    st.info("Check that the Apps Script Web App is deployed, accessible, and the API URL is current.")
    st.stop()

a,b,c,d=st.columns(4)
a.metric("Publications", f"{len(lit):,}")
b.metric("Research topics", f"{len(set(sum(lit['_topics'].tolist(),[]))):,}")
c.metric("Omics-linked papers", f"{int(lit['_omics'].map(bool).sum()):,}")
d.metric("Public dataset records", f"{len(data['Datasets']):,}")
st.divider()
st.subheader("Explore the database")
st.page_link("pages/1_Literature.py", label="Search literature", icon="🔎")
st.page_link("pages/2_Omics_Datasets.py", label="Explore omics & datasets", icon="🧬")
st.page_link("pages/3_Statistics.py", label="View statistics", icon="📊")
