from django.db.models import Q, Min, Max
from django.utils import timezone

from pycoins.models import Alert, Rate, Symbol
from pycoins.notifier.handler import CoinAPI


class Notifier(object):
    def __init__(self):
        self.handler = CoinAPI()

    def get_all_rates(self):
        coins = {coin.code: coin for coin in Symbol.objects.coins()}
        currencies = {currency.code: currency for currency in Symbol.objects.currencies()}

        models = []

        for coin_code, coin in coins.items():
            rates = self.handler.get_rates(coin_code)

            models += [Rate(coin=coin, currency=currencies[rate.currency], value=rate.value, time=rate.time)
                       for rate in rates if rate.currency in currencies]

        Rate.objects.bulk_create(models)

        return models

    def notify(self):
        rates = self.get_all_rates()

        for rate in rates:
            fixed_alerts = (Alert.objects
                            .filter(coin=rate.coin, currency=rate.currency, activated=True)
                            .filter(Q(trigger_type=Alert.TRIGGER_TYPE_CHOICES.LOWER, amount__gte=rate.value)
                                    | Q(trigger_type=Alert.TRIGGER_TYPE_CHOICES.GREATER, amount__lte=rate.value))
                            .select_related('coin', 'currency')
                            .prefetch_related('user'))

            for alert in fixed_alerts:
                alert.notify()

            evolution_alerts = (Alert.objects
                                .filter(coin=rate.coin, currency=rate.currency, activated=True,
                                        trigger_type=Alert.TRIGGER_TYPE_CHOICES.EVOLUTION)
                                .select_related('coin', 'currency')
                                .prefetch_related('user'))

            for alert in evolution_alerts:
                """
                This calculates absolute evolution.
                It can't distinguish positive or negative evolutions.
                """
                min_max = Rate.objects.filter(coin=alert.coin,
                                              currency=alert.currency,
                                              time__gte=timezone.now() - alert.evolution_period
                                              ).aggregate(min=Min('value'),
                                                          max=Max('value'))


                evolution = 0
                if min_max['max'] is not None and min_max['min'] is not None:
                    evolution = ((min_max['max'] - min_max['min']) / min_max['min']) * 100

                if evolution > alert.evolution:
                    alert.notify()
