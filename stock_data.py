import requests
import pandas as pd
from datetime import datetime
from time import sleep
import schedule
import matplotlib.pyplot as plt
import threading
from matplotlib.animation import FuncAnimation

url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9'
}


session = requests.Session()
request = session.get(url,headers = headers)
cookies1 = dict(request.cookies)
response = session.get(url, headers = headers, cookies=cookies1).json()
rawdata = pd.DataFrame(response)
rawop = pd.DataFrame(rawdata['filtered']['data']).fillna(0)
#get_livedta = pd.DataFrame(rawdata['filtered']['data']).fillna(0)
ulvalue = rawdata['records']['underlyingValue']
print("Underlying Value",ulvalue)


def importdata():
    requests = session.get(url,headers=headers)
    cookiess = dict(requests.cookies)
    responses = session.get(url, headers=headers, cookies=cookiess).json()	
    rdata = pd.DataFrame(responses)
    live_raw = pd.DataFrame(rdata['filtered']['data']).fillna(0)
    return live_raw

def dataframe(rawop):
    data = []
    for i in range(0,len(rawop)):       #put underlying value condition to minimize data
        calloi = callcoi = cltp = putoi = putcoi = pltp = 0
        stp = rawop['strikePrice'][i]      
        
        if(rawop['CE'][i]==0):
            calloi = callcoi =0
            
        else:
            calloi = rawop['CE'][i]['openInterest']
            callcoi = rawop['CE'][i]['changeinOpenInterest']
            cltp = rawop['CE'][i]['lastPrice']
            
        if(rawop['PE'][i] == 0):
            putoi = putcoi = 0
        
        else:
            putoi = rawop['PE'][i]['openInterest']
            putcoi = rawop['PE'][i]['changeinOpenInterest']
            pltp = rawop['PE'][i]['lastPrice']
            
        opdata = {
                 'CALL OI':calloi, 'CALL CHANGE OI': callcoi, 'CALL LTP':cltp,'STRIKE PRICE':stp,
                'PUT OI':putoi, 'PUT CHANGE OI':putcoi, 'PUT LTP':pltp
                }
        data.append(opdata)
        
    optionchain = pd.DataFrame(data)
    return optionchain

get_livedata = importdata()

def dataframe1(get_livedata):         #same function for repitative call
    data1 = []
    for i1 in range(0,len(get_livedata)):       #put underlying value condition to minimize data
        calloi1 = callcoi1 = cltp1 = putoi1 = putcoi1 = pltp1 = 0
        stp1 = get_livedata['strikePrice'][i1]
        nows1 = datetime.now().time()
        current_time1 = nows1.isoformat(timespec = 'minutes')
        
        
        if(get_livedata['CE'][i1]==0):
            calloi1 = callcoi1 =0
            
        else:
            calloi1 = get_livedata['CE'][i1]['openInterest']
            callcoi1 = get_livedata['CE'][i1]['changeinOpenInterest']
            cltp1 = get_livedata['CE'][i1]['lastPrice']
            
        if(get_livedata['PE'][i1] == 0):
            putoi1 = putcoi1 = 0
        
        else:
            putoi1 = get_livedata['PE'][i1]['openInterest']
            putcoi1 = get_livedata['PE'][i1]['changeinOpenInterest']
            pltp1 = get_livedata['PE'][i1]['lastPrice']
            
        opdata1 = {
                 'TIME':current_time1,'CALL OI':calloi1, 'CALL CHANGE OI': callcoi1, 'CALL LTP':cltp1,'STRIKE PRICE':stp1,
                'PUT OI':putoi1, 'PUT CHANGE OI':putcoi1, 'PUT LTP':pltp1
                }
        data1.append(opdata1)
        
    optionchain1 = pd.DataFrame(data1)
    return optionchain1



def strprice():
        global ce_from
        global ce_to
        global pe_from
        global pe_to
        global ce_list
        global pe_list
        global temp_time
        optionchains = dataframe(rawop)
        sprice = optionchains['STRIKE PRICE']

        close_number = min(sprice, key=lambda x:abs(int (x)-ulvalue))
        print("close nummber",close_number)

        row_number = optionchains[optionchains['STRIKE PRICE'] == close_number].index[0]
        ce_from = row_number - 5
        ce_to = row_number + 10
        ce_spd = optionchains.loc[ce_from:ce_to,['STRIKE PRICE']]
        ce_spd['STRIKE PRICE'] = 'CE'+'_'+ce_spd['STRIKE PRICE'].map(str) 
        op2= ce_spd['STRIKE PRICE'].tolist()
        ce_list = {l:[] for l in op2}
        #print(op2)

        pe_from = row_number - 10
        pe_to = row_number + 5
        pe_spd = optionchains.loc[pe_from:pe_to,['STRIKE PRICE']]
        pe_spd['STRIKE PRICE'] = 'PE'+'_'+pe_spd['STRIKE PRICE'].map(str)
        op3 = pe_spd['STRIKE PRICE'].tolist()
        pe_list = {k:[] for k in op3}       #creating empty dictionary of list
        #print(op3)
        temp_time = {'TIME':[]}
        
strprice()

def todictionary():
    nows = datetime.now().time()
    current_time = nows.isoformat(timespec = 'minutes')
    opchain = dataframe1(get_livedata)
    opchain = opchain.reindex(columns=['STRIKE PRICE','CALL OI','CALL CHANGE OI','CALL LTP','PUT OI','PUT CHANGE OI','PUT LTP','TIME']) #customizing index of dataframe
    #print(opchain)
    ce_livedata = opchain.loc[ce_from:ce_to,['STRIKE PRICE','CALL CHANGE OI']]
    pe_livedata = opchain.loc[pe_from:pe_to,['STRIKE PRICE','PUT CHANGE OI']]

    op_ce = ce_livedata[['STRIKE PRICE', 'CALL CHANGE OI']]
    op_ce = op_ce.set_index('STRIKE PRICE').T.to_dict('list')
    opce_dict = pd.DataFrame(op_ce)      #converting to datafrom to match column name and get the row value to another table

    op_pe = pe_livedata[['STRIKE PRICE', 'PUT CHANGE OI']]
    op_pe = op_pe.set_index('STRIKE PRICE').T.to_dict('list')             
    oppe_dict = pd.DataFrame(op_pe)    
            
    temp_time['TIME'].append(current_time)
    print(temp_time)

    for column_ce in opce_dict.columns:
        for value_ce in opce_dict[column_ce].values:
            ce_list['CE_'+str(column_ce)].append(value_ce)


    for column_pe in oppe_dict.columns:
        for value_pe in oppe_dict[column_pe].values:
            pe_list['PE_'+str(column_pe)].append(value_pe)        
            
    res_dict = {}
    for d in (temp_time,ce_list,pe_list):res_dict.update(d)
            
    return res_dict

def rep():
    threading.Timer(180.0,rep).start()
    temp_var = todictionary()
    final_dataframe = pd.DataFrame(temp_var)
    print(final_dataframe)

rep()
