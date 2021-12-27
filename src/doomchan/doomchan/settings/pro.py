from ._base import *

DEBUG = False

ALLOWED_HOSTS = [
    "scowq2nkrkswnqg5mnvz4v6mpu6lurxdibz4ikytec4bysmn3ocibeqd.onion",
    "localhost",
    "*.doomchan.com",
    "www.doomchan.com",
    "doomchan.com"
]


CACHES = {
    'default': {
    'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    'LOCATION': '127.0.0.1:11211',
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

X_FRAME_OPTIONS = "DENY"

SESSION_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = True

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_SECONDS = 3600

CSRF_COOKIE_SECURE = True

SECURE_HSTS_PRELOAD = True

ADMINS = [("MoistCat", "moistanonpy@gmail.com"),]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
