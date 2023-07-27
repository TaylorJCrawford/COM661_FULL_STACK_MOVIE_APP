from flask import jsonify, make_response, send_file, request
from pymongo import MongoClient
from bson import json_util
import json
from bson import ObjectId
import bcrypt

from .resolver import MyResolver
from .response_codes import CustomCodes
from modules.users import UserClass
from modules.watchlist import WatchlistClass
from datetime import datetime

"""
    This file holders functions to build responses.
    helper functions don't return a response object instead they are used as a common area to get information
    response_builder functions return a response object to the caller.
"""

def add_new_standard_user_account_response_builder(request):

    users = UserClass()
    code_helper = CustomCodes()
    database_helper = MyResolver()

    required_fields = [ 'username', 'password', 'email']

    # Check fields are present. & Are in the correct format
    missing_fields = database_helper.check_field_types(required_fields, request)

    if len(missing_fields) == 0:

        new_user = {
            'username' : request.form['username'],
            'password' : bcrypt.hashpw(bytes(request.form['password'], encoding='utf-8'), bcrypt.gensalt()),
            'email'    : request.form['email'],
            'admin'    : False
        }

        users.add_new_user(new_user)
        return make_response(jsonify( {'message' : "Register successful"}), 200)
    else:
        return make_response( code_helper.invalid_entity(missing_fields), 422)


def remove_user_account_response_builder(user_id):

    try:
        watchlist = WatchlistClass()
        watchlist.delete_user_watchlist(user_id)

        users = UserClass()
        return users.remove_user_account(user_id)
    except:
        return make_response( {"Error" : "Could not delete user at this time."}, 500)

def get_user_accounts():

    try:
        users = UserClass()
        results = users.get_all_user()
        return make_response(json.loads(json_util.dumps(results)),200)
    except:
        return make_response( {"Error" : "Could not get users at this time."}, 500)

def pagination_response_builder(page_num, page_size):

    # Starting Connection With DB
    movie_collection = MyResolver().movie_collection
    results = []

    # Calculate starting index
    page_start = page_size * (page_num - 1)

    # Search DB and return values
    result_collection = movie_collection.find().skip(page_start).limit(page_size)

    # Build response
    for movie in result_collection:
        movie['_id'] = str(movie['_id'])
        results.append(movie)

    return make_response( json.loads(json_util.dumps(results)),  200)


def poster_response_builder(title):

    # Starting Connection With DB
    database_helper = MyResolver()
    # Creating Common Response Code Object
    code_helper = CustomCodes()


    result = database_helper.get_movie_meta_data_by_title_helper(title)

    if result is not None:
        poster_path = result['poster']
        if 'http' in poster_path:
            return make_response(code_helper.result_poster(poster_path), 200)
        return make_response(send_file(poster_path, mimetype='image/png'), 200)
    else:
        return make_response(code_helper.response_codes['Invalid Title'], 404)


def meta_data_by_title_response_builder(title):

    # Starting Connection With DB
    database_helper = MyResolver()

    code_helper = CustomCodes()
    result = database_helper.get_movie_meta_data_by_title_helper(title)
    # Build Response
    if result is not None:
        result['_id'] = str(result['_id'])
        return make_response( jsonify([result]), 200)
    else:
        return make_response(code_helper.response_codes['Invalid Title'], 404)


def add_new_movie_response_builder(request):
    # Create a new resource

    #   Need to be able to upload image file for poster.
    database_helper = MyResolver()
    code_helper = CustomCodes()
    required_fields = [ 'title', 'language', 'overview', 'popularity',
        'release_date', 'production_companies', 'genres',
        'keywords', 'characters', 'poster', # 'reviews',
    ]

    # Check fields are present. & Are in the correct format
    missing_fields = database_helper.check_field_types(required_fields, request)

    if len(missing_fields) == 0:
        # All fields present - Add data to mongoDB
        review_value = []
        if 'review' in request.form:
            review_value = request.form['review']

        if database_helper.check_date_value(request.form['release_date']):
            new_movie = {
                'title' : request.form['title'], # String
                'language' : request.form['language'], # String
                'overview' : request.form['overview'], # String
                'popularity' : float(request.form['popularity']), # Integer
                'release_date' : request.form['release_date'], # String
                'production_companies' : request.form['production_companies'].split(','), # List
                'genres' : request.form['genres'].split(','), # List
                'keywords' : request.form['keywords'].split(','), # List
                'characters' : eval(request.form['characters']), # Dict (<Actor> <Part>) inside list
                'reviews' : review_value, # List of Dict (<user_id> : <value>, <comment> : <value>, <overall> : <value>)
                'poster' : request.form['poster'] # String
            }

            return make_response( jsonify({ "url": database_helper.add_new_movie_helper(new_movie)} ), 201)
        else:
            return make_response( code_helper.response_codes['Invalid Date Format'], 422)
    else:
        return make_response( code_helper.invalid_entity(missing_fields), 422)


def delete_movie_by_title_response_builder(title):
    database_helper = MyResolver()
    code_helper = CustomCodes()
    result = database_helper.delete_movie_by_title_helper(title)
    if result == True:
        return make_response(code_helper.response_codes['Movie Deleted'], 201)
    else:
        return make_response(code_helper.response_codes['Invalid Title'], 404)


def full_update_movie_by_title_response_builder(title, request):
    # Not allowed to update the review feild in the method! - Design decision
    # PUT = is used for resource updates (creates or replaces).

    database_helper = MyResolver()
    code_helper = CustomCodes()
    # Always need title.
    required_fields = [ 'title' ]

    # Check fields are present. & Are in the correct format
    missing_fields = database_helper.check_field_types(required_fields, request)

    if len(missing_fields) == 0:
        # All fields present - Add data to mongoDB

        if database_helper.check_date_value(request.form['release_date']) == False:
            return make_response( code_helper.response_codes['Invalid Date Format'], 422)


        characters_new = []

        if 'characters' in request.form:
            characters = request.form['characters'].split(',')
            for item in characters:
                temp = json.loads(item)
                characters_new.append(temp)

        updated_movie = {
            'title' : request.form['title'], # String
            'language' : request.form['language'] if 'language' in request.form else "", # String
            'overview' : request.form['overview'] if 'overview' in request.form else "", # String
            'popularity' : float(request.form['popularity']) if 'popularity' in request.form else 0, # Integer
            'release_date' : request.form['release_date'] if 'release_date' in request.form else "", # String
            'production_companies' : request.form['production_companies'].split(',') if 'production_companies' in request.form else "", # List
            'genres' : request.form['genres'].split(',') if 'genres' in request.form else [], # List
            'keywords' : request.form['keywords'].split(',') if 'keywords' in request.form else [], # List
            'characters' : characters_new,
            'poster' : request.form['poster'] if 'poster' in request.form else "" # String
        }

        result = database_helper.update_movie_by_title_helper(title, updated_movie)

        if result != "":
            return make_response( code_helper.result_url(result), 200)
        else:
            return make_response( code_helper.response_codes['Invalid Title'], 404)
    else:
        return make_response( code_helper.invalid_entity(missing_fields), 422)


def partial_update_movie_by_title_response_builder(title, request):

    # Get Existing Values.
    database_helper = MyResolver()
    code_helper = CustomCodes()
    movie = database_helper.get_movie_meta_data_by_title_helper(title)

    if movie is not None:

        characters_new = []

        if 'characters' in request.form:
            characters = request.form['characters'].split(',')
            for item in characters:
                temp = json.loads(item)
                characters_new.append(temp)

        updated_movie = {
                'title' : request.form['title'] if 'title' in request.form else movie['title'],
                'language' : request.form['language'] if 'language' in request.form else movie['language'],
                'overview' : request.form['overview'] if 'overview' in request.form else movie['overview'],
                'popularity' : float(request.form['popularity']) if 'popularity' in request.form else movie['popularity'],
                'release_date' : request.form['release_date'] if 'release_date' in request.form else movie['release_date'],
                'production_companies' : request.form['production_companies'].split(',') if 'production_companies' in request.form else movie['production_companies'],
                'genres' : request.form['genres'].split(',') if 'genres' in request.form else movie['genres'],
                'keywords' : request.form['keywords'].split(',') if 'keywords' in request.form else movie['keywords'],
                'characters' : characters_new,
                # 'characters' : eval(request.form['characters']) if 'characters' in request.form else movie['characters'],
                'poster' : request.form['poster'] if 'poster' in request.form else movie['poster'],
        }

        result = database_helper.update_movie_by_title_helper(title, updated_movie)

        if result != "":
            return make_response( code_helper.result_url(result), 200)
        else:
            return make_response( code_helper.response_codes['No Update'], 404)

    return make_response( code_helper.response_codes['Invalid Title'], 404)

def partial_update_review_by_title_response_builder(user_id, title, request):

    database_helper = MyResolver()

    # Get existing user review for movie by user_id. & chech the is fields to update.
    movie = database_helper.get_user_reviews_by_title(user_id, title)
    code_helper = CustomCodes()
    movie_review_index = None
    for index, value in enumerate(movie[0]['reviews']):
        if value['user_id'] == user_id:
            movie_review_index = index
            break

    updated_review = {
            'user_id' : user_id,
            'created' : movie[0]['reviews'][movie_review_index]['created'],
            'name' : request.form['name'] if 'name' in request.form else movie[0]['reviews'][movie_review_index]['name'],
            'comment' : request.form['comment'] if 'comment' in request.form else movie[0]['reviews'][movie_review_index]['comment'],
            'overview' : request.form['overview'] if 'overview' in request.form else movie[0]['reviews'][movie_review_index]['overview'],
    }

    result = database_helper.update_users_review_by_title_helper(title, updated_review, movie_review_index)

    if result != None:
        return make_response( code_helper.result_url(result), 200)
    else:
        return make_response( code_helper.response_codes['Invalid Title'], 404)

def movie_popularity_search_response_builder(request):

    # OPERATOR_LIST = ['eq', 'ne', 'gt', 'lt', 'gte', 'lte']
    amount = int(request.args.get('amount')) if 'amount' in request.args else None
    # operator = request.args.get('operator') if 'operator' in request.args else None
    database_helper = MyResolver()
    code_helper = CustomCodes()

    if amount != None:
        result = database_helper.moive_top_x_amount(amount)
    else:
        result = database_helper.moive_top_x_amount()

    results = []
    for movie in result:
        movie['_id'] = str(movie['_id'])
        results.append(movie)
    return make_response( jsonify(results), 200)


def receive_movie_reviews_by_title_response_builder(title):

    database_helper = MyResolver()
    code_helper = CustomCodes()
    results = database_helper.movie_reviews_by_title_helper(title)
    if results != None:
        return make_response( jsonify(results), 200)
    else:
        # Return error invalid title.
        return make_response( code_helper.response_codes['Invalid Title'], 404)

def delete_user_review_by_title_response_builder(user_id, title):

    database_helper = MyResolver()
    code_helper = CustomCodes()
    result = database_helper.remove_user_review_by_title_helper(user_id, title)
    if result == True:
        # Reviews have been deleted for that movie
        return make_response(code_helper.response_codes['Review Deleted'], 201)
    else:
        return make_response( code_helper.invalid_user(user_id, title), 404)

def add_new_user_review_to_movie_response_builder(user_id, title, request):

    # Check that users has not already got a review for this movie.

    database_helper = MyResolver()
    code_helper = CustomCodes()
    required_fields = [ 'comment', 'overall', 'name' ]

    # Check fields are present. & Are in the correct format
    missing_fields = database_helper.check_field_types(required_fields, request)

    if len(missing_fields) == 0:
        # Check that users has not already got a review for this movie.
        is_present_movie = database_helper.get_id_movie_by_title(title)
        if is_present_movie != []:
            is_present = database_helper.check_for_presents_of_review_by_title(title, user_id)
            if is_present == False:
                # Comment Not Found.
                new_review = {
                    'user_id' : user_id,
                    'name' : request.form['name'],
                    'comment' : request.form['comment'],
                    'overview' : int(request.form['overall']),
                    'created' : datetime.today().strftime('%Y-%m-%d')
                }

                database_helper.add_new_movie_review_helper(title, new_review)
                # Build review object and pass into resolver to add new comment

                new_review_link = "http://localhost:5000/api/v1.0/movie/" + title

                return make_response( code_helper.result_url(new_review_link, 'New Comment Has Been Added'), 201)
            else:
                # user has already left a comment.
                return make_response( code_helper.response_codes['Review Already Exists'], 403)
                # Return Error Response.
        return make_response( code_helper.response_codes['Invalid Title'], 404)
    else:
        return make_response( code_helper.invalid_entity(missing_fields), 422)

def receive_movie_reviews_by_user_id_response_builder(user_id):
    database_helper = MyResolver()
    code_helper = CustomCodes()
    result = database_helper.get_user_reviews_by_user(user_id)

    if result != None:
        return make_response( code_helper.result(result), 200)
    else:
        # No reviews found.
        return make_response( code_helper.response_codes['No Review'], 204)

def receive_user_movie_reviews_by_title_response_builder(user_id, title):

    database_helper = MyResolver()
    code_helper = CustomCodes()
    result = database_helper.get_user_reviews_by_title(user_id, title)
    print(result)
    if result != None:
        return make_response( code_helper.result(result), 200)
    else:
        # No reviews found.
        return make_response( code_helper.response_codes['No Review'], 204)

def receive_a_list_of_movies_with_keywords_response_builder(keywords : list, operator):

    ALLOW_OPERATORS = ['in', 'all']
    database_helper = MyResolver()
    code_helper = CustomCodes()

    if operator not in ALLOW_OPERATORS:
        return make_response( code_helper.response_codes['Invalid Operator'], 400)
    result = database_helper.get_list_of_movies_with_keywords_helper(keywords, operator)

    if result != None:
        results = []
        for movie in result:
            results.append(movie)

        return make_response( json.loads(json_util.dumps(results)),  200)
    else:
        # No reviews found.
        return make_response( code_helper.response_codes['No Keyword'], 204)

def receive_list_of_movie_by_actor(actor):

    database_helper = MyResolver()
    result = database_helper.get_list_of_movie_by_actor_name_helper(actor)
    results = []

    if result != None:
        for movie in result:
            results.append(movie)

        return make_response( json.loads(json_util.dumps(results)),  200)
    else:
        # No reviews found.
        return make_response( jsonify( { "message": "Actor has no movies stored" }), 204)

def add_movie_to_watchlist_response_builder(title, user_id):
    watchlist = WatchlistClass()
    return watchlist.add_movie(title, user_id)

def remove_movie_from_watchlist_response_builder(title, user_id):
    watchlist = WatchlistClass()
    return watchlist.remove_movie(title, user_id)

def receive_watchlist_for_user_response_builder(user_id):
    watchlist = WatchlistClass()
    return watchlist.get_movies_for_user(user_id)

def get_dataset_size_response_builder():

    try:
        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client.com661_cw
        find = {}

        result = db.movies.count_documents(find)
        return make_response( jsonify( {'result' : result} ), 200)
    except:
        return make_response( {"Error" : "Could not get size of dataset at this time."}, 500)

def update_user_role(request):

    users = UserClass()
    admin = request.form['admin'] if 'admin' in request.form else False
    user_id = request.form['user_id'] if 'user_id' in request.form else ""
    if (user_id == ""):
        return make_response(jsonify( {'message' : 'User ID Need To Be Present In Body.'} ), 404)
    return users.set_admin_role(user_id, admin)
