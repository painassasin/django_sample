LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[{asctime}] [{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {'handlers': ['console'], 'propagate': False, 'level': 'INFO'},
        'config': {'handlers': ['console'], 'propagate': False, 'level': 'DEBUG'},
        'mailing': {'handlers': ['console'], 'propagate': False, 'level': 'DEBUG'},
    },
}
