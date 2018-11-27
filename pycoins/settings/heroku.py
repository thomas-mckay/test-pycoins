import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN', None),
    integrations=[DjangoIntegration()]
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER', '')
EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT', '')
EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN', '')
EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD', '')

HEROKU_JOB_INTERVAL = int(os.environ.get('HEROKU_JOB_INTERVAL', 30))

django_heroku.settings(locals())
