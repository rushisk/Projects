import requests
import pandas as pd
import io
import datetime
import os

def fetch_data(api_key,from_date,to_date):
    api_key = api_key
    url = "https://api.eflow.team/v1/affiliates/reporting/entity/table/export"
    payload = {
        "from": from_date.isoformat(),
        "to": to_date.isoformat(),
        "timezone_id": 80,
        "currency_id": "USD",
        "columns": [
            {
                "column": "offer"
            }
        ],
        "query": {
            "filters": []
        },
        "format": "csv"
    }
    headers = {
        'Content-Type': "application/json",
        'x-eflow-api-key': api_key
    }

    res = requests.post(url, json=payload, headers=headers)
    data_str = res.content.decode("utf-8")
    df = pd.read_csv(io.StringIO(data_str))
    return df


def main(from_date,to_date):  
    from_date = from_date
    to_date = to_date
    current_path = os.getcwd()

    file_name = str(from_date)+"_to_"+str(to_date)+".xlsx"
    i = 0
    while os.path.isfile(os.path.join(current_path,file_name)):
        i += 1
        file_name = f"{file_name}_{i}.xlsx"
    api_keys = {'ID 2': 'API_Key' , 'ID 3': 'API_Key', 'ID 4':'API_Key', 'ID 5':'API_Key', 'ID 6': 'API_Key', 'ID 7':'API_Key', 'ID 8':'API_Key', 'ID 9': 'API_Key'}
    
    with pd.ExcelWriter(os.path.join(current_path,file_name)) as writer:
        for key in api_keys:
            try:
                df = fetch_data(api_keys[key],from_date,to_date)

                if df.empty:
                    df = pd.DataFrame({'msg':['None data']})

                else: 
                    df.to_excel(writer, sheet_name=key, index = False)
            
            except pd.errors.EmptyDataError:
                df = pd.DataFrame({'msg':['none data']})



if __name__ == "__main__":

    def Last_month():
        today = datetime.date.today()
        last_date= today.replace(day=1) - datetime.timedelta(days = 1)
        from_date = last_date.replace(day = 1)
        return(from_date, last_date)


    def MTD():
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        from_date = yesterday.replace(day = 1)
        return(from_date, yesterday)
    
    def Yesterday_func():
        yesterday = datetime.date.today() - datetime.timedelta(days = 1)
        from_date = yesterday
        return(from_date, yesterday)
        
    print("Select date option from below for which you want to download data.\n")
    option = input("1. Yesterday \n2.Month to date \n3. Last Month \n")
    
    if option == '1':
        from_date, to_date = Yesterday_func()
        print(f"Your Selected Date:  {from_date} \t {to_date}")
        main(from_date, to_date)
    
    elif option == '2':
        from_date,to_date= MTD()
        print(f"Your Selected Date:  {from_date} \t {to_date}")
        main(from_date,to_date)
    
    elif option == '3':
        from_date, to_date = Last_month()
        print(f"Your Selected Date:  {from_date} \t {to_date}")
        main(from_date,to_date)
     
    else:
        print("Enter Valid input")
        
