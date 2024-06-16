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

from controller.hello_world import hello

# app.add_endpoint('/hello', 'hello', hello)
app.add_endpoint('/', 'hello', hello)

if __name__ == "__main__":
    app.run(debug=True)
    