from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
import jwt
import os
from datetime import datetime, timedelta

from helper.tool_box import user_authentication
from helper.instaapi import InstagramService


class FlaskAPIServer:
    """
    This class is used to create a Flask API server that can be used to upload content to Instagram.
    """

    def __init__(self):
        self.app = Flask(__name__)  # Use self.app instead of a global app variable
        CORS(self.app, resources={r"/*": {"origins": "*"}})
        self.SECRET_KEY = 'your-secret-key'
        self.token = jwt.encode({'user': 'instauser', 'exp': datetime.utcnow() + timedelta(hours=1)}, self.SECRET_KEY, algorithm='HS256')
        self.register_routes()

    def get_app(self):
        return self.app

    def register_routes(self):
        @self.app.route('/instapush', methods=['POST'])
        @cross_origin('*')
        def instapush():
            # Authentication
            auth_header = request.headers.get('Authorization')
            flag, error_message = user_authentication(auth_header, self.SECRET_KEY)

            if not flag:
                return make_response({"error": error_message}, 401)

            # Get the data from the request
            username = request.form.get('username')
            password = request.form.get('password')
            content_type = request.form.get('type')
            caption = request.form.get('caption')

            file = request.files.get('file')
            thumbnail = request.files.get('thumbnail')

            if not file:
                return make_response({"error": "File is required"}, 400)

            # Save files locally
            file_path = f"/tmp/{file.filename}"
            file.save(file_path)

            thumbnail_path = None
            if content_type == 'video':
                if not thumbnail:
                    return make_response({"error": "Thumbnail is required for video uploads"}, 400)
                thumbnail_path = f"/tmp/{thumbnail.filename}"
                thumbnail.save(thumbnail_path)

            try:
                # Upload content
                if content_type == 'photo':
                    response = InstagramService(username, password).upload_photo(file_path, caption)
                elif content_type == 'video':
                    response = InstagramService(username, password).upload_video(file_path, thumbnail_path, caption)
                elif content_type == 'reel':
                    response = InstagramService(username, password).upload_reel(file_path, caption)
                else:
                    return make_response({"error": "Invalid content type"}, 400)
            except Exception as e:
                return make_response({"error": str(e)}, 500)
            finally:
                # Clean up files
                if os.path.exists(file_path):
                    os.remove(file_path)
                if thumbnail_path and os.path.exists(thumbnail_path):
                    os.remove(thumbnail_path)

            return make_response(response, 200)
