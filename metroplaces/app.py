import os, os.path
import datetime
import simplejson as json
import logging
from flask import (
	Flask,
	# Blueprint,
	Response,
	session,
	get_flashed_messages,
	jsonify,
	request,
	render_template,
	redirect,
	# g,
)
from peewee import (
	Model, 
	CharField, 
	# BlobField,
	BooleanField, 
	TextField, 
	FloatField,
	IntegerField,
	TextField,
	# UUIDField,
	ForeignKeyField,
	DateTimeField,
	fn,
	)
from flask_security.core import current_user
from flask_security.utils import logout_user
from flask.ext.security import (
	Security,
	PeeweeUserDatastore,
	UserMixin, 
	RoleMixin, 
	login_required,
	)
from flask.ext import assets as webassets
from flask.ext.mail import Mail, Message
from flask_restful_swagger import swagger
# from werkzeug.contrib.fixers import ProxyFix

from metroplaces.mpassets import (
	css_all,
	js_vendor,
	# js_main,
	)
from metroplaces.utils import (
	slugify, 
	ReverseProxied,
	add_helpers,
	# crossdomain,
	)

# Expose API constructs through this module
app = Flask(__name__)

# #####################################################
# CHOOSE CONFIGURATION HERE
# #####################################################
# Look in the config.py for these classes
app.config.from_object('config.DevelopmentConfig')
# app.config.from_object('config.ProductionConfig')
# #####################################################

# database bindings have been stored in the config file!
db = app.config['DB']

from metroplaces.models import (
	User,
	Role,
	UserRoles,
	Category,
	Place,
	PlaceFeatures,
	Feature,
	# Tag,
	# TagRelationship,
)

from metroplaces.api import (
	Api, 
	JsonResource,
	PlaceList,
	PlaceMeta,
	CategoryList,
	CatPlaces,
	CategoryMeta,
	APlace,
	)

# parser = reqparse.RequestParser()

# Setup Flask-Security
user_datastore = PeeweeUserDatastore(db, User, Role, UserRoles)
app.security = Security(app, user_datastore)

# Flask Extensions
mail = Mail(app)

# WSGI
# app.wsgi_app = ReverseProxied(app.wsgi_app)

# Asset bundles
assets = webassets.Environment(app)
assets.register('css_all', css_all)
assets.register('js_vendor', js_vendor)
# webassets.register('js_main', js_main)
assets.manifest = 'cache' if not app.debug else False
assets.cache = not app.debug
assets.debug = app.debug

# Coffee Scripts
scripts_path = os.path.abspath(os.path.join(app.config["BASEDIR"],
	"static/scripts"))

coffee_scripts = ["scripts/%s" % (f, )
		for f in os.listdir(scripts_path) if f.endswith(".coffee")]

assets.register("coffee_scripts", webassets.Bundle(*coffee_scripts,
				filters=("coffeescript,rjsmin" if app.config["ASSETS_MINIFY"]
					else "coffeescript"),
				output="scripts/generated.js"))

# Less stylesheets
styles_path = os.path.abspath(os.path.join(app.config["BASEDIR"],
	"static/styles"))

less_stylesheets = ["styles/%s" % (f, )
		for f in os.listdir(styles_path) if f.endswith(".less")]

assets.register("less_stylesheets", webassets.Bundle(*less_stylesheets,
				filters=("less,cssmin" if app.config["ASSETS_MINIFY"]
					else "less"),
				output="styles/generated.css"))


# Sending templated emails
def send_mail(destination, subject, template, **template_kwargs):
	text = flask.render_template("{0}.txt".format(template), **template_kwargs)

	logging.info("Sending email to {0}. Body is: {1}".format(
		destination, repr(text)[:50]))

	msg = Message(
		subject,
		recipients=[destination]
	)

	msg.body = text
	msg.html = flask.render_template("{0}.html".format(template),
			**template_kwargs)

	mail.send(msg)


# WTForms helpers
add_helpers(app)


# Bootstrap helpers
def alert_class_filter(category):
	# Map different message types to Bootstrap alert classes
	categories = {
		"message": "warning"
	}
	return categories.get(category, category)


app.jinja_env.filters['alert_class'] = alert_class_filter

@app.route('/')
def hello():
	placelist = [p for p in Place.select().where(Place.active == True)]
	return render_template('index.html', places=placelist, placelist=placelist)


# api = Api(app)
###################################
# This is important for Swagger
api = swagger.docs(Api(app),
	apiVersion='0.1',
	api_spec_url='/api/spec',
	description='Metro Places API',
	# basePath='http://localhost:5000/api/v1',
	# resourcePath='/',
	produces=["application/json", "text/html"],
	)
###################################

# API routes
api.add_resource(PlaceList, 
	'/api/place',
	'/api/place/',
	)
api.add_resource(APlace, 
	'/api/place/<int:place_id>',
	'/api/place/<int:place_id>/',
	)
api.add_resource(CategoryMeta, 
	'/api/category/<string:cat_name>/meta',
	'/api/category/<string:cat_name>/meta/',
	)
api.add_resource(PlaceMeta, 
	'/api/place/meta',
	'/api/place/meta/',
	)
api.add_resource(CategoryList, 
	'/api/category',
	'/api/category/',
	)
api.add_resource(CatPlaces, 
	'/api/category/<string:cat_name>',
	'/api/category/<string:cat_name>/',
	)
