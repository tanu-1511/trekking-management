from flask import Blueprint, render_template

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/dashboard")
def dashboard():
    return render_template("user/dashboard.html")