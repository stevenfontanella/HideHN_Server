from .base import *

import sys

DEBUG = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        }
    },
    'loggers': {
        'sentiment': {
            'handlers': ['stdout'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
