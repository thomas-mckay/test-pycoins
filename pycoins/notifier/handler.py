import json

import requests
from django.conf import settings
from django.utils.dateparse import parse_datetime


class CoinAPIError(Exception):
    pass


class Rate(object):
    def __init__(self, coin, currency, rate, time):
        self.coin = coin
        self.currency = currency
        self.value = rate
        self.time = time

    @classmethod
    def from_data(cls, **data):
        return cls(
            coin=str(data['asset_id_base']),
            currency=str(data['asset_id_quote']),
            rate=float(data['rate']),
            time=parse_datetime(data['time']),
        )


class CoinAPI(object):
    rates_url = 'exchangerate/'
    def get_headers(self):
        return {'X-CoinAPI-Key' : settings.COIN_API['key']}

    def get_rates(self, coin_code):
        url = '{}{}{}'.format(settings.COIN_API['url'], self.rates_url, coin_code)
        response = requests.get(url, headers=self.get_headers())

        if response.status_code != 200:
            raise CoinAPIError(response.content)

        result = json.loads(response.content)

        return [Rate.from_data(asset_id_base=result['asset_id_base'], **rate_data) for rate_data in result['rates']]
