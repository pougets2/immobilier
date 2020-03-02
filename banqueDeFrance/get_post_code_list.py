import csv
from multiprocessing.pool import Pool
from bs4 import BeautifulSoup

import grequests
import pandas as pd
import requests
import asyncio
import re
import time
import sys
import random

file=open("ukpostcodes.csv", "r")
reader = csv.reader(file)
postcode = set()
for line in reader:
    t=line[1]
    y = t.split(' ')
    postcode.add(y[0])

print(len(postcode))
urls = []
for element in postcode:
    urls.append("https://www.zoopla.co.uk/for-sale/property/"+ element +"/?identifier=" + element + "&q=" + element + "&search_source=refine&radius=0&page_size=100&pn=0")

for element in urls[:15]:
    print(element)
    url = "https://www.zoopla.co.uk/for-sale/property/"+ element +"/?identifier=" + element + "&q=" + element + "&search_source=refine&radius=0&page_size=100&pn=0"
    agent = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    page = requests.get(url, headers=agent)
    try :
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            PAGE_LAST = int(re.findall("\d+", soup.find(class_="paginate bg-muted").get_text())[-1])
        except:
            print("loupé1")
    except:
        print("loupé")