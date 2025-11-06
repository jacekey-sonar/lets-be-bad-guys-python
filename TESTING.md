# Testing Guide for Let's Be Bad Guys

This document provides comprehensive information about the test suite for this deliberately vulnerable Django application.

## Quick Start

### 1. Install Dependencies

Make sure you're in your virtual environment, then install the test dependencies:

```bash
# Activate your virtual environment first
source bin/activate  # or 'Scripts/activate.bat' on Windows

# Install dependencies
pip install -r requirements.txt
```

The following testing packages will be installed:
- `pytest==7.4.3` - Testing framework
- `pytest-django==4.7.0` - Django integration for pytest
- `pytest-cov==4.1.0` - Coverage reporting

### 2. Run Tests

#### Option A: Use the Test Runner Script (Recommended)

```bash
./run_tests.sh
```

This script will:
- Check if you're in a virtual environment
- Install dependencies if needed
- Run all tests with coverage reporting
- Generate an HTML coverage report

#### Option B: Run pytest Directly

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=badguys --cov-report=html
```

## Test Organization

The test suite is organized into four main modules:

### 1. `tests/test_injection.py`
Tests for injection vulnerabilities including:
- SQL Injection (`TestSQLInjection`)
- File Access Injection (`TestFileAccessInjection`)
- Code Execution Injection (`TestCodeExecutionInjection`)

**Example tests:**
- Verifying SQL injection payloads are recognized
- Testing directory traversal attempts
- Validating code execution via base64 payloads

### 2. `tests/test_xss.py`
Tests for Cross-Site Scripting vulnerabilities:
- XSS via Form Fields (`TestXSSForm`)
- XSS via Path Parameters (`TestXSSPath`)
- XSS via Query Parameters (`TestXSSQuery`)

**Example tests:**
- Script tag injection
- HTML event handler injection
- SVG-based XSS payloads

### 3. `tests/test_vulnerabilities.py`
Tests for various other vulnerabilities:
- CSRF (`TestCSRF`)
- Access Control (`TestAccessControl`)
- Redirects and Forwards (`TestRedirectsAndForwards`)
- Direct Object References (`TestDirectObjectReferences`)
- Security Misconfiguration (`TestSecurityMisconfiguration`)
- Data Exposure (`TestDataExposure`)
- Broken Authentication (`TestBrokenAuth`)
- Vulnerable Components (`TestVulnerableComponents`)

### 4. `tests/test_urls.py`
Tests for URL patterns and routing:
- Main page URLs
- URL resolution
- Static file serving
- URL pattern validation

## Running Specific Tests

### By Test File

```bash
pytest tests/test_injection.py
pytest tests/test_xss.py
pytest tests/test_vulnerabilities.py
pytest tests/test_urls.py
```

### By Test Class

```bash
pytest tests/test_injection.py::TestSQLInjection
pytest tests/test_xss.py::TestXSSForm
pytest tests/test_vulnerabilities.py::TestCSRF
```

### By Test Method

```bash
pytest tests/test_injection.py::TestSQLInjection::test_sql_injection_post_correct_payload
pytest tests/test_xss.py::TestXSSForm::test_xss_form_with_script_tag
```

### By Marker

Tests are tagged with markers for easy filtering:

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

### Combine Markers

```bash
# Run injection OR xss tests
pytest -m "injection or xss"

# Run all except slow tests
pytest -m "not slow"
```

## Test Output Options

### Verbose Output

```bash
# Show test names
pytest -v

# Extra verbose (show full test names and parameters)
pytest -vv
```

### Show Print Statements

```bash
pytest -s
```

### Short Traceback

```bash
pytest --tb=short
```

### Stop on First Failure

```bash
pytest -x
```

### Run Last Failed Tests

```bash
pytest --lf
```

## Coverage Reports

### Terminal Coverage Report

```bash
pytest --cov=badguys --cov-report=term-missing
```

This shows:
- Percentage of code covered
- Line numbers that are missing coverage

### HTML Coverage Report

```bash
pytest --cov=badguys --cov-report=html
```

Then open `htmlcov/index.html` in your browser to see:
- Interactive coverage visualization
- Line-by-line coverage details
- Coverage statistics per file

### XML Coverage Report (for CI/CD)

```bash
pytest --cov=badguys --cov-report=xml
```

Generates `coverage.xml` for use with CI/CD tools.

## Test Fixtures

The test suite uses several fixtures defined in `conftest.py`:

### `client`
Django test client for making HTTP requests.

```python
def test_example(client):
    response = client.get('/some-url/')
    assert response.status_code == 200
```

### `admin_user`
Creates an admin user in the test database.

```python
def test_with_admin(admin_user):
    assert admin_user.is_superuser
```

### `regular_user`
Creates a regular (non-admin) user.

```python
def test_with_user(regular_user):
    assert not regular_user.is_superuser
```

### `authenticated_client`
Client logged in as a regular user.

```python
def test_authenticated(authenticated_client):
    response = authenticated_client.get('/profile/')
    assert response.status_code == 200
```

### `admin_client`
Client logged in as an admin user.

```python
def test_admin_access(admin_client):
    response = admin_client.get('/admin-panel/')
    assert response.status_code == 200
```

## Writing New Tests

### Test Structure

```python
import pytest
from django.urls import reverse

@pytest.mark.django_db
@pytest.mark.injection  # Use appropriate marker
class TestNewFeature:
    """Tests for new feature."""

    def test_feature_works(self, client):
        """Test that the feature works as expected."""
        response = client.get(reverse('feature-url'))
        assert response.status_code == 200
        assert b'expected content' in response.content
```

### Best Practices

1. **Use descriptive names**: Test names should explain what they test
2. **Add docstrings**: Explain the purpose of each test
3. **Use markers**: Tag tests with appropriate markers
4. **Test both success and failure**: Include edge cases
5. **Use fixtures**: Leverage existing fixtures for common setup
6. **Assert multiple things**: Check status codes, content, context variables
7. **Clean up**: Remove any files created during tests

### Example Test

```python
@pytest.mark.django_db
@pytest.mark.xss
class TestNewXSSVector:
    """Tests for a new XSS attack vector."""

    def test_xss_in_header(self, client):
        """Test XSS vulnerability in custom header."""
        xss_payload = '<script>alert("XSS")</script>'
        response = client.get(
            reverse('vulnerable-page'),
            HTTP_X_CUSTOM_HEADER=xss_payload
        )
        assert response.status_code == 200
        # Verify the payload is reflected (vulnerability exists)
        assert xss_payload.encode() in response.content
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest --cov=badguys --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml
```

### GitLab CI Example

```yaml
test:
  image: python:3.9
  script:
    - pip install -r requirements.txt
    - pytest --cov=badguys --cov-report=term
  coverage: '/TOTAL.*\s+(\d+%)$/'
```

## Troubleshooting

### Tests Fail to Import Django

**Problem**: `ImportError: No module named django`

**Solution**: Make sure dependencies are installed:
```bash
pip install -r requirements.txt
```

### Database Errors

**Problem**: `django.db.utils.OperationalError`

**Solution**: Tests use an in-memory SQLite database. Make sure `@pytest.mark.django_db` is on your test class or method.

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'badguys'`

**Solution**: Make sure you're running pytest from the project root directory.

### Coverage Not Working

**Problem**: Coverage report shows 0%

**Solution**: Make sure you're using the correct coverage command:
```bash
pytest --cov=badguys --cov-report=term
```

## Performance Tips

### Run Tests in Parallel

Install pytest-xdist:
```bash
pip install pytest-xdist
```

Run tests in parallel:
```bash
pytest -n auto
```

### Skip Slow Tests

Mark slow tests:
```python
@pytest.mark.slow
def test_slow_operation(client):
    # ...
```

Skip them during development:
```bash
pytest -m "not slow"
```

## Test Statistics

Current test coverage:

- **Total Tests**: 100+ test methods
- **Test Files**: 4 modules
- **Coverage Target**: >80% line coverage
- **Test Categories**:
  - Injection: 20+ tests
  - XSS: 20+ tests
  - CSRF: 6+ tests
  - Access Control: 4+ tests
  - Redirects: 10+ tests
  - Other: 40+ tests

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

## Security Note

⚠️ **Important**: These tests verify that vulnerabilities exist and can be exploited. This is intentional for educational purposes. The patterns demonstrated here should **NEVER** be used in production applications. Always follow secure coding practices in real-world projects.

