from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

def construct_chat_blueprint(ROOMS):
    chatRoute = Blueprint(
        "chat", __name__, static_folder="static", template_folder="templates"
    )

    # chat route
    @chatRoute.route("/chat", methods=["GET", "POST"])
    def chat():
        if not current_user.is_authenticated:
            flash("Please login", "danger")
            return redirect(url_for("login.login"))
        return render_template("chat.html", username=current_user.username, rooms=ROOMS)

    return chatRoute
