import requests
from flask import request
from controller.token import save_data, load_token
from web_base.colored_print import print_colored
# POST
def login_client():
    print_colored("[3]------[login_client]-------", "cyan")
    data = request.json
    cred = {
        "username": data.get('username'),
        "password": data.get('password')
    }
    print_colored(str(request.remote_addr), "green")
    print_colored(str(cred), "green")
    
    ip = request.remote_addr
    print(f"[4] Direct ---> {ip}")
    res = requests.post(f"http://{ip}:5000/login", json=cred)
    print(f"[6] response returned!")
    res = res.json()
    save_data(res)
    return {"status": "Succesfully"}