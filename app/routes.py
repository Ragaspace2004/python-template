"""API routes for the Flask application."""

from flask import Blueprint, jsonify, request

from app.utils import calculate_total, validate_email

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/calculate-tax", methods=["POST"])
def calculate_tax():
    """Calculate total with tax."""
    data = request.get_json()
    amount = data.get("amount", 0)
    tax_rate = data.get("tax_rate", 0.1)

    total = calculate_total(amount, tax_rate)

    return jsonify({"amount": amount, "tax_rate": tax_rate, "total": total}), 200


@api_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "message": "API is running"}), 200


@api_bp.route("/calculate", methods=["POST"])
def calculate():
    """Calculate total with tax."""
    data = request.get_json()
    amount = data.get("amount", 0)
    tax_rate = data.get("tax_rate", 0.1)

    total = calculate_total(amount, tax_rate)

    return jsonify({"amount": amount, "tax_rate": tax_rate, "total": total}), 200


@api_bp.route("/validate-email", methods=["POST"])
def validate_email_endpoint():
    """Validate email address."""
    data = request.get_json()
    email = data.get("email", "")

    is_valid = validate_email(email)

    return jsonify({"email": email, "is_valid": is_valid}), 200


@api_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    """Get user by ID."""
    # Mock user data
    users = {
        1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
        2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
    }

    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200
