import responses
from mock import mock

from pycoins.models import Alert
from .base import NotifierTestCase


class NotifierTests(NotifierTestCase):
    def do_notify(self):
        raised_alerts = []
        def mock_notify(alert):
            raised_alerts.append(alert)

        with mock.patch.object(Alert, 'notify', mock_notify):
            self.notifier.notify()

        return raised_alerts

    @responses.activate
    def test_notifier__fixed_alerts(self):
        self.alert_greater
        self.alert_lower
        self.alert_evolution

        self.mock_coin_api__exchange_rates__btc()
        self.mock_coin_api__exchange_rates__eth()

        raised_alerts = self.do_notify()
        self.assertEqual(set(raised_alerts), {self.alert_lower, self.alert_greater})

    @responses.activate
    def test_notifier__evolution_alerts__lower_than_evolution(self):
        self.alert_evolution

        self.mock_coin_api__exchange_rates__btc__5_days_ago()
        raised_alerts = self.do_notify()
        self.assertEqual(set(raised_alerts), set())

        responses.reset()

        self.mock_coin_api__exchange_rates__btc()
        raised_alerts = self.do_notify()
        self.assertEqual(set(raised_alerts), set())

    @responses.activate
    def test_notifier__evolution_alerts__longer_than_evolution_period(self):
        self.alert_evolution

        self.mock_coin_api__exchange_rates__btc__30_days_ago()
        raised_alerts = self.do_notify()
        self.assertEqual(set(raised_alerts), set())

        responses.reset()

        self.mock_coin_api__exchange_rates__btc()
        raised_alerts = self.do_notify()
        self.assertEqual(set(raised_alerts), set())

    @responses.activate
    def test_notifier__evolution_alerts__evolution_match(self):
        self.alert_evolution

        self.mock_coin_api__exchange_rates__btc__10_days_ago()
        raised_alerts = self.do_notify()
        self.assertEqual(set(raised_alerts), set())

        responses.reset()

        self.mock_coin_api__exchange_rates__btc()
        raised_alerts = self.do_notify()
        self.assertEqual(set(raised_alerts), {self.alert_evolution})

