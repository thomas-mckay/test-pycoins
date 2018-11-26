from datetime import timedelta

from django.core import mail
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from mock import mock

from pycoins.models import Alert
from ..utils import PyCoinsTestCase


class AlertModelTests(PyCoinsTestCase):
    def test_alert_model__validate__evolution__has_amount(self):
        self.alert_evolution.amount = 50
        self.alert_evolution.validate(raise_errors=True)
        self.assertEqual(self.alert_evolution.amount, None)

    def test_alert_model__validate__evolution__no_evolution(self):
        self.alert_evolution.evolution = None
        with self.assertRaises(ValidationError):
            self.alert_evolution.validate(raise_errors=True)

    def test_alert_model__validate__evolution__no_evolution_period(self):
        self.alert_evolution.evolution_period = None
        with self.assertRaises(ValidationError):
            self.alert_evolution.validate(raise_errors=True)

    def test_alert_model__validate__fixed__has_evolution(self):
        self.alert_greater.evolution = 50
        self.alert_greater.evolution_period = timedelta(days=20)
        self.alert_greater.validate(raise_errors=True)
        self.assertEqual(self.alert_greater.evolution, None)
        self.assertEqual(self.alert_greater.evolution_period, None)

    def test_alert_model__validate__fixed__no_amount(self):
        self.alert_greater.amount = None
        with self.assertRaises(ValidationError):
            self.alert_greater.validate(raise_errors=True)

        self.alert_greater.amount = 0
        self.alert_greater.validate(raise_errors=True)
        self.assertEqual(self.alert_greater.amount, 0)

    def test_alert_model__save(self):
        with mock.patch.object(self.alert_greater, 'validate'):
            self.alert_greater.last_sent = timezone.now()
            self.alert_greater.save()
            self.assertEqual(self.alert_greater.last_sent, None)
            self.assertEqual(self.alert_greater.validate.call_count, 1)

    def test_alert_model__bulk_create(self):
        alerts = [
            Alert(
                activated=True,
                amount=3000.0,
                coin=self.bitcoin,
                currency=self.us_dollar,
                user=self.user,
                trigger_type=Alert.TRIGGER_TYPE_CHOICES.LOWER,
            ),
            Alert(
                activated=True,
                amount=3000.0,
                coin=self.ethereum,
                currency=self.euro,
                user=self.user,
                trigger_type=Alert.TRIGGER_TYPE_CHOICES.GREATER,
            )
        ]

        with mock.patch.object(Alert, 'validate'):
            Alert.objects.bulk_create(alerts)
            self.assertEqual(Alert.validate.call_count, 2)

    def test_alert_model__notify__already_notified_once(self):
        self.alert_greater.message_interval = None
        self.alert_greater.last_sent = timezone.now()

        self.alert_greater.notify()
        self.assertEqual(len(mail.outbox), 0)

    def test_alert_model__notify__already_notified_within_interval(self):
        self.alert_greater.message_interval = timedelta(days=1)
        self.alert_greater.last_sent = timezone.now() - timedelta(hours=23)

        self.alert_greater.notify()
        self.assertEqual(len(mail.outbox), 0)

    def test_alert_model__notify__never_notified(self):
        self.alert_greater.message_interval = timedelta(days=1)
        self.alert_greater.last_sent = None

        self.alert_greater.notify()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'PyCoin Alert')

    def test_alert_model__notify__already_notified_outside_interval(self):
        self.alert_greater.message_interval = timedelta(days=1)
        self.alert_greater.last_sent = timezone.now() - timedelta(days=1, hours=1)

        self.alert_greater.notify()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'PyCoin Alert')

    def test_alert_model__str(self):
        self.assertEqual('{}'.format(self.alert_greater), "Bitcoin's value is greater than 2000US$")
        self.assertEqual('{}'.format(self.alert_evolution), "Bitcoin's value varies by 20% over a period of 20 days, 0:00:00")
