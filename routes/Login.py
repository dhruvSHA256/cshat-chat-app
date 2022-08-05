from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_user

from models.User import User
from utils.wtform_fields import LoginForm

loginRoute = Blueprint(
    "login", __name__, static_folder="static", template_folder="templates"
)

# login route
@loginRoute.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    # if POST is used and login successful
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for("chat.chat"))

    return render_template("login.html", form=login_form)
