import os
from .base import *


LOGIN_URL = "/userauth/login/"
LOGIN_REDIRECT_URL = "/myapp/home/"
LOGOUT_REDIRECT_URL = "/myapp/home/"
AUTH_USER_MODEL = "userauth.CustomUser"
MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
