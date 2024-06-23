import requests
from flask import request
from controller.token import save_data
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
    try:
        # This gonna change to script file because it gonna retrive script.sh for installation
        response = requests.get(f"http://{ip}:5000/zip_file", headers={
            'Authorization': str(res["data"]['token'])
        })
        response.raise_for_status()
        if response.headers['content-type'] == 'application/zip':
            filename = 'CLIENT/resource/flower-homomorphic_encryption.zip'
            with open(filename, 'wb') as f:
                f.write(response.content)
        
            print(f"ZIP file saved as: {filename}")
        else:
            print("Response content is not a ZIP file.")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    save_data(res)
    return {"status": "Succesfully"}