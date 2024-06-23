from flask import Response, send_file
import os
from dotenv import load_dotenv
from database.auth_middleware import token_required
from web_base.colored_print import print_colored
load_dotenv()
import io
import zipfile
import time

@token_required
def zip_file(_user):
    FILEPATH = f'/home/ubuntu/kltn/SERVER/resources/zip_file/flower-homomorphic_encryption.zip'
    
    return send_file(FILEPATH, 
                     mimetype='application/zip'
                    )
    
    
@token_required
def sh_file(_user):
    FILEPATH = '/home/ubuntu/kltn/SERVER/resources/scripts/install.sh'
    
    return send_file(FILEPATH, 
                     mimetype='application/x-sh'
                    )