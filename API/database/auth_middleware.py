from functools import wraps
import jwt
from flask import request
from database.model import User
import os
from dotenv import load_dotenv
load_dotenv()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            print("------------------------")
            print(request.headers["Authorization"])
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
            print("-----current_user------")
            print(current_user)
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated