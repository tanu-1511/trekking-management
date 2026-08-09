from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

from models.trek import Trek
from models.booking import Booking
from extensions import db

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/dashboard")
def dashboard():
    return render_template("user/dashboard.html")


@user.route("/treks")
def view_treks():

    treks = Trek.query.filter_by(status="Open").all()

    return render_template(
        "user/treks.html",
        treks=treks
    )


@user.route("/treks/book/<int:trek_id>", methods=["POST"])
def book_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    # Check whether slots are available
    if trek.available_slots <= 0:
        flash("Sorry, this trek is fully booked.", "danger")
        return redirect(url_for("user.view_treks"))

    # Check if this user already booked this trek
    existing_booking = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=trek.id,
        status="Booked"
    ).first()

    if existing_booking:
        flash("You have already booked this trek.", "warning")
        return redirect(url_for("user.view_treks"))

    # Create booking
    booking = Booking(
        user_id=current_user.id,
        trek_id=trek.id
    )

    # Reduce available slots
    trek.available_slots -= 1

    db.session.add(booking)
    db.session.commit()

    flash("Trek booked successfully!", "success")

    return redirect(url_for("user.view_treks"))

@user.route("/bookings")
def my_bookings():

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "user/bookings.html",
        bookings=bookings
    )