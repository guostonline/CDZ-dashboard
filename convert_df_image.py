import dataframe_image as dfi
import pywhatkit as whatsapp 
from datetime import date
import time
import streamlit as st
from vendeur_phones import *



class SendImageToFDV:
    def __init__(self,df,fdv):
        self.df=df
        self.fdv=fdv
        
    def send_df_image(self):
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        with st.spinner('Wait for it...'):
            time.sleep(5)
            st.success('Done!')
        dfi.export(self.df,f"images/{self.fdv}_obj.jpg")
        whatsapp.sendwhats_image(vendeur_number_phone[self.fdv],f"images/{self.fdv}.jpg",d1,10)
        st.spinner(text="In progress...")
        print("Image sent successfully")
            
            