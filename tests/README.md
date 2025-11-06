# Test Suite for Let's Be Bad Guys

This directory contains comprehensive tests for the deliberately vulnerable Django application.

## Test Structure

The test suite is organized into the following modules:

- **`test_injection.py`** - Tests for injection vulnerabilities (SQL, file access, code execution)
- **`test_xss.py`** - Tests for Cross-Site Scripting (XSS) vulnerabilities
- **`test_vulnerabilities.py`** - Tests for CSRF, access control, redirects, and other vulnerabilities
- **`test_urls.py`** - Tests for URL patterns and routing

## Running Tests

### Install Dependencies

First, make sure you have pytest and related dependencies installed:

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=badguys --cov-report=html
```

This will generate an HTML coverage report in the `htmlcov/` directory.

### Run Specific Test Files

```bash
pytest tests/test_injection.py
pytest tests/test_xss.py
pytest tests/test_vulnerabilities.py
pytest tests/test_urls.py
```

### Run Tests by Marker

Tests are organized with markers for easy filtering:

```bash
# Run only injection tests
pytest -m injection

# Run only XSS tests
pytest -m xss

# Run only CSRF tests
pytest -m csrf

# Run only access control tests
pytest -m access_control

# Run only redirect tests
pytest -m redirects
```

### Run Specific Test Classes or Methods

```bash
# Run a specific test class
pytest tests/test_injection.py::TestSQLInjection

# Run a specific test method
pytest tests/test_injection.py::TestSQLInjection::test_sql_injection_post_correct_payload
```

### Verbose Output

```bash
pytest -v
pytest -vv  # Extra verbose
```

### Show Print Statements

```bash
pytest -s
```

## Test Configuration

Test configuration is managed in `pytest.ini` at the project root. Key settings include:

- Django settings module: `badguys.settings`
- Coverage reporting enabled by default
- Custom markers for test categorization

## Fixtures

Common test fixtures are defined in `conftest.py` at the project root:

- `client` - Django test client
- `admin_user` - Admin user instance
- `regular_user` - Regular user instance
- `authenticated_client` - Client logged in as regular user
- `admin_client` - Client logged in as admin

## Writing New Tests

When adding new tests:

1. Use appropriate markers (`@pytest.mark.injection`, `@pytest.mark.xss`, etc.)
2. Use descriptive test names that explain what is being tested
3. Include docstrings explaining the test purpose
4. Use the Django test client fixture for making requests
5. Assert both status codes and content where appropriate

Example:

```python
@pytest.mark.django_db
@pytest.mark.injection
class TestNewVulnerability:
    """Tests for new vulnerability."""

    def test_vulnerability_exploited(self, client):
        """Test that the vulnerability can be exploited."""
        response = client.get(reverse('vulnerable-endpoint'))
        assert response.status_code == 200
        assert b'expected content' in response.content
```

## Important Notes

⚠️ **Security Warning**: These tests verify that vulnerabilities exist and can be exploited. This is intentional for educational purposes. Do not use these patterns in production code!

The tests in this suite:
- Verify that vulnerabilities are present and exploitable
- Test both vulnerable and edge case behaviors
- Ensure the application responds correctly to various inputs
- Provide examples of how attacks work

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=badguys --cov-report=xml
```

## Coverage Goals

The test suite aims for high coverage of:
- All view functions
- URL routing
- Request handling (GET, POST)
- Edge cases and error conditions
- Vulnerability exploitation scenarios

