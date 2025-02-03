from flask import Flask, request, jsonify
from models import db, Page, Image
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

class ImageUploadResource(Resource):
    def post(self):
        page_name = request.form.get('name')
        images = request.files.getlist('images')

        if not page_name or not images:
            return {"error": "Page name and images are required"}, 400

        # Create the page
        page = Page(name=page_name)
        db.session.add(page)

        for image in images:
            file_data = image.read()
            filename = image.filename
            new_image = Image(filename=filename, file_data=file_data, page=page)
            db.session.add(new_image)

        db.session.commit()
        return {"message": "Page and images uploaded successfully"}, 201

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
api.add_resource(ImageUploadResource, '/upload')
api.add_resource(PageImagesResource, '/pages/<int:page_id>/images')


if __name__ == '__main__':
    app.run(debug=True)
