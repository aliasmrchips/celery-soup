from __future__ import print_function

from celery import Celery
from celery import chord
from bs4 import BeautifulSoup
from collections import Counter
import requests

app = Celery('soup')

app.config_from_object('config')

@app.task
def map(url):
    
    c = Counter()

    r = requests.get(url)
    
    soup = BeautifulSoup(r.text)
    
    for word in soup.get_text().split():
        if word not in c:
            c[word] = 1
        else:
            c[word] += 1

    return c

@app.task
def reduce(counters):
    res = counters[0]
    for c in counters[1:]:
        res += c
    return res
    
if __name__ == "__main__":

    r = requests.get('http://en.wikipedia.org/wiki/Wikipedia:Top_25_Report')

    d = BeautifulSoup(r.text)
    
    for table in d.find_all('table', class_='wikitable'):
        
        callback = reduce.s()

        header = [ map.s('http://en.wikipedia.org'+link.get('href')) for link in table.find_all('a') ]
        
        res = chord(header)(callback)
        
        m = res.get()
        
        for k in sorted(m, key=m.get, reverse=True)[:25]:
            print(k, m[k])
