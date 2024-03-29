from celery.schedules import crontab
from .base import *


LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "myapp:home"
LOGOUT_REDIRECT_URL = "myapp:home"
AUTH_USER_MODEL = "userauth.CustomUser"
MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'

STATIC_HOST = os.environ.get("DJANGO_STATIC_HOST", "")
STATIC_ROOT = "static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_URL = STATIC_HOST + 'static/'

FIXTURE_DIRS = [
    'myapp/fixtures/myapp/',
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

# Celery settings
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"

CELERY_BEAT_SCHEDULE = {
    "send_orders_task": {
        'task': "myapp.tasks.send_orders_task",
        'schedule': crontab(hour=18, minute=0, day_of_week='fri')
    }
}


# SMTP settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '<your email>'
EMAIL_HOST_PASSWORD = "<your host password>"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

ACCOUNTANT = "<email>"

# Settings for SSl and TLS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
