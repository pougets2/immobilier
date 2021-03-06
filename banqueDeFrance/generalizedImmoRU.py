import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time

start_time = time.time()
url = "https://www.zoopla.co.uk/for-sale/flats/london/?identifier=london&property_type=flats&page_size=25&q=london&search_source=refine&radius=0"
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
page = requests.get(url, headers = agent)
soup = BeautifulSoup(page.content, 'html.parser')
annonces = soup.find_all( class_ = "listing-results-wrapper")
prix_1 = [annonce.find( class_ = "listing-results-price text-price").get_text() for annonce in annonces]
adresses_1 = [annonce.find( class_ = "listing-results-address").get_text() for annonce in annonces]
les_urls_1 = [annonce.find( class_ = "status-wrapper") for annonce in annonces]
les_urls = []
for element in les_urls_1:
    element = str(element)
    les_urls.append("https://www.zoopla.co.uk/" + element[re.search("<a href=",element).end()+1:re.search(">",element[re.search("<a href=",element).end():]).start() + re.search("<a href=",element).end()-1])

Neuf_ou_ancien_1 = [annonce.find( class_ = "status-text status-text-new-home") for annonce in annonces]

Neuf_ou_ancien = ['A' if element is None else 'N' for element in Neuf_ou_ancien_1]


caracteristiques = [annonce.find( class_ = "listing-results-attr") for annonce in annonces]


surface_1 = [(carac.find_all('span', { "class" : "num-icon num-sqft"}),index) for index,carac in enumerate(caracteristiques) if carac.find_all('span', { "class" : "num-icon num-sqft"}) != []]

#print(surface_1)
surface_finale = [liste[0][0].get_text() for liste in surface_1]

#print(surface_finale)
annonces_associees = [caracteristiques[liste[1]] for liste in surface_1]

surfaces = 25*["NA"]
for element in surface_1:
    surfaces[element[1]] = element[0][0].get_text()
#print(surfaces)
items = soup.find_all( class_ = "listing-results-wrapper")


prix_final = ["NA" if "POA" in element else element[element.index("£"):(element[element.index("£"):].index("\n")+element.index("£"))] for element in prix_1]


#url_associes = [les_urls[liste[1]] for liste in surface_1]


#prix_associes = [prix_final[liste[1]] for liste in surface_1]


#adresses_associees = [adresses_1[liste[1]] for liste in surface_1]
#bedroom_number = [annonce.find_all('span', { "class" : "num-icon num-beds"})[0].get_text() for annonce in annonces_associees]
#bath_number = [annonce.find_all('span', { "class" : "num-icon num-baths"})[0].get_text() for annonce in annonces_associees]
#Neuf_ou_ancien_associe = [Neuf_ou_ancien[liste[1]] for liste in surface_1]



nombre_de_chambre_1 = [annonce.find('span', { "class" : "num-icon num-beds"}) for annonce in annonces]
nombre_de_SBD_1 = [annonce.find('span', { "class" : "num-icon num-baths"}) for annonce in annonces]
nombre_de_sejour_1 = [annonce.find('span', { "class" : "num-icon num-reception"}) for annonce in annonces]
description = [annonce.find('h2', class_ = "listing-results-attr").get_text().splitlines()[1] for annonce in annonces]

nombre_de_chambre = []

for element in nombre_de_chambre_1:
    element = str(element)
    try :
        titre = re.search("title=",element).end()
        nombre_de_chambre.append(element[titre+1:re.search(" ", element[titre+1:]).start() + titre + 1])
    except :
        nombre_de_chambre.append("NA")

nombre_de_SDB = []
for element in nombre_de_SBD_1:
    element = str(element)
    try :
        titre = re.search("title=",element).end()
        nombre_de_SDB.append(element[titre+1:re.search(" ", element[titre+1:]).start() + titre + 1])
    except :
        nombre_de_SDB.append("NA")

nombre_de_sejour = []
for element in nombre_de_sejour_1:
    element = str(element)
    try :
        titre = re.search("title=",element).end()
        nombre_de_sejour.append(element[titre+1:re.search(" ", element[titre+1:]).start() + titre + 1])
    except :
        nombre_de_sejour.append("NA")

pages_to_inspect = []
base = "https://www.zoopla.co.uk/for-sale/flats/london/?identifier=london&property_type=flats&page_size=25&q=london&search_source=refine&radius=0&pn="
for i in range(2,400):
    pages_to_inspect.append(base + str(i))

counter = 1
for url in pages_to_inspect:
    print(counter)
    agent = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    page = requests.get(url, headers=agent)
    soup = BeautifulSoup(page.content, 'html.parser')
    annonces = soup.find_all(class_="listing-results-wrapper")
    prix_1 = [annonce.find(class_="listing-results-price text-price").get_text() for annonce in annonces]
    adresses_1 = adresses_1 + [annonce.find(class_="listing-results-address").get_text() for annonce in annonces]
    les_urls_1 = [annonce.find(class_="status-wrapper") for annonce in annonces]
    for element in les_urls_1:
        element = str(element)
        les_urls.append("https://www.zoopla.co.uk/" + element[re.search("<a href=", element).end() + 1:re.search(">",
                                                                                                                 element[
                                                                                                                 re.search(
                                                                                                                     "<a href=",
                                                                                                                     element).end():]).start() + re.search(
            "<a href=", element).end() - 1])

    Neuf_ou_ancien_1 = [annonce.find(class_="status-text status-text-new-home") for annonce in annonces]

    Neuf_ou_ancien = Neuf_ou_ancien + ['A' if element is None else 'N' for element in Neuf_ou_ancien_1]

    caracteristiques = [annonce.find(class_="listing-results-attr") for annonce in annonces]

    surface_1 = [(carac.find_all('span', {"class": "num-icon num-sqft"}), index) for index, carac in
                 enumerate(caracteristiques) if carac.find_all('span', {"class": "num-icon num-sqft"}) != []]

    #print(surface_1)
    surface_finale = [liste[0][0].get_text() for liste in surface_1]

    #print(surface_finale)

    surfaces = surfaces + 25 * ["NA"]
    for element in surface_1:
        surfaces[25*counter + element[1]] = element[0][0].get_text()
    #print(surfaces)
    items = soup.find_all(class_="listing-results-wrapper")

    prix_final = prix_final + ["NA" if "POA" in element else element[element.index("£"):(
                element[element.index("£"):].index("\n") + element.index("£"))] for element in prix_1]


    nombre_de_chambre_1 = [annonce.find('span', {"class": "num-icon num-beds"}) for annonce in annonces]
    nombre_de_SBD_1 = [annonce.find('span', {"class": "num-icon num-baths"}) for annonce in annonces]
    nombre_de_sejour_1 = [annonce.find('span', {"class": "num-icon num-reception"}) for annonce in annonces]
    description = description + [annonce.find('h2', class_="listing-results-attr").get_text().splitlines()[1] for annonce in annonces]

    for element in nombre_de_chambre_1:
        element = str(element)
        try:
            titre = re.search("title=", element).end()
            nombre_de_chambre.append(element[titre + 1:re.search(" ", element[titre + 1:]).start() + titre + 1])
        except:
            nombre_de_chambre.append("NA")

    for element in nombre_de_SBD_1:
        element = str(element)
        try:
            titre = re.search("title=", element).end()
            nombre_de_SDB.append(element[titre + 1:re.search(" ", element[titre + 1:]).start() + titre + 1])
        except:
            nombre_de_SDB.append("NA")

    for element in nombre_de_sejour_1:
        element = str(element)
        try:
            titre = re.search("title=", element).end()
            nombre_de_sejour.append(element[titre + 1:re.search(" ", element[titre + 1:]).start() + titre + 1])
        except:
            nombre_de_sejour.append("NA")

    counter += 1

print(len(nombre_de_SDB))
print(len(les_urls))
immobiler_3 = pd.DataFrame(
    {'url':les_urls,
    'prix':prix_final,
    'adresse' : adresses_1,
     'surface' : surfaces,
     'Etat neuf ou ancien' : Neuf_ou_ancien,
     'Nombre de chambres' : nombre_de_chambre,
     'Nombre de SDB' : nombre_de_SDB,
     'Nombre de séjour' : nombre_de_sejour,
     'Description' : description,
     })

immobiler_3.to_csv("immo_bis.csv")

print("duree=",time.time() - start_time)
print(sorted(surfaces))