from flask import Blueprint, flash, redirect, url_for
from flask_login import logout_user

logoutRoute = Blueprint(
    "logout", __name__, static_folder="static", template_folder="templates"
)

# logout route
@logoutRoute.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("login.login"))
