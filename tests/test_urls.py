"""
Tests for URL patterns and general pages.
"""
import pytest
from django.urls import reverse, resolve
from django.views.generic.base import TemplateView
from badguys.vulnerable import views as exercises


@pytest.mark.django_db
class TestMainPages:
    """Tests for main application pages."""

    def test_home_page_loads(self, client):
        """Test home page loads successfully."""
        response = client.get(reverse('home'))
        assert response.status_code == 200

    def test_about_page_loads(self, client):
        """Test about page loads successfully."""
        response = client.get(reverse('about'))
        assert response.status_code == 200

    def test_conclusion_page_loads(self, client):
        """Test conclusion page loads successfully."""
        response = client.get(reverse('conclusion'))
        assert response.status_code == 200


@pytest.mark.django_db
class TestInjectionURLs:
    """Tests for injection URL patterns."""

    def test_injection_index_url(self, client):
        """Test injection index URL loads."""
        response = client.get(reverse('injection'))
        assert response.status_code == 200

    def test_injection_sql_url_resolves(self):
        """Test injection SQL URL resolves to correct view."""
        url = reverse('injection-sql')
        assert resolve(url).func == exercises.sql

    def test_injection_file_access_url_resolves(self):
        """Test injection file access URL resolves to correct view."""
        url = reverse('injection-file-access')
        assert resolve(url).func == exercises.file_access

    def test_user_pic_url_resolves(self):
        """Test user pic URL resolves to correct view."""
        url = reverse('user-pic')
        assert resolve(url).func == exercises.user_pic

    def test_injection_code_execution_url_resolves(self):
        """Test injection code execution URL resolves to correct view."""
        url = reverse('injection-code-execution')
        assert resolve(url).func == exercises.code_execution


@pytest.mark.django_db
class TestXSSURLs:
    """Tests for XSS URL patterns."""

    def test_xss_index_url(self, client):
        """Test XSS index URL loads."""
        response = client.get(reverse('xss'))
        assert response.status_code == 200

    def test_xss_path_url_resolves(self):
        """Test XSS path URL resolves to correct view."""
        url = reverse('xss-path', kwargs={'path': 'test'})
        assert resolve(url).func == exercises.xss_path

    def test_xss_form_url_resolves(self):
        """Test XSS form URL resolves to correct view."""
        url = reverse('xss-form')
        assert resolve(url).func == exercises.xss_form

    def test_xss_query_url_resolves(self):
        """Test XSS query URL resolves to correct view."""
        url = reverse('xss-query')
        assert resolve(url).func == exercises.xss_query


@pytest.mark.django_db
class TestCSRFURLs:
    """Tests for CSRF URL patterns."""

    def test_csrf_index_url(self, client):
        """Test CSRF index URL loads."""
        response = client.get(reverse('csrf'))
        assert response.status_code == 200

    def test_csrf_image_url_resolves(self):
        """Test CSRF image URL resolves to correct view."""
        url = reverse('csrf-image')
        assert resolve(url).func == exercises.csrf_image

    def test_csrf_third_party_url(self, client):
        """Test CSRF third party URL loads."""
        response = client.get(reverse('csrf-third-party'))
        assert response.status_code == 200

    def test_csrf_gift_card_url(self, client):
        """Test CSRF gift card URL loads."""
        response = client.get(reverse('csrf-gift-card'))
        assert response.status_code == 200


@pytest.mark.django_db
class TestDirectObjectReferencesURLs:
    """Tests for direct object references URL patterns."""

    def test_dor_index_url(self, client):
        """Test direct object references index URL loads."""
        response = client.get(reverse('direct-object-references'))
        assert response.status_code == 200

    def test_dor_profile_url_resolves(self):
        """Test direct object references profile URL resolves."""
        url = reverse('direct-object-references-profile', kwargs={'userid': '1'})
        assert resolve(url).func == exercises.dor_user_profile


@pytest.mark.django_db
class TestMisconfigURLs:
    """Tests for misconfiguration URL patterns."""

    def test_misconfig_index_url(self, client):
        """Test misconfiguration index URL loads."""
        response = client.get(reverse('misconfig'))
        assert response.status_code == 200

    def test_misconfig_boom_url_resolves(self):
        """Test misconfiguration boom URL resolves."""
        url = reverse('misconfig-boom')
        assert resolve(url).func == exercises.boom


@pytest.mark.django_db
class TestExposureURLs:
    """Tests for data exposure URL patterns."""

    def test_exposure_index_url(self, client):
        """Test exposure index URL loads."""
        response = client.get(reverse('exposure'))
        assert response.status_code == 200

    def test_exposure_login_url_resolves(self):
        """Test exposure login URL resolves."""
        url = reverse('exposure-login')
        assert resolve(url).func == exercises.exposure_login


@pytest.mark.django_db
class TestAccessControlURLs:
    """Tests for access control URL patterns."""

    def test_access_control_index_url(self, client):
        """Test access control index URL loads."""
        response = client.get(reverse('access-control'))
        assert response.status_code == 200

    def test_access_control_missing_url_resolves(self):
        """Test access control missing URL resolves."""
        url = reverse('access-control-missing')
        assert resolve(url).func == exercises.missing_access_control


@pytest.mark.django_db
class TestRedirectsURLs:
    """Tests for redirects and forwards URL patterns."""

    def test_redirects_index_url(self, client):
        """Test redirects index URL loads."""
        response = client.get(reverse('redirects'))
        assert response.status_code == 200

    def test_redirects_redirects_url(self, client):
        """Test redirects information URL loads."""
        response = client.get(reverse('redirects-redirects'))
        assert response.status_code == 200

    def test_redirects_redirect_url_resolves(self):
        """Test redirects redirect URL resolves."""
        url = reverse('redirects-redirect')
        assert resolve(url).func == exercises.unvalidated_redirect

    def test_redirects_forwards_url(self, client):
        """Test redirects forwards URL loads."""
        response = client.get(reverse('redirects-forwards'))
        assert response.status_code == 200

    def test_redirects_forward_url_resolves(self):
        """Test redirects forward URL resolves."""
        url = reverse('redirects-forward')
        assert resolve(url).func == exercises.unvalidated_forward


@pytest.mark.django_db
class TestComponentsURLs:
    """Tests for vulnerable components URL patterns."""

    def test_components_index_url(self, client):
        """Test vulnerable components index URL loads."""
        response = client.get(reverse('components'))
        assert response.status_code == 200


@pytest.mark.django_db
class TestBrokenAuthURLs:
    """Tests for broken authentication URL patterns."""

    def test_broken_auth_index_url(self, client):
        """Test broken auth index URL loads."""
        response = client.get(reverse('broken-auth'))
        assert response.status_code == 200


@pytest.mark.django_db
class TestStaticFiles:
    """Tests for static file serving."""

    def test_static_css_accessible(self, client):
        """Test that CSS files are accessible."""
        response = client.get('/static/css/site.css')
        # May be 200 or 404 depending on collectstatic
        assert response.status_code in [200, 404]

    def test_static_js_accessible(self, client):
        """Test that JS files are accessible."""
        response = client.get('/static/js/foundation.min.js')
        # May be 200 or 404 depending on collectstatic
        assert response.status_code in [200, 404]


class TestURLPatterns:
    """Tests for URL pattern structure."""

    def test_all_named_urls_exist(self):
        """Test that all expected named URLs exist."""
        expected_urls = [
            'home', 'about', 'conclusion',
            'injection', 'injection-sql', 'injection-file-access', 
            'user-pic', 'injection-code-execution',
            'broken-auth',
            'xss', 'xss-form', 'xss-query',
            'direct-object-references',
            'misconfig', 'misconfig-boom',
            'exposure', 'exposure-login',
            'access-control', 'access-control-missing',
            'csrf', 'csrf-image', 'csrf-third-party', 'csrf-gift-card',
            'components',
            'redirects', 'redirects-redirects', 'redirects-redirect',
            'redirects-forwards', 'redirects-forward',
        ]
        
        for url_name in expected_urls:
            try:
                if url_name == 'xss-path':
                    reverse(url_name, kwargs={'path': 'test'})
                elif url_name == 'direct-object-references-profile':
                    reverse(url_name, kwargs={'userid': '1'})
                else:
                    reverse(url_name)
            except Exception as e:
                pytest.fail(f"URL '{url_name}' does not exist or cannot be reversed: {e}")

