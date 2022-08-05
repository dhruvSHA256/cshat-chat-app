from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user
from passlib.hash import bcrypt_sha256

from utils.wtform_fields import RegistrationForm, User


def construct_home_blueprint(db):
    homeRoute = Blueprint(
        "/", __name__, static_folder="static", template_folder="templates"
    )

    @homeRoute.route("/home", methods=["GET", "POST"])
    @homeRoute.route("/", methods=["GET", "POST"])
    def home():
        # redirect user to chat page if already login
        if current_user.is_authenticated:
            return redirect(url_for("chat.chat"))
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
            return redirect(url_for("login.login"))

        return render_template("index.html", form=reg_form)

    return homeRoute
