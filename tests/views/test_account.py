from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from mock import mock

from ..utils import PyCoinsTestCase


class AccountViewsTestCase(PyCoinsTestCase):
    def test_user_detail_view__no_auth(self):
        url = reverse('user-details')
        response = self.client.get(url)
        self.assertRedirects(response, '{}?next={}'.format(settings.LOGIN_URL, url),
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=True)

    def test_user_detail_view__auth_ok(self):
        self.login_as_user(self.client)
        response = self.client.get(reverse('user-details'))
        self.assertEqual(response.status_code, 200)

    def test_user_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_user_api_docs_view(self):
        response = self.client.get(reverse('api_docs'))
        self.assertEqual(response.status_code, 200)

    def test_user_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_user_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_user_password_reset_view(self):
        response = self.client.get(reverse('password-reset'))
        self.assertEqual(response.status_code, 200)

    def test_user_password_reset_confirm_view(self):
        response = self.client.get(reverse('password_reset_confirm', kwargs=dict(uidb64='foo', token='ba-bar')))
        self.assertEqual(response.status_code, 200)

    def test_user_account_confirm_email_view(self):
        with mock.patch('pycoins.views.account.VerifyEmailView.post') as mock_post:
            mock_post.return_value = HttpResponse(status=200)

            response = self.client.get(reverse('account_confirm_email', kwargs=dict(key='foo')))
            self.assertRedirects(response, '{}?info=Your+email+has+been+confirmed.'.format(reverse('home')),
                                 status_code=302, target_status_code=200,
                                 fetch_redirect_response=True)

            self.assertEqual(mock_post.call_count, 1)
