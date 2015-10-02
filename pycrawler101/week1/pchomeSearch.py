'''
Created on Oct 3, 2015

@author: c3h3
'''

from pycrawler101.errors import NotFindDataError
import requests
import pandas as pd


def getData(q, page=1):
    url = "http://ecshweb.pchome.com.tw/search/v3.3/all/results?q={q}&page={page}".format(q=q,page=page)
    res = requests.get(url)
    res.raise_for_status()
    df = pd.DataFrame(res.json()["prods"])
    
    return df
    