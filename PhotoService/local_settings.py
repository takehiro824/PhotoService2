import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
SECRET_KEY = 'ior=+ic**p+7&ytyz(gm!p4&jb-cg4mycphzoe0t-b!l0)&#!-'
DEBUG = True