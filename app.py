import os

from flask import Flask, flash, redirect, render_template, url_for
from flask_login import LoginManager, current_user, login_user, logout_user
from passlib.hash import bcrypt_sha256

from models import SQLAlchemy, User
from wtform_fields import LoginForm, RegistrationForm

# config flask app
app = Flask(__name__)
app.secret_key = "replace later"

# config postgres db
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_URL"].replace(
    "postgres", "postgresql"
)
db = SQLAlchemy(app)


# config flask-login for session management
login_manager = LoginManager(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


# main route
@app.route("/", methods=["GET", "POST"])
def index():
    reg_form = RegistrationForm()

    # if POST is used and form is validated
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        hashed_password = bcrypt_sha256.hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Registered Successfully. Please Login", "success")
        return redirect(url_for("login"))

    return render_template("index.html", form=reg_form)


# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    # if POST is used and login successful
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for("chat"))

    return render_template("login.html", form=login_form)


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if not current_user.is_authenticated:
        flash("Please login", "danger")
        return redirect(url_for("login"))
    return "in chat"


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return "Logged out"


if __name__ == "__main__":
    app.run(debug=True)
