from flask import Blueprint, render_template, request, redirect, url_for
from config import db
from models.trek import Trek
from models.user import User
from models.booking import Booking
from datetime import datetime



admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/")
def dashboard():

    total_treks = Trek.query.count()

    total_users = User.query.filter_by(role="user").count()

    total_staff = User.query.filter_by(
        role="staff",
        approval_status="Approved"
    ).count()

    pending_staff = User.query.filter_by(
        role="staff",
        approval_status="Pending"
    ).count()

    total_bookings = Booking.query.count()

    recent_bookings = (
        Booking.query
        .order_by(Booking.id.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "admin/dashboard.html",
        total_treks=total_treks,
        total_users=total_users,
        total_staff=total_staff,
        pending_staff=pending_staff,
        total_bookings=total_bookings,
        recent_bookings=recent_bookings
    )

@admin_bp.route("/treks")
def treks():

    treks = Trek.query.all()

    return render_template(
        "admin/treks.html",
        treks=treks
    )

@admin_bp.route("/treks/edit/<int:trek_id>", methods=["GET", "POST"])
def edit_trek(trek_id):

    trek = db.session.get(Trek, trek_id)

    approved_staff = User.query.filter_by(
        role="staff",
        approval_status="Approved"
    ).all()

    if request.method == "POST":
        trek.trek_name = request.form.get("trek_name")
        trek.location = request.form.get("location")
        trek.difficulty = request.form.get("difficulty")

        trek.start_date = datetime.strptime(request.form.get("start_date"),"%Y-%m-%d").date()
        trek.end_date = datetime.strptime(request.form.get("end_date"),"%Y-%m-%d").date()
        trek.duration = int(request.form.get("duration"))
        trek.max_slots = int(request.form.get("max_slots"))
        trek.description = request.form.get("description")
        trek.status = request.form.get("status")
        trek.assigned_staff_id = request.form.get("assigned_staff_id") or None

        db.session.commit()

        return redirect(url_for("admin.treks"))

    return render_template(
        "admin/edit_trek.html",
        trek=trek,
        approved_staff=approved_staff
    )

@admin_bp.route("/treks/add", methods=["GET", "POST"])
def add_trek():

    approved_staff = User.query.filter_by(
        role="staff",
        approval_status="Approved"
    ).all()

    if request.method == "POST":

        max_slots = int(request.form.get("max_slots"))
        start_date = datetime.strptime( request.form.get("start_date"), "%Y-%m-%d" ).date()
        end_date = datetime.strptime( request.form.get("end_date"), "%Y-%m-%d" ).date()
        duration = int(request.form.get("duration"))
        assigned_staff_id = int(request.form.get("assigned_staff_id")) if request.form.get("assigned_staff_id") else None

        new_trek = Trek(
            trek_name=request.form.get("trek_name"),
            location=request.form.get("location"),
            difficulty=request.form.get("difficulty"),
            start_date=start_date,
            end_date=end_date,
            duration=duration,
            max_slots=max_slots,
            available_slots=max_slots,
            description=request.form.get("description"),
            status=request.form.get("status"),
            assigned_staff_id=assigned_staff_id
            
        )

        db.session.add(new_trek)
        db.session.commit()

        return redirect(url_for("admin.add_trek"))

    return render_template(
        "admin/add_trek.html",
        approved_staff=approved_staff
    )

@admin_bp.route("/treks/delete/<int:trek_id>", methods=["POST"])
def delete_trek(trek_id):

    trek = db.session.get(Trek, trek_id)
    
    if trek is None:
        return "Trek not found"

    db.session.delete(trek)
    db.session.commit()

    return redirect(url_for("admin.treks"))

@admin_bp.route("/staff")
def staff():

    staff = User.query.filter_by(
        role="staff",
        approval_status="Pending"
    ).all()

    return render_template( "admin/staff.html", staff=staff)


@admin_bp.route("/staff/approve/<int:staff_id>", methods=["POST"])
def approve_staff(staff_id):

    staff = db.session.get(User, staff_id)

    if staff is None:
        return "Staff not found"

    staff.approval_status = "Approved"

    db.session.commit()

    return redirect(url_for("admin.staff"))