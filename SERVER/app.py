from flask import Flask
from web_base._flask import FlaskAppWrapper
from dotenv import load_dotenv
import os,json
from bson.objectid import ObjectId
load_dotenv()

flask_app = Flask(__name__)

# Json Encoder
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super(JSONEncoder, self).default(o)
flask_app.json_encoder = JSONEncoder
app = FlaskAppWrapper(flask_app)


# Controller declaration
from controller.hello_world import hello_world
from controller.user import add_user, login
from controller.client import add_client, delete_client, get_total_client, client_login
from controller.fl_server import start_train
from controller.response import zip_file


# Add route
app.add_endpoint('/hello', 'hello', hello_world) # This test need login -> pass Authorized key to headers ->  call
app.add_endpoint('/total_client', 'total_client', get_total_client) #
app.add_endpoint('/start_train', 'start_train', start_train, ["POST"])
app.add_endpoint('/add_user', 'add_user', add_user, ["POST"])
app.add_endpoint('/login', 'login', login, ["POST"])
app.add_endpoint('/add_client', 'add_client', add_client, ["POST"])
app.add_endpoint('/delete_client', 'delete_client', delete_client, ["POST"])
app.add_endpoint('/client_login', 'client_login', client_login, ["POST"])
app.add_endpoint('/zip_file', 'zip_file', zip_file)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv('PORT'))
    