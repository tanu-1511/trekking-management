from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/register")
def choose_register():
    return render_template("choose_register.html")


@auth.route("/register/trekker")
def register_trekker():
    return render_template("register_trekker.html")


@auth.route("/register/staff")
def register_staff():
    return render_template("register_staff.html")