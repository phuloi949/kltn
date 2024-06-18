import requests
from flask import request
from controller.token import save_data
# POST
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    cred = {
        "username": username,
        "password": password
    }
    
    url = request.remote_addr
    res = requests.post(f"http://{url}:5000/login")
    res = res.json()
    save_data(res)
    return {"status": "Succesfully"}