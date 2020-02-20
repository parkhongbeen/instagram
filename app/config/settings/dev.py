from .base import *


SECRETS = SECRETS_FULL['dev']

DEBUG = True
WSGI_APPLICATION = 'config.wsgi.dev.application'
DATABASES = SECRETS['DATABASES']
ALLOWED_HOSTS += [
    '*',
]
INSTALLED_APPS += [

]





# Storage
AWS_STORAGE_BUCKET_NAME = 'wps-instagram-phb2-dev'
