from flask import Flask
from config import Config, db
from routes import all_blueprints
from models import User, Trek, Booking
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.secret_key = "trekking_secret_key"

for bp in all_blueprints:
    app.register_blueprint(bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()


        admin = User.query.filter_by(username="admin").first()

        if not admin:
            admin = User(
                username="admin",
                email="admin@gmail.com",
                password=generate_password_hash("admin123"),
                role="admin",
                approval_status="Approved"
            )

            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)