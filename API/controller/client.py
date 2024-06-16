from database.model import Client
import jwt
from flask import request
import os
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
    client_id = data.get('client_id')
    client_ip = data.get('client_ip')
    client_status = data.get('client_status')
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

