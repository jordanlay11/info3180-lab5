# Add any model classes for Flask-SQLAlchemy here
from . import db

class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    poster = db.Column(db.String(300))
    created_at= db.Column(db.DateTime, default=db.func.current_timestamp())

