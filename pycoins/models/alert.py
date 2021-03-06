from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from extended_choices import Choices
from rest_framework.compat import MinValueValidator, MaxValueValidator
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

    coin = models.ForeignKey('Symbol', null=False, blank=False, db_index=True,
                             on_delete=models.PROTECT, limit_choices_to={'type': Symbol.TYPE_CHOICES.COIN},
                             related_name='coin_alerts')  # the related name is meaningless in our case,
                                                          # but Django needs to be indulged here
    currency = models.ForeignKey('Symbol', null=False, blank=False, db_index=True,
                                 on_delete=models.PROTECT, limit_choices_to={'type': Symbol.TYPE_CHOICES.CURRENCY},
                                 related_name='currency_alerts')  # the related name is meaningless in our case,
                                                                  # but Django needs to be indulged here


    user = models.ForeignKey('auth.User', null=False, blank=False, db_index=True,
                             related_name='alerts', on_delete=models.CASCADE)

    trigger_type = models.PositiveSmallIntegerField(choices=TRIGGER_TYPE_CHOICES, null=False, blank=False)

    # For FIXED trigger types
    amount = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])

    # For EVOLUTION trigger type
    evolution = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    evolution_period = models.DurationField(null=True, blank=True, validators=[MaxValueValidator(timedelta(days=5*365))])

    # Alerting settings
    last_sent = models.DateTimeField(null=True, blank=True)
    message_interval = models.DurationField(null=True, blank=True)
    activated = models.BooleanField(null=True, blank=True, db_index=True)

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
            if self.amount is None:
                errors.append('`amount` parameter is required for fixed alerts.')

            self.evolution = None
            self.evolution_period = None

        if errors and raise_errors:
            raise ValidationError('\n'.join(errors))

        return errors

    def save(self, *args, **kwargs):
        self.validate(raise_errors=True)
        self.last_sent = None
        return super(Alert, self).save(*args, **kwargs)

    def notify(self):
        if self.last_sent and not self.message_interval:
            # We have already notified the user once and alert is not set to repeat
            return

        if (self.last_sent
            and self.message_interval
            and timezone.now() - self.message_interval < self.last_sent):
            # The user has already been notified within the configured interval
            return

        send_mail('PyCoin Alert',
                  '{}'.format(self),
                  settings.DEFAULT_FROM_EMAIL,
                  [self.user.email])

        self.update_last_sent()

    def update_last_sent(self):
        # Bypass the save method (it resets the 'last_sent' field)
        self.__class__.objects.filter(pk=self.pk).update(last_sent=timezone.now())

