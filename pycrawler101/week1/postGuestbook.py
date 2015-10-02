'''
Created on Oct 3, 2015

@author: c3h3
'''

import requests
import pandas as pd

from datetime import datetime
sampleMsg = "TEST MESSAGE " + str(datetime.now())


def postMessage(message=sampleMsg):
    postData = {"content":message}
    res = requests.post("http://apt-bonbon-93413.appspot.com/sign",data=postData)
    res.raise_for_status()
    