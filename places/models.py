import datetime, time

from flask_peewee.admin import Admin, ModelAdmin
from flask_peewee.auth import BaseUser
from flask_peewee.rest import RestResource, UserAuthentication
from peewee import FloatField, DateTimeField, TextField, BooleanField, IntegerField, CharField, ForeignKeyField, fn

# from flask import Blueprint, abort, request, Response, session, redirect, url_for, g
from flask import request

from places import db, admin, api, api_auth

class Department(db.Model):
	name = CharField(default='TAP')

	def __unicode__(self):
		return self.name
		
class Product(db.Model):
	name = CharField(default='Pass')

	def __unicode__(self):
		return self.name

class Service(db.Model):
	name = CharField(default='Sales')

	def __unicode__(self):
		return self.name

class Place(db.Model):
	d = datetime.datetime.now()
	mystamp = int( (int(time.mktime(d.timetuple())) *1000) +(d.microsecond/100))
	stamp = IntegerField(default=mystamp)
	uid = IntegerField(default=mystamp)
	lat = FloatField(default=0.0)
	lon = FloatField(default=0.0)
	name = CharField(default='anonymous',max_length=50)
	address = CharField(default='1 Gateway Plaza',max_length=255)
	city = CharField(default='Los Angeles',max_length=50)
	state = CharField(default='CA',max_length=2)
	zipcode = CharField(default='90012',max_length=10)
	phone = CharField(default='2135551212',max_length=16)
	pub_date = DateTimeField(default=datetime.datetime.now)
	active = BooleanField(default=True)
	comment = TextField(default='')
	
	# FKs
	department = ForeignKeyField(Department, related_name = 'departments')
	product = ForeignKeyField(Product, related_name = 'products')
	service = ForeignKeyField(Service, related_name = 'services')

	# we also do this in the admin
	def save(self, *args, **kwargs):
		# override the dave method so we can set the stamp
		# the stamp will be used to set the version
		d = datetime.datetime.now()
		stamp = int( (int(time.mktime(d.timetuple())) *1000) +(d.microsecond/100))
		self.stamp = stamp
		return super(Place, self).save(*args, **kwargs)

	def __unicode__(self):
		return '[%f,%f,%s]' % (self.lat, self.lon, self.name)

# admin.register(Place) # register "Place" with vanilla ModelAdmin
class PlaceAdmin(ModelAdmin):
	columns = ['name','lat', 'lon']
	foreign_key_lookups = {
		'department': 'name',
		'product': 'name',
		'service': 'name',		
	}
admin.register(Place, PlaceAdmin)

# Department table
class DepartmentAdmin(ModelAdmin):
	columns = ['name']
admin.register(Department, DepartmentAdmin)

# Product table
class ProductAdmin(ModelAdmin):
	columns = ['name']
admin.register(Product, ProductAdmin)

# Service table
class ServiceAdmin(ModelAdmin):
	columns = ['name']
admin.register(Service, ServiceAdmin)






# after all models and panels are registered, configure the urls
admin.setup()

# Exclude the uid from the resource listing
class PlaceResource(RestResource):
	paginate_by=1000
#	 exclude = ('uid')

	def get_request_metadata(self, paginated_query):
		"""override this method to add some more meta info"""
		var = paginated_query.page_var
		request_arguments = request.args.copy()

		current_page = paginated_query.get_page()
		next = previous = ''

		if current_page > 1:
			request_arguments[var] = current_page - 1
			previous = url_for(self.get_url_name('api_list'), **request_arguments)
		if current_page < paginated_query.get_pages():
			request_arguments[var] = current_page + 1
			next = url_for(self.get_url_name('api_list'), **request_arguments)

		maxstamp = Place.select( fn.Max(Place.stamp) ).scalar()
		placecount = Place.select().count()
		
		return {
			'model': self.get_api_name(),
			'page': current_page,
			'version': maxstamp,
			'count': placecount,
			'previous': previous,
			'next': next,
		}

# register our models so they are exposed via /api/<model>/
# api.register(Comment, auth=api_auth, allowed_methods=['GET', 'POST', 'PUT'])
api.register(Place, PlaceResource, auth=api_auth, allowed_methods=['GET', 'POST', 'PUT', 'HEAD'])

class ProductResource(RestResource):
	paginate_by=200
api.register(Product, ProductResource, auth=api_auth, allowed_methods=['GET', 'POST', 'PUT'])

class DepartmentResource(RestResource):
	paginate_by=200
api.register(Department, DepartmentResource, auth=api_auth, allowed_methods=['GET', 'POST', 'PUT'])

class ServiceResource(RestResource):
	paginate_by=200
api.register(Service, ServiceResource, auth=api_auth, allowed_methods=['GET', 'POST', 'PUT'])


# configure the urls
api.setup()
