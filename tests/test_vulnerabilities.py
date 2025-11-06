"""
Tests for various vulnerability views (CSRF, Access Control, Redirects, etc.).
"""
import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.csrf
class TestCSRF:
    """Tests for CSRF vulnerability views."""

    def test_csrf_index_page_loads(self, client):
        """Test CSRF index page loads."""
        response = client.get(reverse('csrf'))
        assert response.status_code == 200

    def test_csrf_image_get_request(self, client):
        """Test CSRF image page with GET request."""
        response = client.get(reverse('csrf-image'))
        assert response.status_code == 200

    def test_csrf_image_with_query_string(self, client):
        """Test CSRF image page with query string."""
        response = client.get(reverse('csrf-image'), {'qs': 'test'})
        assert response.status_code == 200
        assert b'test' in response.content

    def test_csrf_image_post_request(self, client):
        """Test CSRF image accepts POST without token (vulnerable)."""
        # This should work because @csrf_exempt is used
        response = client.post(reverse('csrf-image'), {'qs': 'posted'})
        assert response.status_code == 200

    def test_csrf_third_party_page(self, client):
        """Test CSRF third party page loads."""
        response = client.get(reverse('csrf-third-party'))
        assert response.status_code == 200

    def test_csrf_gift_card_page(self, client):
        """Test CSRF gift card page loads."""
        response = client.get(reverse('csrf-gift-card'))
        assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.access_control
class TestAccessControl:
    """Tests for access control vulnerability views."""

    def test_access_control_index_page(self, client):
        """Test access control index page loads."""
        response = client.get(reverse('access-control'))
        assert response.status_code == 200

    def test_missing_access_control_non_admin(self, client):
        """Test missing access control shows non-admin page by default."""
        response = client.get(reverse('access-control-missing'))
        assert response.status_code == 200
        # Should show non-admin page
        assert b'non_admin' in response.content or b'non-admin' in response.content

    def test_missing_access_control_admin_action(self, client):
        """Test missing access control with admin action parameter."""
        response = client.get(reverse('access-control-missing'), {'action': 'admin'})
        assert response.status_code == 200
        # Should show admin page (vulnerability!)
        assert b'admin' in response.content

    def test_missing_access_control_invalid_action(self, client):
        """Test missing access control with invalid action."""
        response = client.get(reverse('access-control-missing'), {'action': 'invalid'})
        assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.redirects
class TestRedirectsAndForwards:
    """Tests for unvalidated redirects and forwards vulnerabilities."""

    def test_redirects_index_page(self, client):
        """Test redirects index page loads."""
        response = client.get(reverse('redirects'))
        assert response.status_code == 200

    def test_redirects_page(self, client):
        """Test redirects information page loads."""
        response = client.get(reverse('redirects-redirects'))
        assert response.status_code == 200

    def test_forwards_page(self, client):
        """Test forwards information page loads."""
        response = client.get(reverse('redirects-forwards'))
        assert response.status_code == 200

    def test_unvalidated_redirect_internal(self, client):
        """Test unvalidated redirect with internal URL."""
        response = client.get(reverse('redirects-redirect'), {'url': '/'})
        assert response.status_code == 302
        assert response.url == '/'

    def test_unvalidated_redirect_external(self, client):
        """Test unvalidated redirect with external URL (vulnerability)."""
        external_url = 'http://evil.com'
        response = client.get(reverse('redirects-redirect'), {'url': external_url})
        assert response.status_code == 302
        assert response.url == external_url

    def test_unvalidated_redirect_no_url(self, client):
        """Test unvalidated redirect without URL parameter."""
        response = client.get(reverse('redirects-redirect'))
        # Should handle None gracefully
        assert response.status_code in [302, 400, 500]

    def test_unvalidated_forward_valid_function(self, client):
        """Test unvalidated forward with valid function name."""
        response = client.get(reverse('redirects-forward'), {'fwd': 'admin'})
        assert response.status_code == 200
        # Should forward to admin function
        assert b'admin' in response.content

    def test_unvalidated_forward_invalid_function(self, client):
        """Test unvalidated forward with invalid function name."""
        response = client.get(reverse('redirects-forward'), {'fwd': 'nonexistent'})
        assert response.status_code == 200
        # Should show forward failed page
        assert b'nonexistent' in response.content or b'failed' in response.content.lower()

    def test_unvalidated_forward_no_parameter(self, client):
        """Test unvalidated forward without parameter."""
        response = client.get(reverse('redirects-forward'))
        assert response.status_code == 200

    def test_admin_page_directly(self, client):
        """Test accessing admin page directly."""
        response = client.get(reverse('redirects-forward'), {'fwd': 'admin'})
        assert response.status_code == 200


@pytest.mark.django_db
class TestDirectObjectReferences:
    """Tests for insecure direct object references vulnerability."""

    def test_dor_index_page(self, client):
        """Test direct object references index page loads."""
        response = client.get(reverse('direct-object-references'))
        assert response.status_code == 200

    def test_dor_user_profile_user_1(self, client):
        """Test accessing user 1 profile."""
        response = client.get(reverse('direct-object-references-profile', kwargs={'userid': '1'}))
        assert response.status_code == 200
        assert b'Foo' in response.content
        assert b'foo@example.com' in response.content

    def test_dor_user_profile_user_2(self, client):
        """Test accessing user 2 profile (admin user)."""
        response = client.get(reverse('direct-object-references-profile', kwargs={'userid': '2'}))
        assert response.status_code == 200
        assert b'Bar' in response.content
        assert b'bar@example.com' in response.content

    def test_dor_user_profile_update_post(self, client):
        """Test updating user profile via POST."""
        response = client.post(
            reverse('direct-object-references-profile', kwargs={'userid': '1'}),
            {'name': 'Updated Name', 'email': 'updated@example.com'}
        )
        assert response.status_code == 200
        assert b'Updated Name' in response.content
        assert b'updated@example.com' in response.content
        assert response.context['updated'] is True

    def test_dor_user_profile_partial_update(self, client):
        """Test partial update of user profile."""
        response = client.post(
            reverse('direct-object-references-profile', kwargs={'userid': '1'}),
            {'name': 'New Name'}
        )
        assert response.status_code == 200
        assert b'New Name' in response.content

    def test_dor_invalid_user_id(self, client):
        """Test accessing profile with invalid user ID."""
        response = client.get(reverse('direct-object-references-profile', kwargs={'userid': '999'}))
        assert response.status_code == 200
        # Should handle None user_data


@pytest.mark.django_db
class TestSecurityMisconfiguration:
    """Tests for security misconfiguration vulnerabilities."""

    def test_misconfig_index_page(self, client):
        """Test misconfiguration index page loads."""
        response = client.get(reverse('misconfig'))
        assert response.status_code == 200

    def test_boom_raises_exception(self, client):
        """Test that boom endpoint raises an exception."""
        with pytest.raises(Exception) as exc_info:
            client.get(reverse('misconfig-boom'))
        assert str(exc_info.value) == 'boom'


@pytest.mark.django_db
class TestDataExposure:
    """Tests for sensitive data exposure vulnerabilities."""

    def test_exposure_index_page(self, client):
        """Test data exposure index page loads."""
        response = client.get(reverse('exposure'))
        assert response.status_code == 200

    def test_exposure_login_redirects(self, client):
        """Test exposure login redirects to exposure page."""
        response = client.get(reverse('exposure-login'))
        assert response.status_code == 302
        assert response.url == reverse('exposure')


@pytest.mark.django_db
class TestBrokenAuth:
    """Tests for broken authentication and session management."""

    def test_broken_auth_index_page(self, client):
        """Test broken auth index page loads."""
        response = client.get(reverse('broken-auth'))
        assert response.status_code == 200


@pytest.mark.django_db
class TestVulnerableComponents:
    """Tests for using known vulnerable components."""

    def test_components_index_page(self, client):
        """Test vulnerable components index page loads."""
        response = client.get(reverse('components'))
        assert response.status_code == 200

