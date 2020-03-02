import pandas as pd
import csv
# Dataframe containing the data to plot
from math import log, cos, tan ,pi, radians
from random import randint
import folium

#locs = pd.DataFrame({'name': ['a','b'],'lat': [-22.951916, -43.210487], 'lon': [-13.163141, -72.544962]})

# import eoplotlib.

import geoplotlib

# Load the data

#data = locs[['lat', 'lon']]

def get_long_lat():
    file = open("ukpostcodes.csv", "r")
    reader = csv.reader(file)
    test = dict()
    postcode = []
    long = []
    lat = []
    for line in reader:
        t = line[1]
        t1 = line[2]
        t2 = line[3]
        y = t.split(' ')
        try:
            d = float(t1)
            e = float(t2)
            test[y[0]] = [d,e]
        except:
            pass
        postcode.append(y[0])
        lat.append(t1)
        long.append(t2)
    return postcode, lat , long , test

a = get_long_lat()[-1]
a.pop('postcode', None)
print("longueur a avant",len(a))
file_ter = open("postcode-outcodes.csv", "r")
reader = csv.reader(file_ter)
for line in reader:
    t = line[1]
    t1 = line[2]
    t2 = line[3]
    try:
        a[t] = [float(t1),float(t2)]
    except:
        pass
print("longueur a après",len(a))
#print(list(a.values())[1])
#print(get_long_lat()[-1])
#print(len(get_long_lat()[-1]))
# print(list(a.keys())[613])
# print(lat[613])
# print(lon[613])
g = {k: v for k, v in a.items() if (tan(radians(v[0])) + (1 / cos(radians(v[0])))) > 0}
print(len(g))
print(len(a))
d = {}
for k, v in a.items():
    if 0 not in v:
        d[k] = v
    else:
        indice = v.index(0)
        e = v[:]
        e[indice] = 0.0000000000000001
        d[k] = e
print(g)
f = list(g.values())
lat = [f[i][0] for i in range(len(g))]
lon = [f[i][1] for i in range(len(g))]
# print(sum(1 for i in lon[:614] if i < 0))
#locs = pd.DataFrame({'name': ['a','b'],'lat': [-22.951916, -43.210487], 'lon': [-13.163141, -72.544962]})
locs = pd.DataFrame({'postcode': list(g.keys()), 'lat' : lat, 'lon' : lon,})
# Pass the data to geoplotlib.plot
data = locs[['lat', 'lon']]


#geoplotlib.dot(data[1:2], color='b', point_size=1)
#geoplotlib.dot(data[2:3], color='r', point_size=10)
#geoplotlib.dot(data[1:3], color='r', point_size= 1)
#geoplotlib.kde(data[1:3], bw=[5, 5], cmap_levels=10, binsize=0.30)
#geoplotlib.kde(data[3:5], bw=[10, 10], cmap_levels=10, binsize=0.30)

# Display the map.

#geoplotlib.show()