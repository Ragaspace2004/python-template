"""
Utility function tests.
"""

import pytest


def test_data_validation():
    """Test data validation utilities."""

    def validate_positive_number(value):
        """Validate positive number."""
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be a number")
        if value <= 0:
            raise ValueError("Value must be positive")
        return True

    assert validate_positive_number(5) is True
    assert validate_positive_number(3.14) is True

    with pytest.raises(ValueError):
        validate_positive_number(-1)

    with pytest.raises(TypeError):
        validate_positive_number("not a number")


def test_string_utilities():
    """Test string utility functions."""

    def truncate_string(text, max_length):
        """Truncate string to max length."""
        if len(text) <= max_length:
            return text
        return text[: max_length - 3] + "..."

    assert truncate_string("short", 10) == "short"
    assert truncate_string("this is a very long string", 10) == "this is..."


def test_list_utilities():
    """Test list utility functions."""

    def chunk_list(items, chunk_size):
        """Split list into chunks."""
        return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]

    data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    chunks = chunk_list(data, 3)

    assert len(chunks) == 3
    assert chunks[0] == [1, 2, 3]
    assert chunks[2] == [7, 8, 9]


def test_dict_utilities():
    """Test dictionary utility functions."""

    def merge_dicts(*dicts):
        """Merge multiple dictionaries."""
        result = {}
        for d in dicts:
            result.update(d)
        return result

    dict1 = {"a": 1, "b": 2}
    dict2 = {"c": 3, "d": 4}
    merged = merge_dicts(dict1, dict2)

    assert len(merged) == 4
    assert merged["a"] == 1
    assert merged["d"] == 4


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("hello", "HELLO"),
        ("WORLD", "WORLD"),
        ("MiXeD", "MIXED"),
    ],
)
def test_uppercase_conversion(input_str, expected):
    """Test uppercase conversion."""
    assert input_str.upper() == expected


def test_fixture_usage(sample_data):
    """Test using fixture from conftest.py."""
    assert "users" in sample_data
    assert len(sample_data["users"]) == 3
    assert sample_data["config"]["timeout"] == 30


def test_temp_file_fixture(temp_file):
    """Test using temp file fixture."""
    assert temp_file.exists()
    content = temp_file.read_text()
    assert content == "Sample content"
