from flask import Blueprint, render_template
from flask_login import current_user

from models.trek import Trek

staff = Blueprint("staff", __name__, url_prefix="/staff")


@staff.route("/dashboard")
def dashboard():

    treks = Trek.query.filter_by(
        assigned_staff_id=current_user.id
    ).all()

    return render_template(
        "staff/dashboard.html",
        treks=treks
    )