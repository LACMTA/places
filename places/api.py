from sqlalchemy.sql import func
# from flask.ext import restful
from flask.ext import restplus
# from flask.ext.restplus import Api, Resource, fields
from functools import wraps
import types
from werkzeug.contrib.fixers import ProxyFix
from flask import (
	request,
)

from places.models import (
	# User,
	# Role,
	# UserRoles,
	Category,
	Place,
	Feature,
	# Tag,
	# TagRelationship,
)

class Api(restplus.Api):
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
	if not Place.query.filter(Place.id==place_id).count():
		restplus.abort(404, message="Place {} doesn't exist".format(place_id))
	else:
		return Place.query.filter(Place.id==place_id).first()

def abort_if_category_doesnt_exist(cat_name):
	if not Category.query.filter(Category.name==cat_name).count():
		restplus.abort(404, message="Category {} doesn't exist".format(cat_name))
	else:
		return Category.query.filter(Category.name==cat_name).first()

def get_metas(Amodel):
	(minstamp,maxstamp,ct) = Amodel.query.with_entities(
			func.min(Amodel.stamp),
			func.max(Amodel.stamp),
			func.count(Amodel.stamp),
		).filter(Amodel.active==True).first()
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


class JsonResource(restplus.Resource):
	"""
	A restful resource that merges any JSON data in the POST/PUT HTTP body to
	the request.values dictionary
	"""
	method_decorators = [
		json_data_wrapper,
		api_error_wrapper,
		api_helper_wrapper]


