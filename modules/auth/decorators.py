from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """
    Protects routes from unauthenticated access.
    If admin is not logged in, redirect to login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login to access this page.", "warning")
            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)

    return decorated_function