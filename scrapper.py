import requests
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata

def strip_non_ascii(s):

    if isinstance(s, str):
        nfkd = unicodedata.normalize('NFKD', s)
        return str(nfkd.encode('ASCII', 'ignore').decode('ASCII'))
    else:
        return s

website_url = requests.get("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population").text
soup = BeautifulSoup(website_url,"lxml")
# print(soup.prettify())
My_table = soup.find("table",{"class":"wikitable sortable"})
# print(My_table)
links = My_table
City= []
Link=[]
for link in links.findAll('tr'):
    if link.findAll('td'):
        City.append(str(link.findAll('td')[1].find_all('a')[0].get("title")))
        Link.append(str(link.findAll('td')[1].find_all('a')[0].get("href").replace("%E2%80%93","-")))

df=pd.DataFrame()
df['City']=City
# print(df)

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
    print(link[6:])

    data = requests.get('http://dbpedia.org/data/'+link[6:]+'.json').json()
    uri = data['http://dbpedia.org/resource/'+link[6:]]
    for k,v in information.items():
        if 'http://dbpedia.org/ontology/'+k in uri and k != ('timeZone' and 'governmentType'):
            information[k].append(uri['http://dbpedia.org/ontology/'+k][0]['value'])
        elif 'http://dbpedia.org/ontology/'+k in uri and k == ('governmentType' or 'timeZone'):
            information[k].append(uri['http://dbpedia.org/ontology/' + k][0]['value'][28:])
        else:
            information[k].append(None)
    # areacode = matteo['http://dbpedia.org/ontology/areaCode'][0]['value']
    # arealand = matteo['http://dbpedia.org/ontology/areaLand'][0]['value']
    # areawater = matteo['http://dbpedia.org/ontology/areaWater'][0]['value']
    # elevation = matteo['http://dbpedia.org/ontology/elevation'][0]['value']
    # populationtotalranking = matteo['http://dbpedia.org/ontology/populationTotalRanking'][0]['value']
    # utcoffset = matteo['http://dbpedia.org/ontology/utcOffset'][0]['value']
    # areatotal = matteo['http://dbpedia.org/ontology/areaTotal'][0]['value']
    # governmenttype = matteo['http://dbpedia.org/ontology/governmentType'][0]['value'][28:]
    # leadertype = matteo['http://dbpedia.org/ontology/leaderTitle'][0]['value']
    # populationdensity = matteo['http://dbpedia.org/ontology/populationDensity'][0]['value']
    # populationtotal = matteo['http://dbpedia.org/ontology/populationTotal'][0]['value']
    # establisheddate = matteo['http://dbpedia.org/property/establishedDate'][0]['value']
    # establishedyear = matteo['http://dbpedia.org/property/establishedDate'][1]['value']
    # latd = matteo['http://dbpedia.org/property/latd'][0]['value']
    # longd = matteo['http://dbpedia.org/property/longd'][0]['value']
    # longew = matteo['http://dbpedia.org/property/longew'][0]['value']
    # latns = matteo['http://dbpedia.org/property/latns'][0]['value']
    # areametro = matteo['http://dbpedia.org/ontology/areaMetro'][0]['value']
    # timezone = matteo['http://dbpedia.org/ontology/timeZone'][0]['value'][28:]

    # print(areacode, arealand, areawater, elevation, utcoffset, areatotal,
    #       governmenttype, leadertype, populationtotal, latd, longd, longew, latns,
    #       timezone)

    # if c>30:
    #     break
    # else:
    #     c+=1
# print(information)

for k,v in information.items():
    df[k]=v
print (df)