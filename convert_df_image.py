import dataframe_image as dfi
import pywhatkit as whatsapp 
from datetime import date
from vendeur_phones import *



class SendImageToFDV:
    def __init__(self,df,fdv):
        self.df=df
        self.fdv=fdv
        
    def send_df_image(self):
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        dfi.export(self.df,f"images/{self.fdv}.jpg")
        whatsapp.sendwhats_image(vendeur_number_phone[self.fdv],f"images/{self.fdv}.jpg",d1,10)
        print("Image sent successfully")
            
            