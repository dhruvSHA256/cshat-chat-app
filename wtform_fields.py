from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Length, EqualTo
from models import User


def validate_creds(form, field):
    # custom validator for unique username
    user_object = User.query.filter_by(username=form.username.data).first()

    if not user_object:
        raise ValidationError("Username or password incorrect")

    elif user_object.password != field.data:
        raise ValidationError("Username or password incorrect")


class LoginForm(FlaskForm):
    username = StringField(
        "username_label",
        validators=[InputRequired(message="Username Required"), ],
    )
    password = PasswordField(
        "password_label",
        validators=[InputRequired(
            message="Password Required"), validate_creds],
    )
    submit_button = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField(
        "username",
        validators=[
            InputRequired(message="Username Required"),
            Length(
                min=4, max=10,
                message="Username must between 4 and 10 characters long"
            ),
        ],
    )
    password = PasswordField(
        "password",
        validators=[
            InputRequired(message="Password Required"),
            Length(
                min=8, max=25,
                message="Password must between 8 and 25 characters long"
            ),
        ],
    )
    cnfrm_password = PasswordField(
        "cnfrm_password",
        validators=[
            InputRequired(message="Username Required"),
            EqualTo("password", "Passwords are not same"),
        ],
    )
    submit_button = SubmitField("Create")

    def validate_username(self, username):
        # custom validator for unique username
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists")
