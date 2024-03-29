from hashlib import sha1
import math
import random
import re
import sys
import simplejson as json
import dateutil.parser
import traceback
import pytz

from flask import (
	Flask,
	abort,
	render_template,
	request,
	)
from peewee import (
	ForeignKeyField,
	Model,
	SelectQuery,
	)
from flask.ext import restful
from flask_security.core import current_user
# Helpers for form generation
from wtforms.fields import HiddenField, BooleanField

def add_helpers(app):
	def is_hidden_field_filter(field):
		return isinstance(field, HiddenField)

	def is_boolean_field_filter(field):
		return isinstance(field, BooleanField)

	app.jinja_env.filters['is_hidden_field'] = is_hidden_field_filter
	app.jinja_env.filters['is_boolean_field'] = is_boolean_field_filter


def slugify(text, delim=u'_'):
	"""Generates an ASCII-only slug."""
	from unidecode import unidecode
	_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
	result = []
	for word in _punct_re.split(text.lower()):
		result.extend(unidecode(word).split())
	return unicode(delim.join(result))
	

def get_object_or_404(query_or_model, *query):
	if not isinstance(query_or_model, SelectQuery):
		query_or_model = query_or_model.select()
	try:
		return query_or_model.where(*query).get()
	except DoesNotExist:
		abort(404)

def object_list(template_name, qr, var_name='object_list', **kwargs):
	pq = PaginatedQuery(qr, kwargs.pop('paginate_by', 20))
	kwargs[var_name] = pq.get_list()
	return render_template(template_name, pagination=pq, page=pq.get_page(), **kwargs)


# class PaginatedQuery(object):
# 	page_var = 'page'
#
# 	def __init__(self, query_or_model, paginate_by):
# 		self.paginate_by = paginate_by
#
# 		if isinstance(query_or_model, SelectQuery):
# 			self.query = query_or_model
# 			self.model = self.query.model_class
# 		else:
# 			self.model = query_or_model
# 			self.query = self.model.select()
#
# 	def get_page(self):
# 		curr_page = request.args.get(self.page_var)
# 		if curr_page and curr_page.isdigit():
# 			return int(curr_page)
# 		return 1
#
# 	def get_pages(self):
# 		return int(math.ceil(float(self.query.count()) / self.paginate_by))
#
# 	def get_list(self):
# 		return self.query.paginate(self.get_page(), self.paginate_by)
#
#
# def get_next():
# 	if not request.query_string:
# 		return request.path
# 	return '%s?%s' % (request.path, request.query_string)
#
# def slugify(s):
# 	return re.sub('[^a-z0-9_\-]+', '-', s.lower())

def load_class(s):
	print "{{{{{{{{{{{{{{{{{{{{ load_class(s) }}}}}}}}}}}}}}}}}}}}"
	print s
	path, klass = s.rsplit('.', 1)
	__import__(path)
	mod = sys.modules[path]
	return getattr(mod, klass)

def get_dictionary_from_model(model, fields=None, exclude=None):
	model_class = type(model)
	data = {}

	fields = fields or {}
	exclude = exclude or {}
	curr_exclude = exclude.get(model_class, [])
	curr_fields = fields.get(model_class, model._meta.get_field_names())

	for field_name in curr_fields:
		if field_name in curr_exclude:
			continue
		field_obj = model_class._meta.fields[field_name]
		field_data = model._data.get(field_name)
		if isinstance(field_obj, ForeignKeyField) and field_data and field_obj.rel_model in fields:
			rel_obj = getattr(model, field_name)
			data[field_name] = get_dictionary_from_model(rel_obj, fields, exclude)
		else:
			data[field_name] = field_data
	return data

def get_model_from_dictionary(model, field_dict):
	if isinstance(model, Model):
		model_instance = model
		check_fks = True
	else:
		model_instance = model()
		check_fks = False
	models = [model_instance]
	for field_name, value in field_dict.items():
		field_obj = model._meta.fields[field_name]
		if isinstance(value, dict):
			rel_obj = field_obj.rel_model
			if check_fks:
				try:
					rel_obj = getattr(model, field_name)
				except field_obj.rel_model.DoesNotExist:
					pass
				if rel_obj is None:
					rel_obj = field_obj.rel_model
			rel_inst, rel_models = get_model_from_dictionary(rel_obj, value)
			models.extend(rel_models)
			setattr(model_instance, field_name, rel_inst)
		else:
			setattr(model_instance, field_name, field_obj.python_value(value))
	return model_instance, models

def path_to_models(model, path):
	accum = []
	if '__' in path:
		next, path = path.split('__')
	else:
		next, path = path, ''
	if next in model._meta.rel:
		field = model._meta.rel[next]
		accum.append(field.rel_model)
	else:
		raise AttributeError('%s has no related field named "%s"' % (model, next))
	if path:
		accum.extend(path_to_models(model, path))
	return accum


# borrowing these methods, slightly modified, from django.contrib.auth
def get_hexdigest(salt, raw_password):
	data = salt + raw_password
	return sha1(data.encode('utf8')).hexdigest()

# def make_password(raw_password):
# 	salt = get_hexdigest(text_type(random.random()), text_type(random.random()))[:5]
# 	hsh = get_hexdigest(salt, raw_password)
# 	return '%s$%s' % (salt, hsh)

def check_password(raw_password, enc_password):
	salt, hsh = enc_password.split('$', 1)
	return hsh == get_hexdigest(salt, raw_password)
	
	
## EXCEPTIONS
class ImproperlyConfigured(Exception):
	print "Database ImproperlyConfigured!"
	pass




class ReverseProxied(object):
	'''Wrap the application in this middleware and configure the 
	front-end server to add these headers, to let you quietly bind 
	this to a URL other than / and to an HTTP scheme that is 
	different than what is used locally.

	In nginx:
	location /myprefix {
		proxy_pass http://192.168.0.1:5001;
		proxy_set_header Host $host;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Scheme $scheme;
		proxy_set_header X-Script-Name /myprefix;
		}

	:param app: the WSGI application
	'''
	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
		if script_name:
			environ['SCRIPT_NAME'] = script_name
			path_info = environ['PATH_INFO']
			if path_info.startswith(script_name):
				environ['PATH_INFO'] = path_info[len(script_name):]

		scheme = environ.get('HTTP_X_SCHEME', '')
		if scheme:
			environ['wsgi.url_scheme'] = scheme
		return self.app(environ, start_response)




def get_object_or_404(query_or_model, *query):
	if not isinstance(query_or_model, SelectQuery):
		query_or_model = query_or_model.select()
	try:
		return query_or_model.where(*query).get()
	except DoesNotExist:
		abort(404)

def object_list(template_name, qr, var_name='object_list', **kwargs):
	pq = PaginatedQuery(qr, kwargs.pop('paginate_by', 20))
	kwargs[var_name] = pq.get_list()
	return render_template(template_name, pagination=pq, page=pq.get_page(), **kwargs)


class PaginatedQuery(object):
	page_var = 'page'

	def __init__(self, query_or_model, paginate_by):
		self.paginate_by = paginate_by

		if isinstance(query_or_model, SelectQuery):
			self.query = query_or_model
			self.model = self.query.model_class
		else:
			self.model = query_or_model
			self.query = self.model.select()

	def get_page(self):
		curr_page = request.args.get(self.page_var)
		if curr_page and curr_page.isdigit():
			return int(curr_page)
		return 1

	def get_pages(self):
		return int(math.ceil(float(self.query.count()) / self.paginate_by))

	def get_list(self):
		return self.query.paginate(self.get_page(), self.paginate_by)


def get_next():
	if not request.query_string:
		return request.path
	return '%s?%s' % (request.path, request.query_string)

def slugify(s):
	return re.sub('[^a-z0-9_\-]+', '-', s.lower())

def load_class(s):
	path, klass = s.rsplit('.', 1)
	__import__(path)
	mod = sys.modules[path]
	return getattr(mod, klass)

def get_dictionary_from_model(model, fields=None, exclude=None):
	model_class = type(model)
	data = {}

	fields = fields or {}
	exclude = exclude or {}
	curr_exclude = exclude.get(model_class, [])
	curr_fields = fields.get(model_class, model._meta.get_field_names())

	for field_name in curr_fields:
		if field_name in curr_exclude:
			continue
		field_obj = model_class._meta.fields[field_name]
		field_data = model._data.get(field_name)
		if isinstance(field_obj, ForeignKeyField) and field_data and field_obj.rel_model in fields:
			rel_obj = getattr(model, field_name)
			data[field_name] = get_dictionary_from_model(rel_obj, fields, exclude)
		else:
			data[field_name] = field_data
	return data

def get_model_from_dictionary(model, field_dict):
	if isinstance(model, Model):
		model_instance = model
		check_fks = True
	else:
		model_instance = model()
		check_fks = False
	models = [model_instance]
	for field_name, value in field_dict.items():
		field_obj = model._meta.fields[field_name]
		if isinstance(value, dict):
			rel_obj = field_obj.rel_model
			if check_fks:
				try:
					rel_obj = getattr(model, field_name)
				except field_obj.rel_model.DoesNotExist:
					pass
				if rel_obj is None:
					rel_obj = field_obj.rel_model
			rel_inst, rel_models = get_model_from_dictionary(rel_obj, value)
			models.extend(rel_models)
			setattr(model_instance, field_name, rel_inst)
		else:
			setattr(model_instance, field_name, field_obj.python_value(value))
	return model_instance, models

def path_to_models(model, path):
	accum = []
	if '__' in path:
		next, path = path.split('__')
	else:
		next, path = path, ''
	if next in model._meta.rel:
		field = model._meta.rel[next]
		accum.append(field.rel_model)
	else:
		raise AttributeError('%s has no related field named "%s"' % (model, next))
	if path:
		accum.extend(path_to_models(model, path))
	return accum


# ################################
# Exceptions
# ################################
class ImproperlyConfigured(Exception):
	pass