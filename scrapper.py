import requests, re
from bs4 import BeautifulSoup
import pandas as pd


def web_scrapper(URL):
    website_url = requests.get(URL).text
    soup = BeautifulSoup(website_url, "lxml")
    return soup

def clean_location(loc):
    return re.sub(r"[^a-zA-Z0-9.]", "", loc)

def clean_unit(data):
    return re.sub(r"[^0-9]", "", data)

def clean_change(chg):
    chg.replace(u'\u2212', '-')
    return re.sub(r"[^0-9.]", "", chg)

def clean_string(string):
    return re.sub(r"[^a-zA-Z0-9]", "", string)

def clean_header(string):
    string = string.replace("/","").strip().lower()
    string = string.split(" ")
    string = " ".join(re.sub("s$","",re.sub("ies$","y",s)) for s in string)
    string = string.replace("•","").replace("\xa0","").strip()
    string =  re.sub("[\(\[].*?[\)\]]", "", string).strip().replace(")","")
    new_string = redundant_columns(string)
    if new_string :
        return new_string
    else:
        return string


def rearrange(df):
    d = df.columns.tolist()
    r = d.index('rank')
    c = d.index('city')
    s = d.index('state')
    print (r,c,s)
    seq = ['rank','city','state']+d[:c-1]+d[c+1:r-1]+d[r+1:s-1]+d[s+1:]
    df = df[seq]
    return df

def redundant_columns(s):
    #found manually
    if "incorporated" in s:
        return "incorporated"
    elif "airport" in s:
        return "airport"
    else:
        old={'city statu':'city status','consolidated':'consolidated city-county','foundation':'founded','founded a':'founded by',
             'gni feature id':'gni id','zip code prefixe':'zip code','zip codes':'zip code','assemblymembers':'assembly member',
             'assembly':'assembly member','assembly members':'assembly member','assemblymember':'assembly member','counties':'county',
             '[[federal infor\nmation processing standards|fip code]]':'fip code','fip code\n0':'fip code'}

        value = old.get(s)
        return value

def drop_less_informative_columns(df):
    threshold = 0.6
    b=df.isna().sum()[df.isna().sum()> 0]/len(df)
    cols=b[b>threshold].index
    df.drop(cols,inplace=True,axis=1)
    df.drop(['density','estimate','area code'], inplace=True, axis=1) #redundant with other existing column
    return df

wiki = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
soup = web_scrapper(wiki)
table = soup.find("table",{"class":"wikitable sortable"})

completedata=[]
City= []
Link=[]
d=0
for link in table.findAll('tr'):
    col_headers = {
        'rank': None,
        'city': None,
        'state': None,
        'Estimate2018': None,
        'Census2010': None,
        'Change': None,
        'Land Area2016 sqmi': None,
        'Land Area2016 sqkm': None,
        'Population Density2016 sqmi': None,
        'Population Density2016 sqkm': None,
        'Latitude': None,
        'Longitude': None
    }
    if link.findAll('td'):
        for i,(k,v) in enumerate(col_headers.items()):
            if i==2:
                col_headers[k]=clean_string(link.findAll('td')[i].findAll(text=True)[1])
            elif i==5:
                col_headers[k]=clean_change(link.findAll('td')[i].find(text=True))
            elif i in [6,7,8,9]:
                col_headers[k]=clean_unit(link.findAll('td')[i].find(text=True))
            elif i==10 or i==11:
                col_headers[k]=clean_location(link.findAll('td')[10].findAll(text=True)[4].split(" ")[i%10])
            elif i==1:
                col_headers[k]=link.findAll('td')[i].find(text=True)
            else:
                col_headers[k]=clean_unit(link.findAll('td')[i].find(text=True))

        lnk = str(link.findAll('td')[1].find_all('a')[0].get("href").replace("%E2%80%93","-"))
        # Link.append(lnk)
        soup = web_scrapper('https://en.wikipedia.org/'+lnk)
        city = soup.find("table", {"class": "infobox"})
        for row in city.findAll('tr'):
            if row.findAll('td'):
                if len(row.findAll('th')) == 1 and len(row.findAll('td')) == 1:
                    h = clean_header(row.findAll('th')[0].text)
                    dat = row.findAll('td')[0].text.strip()
                    if col_headers.get(h):
                        continue
                    else:
                        col_headers[h]=dat
        completedata.append(col_headers)

    if d>10:
        break
    else:
        d+=1


df2=pd.DataFrame(completedata)

df2 = rearrange(df2)
df2 = drop_less_informative_columns(df2)

print(df2.columns.tolist())


#to be cleaned : city, state , rank appearing twice
#to be cleaned things in bracket mayor , incorporated, metro, type, water, zip code

new_data = {}
print(df2["city"])
soup = web_scrapper('https://www.numbeo.com/cost-of-living/region_rankings.jsp?title=2019&region=021')
COL = soup.find("table", {"id": "t2"})
COL_body = COL.find('tbody')
COL_rows = COL_body.find_all('tr')
living = {}
for col_row in COL_rows:
    cty = col_row.findAll('td')[1].text
    data = col_row.findAll('td')[2].text
    # header = col_row.findAll('th')
    if cty.split(",")[-1].lower().strip() == 'united states' :
        if cty.split(",")[0] in df2["city"].tolist():
            living[cty.split(",")[0]]=data
        elif cty.split(",")[0].lower().strip()== 'new york':
            living['New York City']=data

lst=[]
for e in df2["city"].tolist():
    lst.append(living.get(e))

df2["Cost of living"] = lst
df2.to_csv("MajorCities.csv", index=False, encoding='utf-8-sig')


# data = pd.read_html(str(table))
#
# df = pd.concat(data)
# # print(df.columns.values)
# # print(data[0].columns.values)
# df.columns=cols
# df.to_csv("try1.csv",index=False,encoding='utf-8-sig')
# print(df['2018 estimate'])
#
# information ={
#     'postalCode' : [],
#     'areaCode' : [],
#     'areaLand' : [],
#     'areaWater' : [],
#     'elevation' : [],
#     'populationTotalRanking' : [],
#     'utcOffset' : [],
#     'areaTotal' : [],
#     'governmentType' : [],
#     'leaderTitle' : [],
#     'populationDensity' : [],
#     'populationTotal' : [],
#     # 'establishedDate' : [],
#     # 'latd': [],
#     # 'longd': [],
#     'areaMetro' : [],
#     'timeZone' : []
# }






# # Major cities Data from DBpedia
# for link in Link:
#     data = requests.get('http://dbpedia.org/data/'+link[6:]+'.json').json()
#     uri = data['http://dbpedia.org/resource/'+link[6:]]
#     for k,v in information.items():
#         if 'http://dbpedia.org/ontology/'+k in uri and k=='areaCode':
#             temp = str(uri['http://dbpedia.org/ontology/' + k][0]['value'])\
#                 .replace("&minus;", "-").replace(":00", "").replace("−", "-")\
#                 .replace("&",",").replace(",",", ").replace("/",", ").replace("and",", ")
#             temp = re.sub("[^0-9^,^ ]","",temp)
#             information[k].append(temp)
#
#         elif 'http://dbpedia.org/ontology/'+k in uri and k != 'timeZone' and k != 'governmentType':
#             information[k].append(str(uri['http://dbpedia.org/ontology/' + k][0]['value'])
#                                   # .replace("&",",").replace("and",",").replace("/",",")
#                                   .replace("&minus;","-").replace(":00","").replace("−","-").replace("−", "-").replace("−0", "-"))
#         elif 'http://dbpedia.org/ontology/'+k in uri and (k == 'governmentType' or k == 'timeZone'):
#             information[k].append(uri['http://dbpedia.org/ontology/' + k][0]['value'][28:].replace("–"," ").replace("_"," "))
#         else:
#             information[k].append("N/A")
# for k,v in information.items():
#     df[k]=v
#
# df.to_csv("DBpediaMajorCities.csv",index=False,encoding='utf-8-sig')
