DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'rest_framework_gis',
)

SECRET_KEY = 'testsecretkey'
