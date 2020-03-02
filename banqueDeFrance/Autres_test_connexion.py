from proxy_requests import ProxyRequests
from proxy_requests import ProxyRequests, ProxyRequestsBasicAuth
import requests
import pandas as pd
from bs4 import BeautifulSoup

page = requests.get('https://forecast.weather.gov/MapClick.php?lat=34.05349000000007&lon=-118.24531999999999#.XiXcNlNKhQI')
#print(page.status_code)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup)
week = soup.find(id = 'seven-day-forecast-body')
# print(week)

items = week.find_all(class_ = 'tombstone-container')
print(items[0])
url = 'https://forecast.weather.gov/MapClick.php?lat=34.05349000000007&lon=-118.24531999999999#.XiXcNlNKhQI'
r = ProxyRequests(url)
r.get()
r.get_json()
r.get_proxy_used()