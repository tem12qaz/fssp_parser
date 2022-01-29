config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'file_format': {
            'format': '{asctime} - {name} - {levelname} - {filename}:{module}:{lineno} - {message}',
            'style': '{'
        }
    },
    'handlers': {
        'error_handler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        }
    },
    'loggers': {
        'file_logger': {
            'level': 'INFO',
            'handlers': [
                'error_handler'
            ]
        }
    }
}
