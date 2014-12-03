import os

# config

class BaseConfig:
	BASEDIR = os.path.abspath(os.path.dirname(__file__))
	PROJECT_NAME = "metroplaces"
	SECRET_KEY = "m3tr0n3t"

	DEBUG = True
	#add this so that flask doesn't swallow error messages
	PROPAGATE_EXCEPTIONS = DEBUG
	ASSETS_DEBUG = DEBUG

	DATABASE = {
		'name': 'metroplaces_base.db',
		'engine': 'peewee.SqliteDatabase',
		'check_same_thread': False,
	}
	# DATABASE = {
	# 	'name': 'places_base',
	# 	'engine': 'peewee.PostgresqlModel',
	# 	'user':'metro',
	# 	'password':'m3tr0n3t',
	# }

	if os.name == "nt":
		LESS_BIN = "lessc.cmd"
		COFFEE_BIN = "coffee.cmd"

	# Debug
	ASSETS_MINIFY = False
	ASSETS_USE_CDN = False

	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = 'test@gmail.com'
	MAIL_PASSWORD = ''

	DEFAULT_MAIL_SENDER = ("metro places", "test@gmail.com")

	# Flask-Security Flags
	SECURITY_CONFIRMABLE = True
	SECURITY_REGISTERABLE = True
	SECURITY_RECOVERABLE = True
	SECURITY_TRACKABLE = True

	SECURITY_PASSWORD_HASH = "bcrypt"

	SECURITY_PASSWORD_SALT = "$2a$12$sSoMBQ9V4hxNba5E0Xl3Fe"
	SECURITY_CONFIRM_SALT = "$2a$12$QyCM19UPUNLMq8n225V7qu"
	SECURITY_RESET_SALT = "$2a$12$GrrU0tYteKw45b5VfON5p."
	SECURITY_REMEMBER_SALT = "$2a$12$unlKF.sL4gnm4icbk0tvVe"


class DevelopmentConfig(BaseConfig):
	# DATABASE = {
	# 	'name': 'metroplaces_dev.db',
	# 	# 'engine': 'peewee.SqliteDatabase',
	# 	'check_same_thread': False,
	# 	'engine': 'APSWDatabase',
	# }
	DATABASE = {
		'name': 'places_dev',
		'engine': 'peewee.PostgresqlModel',
		'user':'metro',
		'password':'m3tr0n3t',
	}
	ASSETS_MINIFY = True
	ASSETS_USE_CDN = False

class ProductionConfig(BaseConfig):
	# DATABASE = {
	# 	'name': 'metroplaces_prod.db',
	# 	# 'engine': 'peewee.SqliteDatabase',
	# 	'check_same_thread': False,
	# 	'engine': 'APSWDatabase',
	# }
	DATABASE = {
		'name': 'places_prod',
		'engine': 'peewee.PostgresqlModel',
		'user':'metro',
		'password':'m3tr0n3t',
	}
	DEBUG = False
	PROPAGATE_EXCEPTIONS = True

	ASSETS_MINIFY = True
	ASSETS_USE_CDN = True
