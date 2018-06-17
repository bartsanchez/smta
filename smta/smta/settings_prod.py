from smta.settings import *  # noqa

# DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PASSWORD': 'testdb',
    },
}
