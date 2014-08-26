# config

class Configuration(object):
    DBFILE = 'data.db'
    DATABASE = {
        'name': DBFILE,
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }
    SECRET_KEY = 'm3tr0'
    DEBUG = True
    #add this so that flask doesn't swallow error messages
    PROPAGATE_EXCEPTIONS = DEBUG
    ASSETS_DEBUG = True