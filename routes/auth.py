from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user
from models.user import User
from extensions import db, bcrypt
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            if user.blacklisted:
                flash("Your account has been blacklisted. Please contact support.", "danger")
                return render_template("login.html")
            if not user.approved:
                flash("Your account is awaiting approval. Please wait for admin approval.", "warning")
                return render_template("login.html")
            login_user(user)
            flash("Logged in successfully!", "success")
            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))
            elif user.role == "staff":
                return redirect(url_for("staff.dashboard"))
            else:
                return redirect(url_for("user.dashboard"))
        else:
            flash("Invalid email or password.", "danger")
    return render_template("login.html")


@auth.route("/register")
def choose_register():
    return render_template("choose_register.html")


@auth.route("/register/trekker", methods=["GET", "POST"])
def register_trekker():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with this email already exists.", "danger")
            return render_template("register_trekker.html")

        hashed_password= bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(
            name=name,
            email=email,
            phone=phone,
            password=hashed_password,
            role="user",
            approved=True,
            blacklisted=False
        )
        db.session.add(new_user)
        db.session.commit()
        return render_template(
            "registration_success.html",
            message="Your trekker account has been created. You can now log in."
        )
    return render_template("register_trekker.html")


@auth.route("/register/staff", methods=["GET", "POST"])
def register_staff():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_staff = User(
            name=name,
            email=email,
            phone=phone,
            password=hashed_password,
            role="staff",
            approved=False,
            blacklisted=False
        )

        db.session.add(new_staff)
        db.session.commit()

        return render_template(
            "registration_success.html",
            message="Your staff account has been created and is awaiting admin approval."
        )

    return render_template("register_staff.html")

admin = Blueprint("admin", __name__, url_prefix="/admin")
@admin.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")

staff = Blueprint("staff", __name__, url_prefix="/staff")
@staff.route("/dashboard")
def dashboard():
    return render_template("staff/dashboard.html")

user = Blueprint("user", __name__, url_prefix="/user")
@user.route("/dashboard")
def dashboard():
    return render_template("user/dashboard.html")