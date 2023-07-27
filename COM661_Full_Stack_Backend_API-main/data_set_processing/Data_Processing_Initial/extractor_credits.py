import json
import re

# CAST
# {ID, { <character>, <name> }}

file = open('./Processed/credits.json', 'r')

regex_p_name = re.compile("'name': ([^:]+(?=,|$))")
regex_p_character = re.compile("'character': ([^:]+(?=,|$))")

data = json.load(file)

dic = {}

def breakdown_map(name, character, result):
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
    breakdown_map(templist_cast_name, templist_cast_char, outcome)

    dic[id] = outcome

print(dic["862"]) # Toy Story


