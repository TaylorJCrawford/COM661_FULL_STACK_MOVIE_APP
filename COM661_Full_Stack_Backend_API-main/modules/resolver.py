from flask import Flask, jsonify, make_response, send_file
from pymongo import MongoClient
from bson import ObjectId
import datetime
import re

"""
    This file holders common functions to connect & query the database
"""

SERVER_URL = "http://localhost:5000"

class MyResolver:

    def __init__(self):
        self.movie_collection = self.connect_to_db_helper()


    def connect_to_db_helper(self) -> object:

        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client.com661_cw
        movies_collection = db.movies
        return movies_collection

    def check_db_helper(self):
        client = MongoClient("mongodb://127.0.0.1:27017")
        return client

    def check_field_types(self, fields :list, request) -> list:
        # Takes in dict that is: <key> : <data_type>

        invalid_fields = {}
        for key in fields:
            if key not in request.form:
                invalid_fields[key] = "The " + key + " field is required."

        return invalid_fields

    def check_for_presents_of_review_by_title(self, title, user_id):
        print('aggregate start')
        pipeline = [
            {
                "$match" : { 'title' : title},
            },
            {
                "$project" : { "reviews.user_id" : 1 , "reviews.comment" : 1, "reviews.overall" : 1},
            },
            {
                "$match" : { 'reviews.user_id' : user_id},
            }
        ]

        results = []
        for x in self.movie_collection.aggregate(pipeline):
            results.append(x)

        print(results)

        if results != []:
            # Comment found for user.
            return True
        else:
            # No result found.
            return False

    def get_user_reviews_by_user(self, user_id):

        result_list = []
        for x in self.movie_collection.find({'reviews.user_id' : user_id}):
            x['_id'] = str(x['_id'])
            result_list.append(x)

        return result_list

    def get_user_reviews_by_title(self, user_id, title):

        result_list = []
        for x in self.movie_collection.find( {'title' : title, 'reviews.user_id' : user_id}):
            x['_id'] = str(x['_id'])
            result_list.append(x)
        return result_list

    def get_id_movie_by_title(self, title):
        result = self.get_movie_meta_data_by_title_helper(title)

        if result != None:
            return result['_id']
        return []

    def get_movie_meta_data_by_title_helper(self, title):
        result = self.movie_collection.find_one( { 'title' : re.compile(title, re.IGNORECASE) })
        return result

    def get_list_of_movies_with_keywords_helper(self, keywords, operator):

        # $in
        # Has anyone of these keywords
            # db.movies.find( { 'keywords' : { $in : ['kgb', 'red army' ] } })

        # Has All KeyWords
            # db.movies.find( { 'keywords' : { $all : ['kgb', 'red army' ] } })

        result = self.movie_collection.find( { 'keywords' : { '$' + operator : keywords }})
        return result

    def check_date_value(self, date):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def get_list_of_movie_by_actor_name_helper(self, actor):

        result = self.movie_collection.find( {'characters.' + actor : { '$exists' : 'true' } } )
        return result

    def add_new_movie_helper(self, new_movie) -> str:
        movie_title = new_movie['title']
        self.movie_collection.insert_one(new_movie)
        result = SERVER_URL +'/api/v1.0/movie?title=' + movie_title
        return result

    def delete_movie_by_title_helper(self, title) -> bool:

        result = self.movie_collection.delete_one( { "title" : title })

        if result.deleted_count == 1:
            return True
        return False

    def update_movie_by_title_helper(self, title, new_fields :dict) -> str:

        result = self.movie_collection.update_one(
            {
                'title' : title
            },
            {
                '$set' : {
                    'title' : new_fields['title'],
                    'language' : new_fields['language'],
                    'overview' : new_fields['overview'],
                    'popularity' : new_fields['popularity'],
                    'release_date' : new_fields['release_date'],
                    'production_companies' : new_fields['production_companies'],
                    'genres' : new_fields['genres'],
                    'keywords' : new_fields['keywords'],
                    'characters' : new_fields['characters'],
                    'poster' : new_fields['poster']
                }
            }
        )

        if result.matched_count == 1:
            return SERVER_URL + '/api/v1.0/movie/' + new_fields['title']
        return ""

    def update_users_review_by_title_helper(self, title, new_review, movie_review_idex):

        movie_id = self.get_id_movie_by_title(title)

        result = self.movie_collection.update_one(
            {
                '_id' : ObjectId(movie_id),
                'reviews.user_id' : new_review['user_id']
            },
            {
                '$set' : {
                    'reviews.$.user_id' : new_review['user_id'],
                    'reviews.$.name' : new_review['name'],
                    'reviews.$.comment' : new_review['comment'],
                    'reviews.$.overview' : new_review['overview']
                }
            }
        )

        if result.matched_count == 1:
            return SERVER_URL + '/api/v1.0/movie/' + title
        return ""

    def moive_top_x_amount(self, amount=10):
        pipeline = [
            {
                "$sort" : { "popularity" : -1},
            },
            {
                "$limit" : amount,
            }
        ]

        return self.movie_collection.aggregate(pipeline)


    def movie_popularity_search_helper(self, amount = 10, operator = 'eq'):
        result = self.movie_collection.find( {'popularity': { '$' + operator : amount } } )
        if result != None:
            return result
        else:
            return None


    def movie_reviews_by_title_helper(self, title):
        result = self.get_movie_meta_data_by_title_helper(title)
        if result != None:
            return result['reviews']
        else:
            return None

    def remove_all_movie_reviews_by_title_helper(self, title):
        result = self.movie_collection.update_one({'title': title}, { "$set" : { "reviews" : "[]" }})

        if result.modified_count == 1:
            return True
        return False

    def add_new_movie_review_helper(self, title, new_review):

        result = self.movie_collection.update_one({'title': title}, { '$push' : { 'reviews' : new_review }})

        if result.modified_count == 1:
                return True
        return False

    def remove_user_review_by_title_helper(self, user_id, title):
        result = self.movie_collection.update_one({'title' : title}, { '$pull' : {'reviews' : {'user_id' : user_id}}})

        if result.modified_count == 1:
            return True
        return False