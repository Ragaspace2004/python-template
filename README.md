# Python DevSecOps Template

A production-ready Python Flask API template with comprehensive DevSecOps CI/CD pipeline.

## Features

- ✅ Flask REST API
- ✅ Automated testing with Pytest
- ✅ Code linting with Ruff
- ✅ Type checking with mypy
- ✅ Security scanning with Bandit & Semgrep
- ✅ Secret detection with Gitleaks
- ✅ Pre-commit hooks
- ✅ GitHub Actions CI/CD
- ✅ Dependency management with Dependabot

## Quick Start

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd python-template

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Running the Application

```bash
# Development mode
python main.py

# The API will be available at http://localhost:5000
```

### API Endpoints

- `GET /api/health` - Health check
- `POST /api/calculate` - Calculate total with tax
- `POST /api/validate-email` - Validate email address
- `GET /api/users/<id>` - Get user by ID

### Example Requests

```bash
# Health check
curl http://localhost:5000/api/health

# Calculate total
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "tax_rate": 0.1}'

# Validate email
curl -X POST http://localhost:5000/api/validate-email \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_routes.py
```

### Code Quality Checks

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Linting
ruff check .

# Formatting
ruff format .

# Type checking
mypy app/

# Security scan
bandit -c pyproject.toml -r .
```

## CI/CD Pipeline

### Pre-commit Hooks (Local)

Runs automatically on `git commit`:
- Trailing whitespace removal
- End-of-file fixer
- YAML validation
- Ruff linting & formatting
- mypy type checking
- Bandit security scan
- Gitleaks secret detection
- Pytest tests

### GitHub Actions (CI)

Runs on every push and PR:
- **Pre-commit CI**: All pre-commit checks
- **Semgrep**: Advanced security scanning
- **Dependabot**: Automated dependency updates

### Workflow Labels

PRs are automatically labeled:
- `pre-commit` - Pre-commit CI ran
- `semgrep` - Semgrep security scan ran
- `ci-passed` / `ci-failed` - CI status
- `security-passed` / `security-findings` - Security status

## Project Structure

```
.
├── app/
│   ├── __init__.py       # Flask app factory
│   ├── routes.py         # API routes
│   └── utils.py          # Utility functions
├── tests/
│   ├── conftest.py       # Pytest fixtures
│   ├── test_routes.py    # Route tests
│   └── test_utils.py     # Utility tests
├── .github/
│   └── workflows/        # GitHub Actions workflows
├── main.py               # Application entry point
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── pyproject.toml        # Project configuration
├── ruff.toml            # Ruff configuration
└── .pre-commit-config.yaml  # Pre-commit hooks

```

## Configuration

### Ruff (Linting & Formatting)

Configuration in `ruff.toml`:
- Line length: 100
- Target: Python 3.11
- Enabled rules: pycodestyle, Pyflakes, isort, pep8-naming, etc.

### Bandit (Security)

Configuration in `pyproject.toml`:
- Severity: MEDIUM and above
- Excludes: tests, venv
- Skips: B101 (assert in tests)

### mypy (Type Checking)

Configuration in `pyproject.toml`:
- Python version: 3.11
- Ignore missing imports
- Show error codes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and checks: `pre-commit run --all-files`
5. Commit your changes
6. Push and create a Pull Request

## Security

- All secrets should be in environment variables
- Never commit `.env` files
- Bandit scans for security issues
- Gitleaks prevents secret leaks
- Semgrep for advanced security patterns

## License

MIT License

## Support

For issues or questions, please open a GitHub issue.
