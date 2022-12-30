import os
import pandas as pd
import glob
import re
from tkinter import filedialog, Tk

regex = r"^(([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,18}(?:\.[a-z]{2})?))$"

#regex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

path = os.getcwd()
files = glob.glob(os.path.join(path,"*.xlsx"))

df_email = pd.DataFrame()
for f in files:
    df=pd.read_excel(f)
    
    for row in df.values.tolist():
        for col in row:
            matches = re.findall(regex, str(col))
            if matches:
                df_email = df_email.append([matches[0]], ignore_index=True)
 
df_email.columns = ['email_id', 'username', 'isp', 'domain'] 

root = Tk()  # this is to close the dialogue box later     
try:
    # with block automatically closes file
    with filedialog.asksaveasfile(mode='w', defaultextension=".xlsx") as file:
        df_email.to_excel(file.name, index=False)
        
except AttributeError:
    # if user cancels save, filedialog returns None rather than a file object, and the 'with' will raise an error
    print("The user cancelled save")
    
root.destroy() # close the dialogue box

