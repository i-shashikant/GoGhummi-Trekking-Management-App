from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from config import db



auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        role = session.get("role")

        if role == "admin":
            return redirect(url_for("admin.dashboard"))
        elif role == "staff":
            return redirect(url_for("staff.dashboard"))
        else:
            return redirect(url_for("user.dashboard"))
        
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            if user.approval_status == "Blacklisted":
                flash("Your account has been blacklisted. Please contact the administrator.", "danger")
                return redirect(url_for("auth.login"))

            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role

            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))

            elif user.role == "staff":

                if user.approval_status == "Pending":
                    flash("Your staff account is pending admin approval.", "warning")
                    return redirect(url_for("auth.login"))

                flash("Login Successful.", "success")
                return redirect(url_for("staff.dashboard"))

            else:
                flash("Login Successful.", "success")
                return redirect(url_for("user.dashboard"))

        flash("Invalid username or password.", "danger")
        return redirect(url_for("auth.login"))

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if "user_id" in session:
        role = session.get("role")

        if role == "admin":
            return redirect(url_for("admin.dashboard"))
        elif role == "staff":
            return redirect(url_for("staff.dashboard"))
        else:
            return redirect(url_for("user.dashboard"))
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password=generate_password_hash(request.form["password"])
        role = request.form.get("role")
        phone = request.form.get("phone")

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Username already exists.", "danger")
            return redirect(url_for("auth.register"))

        if existing_email:
            flash("Email already exists.", "danger")
            return redirect(url_for("auth.register"))
        existing_phone = User.query.filter_by(phone=phone).first()

        if existing_phone:
            flash("Phone number already exists.", "danger")
            return redirect(url_for("auth.register"))

        if role == "staff":
            approval_status = "Pending"
        else:
            approval_status = "Approved"

        new_user = User(username=username, email=email, phone=phone, password=password, role=role, approval_status=approval_status)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "info")

    return redirect(url_for("auth.login"))

@auth_bp.route("/")
def index():
    return render_template("index.html")
