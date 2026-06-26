from flask import Flask, render_template, request
from database import create_tables, add_user, get_user_by_username

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

create_tables()
if __name__ == "__main__":
    app.run(debug=True) 