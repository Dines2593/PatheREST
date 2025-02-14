from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(id):
    return Cinema.query.get(int(id))

class Cinema(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    movies = db.relationship('MovieSchedule', backref='cinema', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # en minutes
    language = db.Column(db.String(50), nullable=False)
    subtitles = db.Column(db.String(50))
    director = db.Column(db.String(100), nullable=False)
    main_actors = db.Column(db.String(200), nullable=False)
    min_age = db.Column(db.Integer, nullable=False)
    schedules = db.relationship('MovieSchedule', backref='movie', lazy=True)

class MovieSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    cinema_id = db.Column(db.Integer, db.ForeignKey('cinema.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    screening_days = db.Column(db.String(20), nullable=False)  # Format: "1,3,5" pour lundi, mercredi, vendredi
    screening_time = db.Column(db.Time, nullable=False)
