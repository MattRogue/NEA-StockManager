from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from .client import Client
from .models import create_staff, check_staff
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)


@auth.route("/signup/", methods=["POST", "GET"])
@login_required
def signup():
    if request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")
        firstname = request.form.get("firstname").capitalize()
        surname = request.form.get("surname").capitalize()
        type = request.form.get("type").capitalize()
        user = create_staff(email, password, firstname, surname, type)
        if user:
            flash("Account created!", category="success")
        else:
            flash("Account creation failed!", category="failed")
        return redirect(url_for("auth.signup"))
    return render_template("signup.html", user=current_user)


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route('/login/', methods=["POST", "GET"])
def login():        
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = check_staff(email, password)
        if user:
            login_user(user, remember=False)
            session.permanent = True
            return redirect(url_for("views.home"))
        else:
            flash("Incorrect password or email", category="failed")
    return render_template("login.html", user=current_user)


@auth.route("/")
def index(): #Check if user is logged in then redirect=default
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    return redirect(url_for("auth.login"))
