LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout',  # Use 'ext://sys.stderr' for stderr
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'myapp.log',
            'formatter': 'standard',
            'mode': 'a',
        },
        # Add more handlers here (e.g., HTTPHandler for an HTTP stream)
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}


