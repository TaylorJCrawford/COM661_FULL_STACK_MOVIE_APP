import json
import re

# title, language, overview, popularity, release_date, production_companies, genres

file = open('./Processed/movies_metadata.json', 'r')

regex_p = re.compile("'name': ([^:]+(?=,|$))")

data = json.load(file)

dic = {}

def breakdown_map(dataSet, result):

    for item in dataSet:
        item = item.replace("'", "")
        item = item.replace("}", "")
        item = item.replace("]", "")
        result.append([item])

for record in data:
    # for each record:

    genres_list = []
    production_companies_list = []
    genres = record["genres"]
    production_companies = record["production_companies"]

    try:
        dataSet = regex_p.findall(genres)
        breakdown_map(dataSet, genres_list)
    except:
        pass
    try:
        dataSet2 = regex_p.findall(production_companies)
        breakdown_map(dataSet2, production_companies_list)
    except:
        pass

    id = record["id"]
    title = record["title"]
    language = record["original_language"]
    overview = record["overview"]
    popularity = record["popularity"]
    release_date = record["release_date"]


    dic[record["id"]] = {
        "id" : id,
        "title" : title,
        "language" : language,
        "overview" : overview,
        "popularity" : popularity,
        "release_date" : release_date,
        "production_companies" : production_companies_list,
        "genres" : genres_list
    }

print(dic['11862']) 
