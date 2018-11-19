from .base import *

SECRET_KEY = '$ecret'

DEBUG = True
ALLOWED_HOSTS = []


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
