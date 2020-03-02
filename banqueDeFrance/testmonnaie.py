import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time

start_time = time.time()

url = "https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&page_size=100&q=london&search_source=refine&radius=0"
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
page = requests.get(url, headers = agent)
soup = BeautifulSoup(page.content, 'html.parser')
annonces = soup.find_all( class_ = "listing-results-wrapper")


page_to_inspect = []
base = "https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&page_size=100&q=london&search_source=refine&radius=0&pn="


les_urls = ["https://www.zoopla.co.uk/" + annonce.find( class_ = "status-wrapper").find("a")['href'] for annonce in annonces]

description = [annonce.find('h2', class_ = "listing-results-attr").get_text().splitlines()[1] for annonce in annonces]

prix_1 = [annonce.find( class_ = "listing-results-price text-price").get_text() for annonce in annonces]

print(prix_1)
prix_final = [element[element.index("£"):(element[element.index("£"):].index("\n")+element.index("£"))] if "£" in element else "NA" for element in prix_1]

for i in range(2,101):
    page_to_inspect.append(base + str(i))

counter = 2

for url in page_to_inspect:
    print(counter)
    agent = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    page = requests.get(url, headers=agent)
    soup = BeautifulSoup(page.content, 'html.parser')
    annonces = soup.find_all(class_="listing-results-wrapper")
    les_urls = les_urls + ["https://www.zoopla.co.uk/" + annonce.find(class_="status-wrapper").find("a")['href'] for
                           annonce in
                           annonces]
    prix_1 +=  [annonce.find( class_ = "listing-results-price text-price").get_text() for annonce in annonces]
    counter += 1

test = [les_urls[index] for index,element in enumerate(prix_1) if (element.find("£") + element.find("POA") < -1)]
print(test)

