import requests
from flask import request
from controller.token import save_data, load_token
from web_base.colored_print import print_colored
# POST
def login_client():
    data = request.json
    cred = {
        "username": data.get('username'),
        "password": data.get('password')
    }
    print_colored(request.remote_addr, "green")
    print_colored(cred, "green")
    
    url = request.remote_addr
    res = requests.post(f"http://{url}:5000/login", json=cred)
    res = res.json()
    save_data(res)
    return {"status": "Succesfully"}