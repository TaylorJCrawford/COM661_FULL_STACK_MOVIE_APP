from pymongo import MongoClient
from flask import Flask, request, jsonify, make_response, send_file
from bson import ObjectId

class UserClass():

    def __init__(self) -> None:
        self.users_collection = self.connect_to_db_helper('users')
        self.blacklist_collection = self.connect_to_db_helper('blacklist')
        self.watchlist_collection = self.connect_to_db_helper('watchlist')
        pass

    def connect_to_db_helper(self, collection) -> object:

        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client.com661_cw
        if collection == 'users':
            return db.users
        elif collection == 'blacklist':
            return db.blacklist
        elif collection == 'watchlist':
            return db.watchlist

    def get_all_user(self):

        result_list = []
        result_collection = self.users_collection.find()
        for x in result_collection:
            x['_id'] = str(x['_id'])
            result_list.append(x)

        return result_list

    def add_new_user(self, new_user):

        result = self.users_collection.insert_one(new_user)
        return result

    def remove_user_account(self, user_id):

        result = self.users_collection.delete_one({'_id' : ObjectId(user_id)})
        if result.deleted_count == 1:
            return make_response( {"Complete" : "Account Has Been Delete."}, 200)
        return make_response( {"Error" : "Could not remove account at this time."}, 500)

    def set_admin_role(self, user_id, admin):

        result = self.users_collection.update_one(
            {
                '_id' : ObjectId(user_id)
            },
            {
                '$set' : {
                    'admin' : eval(admin)
                }
            }
        )

        if result.matched_count == 1:
            return make_response( {"Complete" : "User Role Has Been Updated."}, 200)
        return make_response( {"Error" : "Could not update user role at this time."}, 500)


    def does_username_exist(self, username):
        result_collection = self.users_collection.find( { 'username' : username })

        results = []
        for x in result_collection:
            results.append(x)
            print(x)

        if (results != []):
            return make_response( {"Present" : "true"}, 200)
        return make_response( {"Present" : "false"}, 200)