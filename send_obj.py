import pandas 
import pywhatkit as whatsapp 
import dataframe_image as dfi
from vendeur_phones import vendeur_number_phone

class SendObjectif:
    def __init__(self,excel,fdv):
        self.excel =excel
        self.fdv =fdv
        
    def send_obj(self):
        
        dfi.export(self.df,f"images/{self.fdv}_obj.jpg")
        whatsapp.sendwhats_image(vendeur_number_phone[self.fdv],f"images/{self.fdv}_obj.jpg","Objectif",10) 
    
    def prepare_file(self):
        df = pandas.read_excel(
        io=self.excel,
        engine="openpyxl",
        skiprows=1,
        usecols=['SECTEUR','FAM',' DEC 2021',"DEC 2022","evol"],
       
        
)   
        df=df.get("base")
        df=df.astype({
            " DEC 2021":"float",
            "DEC 2022":"float"
            
        })
        df["evol"]=(df[" DEC 2021"]/ df['DEC 2022'])-1
        
        print(df)
        
         