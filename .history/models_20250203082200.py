from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(50), nullable=False)
    image_data = db.Column(db.LargeBinary)  # BLOB field for image data
    suggested_at = db.Column(db.DateTime, default=datetime.utcnow)


