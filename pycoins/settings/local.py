from .base import *

SECRET_KEY = '$ecret'

DEBUG = True
ALLOWED_HOSTS = []


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'sql': {
            '()': 'pycoins.utils.logger.SQLFormatter',
            'format': '[%(duration).3f] %(statement)s',
        }
    },
    'handlers': {
        'sql': {
            'level': 'DEBUG',
            'formatter': 'sql',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['sql'],
            'level': 'DEBUG',
        },
    }
}
