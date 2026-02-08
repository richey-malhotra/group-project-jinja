"""
Authentication Routes — Login, Logout, and Session Management

Why sessions?
- HTTP is stateless — the server doesn't remember who you are between requests
- Sessions store a user identifier in an encrypted cookie
- Flask's session uses a signed cookie (protected by SECRET_KEY)
- This means we can check "who is logged in" on every request

Role-based access:
- admin: full access, can manage users
- manager: can view all tasks, manage their department
- staff: can view/edit only their assigned tasks
"""

from functools import wraps
from flask import Blueprint, request, session, redirect, url_for, flash, render_template, abort
from werkzeug.security import check_password_hash
from database import get_db

auth_bp = Blueprint("auth", __name__)


def login_required(f):
    """Decorator that protects routes — only logged-in users can access them.

    How decorators work:
    - They wrap a function with extra behaviour
    - @login_required before a route means "check login first"
    - If not logged in, redirect to login page with a flash message

    Unlike an API (which returns 401 JSON), a server-rendered app redirects
    the user to a login page — a better experience for browser-based users.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def role_required(*roles):
    """Decorator that checks the user has one of the allowed roles.

    Usage: @role_required('admin', 'manager')

    Returns 403 Forbidden if the user's role is not in the allowed list.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                flash("Please log in to access this page", "error")
                return redirect(url_for("auth.login"))
            if session.get("role") not in roles:
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@auth_bp.route("/", methods=["GET"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate a user and create a session.

    GET: render the login form
    POST: process login credentials from the form

    Security notes:
    - We never reveal WHETHER the username exists (same error for both cases)
    - Password is checked against the HASH, never compared as plain text
    - Session stores minimal info (id, username, role)
    - POST-Redirect-Get pattern prevents form resubmission on refresh
    """
    # If already logged in, redirect to dashboard
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "GET":
        return render_template("login.html")

    # POST — process login form
    username = request.form.get("username", "").strip().lower()
    password = request.form.get("password", "")

    # Validate input exists
    if not username or not password:
        flash("Username and password are required", "error")
        return redirect(url_for("auth.login"))

    # Look up user in database
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()

    # Check credentials — same error message for "user not found" and "wrong password"
    # This prevents attackers from discovering valid usernames
    if user is None or not check_password_hash(user["password_hash"], password):
        flash("Invalid username or password", "error")
        return redirect(url_for("auth.login"))

    # Create session — store user info for subsequent requests
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["role"] = user["role"]
    session["full_name"] = user["full_name"]
    session["department"] = user["department"]

    flash(f"Welcome back, {user['full_name']}!", "success")
    return redirect(url_for("dashboard.dashboard"))


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    """End the user's session.

    session.clear() removes all stored data — the user is now anonymous.
    Redirects to login page after clearing the session.
    """
    session.clear()
    flash("You have been logged out", "success")
    return redirect(url_for("auth.login"))
