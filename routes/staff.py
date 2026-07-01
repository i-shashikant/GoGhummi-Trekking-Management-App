from flask import Blueprint, render_template, request, redirect, url_for, session
from config import db
from models.trek import Trek
from models.booking import Booking

staff_bp = Blueprint("staff", __name__)

@staff_bp.route("/staff")
def staff_dashboard():

    staff_id = session["user_id"]

    treks = Trek.query.filter_by(
        assigned_staff_id=staff_id
    ).all()

    return render_template(
        "staff_dashboard.html",
        treks=treks
    )

@staff_bp.route("/staff/update/<int:trek_id>", methods=["GET", "POST"])
def update_trek_staff(trek_id):

    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return "Trek not found"
    
    if request.method == "POST":

        trek.available_slots = int(request.form.get("available_slots"))

        trek.status = request.form.get("status")

        db.session.commit()

        return redirect(url_for("staff.staff_dashboard"))
    
    return render_template(
    "update_trek_staff.html",
    trek=trek
    )

@staff_bp.route("/staff/participants/<int:trek_id>")
def staff_participants(trek_id):

    bookings = Booking.query.filter_by(
        trek_id=trek_id
    ).all()

    return render_template(
        "staff_participants.html",
        bookings=bookings
    )