from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class RestrictedTemplateView(LoginRequiredMixin, TemplateView):
    redirect_field_name = 'next'
