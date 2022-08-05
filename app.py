import os
import time

from flask import Flask, flash, redirect, render_template, url_for
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_socketio import SocketIO, join_room, leave_room, send
from passlib.hash import bcrypt_sha256

from models.User import SQLAlchemy, User
from routes.Chat import construct_chat_blueprint
from routes.Home import construct_home_blueprint
from routes.Login import loginRoute
from routes.Logout import logoutRoute

# from utils.wtform_fields import RegistrationForm

# config flask app
app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

# config postgres db
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_URL"].replace(
    "postgres", "postgresql"
)
db = SQLAlchemy(app)

# config flask-socketio
socketio = SocketIO(app)

# config flask-login for session management
login_manager = LoginManager(app)
login_manager.init_app(app)


# room list
ROOMS = ["lounge", "news", "games", "coding"]


@app.errorhandler(404)
def page_not_found(_):
    return render_template("404.html"), 404


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


# logout route
app.register_blueprint(logoutRoute, url_prefix="")

# login route
app.register_blueprint(loginRoute, url_prefix="")

# chat route
app.register_blueprint(construct_chat_blueprint(ROOMS), url_prefix="")

# home route
app.register_blueprint(construct_home_blueprint(db), url_prefix="")


# message event
@socketio.on("message")
def message(data):
    msg = data["msg"]
    username = data["username"]
    room = data["room"]
    time_stamp = time.strftime("%b-%d %I:%M%p", time.localtime())
    send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)


# user joined the room
@socketio.on("join")
def on_join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)
    send({"msg": username + " has joined the " + room + " room."}, room=room)


# user left the room
@socketio.on("leave")
def on_leave(data):
    username = data["username"]
    room = data["room"]
    leave_room(room)
    send({"msg": username + " has left the room"}, room=room)


if __name__ == "__main__":
    if os.environ["LOCAL"]:
        # if running locally
        socketio.run(app, debug=True)
    else:
        # if running on heroku
        app.run()
