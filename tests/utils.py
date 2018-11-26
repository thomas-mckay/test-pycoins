from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase, Client
from exam import Exam, fixture
from rest_framework.test import APIClient

from pycoins.models import Alert, Symbol


class PyCoinsTestCase(Exam, TestCase):
    @fixture
    def client(self):
        return Client()

    @fixture
    def api_client(self):
        return APIClient()

    @fixture
    def staff(self):
        return User.objects.create_superuser(username='john_nada',
                                             email='john@they_live.com',
                                             password='AllOuttaBubbleGum')

    def login_as_staff(self, client):
        ok = client.login(username=self.staff.username, password='AllOuttaBubbleGum')
        self.assertEqual(ok, True)

    @fixture
    def user(self):
        return User.objects.create_user(username='jack_burton',
                                        email='big_trouble@little_china.com',
                                        password='AllInTheReflexes')

    def login_as_user(self, client):
        ok = client.login(username=self.user.username, password='AllInTheReflexes')
        self.assertEqual(ok, True)

    @fixture
    def bitcoin(self):
        return Symbol.objects.create(
            name="Bitcoin",
            code="BTC",
            symbol="btc",
            type=Symbol.TYPE_CHOICES.COIN,
        )

    @fixture
    def ethereum(self):
        return Symbol.objects.create(
            name="Ethereum",
            code="ETH",
            symbol="eth",
            type=Symbol.TYPE_CHOICES.COIN,
        )

    @fixture
    def euro(self):
        return Symbol.objects.create(
            name="Euro",
            code="EUR",
            symbol="€",
            type=Symbol.TYPE_CHOICES.CURRENCY,
        )

    @fixture
    def us_dollar(self):
        return Symbol.objects.create(
            name="US Dollar",
            code="USD",
            symbol="US$",
            type=Symbol.TYPE_CHOICES.CURRENCY,
        )

    @fixture
    def alert_lower(self):
        return Alert.objects.create(
            coin=self.ethereum,
            currency=self.euro,
            user=self.user,
            trigger_type=Alert.TRIGGER_TYPE_CHOICES.LOWER,
            amount=4000,
            activated=True,
        )

    @fixture
    def alert_greater(self):
        return Alert.objects.create(
            coin=self.bitcoin,
            currency=self.us_dollar,
            user=self.user,
            trigger_type=Alert.TRIGGER_TYPE_CHOICES.GREATER,
            amount=2000,
            activated=True,
        )

    @fixture
    def alert_evolution(self):
        return Alert.objects.create(
            coin=self.bitcoin,
            currency=self.euro,
            user=self.user,
            trigger_type=Alert.TRIGGER_TYPE_CHOICES.EVOLUTION,
            evolution=20,
            evolution_period=timedelta(days=20),
            activated=True,
        )
