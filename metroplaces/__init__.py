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
	SqliteDatabase,
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
# Flask restful
from flask.ext.restful import (
	reqparse, 
	abort, 
	# Api,
	Resource, 
	fields,
	marshal_with,
	)
from flask_restful_swagger import swagger
from werkzeug.contrib.fixers import ProxyFix

from metroplaces.config import BaseConfig, DevelopmentConfig, ProductionConfig
from metroplaces.utils.api import Api, JsonResource
from metroplaces.utils import (
	slugify, 
	ReverseProxied,
	wtf,
	# crossdomain,
	)

# Expose API constructs through this module
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Create database connection object
db = SqliteDatabase('metroplaces.sqlite', check_same_thread=False)

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
wtf.add_helpers(app)


# Bootstrap helpers
def alert_class_filter(category):
	# Map different message types to Bootstrap alert classes
	categories = {
		"message": "warning"
	}
	return categories.get(category, category)


app.jinja_env.filters['alert_class'] = alert_class_filter


# Admin interface
# class SecuredAdminIndexView(AdminIndexView):
# 	def is_accessible(self):
# 		return current_user.has_role("admin")
#
#
# class SecuredModelView(ModelView):
# 	def is_accessible(self):
# 		return current_user.has_role("admin")


# Automatically include views, files and APIs
# include_files = set(["views.py", "models.py", "api.py"])
#
# for root, dirname, files in os.walk(app.config["BASEDIR"]):
# 	for filename in files:
# 		if filename in include_files:
# 			relative = os.path.relpath(os.path.join(root, filename))[:-3]
# 			module = ".".join(relative.split(os.sep))
# 			__import__(module, level=-1)
#
# for cls in model_classes:
# 	admin.add_view(SecuredModelView(cls, db.session,
# 		category="CRUD"))
#

# api = Api(app)
###################################
# This is important:
api = swagger.docs(Api(app),
	apiVersion='0.1',
	api_spec_url='/api/spec',
	description='Metro Places API',
	# basePath='http://localhost:5000/api/v1',
	# resourcePath='/',
	produces=["application/json", "text/html"],
	)
###################################
parser = reqparse.RequestParser()

def abort_if_place_doesnt_exist(place_id):
	if not Place.select().where(Place.id==place_id).count():
		abort(404, message="Place {} doesn't exist".format(place_id))
	else:
		return Place.get(Place.id==place_id)

def abort_if_category_doesnt_exist(cat_name):
	if not Category.select().where(Category.name==cat_name).count():
		abort(404, message="Category {} doesn't exist".format(cat_name))
	else:
		return Category.get(Category.name==cat_name)

def get_metas(Amodel):
	(minstamp,maxstamp,ct) = Amodel.select(
		fn.Min(Amodel.stamp), fn.Max(Amodel.stamp), fn.Count(Amodel.stamp), 
	).scalar(as_tuple=True)
	return {
			"version": maxstamp,
			"maxstamp": maxstamp,
			"minstamp": minstamp,
			"count": ct,
			"model": str(Amodel),
		}

# PlaceList
#   shows a list of all Places
class PlaceList(JsonResource):
	paginate_by=1000
	allowed_methods=['GET', 'POST', 'PUT', 'HEAD']

	@swagger.operation(
		notes="""Use this method to all active places.""",
		responseClass=Place.__name__,
		nickname='place list',
		parameters=[],
		responseMessages=[
			{
				"code": 201,
				"message": "Created. The URL should be in the Location header"
			},
			{
				"code": 405,
				"message": "Invalid input"
			}
		]
	)
	def get(self):
		metas = get_metas(Place)
		mps = Place.select().where(Place.active == True)
		placelist = [ p.__dict__() for p in mps]
		return { "meta": metas,"objects": placelist }
api.add_resource(PlaceList, 
	'/api/place',
	'/api/place/',
	)


# CategoryList
#   shows a list of all Places
class CategoryList(JsonResource):
	paginate_by=1000
	allowed_methods=['GET', 'POST', 'PUT', 'HEAD']

	@swagger.operation(
		notes="""Use this method to list all active categories.""",
		responseClass=Category.__name__,
		nickname='category list',
		parameters=[],
		responseMessages=[
			{
				"code": 201,
				"message": "Created. The URL should be in the Location header"
			},
			{
				"code": 405,
				"message": "Invalid input"
			}
		]
	)
	def get(self):
		metas = get_metas(Category)
		mps = Category.select()
		catlist = [
			{
				'name': p.name,
				'description': p.description,
			}
			for p in mps]
		return { "meta": metas,"objects": catlist }
		
api.add_resource(CategoryList, 
	'/api/category',
	'/api/category/',
	)


# CatPlaces
#   shows a list of all Places in a specific category
class CatPlaces(JsonResource):

	@swagger.operation(
		notes='Use this method to list places by category.',
		responseClass=Place.__name__,
		nickname='place-by-category',
		parameters=[
			{
				"name": "category name",
				"description": "YAML.",
				"required": True,
				"allowMultiple": False,
				"dataType": Category.__name__,
				"paramType": "category name"
			}
			],
			responseMessages=[
			{
				"code": 201,
				"message": "Created. The URL should be in the Location header"
			},
			{
				"code": 405,
				"message": "Invalid input"
			}
		]
	)
	def get(self,cat_name):
		mycat = abort_if_category_doesnt_exist(cat_name)
		metas = get_metas(Place)
		mps = Place.select().where(Place.category == mycat).where(Place.active == True)
		placelist = [p.__dict__() for p in mps]
		return { "meta": metas,"objects": placelist }

	# def post(self):
	# 	pass

api.add_resource(CatPlaces, 
	'/api/category/<string:cat_name>',
	'/api/category/<string:cat_name>/',
	)

# Place
#   single place: edit, delete
class APlace(JsonResource):

	@swagger.operation(
		notes='Use this methodget info on a single place.',
		responseClass=Place.__name__,
		nickname='place-by-category',
		parameters=[
			{
				"name": "place id",
				"description": "YAML.",
				"required": True,
				"allowMultiple": False,
				"dataType": Place.__name__,
				"paramType": "place id"
			}
			],
			responseMessages=[
			{
				"code": 201,
				"message": "Created. The URL should be in the Location header"
			},
			{
				"code": 405,
				"message": "Invalid input"
			}
		]
	)
	def get(self, place_id):
		p = abort_if_place_doesnt_exist(place_id)
		return p.__dict__()


	# def put(self, place_id):
	# 	msg=""
	# 	l = abort_if_place_doesnt_exist(place_id)
	# 	return {
	# 		'title':l.title,
	# 		'presentation_id':l.id,
	# 		'score':l.get_score(),
	# 		'session':l.sessn.title,
	# 		'vendor':l.vendor.title,
	# 		'msg':msg,
	# 		'bluh':bluh,
	# 		'email':current_user.email,
	# 	},201

api.add_resource(APlace, 
	'/api/place/<int:place_id>',
	'/api/place/<int:place_id>/',
	)
