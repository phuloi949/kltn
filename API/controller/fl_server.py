from database.model import Client
import jwt
from flask import request
import os
from dotenv import load_dotenv
from database.auth_middleware import token_required
from database.auth_ip import ip_token_validate
load_dotenv()


@token_required
def trigger_fl_server_run(_current_user):
    data = request.json
    if(not data):
        return {
            "message": "No data received"
            }
    _command = f'''python main_server.py server 
                --data_path {data.get('data_path')} 
                --dataset {data.get('dataset')} 
                --seed {data.get('seed')} 
                --num_workers {data.get('num_workers')} 
                --max_epochs {data.get('max_epochs')} 
                --batch_size {data.get('batch_size')} 
                --length {data.get('length')} 
                --split {data.get('split')} 
                --device {data.get('device')} 
                --number_clients {data.get('number_clients')} 
                --min_fit_clients {data.get('min_fit_clients')} 
                --min_avail_clients {data.get('min_avail_clients')} 
                --min_eval_clients {data.get('min_eval_clients')} 
                --rounds {data.get('rounds')} 
                --frac_fit {data.get('frac_fit')} 
                --frac_eval {data.get('frac_eval')}'''
    os.system(_command)
    return {"message": "Command successfully!"}
    