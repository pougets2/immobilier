import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import sys
from matplotlib.pyplot import plot, show, xlim, ylim

def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

start_time = time.time()

url = "https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&page_size=100&q=london&search_source=refine&radius=0"
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
page = requests.get(url, headers = agent)
soup = BeautifulSoup(page.content, 'html.parser')
annonces = soup.find_all( class_ = "listing-results-wrapper")

prix = [re.sub("[^0-9]","",annonce.find( class_ = "listing-results-price text-price").get_text())
        if re.sub("[^0-9]","",annonce.find( class_ = "listing-results-price text-price").get_text()) != ''
        else "NA" for annonce in annonces]

adresses = [annonce.find( class_ = "listing-results-address").get_text() for annonce in annonces]

les_urls = ["https://www.zoopla.co.uk/" + annonce.find( class_ = "status-wrapper").find("a")['href'] for annonce in annonces]

nombre_de_chambre = [annonce.find('span', {"class": "num-icon num-beds"}).get_text() if
                     annonce.find('span', {"class": "num-icon num-beds"}) is not None else "NA" for annonce in annonces]

nombre_de_SDB = [annonce.find('span', {"class": "num-icon num-baths"}).get_text() if
                 annonce.find('span', {"class": "num-icon num-baths"}) is not None else "NA" for annonce in annonces]

nombre_de_sejour = [annonce.find('span', {"class": "num-icon num-reception"}).get_text() if
                    annonce.find('span', {"class": "num-icon num-reception"}) is not None else "NA" for annonce in annonces]

surfaces = [str(int(re.sub("[^0-9]","",annonce.find('span', {"class": "num-icon num-sqft"}).get_text()))*0.092903)
            if (annonce.find('span', {"class": "num-icon num-sqft"}) is not None) and
               ("ft" in annonce.find('span', {"class": "num-icon num-sqft"}).get_text()) else
            (re.sub("[^0-9]","",annonce.find('span', {"class": "num-icon num-sqft"}).get_text()) if
             annonce.find('span', {"class": "num-icon num-sqft"}) is not None else "NA") for annonce in annonces]

description = [annonce.find('h2', class_ = "listing-results-attr").get_text().splitlines()[1] for annonce in annonces]

Neuf_ou_ancien = ["N" if annonce.find( class_ = "status-text status-text-new-home") is not None else "A" for annonce in annonces]

Aide = ["Help to buy" if "help to buy" in str(annonce.find('p')).lower() else "NA" for annonce in annonces]

Auction = [ "Enchères" if "auction" in str(annonce.find('p')).lower() else "vente" for annonce in annonces]


base = "https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&page_size=100&q=london&search_source=refine&radius=0&pn="

stock_temps = [0]
for z in range(10,101,10):
    page_to_inspect = []
    for i in range(2,z):
        page_to_inspect.append(base + str(i))


    counter = 2
    for url in page_to_inspect:
        print_progress(counter-1,100)
        agent = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        page = requests.get(url, headers=agent)
        soup = BeautifulSoup(page.content, 'html.parser')
        annonces = soup.find_all(class_="listing-results-wrapper")

        prix += [re.sub("[^0-9]","",annonce.find( class_ = "listing-results-price text-price").get_text())
                       if re.sub("[^0-9]","",annonce.find( class_ = "listing-results-price text-price").get_text()) != ''
                 else "NA" for annonce in annonces]

        adresses += [annonce.find(class_="listing-results-address").get_text() for annonce in annonces]

        les_urls += ["https://www.zoopla.co.uk/" + annonce.find(class_="status-wrapper").find("a")['href'] for annonce in
                    annonces]

        nombre_de_chambre += [annonce.find('span', {"class": "num-icon num-beds"}).get_text() if annonce.find('span', {
            "class": "num-icon num-beds"}) is not None else "NA" for annonce in annonces]

        nombre_de_SDB +=  [annonce.find('span', {"class": "num-icon num-baths"}).get_text() if annonce.find('span', {
            "class": "num-icon num-baths"}) is not None else "NA" for annonce in annonces]

        nombre_de_sejour += [annonce.find('span', {"class": "num-icon num-reception"}).get_text() if annonce.find('span', {
            "class": "num-icon num-reception"}) is not None else "NA" for annonce in annonces]

        surfaces += [str(int(re.sub("[^0-9]","",annonce.find('span', {"class": "num-icon num-sqft"}).get_text()))*0.092903) if
                               (annonce.find('span', {"class": "num-icon num-sqft"}) is not None) and
                               ("ft" in annonce.find('span', {"class": "num-icon num-sqft"}).get_text()) else
                               str((re.sub("[^0-9]","",annonce.find('span', {"class": "num-icon num-sqft"}).get_text())) if
                                annonce.find('span', {"class": "num-icon num-sqft"}) is not None else "NA") for annonce in annonces]

        description += [annonce.find('h2', class_="listing-results-attr").get_text().splitlines()[1] for annonce in annonces]

        Neuf_ou_ancien += ["N" if annonce.find(class_="status-text status-text-new-home") is not None else "A" for annonce in
                          annonces]

        Auction += [ "Enchères" if "auction" in str(annonce.find('p')).lower() else "vente" for annonce in annonces]
        counter += 1

        Aide += ["Help to buy" if "help to buy" in str(annonce.find('p')).lower() else "NA" for annonce in annonces]


    Type_bien = ["Appartement" if "flat" in dec.lower() else ("Maison" if "house" in dec.lower() else (
        "Terrain" if "land" in dec.lower() else ("Maisonette" if "maisonette" in dec.lower() else (
            "Studio" if "studio" in dec.lower() else ("Maison avec jardin" if "property" in dec.lower() else
            ("Bungalow" if "bungalow" in dec.lower() else ("Cottage" if "cottage" in dec.lower() else
            ("Duplex" if "duplex" in dec.lower() else ("Triplex" if "triplex" in dec.lower() else
            ("Garage/parking" if "garage" in dec.lower() else
             ("Mobilehome" if "mobile/park home" in dec.lower() else "NA")))))))))))
                 for dec in description]
    stock_temps.append((time.time() - start_time)/60)
    print("duree=", time.time() - start_time)

temps = [0] + [stock_temps[i+1]-stock_temps[i] for i in range(len(stock_temps)-1)]

z = [k*1000 for k in range(0,11)]

plot(z,temps,"r")
show()