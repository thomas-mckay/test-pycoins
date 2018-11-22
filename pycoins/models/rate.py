from django.db import models

from pycoins.models.symbol import Symbol


class Rate(models.Model):
    coin = models.ForeignKey('Symbol', null=False, blank=False,
                             on_delete=models.PROTECT, limit_choices_to={'type': Symbol.TYPE_CHOICES.COIN},
                             related_name='coin_rates')

    currency = models.ForeignKey('Symbol', null=False, blank=False,
                             on_delete=models.PROTECT, limit_choices_to={'type': Symbol.TYPE_CHOICES.CURRENCY},
                             related_name='currency_rates')

    value = models.FloatField(null=False, blank=False)
    time = models.DateTimeField(null=False, blank=False)
