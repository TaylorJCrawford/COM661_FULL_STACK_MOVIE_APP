from pymongo import MongoClient
from flask import Flask, request, jsonify, make_response, send_file
from bson import ObjectId
class WatchlistClass():

    def __init__(self) -> None:
        self.watchlist_collection = self.connect_to_db_helper()

    def connect_to_db_helper(self) -> object:
        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client.com661_cw
        return db.watchlist

    def get_movies_for_user(self, user_id):
        result_list = []

        for x in self.watchlist_collection.find({'user_id' : user_id}):
            result_list.append(x['watchlist'])

        return make_response( result_list, 200)

    def add_movie(self, title, user_id):
        new_watchlist = {
            'title': title
        }

        result = self.watchlist_collection.update_one({'user_id' : user_id}, { '$push' : { 'watchlist' : new_watchlist }}, upsert=True)

        if result.modified_count == 1:
            return make_response( {"Complete" : "New Movie Added To Watchlist"}, 200)
        return make_response( {"Error" : "Could not add movie at this time."}, 500)

    def remove_movie(self, title, user_id):
        result = self.watchlist_collection.update_one({'user_id' : user_id}, { '$pull' : {'watchlist' : {'title' : title}}})

        if result.modified_count == 1:
            return make_response( {"Complete" : "Movie has been remove from watchlist."}, 200)
        return make_response( {"Error" : "Could not remove movie at this time."}, 500)

    def delete_user_watchlist(self, user_id):

        result = self.watchlist_collection.delete_one({'user_id' : user_id})
        if result.deleted_count == 1:
            return True
        return False
