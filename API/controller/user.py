from database.model import User
import jwt
from flask import request
import os
from dotenv import load_dotenv
load_dotenv()


def add_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    return User().create(username, password)

def login():
    data = request.json
    if not data:
        return {
            "message": "Please provide user details",
            "data": None,
            "error": "Bad request"
        }, 400
    username = data.get('username')
    password = data.get('password')
    user = User().login(username,password)
    if user:
        try:
            print(os.getenv('SECRET_KEY'))
            user["token"] = jwt.encode(
                {"user_id": user["_id"]},
                os.getenv('SECRET_KEY'),
                algorithm="HS256"
            )
            print(user)
            
            return {
                "message": "Successfully fetched auth token",
                "data": user,
                "script": "python -m or sth"
            }
        except Exception as e:
            print(f"Something went wrong: {e}")
            return {
                "error": "Something went wrong",
                "message": str(e)
            }, 500
    return {
            "message": "Error fetching auth token!, invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }, 404