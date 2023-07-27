from pymongo import MongoClient
import bcrypt

# Credit: Moore, Adrian - aa.moore@ulster.ac.uk
# ** Code Modified to make use of new db. **

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.com661_cw      # select the database
users = db.users        # select the collection name


staff_list = [
          {
            "username" : "homer",
            "password" : b"homer_s",
            "email" : "homer@springfield.net",
            "admin" : False
          },
          {
            "username" : "marge",
            "password" : b"marge_s",
            "email" : "marge@springfield.net",
            "admin" : False
          },
          {
            "username" : "bart",
            "password" : b"bart_s",
            "email" : "bart@springfield.net",
            "admin" : False
          },
          {
            "username" : "lisa",
            "password" : b"lisa_s",
            "email" : "lisa@springfield.net",
            "admin" : True
          },
          {
            "username" : "maggie",
            "password" : b"maggie_s",
            "email" : "maggie@springfield.net",
            "admin" : False
          }
       ]

for new_staff_user in staff_list:
      new_staff_user["password"] = bcrypt.hashpw(new_staff_user["password"], bcrypt.gensalt())
      users.insert_one(new_staff_user)
