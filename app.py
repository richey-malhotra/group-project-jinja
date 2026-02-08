"""
MJ Limited Staff Portal — Main Application Entry Point

This is the Flask application factory. It creates and configures the app,
registers all route blueprints, and sets up shared resources like the
database connection and upload folder.

Why Flask + Jinja2?
- Lightweight: minimal boilerplate, easy to understand
- Server-rendered: Flask generates complete HTML pages via Jinja2 templates
- Secure by default: Jinja2 auto-escapes all template variables (XSS protection)
- Explicit: no magic — every route, query, and template call is visible
"""

import os
from flask import Flask, render_template, flash, redirect, request
from dotenv import load_dotenv

# Load environment variables from .env file
# This keeps secrets out of source code — a key security practice
load_dotenv()


def create_app():
    """Application factory pattern — creates and configures the Flask app.

    Why use a factory?
    - Allows different configs for dev/test/production
    - Makes the app testable
    - Professional best practice
    """
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
    )

    # --- Configuration ---
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-fallback-key")
    app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "uploads")
    app.config["MAX_CONTENT_LENGTH"] = int(
        os.getenv("MAX_CONTENT_LENGTH", 5 * 1024 * 1024)
    )  # 5MB default

    # Session cookie settings
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    # Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # --- Database initialisation ---
    from database import init_db

    init_db()

    # --- Register route blueprints ---
    # Blueprints keep routes organised by feature — each feature gets its own file
    # No /api prefix — routes serve HTML pages directly
    from routes.auth import auth_bp
    from routes.tasks import tasks_bp
    from routes.clients import clients_bp
    from routes.dashboard import dashboard_bp
    from routes.attachments import attachments_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp, url_prefix="/tasks")
    app.register_blueprint(clients_bp, url_prefix="/clients")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(attachments_bp, url_prefix="/attachments")

    # --- Error handlers ---
    @app.errorhandler(404)
    def not_found(e):
        """Custom 404 — renders a styled template instead of Flask's default."""
        return render_template("404.html"), 404

    @app.errorhandler(413)
    def file_too_large(e):
        """Handle file uploads that exceed the size limit."""
        flash("File too large. Maximum size is 5MB.", "error")
        return redirect(request.referrer or url_for("dashboard.dashboard"))

    return app


# --- Entry point ---
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
