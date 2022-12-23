#This program extracts IP addresses and email addresses from Excel/CSV files.
#This code can run with multiple tabs in single excel file

import os
import pandas as pd

import re
#regex = r"^(([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,18}(?:\.[a-z]{2})?))$"

#regex = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'

path = "."
files = os.listdir(path)
print(files)
files_xls = [f for f in files if f[-4:] == 'xlsx']
files_xls.sort(key=lambda x: os.path.getmtime(x), reverse=True)
os.chdir(path)
df_email = pd.DataFrame()
for i in range(1): #Read the excel file with the most recent modified timestamp
    print(files_xls[i])

    xls = pd.ExcelFile(files_xls[i])
    for sheet in xls.sheet_names:
        df = pd.read_excel(files_xls[i], sheet_name=sheet)

        for row in df.values.tolist():
            for col in row:
                matches = re.findall(regex, str(col))
                if matches:
                    df_email = df_email.append([matches[0]], ignore_index=True)
#print(df_email)
#df_email.columns = ['email_id', 'username', 'isp', 'domain']
df_email.to_csv(r'C:\Users\rushikeshk\Desktop\test\test2\file1.csv', index=False)
