from flask import Flask
from web_base._flask import FlaskAppWrapper
from dotenv import load_dotenv
import os
load_dotenv()

flask_app = Flask(__name__)
app = FlaskAppWrapper(flask_app)
# app = FlaskAppWrapper(flask_app, [("SECRET_KEY", f"{SECRET_KEY}")])

# Controller declaration
from controller.hello_world import hello_world
from controller.user import add_user, login


# Add route
app.add_endpoint('/hello', 'hello', hello_world)
app.add_endpoint('/add_user', 'add_user', add_user, ["POST"])
app.add_endpoint('/login', 'login', login, ["POST"])


if __name__ == "__main__":
    app.run(debug=True)