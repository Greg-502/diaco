from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['diaco502.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vsvgl17v1v03eljh',
        'USER': 'jrwathta3cxtgnvk',
        'PASSWORD': 'uxxqbexe7qbjd2ya',
        'HOST': 'z5zm8hebixwywy9d.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
        'PORT': '3306'
    }
}
