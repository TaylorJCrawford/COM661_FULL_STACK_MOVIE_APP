import datetime as dt
from pymongo import MongoClient

# Convert Popularity Fields in collection to type float.
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.com661_cw
movies_collection = db.movies

# movies = movies_collection.find()

# movies = movies_collection.find({ "popularity": { "$exists": True } })

counter = 0
for item in movies_collection.find({ "popularity": { "$exists": True } }):
    counter += 1
    pop = item["popularity"]
    # date = item["release_date"]
    # print(type(date))
    # d = dt.datetime.strptime(date,'%y--%m--%d')

    # Convert datetime object to date object.
    # d = d.date()

    # print(d.isoformat())
    # 1973-01-25

    movies_collection.update_one( { "movie_id" : item["movie_id"] } ,
        { "$set" : { "popularity" : float(pop) } } )

    # movies_collection.update_one( { "movie_id" : item["movie_id"] } ,
    #     { "$set" : { "popularity" : float(pop), "release_date": d.isoformat() } } )

# print(temp)
# print(temp['movie_id'])


