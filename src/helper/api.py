from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin

from tool_box import user_authentication
import instaapi as insta

class FlaskAPIServer:

    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    token = ''

    def get_app(self):
        return self.app

    @staticmethod
    @cross_origin('*')
    @app.route('/instapush', methods=['POST'])
    def instapush():
        # Authentication
        auth_header = request.headers.get('Authorization')
        flag, error_message = user_authentication(auth_header, FlaskAPIServer.token)

        if not flag:
            return make_response(error_message, 401)

        # Get the data from the request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        content_type = data.get('type')
        caption = data.get('caption')
        file = data.get('file')
        thumbnail = data.get('thumbnail')

        # Upload the content to Instagram
        if content_type == 'photo':
            response = insta.InstagramService(username, password).upload_photo(file, caption)
            return make_response(response, 200)
        elif content_type == 'video':
            response = insta.InstagramService(username, password).upload_video(file, thumbnail, caption)
            return make_response(response, 200)
        elif content_type == 'reel':
            response = insta.InstagramService(username, password).upload_reel(file, caption)
            return make_response(response, 200)
        else:
            return make_response('Invalid content type', 400)