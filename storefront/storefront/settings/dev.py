from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-h2rnfyd0i^oytp15jt+=g@mu+ji^zt$&h76yx_)a^gf%9$l!z^"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "storefront3",
        "HOST": "localhost",
        "PORT": 3306,
        "USER": "root",
        "PASSWORD": "139254",
    }
}


if DEBUG:
    MIDDLEWARE += [
        "silk.middleware.SilkyMiddleware",
    ]


CELERY_BROKER_URL = "redis://localhost:6379/1"


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/2",
        "TIMEOUT": 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


EMAIL_HOST = "localhost"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 9696
