from django.conf import settings
from django.urls import reverse
from exam import fixture

from ..utils import PyCoinsTestCase


class AlertsViewsTestCase(object):
    def test_alert_views__no_auth(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '{}?next={}'.format(settings.LOGIN_URL, self.url),
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=True)

    def test_alert_views__auth_ok(self):
        self.login_as_user(self.client)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class AlertListViewTests(AlertsViewsTestCase, PyCoinsTestCase):
    @fixture
    def url(self):
        return reverse('user-alerts')


class AlertCreateViewTests(AlertsViewsTestCase, PyCoinsTestCase):
    @fixture
    def url(self):
        return reverse('user-alert-create')


class AlertChangeViewTests(AlertsViewsTestCase, PyCoinsTestCase):
    @fixture
    def url(self):
        return reverse('user-alert-change', kwargs={'pk': self.alert_evolution.pk})
