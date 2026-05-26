"""Main entry point for the Flask application."""

import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Get host from environment variable, default to localhost for security
    # Use 0.0.0.0 only in development/Docker environments
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "5000"))
    debug = os.getenv("FLASK_ENV", "production") == "development"

    app.run(debug=debug, host=host, port=port)  # nosec B104
