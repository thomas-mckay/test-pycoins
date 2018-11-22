from django.db import models
from extended_choices import Choices
from rest_framework.exceptions import ValidationError

from pycoins.models.symbol import Symbol


class AlertManager(models.Manager):
    def bulk_create(self, objects, *args, **kwargs):
        for obj in objects:
            obj.validate(raise_errors=True)

        return super(AlertManager, self).bulk_create(objects, *args, **kwargs)


class Alert(models.Model):
    TRIGGER_TYPE_CHOICES = Choices(
        ('LOWER', 1, 'Lower than'),
        ('GREATER', 2, 'Greater than'),
        ('EVOLUTION', 3, 'Evolution'),
    )

    coin = models.ForeignKey('Symbol', null=False, blank=False,
                             on_delete=models.PROTECT, limit_choices_to={'type': Symbol.TYPE_CHOICES.COIN},
                             related_name='coin_alerts')  # the related name is meaningless in our case,
                                                          # but Django needs to be indulged here
    currency = models.ForeignKey('Symbol', null=False, blank=False,
                                 on_delete=models.PROTECT, limit_choices_to={'type': Symbol.TYPE_CHOICES.CURRENCY},
                                 related_name='currency_alerts')  # the related name is meaningless in our case,
                                                                  # but Django needs to be indulged here


    user = models.ForeignKey('auth.User', related_name='alerts', null=False, blank=False, on_delete=models.CASCADE)

    trigger_type = models.PositiveSmallIntegerField(choices=TRIGGER_TYPE_CHOICES, null=False, blank=False)

    # For FIXED trigger types
    amount = models.FloatField(null=True, blank=True)

    # For EVOLUTION trigger type
    evolution = models.FloatField(null=True, blank=True)
    evolution_period = models.DurationField(null=True, blank=True)

    # Alerting settings
    last_sent = models.DateTimeField(null=True, blank=True)
    message_interval = models.DurationField(null=True, blank=True)
    activated = models.BooleanField(null=True, blank=True)

    objects = AlertManager()

    def __str__(self):
        if self.trigger_type == self.TRIGGER_TYPE_CHOICES.EVOLUTION:
            return "{}'s value varies by {}% over a period of {}".format(self.coin.name,
                                                                         self.evolution,
                                                                         self.evolution_period)

        return "{}'s value is {} {}{}".format(self.coin.name,
                                              self.TRIGGER_TYPE_CHOICES.for_value(self.trigger_type).display.lower(),
                                              self.amount,
                                              self.currency.symbol)

    def validate(self, raise_errors=False):
        errors = []

        if self.trigger_type == self.TRIGGER_TYPE_CHOICES.EVOLUTION:
            if not self.evolution:
                errors.append('`evolution` parameter is required for evolution alerts.')

            if not self.evolution_period:
                errors.append('`evolution_period` parameter is required for evolution alerts.')

            self.amount = None

        else:
            if not self.amount:
                errors.append('`amount` parameter is required for fixed alerts.')

            self.evolution = None
            self.evolution_period = None

        if errors and raise_errors:
            raise ValidationError('\n'.join(errors))

        return errors

    def save(self, *args, **kwargs):
        self.validate(raise_errors=True)
        return super(Alert, self).save(*args, **kwargs)
