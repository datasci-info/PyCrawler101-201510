'''
Created on Oct 17, 2015

@author: c3h3
'''

import requests
from lxml import etree
import pandas as pd


def getData():
    #TODO: get all cities!
    city = u"台北市"
    dfs = [getStoreData(city,t) for t in ls_town_df("01")["TownName"]]
    return pd.concat(dfs)

def ls_town_df(cityId="01"):
    postData = {"commandid":"GetTown",
                "cityid":cityId}
    res = requests.post("http://emap.pcsc.com.tw/EMapSDK.aspx",data=postData)
    doc = etree.fromstring(res.text.encode("utf8"))
    data = map(lambda e:dict([(c.tag,c.text) for c in e.iterchildren()]),  doc.xpath("//GeoPosition"))
    df = pd.DataFrame(data)
    return df

def getStoreData(city = u"台北市", town = u"大安區"):
    postData = {"commandid" : "SearchStore",
                "city" : city,
                "town": town}

    res = requests.post("http://emap.pcsc.com.tw/EMapSDK.aspx",data=postData)
    doc = etree.fromstring(res.text.encode("utf8"))
    data = map(lambda e:dict([(c.tag,c.text) for c in e.iterchildren()]),  doc.xpath("//GeoPosition"))
    df = pd.DataFrame(data)
    return df 
