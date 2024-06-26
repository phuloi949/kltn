from database.model import Client
import jwt
from flask import request
import os
import requests
from dotenv import load_dotenv
from database.auth_middleware import token_required
from database.auth_ip import ip_token_validate
from web_base.colored_print import print_colored
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
    client_status = "Added!"
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
    print_colored("------[delete_client]-------", "cyan")
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
    print_colored("------[get_total_client]-------", "cyan")
    return  Client().count_client(str(_current_user["_id"]))

@token_required
def client_login(_current_user):
    print_colored("[1]------[client_login]-------", "cyan")
    data = request.json
    client_ip = data.get('client_ip')
    cred = {
        "username": data.get('username'),
        "password": data.get('password')
    }
    print_colored(str(cred), "green")
    print_colored(str(client_ip), "green")
    print(f"[2] Direct ---> {client_ip}")
    res = requests.post(f"http://{client_ip}:5000/login_client", json=cred)
    # res = res.json()
    print("[7] --- Token have been sent !")
    print(str(res.json()))
    update = Client().update_client_status(_current_user["_id"])
    print(str(update))
    print("[8] --- Return to app")
    return res.json()