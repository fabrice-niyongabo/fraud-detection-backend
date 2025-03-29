from flask import jsonify, request
import jwt 
from http import HTTPStatus
from functools import wraps
from app.config import Config

# Custom decorator to verify JWT

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            current_user = {
                "email": data['email'],
                "isActive": data.get('isActive', True)  # Default to True if not present
            }
        except Exception as e:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)
    return decorated