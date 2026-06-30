from flask import Blueprint, render_template, session, redirect, url_for
from models.trek import Trek
from models.booking import Booking
from datetime import date
from config import db

user_bp = Blueprint("user", __name__)

@user_bp.route("/user")
def user_dashboard():
    treks = Trek.query.filter_by(status="Open").all()
    return render_template("user_dashboard.html", treks=treks)

@user_bp.route("/book_trek/<int:trek_id>", methods=["GET"])
def book_trek(trek_id):
    user_id = session["user_id"]

    trek = db.session.get(Trek, trek_id)
    if not trek:
        return "Trek not found"
    if trek.available_slots <= 0:
        return "No available slots for this trek"
    
    existing_booking = Booking.query.filter_by(
        user_id=user_id,
        trek_id=trek_id
    ).first()

    if existing_booking:
        return "You have already booked this trek."

    booking = Booking(user_id=user_id, trek_id=trek.id, booking_date=date.today(), status="Booked")
    trek.available_slots -= 1
    db.session.add(booking)
    db.session.commit()

    return redirect(url_for("user.user_dashboard"))

@user_bp.route("/my_bookings")
def my_bookings():

    user_id = session["user_id"]

    bookings = Booking.query.filter_by(user_id=user_id).all()

    return render_template(
        "my_bookings.html",
        bookings=bookings
    )
