from cmath import e
from html import entities
import json
import re
from tokenize import Double

# title, language, overview, popularity, release_date, production_companies, genres

file = open('./Processed/movies_metadata.json', 'r')

regex_p = re.compile("'name': ([^:]+(?=,|$))")

data = json.load(file)

dic_meta = {}

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


    dic_meta[record["id"]] = {
        "id" : id,
        "title" : title,
        "language" : language,
        "overview" : overview,
        "popularity" : popularity,
        "release_date" : release_date,
        "production_companies" : production_companies_list,
        "genres" : genres_list
    }

# print(dic_meta['11862']) 

file.close()

# CAST
# {ID, { <character>, <name> }}

file = open('./Processed/credits.json', 'r')

regex_p_name = re.compile("'name': ([^:]+(?=,|$))")
regex_p_character = re.compile("'character': ([^:]+(?=,|$))")

data = json.load(file)

dic_credits= {}

def breakdown_map_credits(name, character, result):
    for idx, actor in enumerate(name):

        try:
            character_idx = character[idx]
        except:
            character_idx = ""
        actor = actor.replace("'", "")
        character_idx = character_idx.replace("'", "")

        result.append([character_idx, actor])

for record in data:
    outcome = []

    id = record['id']
    cast = record['cast']

    templist_cast_name = regex_p_name.findall(cast)
    templist_cast_char = regex_p_character.findall(cast)
    breakdown_map_credits(templist_cast_name, templist_cast_char, outcome)

    dic_credits[id] = outcome

# print(dic_credits["862"]) # Toy Story


file.close()

# {ID, [ < keywords > ]}

# ---------------------------------------- Keywords ------------------------------------------------

regex_p = re.compile("'name': ([^:]+(?=,|$))")

# Read in data from json file.
file = open('./Processed/keywords.json', 'r')

data = json.load(file)

dic_keywords = {}

for record in data:
    templist = []
    # print(record)
    # print("**********************************************")
    keywords = record["keywords"]
    id = record["id"]
    result = regex_p.findall(keywords)
    for word in result:
        word = word.replace("'", "")
        word = word.replace("}", "")
        word = word.replace("]", "")
        # print(word)
        templist.append(word)
    dic_keywords[id] = templist

file.close()

# print("-------------------------- --------------------------")
# # Seaching ID
# print(dic_keywords['17414'])

# print("-------------------------- --------------------------")

# -------------------------------------------------------------------------------------------------------



# print(dic_meta)
# dic_keywords
# dic_credits

# dic_meta[record["id"]] = {
#     "id" : id,
#     "title" : title,
#     "language" : language,
#     "overview" : overview,
#     "popularity" : popularity,
#     "release_date" : release_date,
#     "production_companies" : production_companies_list,
#     "genres" : genres_list
#     }

collection = {}
total_list = []
# print(dic_meta["813"])

number_of_records = 50

counter = 0
for idx, each_key in enumerate(dic_meta):
    if counter == number_of_records:
        break 
    # print(each_key)
    # print(dic_keywords[each_key])
    try:
        dic_keywords[each_key]
        dic_credits[each_key]
    except:
        continue

    # Dict ---------------

    # temp_dic = {}
    # genres_list = []
    # metadata = dic_meta[each_key]
    # metadata = metadata["genres"]
    # # print(metadata["genres"])

    # for idx, genra in enumerate(metadata):
    #     # print(type(genra))
    #     # print(genra[0])
    #     temp_dic = {}
    #     key = "genre" + str(idx + 1)
    #     temp_dic[key] = genra[0]
    #     genres_list.append(temp_dic)

    # List ---------------

    genres_list = []
    metadata = dic_meta[each_key]
    metadata = metadata["genres"]
    # print(metadata["genres"])

    for genra in metadata:
        genres_list.append(genra[0])




    # print(metadata["genres"])

    # Dict ---------------

    # temp_dic = {}
    # keyword_list = []
    # keywords = dic_keywords[each_key]
    # for idx, word in enumerate(keywords):
    #     # print(word)
    #     temp_dic = {}
    #     key = "keyword" + str(idx + 1)
    #     # dic_temp2[key] = word
    #     temp_dic[key] = word
    #     keyword_list.append(temp_dic)


    # List ---------------
    keywords = dic_keywords[each_key]

    keyword_list = []
    for word in keywords:
        keyword_list.append(word)

    temp_dic = {}
    actors_list = []

      # Dict ---------------
    # CAST
    # {ID, { <character>, <name> }}
    temp_dic = {}
    cast_list = []
    casts = dic_credits[each_key]
    for actor in casts:
        temp_dic = {}
        character = actor[0]
        key_actor = actor[1]
        temp_dic[key_actor] = character
        cast_list.append(temp_dic)

    # List -----------------



    # Production Company
    # {ID, { <character>, <name> }}
    meta_data = dic_meta[each_key]

    # Dict ---------------

    # temp_dic = {}
    # company_list = []
    # companies = meta_data["production_companies"]
    # for idx, company in enumerate(companies):
    #     key = "Company" + str(idx + 1)
    #     temp_dic = {}
    #     temp_dic[key] = company[0]
    #     company_list.append(temp_dic)

    # List ---------------
    company_list = []
    companies = meta_data["production_companies"]
    for company in companies:
        company_list.append(company[0])

    # print(dic_credits[each_key])


    # collection[each_key] = {
    #     "movie_id" : each_key,
    #     "title" : meta_data["title"],
    #     "language" : meta_data["language"],
    #     "overview" : meta_data["overview"],
    #     "popularity" : meta_data["popularity"],
    #     "release_date" : meta_data["release_date"],
    #     "production_companies" : company_list,
    #     "genres" : genres_list,
    #     "keywords" : keyword_list,
    #      "crew" : {
    #         "characters" : cast_list
    #     },
    #     "reviews" : [
    #     ]
    # }
    popularity_value = float(meta_data['popularity'])
    total_list.append (
        {
            # "movie_id" : each_key,
            "title" : meta_data["title"],
            "language" : meta_data["language"],
            "overview" : meta_data["overview"],
            "popularity" : popularity_value,
            "release_date" : meta_data["release_date"],
            "production_companies" : company_list,
            "genres" : genres_list,
            "keywords" : keyword_list,
            "characters" : cast_list,
            "reviews" : [ ]
        }
    )
    counter += 1

# print(collection["862"])
# total_list = []
# for key in collection:
#     obj = collection[key]
#     total_list.append({obj})

# print(total_list)

print("Start Writing To File")
# with open('result.json', 'w') as fp:
    # json.dump(collection, fp)
    # json.dump(total_list, fp)

fout = open('result.json', 'w')
fout.write(json.dumps(total_list))
fout.close()

print("Finished Writing To File")

print("----------------------- DONE ------------------------")


# https://www.tutorialspoint.com/add-a-key-value-pair-to-dictionary-in-python