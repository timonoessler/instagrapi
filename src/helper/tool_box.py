from flask import make_response, jsonify

def user_authentication(auth_header, token):
    # Extract the token (bearer scheme expected)
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(" ")[1]  # Remove the 'Bearer' prefix
    else:
        return False, 'Coud not extract token'

    # Check if the token is in the dict of tokens and extracts the user and password for the database
    if token != token:
        return False, 'Invalid token'

    return True, 'Token is valid'