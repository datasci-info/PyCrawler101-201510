'''
Created on Oct 17, 2015

@author: c3h3
'''

import requests
from lxml import etree
import lxml.html
from HTMLParser import HTMLParser
import pandas as pd
parser = HTMLParser()


def getData():
    url = "http://news.cnyes.com/headline_channel/list.shtml"
    urls = listNewsUrls(url)
    data  = map(getNewsData,urls)
    df = pd.DataFrame(data)
    return df

def getNewsData(url):
    res = requests.get(url)
    res.encoding = "utf8"
    doc = etree.HTML(res.text)
    
    data = {"title":doc.xpath("//div[@class='newsContent bg_newsPage_Lblue']/h1")[0].text,
            "info": doc.xpath("//div[@class='newsContent bg_newsPage_Lblue']/div[@class='info']")[0].text,
            "url":url}
    
    e = doc.xpath("//div[@class='newsContent bg_newsPage_Lblue']/div[@id='newsText']")[0]
    data["body"] = parser.unescape(lxml.html.tostring(e))
    return dat

def listNewsUrls(url):
    res = requests.get(url)
    doc = etree.HTML(res.text)
    urls = map(lambda e:e.attrib["href"], doc.xpath("//ul[@class='list_1 bd_dbottom']//li/a"))
    return urls 
    a