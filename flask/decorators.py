from functools import wraps
from flask import request
from flask_restplus import abort


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.headers.get('Authorization'):
            return func(*args, **kwargs)
        else:
            return abort(401)
    return wrapper
