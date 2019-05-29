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
    return re.sub(r"[^0-9.]", "", data)

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
        old={'city statu':'city status','consolidated':'consolidated city-county','foundation':'founded',
             'founded a':'founded by','gni feature id':'gni id','zip code prefixe':'zip code',
             'zip codes':'zip code','assemblymembers':'assembly member','assembly':'assembly member',
             'assembly members':'assembly member','assemblymember':'assembly member','counties':'county',
             '[[federal infor\nmation processing standards|fip code]]':'fip code','fip code\n0':'fip code'}

        value = old.get(s)
        return value

def drop_less_informative_columns(df):
    threshold = 0.6
    b=df.isna().sum()[df.isna().sum()> 0]/len(df)
    cols=b[b>threshold].index
    df.drop(cols,inplace=True,axis=1)
    df.drop(['density','estimate','area code','zip code'], inplace=True, axis=1) #redundant with other existing column
    return df

def remove_brackets(lst1):
    new_lst1=[]
    for e1 in lst1:
        if str(type(e1)) != 'nan':
            e1 = re.sub(r" ?\[[^)]+\]", "", str(e1)).strip()
            e1 = re.sub(r" ?\([^)]+\)", "", e1).strip()
        new_lst1.append(e1)
    return new_lst1

def clean_unit_col(lst2):
    new_lst2=[]
    for e2 in lst2:
        if "-" in e2:
            e2= e2.split("-")[1]
        if "%" in e2:
            e2 = e2.split(" ")[0]
        new_lst2.append(re.sub(r"[^0-9.]", "", e2))
    return new_lst2

def float_format(lst3):
    new_lst3=[]
    for e3 in lst3:
        if e3.strip() == '.':
            e3 = ""
        if e3.strip():
            e3 = float(e3)
        new_lst3.append(e3)
    return new_lst3

def scrap_wikipedia(table2):
    completedata2 = []
    for link in table2.findAll('tr'):
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
            for i, (k, v) in enumerate(col_headers.items()):
                if i == 2:
                    col_headers[k] = clean_string(link.findAll('td')[i].findAll(text=True)[1])
                elif i == 5:
                    col_headers[k] = clean_change(link.findAll('td')[i].find(text=True))
                elif i in [6, 7, 8, 9]:
                    col_headers[k] = clean_unit(link.findAll('td')[i].find(text=True))
                elif i == 10 or i == 11:
                    col_headers[k] = clean_location(link.findAll('td')[10].findAll(text=True)[4].split(" ")[i % 10])
                elif i == 1:
                    col_headers[k] = link.findAll('td')[i].find(text=True)
                else:
                    col_headers[k] = clean_unit(link.findAll('td')[i].find(text=True))

            lnk2 = str(link.findAll('td')[1].find_all('a')[0].get("href").replace("%E2%80%93", "-"))
            soup2 = web_scrapper('https://en.wikipedia.org/' + lnk2)
            city = soup2.find("table", {"class": "infobox"})
            for row in city.findAll('tr'):
                if row.findAll('td'):
                    if len(row.findAll('th')) == 1 and len(row.findAll('td')) == 1:
                        h = clean_header(row.findAll('th')[0].text)
                        dat = row.findAll('td')[0].text.strip()
                        if col_headers.get(h):
                            continue
                        else:
                            col_headers[h] = dat
            completedata2.append(col_headers)
    return completedata2

def scrap_page(COL2):
    COL_body2 = COL2.find('tbody')
    COL_rows2 = COL_body2.find_all('tr')
    living2 = {}
    for col_row2 in COL_rows2:
        cty2 = col_row2.findAll('td')[1].text
        data2 = col_row2.findAll('td')[2].text
        # header = col_row.findAll('th')
        if cty2.split(",")[-1].lower().strip() == 'united states':
            if cty2.split(",")[0] in df2["city"].tolist():
                living2[cty2.split(",")[0]] = data2
            elif cty2.split(",")[0].lower().strip() == 'new york':
                living2['New York City'] = data2
    return living2

def scrap_other(COL3):
    COL_body3 = COL3.findAll('li')
    traffic3 = {}
    for lst3 in COL_body3:
        raw = lst3.text.split(",")
        cty = raw[0]
        hours = raw[1].split(":")[1][:-3].strip("hours").strip()
        if cty in df2["city"].tolist():
            traffic3[cty] = float(hours.replace("hours","").strip())
    return traffic3

if __name__=='__main__':

    wiki = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
    soup = web_scrapper(wiki)
    table = soup.find("table",{"class":"wikitable sortable"})
    completedata = scrap_wikipedia(table)
    df2=pd.DataFrame(completedata)
    df2 = rearrange(df2)
    df2 = drop_less_informative_columns(df2)

    #Additional data : Cost of Living in major cities
    #This column may contain null values [Why? Refer to ReadMe].

    soup = web_scrapper('https://www.numbeo.com/cost-of-living/region_rankings.jsp?title=2019&region=021')
    COL = soup.find("table", {"id": "t2"})
    living= scrap_page(COL)
    lst=[]
    for e in df2["city"].tolist():
        lst.append(living.get(e))
    df2["Cost of living Index"] = lst

    #Additional Data: Average annual hours spent in traffic
    #Non conventional database
    #non table data
    lnk = 'https://www.forbes.com/sites/jimgorzelany/2019/02/11/here-are-the-u-s-cities-' \
          'suffering-the-worst-traffic-congestion/#1506f0e36e36'
    soup = web_scrapper(lnk)
    COL = soup.find("ol")
    traffic=scrap_other(COL)
    new_lst=[]
    for e in df2["city"].tolist():
        new_lst.append(traffic.get(e))
    df2["Average annual traffic hours"] = new_lst

    # Cleaning columns data changing formats

    brack_cols=['mayor','elevation','type','water','metro','land']
    for c in brack_cols:
        df2[c] = remove_brackets(df2[c].tolist())

    unit_cols=['elevation','land','metro','water','rank','Census2010','Estimate2018','Land Area2016 sqkm',
               'Land Area2016 sqmi','Population Density2016 sqkm','Population Density2016 sqmi']
    for c in unit_cols:
        df2[c] = clean_unit_col(df2[c].tolist())
        print(c)
        df2[c] = float_format(df2[c].tolist())

    df2.to_csv("MajorCities.csv", index=False, encoding='utf-8-sig')

    # Major cities Data from DBpedia
    # DBpedia was explored as well but turns out, there are much recent and updated information on other pages.

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