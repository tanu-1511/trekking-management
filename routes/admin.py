from flask import Blueprint, render_template, request, redirect, url_for

from models.trek import Trek
from models.user import User
from models.booking import Booking

from extensions import db

from datetime import datetime

from sqlalchemy import or_


admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# =========================
# ADMIN DASHBOARD
# =========================

@admin.route("/dashboard")
def dashboard():

    total_treks = Trek.query.count()

    total_users = User.query.filter_by(
        role="user"
    ).count()

    total_staff = User.query.filter_by(
        role="staff"
    ).count()

    total_bookings = Booking.query.count()

    return render_template(
        "admin/dashboard.html",
        total_treks=total_treks,
        total_users=total_users,
        total_staff=total_staff,
        total_bookings=total_bookings
    )


# =========================
# TREK MANAGEMENT
# =========================

@admin.route("/treks")
def manage_treks():

    search = request.args.get("q", "").strip()

    if search:

        if search.isdigit():

            treks = Trek.query.filter(
                or_(
                    Trek.id == int(search),
                    Trek.name.ilike(f"%{search}%")
                )
            ).all()

        else:

            treks = Trek.query.filter(
                Trek.name.ilike(f"%{search}%")
            ).all()

    else:

        treks = Trek.query.all()

    return render_template(
        "admin/treks.html",
        treks=treks,
        search=search
    )


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

        available_slots = int(
            request.form.get("available_slots")
        )

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

        return redirect(
            url_for("admin.manage_treks")
        )

    return render_template(
        "admin/create_trek.html"
    )


@admin.route(
    "/treks/edit/<int:trek_id>",
    methods=["GET", "POST"]
)
def edit_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    staff_members = User.query.filter_by(
        role="staff",
        approved=True
    ).all()

    if request.method == "POST":

        trek.name = request.form.get("name")

        trek.location = request.form.get(
            "location"
        )

        trek.difficulty = request.form.get(
            "difficulty"
        )

        trek.start_date = datetime.strptime(
            request.form.get("start_date"),
            "%Y-%m-%d"
        ).date()

        trek.end_date = datetime.strptime(
            request.form.get("end_date"),
            "%Y-%m-%d"
        ).date()

        trek.available_slots = int(
            request.form.get("available_slots")
        )

        trek.status = request.form.get(
            "status"
        )

        trek.description = request.form.get(
            "description"
        )

        assigned_staff_id = request.form.get(
            "assigned_staff_id"
        )

        if assigned_staff_id:

            trek.assigned_staff_id = int(
                assigned_staff_id
            )

        else:

            trek.assigned_staff_id = None

        db.session.commit()

        return redirect(
            url_for("admin.manage_treks")
        )

    return render_template(
        "admin/edit_trek.html",
        trek=trek,
        staff_members=staff_members
    )


@admin.route(
    "/treks/delete/<int:trek_id>",
    methods=["POST"]
)
def delete_trek(trek_id):

    trek = Trek.query.get_or_404(
        trek_id
    )

    db.session.delete(trek)
    db.session.commit()

    return redirect(
        url_for("admin.manage_treks")
    )


# =========================
# STAFF MANAGEMENT
# =========================

@admin.route("/staff")
def manage_staff():

    search = request.args.get(
        "q",
        ""
    ).strip()

    if search:

        if search.isdigit():

            staff_members = User.query.filter(
                User.role == "staff",
                or_(
                    User.id == int(search),
                    User.name.ilike(
                        f"%{search}%"
                    )
                )
            ).all()

        else:

            staff_members = User.query.filter(
                User.role == "staff",
                User.name.ilike(
                    f"%{search}%"
                )
            ).all()

    else:

        staff_members = User.query.filter_by(
            role="staff"
        ).all()

    return render_template(
        "admin/staff.html",
        staff_members=staff_members,
        search=search
    )


@admin.route(
    "/staff/approve/<int:staff_id>",
    methods=["POST"]
)
def approve_staff(staff_id):

    staff = User.query.get_or_404(
        staff_id
    )

    staff.approved = True

    db.session.commit()

    return redirect(
        url_for("admin.manage_staff")
    )


# =========================
# USER MANAGEMENT
# =========================

@admin.route("/users")
def manage_users():

    search = request.args.get(
        "q",
        ""
    ).strip()

    if search:

        if search.isdigit():

            users = User.query.filter(
                User.role == "user",
                or_(
                    User.id == int(search),
                    User.name.ilike(
                        f"%{search}%"
                    )
                )
            ).all()

        else:

            users = User.query.filter(
                User.role == "user",
                User.name.ilike(
                    f"%{search}%"
                )
            ).all()

    else:

        users = User.query.filter_by(
            role="user"
        ).all()

    return render_template(
        "admin/users.html",
        users=users,
        search=search
    )


@admin.route(
    "/users/blacklist/<int:user_id>",
    methods=["POST"]
)
def blacklist_user(user_id):

    user = User.query.get_or_404(
        user_id
    )

    user.blacklisted = True

    db.session.commit()

    return redirect(
        url_for("admin.manage_users")
    )


@admin.route(
    "/users/unblacklist/<int:user_id>",
    methods=["POST"]
)
def unblacklist_user(user_id):

    user = User.query.get_or_404(
        user_id
    )

    user.blacklisted = False

    db.session.commit()

    return redirect(
        url_for("admin.manage_users")
    )

@admin.route(
    "/staff/blacklist/<int:staff_id>",
    methods=["POST"]
)
def blacklist_staff(staff_id):

    staff = User.query.get_or_404(staff_id)

    staff.blacklisted = True

    db.session.commit()

    return redirect(
        url_for("admin.manage_staff")
    )


@admin.route(
    "/staff/unblacklist/<int:staff_id>",
    methods=["POST"]
)
def unblacklist_staff(staff_id):

    staff = User.query.get_or_404(staff_id)

    staff.blacklisted = False

    db.session.commit()

    return redirect(
        url_for("admin.manage_staff")
    )