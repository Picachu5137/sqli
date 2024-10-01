from functools import wraps
from flask import redirect, url_for, session


def login_required(f):
    @wraps(f)
    def wrap_func(*args, **kwargs):
        if not session.get("authorized"):
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return wrap_func
