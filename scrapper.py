import requests
from bs4 import BeautifulSoup
import pandas as pd

website_url = requests.get("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population").text
soup = BeautifulSoup(website_url,"lxml")
My_table = soup.find("table",{"class":"wikitable sortable"})
links = My_table
City= []
Link=[]
for link in links.findAll('tr'):
    if link.findAll('td'):
        City.append(str(link.findAll('td')[1].find_all('a')[0].get("title")))
        Link.append(str(link.findAll('td')[1].find_all('a')[0].get("href").replace("%E2%80%93","-")))

df=pd.DataFrame()
df['City']=City
c=0
information ={
    'postalCode' : [],
    'areaCode' : [],
    'areaLand' : [],
    'areaWater' : [],
    'elevation' : [],
    'populationTotalRanking' : [],
    'utcOffset' : [],
    'areaTotal' : [],
    'governmentType' : [],
    'leaderTitle' : [],
    'populationDensity' : [],
    'populationTotal' : [],
    'establishedDate' : [],
    'latd': [],
    'longd': [],
    'areaMetro' : [],
    'timeZone' : []
}

for link in Link:
    data = requests.get('http://dbpedia.org/data/'+link[6:]+'.json').json()
    uri = data['http://dbpedia.org/resource/'+link[6:]]
    for k,v in information.items():
        if 'http://dbpedia.org/ontology/'+k in uri and k != 'timeZone' and k != 'governmentType':
            information[k].append(uri['http://dbpedia.org/ontology/' + k][0]['value'])
        elif 'http://dbpedia.org/ontology/'+k in uri and (k == 'governmentType' or k == 'timeZone'):
            print(k)
            information[k].append(uri['http://dbpedia.org/ontology/' + k][0]['value'][28:])
        else:
            information[k].append(None)

for k,v in information.items():
    df[k]=v
print (df['timeZone'],df['governmentType'])