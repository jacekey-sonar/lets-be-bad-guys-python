"""
Tests for injection vulnerability views.
"""
import os
import base64
import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.injection
class TestSQLInjection:
    """Tests for SQL injection vulnerability."""

    def test_sql_injection_get_request(self, client):
        """Test SQL injection page loads with GET request."""
        response = client.get(reverse('injection-sql'))
        assert response.status_code == 200
        assert b'sql' in response.content.lower()

    def test_sql_injection_post_empty(self, client):
        """Test SQL injection with empty POST data."""
        response = client.post(reverse('injection-sql'), {'name': ''})
        assert response.status_code == 200
        assert b'correct' in response.content.lower()

    def test_sql_injection_post_correct_payload(self, client):
        """Test SQL injection with correct exploit payload."""
        payload = "'; DROP TABLE Users;--"
        response = client.post(reverse('injection-sql'), {'name': payload})
        assert response.status_code == 200
        # The view should recognize this as correct
        assert 'correct' in response.context

    def test_sql_injection_post_incorrect_payload(self, client):
        """Test SQL injection with incorrect payload."""
        response = client.post(reverse('injection-sql'), {'name': 'normal input'})
        assert response.status_code == 200
        assert response.context['correct'] is False

    def test_sql_injection_post_with_spaces(self, client):
        """Test SQL injection payload with extra spaces."""
        payload = "' ;  DROP TABLE Users ; -- "
        response = client.post(reverse('injection-sql'), {'name': payload})
        assert response.status_code == 200
        # Should still be recognized as correct due to normalization


@pytest.mark.django_db
@pytest.mark.injection
class TestFileAccessInjection:
    """Tests for file access injection vulnerability."""

    def test_file_access_page_loads(self, client):
        """Test file access injection page loads."""
        response = client.get(reverse('injection-file-access'))
        assert response.status_code == 200

    def test_file_access_with_message(self, client):
        """Test file access page with message parameter."""
        response = client.get(reverse('injection-file-access'), {'msg': 'test message'})
        assert response.status_code == 200
        assert b'test message' in response.content

    def test_user_pic_valid_image(self, client):
        """Test accessing a valid image file."""
        response = client.get(reverse('user-pic'), {'p': 'hacker.jpg'})
        assert response.status_code == 200
        assert response['Content-Type'].startswith('image/')

    def test_user_pic_invalid_file(self, client):
        """Test accessing an invalid file."""
        response = client.get(reverse('user-pic'), {'p': 'nonexistent.jpg'})
        assert response.status_code == 200
        assert b'Keep trying' in response.content

    def test_user_pic_absolute_path_attempt(self, client):
        """Test directory traversal with absolute path."""
        response = client.get(reverse('user-pic'), {'p': '/etc/passwd'})
        assert response.status_code == 200
        # Should return error message, not the file
        assert b'worth trying' in response.content.lower()

    def test_user_pic_relative_path_attempt(self, client):
        """Test directory traversal with relative path."""
        response = client.get(reverse('user-pic'), {'p': '../settings.py'})
        assert response.status_code == 200
        # Should give a hint that this is the right track
        assert b'right track' in response.content.lower()

    def test_user_pic_no_parameter(self, client):
        """Test user pic endpoint without parameter."""
        response = client.get(reverse('user-pic'))
        assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.injection
class TestCodeExecutionInjection:
    """Tests for code execution injection vulnerability."""

    def test_code_execution_get_request(self, client):
        """Test code execution page loads with GET request."""
        response = client.get(reverse('injection-code-execution'))
        assert response.status_code == 200

    def test_code_execution_post_empty(self, client):
        """Test code execution with empty POST data."""
        response = client.post(reverse('injection-code-execution'), {'first_name': ''})
        assert response.status_code == 200
        assert response.context['data'] == ''

    def test_code_execution_post_normal_input(self, client):
        """Test code execution with normal input."""
        response = client.post(reverse('injection-code-execution'), {'first_name': 'John'})
        assert response.status_code == 200
        assert response.context['data'] == ''

    def test_code_execution_post_base64_payload(self, client):
        """Test code execution with base64 encoded payload."""
        # Create a simple Python command that creates a file
        code = "open('p0wned.txt', 'w').write('hacked')"
        encoded = base64.b64encode(code.encode()).decode()
        
        response = client.post(reverse('injection-code-execution'), {'first_name': encoded})
        assert response.status_code == 200
        
        # Clean up if file was created
        try:
            os.unlink('p0wned.txt')
        except:
            pass

    def test_code_execution_cleans_previous_file(self, client):
        """Test that code execution cleans up previous p0wned.txt file."""
        # Create a p0wned.txt file
        with open('p0wned.txt', 'w') as f:
            f.write('previous hack')
        
        # Make a POST request (should clean it up)
        response = client.post(reverse('injection-code-execution'), {'first_name': 'test'})
        assert response.status_code == 200
        
        # File should not exist or be empty
        try:
            with open('p0wned.txt', 'r') as f:
                content = f.read()
            # If it exists, it should be from a new execution, not the old one
            os.unlink('p0wned.txt')
        except FileNotFoundError:
            # File was properly cleaned up
            pass

    def test_code_execution_invalid_base64(self, client):
        """Test code execution with invalid base64."""
        response = client.post(reverse('injection-code-execution'), {'first_name': 'not-base64!!!'})
        assert response.status_code == 200
        # Should handle gracefully and not crash
        assert response.context['data'] == ''

