from flask import Blueprint, render_template, request, redirect, url_for
from models.trek import Trek
from extensions import db
from datetime import datetime


admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")

@admin.route("/treks")
def manage_treks():
    treks = Trek.query.all()
    return render_template("admin/treks.html", treks=treks)  

@admin.route("/treks/create", methods=["GET", "POST"])
def create_trek():

    if request.method == "POST":

        name = request.form.get("name")
        location = request.form.get("location")
        difficulty = request.form.get("difficulty")
        start_date = datetime.strptime(
            request.form.get("start_date"),
            "%Y-%m-%d"
        ).date()
        end_date = datetime.strptime(
            request.form.get("end_date"),
            "%Y-%m-%d"
        ).date()
        available_slots = int(request.form.get("available_slots"))
        status = request.form.get("status")
        description = request.form.get("description")

        new_trek = Trek(
            name=name,
            location=location,
            difficulty=difficulty,
            start_date=start_date,
            end_date=end_date,
            available_slots=available_slots,
            status=status,
            description=description
        )

        db.session.add(new_trek)
        db.session.commit()

        return redirect(url_for("admin.manage_treks"))

    return render_template("admin/create_trek.html")

