import json

from rest_framework.reverse import reverse

from pycoins.models import Alert, Symbol
from .generic import RestrictedTemplateView


class BaseAlertView(RestrictedTemplateView):
    def get_context_data(self, **kwargs):
        context = super(BaseAlertView, self).get_context_data(**kwargs)

        context['frontend_app_context'] = json.dumps(
            {
                'alertTriggerTypes': dict(Alert.TRIGGER_TYPE_CHOICES),
                'symbolTypes': dict(Symbol.TYPE_CHOICES),
            }
        )

        context['constants'] = {
            'alert_trigger_types': Alert.TRIGGER_TYPE_CHOICES,
            'symbol_types': Symbol.TYPE_CHOICES,
        }

        return context


class AlertListView(BaseAlertView):
    template_name = "alert/list.html"


class AlertView(BaseAlertView):
    template_name = "alert/form.html"

    def get_context_data(self, **kwargs):
        context = super(AlertView, self).get_context_data(**kwargs)
        alert_id = kwargs.get('pk', None)

        if alert_id:
            context['alert_id'] = alert_id
            context['action_url'] = reverse('api:alert-detail', kwargs={'user_pk': self.request.user.pk, 'pk': alert_id})
            context['method'] = 'PUT'

        else:
            context['action_url'] = reverse('api:alert-list', kwargs={'user_pk': self.request.user.pk})
            context['method'] = 'POST'

        context['coin_choices'] = [(symbol.id, symbol.name) for symbol in Symbol.objects.coins()]
        context['currency_choices'] = [(symbol.id, symbol.name) for symbol in Symbol.objects.currencies()]

        return context
