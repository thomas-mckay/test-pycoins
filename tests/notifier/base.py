from datetime import timedelta

import responses
from django.conf import settings
from django.utils import timezone
from exam import fixture

from pycoins.notifier import CoinAPI, Notifier
from ..utils import PyCoinsTestCase


class NotifierTestCase(PyCoinsTestCase):
    @fixture
    def notifier(self):
        return Notifier()

    def mock_coin_api__exchange_rates__btc(self):
        datetime_str = timezone.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        responses.add(
            'GET',
            url = '{}{}{}'.format(settings.COIN_API['url'], CoinAPI.rates_url, 'BTC'),
            json={
                "asset_id_base": "BTC",
                "rates": [
                    {
                        "time": datetime_str,
                        "asset_id_quote": "USD",
                        "rate": 3258.8875417798037784035133948
                    },
                    {
                        "time": datetime_str,
                        "asset_id_quote": "EUR",
                        "rate": 2782.5255080599273092901331567
                    },
                    {
                        "time": datetime_str,
                        "asset_id_quote": "GBP",
                        "rate": 2509.6024203799580199765804823
                    }
                ]
            }, status=200, content_type='application/json'
        )

    def mock_coin_api__exchange_rates__btc__5_days_ago(self):
        datetime_str = (timezone.now() - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        responses.add(
            'GET',
            url = '{}{}{}'.format(settings.COIN_API['url'], CoinAPI.rates_url, 'BTC'),
            json={
                "asset_id_base": "BTC",
                "rates": [
                    {
                        "time": datetime_str,
                        "asset_id_quote": "EUR",
                        "rate": 3000.5255080599273092901331567
                    },
                ]
            }, status=200, content_type='application/json'
        )

    def mock_coin_api__exchange_rates__btc__10_days_ago(self):
        datetime_str = (timezone.now() - timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        responses.add(
            'GET',
            url = '{}{}{}'.format(settings.COIN_API['url'], CoinAPI.rates_url, 'BTC'),
            json={
                "asset_id_base": "BTC",
                "rates": [
                    {
                        "time": datetime_str,
                        "asset_id_quote": "EUR",
                        "rate": 3400.5255080599273092901331567
                    },
                ]
            }, status=200, content_type='application/json'
        )

    def mock_coin_api__exchange_rates__btc__30_days_ago(self):
        datetime_str = (timezone.now() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        responses.add(
            'GET',
            url = '{}{}{}'.format(settings.COIN_API['url'], CoinAPI.rates_url, 'BTC'),
            json={
                "asset_id_base": "BTC",
                "rates": [
                    {
                        "time": datetime_str,
                        "asset_id_quote": "EUR",
                        "rate": 3400.5255080599273092901331567
                    },
                ]
            }, status=200, content_type='application/json'
        )

    def mock_coin_api__exchange_rates__eth(self):
        datetime_str = timezone.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        responses.add(
            'GET',
            url = '{}{}{}'.format(settings.COIN_API['url'], CoinAPI.rates_url, 'ETH'),
            json={
                "asset_id_base": "ETH",
                "rates": [
                    {
                        "time": datetime_str,
                        "asset_id_quote": "USD",
                        "rate": 4258.8875417798037784035133948
                    },
                    {
                        "time": datetime_str,
                        "asset_id_quote": "EUR",
                        "rate": 3782.5255080599273092901331567
                    },
                    {
                        "time": datetime_str,
                        "asset_id_quote": "GBP",
                        "rate": 3509.6024203799580199765804823
                    }
                ]
            }, status=200, content_type='application/json'
        )
