from functools import wraps
from flask import request, jsonify
from .authorization import get_user_by_token

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"message":"Token is required"}),401
            user = get_user_by_token(token)
            if not user:
                return jsonify({"error":"Invalid or expired token"}),401

            if not user or not user.has_role(role):
                return jsonify({"error":"permission denied"}), 403
            
            return func(*args,**kwargs)
        return wrapper
    return decorator

            
