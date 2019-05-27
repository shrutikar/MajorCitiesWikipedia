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
        Link.append(str(link.findAll('td')[1].find_all('a')[0].get("href")))

df=pd.DataFrame()
df['City']=City
# print(df)
c=0
Information = ['City', 'State', 'Coordinates', 'Area-Total','Area-Land','Area-Water','Area-Metro','Elevation','PopulationEstimate','Timezones','ZipCodes','AreaCodes']
city,State,Coordinates,AreaTotal,AreaLand,AreaWater,AreaMetro,Elevation,PopulationEstimate,Timezones,ZipCodes,AreaCodes=[],[],[],[],[],[],[],[],[],[],[],[]
for link in Link:
    # url = requests.get("https://en.wikipedia.org"+link).text
    # soup = BeautifulSoup(url, "lxml")
    # table = soup.find('table',{'class': 'infobox geography vcard'})
    # results = table.find_all('tr')
    # # for i,tr in enumerate(table.find_all('tr')):
    # #     print(i,tr.text)
    # #     string=str(tr.text).lower()
    # #     if string[0:5] == 'state':
    # #         # print("{0}".format('*'*10))
    # #         State.append(strip_non_ascii(string.split('state')[1]).strip(" ").strip("\n"))
    # #     if string[0:11] == 'coordinates':
    # #         # print("{0}".format('*' * 10))
    # #         # print(string.split('coordinates')[1].strip(" ").strip(":"))
    # #         Coordinates.append(string.split('coordinates')[1].strip(" ").strip(":").replace("\ufeff"," "))
    # #     if strip_non_ascii(string).strip(" ")[0:5]=='total':
    # #         print("{0}".format('*' * 10))
    # #         print(string.split('total')[1].strip(" ").strip(":"))

    print(link[6:])

    data = requests.get('http://dbpedia.org/data/'+link[6:]+'.json').json()
    matteo = data['http://dbpedia.org/resource/'+link[6:]]
    # postalcode = matteo['http://dbpedia.org/ontology/postalCode'][0]['value']
    areacode = matteo['http://dbpedia.org/ontology/areaCode'][0]['value']
    arealand = matteo['http://dbpedia.org/ontology/areaLand'][0]['value']
    areawater = matteo['http://dbpedia.org/ontology/areaWater'][0]['value']
    elevation = matteo['http://dbpedia.org/ontology/elevation'][0]['value']
    # populationtotalranking = matteo['http://dbpedia.org/ontology/populationTotalRanking'][0]['value']
    utcoffset = matteo['http://dbpedia.org/ontology/utcOffset'][0]['value']
    areatotal = matteo['http://dbpedia.org/ontology/areaTotal'][0]['value']
    governmenttype = matteo['http://dbpedia.org/ontology/governmentType'][0]['value']
    leadertype = matteo['http://dbpedia.org/ontology/leaderTitle'][0]['value']
    # populationdensity = matteo['http://dbpedia.org/ontology/populationDensity'][0]['value']
    populationtotal = matteo['http://dbpedia.org/ontology/populationTotal'][0]['value']
    # establisheddate = matteo['http://dbpedia.org/property/establishedDate'][0]['value']
    # establishedyear = matteo['http://dbpedia.org/property/establishedDate'][1]['value']
    latd = matteo['http://dbpedia.org/property/latd'][0]['value']
    longd = matteo['http://dbpedia.org/property/longd'][0]['value']
    longew = matteo['http://dbpedia.org/property/longew'][0]['value']
    latns = matteo['http://dbpedia.org/property/latns'][0]['value']
    # areametro = matteo['http://dbpedia.org/ontology/areaMetro'][0]['value']
    timezone = matteo['http://dbpedia.org/ontology/timeZone'][0]['value']

    print(areacode, arealand, areawater, elevation, utcoffset, areatotal,
          governmenttype, leadertype, populationtotal, latd, longd, longew, latns,
          timezone)

    if c>10:
        break
    else:
        c+=1
# print(State,Coordinates)
