import pandas as pd
import openpyxl
import dataframe_image
import streamlit as st
from SheetFix import *
from convert_df_image import *
from vendeur_phones import *



st.set_page_config(page_title="Rapport FDV",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )
st.sidebar.header("Options")



uploaded_file = st.sidebar.file_uploader(
    "Choisir un fichier excel.", type="xlsx",)
get_day_work=24
day_work=1
if uploaded_file is not None:
    sheet = SheetFix(uploaded_file)
    sheet.fix_the_sheet()
    day_work= sheet.get_day_work
    
    
day_work = int(st.sidebar.text_input("day work", value=day_work))    
day_rest = int(st.sidebar.text_input("day rest", value=24-day_work))   


df = pd.read_excel(
    io='finale.xlsx',
    engine="openpyxl",
    sheet_name=["AGADIR"],

)

df = df.get("AGADIR")

vendeurs=st.sidebar.multiselect('Vendeurs',df["Vendeur"].unique(),default="K92 DARKAOUI MOHAMED")
all_vendeur_option=st.sidebar.checkbox("All_Vendeur",value=True)
if all_vendeur_option==False:
    
    df=df.query("Vendeur== @vendeurs")

df["Obj TTC"] = df.apply(lambda x: x["OBJ"] * 24*1.2/day_work, axis=1)

df["Rest TTC"] = df.apply(lambda x: (x["Obj TTC"] - x["REAL"]*1.2)/day_rest, axis=1)
df["Percent"] = df["Percent"].apply(lambda x:x*100 ) 
#df["Percent"]=df["Percent"].str[:-1].astype("float")

print(df)

# all_vendeurs=df["Vendeur"].unique()
df = df.astype({
            "REAL": "int",
            "OBJ": "int",
            "EnCours": "int",
            "Obj TTC": "int",
            "Rest TTC": "int",
            "Percent": "int",
            
})
#df['Pourcent'] = df['Pourcent'].str.rstrip('%').astype('float') / 100.0

df=df.style.applymap(lambda x: "background-color: #ed8269" if x< -10 else ( "background-color: #FDCDC3" if x<0 else ("background-color: white" if x==0 else "background-color: #A1EB0E" )), subset=["Percent"])
#df=df.style.format({"Percent":"{:.0%}"})



#
st.dataframe(df)
df=df.data

def send_image():
    for vendeur in vendeurs:
       
        nv_df=df.query(f"Vendeur== '{vendeur}'")
        
        
        #df["Percent"] = df.apply(lambda x:x["Percent"] /100, axis=1)
        nv_df=nv_df.astype({
            "REAL":"int",
            "OBJ":"int",
            "EnCours":"int",
            "Obj TTC":"int",
            "Rest TTC":"int",
            
            
        })
        
        #nv_df=nv_df.style.format({"Pourcent":"{:.0%}"})
        
        nv_df=nv_df.style.applymap(lambda x: "background-color: #ed8269" if x< -10 else ( "background-color: #FDCDC3" if x<0 else ("background-color: white" if x==0 else "background-color: #A1EB0E" )), subset=["Percent"])
        
        send_image=SendImageToFDV(nv_df,vendeur)
        send_image.send_df_image()
st.sidebar.button("Send df..",on_click=send_image)

# if uploaded_file is not None:
# sheet=SheetFix()
# sheet.fix_the_sheet(uploaded_file)
