import json

def save_data(data):
    with open('/home/ubuntu/kltn/CLIENT/controller/tokens.json', 'w') as f:
        json.dump(data, f)

def load_token():
    try:
        with open('CLIENT/controller/tokens.json', 'r') as f:
            data = json.load(f)
            return data.get('token', 'Token not found!')
    except FileNotFoundError:
        return 'Token file not found!'
    
    
save_data("kk")