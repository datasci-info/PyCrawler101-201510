'''
Created on Oct 16, 2015

@author: c3h3
'''

import requests
from pyquery import PyQuery
import pandas as pd
import urllib
from datetime import datetime


def getData(n_past_data = 100):
    
    list_df = get_headline_list(n_past_data)
    news_df = pd.DataFrame(map(get_news_data,list_df["url"]))
    
    return {"list_df":list_df, "news_df":news_df} 


def get_headline_list(n_past_data = 100): 

    assert isinstance(n_past_data, int)
    s = requests.Session()
    res = s.get("http://www.marketwatch.com/newsviewer")
    S = PyQuery(res.text)
    data = S("li").map(lambda i,e: {"id": PyQuery(e).attr("id"),
                                    "timestamp": PyQuery(e).attr("timestamp"),
                                    "title": PyQuery(e)(".nv-text-cont").text(),
                                    "details": PyQuery(e)(".nv-details").outerHtml(),
                                    "url": PyQuery(e)(".nv-text-cont a").attr("href"),
                                   })
    
    if n_past_data > 0:
        postData = dict(map(lambda xx: (xx.split("=")[0],urllib.unquote(xx.split("=")[1])) ,
                            "topstories=true&rtheadlines=true&pulse=true&commentary=true&video=true&premium=true&blogs=true&topic=All+Topics&docId=1187576694&timestamp=10%2F15%2F2015+10%3A01%3A32+AM&pullCount=10".split("&")))
    
        postData["timestamp"] = data[-1]["timestamp"]
        postData["docId"] = data[-1]["id"]
        postData["topic"] = postData["topic"].replace("+"," ")
        postData["pullCount"] = n_past_data
        
        pastRes = s.post("http://www.marketwatch.com/newsviewer/mktwheadlines",data=postData)
        pastS = PyQuery(pastRes.text)
        pastData = pastS("li").map(lambda i,e: {"id": PyQuery(e).attr("id"),
                                                "timestamp": PyQuery(e).attr("timestamp"),
                                                "title": PyQuery(e)(".nv-text-cont").text(),
                                                "details": PyQuery(e)(".nv-details").outerHtml(),
                                                "url": PyQuery(e)(".nv-text-cont a").attr("href"),
                                               })
        
    data.extend(pastData)
    df = pd.DataFrame(data)
    df = df[df["timestamp"].notnull()]
    df["url"] = df["url"].map(lambda url: "http://www.marketwatch.com"+url if url else url)
    df["time"] = df["timestamp"].map(lambda tt: datetime.strptime(tt,"%m/%d/%Y %I:%M:%S %p") if tt else tt)
    
    df.sort("time",ascending=False)
    
    return df

def get_news_data(url):
    res = requests.get(url)
    S = PyQuery(res.text)
    
    article_data = {}
    
    article_data["url"] = url
    article_data["headline"] = S("#article-headline").text()
    article_data["published-timestamp"] = S("#published-timestamp").text()
    article_data["body"] = S("#article-body").outerHtml()
    article_data["related-articles"] = S("related-articles").outerHtml()
    
    return article_data
