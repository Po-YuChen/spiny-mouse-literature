import streamlit as st
from utils.google_sheets import load_google_sheets
from utils.database import enrich_literature, filter_literature
from utils.ui import publication_card

st.set_page_config(page_title="Literature | Spiny Mouse Database", page_icon="🔎", layout="wide")
st.title("Literature Search")
data=load_google_sheets(); lit=enrich_literature(data)
q=st.text_input("Search literature", placeholder="e.g. kidney regeneration, macrophage, scRNA-seq")
with st.expander("Filters", expanded=True):
    r1=st.columns(4)
    years=r1[0].multiselect("Year", sorted(lit["Year"].astype(str).unique(), reverse=True))
    topics=r1[1].multiselect("Topic", sorted(set(sum(lit["_topics"].tolist(),[]))))
    species=r1[2].multiselect("Species", sorted(set(sum(lit["_species"].tolist(),[]))))
    organs=r1[3].multiselect("Organ", sorted(set(sum(lit["_organs"].tolist(),[]))))
    r2=st.columns(4)
    disease=r2[0].multiselect("Disease model", sorted(set(sum(lit["_disease_models"].tolist(),[]))))
    omics=r2[1].multiselect("Omics", sorted(set(sum(lit["_omics"].tolist(),[]))))
    article_types=r2[2].multiselect("Article type", sorted(lit["Article_Type"].dropna().unique()))
    has_dataset=r2[3].toggle("Has public dataset")
res=filter_literature(lit,q,years,topics,species,organs,disease,omics,article_types,has_dataset)
st.write(f"**{len(res):,} publications found**")
page_size=st.selectbox("Results per page",[10,20,50],index=1)
pages=max(1,(len(res)+page_size-1)//page_size)
page=st.number_input("Page",1,pages,1)
for _,row in res.iloc[(page-1)*page_size:page*page_size].iterrows():
    publication_card(row); st.divider()
