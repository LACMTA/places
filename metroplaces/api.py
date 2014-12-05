from flask.ext import restful
from flask_restful_swagger import swagger
from functools import wraps
import types
from werkzeug.contrib.fixers import ProxyFix
from flask import (
	# Flask,
	# # Blueprint,
	# Response,
	# session,
	# get_flashed_messages,
	# jsonify,
	request,
	# render_template,
	# redirect,
	# g,
)
from peewee import (
	# Model,
	# CharField,
	# # BlobField,
	# BooleanField,
	# TextField,
	# FloatField,
	# IntegerField,
	# TextField,
	# # UUIDField,
	# ForeignKeyField,
	# DateTimeField,
	fn,
	)

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

class Api(restful.Api):
	"""
	Flask Restful intercepts all exceptions and returns JSON error which is
	really annoying if we want to serve both an API and standard pages within
	the same project.

	Here we split the error handling based on the request path prefix. There
	are also convenience methods for
	"""
	def __init__(self, app, prefix='', default_mediatype='application/json',
			decorators=None):
		super(Api, self).__init__(app, prefix, default_mediatype, decorators)

		app.handle_exception = self.handle_exception
		app.handle_user_exception = self.handle_user_exception

	def handle_exception(self, e):
		if request.path.startswith(self.prefix):
			return super(Api, self).handle_error(e)

		if request.endpoint in self.endpoints:
			return super(Api, self).handle_error(e)
		else:
			return Flask.handle_exception(self.app, e)

	def handle_user_exception(self, e):
		if request.path.startswith(self.prefix):
			return super(Api, self).handle_error(e)

		if request.endpoint in self.endpoints:
			return super(Api, self).handle_error(e)
		else:
			return Flask.handle_user_exception(self.app, e)

	def serialize_date(self, date):
		if date:
			if current_user.is_active():
				utc = pytz.utc.localize(date)
				localized = utc.astimezone(current_user.get_tz())
				return localized.isoformat()
			return date.isoformat()

		return None

	def parse_date(self, date_string):
		if date_string:
			localized = dateutil.parser.parse(date_string)
			return localized.astimezone(pytz.utc).replace(tzinfo=None)

		return None


def abort_if_place_doesnt_exist(place_id):
	if not Place.select().where(Place.id==place_id).count():
		restful.abort(404, message="Place {} doesn't exist".format(place_id))
	else:
		return Place.get(Place.id==place_id)

def abort_if_category_doesnt_exist(cat_name):
	if not Category.select().where(Category.name==cat_name).count():
		restful.abort(404, message="Category {} doesn't exist".format(cat_name))
	else:
		return Category.get(Category.name==cat_name)

def get_metas(Amodel):
	(minstamp,maxstamp,ct) = Amodel.select(
		fn.Min(Amodel.stamp), fn.Max(Amodel.stamp), fn.Count(Amodel.stamp), 
	).where(Amodel.active == True).scalar(as_tuple=True)
	return {
			"version": maxstamp,
			"maxstamp": maxstamp,
			"minstamp": minstamp,
			"count": ct,
			"model": str(Amodel),
		}

def json_data_wrapper(method):
	"""
	Load JSON data from HTTP request bodies if possible
	"""
	if request.data:
		try:
			values = json.loads(request.data)
			if values:
				values.update(request.values.items())
				request.values = values
		except:
			traceback.print_exc()
			pass

	return method


class ApiError(Exception):
	"""
	An exception that sets the HTTP error code and returns a message
	"""
	def __init__(self, code, message):
		super(ApiError, self).__init__(message)
		self.code = code


def required_error(name):
	"""
	The error message presented when a required field is not present
	"""
	return "You must specify a value for {0}".format(" ".join(name.split("_")))


class ApiDict(dict):
	"""
	A thin dict wrapper that lets you use required to get params or throw
	ApiErrors
	"""

	def __init__(self, *args, **kwargs):
		super(ApiDict, self).__init__(*args, **kwargs)

	def required(self, name, error=None):
		val = self.get(name, None)

		if not val:
			raise ApiError(400, error or required_error(name))

		return val

	def optional(self, name, default=None):
		return self.get(name, default)


def api_error_wrapper(method):
	"""
	Return JSON error messages
	"""
	@wraps(method)
	def handle_error(*args, **kwargs):
		try:
			return method(*args, **kwargs)
		except ApiError, e:
			return {
				"status": e.code,
				"message": e.message
			}, e.code

	return handle_error


def api_helper_wrapper(method):
	"""
	Helpers for fetching paramaters and dictionaries out of a request object
	"""
	def required_dict(self, name, error=None):
		val = request.values.get(name, None)

		if not val:
			raise ApiError(400, error or required_error(name))

		return ApiDict(**val)

	def required(self, name, error=None):
		val = request.values.get(name, None)

		if not val:
			raise ApiError(400, error or required_error(name))

		return val

	def optional(self, name, default=None):
		return request.values.get(name, default)

	def optional_dict(self, name, default=None):
		return ApiDict(**request.values.get(name, default))

	request.required = types.MethodType(required, request,
		request.__class__)
	request.optional = types.MethodType(optional, request,
		request.__class__)
	request.required_dict = types.MethodType(required_dict, request,
		request.__class__)
	request.optional_dict = types.MethodType(optional_dict, request,
		request.__class__)

	return method


class JsonResource(restful.Resource):
	"""
	A restful resource that merges any JSON data in the POST/PUT HTTP body to
	the request.values dictionary
	"""

	method_decorators = [
		json_data_wrapper,
		api_error_wrapper,
		api_helper_wrapper]

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
		placelist = [ p.__dict__() for p in mps ]
		return { "meta": metas,"objects": placelist }




class PlaceMeta(JsonResource):
	paginate_by=1000
	allowed_methods=['GET']

	@swagger.operation(
		notes="""Use this method to get the latest version and other meta info.""",
		responseClass=Place.__name__,
		nickname='place meta',
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
		return { "meta": metas }

# CategoryList
#   shows a list of all Places
class CategoryList(JsonResource):
	paginate_by=1000
	allowed_methods=['GET']

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


class CategoryMeta(JsonResource):
	paginate_by=1000
	allowed_methods=['GET']

	def get(self,cat_name):
		mycat = abort_if_category_doesnt_exist(cat_name)
		(minstamp,maxstamp,ct) = Place.select(
			fn.Min(Place.stamp), fn.Max(Place.stamp), fn.Count(Place.stamp), 
		).where(Place.category == mycat).where(Place.active == True).scalar(as_tuple=True)
		return {
				"version": maxstamp,
				"maxstamp": maxstamp,
				"minstamp": minstamp,
				"count": ct,
				"model": str(Place),
			}



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

