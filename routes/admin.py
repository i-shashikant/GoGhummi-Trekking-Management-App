from flask import Blueprint, render_template, request, redirect, url_for, flash
from config import db
from models.trek import Trek
from models.user import User
from models.booking import Booking
from datetime import datetime
from utils.auth import admin_required



admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/")
@admin_required
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
@admin_required
def treks():

    q = request.args.get("q", "").strip()
    query = Trek.query

    if q:
        query = query.filter(Trek.trek_name.ilike(f"%{q}%"))
    treks = query.order_by(Trek.start_date).all()
    staff_list = User.query.filter_by(role="staff", approval_status="Approved").all()
    return render_template("admin/treks.html", treks=treks, staff_list=staff_list, q=q)

@admin_bp.route("/treks/edit/<int:trek_id>", methods=["GET", "POST"])
@admin_required
def edit_trek(trek_id):

    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return "Trek not found", 404

    staff_list = User.query.filter_by(
        role="staff",
        approval_status="Approved"
    ).all()
    old_max_slots = trek.max_slots
    old_available_slots = trek.available_slots
    booked_slots = old_max_slots - old_available_slots

    if request.method == "POST":

        trek.trek_name = request.form["trek_name"]
        trek.location = request.form["location"]
        trek.difficulty = request.form["difficulty"]
        trek.start_date = datetime.strptime(
            request.form["start_date"],
            "%Y-%m-%d"
        ).date()

        trek.end_date = datetime.strptime(
            request.form["end_date"],
            "%Y-%m-%d"
        ).date()

        trek.duration = int(request.form["duration"])
        trek.price = int(request.form["price"])

        new_max_slots = int(request.form["max_slots"])

        if new_max_slots < booked_slots:
            flash(
                f"Cannot reduce maximum slots below the number of booked participants ({booked_slots}).",
                "danger"
            )
            return redirect(
                url_for("admin.edit_trek", trek_id=trek.id)
            )
        trek.max_slots = new_max_slots
        trek.available_slots = new_max_slots - booked_slots
        trek.description = request.form["description"]

        trek.status = request.form["status"]

        trek.assigned_staff_id = (
            request.form.get("assigned_staff_id") or None
        )

        db.session.commit()

        flash("Trek updated successfully.", "success")
        return redirect(url_for("admin.treks"))

    return render_template(
        "admin/edit_trek.html",
        trek=trek,
        staff_list=staff_list,
    )

@admin_bp.route("/treks/add", methods=["GET", "POST"])
@admin_required
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
            price=int(request.form.get("price")),
            max_slots=max_slots,
            available_slots=max_slots,
            description=request.form["description"],
            status=request.form["status"],
            assigned_staff_id=request.form.get("assigned_staff_id") or None
        )

        db.session.add(new_trek)
        db.session.commit()

        flash("Trek created successfully.", "success")
        return redirect(url_for("admin.treks"))

    return render_template(
        "admin/add_trek.html",
        staff_list=approved_staff
    )

@admin_bp.route("/treks/delete/<int:trek_id>", methods=["POST"])
@admin_required
def delete_trek(trek_id):

    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return "Trek not found", 404

    # Prevent deleting a trek that has bookings
    if trek.bookings:
        return "Cannot delete a trek that has bookings."

    db.session.delete(trek)
    db.session.commit()
    flash("Trek deleted successfully.", "success")
    return redirect(url_for("admin.treks"))

@admin_bp.route("/staff")
@admin_required
def staff():

    q = request.args.get("q", "").strip()

    query = User.query.filter_by(role="staff")

    if q:
        query = query.filter(User.username.ilike(f"%{q}%"))

    staff_list = query.order_by(User.username).all()

    return render_template(
        "admin/staff.html",
        staff_list=staff_list,
        q=q
    )


@admin_bp.route("/staff/approve/<int:user_id>", methods=["POST"])
@admin_required
def approve_staff(user_id):

    staff = db.session.get(User, user_id)

    if staff is None:
        return "Staff not found", 404

    staff.approval_status = "Approved"

    db.session.commit()
    flash("Staff approved successfully.", "success")
    return redirect(url_for("admin.staff"))

@admin_bp.route("/staff/blacklist/<int:user_id>", methods=["POST"])
@admin_required
def blacklist_staff(user_id):

    staff = db.session.get(User, user_id)

    if staff is None:
        return "Staff not found", 404

    staff.approval_status = "Blacklisted"

    db.session.commit()

    return redirect(url_for("admin.staff"))


@admin_bp.route("/treks/assign/<int:trek_id>", methods=["POST"])
@admin_required
def assign_staff(trek_id):

    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return "Trek not found", 404

    staff_id = request.form.get("assigned_staff_id")

    if staff_id:
        trek.assigned_staff_id = int(staff_id)
    else:
        trek.assigned_staff_id = None

    db.session.commit()
    flash("Staff assigned successfully.", "success")
    return redirect(url_for("admin.treks"))


@admin_bp.route("/users")
@admin_required
def users():

    q = request.args.get("q", "").strip()

    query = User.query.filter_by(role="user")

    if q:
        query = query.filter(User.username.ilike(f"%{q}%"))

    users = query.order_by(User.username).all()

    return render_template(
        "admin/users.html",
        users=users,
        q=q
    )

@admin_bp.route("/users/blacklist/<int:user_id>", methods=["POST"])
@admin_required
def blacklist_user(user_id):

    user = db.session.get(User, user_id)

    if user is None:
        return "User not found", 404

    user.approval_status = "Blacklisted"

    db.session.commit()
    flash("Staff blacklisted successfully.", "warning")
    return redirect(url_for("admin.users"))

@admin_bp.route("/users/activate/<int:user_id>", methods=["POST"])
@admin_required
def activate_user(user_id):

    user = db.session.get(User, user_id)

    if user is None:
        return "User not found", 404

    user.approval_status = "Approved"

    db.session.commit()

    return redirect(url_for("admin.users"))


@admin_bp.route("/bookings")
@admin_required
def bookings():

    bookings = (
        Booking.query
        .order_by(Booking.booking_date.desc())
        .all()
    )

    return render_template(
        "admin/bookings.html",
        bookings=bookings
    )
