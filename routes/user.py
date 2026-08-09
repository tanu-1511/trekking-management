from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    current_user,
    login_required
)

from routes.auth import role_required

from models.trek import Trek
from models.booking import Booking

from extensions import db


user = Blueprint(
    "user",
    __name__,
    url_prefix="/user"
)


# =========================
# USER DASHBOARD
# =========================

@user.route("/dashboard")
@login_required
@role_required("user")
def dashboard():

    return render_template(
        "user/dashboard.html"
    )


# =========================
# VIEW / SEARCH / FILTER TREKS
# =========================

@user.route("/treks")
@login_required
@role_required("user")
def view_treks():

    search = request.args.get(
        "q",
        ""
    ).strip()

    difficulty = request.args.get(
        "difficulty",
        ""
    ).strip()

    location = request.args.get(
        "location",
        ""
    ).strip()

    query = Trek.query.filter_by(
        status="Open"
    )

    if search:

        query = query.filter(
            Trek.name.ilike(
                f"%{search}%"
            )
        )

    if difficulty:

        query = query.filter(
            Trek.difficulty == difficulty
        )

    if location:

        query = query.filter(
            Trek.location.ilike(
                f"%{location}%"
            )
        )

    treks = query.all()

    return render_template(
        "user/treks.html",
        treks=treks,
        search=search,
        difficulty=difficulty,
        location=location
    )


# =========================
# BOOK TREK
# =========================

@user.route(
    "/treks/book/<int:trek_id>",
    methods=["POST"]
)
@login_required
@role_required("user")
def book_trek(trek_id):

    trek = Trek.query.get_or_404(
        trek_id
    )

    # Only open treks can be booked
    if trek.status != "Open":

        flash(
            "This trek is not currently open for booking.",
            "danger"
        )

        return redirect(
            url_for("user.view_treks")
        )

    # Check available slots
    if trek.available_slots <= 0:

        flash(
            "Sorry, this trek is fully booked.",
            "danger"
        )

        return redirect(
            url_for("user.view_treks")
        )

    # Prevent duplicate booking
    existing_booking = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=trek.id,
        status="Booked"
    ).first()

    if existing_booking:

        flash(
            "You have already booked this trek.",
            "warning"
        )

        return redirect(
            url_for("user.view_treks")
        )

    booking = Booking(
        user_id=current_user.id,
        trek_id=trek.id
    )

    trek.available_slots -= 1

    db.session.add(
        booking
    )

    db.session.commit()

    flash(
        "Trek booked successfully!",
        "success"
    )

    return redirect(
        url_for("user.view_treks")
    )


# =========================
# MY BOOKINGS
# =========================

@user.route("/bookings")
@login_required
@role_required("user")
def my_bookings():

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    booking_data = []

    for booking in bookings:

        trek = Trek.query.get(
            booking.trek_id
        )

        if trek:

            booking_data.append({
                "booking": booking,
                "trek": trek
            })

    return render_template(
        "user/bookings.html",
        booking_data=booking_data
    )


# =========================
# USER PROFILE
# =========================

@user.route(
    "/profile",
    methods=["GET", "POST"]
)
@login_required
@role_required("user")
def profile():

    if request.method == "POST":

        current_user.name = request.form.get(
            "name"
        )

        current_user.email = request.form.get(
            "email"
        )

        current_user.phone = request.form.get(
            "phone"
        )

        db.session.commit()

        flash(
            "Profile updated successfully!",
            "success"
        )

        return redirect(
            url_for("user.profile")
        )

    return render_template(
        "user/profile.html",
        user=current_user
    )