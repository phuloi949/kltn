from flask import request
import requests
import os
from dotenv import load_dotenv
from database.auth_middleware import token_required
from web_base.colored_print import print_colored
load_dotenv()


@token_required
def start_train(_current_user):
    data = request.json
    print_colored(str(data), "yellow")
    if(not data):
        return {
            "message": "No data received"
        }
    # server_train_command = ". script/activate && conda run -n myenv python main_train.py"
    # os.system(server_train_command)
    client_ip = data.get('client_ip')
    # **
    try:
        res = requests.get(f"http://{client_ip}:5000/client_install")
        if (res.json()["status"] != "Successfully"):
            return {"status": "Install dependencies failed"}
        print_colored("Done install", "green")
        res = requests.get(f"http://{client_ip}:5000/client_train")
        if (res.json()["status"] != "Successfully"):
            return {"status": "Train proccess failed"}
        print_colored("Start training process succesfully", "green")
        return {"message": "Train process successfully!"}
    except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500
    