from flask import Flask, render_template, request, redirect, url_for
from database import create_tables, add_user, get_user_by_username, add_trek, get_all_treks, delete_trek, get_trek_by_id, update_trek

app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = get_user_by_username(username)
        if user: 
            if user[3] == password:
                return render_template("dashboard.html")
            else:
                return "Invalid Password"
        else: 
            return "Username doesn't exists!"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        existing_user = get_user_by_username(username)

        if existing_user:
            return "username already exists!"
        
        add_user(username, email, password)
        return "User registered successfully!"
    return render_template("register.html")

@app.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/create_trek", methods=["GET", "POST"])
def create_trek():
    if request.method == "POST":
        trek_name = request.form.get("trek_name")
        location = request.form.get("location")
        difficulty = request.form.get("difficulty")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        duration = request.form.get("duration")
        max_slots = request.form.get("max_slots")
        description = request.form.get("description")
        status = request.form.get("status")
        assigned_staff_id = request.form.get("assigned_staff_id")

        add_trek(trek_name, location, difficulty, start_date, end_date, duration, max_slots, description, status, assigned_staff_id)
        return redirect(url_for("admin_dashboard"))
    #     # Handle form submission for creating a new trek
    #     pass
    return render_template("create_trek.html")

@app.route("/view_treks")
def view_treks():
    treks = get_all_treks()
    return render_template("view_treks.html", treks=treks)

@app.route("/delete_trek/<int:trek_id>")
def delete_trek_route(trek_id):

    delete_trek(trek_id)

    return redirect(url_for("view_treks"))

@app.route("/edit_trek/<int:trek_id>", methods=["GET", "POST"])
def edit_trek(trek_id):
    trek = get_trek_by_id(trek_id)
    if request.method == "POST":
        trek_name = request.form.get("trek_name")
        location = request.form.get("location")
        difficulty = request.form.get("difficulty")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        duration = request.form.get("duration")
        max_slots = request.form.get("max_slots")
        description = request.form.get("description")
        status = request.form.get("status")
        assigned_staff_id = request.form.get("assigned_staff_id")

        update_trek(trek_id, trek_name, location, difficulty, start_date, end_date, duration, max_slots, description, status, assigned_staff_id)
        return redirect(url_for("view_treks"))
    return render_template("edit_trek.html", trek=trek)

create_tables()
if __name__ == "__main__":
    app.run(debug=True) 