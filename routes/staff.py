from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import db
from models.trek import Trek
from models.user import User
from models.booking import Booking

staff_bp = Blueprint("staff", __name__)

@staff_bp.route("/")
def dashboard():

    user = db.session.get(User, session["user_id"])

    assigned_treks = Trek.query.filter_by(
        assigned_staff_id=user.id
    ).order_by(
        Trek.start_date
    ).all()

    return render_template(
        "staff/dashboard.html",
        user=user,
        assigned_treks=assigned_treks
    )


@staff_bp.route("/treks")
def assigned_treks():

    user = db.session.get(User, session["user_id"])

    treks = Trek.query.filter_by(
        assigned_staff_id=user.id
    ).order_by(
        Trek.start_date
    ).all()

    return render_template(
        "staff/assigned_treks.html",
        treks=treks
    )

@staff_bp.route("/participants/<int:trek_id>")
def participants(trek_id):

    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return "Trek not found", 404

    return render_template(
        "staff/participants.html",
        trek=trek,
        bookings=trek.bookings
    )

@staff_bp.route("/update/<int:trek_id>", methods=["POST"])
def update_trek(trek_id):

    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return "Trek not found", 404

    trek.status = request.form["status"]

    db.session.commit()
    flash("Trek status updated successfully.", "success")
    return redirect(url_for("staff.dashboard"))