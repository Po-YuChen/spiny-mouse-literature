import pandas as pd
import streamlit as st
from utils.google_sheets import load_google_sheets
from utils.database import enrich_literature

st.set_page_config(page_title="Omics & Datasets", page_icon="🧬", layout="wide")
st.title("Omics & Public Datasets")
data=load_google_sheets(); lit=enrich_literature(data); ds=data["Datasets"].copy()
small=lit[["Literature_ID","Title","Year","Journal","_species","_organs"]]
m=ds.merge(small,on="Literature_ID",how="left")
c1,c2,c3=st.columns(3)
dbs=c1.multiselect("Repository",sorted(m["Database"].dropna().unique()))
oms=c2.multiselect("Omics type",sorted(m["Omics_Type"].dropna().unique()))
q=c3.text_input("Search accession or publication")
mask=pd.Series(True,index=m.index)
if dbs: mask &= m["Database"].isin(dbs)
if oms: mask &= m["Omics_Type"].isin(oms)
if q.strip():
    q=q.lower().strip()
    mask &= m.apply(lambda r:q in " ".join([str(r.get("Accession","")),str(r.get("Title","")),str(r.get("PMID",""))]).lower(),axis=1)
res=m[mask]
st.write(f"**{len(res):,} dataset records found**")
for _,r in res.iterrows():
    st.markdown(f"### {r.get('Accession','')}")
    st.write(f"**{r.get('Omics_Type','')}** · {r.get('Database','')}")
    st.write(f"Associated publication: **{r.get('Title','')}**")
    st.caption(f"{r.get('Year','')} · {r.get('Journal','')} · Species: {', '.join(r.get('_species',[]) or [])} · Organ: {', '.join(r.get('_organs',[]) or [])}")
    if str(r.get("Dataset_URL","")).strip():
        st.link_button("Open public dataset",r["Dataset_URL"])
    st.divider()
