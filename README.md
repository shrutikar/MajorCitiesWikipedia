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
6. Additional data can be collected for these cities from other webpages like:. Since there was no particular usecase for this dataset, [Cost of Living in Major Cities in North America](https://www.numbeo.com/cost-of-living/region_rankings.jsp?title=2019&region=021) , []() have been scrapped for demonstration.

#### Note
DBpedia was also explored during this assignment. On comparison with scrapped wikipedia data and DBpedia data, DBpedia data seemed to be outdated. This may be suitable for research purpose. The script is more focused to capture recent data availlable.
