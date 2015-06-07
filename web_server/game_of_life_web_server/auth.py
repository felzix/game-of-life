from flask import abort, session
from functools import wraps


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            abort(401)
    return decorated
