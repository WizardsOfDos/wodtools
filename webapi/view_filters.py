from functools import wraps
from flask import request, abort

from webapi import app


def acceptable_content_types(content_types=[]):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            if request.headers['Content-Type'] not in content_types:
                abort(400)
            else:
                return f(*args, **kwargs)
        return decorator_function
    return decorator