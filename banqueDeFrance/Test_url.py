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
outil = ['London', 'West Midlands', 'Greater Manchester', 'West Yorkshire', 'Kent', 'Essex', 'Merseyside',
         'South Yorkshire', 'Hampshire', 'Lancashire', 'Surrey', 'Hertfordshire', 'Tyne and Wear', 'Norfolk', 'Staffordshire',
         'West Sussex', 'Nottinghamshire', 'Derbyshire', 'Devon', 'Suffolk', 'Lincolnshire', 'Northamptonshire', 'Oxfordshire',
         'Leicestershire', 'Cambridgeshire', 'North Yorkshire', 'Gloucestershire', 'Worcestershire', 'Warwickshire', 'Cornwall',
         'Somerset', 'East Sussex', 'County Durham', 'Buckinghamshire', 'Cumbria', 'Wiltshire', 'Bristol', 'Dorset', 'Cheshire East',
         'East Riding of Yorkshire', 'Leicester', 'Cheshire West and Chester', 'Northumberland', 'Shropshire', 'Nottingham',
         'Brighton & Hove', 'Medway', 'South Gloucestershire', 'Plymouth', 'Hull', 'Central Bedfordshire', 'Milton Keynes',
         'Derby', 'Stoke-on-Trent', 'Southampton', 'Swindon', 'Portsmouth', 'Luton', 'North Somerset', 'Warrington', 'York',
         'Stockton-on-Tees', 'Peterborough', 'Herefordshire', 'Bournemouth', 'Bath and North East Somerset', 'Southend-on-Sea',
         'North Lincolnshire', 'Telford and Wrekin', 'North East Lincolnshire', 'Thurrock', 'Bedford', 'Reading', 'Wokingham',
         'West Berkshire', 'Poole', 'Blackburn with Darwen', 'Windsor and Maidenhead', 'Blackpool', 'Slough', 'Middlesbrough',
         'Isle of Wight', 'Redcar and Cleveland', 'Torbay', 'Halton', 'Bracknell Forest', 'Darlington', 'Hartlepool', 'Rutland',
         'Isles of Scilly']


outil_bis = [element.replace(" ","-") for element in outil]

print(outil_bis)

print(outil_bis.index("Cheshire-East"))
print(len(outil_bis))
BASE = ["https://www.zoopla.co.uk/for-sale/property/"+ element +"/?identifier=" + element + "&q=" + element + "&search_source=refine&radius=0&page_size=100&pn=1" for element in outil_bis]
print(BASE[38:])
print(BASE)

url = BASE[38]

#on définit notre agent afin de ne pas être pris pour un robot par le site
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

#on effectue une requête afin d'obtenir la page
page = requests.get(url, headers = agent)

#on affiche la page selon son code HTML ce qui permet de travailler en parallèle avec l'outil inspecter de Chrome
# où on voit également le code html

soup = BeautifulSoup(page.content, 'html.parser')

#on récupère dans la page ce qui nous interesse cad les annonces
annonces = soup.find_all( class_ = "listing-results-wrapper")
prix = [re.sub("[^0-9]", "", annonce.find(class_="listing-results-price text-price").get_text())
                       if re.sub("[^0-9]", "", annonce.find(class_="listing-results-price text-price").get_text()) != ''
                       else "NA" for annonce in annonces]
print(annonces)