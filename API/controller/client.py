from database.model import Client
import jwt
from flask import request
import os
import requests
from dotenv import load_dotenv
from database.auth_middleware import token_required
from database.auth_ip import ip_token_validate
load_dotenv()

@token_required
def add_client(_current_user):
    """
        Add client to db
    """
    data = request.json
    if(not data):
        return {
            "message": "No data received"
            }
    client_id = data.get('client_id')
    client_ip = data.get('client_ip')
    
    # request to client to check is online
    print(f"http://{client_ip}:5000/is_online")
    status = requests.get(f"http://{client_ip}:5000/is_online")
    print(status.json())
    client_status = True
    # if (status.json()['status'] != True):
        # client_status = False
    model = data.get('model')
    _id = str(_current_user["_id"])
    
    return Client().create(
        client_id=client_id,
        client_ip=client_ip,
        client_status=client_status,
        model=model,
        _id = _id
    )

@token_required
def delete_client(_current_user):
    data = request.json
    client_id = data.get('client_id')
    token = data.get('token')
    ip = Client().get_ip_by_client_id(client_id)
    if(not ip_token_validate(token, ip)):
        return {
            "message": "no ip match"
        }
    return Client().delete_by_client_id(client_id)

@token_required
def get_total_client(_current_user):
    return  Client().count_client(str(_current_user["_id"]))

@token_required
def client_login(_current_user):
    data = request.json
    client_ip = data.get('client_ip')
    username = data.get('username')
    password = data.get('password')
    print("Start to req")
    print(f"{client_ip}, {username}, {password}")
    res = requests.post(
        f"http://{client_ip}:5000/login",
        json = {
            "username": username,
            "password": password
        }
    )
    print("type of: ")
    print((res))
    print("-------")
    # res = res.json()
    if(res['status']!= "Succesfully"):
        return {'status': 'Failed'}
    return {'status': 'Successfully!'}