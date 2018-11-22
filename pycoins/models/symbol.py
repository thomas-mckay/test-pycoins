from django.db import models
from extended_choices import Choices


class SymbolQueryset(models.QuerySet):
    def coins(self):
        return self.filter(type=self.model.TYPE_CHOICES.COIN)

    def currencies(self):
        return self.filter(type=self.model.TYPE_CHOICES.CURRENCY)


class SymbolManager(models.Manager):
    def get_queryset(self):
        return SymbolQueryset(self.model)

    def coins(self):
        return self.get_queryset().coins()

    def currencies(self):
        return self.get_queryset().currencies()


class Symbol(models.Model):
    TYPE_CHOICES = Choices(
        ('COIN', 1, 'Coin'),
        ('CURRENCY', 2, 'Currency'),
    )

    name = models.CharField(max_length=50, null=False, blank=False)
    code = models.CharField(max_length=5, null=False, blank=False)
    symbol = models.CharField(max_length=5, null=False, blank=False)

    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, null=False, blank=False)

    objects = SymbolManager()

    def __str__(self):
        return '{} ({}/{})'.format(self.name, self.symbol, self.code)
