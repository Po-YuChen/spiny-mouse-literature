import plotly.express as px
import streamlit as st
from utils.google_sheets import load_google_sheets
from utils.database import enrich_literature

st.set_page_config(page_title="Statistics", page_icon="📊", layout="wide")
st.title("Statistics")
data=load_google_sheets(); lit=enrich_literature(data)

def counts(col,label):
    t=lit[["Literature_ID",col]].explode(col)
    t=t[t[col].astype(str).ne("")]
    return t.groupby(col)["Literature_ID"].nunique().sort_values(ascending=False).rename("Publications").reset_index().rename(columns={col:label})

y=lit.dropna(subset=["Year_num"]).groupby("Year_num")["Literature_ID"].nunique().reset_index(name="Publications").sort_values("Year_num")
y["Year"]=y["Year_num"].astype(int).astype(str)
st.plotly_chart(px.line(y,x="Year",y="Publications",markers=True,title="Publications over time"),use_container_width=True)

a,b=st.columns(2)
t=counts("_topics","Topic").head(15)
a.plotly_chart(px.bar(t.sort_values("Publications"),x="Publications",y="Topic",orientation="h",title="Publications by topic"),use_container_width=True)
o=counts("_organs","Organ").head(15)
b.plotly_chart(px.bar(o.sort_values("Publications"),x="Publications",y="Organ",orientation="h",title="Most studied organs / tissues"),use_container_width=True)

c,d=st.columns(2)
s=counts("_species","Species").head(15)
c.plotly_chart(px.bar(s.sort_values("Publications"),x="Publications",y="Species",orientation="h",title="Species distribution"),use_container_width=True)
dm=counts("_disease_models","Disease model").head(15)
d.plotly_chart(px.bar(dm.sort_values("Publications"),x="Publications",y="Disease model",orientation="h",title="Disease / experimental model categories"),use_container_width=True)

e,f=st.columns(2)
om=counts("_omics","Omics type")
e.plotly_chart(px.bar(om.sort_values("Publications"),x="Publications",y="Omics type",orientation="h",title="Omics technologies"),use_container_width=True)
ds=data["Datasets"]
if not ds.empty:
    rp=ds.groupby("Database")["Dataset_ID"].nunique().sort_values().reset_index(name="Datasets")
    f.plotly_chart(px.bar(rp,x="Datasets",y="Database",orientation="h",title="Public datasets by repository"),use_container_width=True)
