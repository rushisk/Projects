import re
import os
import sys
import pandas as pd


base_dir = os.getcwd()
email_regex = r"^(([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,18}(?:\.[a-z]{2})?))$"
ip_regex = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'


def get_email():
    df_email = pd.DataFrame()
    all_files = os.listdir(input_dir)
    for entry in all_files:
        if entry.endswith(".xlsx"):    
            df = pd.read_excel(os.path.join(input_dir,entry))
            for row in df.values.tolist():
                for col in row:
                    email_matches = re.findall(email_regex, str(col))
                    if email_matches:
                        df_email = df_email.append([email_matches[0]], ignore_index=True)
            df_email.columns = ['email_id', 'username', 'isp', 'domain'] 
            df_email.to_excel(result_file, index=False)


def get_ip():
    df_ip = pd.DataFrame()
    all_files = os.listdir(input_dir)
    for entry in all_files:
        if entry.endswith(".xlsx"):
            df = pd.read_excel(os.path.join(input_dir,entry))
            for row in df.values.tolist():
                for col in row:
                    ip_matches = re.findall(ip_regex, str(col))
                    if ip_matches:
                        df_ip = df_ip.append([ip_matches[0]], ignore_index=True)
            df_ip.columns = ['ip address'] 
            df_ip.to_excel(result_file, index=False)


user_file_name = input('Enter result file name:\t')
if not user_file_name.endswith(".xlsx"):
    user_file_name = user_file_name + ".xlsx"
result_file = os.path.join(base_dir, user_file_name)

input_dir = os.path.join(base_dir, "input")
try:
    user_option = int(input("What do you want to grep:\n1]IP->press 1\n2]Email->press 2\nYour choice:\t"))
except Exception:
    print("You are not entering INT values:\t")
    sys.exit()
if user_option == 1:
    get_email()    
elif user_option == 2:
    get_ip()    
else:
    print("Your choice is not OK, redo..")

