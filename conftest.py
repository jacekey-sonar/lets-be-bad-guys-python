"""
Pytest configuration and fixtures for the badguys project.
"""
import pytest
from django.test import Client
from django.contrib.auth.models import User


@pytest.fixture
def client():
    """Django test client fixture."""
    return Client()


@pytest.fixture
def admin_user(db):
    """Create an admin user for testing."""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )


@pytest.fixture
def regular_user(db):
    """Create a regular user for testing."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='test123'
    )


@pytest.fixture
def authenticated_client(client, regular_user):
    """Client authenticated as a regular user."""
    client.login(username='testuser', password='test123')
    return client


@pytest.fixture
def admin_client(client, admin_user):
    """Client authenticated as an admin user."""
    client.login(username='admin', password='admin123')
    return client

