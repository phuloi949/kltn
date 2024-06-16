from functools import wraps
import jwt
from flask import request
from database.model import User
from web_base.colored_print import print_colored
from web_base.text_art import art_authenticated
import os
from dotenv import load_dotenv
load_dotenv()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
            current_user=User().get_by_id(data["user_id"])
            if current_user is None:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
            print_colored(art_authenticated , "green")   
            print_colored(f"Identity: {current_user['username']}", "yellow")
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500
        
        return f(current_user, *args, **kwargs)

    return decorated