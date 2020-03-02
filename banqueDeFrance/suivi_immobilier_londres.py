from multiprocessing.pool import Pool
from bs4 import BeautifulSoup

import grequests
import pandas as pd
import requests
import asyncio
import re
import time
import sys


# URL de base
BASE = "https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&page_size=100&q=london&search_source=refine&radius=0&pn="

# Numéros de pages à parser
PAGE_INIT = 0
PAGE_LAST = 100

# Affichage de la progression
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

# Definition du corps d'une annonce
class PageBundle:
    prix = []
    adresses = []
    les_urls = []
    nombre_de_chambre = []
    nombre_de_SDB = []
    nombre_de_sejour = []
    surfaces = []
    description = []
    Neuf_ou_ancien = []
    Auction = []
    Aide = []

# Autres variables globales
start_time = time.time()
counter = 0
p = PageBundle()

# Parsing du contenu d'une page
def parse_page(page):
    global counter, p

    # Update de la barre de progression
    counter += 1
    print_progress(counter-1, 100)

    # Parsing de la page
    soup = BeautifulSoup(page.content, 'html.parser')

    annonces = soup.find_all(class_="listing-results-wrapper")
    p.prix += [re.sub("[^0-9]","",annonce.find( class_ = "listing-results-price text-price").get_text())
                   if re.sub("[^0-9]","",annonce.find( class_ = "listing-results-price text-price").get_text()) != ''
             else "NA" for annonce in annonces]
    p.adresses += [annonce.find(class_="listing-results-address").get_text() for annonce in annonces]
    p.les_urls += ["https://www.zoopla.co.uk/" + annonce.find(class_="status-wrapper").find("a")['href'] for annonce in
                annonces]
    p.nombre_de_chambre += [annonce.find('span', {"class": "num-icon num-beds"}).get_text() if annonce.find('span', {
        "class": "num-icon num-beds"}) is not None else "NA" for annonce in annonces]
    p.nombre_de_SDB +=  [annonce.find('span', {"class": "num-icon num-baths"}).get_text() if annonce.find('span', {
        "class": "num-icon num-baths"}) is not None else "NA" for annonce in annonces]
    p.nombre_de_sejour += [annonce.find('span', {"class": "num-icon num-reception"}).get_text() if annonce.find('span', {
        "class": "num-icon num-reception"}) is not None else "NA" for annonce in annonces]
    p.surfaces += [str(int(re.sub("[^0-9]","",annonce.find('span', {"class": "num-icon num-sqft"}).get_text()))*0.092903) if
                           (annonce.find('span', {"class": "num-icon num-sqft"}) is not None) and
                           ("ft" in annonce.find('span', {"class": "num-icon num-sqft"}).get_text()) else
                           str((re.sub("[^0-9]","",annonce.find('span', {"class": "num-icon num-sqft"}).get_text())) if
                            annonce.find('span', {"class": "num-icon num-sqft"}) is not None else "NA") for annonce in annonces]
    p.description += [annonce.find('h2', class_="listing-results-attr").get_text().splitlines()[1] for annonce in annonces]
    p.Neuf_ou_ancien += ["N" if annonce.find(class_="status-text status-text-new-home") is not None else "A" for annonce in
                      annonces]
    p.Auction += ["Enchères" if "auction" in str(annonce.find('p')).lower() else "vente" for annonce in annonces]
    p.Aide += ["Help to buy" if "help to buy" in str(annonce.find('p')).lower() else "NA" for annonce in annonces]


# Charger toutes les pages d'une manière asynchrone
def load_pages():
    global BASE, PAGE_INIT, PAGE_LAST

    reqs = (grequests.get(BASE+str(i)) for i in range(PAGE_INIT, PAGE_LAST+1))
    pages = grequests.map(reqs)
    parse_parallel(pages)

# Parser les pages en parallèle
def parse_parallel(pages):
    for page in pages:
        # Ajout des tâches à la queue
        parse_page(page)

# Conversion vers un fichier CSV
def to_csv(p, filename):
    Type_bien = ["Appartement" if "flat" in dec.lower() else ("Maison" if "house" in dec.lower() else (
        "Terrain" if "land" in dec.lower() else ("Maisonette" if "maisonette" in dec.lower() else (
            "Studio" if "studio" in dec.lower() else ("Maison avec jardin" if "property" in dec.lower() else
            ("Bungalow" if "bungalow" in dec.lower() else ("Cottage" if "cottage" in dec.lower() else
            ("Duplex" if "duplex" in dec.lower() else ("Triplex" if "triplex" in dec.lower() else
            ("Garage/parking" if "garage" in dec.lower() else
            ("Mobilehome" if "mobile/park home" in dec.lower() else "NA")))))))))))
                for dec in p.description]

    codepostal_londres = ["E" + str(i) for i in range(30)] + ["EC" + str(i) for i in range(30)] + ["N" + str(i) for i in
                                                                                                   range(30)] + \
                         ["NW" + str(i) for i in range(30)] + ["SE" + str(i) for i in range(30)] + ["SW" + str(i) for i
                                                                                                    in range(30)] + \
                         ["W" + str(i) for i in range(30)] + ["WC" + str(i) for i in range(30)]

    codepostal_1 = [element[element.rfind(" ") + 1:] for element in p.adresses]

    county = ['bedfordshire', 'bedford', 'berkshire', 'berk', 'buckinghamshire', 'buckingham', 'cambridgeshire',
              'cambridge',
              'cheshire', 'chester', 'cornwall', 'cumberland', 'derbyshire', 'derby', 'devon', 'dorset', 'durham',
              'essex',
              'gloucestershire', 'gloucester', 'hampshire', 'southamptonshire', 'herefordshire', 'hereford',
              'hertfordshire', 'hertford',
              'huntingdonshire', 'huntingdon', 'kent', 'lancashire', 'lancaster', 'leicestershire', 'leicester',
              'lincolnshire',
              'lincoln', 'middlesex', 'norfolk', 'northamptonshire', 'northampton', 'northumberland', 'nottinghamshire',
              'nottingham', 'oxfordshire', 'oxford', 'rutland', 'shropshire', 'salop', 'somerset', 'somersetshire',
              'staffordshire',
              'stafford', 'suffolk', 'surrey', 'sussex', 'warwickshire', 'warwick', 'westmorland', 'wiltshire', 'wilt',
              'worcestershire',
              'worcester', 'yorkshire', 'york']

    Ville_1 = ["Londres" if element[element.rfind(" ") + 1:] in codepostal_londres else
               (element[element.find(",") + 2:element.rfind(",")] if element[element.rfind(",") + 2:element.rfind(
                   " ")].lower() in county
                else (element[element.rfind(",") + 2:element.rfind(" ")] if element[
                                                                            element.rfind(",") + 2:element.rfind(
                                                                                " ")] else "NA"))
               for element in p.adresses]

    Ville = [
        element[element.find(",") + 1:] if "," in element else ("NA" if element == '' else ("NA" if element == "." else
                                                        ("NA" if element == ' .' else element)))for element in Ville_1]

    adresses = [element.replace(",","") for element in p.adresses]

    codepostal = [element.replace(",","") for element in codepostal_1]

    Ville_final = [element.replace(",","") for element in Ville]

    immobiler_5 = pd.DataFrame({
        "URL" : p.les_urls,
        "ville" : Ville_final,
        "code postal" : codepostal,
        "Adresses": adresses,
        "prix livre" : p.prix,
        "surface m2": p.surfaces,
        "Enchere ou vente" : p.Auction,
        "Etat neuf ou ancien": p.Neuf_ou_ancien,
        "Nombre de chambres": p.nombre_de_chambre,
        "Nombre de SDB": p.nombre_de_SDB,
        "Nombre de séjour": p.nombre_de_sejour,
        "Description" : p.description,
        "Type bien" : Type_bien,
        "Aide" : p.Aide,
    })

    immobiler_5.to_csv(filename)


load_pages()

# Writing the page into a CSV file
to_csv(p, "sortie.csv")
print("duree=", time.time() - start_time)