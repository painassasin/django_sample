from .base import env, IS_TESTING

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

if env.bool('EMAIL_TO_CONSOLE'):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if IS_TESTING:
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
