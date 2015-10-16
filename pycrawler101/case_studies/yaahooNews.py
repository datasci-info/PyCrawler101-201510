'''
Created on Oct 17, 2015

@author: c3h3
'''

import requests
from pyquery import PyQuery
import urllib
import pandas as pd

def getData(url):
    urls = listNewsUrls(url)
    return pd.DataFrame(map(getNewsData,urls))


def getNewsData(url):
    
    res = requests.get(url)
    S = PyQuery(res.text)
    data = {"datePublished": S('div[itemtype="https://schema.org/Article"] > meta[itemprop="datePublished"]').attr("content"),
        "provider": S('div[itemtype="https://schema.org/Article"] > meta[itemprop="provider"]').attr("content"),
        "headline": S('div[itemtype="https://schema.org/Article"] > meta[itemprop="headline"]').attr("content"),
        "description": S('div[itemtype="https://schema.org/Article"] > meta[itemprop="description"]').attr("content"),
        "articleBody": S('div[itemtype="https://schema.org/Article"] > div[itemprop="articleBody"]').outerHtml(),}
    return data


def listNewsUrls(url):
    res = requests.get(url)
    S = PyQuery(res.text)
    return ["https://tw.news.yahoo.com" + url for url in S("a.title").map(lambda i,e:PyQuery(e).attr("href")) if url != "#"]
