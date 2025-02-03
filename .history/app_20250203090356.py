import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_cors import CORS
from werkzeug.utils import secure_filename
from models import db, Page, Image
import base64

app = Flask(__name__)

# Ensure the directory exists
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size 16MB

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

class PageResource(Resource):
    def post(self):
        page_name = request.json.get('name')
        if not page_name:
            return {"error": "Page name is required"}, 400

        page = Page(name=page_name)
        db.session.add(page)
        db.session.commit()
        return {"message": f"Page '{page_name}' created successfully", "page_id": page.id}, 201

    def get(self):
        pages = Page.query.all()  # Get all pages from the database
        pages_data = []

        for page in pages:
            pages_data.append({
                "id": page.id,
                "name": page.name
            })

        return {"pages": pages_data}, 200

class ImageResource(Resource):
    def post(self):
        page_id = request.form.get('page_id')
        images = request.files.getlist('images')

        if not page_id or not images:
            return {"error": "Page ID and images are required"}, 400

        page = Page.query.get(page_id)
        if not page:
            return {"error": "Page not found"}, 404

        for image in images:
            filename = secure_filename(image.filename)
            file_data = image.read()
            new_image = Image(filename=filename, file_data=file_data, page_id=page.id)  # Use page_id instead of page object
            db.session.add(new_image)

        db.session.commit()
        return {"message": "Images added to the page successfully"}, 201

class PageImagesResource(Resource):
    def get(self, page_id):
        page = Page.query.get_or_404(page_id)
        images_data = []

        for image in page.images:
            encoded_image = base64.b64encode(image.file_data).decode('utf-8')
            images_data.append({
                "filename": image.filename,
                "file_data": encoded_image
            })

        return {"page_name": page.name, "images": images_data}, 200

# Register API resources
api.add_resource(PageResource, '/pages')
api.add_resource(ImageResource, '/pages/images')
api.add_resource(PageImagesResource, '/pages/<int:page_id>/images')

if __name__ == '__main__':
    app.run(debug=True)
