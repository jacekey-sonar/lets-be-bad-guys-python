"""
Tests for Cross-Site Scripting (XSS) vulnerability views.
"""
import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.xss
class TestXSSForm:
    """Tests for XSS via form field vulnerability."""

    def test_xss_form_get_request(self, client):
        """Test XSS form page loads with GET request."""
        response = client.get(reverse('xss-form'))
        assert response.status_code == 200

    def test_xss_form_with_normal_input(self, client):
        """Test XSS form with normal query string."""
        response = client.get(reverse('xss-form'), {'qs': 'hello world'})
        assert response.status_code == 200
        assert b'hello world' in response.content

    def test_xss_form_with_script_tag(self, client):
        """Test XSS form with script tag in query string."""
        xss_payload = '<script>alert("XSS")</script>'
        response = client.get(reverse('xss-form'), {'qs': xss_payload})
        assert response.status_code == 200
        # The payload should be in the response (demonstrating vulnerability)
        assert xss_payload.encode() in response.content

    def test_xss_form_with_html_injection(self, client):
        """Test XSS form with HTML injection."""
        xss_payload = '<img src=x onerror=alert(1)>'
        response = client.get(reverse('xss-form'), {'qs': xss_payload})
        assert response.status_code == 200
        assert b'<img' in response.content

    def test_xss_form_sets_cookie(self, client):
        """Test that XSS form sets a cookie."""
        response = client.get(reverse('xss-form'))
        assert response.status_code == 200
        assert 'monster' in response.cookies
        assert response.cookies['monster'].value == 'omnomnomnomnom!'

    def test_xss_form_default_value(self, client):
        """Test XSS form with default value when no query string."""
        response = client.get(reverse('xss-form'))
        assert response.status_code == 200
        assert b'hello' in response.content

    def test_xss_form_with_special_characters(self, client):
        """Test XSS form with special characters."""
        special_chars = '"><script>alert(document.cookie)</script>'
        response = client.get(reverse('xss-form'), {'qs': special_chars})
        assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.xss
class TestXSSPath:
    """Tests for XSS via path parameter vulnerability."""

    def test_xss_path_with_default(self, client):
        """Test XSS path with default value."""
        response = client.get(reverse('xss-path', kwargs={'path': 'default'}))
        assert response.status_code == 200
        assert b'default' in response.content

    def test_xss_path_with_normal_input(self, client):
        """Test XSS path with normal input."""
        response = client.get(reverse('xss-path', kwargs={'path': 'test/path'}))
        assert response.status_code == 200
        assert b'test/path' in response.content

    def test_xss_path_with_script_tag(self, client):
        """Test XSS path with script tag."""
        xss_payload = '<script>alert("XSS")</script>'
        response = client.get(reverse('xss-path', kwargs={'path': xss_payload}))
        assert response.status_code == 200
        # The payload should be reflected in the response
        assert b'<script>' in response.content

    def test_xss_path_with_encoded_payload(self, client):
        """Test XSS path with URL encoded payload."""
        # Test with a payload that might be URL encoded
        response = client.get(reverse('xss-path', kwargs={'path': 'test<>'}))
        assert response.status_code == 200

    def test_xss_path_with_slashes(self, client):
        """Test XSS path handles multiple slashes."""
        response = client.get(reverse('xss-path', kwargs={'path': 'path/with/slashes'}))
        assert response.status_code == 200
        assert b'path/with/slashes' in response.content


@pytest.mark.django_db
@pytest.mark.xss
class TestXSSQuery:
    """Tests for XSS via query parameter vulnerability."""

    def test_xss_query_get_request(self, client):
        """Test XSS query page loads with GET request."""
        response = client.get(reverse('xss-query'))
        assert response.status_code == 200

    def test_xss_query_with_default_value(self, client):
        """Test XSS query with default value when no query string."""
        response = client.get(reverse('xss-query'))
        assert response.status_code == 200
        assert b'hello' in response.content

    def test_xss_query_with_normal_input(self, client):
        """Test XSS query with normal query string."""
        response = client.get(reverse('xss-query'), {'qs': 'test query'})
        assert response.status_code == 200
        assert b'test query' in response.content

    def test_xss_query_with_script_tag(self, client):
        """Test XSS query with script tag."""
        xss_payload = '<script>alert("XSS")</script>'
        response = client.get(reverse('xss-query'), {'qs': xss_payload})
        assert response.status_code == 200
        assert xss_payload.encode() in response.content

    def test_xss_query_with_event_handler(self, client):
        """Test XSS query with event handler."""
        xss_payload = '<img src=x onerror=alert(1)>'
        response = client.get(reverse('xss-query'), {'qs': xss_payload})
        assert response.status_code == 200
        assert b'onerror' in response.content

    def test_xss_query_with_javascript_protocol(self, client):
        """Test XSS query with javascript: protocol."""
        xss_payload = '<a href="javascript:alert(1)">click</a>'
        response = client.get(reverse('xss-query'), {'qs': xss_payload})
        assert response.status_code == 200

    def test_xss_query_with_svg_payload(self, client):
        """Test XSS query with SVG-based payload."""
        xss_payload = '<svg onload=alert(1)>'
        response = client.get(reverse('xss-query'), {'qs': xss_payload})
        assert response.status_code == 200
        assert b'<svg' in response.content

    def test_xss_query_with_empty_string(self, client):
        """Test XSS query with empty string."""
        response = client.get(reverse('xss-query'), {'qs': ''})
        assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.xss
class TestXSSIndex:
    """Tests for XSS index page."""

    def test_xss_index_page_loads(self, client):
        """Test XSS index page loads successfully."""
        response = client.get(reverse('xss'))
        assert response.status_code == 200
        assert b'cross-site scripting' in response.content.lower() or b'xss' in response.content.lower()

