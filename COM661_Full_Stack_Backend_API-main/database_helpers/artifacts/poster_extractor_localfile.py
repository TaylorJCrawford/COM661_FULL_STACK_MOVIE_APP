# Get posters for each of the movies stored in dataset.

# http://omdbapi.com/
# http://www.omdbapi.com/?i=tt3896198&apikey=PLACEHOLDER
# http://www.omdbapi.com/?t=%22toy%20story%22&apikey=PLACEHOLDER

from pymongo import MongoClient
import requests
import json

# Convert Popularity Fields in collection to type float.
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.com661_cw
movies_collection = db.movies

counter = 0
for item in movies_collection.find():
    movie_title = item["title"]
    print(f"Counter= {counter}, Title= {movie_title}")

    image_url = "http://www.omdbapi.com/?t="+ movie_title +"&apikey=PLACEHOLDER"

    file_name = movie_title
    file_name = 'posters/'+  file_name.replace(' ', '_') + '.png'

    my_bytes_value = requests.get(image_url).content
    json_value = json.loads(my_bytes_value)
    try:
        img_data = requests.get(json_value['Poster']).content
    except:
        continue

    with open(file_name, 'wb') as handler:
        handler.write(img_data)
    counter += 1

    movies_collection.update_one(
        {'title':movie_title},
        { "$set": {"poster": file_name} },
        False,
        True
    )