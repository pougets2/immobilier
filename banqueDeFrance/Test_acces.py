import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import sys
from lxml.html import fromstring
from itertools import cycle
from torrequest import TorRequest
import stem.process

from stem.util import term

def get_proxies():
    url = 'https://free-proxy-list.net/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup)
    a = soup.find(class_ = "table-responsive")
    table = a.find("tbody")
    bis = table.find_all("tr")
    blabla_bis = [re.findall('([\d.]+)', str(element)) for element in bis]
    res = {element[0]+ ":" + element[1] for element in blabla_bis}
    return (res)

proxies = get_proxies()
print(proxies)
proxy_pool = cycle(proxies)

url = "https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&page_size=100&q=london&search_source=refine&radius=0"

# tr = TorRequest()
# response = requests.get('http://ipecho.net/plain')
# print("My Original IP Address:", response.text)
#
# tr.reset_identity()  # Reset Tor
# response = tr.get('http://ipecho.net/plain')
# print("New Ip Address", response.text)
# bis = tr.get(url)
# soup = BeautifulSoup(bis.content, 'html.parser')
# annonces = soup.find_all(class_="listing-results-wrapper")
# print(annonces)


for i in range(1,11):
     #Get a proxy from the pool
     proxy = next(proxy_pool)
     print("Request #%d"%i)
     url = 'https://httpbin.org/ip'
     try:
         print("before")
         time.sleep(5)
         print("after")
         response = requests.get(url,proxies={"http": proxy, "https": proxy}, timeout=5)
         print(response.json())
         response1 = requests.get("https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&page_size=100&q=london&search_source=refine&radius=0",
                                  proxies={"http": proxy, "https": proxy}, timeout=5)
         print(response1.json())

     except:
         #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
         #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
         print("Skipping. Connnection error")

# url = 'https://httpbin.org/ip'