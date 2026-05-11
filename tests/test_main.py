"""
Sample test module for the Python DevSecOps CI pipeline.
This demonstrates basic pytest functionality.
"""

import pytest


def test_sample_pass():
    """Basic passing test."""
    assert True


def test_addition():
    """Test basic arithmetic."""
    assert 1 + 1 == 2


def test_string_operations():
    """Test string operations."""
    text = "DevSecOps"
    assert text.lower() == "devsecops"
    assert len(text) == 9


def test_list_operations():
    """Test list operations."""
    items = [1, 2, 3, 4, 5]
    assert len(items) == 5
    assert sum(items) == 15
    assert max(items) == 5


def test_dictionary_operations():
    """Test dictionary operations."""
    config = {"environment": "test", "debug": True, "version": "1.0.0"}
    assert config["environment"] == "test"
    assert config.get("debug") is True
    assert "version" in config


class TestSampleClass:
    """Sample test class demonstrating test organization."""

    def test_class_method(self):
        """Test within a class."""
        assert "test" in "pytest"

    def test_with_fixture(self):
        """Test demonstrating fixture usage."""
        test_data = {"key": "value"}
        assert test_data["key"] == "value"


@pytest.mark.parametrize(
    "input_value,expected",
    [
        (1, 2),
        (2, 4),
        (3, 6),
        (4, 8),
    ],
)
def test_parametrized(input_value, expected):
    """Test with parametrization."""
    assert input_value * 2 == expected


def test_exception_handling():
    """Test exception handling."""
    with pytest.raises(ZeroDivisionError):
        _ = 1 / 0


def test_type_checking():
    """Test type checking."""
    value = "string"
    assert isinstance(value, str)
    assert not isinstance(value, int)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
