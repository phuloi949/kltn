import bson, os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_URI='mongodb://root:example@mongodb:27017/'
DATABASE_NAME = 'my-database'
USER_COLLECTION = "users"
CLIENT_COLLECTION = "clients"
_mongodb = MongoClient(DATABASE_URI)[DATABASE_NAME]
userdb = _mongodb[USER_COLLECTION]
clientdb = _mongodb[CLIENT_COLLECTION]
x=0

class User:
    """User Model"""
    def __init__(self):
        return

    def create(self, username="", password=""):
        """Create a new user"""
        
        data = {
                "username": username,
                "password": generate_password_hash(password)
            }
        new_user = userdb.insert_one(data)
        print(new_user)
        return self.get_by_id(new_user.inserted_id), 200
    
    def get_by_id(self, user_id):
        """Get a user by id"""
        user = userdb.find_one({"_id": bson.ObjectId(user_id)})
        if not user:
            return
        user["_id"] = str(user["_id"])
        user.pop("password")
        return user
    
    def get_by_username(self, username):
        """Get a user by email"""
        user = userdb.find_one({"username": username})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user
    
    def login(self, username, password):
        """Login a user"""
        user = self.get_by_username(username)
        if not user or not check_password_hash(user["password"], password):
            return "Unauthorize", 401
        user.pop("password")
        return user