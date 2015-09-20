'''
Created on Sep 20, 2015

@author: c3h3
'''

from pycrawler101.errors import NotFindDataError

import requests
import re
from datetime import datetime
import pandas as pd
import numpy as np


def yahooStockMajor(stock_id):
    url = "https://tw.stock.yahoo.com/d/s/major_{stock_id}.html".format(stock_id=stock_id)
    res = requests.get(url)
    res.raise_for_status()
    
    tables = pd.read_html(res.text)
    filtered_tables = filter(lambda xx:xx.shape[1] == 8, tables)
    if len(filtered_tables) == 0:
        raise NotFindDataError(url)
    else:
        df = filter(lambda xx:xx.shape[1] == 8, tables)[0]
    
    df = pd.DataFrame(np.r_[df.values[1:,0:3], df.values[1:,4:7]],columns=["broker","long","short"])
    
    pat = re.compile(u"([0-9]+ /[0-9]+ /[0-9]+)")
    date = map(int,pat.findall(res.text)[0].split("/"))
    date[0] = 1911 + date[0]
    date = datetime(*date)
    
    df["stock_id"] = stock_id
    df["date"] = date
    
    df = df[["date","stock_id", "broker","long","short"]]
    
    return df
    
    