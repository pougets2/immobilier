import csv
import pandas as pd

file = open("2020-02-28.csv", "r")
reader = csv.reader(file)
datas = pd.read_csv(file)
del datas['URL']
del datas['Unnamed: 0']
file.close()

file2 = open('caca_ter.csv', 'r')
reader2 = csv.reader(file2)
datas2 = pd.read_csv(file2)
del datas2['URL']
del datas2['Unnamed: 0']
print(datas.count())
print(datas2.count())
file2.close()
# with open('caca_ter.csv', 'r') as t1, open('2020-02-28.csv', 'r') as t2:
#     fileone = t1.readlines()
#     filetwo = t2.readlines()
#
# with open('update.csv', 'w') as outFile:
#     for line in filetwo:
#         if line not in fileone:
#             outFile.write(line)

print("final")
print(pd.concat([datas, datas2]).drop_duplicates().count())
df_2notin1 = datas2[~(datas2['ville'].isin(datas['ville']) & datas2['code postal'].isin(datas['code postal'])
                      & datas2['Adresses'].isin(datas['Adresses'])& datas2['prix livre'].isin(datas['prix livre'])
                      & datas2['surface m2'].isin(datas['surface m2'])& datas2['Enchere ou vente'].isin(datas['Enchere ou vente'])
                      & datas2['Etat neuf ou ancien'].isin(datas['Etat neuf ou ancien'])& datas2['Nombre de chambres'].isin(datas['Nombre de chambres'])
                      & datas2['Nombre de SDB'].isin(datas['Nombre de SDB']) & datas2['Nombre de séjour'].isin(datas['Nombre de séjour'])
                      & datas2['Description'].isin(datas['Description']) & datas2['Type bien'].isin(datas['Type bien'])
                      & datas2['Aide'].isin(datas['Aide']))].reset_index(drop=True)
print(df_2notin1.count())
print(datas[~datas.isin(datas2)].dropna())


