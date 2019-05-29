# MajorCitiesWikipedia

#### A scrapper for major cities in USA.

---
## Installation of packages and libraries

Install the requirements in requirements.txt:
```
pip install -r requirements.txt
```
### Start scrapping

Then run the scrapper.py file :
```
python scrapper.py
```
The final CSV will be saved as 'MajorCities.csv'

---

### Steps taken for Data preperation

The scipt scrapper.py is designed to demonstrate Web Scrapping Unconventional Datasets, Cleaning, Transforming and Storing skills. 

1. Entier table is scrapped from [List of United States cities by population](https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population).
2. For row, i.e. city from the table, the respective city's wiki page is scrapped for additional data.
3. While scarping, regex is used to clean the data format. Other formats like location, units are also handled while scraping.
4. Collected data headers may be redundant or may contain non-significant data. Therefore, columns with same data but different header names are combined.
5. Null values are handled by dropping the columns with 60% or more null values.
6. Additional data can be collected for these cities from other webpages. Since there was no particular usecase for this dataset, [Cost of Living in Major Cities in North America](https://www.numbeo.com/cost-of-living/region_rankings.jsp?title=2019&region=021) , [Average annual hours spent in traffic](https://www.forbes.com/sites/jimgorzelany/2019/02/11/here-are-the-u-s-cities-suffering-the-worst-traffic-congestion/#1506f0e36e36) have been scrapped for demonstration.
Though these datasets are not as robost as the list of cities we are working with, the idea is to demonstrate web scrapping skills. Other than scrapping Wikipedia tables, the Cost of Living column demonstrates scrapping tables from other than wikipedia pages, and Average annual traffic hours demonstrate scrapping non-tables i.e., lists. 

#### Note
DBpedia was also explored during this project. On comparison with scrapped wikipedia data, DBpedia data seemed to be outdated which may be suitable for research purpose. In our case, the script is more focused to capture recent data availlable.

While experimenting, there were several websites with restricted number of requests. Those websites have been skipped for final demonstration. 
