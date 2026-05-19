"""
Security-related tests to demonstrate security testing practices.
"""


def test_no_hardcoded_secrets():
    """Ensure no hardcoded secrets in test data."""
    test_config = {"api_key": "test_key_placeholder", "password": "test_password"}
    # In real scenarios, these would come from environment variables
    assert "placeholder" in test_config["api_key"]


def test_input_validation():
    """Test input validation logic."""

    def validate_email(email):
        """Simple email validation."""
        return "@" in email and "." in email.split("@")[1]

    assert validate_email("user@example.com") is True
    assert validate_email("invalid-email") is False


def test_sql_injection_prevention():
    """Demonstrate SQL injection prevention awareness."""
    # This is a demonstration - in real code, use parameterized queries
    user_input = "admin' OR '1'='1"

    # Bad practice (vulnerable)
    # query = f"SELECT * FROM users WHERE username = '{user_input}'"

    # Good practice (parameterized)
    def safe_query(username):
        """Simulate parameterized query."""
        return ("SELECT * FROM users WHERE username = ?", (username,))

    query, params = safe_query(user_input)
    assert "?" in query
    assert user_input in params


def test_xss_prevention():
    """Test XSS prevention."""

    def sanitize_html(text):
        """Simple HTML sanitization."""
        # Order matters: escape & first to avoid double-escaping
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        return text

    malicious_input = "<script>alert('XSS')</script>"
    sanitized = sanitize_html(malicious_input)
    assert "<script>" not in sanitized
    assert "&lt;script&gt;" in sanitized


def test_path_traversal_prevention():
    """Test path traversal prevention."""

    def is_safe_path(user_path):
        """Check if path is safe from traversal attacks."""
        return ".." not in user_path and not user_path.startswith("/")

    assert is_safe_path("documents/file.txt") is True
    assert is_safe_path("../etc/passwd") is False
    assert is_safe_path("/etc/passwd") is False


class TestAuthentication:
    """Authentication-related security tests."""

    def test_password_requirements(self):
        """Test password strength requirements."""

        def is_strong_password(password):
            """Check password strength."""
            return (
                len(password) >= 8
                and any(c.isupper() for c in password)
                and any(c.islower() for c in password)
                and any(c.isdigit() for c in password)
            )

        assert is_strong_password("StrongP@ss123") is True
        assert is_strong_password("weak") is False

    def test_session_timeout(self):
        """Test session timeout logic."""
        import time

        session_start = time.time()
        timeout_seconds = 3600  # 1 hour

        def is_session_valid(start_time, timeout):
            """Check if session is still valid."""
            return (time.time() - start_time) < timeout

        assert is_session_valid(session_start, timeout_seconds) is True
