from web_base.colored_print import print_colored
from controller.token import load_token
import os

# def client_install():
    
#     print_colored("client_install", "green")
#     return {"status": "Successfully"}

def client_train():
    print_colored("client_train", "green")
    if not os.path.exists("CLIENT/resource/_flower"):
        print("Failed!")
        return {"status": "Havent setup the environment"}
    os.system("conda run -n fl_env python CLIENT/resource/_flower/main_client.py")
    return {"status": "Successfully"}