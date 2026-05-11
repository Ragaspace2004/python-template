"""
Pytest configuration and shared fixtures.
"""

import pytest


@pytest.fixture
def sample_data():
    """Fixture providing sample test data."""
    return {
        "users": ["alice", "bob", "charlie"],
        "config": {"timeout": 30, "retries": 3},
    }


@pytest.fixture
def temp_file(tmp_path):
    """Fixture providing a temporary file."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Sample content")
    return file_path


@pytest.fixture(scope="session")
def session_data():
    """Session-scoped fixture for data shared across tests."""
    return {"session_id": "test-session-123"}
