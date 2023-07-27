# This script is being used to pull information out of each json file and create a single one.

import json
import re

# {ID, [ < keywords > ]}

# ---------------------------------------- Keywords ------------------------------------------------

regex_p = re.compile("'name': ([^:]+(?=,|$))")

# Read in data from json file.
file = open('./Processed/keywords.json', 'r')

data = json.load(file)

dic = {}

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
    dic[id] = templist

file.close()

print("-------------------------- --------------------------")
# Seaching ID
print(dic['17414'])

print("-------------------------- --------------------------")

# -------------------------------------------------------------------------------------------------------