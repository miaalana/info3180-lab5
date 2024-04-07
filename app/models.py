# Add any model classes for Flask-SQLAlchemy here
from datetime import datetime
from . import db

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    poster = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Movie {self.title}>'
