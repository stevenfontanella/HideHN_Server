from .base import *

DEBUG = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'var/log': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/django-logs/django.log',
        },
    },
    'loggers': {
        'sentiment': {
            'handlers': ['var/log'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
