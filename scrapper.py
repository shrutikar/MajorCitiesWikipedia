import requests
from bs4 import BeautifulSoup
import pandas as pd


website_url = requests.get("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population").text
soup = BeautifulSoup(website_url,"lxml")
# print(soup.prettify())
My_table = soup.find("table",{"class":"wikitable sortable"})
# print(My_table)
links = My_table
i=0
City= []
Link=[]
for link in links.findAll('tr'):
    if link.findAll('td'):
        City.append(str(link.findAll('td')[1].find_all('a')[0].get("title")))
        Link.append(str(link.findAll('td')[1].find_all('a')[0].get("href")))

df=pd.DataFrame()
df['City']=City
print(df)

for link in Link:
    url = requests.get("https://en.wikipedia.org"+link).text
    soup = BeautifulSoup(url, "lxml")
    table = soup.find('table',{'class': 'infobox geography vcard'})
    results = table.find_all('tr')
    # print(type(results))
    # print('Number of results', len(results))
    # print(results)
    fresult = [e.text for e in results]
    # print(fresult)
    result = {}
    exceptional_row_count = 0
    for tr in table.find_all('tr'):
        print(tr)
        if tr.find('th'):
            result[tr.find('th').text] = tr.find('td').text
        else:
            # the first row Logos fall here
            exceptional_row_count += 1
    if exceptional_row_count > 1:
        print('WARNING ExceptionalRow>1: ', table)
    print(result)
    break