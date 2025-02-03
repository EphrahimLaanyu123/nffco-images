from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'

db = SQLAlchemy(app)

# Models
class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    images = db.relationship('Image', backref='page', lazy=True)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)

# Create the database
@app.before_first_request
def create_tables():
    db.create_all()

# Routes
@app.route('/pages', methods=['POST'])
def create_page():
    data = request.form
    files = request.files.getlist('images')

    title = data.get('title')
    description = data.get('description')

    if not title:
        return jsonify({"error": "Title is required"}), 400

    page = Page(title=title, description=description)
    db.session.add(page)
    db.session.commit()

    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = Image(filename=filename, page_id=page.id)
            db.session.add(image)

    db.session.commit()
    return jsonify({"message": "Page created successfully", "page_id": page.id}), 201

@app.route('/pages', methods=['GET'])
def get_pages():
    pages = Page.query.all()
    output = []

    for page in pages:
        images = [url_for('static', filename=f'images/{img.filename}') for img in page.images]
        output.append({
            "id": page.id,
            "title": page.title,
            "description": page.description,
            "images": images
        })

    return jsonify(output)

@app.route('/pages/<int:page_id>', methods=['GET'])
def get_page(page_id):
    page = Page.query.get_or_404(page_id)
    images = [url_for('static', filename=f'images/{img.filename}') for img in page.images]

    return jsonify({
        "id": page.id,
        "title": page.title,
        "description": page.description,
        "images": images
    })

@app.route('/pages/<int:page_id>', methods=['PUT'])
def update_page(page_id):
    page = Page.query.get_or_404(page_id)
    data = request.form
    files = request.files.getlist('images')

    page.title = data.get('title', page.title)
    page.description = data.get('description', page.description)

    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = Image(filename=filename, page_id=page.id)
            db.session.add(image)

    db.session.commit()
    return jsonify({"message": "Page updated successfully"})

@app.route('/pages/<int:page_id>', methods=['DELETE'])
def delete_page(page_id):
    page = Page.query.get_or_404(page_id)

    # Delete associated images
    for img in page.images:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
        if os.path.exists(image_path):
            os.remove(image_path)
        db.session.delete(img)

    db.session.delete(page)
    db.session.commit()
