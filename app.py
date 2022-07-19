from flask import Flask, redirect, render_template, url_for
from models import User, SQLAlchemy
from wtform_fields import RegistrationForm, LoginForm
import os

# config flask app
app = Flask(__name__)
app.secret_key = "replace later"

# config postgres db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL'].replace(
    "postgres", "postgresql")
db = SQLAlchemy(app)


# main route
@app.route("/", methods=["GET", "POST"])
def index():
    reg_form = RegistrationForm()

    # if POST is used and form is validated
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)


# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    # if POST is used and login successful
    if login_form.validate_on_submit():
        return "logged in"

    return render_template("login.html", form=login_form)


if __name__ == "__main__":
    app.run(debug=True)
