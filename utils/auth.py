from functools import wraps
from flask import session, redirect, url_for, flash


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
        if session.get("role") != "staff":
            flash("Access denied.", "danger")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper


def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("role") != "user":
            flash("Access denied.", "danger")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper