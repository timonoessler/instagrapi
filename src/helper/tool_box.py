from flask import make_response, jsonify
import jwt

def user_authentication(auth_header, secret_key):
    # Extract the token (bearer scheme expected)
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(" ")[1]  # Remove the 'Bearer' prefix
    else:
        return False, 'Could not extract token'

    try:
        # Decode the token using the secret key
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return True, 'Token is valid'
    except jwt.InvalidTokenError:
        return False, 'Invalid token'