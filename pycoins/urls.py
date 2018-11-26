from django.conf import settings
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_swagger.views import get_swagger_view

from pycoins.views import account, alert, generic


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v{}/'.format(settings.API_VERSION), include(("pycoins.api.urls", "api"), namespace='api')),


    url(r'^$',
        TemplateView.as_view(template_name="home.html"),
        name='home'),

    # Signup
    url(r'^signup/$',
        TemplateView.as_view(template_name="user/signup.html"),
        name='signup'),

    # Login/out
    url(r'^login/$',
        TemplateView.as_view(template_name="user/login.html"),
        name='login'),

    # Password
    url(r'^password-reset/$',
        TemplateView.as_view(template_name="user/password_reset.html"),
        name='password-reset'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="user/password_reset_confirm.html"),
        name='password_reset_confirm'),

    # Current user data
    url(r'^user-details/$',
        generic.RestrictedTemplateView.as_view(template_name="user/user_details.html"),
        name='user-details'),

    # Auto-generated API documentation
    url(r'^docs/$', get_swagger_view(title='API Docs'), name='api_docs'),

    # Alerts
    url(r'^alerts/$',
        alert.AlertListView.as_view(template_name="alert/list.html"),
        name='user-alerts'),

    url(r'^alerts/create/$',
        alert.AlertView.as_view(),
        name='user-alert-create'),

    url(r'^alerts/(?P<pk>\d+)/$',
        alert.AlertView.as_view(),
        name='user-alert-change'),

    url(r'^account/', include('allauth.urls')),

    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$',
        account.confirm_email,
        name='account_confirm_email'),
]
