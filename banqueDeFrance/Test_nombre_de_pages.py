import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import sys



start_time = time.time()

#url du site
url = "https://www.zoopla.co.uk/for-sale/property/bedfordshire/?identifier=bedfordshire&q=bedfordshire&search_source=refine&radius=0&page_size=100&pn=2"

#on définit notre agent afin de ne pas être pris pour un robot par le site
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

#on effectue une requête afin d'obtenir la page
page = requests.get(url, headers = agent)

#on affiche la page selon son code HTML ce qui permet de travailler en parallèle avec l'outil inspecter de Chrome
# où on voit également le code html

soup = BeautifulSoup(page.content, 'html.parser')

nombre = int(re.findall("\d+", soup.find( class_ = "paginate bg-muted").get_text())[-1])
print(nombre)
print(type(nombre))