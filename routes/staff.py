from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import db
from models.trek import Trek
from models.user import User
from models.booking import Booking
from utils.auth import staff_required

staff_bp = Blueprint("staff", __name__)

@staff_bp.route("/dashboard")
@staff_required
def dashboard():

    user = db.session.get(User, session["user_id"])

    assigned_treks = Trek.query.filter_by(
        assigned_staff_id=session["user_id"]
    ).order_by(Trek.start_date).all()

    assigned_count = len(assigned_treks)

    open_count = sum(
        1 for trek in assigned_treks
        if trek.status == "Open"
    )

    booking_count = Booking.query.join(Trek).filter(
        Trek.assigned_staff_id == session["user_id"]
    ).count()

    return render_template(
        "staff/dashboard.html",
        user=user,
        assigned_treks=assigned_treks,
        assigned_count=assigned_count,
        open_count=open_count,
        booking_count=booking_count
    )


@staff_bp.route("/treks")
@staff_required
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
@staff_required
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
@staff_required
def update_trek(trek_id):

    trek = db.session.get(Trek, trek_id)

    new_capacity = int(request.form["max_slots"])

    booked = Booking.query.filter_by(
        trek_id=trek.id
    ).count()

    if new_capacity < booked:
        flash(
            f"Capacity cannot be less than {booked} because users are already booked.",
            "danger"
        )
        return redirect(url_for("staff.manage_trek", trek_id=trek.id))
    
    trek.status = request.form["status"]
    trek.max_slots = new_capacity
    trek.available_slots = new_capacity - booked

    db.session.commit()
    
    flash("Trek details updated successfully.", "success")
    return redirect(url_for("staff.dashboard"))

@staff_bp.route("/manage/<int:trek_id>")
@staff_required
def manage_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    bookings = Booking.query.filter_by(
        trek_id=trek.id
    ).all()

    return render_template(
        "staff/manage_trek.html",
        trek=trek,
        bookings=bookings
    )