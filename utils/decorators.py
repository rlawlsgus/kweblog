# utils/decorators.py
from flask import session, redirect, url_for, flash
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("로그인이 필요합니다.")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function
