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
    # fin = open(FILEPATH, 'r')
    # result = send_file(fin, as_attachment=True)
    # print(result)
    # return result
####
    # FILEPATH = f'/home/ubuntu/kltn/SERVER/resources/zip_file/flower-homomorphic_encryption.zip'
    # fileobj = io.BytesIO()
    # with zipfile.ZipFile(fileobj, 'w') as zip_file:
    #     zip_info = zipfile.ZipInfo(FILEPATH)
    #     zip_info.date_time = time.localtime(time.time())[:6]
    #     zip_info.compress_type = zipfile.ZIP_DEFLATED
    #     with open(FILEPATH, 'rb') as fd:
    #         zip_file.writestr(zip_info, fd.read())
    # fileobj.seek(0)

    # # Changed line below
    # return Response(fileobj.getvalue(),
    #                 mimetype='application/zip',
    #                 headers={'Content-Disposition': 'attachment;filename=your_filename.zip'})
    
    
@token_required
def sh_file(_user):
    FILEPATH = '/home/ubuntu/kltn/SERVER/resources/scripts/install.sh'
    
    return send_file(FILEPATH, 
                     mimetype='application/x-sh'
                    )