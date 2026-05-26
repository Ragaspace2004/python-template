"""Flask application factory."""

import os

from flask import Flask


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    # Use environment variable for secret key, fallback to dev key
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # Register blueprints
    from app.routes import api_bp

    app.register_blueprint(api_bp)

    return app
