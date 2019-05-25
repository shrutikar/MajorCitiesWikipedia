import requests
from bs4 import BeautifulSoup
import pandas as pd


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
print(df)
c=0
Information = ['City', 'State', 'Coordinates', 'Area-Total','Area-Land','Area-Water','Area-Metro','Elevation','PopulationEstimate','Timezones','ZipCodes','AreaCodes']
city,State,Coordinates,AreaTotal,AreaLand,AreaWater,AreaMetro,Elevation,PopulationEstimate,Timezones,ZipCodes,AreaCodes=[],[],[],[],[],[],[],[],[],[],[],[]
for link in Link:
    url = requests.get("https://en.wikipedia.org"+link).text
    soup = BeautifulSoup(url, "lxml")
    table = soup.find('table',{'class': 'infobox geography vcard'})
    results = table.find_all('tr')
    for i,tr in enumerate(table.find_all('tr')):
        print(i,tr.text)
        string=str(tr.text).lower()
        if string[0:5] == 'state':
            print("{0}".format('*'*10))
            print(string.split('state')[1].strip(" "))
    if c>0:
        break
    else:
        c+=1
# print(State)
