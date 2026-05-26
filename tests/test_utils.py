"""Tests for utility functions."""

import pytest

from app.utils import calculate_total, format_currency, validate_email


def test_calculate_total():
    """Test calculate_total function."""
    assert calculate_total(100, 0.1) == 110.0
    assert calculate_total(50, 0.2) == 60.0
    assert calculate_total(0, 0.1) == 0.0


def test_calculate_total_negative_amount():
    """Test calculate_total with negative amount."""
    with pytest.raises(ValueError, match="Amount cannot be negative"):
        calculate_total(-100, 0.1)


def test_calculate_total_invalid_tax_rate():
    """Test calculate_total with invalid tax rate."""
    with pytest.raises(ValueError, match="Tax rate must be between 0 and 1"):
        calculate_total(100, 1.5)

    with pytest.raises(ValueError, match="Tax rate must be between 0 and 1"):
        calculate_total(100, -0.1)


def test_validate_email():
    """Test email validation."""
    # Valid emails
    assert validate_email("test@example.com") is True
    assert validate_email("user.name@domain.co.uk") is True
    assert validate_email("user+tag@example.com") is True

    # Invalid emails
    assert validate_email("") is False
    assert validate_email("invalid") is False
    assert validate_email("@example.com") is False
    assert validate_email("user@") is False


def test_format_currency():
    """Test currency formatting."""
    assert format_currency(100.50, "USD") == "$100.50"
    assert format_currency(50.99, "EUR") == "€50.99"
    assert format_currency(75.25, "GBP") == "£75.25"
    assert format_currency(100, "JPY") == "$100.00"  # Default to USD
