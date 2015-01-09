from datetime import timedelta
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	DEBUG = False
	TESTING = False
	SQLALCHEMY_DATABASE_URI = ''
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	APP_NAME = 'Metro Places'
	SECRET_KEY = 'this is a test'
	JWT_EXPIRATION_DELTA = timedelta(days=30)
	# JWT_AUTH_URL_RULE = '/api/v1/auth'
	SECURITY_REGISTERABLE = False
	SECURITY_RECOVERABLE = True
	SECURITY_TRACKABLE = True
	SECURITY_PASSWORD_HASH = 'sha512_crypt'
	SECURITY_PASSWORD_SALT = 'add_salt'

	@staticmethod
	def init_app(app):
		pass

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/db'

class DevelopmentConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
	DEBUG = True

class TestingConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'sqlite://'
	TESTING = True


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}
