from django.urls import reverse
from exam import fixture

from pycoins.models import Alert, Symbol
from ..utils import PyCoinsTestCase


class AlertDetailApiTests(PyCoinsTestCase):
    @fixture
    def url(self):
        return reverse('api:alert-detail', kwargs={'user_pk': self.user.pk, 'pk': self.alert_greater.pk})

    def test_alert_detail_api__get__no_auth(self):
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_alert_detail_api__get__wrong_auth(self):
        self.login_as_staff(self.api_client)
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_alert_detail_api__get__auth_ok(self):
        self.login_as_user(self.api_client)

        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), {
            'activated': True,
            'amount': 2000.0,
            'coin': self.bitcoin.pk,
            'coin_obj': {
                'code': 'BTC',
                'name': 'Bitcoin',
                'symbol': 'btc',
                'type': Symbol.TYPE_CHOICES.COIN,
            },
            'currency': self.us_dollar.pk,
            'currency_obj': {
                'code': 'USD',
                'name': 'US Dollar',
                'symbol': 'US$',
                'type': Symbol.TYPE_CHOICES.CURRENCY,
            },
            'detail_url': '/api/v0.1/users/1/alerts/1/',
            'evolution': None,
            'evolution_period': None,
            'id': self.alert_greater.pk,
            'message_interval': None,
            'trigger_type': Alert.TRIGGER_TYPE_CHOICES.GREATER,
        })

    def test_alert_detail_api__put(self):
        self.login_as_user(self.api_client)

        response = self.api_client.put(self.url, {
            'activated': True,
            'amount': 3000.0,
            'coin': self.bitcoin.pk,
            'currency': self.us_dollar.pk,
            'id': self.alert_greater.pk,
            'evolution': None,
            'evolution_period': None,
            'message_interval': None,
            'trigger_type': Alert.TRIGGER_TYPE_CHOICES.GREATER,
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['amount'], 3000)

    def test_alert_detail_api__delete(self):
        self.login_as_user(self.api_client)

        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 200)

        response = self.api_client.delete(self.url)
        self.assertEqual(response.status_code, 204)

        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 404)


class AlertListApiTests(PyCoinsTestCase):
    @fixture
    def url(self):
        return reverse('api:alert-list', kwargs={'user_pk': self.user.pk})

    def assertAlertListEquals(self, alert_list_json, alert_list_db):
        return self.assertEqual(
            {alert['id'] for alert in alert_list_json},
            {alert.pk for alert in alert_list_db}
        )

    def test_alert_list_api__get__no_auth(self):
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_alert_list_api__get__as_user(self):
        self.alert_lower
        self.alert_greater
        self.alert_evolution

        self.login_as_user(self.api_client)

        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertAlertListEquals(response.json(), [self.alert_lower, self.alert_greater, self.alert_evolution])

        self.alert_evolution.user = self.staff
        self.alert_evolution.save(update_fields=['user'])

        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertAlertListEquals(response.json(), [self.alert_lower, self.alert_greater])

    def test_alert_list_api__post(self):
        self.login_as_user(self.api_client)

        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

        response = self.api_client.post(self.url, {
            'activated': True,
            'amount': 3000.0,
            'coin': self.ethereum.pk,
            'currency': self.euro.pk,
            'evolution': None,
            'evolution_period': None,
            'message_interval': '1 day',
            'trigger_type': Alert.TRIGGER_TYPE_CHOICES.GREATER,
        }, format='json')

        self.assertEqual(response.status_code, 201)

        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
