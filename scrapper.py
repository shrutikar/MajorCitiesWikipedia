import requests, re
from bs4 import BeautifulSoup
import pandas as pd

website_url = requests.get("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population").text
soup = BeautifulSoup(website_url,"lxml")
My_table = soup.find("table",{"class":"wikitable sortable"})
links = My_table
City= []
Link=[]
d=0
for link in links.findAll('tr'):
    if link.findAll('td'):
        City.append(str(link.findAll('td')[1].find_all('a')[0].get("title")))
        Link.append(str(link.findAll('td')[1].find_all('a')[0].get("href").replace("%E2%80%93","-")))
    # if d>10:
    #     break
    # else:
    #     d+=1
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
    # 'establishedDate' : [],
    # 'latd': [],
    # 'longd': [],
    'areaMetro' : [],
    'timeZone' : []
}

for link in Link:
    data = requests.get('http://dbpedia.org/data/'+link[6:]+'.json').json()
    uri = data['http://dbpedia.org/resource/'+link[6:]]
    for k,v in information.items():
        if 'http://dbpedia.org/ontology/'+k in uri and k=='areaCode':
            temp = str(uri['http://dbpedia.org/ontology/' + k][0]['value'])\
                .replace("&minus;", "-").replace(":00", "").replace("−", "-")\
                .replace("&",",").replace(",",", ").replace("/",", ").replace("and",", ")
            temp = re.sub("[^0-9^,^ ]","",temp)
            information[k].append(temp)

        elif 'http://dbpedia.org/ontology/'+k in uri and k != 'timeZone' and k != 'governmentType':
            information[k].append(str(uri['http://dbpedia.org/ontology/' + k][0]['value'])
                                  # .replace("&",",").replace("and",",").replace("/",",")
                                  .replace("&minus;","-").replace(":00","").replace("−","-"))
        elif 'http://dbpedia.org/ontology/'+k in uri and (k == 'governmentType' or k == 'timeZone'):
            information[k].append(uri['http://dbpedia.org/ontology/' + k][0]['value'][28:].replace("–"," ").replace("_"," "))
        else:
            information[k].append("N/A")
for k,v in information.items():
    df[k]=v

df.to_csv("MajorCities.csv",index=False,encoding='utf-8-sig')