# from flask import Flask, render_template, request, redirect, url_for, session
# from database import create_tables, add_user, get_user_by_username, add_trek, get_all_treks, delete_trek, get_trek_by_id, update_trek, get_pending_staff, approve_staff, get_approved_staff, get_treks_by_staff, update_trek_by_staff
# from database import get_open_treks, book_trek, decrease_available_slots, has_booked_trek, get_user_bookings, get_users_by_trek

# from config import Config, db

# app = Flask(__name__)
# app.config.from_object(Config)
# db.init_app(app)

# app.secret_key = "trekking_secret_key"

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")

#         user = get_user_by_username(username)

#         if user:

#             if user[3] == password:
#                 session["user_id"] = user[0]
#                 session["username"] = user[1]
#                 session["role"] = user[4]

#                 if user[4] == "admin":
#                     return render_template("admin_dashboard.html")

#                 elif user[4] == "user":
#                     return redirect(url_for("user_dashboard"))

#                 elif user[4] == "staff":

#                     if user[5] == "Pending":
#                         return "Your account is waiting for admin approval."

#                     return redirect(url_for("staff_dashboard"))

#             else:
#                 return "Invalid Password"

#         else:
#             return "Username doesn't exist!"

#     return render_template("login.html")

# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form.get("username")
#         email = request.form.get("email")
#         password = request.form.get("password")
#         existing_user = get_user_by_username(username)
#         role = request.form.get("role")

#         if existing_user:
#             return "username already exists!"
#         if role == "staff":
#             approval_status = "Pending"
#         else:
#             approval_status = "Approved"

#         add_user(username, email, password, role, approval_status)
#         return "User registered successfully!"
#     return render_template("register.html")

# @app.route("/admin")
# def admin_dashboard():
#     return render_template("admin_dashboard.html")

# @app.route("/create_trek", methods=["GET", "POST"])
# def create_trek():
#     if request.method == "POST":
#         trek_name = request.form.get("trek_name")
#         location = request.form.get("location")
#         difficulty = request.form.get("difficulty")
#         start_date = request.form.get("start_date")
#         end_date = request.form.get("end_date")
#         duration = request.form.get("duration")
#         max_slots = request.form.get("max_slots")
#         description = request.form.get("description")
#         status = request.form.get("status")
#         assigned_staff_id = request.form.get("assigned_staff_id")

#         add_trek(trek_name, location, difficulty, start_date, end_date, duration, max_slots, description, status, assigned_staff_id)
#         return redirect(url_for("admin_dashboard"))

#     approved_staff = get_approved_staff()
#     return render_template("create_trek.html", approved_staff=approved_staff)

# @app.route("/view_treks")
# def view_treks():
#     treks = get_all_treks()
#     return render_template("view_treks.html", treks=treks)

# @app.route("/delete_trek/<int:trek_id>")
# def delete_trek_route(trek_id):

#     delete_trek(trek_id)

#     return redirect(url_for("view_treks"))

# @app.route("/edit_trek/<int:trek_id>", methods=["GET", "POST"])
# def edit_trek(trek_id):
#     trek = get_trek_by_id(trek_id)
#     approved_staff = get_approved_staff()
#     if request.method == "POST":
#         trek_name = request.form.get("trek_name")
#         location = request.form.get("location")
#         difficulty = request.form.get("difficulty")
#         start_date = request.form.get("start_date")
#         end_date = request.form.get("end_date")
#         duration = request.form.get("duration")
#         max_slots = request.form.get("max_slots")
#         description = request.form.get("description")
#         status = request.form.get("status")
#         assigned_staff_id = request.form.get("assigned_staff_id")

#         update_trek(trek_id, trek_name, location, difficulty, start_date, end_date, duration, max_slots, description, status, assigned_staff_id)
#         return redirect(url_for("view_treks"))
#     approved_staff = get_approved_staff()
#     return render_template("edit_trek.html", trek=trek, approved_staff=approved_staff)

# @app.route("/pending_staff")
# def pending_staff():
#     staff = get_pending_staff()
#     return render_template("pending_staff.html", staff=staff)

# @app.route('/approve_staff/<int:staff_id>')
# def approve_staff_route(staff_id):
#     approve_staff(staff_id)
#     return redirect(url_for("pending_staff"))

# @app.route('/staff')
# def staff_dashboard():

#     staff_id = session["user_id"]
#     treks = get_treks_by_staff(staff_id)
#     return render_template("staff_dashboard.html", treks=treks)

# @app.route("/staff/update/<int:trek_id>", methods=["GET", "POST"])
# def update_trek_staff(trek_id):

#     trek = get_trek_by_id(trek_id)

#     if request.method == "POST":

#         available_slots = request.form.get("available_slots")
#         status = request.form.get("status")

#         update_trek_by_staff(
#             trek_id,
#             available_slots,
#             status
#         )

#         return redirect(url_for("staff_dashboard"))

#     return render_template(
#         "update_trek_staff.html", trek=trek
#     )

# @app.route("/user")
# def user_dashboard():
#     treks = get_open_treks()
#     return render_template("user_dashboard.html", treks=treks)


# @app.route("/book_trek/<int:trek_id>", methods=["GET"])
# def book_trek_route(trek_id):
#     user_id = session["user_id"]

# # Already booked?
#     if has_booked_trek(user_id, trek_id):
#         return "You have already booked this trek."

#     trek = get_trek_by_id(trek_id)

#     # No slots left?
#     if trek[8] <= 0:
#         return "Sorry! No slots available."

#     book_trek(user_id, trek_id)

#     decrease_available_slots(trek_id)

#     return redirect(url_for("user_dashboard"))

# @app.route("/my_bookings")
# def my_bookings():
#     user_id = session["user_id"]
#     bookings = get_user_bookings(user_id)
#     return render_template("my_bookings.html", bookings=bookings)

# @app.route("/staff/participants/<int:trek_id>")
# def staff_participants(trek_id):
#     participants = get_users_by_trek(trek_id)
#     return render_template("staff_participants.html", participants=participants)

# create_tables()
# if __name__ == "__main__":
#     app.run(debug=True) 