"""
Tests for helper functions and utilities in the vulnerable views.
"""
import pytest
from badguys.vulnerable.views import norm


class TestHelperFunctions:
    """Tests for utility functions used in views."""

    def test_norm_strips_whitespace(self):
        """Test that norm() strips leading and trailing whitespace."""
        assert norm('  test  ') == 'test'
        assert norm('\ttest\n') == 'test'

    def test_norm_removes_spaces(self):
        """Test that norm() removes all spaces."""
        assert norm('hello world') == 'helloworld'
        assert norm('a b c d') == 'abcd'

    def test_norm_converts_to_lowercase(self):
        """Test that norm() converts to lowercase."""
        assert norm('HELLO') == 'hello'
        assert norm('HeLLo WoRLd') == 'helloworld'

    def test_norm_combined_operations(self):
        """Test that norm() performs all operations together."""
        assert norm('  HELLO WORLD  ') == 'helloworld'
        assert norm('\t Test String \n') == 'teststring'

    def test_norm_empty_string(self):
        """Test that norm() handles empty strings."""
        assert norm('') == ''
        assert norm('   ') == ''

    def test_norm_special_characters(self):
        """Test that norm() preserves special characters."""
        assert norm("'; DROP TABLE") == "';droptable"
        assert norm('<script>alert(1)</script>') == '<script>alert(1)</script>'


@pytest.mark.django_db
class TestViewContextData:
    """Tests for context data passed to templates."""

    def test_sql_injection_context(self, client):
        """Test SQL injection view passes correct context."""
        response = client.post('/injection/sql', {'name': 'test'})
        assert 'name' in response.context
        assert 'correct' in response.context
        assert 'solution_sql' in response.context

    def test_xss_form_context(self, client):
        """Test XSS form view passes correct context."""
        response = client.get('/cross-site-scripting/form-field', {'qs': 'test'})
        assert 'qs' in response.context
        assert response.context['qs'] == 'test'

    def test_xss_path_context(self, client):
        """Test XSS path view passes correct context."""
        response = client.get('/cross-site-scripting/path-matching/testpath')
        assert 'path' in response.context
        assert response.context['path'] == 'testpath'

    def test_xss_query_context(self, client):
        """Test XSS query view passes correct context."""
        response = client.get('/cross-site-scripting/query-params', {'qs': 'query'})
        assert 'qs' in response.context
        assert response.context['qs'] == 'query'

    def test_dor_user_profile_context(self, client):
        """Test direct object reference view passes correct context."""
        response = client.get('/direct-object-references/users/1')
        assert 'user_data' in response.context
        assert 'user_id' in response.context
        assert response.context['user_id'] == '1'

    def test_csrf_image_context(self, client):
        """Test CSRF image view passes correct context."""
        response = client.get('/csrf/image', {'qs': 'test'})
        assert 'qs' in response.context


@pytest.mark.django_db
class TestResponseHeaders:
    """Tests for HTTP response headers."""

    def test_xss_form_sets_cookie(self, client):
        """Test that XSS form view sets the monster cookie."""
        response = client.get('/cross-site-scripting/form-field')
        assert 'monster' in response.cookies
        assert response.cookies['monster'].value == 'omnomnomnomnom!'

    def test_content_type_for_images(self, client):
        """Test that user-pic returns correct content type for images."""
        response = client.get('/user-pic', {'p': 'hacker.jpg'})
        if response.status_code == 200 and len(response.content) > 100:
            # If the image was successfully loaded
            assert 'image' in response['Content-Type']

    def test_content_type_for_html(self, client):
        """Test that HTML pages return correct content type."""
        response = client.get('/')
        assert response.status_code == 200
        assert 'text/html' in response['Content-Type']


@pytest.mark.django_db
class TestHTTPMethods:
    """Tests for HTTP method handling."""

    def test_sql_injection_accepts_get(self, client):
        """Test SQL injection view accepts GET requests."""
        response = client.get('/injection/sql')
        assert response.status_code == 200

    def test_sql_injection_accepts_post(self, client):
        """Test SQL injection view accepts POST requests."""
        response = client.post('/injection/sql', {'name': 'test'})
        assert response.status_code == 200

    def test_code_execution_get_vs_post(self, client):
        """Test code execution view behaves differently for GET vs POST."""
        get_response = client.get('/injection/code-execution')
        post_response = client.post('/injection/code-execution', {'first_name': 'test'})
        
        assert get_response.status_code == 200
        assert post_response.status_code == 200
        # POST should process the data
        assert 'first_name' in post_response.context

    def test_dor_profile_get_vs_post(self, client):
        """Test direct object reference view handles GET and POST differently."""
        get_response = client.get('/direct-object-references/users/1')
        assert get_response.status_code == 200
        assert 'updated' not in get_response.context or not get_response.context.get('updated')
        
        post_response = client.post(
            '/direct-object-references/users/1',
            {'name': 'New Name', 'email': 'new@example.com'}
        )
        assert post_response.status_code == 200
        assert post_response.context.get('updated') is True


@pytest.mark.django_db
class TestErrorHandling:
    """Tests for error handling in views."""

    def test_user_pic_handles_missing_file(self, client):
        """Test user-pic handles missing files gracefully."""
        response = client.get('/user-pic', {'p': 'nonexistent.jpg'})
        assert response.status_code == 200
        # Should return HTML with error message, not crash

    def test_user_pic_handles_none_parameter(self, client):
        """Test user-pic handles None parameter."""
        response = client.get('/user-pic')
        assert response.status_code == 200

    def test_unvalidated_forward_handles_invalid_function(self, client):
        """Test unvalidated forward handles invalid function names."""
        response = client.get('/redirects-and-forwards/forward', {'fwd': 'invalid_function'})
        assert response.status_code == 200
        # Should show error page, not crash

    def test_dor_handles_invalid_user_id(self, client):
        """Test direct object reference handles invalid user IDs."""
        response = client.get('/direct-object-references/users/999')
        assert response.status_code == 200
        # Should handle None user_data gracefully


@pytest.mark.django_db
class TestDefaultValues:
    """Tests for default values in views."""

    def test_xss_form_default_query_string(self, client):
        """Test XSS form uses default value when no query string."""
        response = client.get('/cross-site-scripting/form-field')
        assert response.status_code == 200
        assert response.context['qs'] == 'hello'

    def test_xss_query_default_query_string(self, client):
        """Test XSS query uses default value when no query string."""
        response = client.get('/cross-site-scripting/query-params')
        assert response.status_code == 200
        assert response.context['qs'] == 'hello'

    def test_xss_path_default_path(self, client):
        """Test XSS path uses path parameter."""
        response = client.get('/cross-site-scripting/path-matching/default')
        assert response.status_code == 200
        assert response.context['path'] == 'default'

    def test_file_access_default_message(self, client):
        """Test file access uses empty default message."""
        response = client.get('/injection/file-access')
        assert response.status_code == 200
        assert response.context['msg'] == ''

    def test_csrf_image_default_query_string(self, client):
        """Test CSRF image uses empty default query string."""
        response = client.get('/csrf/image')
        assert response.status_code == 200
        assert response.context['qs'] == ''

