from .base import *

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
AUTH_USER_MODEL = "userauth.CustomUser"
MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'
STATICFILES_DIRS = ['static']
FIXTURE_DIRS = [
    'myapp/fixtures/myapp/',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
