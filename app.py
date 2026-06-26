from flask import Flask, render_template, request
from database import create_tables, add_user

app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(f"Username: {username}, Password: {password}")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        add_user(username, email, password)
        return "User registered successfully!"
    return render_template("register.html")

if __name__ == "__main__":
    create_tables()
    app.run(debug=True) 