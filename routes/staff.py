from flask import Blueprint, render_template

staff = Blueprint("staff", __name__, url_prefix="/staff")


@staff.route("/dashboard")
def dashboard():
    return render_template("staff/dashboard.html")