import pandas as pd
import openpyxl
import streamlit as st
import plotly.express as px
from SheetFix import *
from convert_df_image import *
from vendeur_phones import *
from operator import itemgetter


st.set_page_config(page_title="Rapport FDV",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )
st.sidebar.header("Options")


uploaded_file = st.sidebar.file_uploader(
    "Choisir un fichier excel.", type="xlsx",)
get_day_work = 24
day_work = 1
if uploaded_file is not None:
    sheet = SheetFix(uploaded_file)
    sheet.fix_the_sheet()
    day_work = sheet.get_day_work


day_work = int(st.sidebar.text_input("day work", value=day_work))
day_rest = int(st.sidebar.text_input("day rest", value=24-day_work))


df = pd.read_excel(
    io='finale.xlsx',
    engine="openpyxl",
    sheet_name=["AGADIR"],

)
som_check = True
vmm_check = False
df = df.get("AGADIR")
list_vendeurs = []
col1,col2=st.sidebar.columns(2)
with col1:
    som_vendeurs = st.checkbox("SOM Vendeurs", value=False)
with col2:
    vmm_vendeurs = st.checkbox("VMM Vendeurs", value=False)
vmm_vendeurs_list=['K91 BAIZ MOHAMED','K81 AISSI SAMIR','035 AKANTOR REDOUAN','Y60 ATOUAOU AIMAD','F77 EL MEZRAOUI YOUSSEF','T45 FAICAL GOUIZID']    
som_vendeurs_list=['K92 DARKAOUI MOHAMED','F78 GHOUSMI MOURAD','D86 ACHAOUI AZIZ','D45 OUARSSASSA YASSINE','Y59 EL GHANMI MOHAMED','T45 FAICAL GOUIZID']
vendeurs = st.sidebar.multiselect(
    'Vendeurs', df["Vendeur"].unique(),
    default=som_vendeurs_list if som_vendeurs else ( vmm_vendeurs_list if vmm_vendeurs else "K92 DARKAOUI MOHAMED")
)
som_vmm=st.sidebar.selectbox("Choisir la famille",["SOM et VMM","SOM","VMM"])

famille = "C.A (ht)"
if som_vmm=="SOM":
    famille = st.sidebar.multiselect(
        "Famille:",
        options=df["Famille"].unique(),
        default=[df["Famille"][index] for index in [0, 1, 2, 6]]
    )
elif som_vmm=="VMM":
    famille = st.sidebar.multiselect(
        "Famille:",
        options=df["Famille"].unique(),
        default=df["Famille"][3:7]
    )
else :
    famille = st.sidebar.multiselect(
        "Famille:",
        options=df["Famille"].unique(),
        default=df["Famille"][0:7]
    )    


all_vendeur_option = st.sidebar.checkbox("All_Vendeur", value=False)
df["Obj TTC"] = df.apply(lambda x: x["OBJ"] * 24*1.2/day_work, axis=1)

df["Rest TTC"] = df.apply(lambda x: (
    x["Obj TTC"] - x["REAL"]*1.2)/day_rest, axis=1)
df["Percent"] = df["Percent"].apply(lambda x: x*100)
# whatsapp_data=df.query("Vendeur==@vendeurs")
whatsapp_data = df
df_levure = df.query("Famille=='LEVURE' & Vendeur==@vendeurs")
df_flan = df.query("Famille=='FLAN' & Vendeur==@vendeurs")
df_bouillon = df.query("Famille=='BOUILLON' & Vendeur==@vendeurs")
df_condiment = df.query("Famille=='CONDIMENTS' & Vendeur==@vendeurs")
df_confiture = df.query("Famille=='CONFITURE' & Vendeur==@vendeurs")
df_conserve = df.query("Famille=='CONSERVES' & Vendeur==@vendeurs")

if all_vendeur_option == False:
    df = df.query("Famille==@famille & Vendeur==@vendeurs & Vendeur!='SOUATI NOUREDDINE' & Vendeur!='CDZ AGADIR DET2' & Vendeur!='VIDE' & Vendeur!='CDZ AGADIR GROS'")
else:
    df = df.query(
        "Famille==@famille  & Vendeur!='SOUATI NOUREDDINE'  & Vendeur!='CDZ AGADIR DET2' & Vendeur!='VIDE' & Vendeur!='CDZ AGADIR GROS'")

    list_vendeurs = df["Vendeur"].unique()


# df["Percent"]=df["Percent"].str[:-1].astype("float")


# all_vendeurs=df["Vendeur"].unique()
df = df.astype({
    "REAL": "int",
            "OBJ": "int",
            "EnCours": "int",
            "Obj TTC": "int",
            "Rest TTC": "int",
            "Percent": "int",

})

st.dataframe(df)
vendeur_ca = (
    df.groupby(by=["Vendeur"]).sum()[["REAL", "OBJ"]].sort_values(by="REAL")
)
ca_vendeur = px.bar(
    vendeur_ca,
    x="REAL",
    y=vendeur_ca.index,
    orientation="h",
    title=f'{famille[0]}',
    color_discrete_sequence=["#0083B8"] * len(vendeur_ca),
    template="plotly_white",
    color='REAL',
    height=300,
    width=500
    

)
# circle=px.pie(df,names=list_vendeurs,values="REAL")

ca_by_vendeur = px.bar(vendeur_ca, y=vendeurs, x=[
    "REAL", "OBJ"], title="CA", barmode='group',height=300,
    width=500)

try:
    col1,col2=st.columns(2)
    with col1:
        st.plotly_chart(ca_vendeur)
    with col2:
        
        st.plotly_chart(ca_by_vendeur)
    

except Exception as e :
    print("an error " +e)
# st.plotly_chart(circle)
df = df.style.applymap(lambda x: "background-color: #ed8269" if x < -10 else ("background-color: #FDCDC3" if x <
                       0 else ("background-color: white" if x == 0 else "background-color: #A1EB0E")), subset=["Percent"])

ca_by_vendeur = px.bar(vendeur_ca, y=vendeurs, x=[
    "REAL", "OBJ"], title="CA", barmode='group')
try:

    if som_vmm=="SOM" or som_vmm=="SOM et VMM":
        col1, col2, col3 = st.columns(3)
        with col1:
            levure_ca = (
    df_levure.groupby(by=["Famille"]).sum()[
        ["REAL", "OBJ"]].sort_values(by="REAL")
)
            ca_by_levure = px.bar(levure_ca, y=vendeurs, x=[
                "REAL", "OBJ"], title="LEVURE", barmode='group', width=400, height=250)
            st.plotly_chart(ca_by_levure)
        with col2:
            flan_ca = (
    df_flan.groupby(by=["Famille"]).sum()[
        ["REAL", "OBJ"]].sort_values(by="REAL")
)
            ca_by_flan = px.bar(flan_ca, y=vendeurs, x=[
                "REAL", "OBJ"], title="FLAN", barmode='group', width=400, height=250)
            st.plotly_chart(ca_by_flan)
        with col3:
            buillon_ca = (
    df_bouillon.groupby(by=["Famille"]).sum()[
        ["REAL", "OBJ"]].sort_values(by="REAL")
)
            ca_by_buillon = px.bar(df_bouillon, y=vendeurs, x=[
                "REAL", "OBJ"], title="BUILLON", barmode='group', width=400, height=250)
            st.plotly_chart(ca_by_buillon)
    if som_vmm=="VMM" or som_vmm=="SOM et VMM":
        col1, col2, col3 = st.columns(3)

        with col1:
            condiment_ca = (
    df_condiment.groupby(by=["Famille"]).sum()[
        ["REAL", "OBJ"]].sort_values(by="REAL")
)
            ca_by_condiment = px.bar(condiment_ca, y=vendeurs, x=[
                "REAL", "OBJ"], title="CONDIMENT", barmode='group', width=400, height=250)
            st.plotly_chart(ca_by_condiment)
        with col2:
            confiture_ca = (
    df_confiture.groupby(by=["Famille"]).sum()[
        ["REAL", "OBJ"]].sort_values(by="REAL")
)
            ca_by_confiture = px.bar(confiture_ca, y=vendeurs, x=[
                "REAL", "OBJ"], title="CONFITURE", barmode='group', width=400, height=250)
            st.plotly_chart(ca_by_confiture)
        with col3:
            conserve_ca = (
    df_conserve.groupby(by=["Famille"]).sum()[
        ["REAL", "OBJ"]].sort_values(by="REAL")
)
            ca_by_conserve = px.bar(conserve_ca, y=vendeurs, x=[
                "REAL", "OBJ"], title="CONSERVE", barmode='group', width=400, height=250)
            st.plotly_chart(ca_by_conserve)
except Exception as e:
    print("an error " + e )

# whatsapp_data=whatsapp_data.data


def send_image():
    for vendeur in vendeurs:

        nv_df = whatsapp_data.query(f"Vendeur== '{vendeur}'")

        #df["Percent"] = df.apply(lambda x:x["Percent"] /100, axis=1)
        nv_df = nv_df.astype({
            "REAL": "int",
            "OBJ": "int",
            "EnCours": "int",
            "Obj TTC": "int",
            "Rest TTC": "int",
            "Percent": "int",


        })
            
        nv_df = nv_df.style.applymap(lambda x: "background-color: #ed8269" if x < -10 else ("background-color: #FDCDC3" if x <
                                     0 else ("background-color: white" if x == 0 else "background-color: #A1EB0E")), subset=["Percent"])
        

        send_image = SendImageToFDV(nv_df, vendeur)
        send_image.send_df_image()


st.sidebar.button("Send df..", on_click=send_image)

# if uploaded_file is not None:
# sheet=SheetFix()
# sheet.fix_the_sheet(uploaded_file)
