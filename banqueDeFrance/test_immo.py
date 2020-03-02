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

prix = [re.sub("[^0-9]","",annonce.find( class_ = "listing-results-price text-price").get_text())
        if re.sub("[^0-9]","",annonce.find( class_ = "listing-results-price text-price").get_text()) != ''
        else "NA" for annonce in annonces]

Auction = ["Enchères" if "auction" in annonce.find("a", class_ = "listing-results-right clearfix").get_text().lower() else "Vente" for annonce in annonces]
les_differentes_pages = len(description)*["https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&page_size=100&q=london&search_source=refine&radius=0"]

print(len(les_differentes_pages))
for i in range(2,5):
    page_to_inspect.append(base + str(i))

counter = 2

for url in page_to_inspect:
    print(counter)
    agent = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    page = requests.get(url, headers=agent)
    soup = BeautifulSoup(page.content, 'html.parser')
    annonces = soup.find_all(class_="listing-results-wrapper")

    les_urls = les_urls + ["https://www.zoopla.co.uk/" + annonce.find(class_="status-wrapper").find("a")['href'] for annonce in
                annonces]

    prix = prix + [re.sub("[^0-9]", "", annonce.find(class_="listing-results-price text-price").get_text())
                   if re.sub("[^0-9]", "",
                             annonce.find(class_="listing-results-price text-price").get_text()) != '' else "NA" for
                   annonce in annonces]

    description = description + [annonce.find('h2', class_="listing-results-attr").get_text().splitlines()[1] for
                                 annonce in annonces]
    les_differentes_pages = les_differentes_pages + 100*[url]

    Auction += ["Enchères" if "auction" in annonce.find("a", class_ = "listing-results-right clearfix").get_text().lower() else "Vente" for annonce in annonces]
    counter += 1



print("pages=",len(les_differentes_pages))
print("url=",len(les_urls))
print("description=",len(description))
print("prix=",len(prix))
print("Auction=",len(Auction))

immobiler_10 = pd.DataFrame(
   {"URL" : les_urls,
    "pages" :  les_differentes_pages,
     "description" : description,
     "prix" : prix,
    "Enchère ou vente" : Auction,
     })


immobiler_10.prix = immobiler_10.prix.apply(pd.to_numeric, errors='coerce')

immo_11 = immobiler_10.sort_values(by = 'prix')

immo_11.to_csv("orchidée.csv")

print("duree=",time.time() - start_time)
