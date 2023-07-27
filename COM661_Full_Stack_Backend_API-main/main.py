from flask import Flask, request, jsonify, make_response, session
from flask_cors import CORS
from functools import wraps
import bcrypt
import jwt
import datetime

from modules.response_codes import CustomCodes
import modules.response_builder as builder
from modules.users import UserClass
from modules.resolver import MyResolver

# Data Set Link:
# https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?resource=download&select=credits.csv

############################################################
# App Setup
############################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
CORS(app)

VERSION_01_API = '/api/v1.0'
VERSION_02_API = '/api/v2.0'


############################################################
# Route Decorators
############################################################

def jwt_required(func):
    '''User Must have an account to access the content.'''
    @wraps(func)
    def jwt_required_wrapper(*args, **kwarges):
        users = UserClass()

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return make_response(jsonify({'message' : 'Token is invalid'}), 401)
        bl_token = users.blacklist_collection.find_one({"token":token})
        if bl_token is not None:
            return make_response(jsonify({'message': 'Token has been cancelled'}), 401)
        return func(*args, **kwarges)
    return jwt_required_wrapper

def admin_required(func):
    '''User account must be of admin rank.'''
    @wraps(func)
    def admin_required_wrapper(*args, **kwargs):
        token = request.headers['x-access-token']
        data = jwt.decode(token, app.config['SECRET_KEY'])
        if data['admin']:
            return func(*args, **kwargs)
        else:
            return make_response(jsonify({'message' : 'Admin access required'}), 401)
    return admin_required_wrapper

def check_for_author(id_of_post, token=None):

    token_value = decode_jwt_token(token)
    if token_value['_id'] == id_of_post:
        return True

    error = 'Author access required'
    message = 'Only the author of the content can make changes'
    return make_response(jsonify({'error' : error, 'message' : message}), 401)

def decode_jwt_token(token):
    return jwt.decode(token, "mysecret")

def check_for_author_or_admin(id_of_post, token):

    token_value = decode_jwt_token(token)

    if token_value['_id'] == id_of_post:
        return True
    elif token_value['admin'] == True:
        return True

    error = 'Author access required or Admin'
    message = 'Only the author or admin of the content can make changes'
    return make_response(jsonify({'error' : error, 'message' : message}), 401)

############################################################
# Start Of helper endpoints
############################################################

@app.route( VERSION_01_API + '/dataset_size', methods=['GET'])
def get_dataset_size():
    return builder.get_dataset_size_response_builder()

############################################################
# Start Of "/account" account management
############################################################

@app.route( VERSION_01_API + '/account/login', methods=['GET'])
def login():

    users = UserClass()
    response_helper = CustomCodes()
    print(request.form.keys())
    auth = request.authorization

    if auth:
        user = users.users_collection.find_one( {'username': auth.username })
        print("User Login: " + user['username'])
        if user is not None:
            if bcrypt.checkpw(bytes(auth.password, 'UTF-8'), user['password']):
                token = jwt.encode(
                    {
                        "_id" : str(user['_id']),
                        'user' : auth.username,
                        'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                        'admin' : user["admin"],
                    }, app.config['SECRET_KEY'] )
                return make_response(response_helper.valid_token(token.decode('UTF-8'), user["admin"], str(user['_id'])), 200)
            else:
                return make_response(response_helper.response_codes['Bad Password'], 401)
        else:
            return make_response(response_helper.response_codes['Bad Username'], 401)

    return make_response(response_helper.response_codes['Auth Required'], 401)

@app.route( VERSION_01_API + '/account/logout', methods=["GET"])
@jwt_required
def logout():
    users = UserClass()
    token = request.headers['x-access-token']
    users.blacklist_collection.insert_one({"token": token})
    return make_response(jsonify( {'message' : "Logout successful"}), 200)

@app.route( VERSION_01_API + '/account/register', methods=['POST'])
def register_user():
    return builder.add_new_standard_user_account_response_builder(request)

@app.route( VERSION_01_API + '/account/remove/<user_id>', methods=['DELETE'])
@jwt_required
def remove_account(user_id):
    result = check_for_author_or_admin(user_id, request.headers['x-access-token'])
    if result != True:
        return result
    return builder.remove_user_account_response_builder(user_id)

@app.route( VERSION_01_API + '/account', methods=['GET'])
@admin_required
def getUserAccounts():
    return builder.get_user_accounts()

@app.route( VERSION_01_API + '/account/role', methods=['POST'])
@admin_required
def update_admin_role():
    return builder.update_user_role(request)

@app.route( VERSION_01_API + '/checkUsername/<username>', methods=['GET'])
def check_for_username(username):
    users = UserClass()
    return users.does_username_exist(username)


############################################################
# Start Of "/movie" resources
############################################################

# -----------------------------------------|-----------------------------------------|
# GET /movie                               | # GET /movie?page=x&page_szie=x - User  |
# Receive a list of movies. - User         | # Receive a list of items per page.     |
# -----------------------------------------|-----------------------------------------|

@app.route( VERSION_01_API + '/movie', methods=['GET'])
def movie_home():

    # Request - Standard Movie Collection,
    page_num, page_size = 1,10
    # Checking for pagination data:
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    result = builder.pagination_response_builder(page_num, page_size)
    return result

# -----------------------------------------|
# POST  /movie - admin                     |
# Add a new movie to the collection.       |
# -----------------------------------------|

@app.route( VERSION_01_API + '/movie', methods=['POST'])
@jwt_required
@admin_required
def add_new_movie():
    return builder.add_new_movie_response_builder(request)


############################################################
# Start Of "/movie/title" resources
############################################################

# -----------------------------------------|
# GET /movie/<title>/poster                |
# Receive an image of the poster.          |
# -----------------------------------------|
@app.route( VERSION_01_API + '/movie/<title>/poster', methods=['GET'])
def get_movie_poster(title):
    return builder.poster_response_builder(title)


# -----------------------------------------|
# GET /movie/{title} - User                |
# Receive metadata for a specific movie.   |
# -----------------------------------------|

@app.route( VERSION_01_API + '/movie/<title>', methods=['GET'])
def recieve_movie_inform_by_title(title):
    return builder.meta_data_by_title_response_builder(title)


# -----------------------------------------|
# DELETE /movie/{title} - Admin            |
# Remove a movie by title.                 |
# -----------------------------------------|

@app.route( VERSION_01_API + '/movie/<title>', methods=['DELETE'])
@jwt_required
@admin_required
def remove_movie_by_title(title):
    return builder.delete_movie_by_title_response_builder(title)


# -----------------------------------------|
# PUT /movie/<title> - Admin               |
# Update data content of the moive         |
# (All fields missing fields will be       |
#   deleted / set to default)              |
# -----------------------------------------|

@app.route( VERSION_01_API + '/movie/<title>', methods=["PUT"])
@jwt_required
@admin_required
def full_update_movie_by_title(title):
    return builder.full_update_movie_by_title_response_builder(title, request)


# -----------------------------------------|
# PATCH /movie/<title> - Admin             |
# Update data content of the moive         |
# (Only fields specified)                  |
# -----------------------------------------|

@app.route( VERSION_01_API + '/movie/<title>', methods=["PATCH"])
@jwt_required
@admin_required
def partial_update_movie_by_title(title):
    return builder.partial_update_movie_by_title_response_builder(title, request)


############################################################
# Start Of "/movie/search" resources
############################################################

# -----------------------------------------|-----------------------------------------|
# GET /movie/search?keywords[] - User      | # GET /movie/search?actor=x - User      |
# Recieve a list of movies that match      | # Recieve a list of movies with the     |
# keywords.                                | # actor in it.                          |
#                                          |                                         |
#   criteria = Strict - $all               |                                         |
#            = Loose - $in                 |                                         |
# -----------------------------------------|-----------------------------------------|

@app.route( VERSION_01_API + '/movie/search', methods=['GET'])
def recieve_movies_inform_by_keywords():

    if request.args.get('actor'):
        actor = request.args.get('actor')
        return builder.receive_list_of_movie_by_actor(actor)
    elif request.args.get('keywords'):
        operator = 'in'
        keywords = request.args.get('keywords')
        if request.args.get('operator'):
            operator = request.args.get('operator')

        return builder.receive_a_list_of_movies_with_keywords_response_builder(keywords.split(','), operator)

    # Catch all - return error
    # mandatory parameters are missing, or that syntactically invalid parameter values have been detected
    return make_response( jsonify( { 'message' : 'Invalid Request', 'error' : 'No search criteria' } ), 400)


############################################################
# Start Of "/movie/popularity" resources
############################################################

# -----------------------------------------|----------------------------------------------------------------|
# GET /movie/popularity?amount=x - User    | # GET /movie/popularity?operator=x&amount=x - User             |
# Recieve a list of the most popular movies| # Recieve a list of moveis based on a values passed in.        |
# (Default 10). -> amount optional         | # operator_values = eq : equivalent, ne : not equivalentm      |
#                                          | # gt : greater than, lt : less than,                           |
#                                          | # gte : greater than or equal to, lte : less than or equal to  |
# -----------------------------------------|----------------------------------------------------------------|
@app.route( VERSION_01_API + '/movie/popularity', methods=['GET'])
def movie_popularity():
    return builder.movie_popularity_search_response_builder(request)


############################################################
# Start Of "/movie/reviews" resources
############################################################

# --------------------------------------------|
# GET /movie/reviews/<title> - User           |
# Receive all movie reviews for a given movie.|
# --------------------------------------------|
@app.route( VERSION_01_API + '/movie/reviews/<title>', methods=['GET'])
def movie_review(title):
    return builder.receive_movie_reviews_by_title_response_builder(title)


# ------------------------------------------|
# POST /movie/reviews/<user_id>/<title>     |
# User (Admin cannot update review for user)|
# Add a new review to a moive.              |
# Form comment=x&overall=x                  |
# ------------------------------------------|
@app.route( VERSION_01_API + '/movie/reviews/<title>/<user_id>', methods=['POST'])
@jwt_required
def add_new_user_review_to_movie(title, user_id):
    # print(request.headers['x-access-token'])
    result = check_for_author(user_id, request.headers['x-access-token'])
    if result != True:
        return result
    return builder.add_new_user_review_to_movie_response_builder(user_id, title, request)


# -------------------------------------------|
# PATCH /movie/reviews/<user_id>/<title>     |
# User (Admin cannont update review for user)|
# Update review comment or specific value.   |
# (Only update fields specified)             |
# -------------------------------------------|
@app.route( VERSION_01_API + '/movie/reviews/<title>/<user_id>', methods=['PATCH'])
@jwt_required
def partial_update_review_by_title(title, user_id):
    result = check_for_author(user_id, request.headers['x-access-token'])
    if result != True:
        return result
    return builder.partial_update_review_by_title_response_builder(user_id, title, request)


# ---------------------------------------------|
# DELETE /movie/reviews/<user_id>/<title>      |
# User (User can only delete there own review) |
# Delete the user's review for a given movie.  |
# ---------------------------------------------|
@app.route( VERSION_01_API + '/movie/reviews/<title>/<user_id>', methods=['DELETE'])
@jwt_required
def remove_user_review_from_movie(title, user_id):
    print("REMOVING COMMENT")
    result = check_for_author_or_admin(user_id, request.headers['x-access-token'])
    if result != True:
        return result
    return builder.delete_user_review_by_title_response_builder(user_id, title)


# --------------------------------------------|
# GET /movie/reviews/<user_id>/<title> - User |
# Get the user's review for a given movie.    |
# --------------------------------------------|
@app.route( VERSION_01_API + '/movie/reviews/<title>/<user_id>', methods=['GET'])
def receive_user_reviews_by_title(title, user_id):
    return builder.receive_user_movie_reviews_by_title_response_builder(user_id, title)


############################################################
# Start Of v2.0 "/movie/{user_id}" resources
############################################################

# --------------------------------------------|
# GET /movie/{user_id} - User Only            |
# Get watchlist information for user.         |
# --------------------------------------------|
@app.route( VERSION_02_API + '/movie/<user_id>', methods=['GET'])
@jwt_required
def get_watchlist_for_user(user_id):

    result = check_for_author_or_admin(user_id, request.headers['x-access-token'])
    if result != True:
        return result
    return builder.receive_watchlist_for_user_response_builder(user_id)

# --------------------------------------------|
# DELETE /movie/{title}/{user_id} - User Only |
# Remove movie from users watchlist.          |
# --------------------------------------------|
@app.route( VERSION_02_API + '/movie/<title>/<user_id>', methods=['DELETE'])
@jwt_required
def remove_movie_from_watchlist(title, user_id):

    result = check_for_author(user_id, request.headers['x-access-token'])
    if result != True:
        return result

    return builder.remove_movie_from_watchlist_response_builder(title, user_id)

# --------------------------------------------|
# POST /movie/{title}/{user_id} - User Only   |
# Add new movie to watchlist.                 |
# --------------------------------------------|
@app.route( VERSION_02_API + '/movie/<title>/<user_id>', methods=['POST'])
@jwt_required
def add_movie_to_watchlist(title, user_id):

    result = check_for_author(user_id, request.headers['x-access-token'])
    if result != True:
        return result

    return builder.add_movie_to_watchlist_response_builder(title, user_id)


if __name__ =='__main__':
    app.run(debug = True)
