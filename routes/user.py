from flask import Blueprint, render_template, session, redirect, url_for, request, flash, render_template, session
from models.trek import Trek
from models.booking import Booking
from models.user import User
from datetime import date
from config import db
from utils.auth import user_required
from werkzeug.security import generate_password_hash


user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/")
@user_required
def dashboard():

    user = db.session.get(User, session["user_id"])
    open_treks = (
        Trek.query
        .filter_by(status="Open")
        .order_by(Trek.start_date)
        .limit(6)
        .all()
    )

    my_bookings = (
        Booking.query
        .filter_by(user_id=user.id)
        .order_by(Booking.booking_date.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "user/dashboard.html",
        user=user,
        open_treks=open_treks,
        my_bookings=my_bookings
    )

@user_bp.route("/profile", methods=["GET", "POST"])
@user_required
def profile():

    user = db.session.get(User, session["user_id"])

    if request.method == "POST":

        email = request.form.get("email")
        phone = request.form.get("phone")
        new_password = request.form.get("new_password")

        existing_email = User.query.filter(
            User.email == email,
            User.id != user.id
        ).first()
        if existing_email:
            flash("Email already exists.", "danger")
            return redirect(url_for("user.profile"))

        existing_phone = User.query.filter(
            User.phone == phone,
            User.id != user.id
        ).first()

        if existing_phone:
            flash("Phone number already exists.", "danger")
            return redirect(url_for("user.profile"))

        user.email = email
        user.phone = phone

        if new_password:
            user.password = generate_password_hash(new_password)

        db.session.commit()

        flash("Profile updated successfully.", "success")

        return redirect(url_for("user.profile"))

    total_bookings = Booking.query.filter_by(
        user_id=user.id
    ).count()

    return render_template(
        "user/profile.html",
        user=user,
        total_bookings=total_bookings
    )

@user_bp.route("/treks")
@user_required
def browse_treks():

    q = request.args.get("q", "").strip()
    difficulty = request.args.get("difficulty", "")
    location = request.args.get("location", "").strip()

    query = Trek.query.filter_by(status="Open")

    if q:
        query = query.filter(
            Trek.trek_name.ilike(f"%{q}%")
        )

    if difficulty:
        query = query.filter_by(
            difficulty=difficulty
        )

    if location:
        query = query.filter(
            Trek.location.ilike(f"%{location}%")
        )

    treks = Trek.query.order_by(Trek.start_date).all()

    return render_template(
        "user/browse_treks.html",
        treks=treks,
        q=q,
        difficulty=difficulty,
        location=location
    )

@user_bp.route("/treks/<int:trek_id>")
@user_required
def trek_detail(trek_id):

    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return "Trek not found", 404

    already_booked = Booking.query.filter_by(
        user_id=session["user_id"],
        trek_id=trek.id,
        status="Booked"
    ).first()

    return render_template(
        "user/trek_detail.html",
        trek=trek,
        already_booked=already_booked
    )

@user_bp.route("/book/<int:trek_id>", methods=["POST"])
@user_required
def book_trek(trek_id):

    user = db.session.get(User, session["user_id"])
    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return "Trek not found", 404

    # Already booked?
    existing = Booking.query.filter_by(
        user_id=user.id,
        trek_id=trek.id,
        status="Booked"
    ).first()

    if existing:
        flash("You have already booked this trek.", "warning")
        return redirect(url_for("user.trek_detail", trek_id=trek.id))

    # Trek must be open
    if trek.status != "Open":
        flash("This trek is not open for booking.", "danger")
        return redirect(url_for("user.trek_detail", trek_id=trek.id))

    # Slots available?
    if trek.available_slots <= 0:
        flash("No slots available for this trek.", "danger")
        return redirect(url_for("user.trek_detail", trek_id=trek.id))

    booking = Booking(
        user_id=user.id,
        trek_id=trek.id,
        booking_date=date.today(),
        status="Booked"
    )

    trek.available_slots -= 1

    db.session.add(booking)
    db.session.commit()
    flash("Trek booked successfully!", "success")
    return redirect(url_for("user.my_bookings"))

@user_bp.route("/bookings")
@user_required
def my_bookings():

    bookings = (
        Booking.query
        .filter_by(user_id=session["user_id"])
        .order_by(Booking.booking_date.desc())
        .all()
    )

    return render_template(
        "user/bookings.html",
        bookings=bookings
    )

@user_bp.route("/cancel/<int:booking_id>", methods=["POST"])
@user_required
def cancel_booking(booking_id):

    booking = db.session.get(Booking, booking_id)

    if booking is None:
        return "Booking not found", 404

    # Don't cancel twice
    if booking.status == "Cancelled":
        return redirect(url_for("user.my_bookings"))

    trek = booking.trek

    booking.status = "Cancelled"

    # Restore one slot
    trek.available_slots += 1

    db.session.commit()
    flash("Booking cancelled successfully.", "info")
    return redirect(url_for("user.my_bookings"))
