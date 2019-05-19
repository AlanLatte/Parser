import os

class Config(object):
    BASE_DIR            = os.path.abspath(os.path.dirname(__file__))
    CSRF_ENABLED        = True
    SECRET_KEY          = os.urandom(16)
    DATA_BASE_STORAGE   = os.path.join(BASE_DIR, 'STORAGE')
    ALL_TAGS            = os.path.join(BASE_DIR, 'TAGS')
