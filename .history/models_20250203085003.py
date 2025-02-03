from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    images = db.relationship('Image', backref='page', lazy=True, cascade="all, delete-orphan")  # Relationship setup

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
        file_data = db.Column(db.LargeBinary, nullable=False)  # This should be a binary field to store image data

