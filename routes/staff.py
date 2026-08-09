from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from flask_login import (
    current_user,
    login_required
)

from routes.auth import role_required

from models.trek import Trek
from models.booking import Booking
from models.user import User

from extensions import db


staff = Blueprint(
    "staff",
    __name__,
    url_prefix="/staff"
)


# =========================
# STAFF DASHBOARD
# =========================

@staff.route("/dashboard")
@login_required
@role_required("staff")
def dashboard():

    treks = Trek.query.filter_by(
        assigned_staff_id=current_user.id
    ).all()

    participant_counts = {}

    for trek in treks:

        participant_counts[trek.id] = (
            Booking.query.filter_by(
                trek_id=trek.id,
                status="Booked"
            ).count()
        )

    return render_template(
        "staff/dashboard.html",
        treks=treks,
        participant_counts=participant_counts
    )


# =========================
# VIEW PARTICIPANTS
# =========================

@staff.route(
    "/trek/<int:trek_id>/participants"
)
@login_required
@role_required("staff")
def participants(trek_id):

    trek = Trek.query.get_or_404(
        trek_id
    )

    if trek.assigned_staff_id != current_user.id:

        return "Unauthorized", 403

    bookings = Booking.query.filter_by(
        trek_id=trek.id,
        status="Booked"
    ).all()

    participants = []

    for booking in bookings:

        user = User.query.get(
            booking.user_id
        )

        if user:

            participants.append({
                "booking": booking,
                "user": user
            })

    return render_template(
        "staff/participants.html",
        trek=trek,
        participants=participants
    )


# =========================
# UPDATE ASSIGNED TREK
# =========================

@staff.route(
    "/trek/<int:trek_id>/edit",
    methods=["GET", "POST"]
)
@login_required
@role_required("staff")
def edit_trek(trek_id):

    trek = Trek.query.get_or_404(
        trek_id
    )

    if trek.assigned_staff_id != current_user.id:

        return "Unauthorized", 403

    if request.method == "POST":

        trek.available_slots = int(
            request.form.get(
                "available_slots"
            )
        )

        trek.status = request.form.get(
            "status"
        )

        db.session.commit()

        return redirect(
            url_for(
                "staff.dashboard"
            )
        )

    return render_template(
        "staff/edit_trek.html",
        trek=trek
    )