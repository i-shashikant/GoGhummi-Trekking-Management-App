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

    q = request.args.get("q", "").strip()
    query = Trek.query

    if q:
        query = query.filter(Trek.trek_name.ilike(f"%{q}%"))
    treks = query.order_by(Trek.start_date).all()
    staff_list = User.query.filter_by(role="staff", approval_status="Approved").all()
    return render_template("admin/treks.html", treks=treks, staff_list=staff_list, q=q)

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

        max_slots = int(request.form["max_slots"])

        new_trek = Trek(
            trek_name=request.form["trek_name"],
            location=request.form["location"],
            difficulty=request.form["difficulty"],
            start_date=datetime.strptime(
                request.form["start_date"],
                "%Y-%m-%d"
            ).date(),
            end_date=datetime.strptime(
                request.form["end_date"],
                "%Y-%m-%d"
            ).date(),
            duration=int(request.form["duration"]),
            max_slots=max_slots,
            available_slots=max_slots,
            description=request.form["description"],
            status=request.form["status"],
            assigned_staff_id=request.form.get("assigned_staff_id") or None
        )

        db.session.add(new_trek)
        db.session.commit()

        return redirect(url_for("admin.treks"))

    return render_template(
        "admin/add_trek.html",
        staff_list=approved_staff
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

@admin_bp.route("/users")
def users():
    return render_template(
        "admin/users.html",
        users=[]
    )


@admin_bp.route("/bookings")
def bookings():
    return render_template(
        "admin/bookings.html",
        bookings=[]
    )


# @admin_bp.route("/staff")
# def staff():
#     staff_list = User.query.filter_by(role="staff").all()

#     return render_template(
#         "admin/staff.html",
#         staff_list=staff_list,
#         q=""
#     )


# @admin_bp.route("/treks")
# def treks():

#     treks = Trek.query.all()

#     staff_list = User.query.filter_by(
#         role="staff",
#         approval_status="Approved"
#     ).all()

#     return render_template(
#         "admin/treks.html",
#         treks=treks,
#         staff_list=staff_list,
#         q=""
#     )