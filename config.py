from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config:
    SECRET_KEY = "trek_secret_key"
    SQLALCHEMI_DATABASE_URI = "sqlite:///trek.db"
    SQLALCHEMY_TRACK_MODIFICAITONS = False