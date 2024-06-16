from functools import wraps
import jwt
from flask import request
# from database.model import User
import os
from dotenv import load_dotenv
load_dotenv()


def ip_token_validate(token, ip):
    data=jwt.decode(token, os.getenv('SECRET_KEY_IP'), algorithms=["HS256"])
    if(data["client_ip"] != ip):
        return False
    return True


# TEST EXAMPLE
# _token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaXAiOiIxOTIuMTY4LjE2OC4yMiJ9.9_Evllgr6uSXO6K-R50CgebWxItgWdT9ohi4yKTnoLs"
# data=jwt.decode(_token, os.getenv('SECRET_KEY_IP'), algorithms=["HS256"])
# print(data["client_ip"])

# print(ip_token_validate(_token, "192.168.168.22"))
