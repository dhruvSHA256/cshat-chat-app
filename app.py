from flask import Flask, render_template
from models import User, SQLAlchemy
from wtform_fields import RegistrationForm
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

    # if form is validated
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "inserted into db"

    return render_template("index.html", form=reg_form)


if __name__ == "__main__":
    app.run(debug=True)
