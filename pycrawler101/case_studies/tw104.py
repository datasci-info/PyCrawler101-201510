'''
Created on Oct 15, 2015

@author: c3h3
'''

import requests
from pyquery import PyQuery
from datetime import datetime
import pandas as pd


def getData(search_kw):
    page = 1
    url = "http://www.104.com.tw/jobbank/joblist/auto_joblist.cfm?auto=1&jobsource=n104bank1&ro=0&keyword={skw}&order=1&asc=0&page={page}&psl=N_B".format(skw=search_kw.replace(" ","+"),page=page)
    res = requests.get(url)
    S = PyQuery(res.text)
    max_pages = int(PyQuery(S("#box_page_bottom_2 li > a")[-1]).text())
    data = []
    data.extend(S(".j_cont").map(lambda i,e: {"name":PyQuery(e)(".job_name").text(),
                                           "url":PyQuery(e)("a").attr("href"),
                                           "meta":dict(PyQuery(e)("meta").map(lambda ii,ee:(PyQuery(ee).attr("itemprop"),PyQuery(ee).attr("content")))),
                                           "area":PyQuery(e)(".area_summary").text(),
                                           "company_name":PyQuery(e)(".compname_summary").text(),
                                           "company_meta":PyQuery(e)(".compname_summary span").attr("title"),
                                           "candidates_summary":PyQuery(e)(".candidates_summary").text(),
                                           "requirement":PyQuery(e)(".requirement").text(),
                                           "joblist_summary":PyQuery(e)(".joblist_summary").text(),
                                           "searched_keyword":search_kw,
                                           "crawledAt":datetime.utcnow()}))
    
    for page in range(2,max_pages+1):
        url = "http://www.104.com.tw/jobbank/joblist/auto_joblist.cfm?auto=1&jobsource=n104bank1&ro=0&keyword={skw}&order=1&asc=0&page={page}&psl=N_B".format(skw=search_kw.replace(" ","+"),page=page)
        res = requests.get(url)
        S = PyQuery(res.text)
        data.extend(S(".j_cont").map(lambda i,e: {"name":PyQuery(e)(".job_name").text(),
                                           "url":PyQuery(e)("a").attr("href"),
                                           "meta":dict(PyQuery(e)("meta").map(lambda ii,ee:(PyQuery(ee).attr("itemprop"),PyQuery(ee).attr("content")))),
                                           "area":PyQuery(e)(".area_summary").text(),
                                           "company_name":PyQuery(e)(".compname_summary").text(),
                                           "company_meta":PyQuery(e)(".compname_summary span").attr("title"),
                                           "candidates_summary":PyQuery(e)(".candidates_summary").text(),
                                           "requirement":PyQuery(e)(".requirement").text(),
                                           "joblist_summary":PyQuery(e)(".joblist_summary").text(),
                                           "searched_keyword":search_kw,
                                           "crawledAt":datetime.utcnow()}))
    
        
    df = pd.DataFrame(data)
    return df