from bson.objectid import ObjectId
from pymongo import MongoClient
from colorama import Fore, Style, init
import jwt, os
import json
from werkzeug.security import generate_password_hash, check_password_hash
from web_base.colored_print import print_colored
from dotenv import load_dotenv
load_dotenv()

"""
This is for colorfull loging
"""
# init(autoreset=True)

# def print_colored(text, color):
#     """
#     Print text in a specified color.

#     :param text: The text to print.
#     :type text: str
#     :param color: The color to print the text in.
#     :type color: str
#     """
#     color_dict = {
#         'red': Fore.RED,
#         'green': Fore.GREEN,
#         'yellow': Fore.YELLOW,
#         'blue': Fore.BLUE,
#         'magenta': Fore.MAGENTA,
#         'cyan': Fore.CYAN,
#         'white': Fore.WHITE
#     }
#     print(color_dict.get(color.lower(), Fore.WHITE) + text)
    
    
MONGODB_CREDENTIAL = "" if os.getenv('MONGODB_CREDENTIAL')=="@" else os.getenv('MONGODB_CREDENTIAL')
DATABASE_URI=f"mongodb://{MONGODB_CREDENTIAL}{os.getenv('MONGODB_HOST')}:27017/"
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
        user = userdb.find_one({"_id": ObjectId(user_id)})
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
    
    
class Client():
    def __init__(self):
        return
    
    def create(self, client_id="", client_ip="", client_status="", model="", _id=""):
        """Create a new user"""
        _token = jwt.encode(
                {"client_ip": client_ip},
                os.getenv('SECRET_KEY_IP'),
                algorithm="HS256"
            )
        data = {
                "client_id": client_id,
                "client_ip": client_ip,
                "client_status": client_status,
                "model": model,
                "token": _token,
                "creator": _id
            }
        new_client = clientdb.insert_one(data)
        print_colored(f"[ Done create client! ]: {new_client}", "cyan")
        return self.get_by_id(new_client.inserted_id)
    
    def delete_by_id(self, id):
        """Delete a client by its ID"""
        result = clientdb.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return {"message": "Client deleted successfully"}, 200
        else:
            return {"message": "Client not found"}, 404
        
    def delete_by_client_id(self, client_id):
        """Delete a client by its client_ID"""
        result = clientdb.delete_one({"client_id": client_id})
        if result.deleted_count > 0:
            
            return {"message": "Client deleted successfully"}, 200
        else:
            return {"message": "Client not found"}, 404
    
    def update_token(self, creator_id, new_token):
        """Update the token of all clients created by a specific creator"""
        print('This is update token')
        result = clientdb.update_many(
            {"creator": creator_id},
            {"$set": {"token": new_token}}
        )
        if result.matched_count > 0:
            print("this id match")
            return {"message": f"Token updated for {result.matched_count} clients"}, 200
        else:
            print("this id err")
            return {"message": "No clients found for the specified creator"}, 404
    
    def get_by_id(self, id):
        """Get a client by its ID"""
        client = clientdb.find_one({"_id": ObjectId(id)})
        client["_id"] = str(client["_id"])
        if client:
            return client
        else:
            return None
        
    def get_id_by_client_id(self, client_id):
        """Get a client by its ID"""
        client = clientdb.find_one({"client_id": client_id})
        _id = str(client["_id"])
        if client:
            return _id
        else:
            return None
        
    def get_ip_by_client_id(self, client_id):
        """Get a client by its ID"""
        client = clientdb.find_one({"client_id": client_id})
        ip = (client["client_ip"])
        if client:
            return ip
        else:
            return None
        
    def get_by_ip(self, ip):
        """Get a client by its ID"""
        
        client = clientdb.find_one({"client_ip": ip})
        if client:
            return str(client["_id"])
        else:
            return None
    
    def count_client(self, user_id):
        return str(clientdb.count_documents({"creator": user_id}))

         
    
# Example test

# print("----------TEST ADD CLIENT -------------")
# jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjY2ZDk0Y2NhNjY2NTYxZThlZGY3MzAxIn0.KCzs2hl0MGow_qRo0TYnMnTIbwxvHPxcmbYymvNBfS8"
# __id = "666d9238465e5dedef9661d5"
# x = Client().create(
#     client_id="client123",
#     client_ip="192.168.123.222",
#     client_status="offline",
#     model="CNN",
#     _id = __id
# )
# print(x)

# data=jwt.decode(token, os.getenv('SECRET_KEY_IP'), algorithms=["HS256"])
#     if(data["client_ip"] != ip):
#         return False

# _jwt_token = "___eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjY2ZDk0Y2NhNjY2NTYxZThlZGY3MzAxIn0.KCzs2hl0MGow_qRo0TYnMnTIbwxvHPxcmbYymvNBfS8"
# x = Client().update_token(
#     creator_id=__id,
#     new_token=_jwt_token
# )

# print(x)

# Client().delete_by_id("666e4f9943f4ca2f7c8bf417")