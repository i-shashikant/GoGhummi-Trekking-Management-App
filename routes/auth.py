from flask import Blueprint, render_template, redirect, url_for, request, session
from models.user import User
from config import db



auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:

            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role

            if user.role == "admin":
                return redirect(url_for("admin.admin_dashboard"))

            elif user.role == "staff":

                if user.approval_status == "Pending":
                    return "Waiting for admin approval."

                return redirect(url_for("staff.staff_dashboard"))

            else:
                return redirect(url_for("user.user_dashboard"))

        return "Invalid username or password"

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return render_template("register.html", error="Username already exists")
        
        if role == "staff":
            approval_status = "Pending"
        else:
            approval_status = "Approved"

        new_user = User(username=username, email=email, password=password, role=role, approval_status=approval_status)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html")
