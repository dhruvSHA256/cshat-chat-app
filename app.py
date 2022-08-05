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

# main route
# @app.route("/", methods=["GET", "POST"])
# def index():
#     reg_form = RegistrationForm()

#     # if POST is used and form is validated
#     if reg_form.validate_on_submit():
#         username = reg_form.username.data
#         password = reg_form.password.data
#         hashed_password = bcrypt_sha256.hash(password)
#         user = User(username=username, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()

#         flash("Registered Successfully. Please Login", "success")
#         return redirect(url_for("login"))

#     return render_template("index.html", form=reg_form)


# login route
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     login_form = LoginForm()

#     # if POST is used and login successful
#     if login_form.validate_on_submit():
#         user_object = User.query.filter_by(username=login_form.username.data).first()
#         login_user(user_object)
#         return redirect(url_for("chat.chat"))

#     return render_template("login.html", form=login_form)


# chat route
# @app.route("/chat", methods=["GET", "POST"])
# def chat():
#     if not current_user.is_authenticated:
#         flash("Please login", "danger")
#         return redirect(url_for("login"))
#     return render_template("chat.html", username=current_user.username, rooms=ROOMS)


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
