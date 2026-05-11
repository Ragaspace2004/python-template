# Test Suite

This directory contains the test suite for the Python DevSecOps CI pipeline.

## Test Files

- **`test_main.py`** - Basic functionality tests demonstrating pytest features
- **`test_security.py`** - Security-focused tests (input validation, XSS, SQL injection prevention, etc.)
- **`test_utils.py`** - Utility function tests with fixtures
- **`conftest.py`** - Shared pytest fixtures and configuration
- **`__init__.py`** - Package initialization

## Running Tests

### Run all tests
```bash
pytest
```

### Run with verbose output
```bash
pytest -v
```

### Run specific test file
```bash
pytest tests/test_security.py
```

### Run specific test
```bash
pytest tests/test_main.py::test_addition
```

### Run with coverage
```bash
pytest --cov=. --cov-report=html
```

## Test Statistics

- **Total Tests:** 29
- **Test Files:** 3
- **Coverage Areas:**
  - Basic functionality (13 tests)
  - Security testing (7 tests)
  - Utility functions (9 tests)

## Test Categories

### Basic Tests (`test_main.py`)
- Simple assertions
- String/list/dict operations
- Class-based tests
- Parametrized tests
- Exception handling

### Security Tests (`test_security.py`)
- Hardcoded secrets detection
- Input validation
- SQL injection prevention
- XSS prevention
- Path traversal prevention
- Password strength validation
- Session timeout logic

### Utility Tests (`test_utils.py`)
- Data validation
- String utilities
- List chunking
- Dictionary merging
- Fixture usage examples

## Fixtures

Available fixtures (defined in `conftest.py`):

- **`sample_data`** - Provides sample test data dictionary
- **`temp_file`** - Creates a temporary file for testing
- **`session_data`** - Session-scoped data shared across tests

## Best Practices

✅ **DO:**
- Write descriptive test names
- Use fixtures for reusable test data
- Test edge cases and error conditions
- Keep tests independent
- Use parametrize for similar test cases

❌ **DON'T:**
- Hardcode secrets in tests
- Create tests with external dependencies
- Write tests that depend on execution order
- Skip security-related tests
