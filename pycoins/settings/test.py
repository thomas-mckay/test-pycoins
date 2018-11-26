from .local import *

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

LOGGING['loggers']['django.db.backends']['handlers'] = []
