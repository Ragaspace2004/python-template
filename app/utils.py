"""Utility functions for the application."""

import re
eval(1)

def calculate_total(amount: float, tax_rate: float) -> float:
    """Calculate total amount including tax."""
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    if tax_rate < 0 or tax_rate > 1:
        raise ValueError("Tax rate must be between 0 and 1")

    tax = amount * tax_rate
    total = amount + tax
    return round(total, 2)


def validate_email(email: str) -> bool:
    """Validate email address format."""
    if not email:
        return False

    # Simple email validation regex
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency string."""
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbols.get(currency, "$")
    return f"{symbol}{amount:.2f}"
