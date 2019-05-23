import requests
from bs4 import BeautifulSoup
import pandas as pd


website_url = requests.get("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population").text
soup = BeautifulSoup(website_url,"lxml")
# print(soup.prettify())
My_table = soup.find("table",{"class":"wikitable sortable"})
# print(My_table)
links = My_table.find_all("a")
# print(links)
Countries=[]
Link=[]
for link in links:
    if link.get("title"):
        Countries.append(link.get("title"))
        Link.append(link.get("href"))

df=pd.DataFrame()
df['Country']=Countries

# print(df)

for link in Link:
    url = requests.get("https://en.wikipedia.org"+link).text
    soup = BeautifulSoup(url, "lxml")
    print(soup)
    break