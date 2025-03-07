from functools import wraps
from flask import request, jsonify
from .authorization import get_user_by_token,check_role
from shared.exceptions import NotLoggedIn
from shared.response import messages

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

            
def required_login(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            token = request.headers.get("Authorization")
            print(token)
            if not token:
                raise NotLoggedIn(messages["You are not logged in, please login to access this"])
            user_role = check_role(role,token)
            if not user_role:
                raise NotLoggedIn(messages["You are not authorized to access this endpoint"])
            return func(*args,**kwargs)
        return wrapper
    return decorator

