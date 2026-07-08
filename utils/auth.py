from functools import wraps
from flask import session, redirect, url_for, flash
from models.user import User
from config import db


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Access denied.", "danger")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper


def staff_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        user = db.session.get(User, session["user_id"])

        if (
            user is None
            or user.role != "staff"
            or user.approval_status != "Approved"
        ):
            session.clear()
            flash("Your account has been blocked by the administrator.", "danger")
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return wrapper


def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        user = db.session.get(User, session["user_id"])

        if (
            user is None
            or user.role != "user"
            or user.approval_status == "Blacklisted"
        ):
            session.clear()
            flash(
                "Your account has been blacklisted by the administrator.",
                "danger"
            )
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return wrapper