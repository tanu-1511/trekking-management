from flask import Blueprint, render_template, request
from models.user import User
from extensions import db, bcrypt
auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
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
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(
            name=name,
            email=email,
            phone=phone,
            password=hashed_password,
            role="trekker",
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