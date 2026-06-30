from flask import Blueprint, render_template, request, redirect, url_for
from config import db
from models.trek import Trek
from models.user import User
from datetime import datetime



admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@admin_bp.route("/view_treks")
def view_treks():

    treks = Trek.query.all()

    return render_template(
        "view_treks.html",
        treks=treks
    )

@admin_bp.route("/edit_trek/<int:trek_id>", methods=["GET","POST"])
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
        trek.start_date = request.form.get("start_date")
        trek.end_date = request.form.get("end_date")
        trek.duration = request.form.get("duration")
        trek.max_slots = request.form.get("max_slots")
        trek.available_slots = request.form.get("available_slots")
        trek.description = request.form.get("description")
        trek.status = request.form.get("status")
        trek.assigned_staff_id = request.form.get("assigned_staff_id")

    db.session.commit()

    return redirect(url_for("admin.view_treks"))

    return render_template(
        "edit_trek.html",
        trek=trek,
        approved_staff=approved_staff
    )

@admin_bp.route("/create_trek", methods=["GET", "POST"])
def create_trek():

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

        return redirect(url_for("admin.view_treks"))

    return render_template(
        "create_trek.html",
        approved_staff=approved_staff
    )

@admin_bp.route("/delete_trek/<int:trek_id>")
def delete_trek(trek_id):

    trek = db.session.get(Trek, trek_id)
    
    if trek is None:
        return "Trek not found"

    db.session.delete(trek)
    db.session.commit()

    return redirect(url_for("admin.view_treks"))

@admin_bp.route("/pending_staff")
def pending_staff():

    staff = User.query.filter_by(
        role="staff",
        approval_status="Pending"
    ).all()

    return render_template(
        "pending_staff.html",
        staff=staff
    )


@admin_bp.route("/approve_staff/<int:staff_id>")
def approve_staff(staff_id):

    staff = db.session.get(User, staff_id)

    if staff is None:
        return "Staff not found"

    staff.approval_status = "Approved"

    db.session.commit()

    return redirect(url_for("admin.pending_staff"))