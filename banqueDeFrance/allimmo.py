import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import sys


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

#url du site
url = "https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&page_size=100&q=london&search_source=refine&radius=0"

#on définit notre agent afin de ne pas être pris pour un robot par le site
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

#on effectue une requête afin d'obtenir la page
page = requests.get(url, headers = agent)

#on affiche la page selon son code HTML ce qui permet de travailler en parallèle avec l'outil inspecter de Chrome
# où on voit également le code html

soup = BeautifulSoup(page.content, 'html.parser')

#on récupère dans la page ce qui nous interesse cad les annonces
annonces = soup.find_all( class_ = "listing-results-wrapper")

#on récupère le texte associé au prix et on en prend seulement les données chiffrés
prix = [re.sub("[^0-9]","",annonce.find( class_ = "listing-results-price text-price").get_text())
        if re.sub("[^0-9]","",annonce.find( class_ = "listing-results-price text-price").get_text()) != ''
        else "NA" for annonce in annonces]

#de même avec les adresses
adresses = [annonce.find( class_ = "listing-results-address").get_text() for annonce in annonces]

#on récupère les urls précis des annonces
les_urls = ["https://www.zoopla.co.uk/" + annonce.find( class_ = "status-wrapper").find("a")['href'] for annonce in annonces]

#le nombre de chambre
nombre_de_chambre = [annonce.find('span', {"class": "num-icon num-beds"}).get_text() if
                     annonce.find('span', {"class": "num-icon num-beds"}) is not None else "NA" for annonce in annonces]

#le nombre de SDB
nombre_de_SDB = [annonce.find('span', {"class": "num-icon num-baths"}).get_text() if
                 annonce.find('span', {"class": "num-icon num-baths"}) is not None else "NA" for annonce in annonces]

#le nombre de pièces de vie
nombre_de_sejour = [annonce.find('span', {"class": "num-icon num-reception"}).get_text() if
                    annonce.find('span', {"class": "num-icon num-reception"}) is not None else "NA" for annonce in annonces]


#on récupère la surface qui est convertie en m2
surfaces = [str(int(re.sub("[^0-9]","",annonce.find('span', {"class": "num-icon num-sqft"}).get_text()))*0.092903)
            if (annonce.find('span', {"class": "num-icon num-sqft"}) is not None) and
               ("ft" in annonce.find('span', {"class": "num-icon num-sqft"}).get_text()) else
            (re.sub("[^0-9]","",annonce.find('span', {"class": "num-icon num-sqft"}).get_text()) if
             annonce.find('span', {"class": "num-icon num-sqft"}) is not None else "NA") for annonce in annonces]

#On récupère la description du bien
description = [annonce.find('h2', class_ = "listing-results-attr").get_text().splitlines()[1] for annonce in annonces]

#le caratère neuf ou ancien
Neuf_ou_ancien = ["N" if annonce.find( class_ = "status-text status-text-new-home") is not None else "A" for annonce in annonces]

#On vérifie si l'aide help to buy est disponible
Aide = ["Help to buy" if "help to buy" in str(annonce.find('p')).lower() else "NA" for annonce in annonces]

#On regarde s'il s'agit d'enchères
Auction = [ "Enchères" if "auction" in str(annonce.find('p')).lower() else "vente" for annonce in annonces]

#ensuite on réitère ce processus sur un grand nombre de pages
page_to_inspect = []
base = "https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&page_size=100&q=london&search_source=refine&radius=0&pn="
for i in range(2,101):
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

#Ville = [element[element.rfind(",")+1:element.rfind(" ")] for element in adresses]

codepostal = [element[element.rfind(" ")+1:] for element in adresses]

maxcode = [int(s) for code in codepostal for s in re.findall(r'\d+',code) ]

print(sorted([]))
codepostal_londres = ["E","EC","N","NW","SE","SW","W","WC"]

ville = ["Londres" if code in element else "NA" for element in codepostal for code in codepostal_londres]
immobiler_5 = pd.DataFrame({
    "URL" : les_urls,
    "code postal" : codepostal,
    "adresse": adresses,
    "prix £" : prix,
    "surface m2": surfaces,
    "Enchère ou vente" : Auction,
    "Etat neuf ou ancien": Neuf_ou_ancien,
    "Nombre de chambres": nombre_de_chambre,
    "Nombre de SDB": nombre_de_SDB,
    "Nombre de séjour": nombre_de_sejour,
    "Description" : description,
    "Type bien" : Type_bien,
    "Aide" :Aide,
})

immobiler_5.to_csv("patate.csv")

print("duree=",time.time() - start_time)