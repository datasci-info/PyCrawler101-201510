'''
Created on Oct 3, 2015

@author: c3h3
'''

import requests
import pandas as pd

def getData(marketID="sii"):
    limitIDs = ["sii","otc","rotc","pub"]
    assert marketID in limitIDs
     
    postData = {"encodeURIComponent":1,
                "step":1,
                "firstin":1,
                "TYPEK":marketID,
                "code":""}
    
    res = requests.post("http://mops.twse.com.tw/mops/web/ajax_t51sb01",data=postData)
    res.raise_for_status()
    res.encoding = "utf8"
    df = pd.read_html(res.text)[0]
    columns = df.iloc[0]
    df = df[df[0].str.match("[0-9]+")]
    df.columns = columns
    
    return df
    