from bs4 import BeautifulSoup
import grequests
import pandas as pd
import requests
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
base = "https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&page_size=100&q=london&search_source=refine&radius=0&pn="
counter = 2

# Parsing du contenu d'une page
def parse_page(page):
    global prix, adresses, les_urls, nombre_de_chambre, nombre_de_SDB, nombre_de_sejour
    global surfaces, description, Neuf_ou_ancien, Auction, Aide, counter

    # Update de la barre de progression
    counter += 1
    print_progress(counter-1, 100)

    # Parsing de la page
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
    Aide += ["Help to buy" if "help to buy" in str(annonce.find('p')).lower() else "NA" for annonce in annonces]


# Charger toutes les pages d'une manière asynchrone
def load_pages():
    global base
    reqs = (grequests.get(base+str(i)) for i in range(2,100))
    pages = grequests.map(reqs)
    parse_parallel(pages)

# Parser les pages en parallèle
def parse_parallel(pages):
    for page in pages:
        parse_page(page)
    #with Pool(5) as p:
        # Ajout des tâches à la queue
    #    p.map(parse_page, pages)


load_pages()

Type_bien = ["Appartement" if "flat" in dec.lower() else ("Maison" if "house" in dec.lower() else (
    "Terrain" if "land" in dec.lower() else ("Maisonette" if "maisonette" in dec.lower() else (
        "Studio" if "studio" in dec.lower() else ("Maison avec jardin" if "property" in dec.lower() else
        ("Bungalow" if "bungalow" in dec.lower() else ("Cottage" if "cottage" in dec.lower() else
        ("Duplex" if "duplex" in dec.lower() else ("Triplex" if "triplex" in dec.lower() else
        ("Garage/parking" if "garage" in dec.lower() else
         ("Mobilehome" if "mobile/park home" in dec.lower() else "NA")))))))))))
             for dec in description]



codepostal_londres = ["E"+ str(i) for i in range(30)]+["EC"+ str(i) for i in range(30)]+["N"+ str(i) for i in range(30)]+\
                     ["NW"+ str(i) for i in range(30)] + ["SE"+ str(i) for i in range(30)]+["SW"+ str(i) for i in range(30)]+\
                     ["W"  + str(i) for i in range(30)]+["WC"+ str(i) for i in range(30)]


codepostal = [element[element.rfind(" ")+1:] for element in adresses]

county = ['bedfordshire', 'bedford', 'berkshire', 'berk', 'buckinghamshire', 'buckingham', 'cambridgeshire', 'cambridge',
          'cheshire', 'chester', 'cornwall', 'cumberland', 'derbyshire', 'derby', 'devon', 'dorset', 'durham', 'essex',
          'gloucestershire', 'gloucester', 'hampshire', 'southamptonshire', 'herefordshire', 'hereford', 'hertfordshire', 'hertford',
          'huntingdonshire', 'huntingdon', 'kent', 'lancashire', 'lancaster', 'leicestershire', 'leicester', 'lincolnshire',
          'lincoln', 'middlesex', 'norfolk', 'northamptonshire', 'northampton', 'northumberland', 'nottinghamshire',
          'nottingham', 'oxfordshire', 'oxford', 'rutland', 'shropshire', 'salop', 'somerset','somersetshire','staffordshire',
          'stafford','suffolk', 'surrey', 'sussex', 'warwickshire', 'warwick', 'westmorland', 'wiltshire', 'wilt', 'worcestershire',
          'worcester', 'yorkshire', 'york']

Ville_1 = ["Londres" if element[element.rfind(" ")+1:] in codepostal_londres else
         (element[element.find(",")+2:element.rfind(",")]if element[element.rfind(",")+2:element.rfind(" ")].lower() in county
          else (element[element.rfind(",")+2:element.rfind(" ")] if element[element.rfind(",")+2:element.rfind(" ")] else "NA"))
           for element in adresses]


Ville = [element[element.find(",")+1:] if "," in element else ("NA" if element == '' else ("NA" if element == "." else
                                                    ("NA" if element == ' .' else element)))for element in Ville_1]

Test = [(index,element) for index,element in enumerate(Ville) if element.lower() in county]

a = {'', 'Westking Place', 'Erith', 'Greenford', ' Purley', ' West Drayton', 'Kingswood', ' Coulsdon',
     'Crayford', 'Orpington', 'Westminster', '.', 'Couldson', 'Hayes', 'Harold Wood', 'Fitzrovia', 'Ealing', 'Essex',
     'Clayhall', ' Northwood', 'Hornchurch', 'Morden', 'Bromley Kent', 'Welling', 'Chessington',
     'Essex.', ' South Croydon', 'Bromley', ' Bromley', 'Hanworth', 'Elm Park', 'Islington', 'South Harrow', 'West Purley',
     'Keston', 'Shirley', 'Barnehurst', 'Waltham Cross', 'Hackbridge', ' Woodford Green', 'New Barnet', 'Denham', 'Bickley',
     'Old Coulsdon', 'Ham Gate', 'Essesx', 'Burnt Oak', 'South Sutton', 'Charterhouse Square', ' Enfield',
     'Wembley Park', 'Beddington', 'Green Street Green', 'Waddon', 'West Drayton', 'Surbiton', 'Wallington',
     'Kingston Upon Thames', 'Kew', 'Grosvenor Waterside', ' Potters Bar', ' Sevenoaks', 'Gidea Park', 'South Welling',
     'Blackfen', 'Chiswick', 'St. Margarets', 'Hounslow', ' Uxbridge', 'Harrow-On-The-Hill', 'Richmond Hill', 'Seven Kings',
     'Cockfosters', 'United Kingdom', 'Harrow Weald', 'Motspur Park', ' Surbiton', 'NA', 'Northwood', 'West Ewell Epsom',
     'Enfield', 'Beckenham', 'Uxbridge', 'Bloomsbury', 'Bellamy Drive',
     'Chadwell Heath', 'Dartford', ' Brentford', 'Croydon', 'South Croydon', 'Wapping', 'Rush Green', ' Welling',
     'Eastcote', 'Caterham', 'South Mimms', 'Coombe Hill', 'Downham', 'Cuffley', 'Pinner Village', 'Eastcote Station',
     'Cottage Close', 'Addiscombe', 'East Barnet', 'Kenton', 'Stanmore', 'West Croydon', 'Hainault', ' Ilford', 'Barking Essex',
     'Goodmayes', ' Erith', 'Kew Bridge', 'Southall', 'Greater London', 'St Pauls Cray', 'Ruislip', 'Chelsfield', 'Yiewsley',
     ' Carshalton', ' Orpington', 'Belvedere', 'Lower Sloane Street', 'Twickenham', 'Ewell Village', 'Chipstead', ' Thornton',
     'Ewell', 'Harrow On The Hill', ' Richmond', 'Hinchley Wood', 'Redbridge', 'Marylebone', 'Hampton Wick', 'East Molesey',
     ' Harrow', 'Hillingdon', 'New Malden', 'Bedfont', 'Cheam', 'Sydney Road', ' Chessington', 'Whitton',
     'Chislehurst', 'Tadworth', 'Brentford', 'Holborn', 'St Mary Cray', 'Northwood Hills', 'Pimlico London', 'Edgware',
     'Mayfair', 'Rainham', 'Herts', ' Upminster', 'Perivale Greenford', 'Kenley', 'Eastcote Lane', 'North Cheam', 'Alperton',
     'Cranford', 'Feltham', ' Feltham', 'Isleworth', 'Yeading', 'Hampton Hill', 'Close To', 'Knightsbridge', 'Hatch End',
     'Pinner', 'Romford', 'Ilford', 'Covent Garden', 'Sutton', 'Kingston-Upon-Thames', 'Newbury Park', 'Wembley',
     'Norwood Green', ' Kingston Upon Thames, London', 'Pimlico', 'Emerson Park', 'Upminster', 'South Orpington',
     ' Stanmore', 'Horseferry Road', 'Banstead', ' Barnet', ' Stoneleigh', 'Forestdale', 'Stoneleigh', 'Shoreditch',
     'Brook Avenue', 'Benhill Wood Road', 'Northumberland Heath', 'City', 'London', 'Strand', 'Montpelier Rd',
     ' Pinner', 'Bexley', 'Cheam Village', 'Little Heath', 'Nr Biggin Hill', 'Chelsea', 'Thornton Heath', 'Hadley Wood',
     'West Molesey', ' Romford', 'Sanderstead', ' Pearson Square London', ' Hillingdon', ' Mitcham', 'Shortlands',
     'Rickmansworth', ' Isleworth', 'Belgravia', 'Havering', ' Sidcup', 'Hadley Green',
     'Teddington', 'Coulsdon', ' Hayes', 'Esher', 'West Wickham', 'Londres', 'Bexleyheath', 'Heston', 'Dagenham',
     'Chigwell', 'Mitcham', 'Arkley', 'Sudbury / Wembley', 'Woodford Green', 'Hampton', 'Harefield', 'Stourcliffe Street',
     'Thames Ditton', 'Hanwell Borders', 'Kingston', 'Hadley Highstone', 'Carshalton', ' Harefield', 'Epsom Downs', 'Harrow',
     'Sidup', 'Epsom', 'Sidcup', ' Epsom', 'Richmond', 'East Croydon', ' Croydon', 'Green',
     'Potters Bar', 'Ruislip Manor', 'Northolt', 'England', ' Cheam', 'Ickenham', 'Barking', 'Barnet', 'Cowley',
     'Tooting Junction', 'Ewell Court', 'Whitton/Hounslow', 'Surrey.', 'Worcester Park', 'High Holborn', 'Selsdon',
     'Devey Close', 'St Margarets', ' Sutton', ' Kew', 'Purley', 'Upper Belvedere'}

print(Test)

poubelle = 0
for element in Ville:
    if element not in a:
        poubelle +=1

print("poubelle=",poubelle)
print(set(Ville))

print(set(codepostal))

immobiler_5 = pd.DataFrame({
    "URL" : les_urls,
    "ville" : Ville,
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

print("duree=", time.time() - start_time)
