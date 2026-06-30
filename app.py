from flask import Flask
from config import Config, db
from routes import all_blueprints
from models import User, Trek, Booking

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.secret_key = "trekking_secret_key"

for bp in all_blueprints:
    app.register_blueprint(bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)