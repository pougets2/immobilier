import csv


file=open("list-counties-uk-86j.csv", "r")
reader = csv.reader(file)
counties = []
for line in reader:
    t=line[1]
    counties.append(t)

print(len(counties))
print(counties[2])