import pytz
import time
from datetime import datetime
import simplejson as json
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
	)
from flask.ext.security import (
	Security,
	PeeweeUserDatastore,
	UserMixin, 
	RoleMixin, 
	login_required,
	)
from flask.ext.restful import (
	reqparse, 
	abort, 
	# Api,
	Resource, 
	fields,
	marshal_with,
	)
from flask_restful_swagger import swagger

# from metroplaces import app, db, api
from metroplaces import db

def set_stamp():
	d = datetime.now()
	return int( (int(time.mktime(d.timetuple())) *1000) +(d.microsecond/100))

class BaseModel(Model):
	class Meta:
		database = db

# @swagger.model
@swagger.model
class Category(BaseModel):
	"""Categories are groups of places."""
	name = CharField(unique=True)
	description = TextField(null=True)
	active = BooleanField(default=True)
	stamp = IntegerField( default=set_stamp() )

	resource_fields = {
		# for swagger
		'name': fields.String(),
		'description': fields.String(),
		'active': fields.Boolean(),
		'stamp': fields.Integer(),
	}

	def save(self, *args, **kwargs):
		self.stamp = set_stamp()
		return super(Category, self).save(*args, **kwargs)

	def __repr__(self):
		return '<Category %r>' % (self.name)

	def __unicode__(self):
		return self.name

	def __dict__(self):
		return {
			'name':self.name,
			'description':self.description,
			'active':self.active,
		}

class Role(BaseModel, RoleMixin):
	name = CharField(unique=True)
	description = TextField(null=True)

	def __repr__(self):
		return '<User %r>' % (self.name)

	def __unicode__(self):
		return self.name

class User(BaseModel, UserMixin):
	email = TextField()
	password = TextField(default='MetroTechLA')
	active = BooleanField(default=True)
	confirmed_at = DateTimeField(null=True)
	
	@property
	def admin(self):
		return self.has_role('admin')

	@property
	def is_admin(self):
		return self.has_role('admin')

	def __repr__(self):
		return '<User %r>' % (self.email)

	def __unicode__(self):
		return self.email

class UserRoles(BaseModel):
	# Because peewee does not come with built-in many-to-many
	# relationships, we need this intermediary class to link
	# user to roles.
	user = ForeignKeyField(User, related_name='roles')
	role = ForeignKeyField(Role, related_name='users')
	name = property(lambda self: self.role.name)
	description = property(lambda self: self.role.description)
	
	def __repr__(self):
		return '<User %r, Role %r>' % (self.user.email, self.role.name)

	def __unicode__(self):
		return '(%r,%r)' % (self.user.email, self.role.name)

@swagger.model
class Feature(BaseModel, RoleMixin):
	"""Places have Features"""
	name = CharField(unique=True)
	description = TextField(null=True)

	resource_fields = {
		# for swagger
		'name': fields.String(),
		'description': fields.String(),
	}

	def __repr__(self):
		return '<Feature %r>' % (self.name)

	def __unicode__(self):
		return self.name

	def __dict__(self):
		return {
			'name':self.name,
			'description':self.description,
		}

@swagger.model
class Place(BaseModel):
	"""Places are stable locations describable by addresses and lat/lon points"""
	name = CharField()
	description = TextField(null=True)
	pub_date = DateTimeField( default=datetime.now() )
	stamp = IntegerField( default=set_stamp() )
	address = CharField(null=True)
	city = CharField(default='Los Angeles')
	state = CharField(max_length=2,default='CA')
	lat = FloatField(default=0.0)
	lon = FloatField(default=0.0)
	zipcode = CharField(default='90012')
	phone = CharField(default='2135551212',max_length=16)
	active = BooleanField(default=True)
	comment = TextField(default='')
	url = CharField(null=True)
	
	# FKs
	category = ForeignKeyField(Category, related_name = 'categories', default=1)

	resource_fields = {
		# for swagger
		'name': fields.String(),
		'description': fields.String(),
		# 'category': fields.Integer(),
		'pub_date': fields.DateTime( default=datetime.now() ),
		'address': fields.String(),
		'state': fields.String(),
		'city': fields.String(),
		'lat': fields.Float(default=0.0),
		'lon': fields.Float(default=0.0),
		'zipcode': fields.String(default='90012'),
		'active': fields.Boolean(default=True),
		'comment': fields.String(default=''),
		'url': fields.String(),
	}

	def _geocode(self, address,city,state,zipcode):
		from geopy.geocoders import Nominatim, GeocoderDotUS
		addrstr = "%s %s, %s %s" %(address,city, state, zipcode)
		try:
			geolocator = Nominatim()
			loc = geolocator.geocode(addrstr)
			self.lat = loc.latitude
			self.lon = loc.longitude
		except Exception, e:
			print "FAIL: %s. Maybe try GeocoderDotUS?" %(e)
			try:
				geolocator = GeocoderDotUS()
				loc = geolocator.geocode(addrstr)
				self.lat = loc.latitude
				self.lon = loc.longitude
			except Exception, e:
				pass
				print "FAIL: %s. Maybe try google geocoder?" %(e)

	# we also do this in the admin
	def save(self, *args, **kwargs):
		address = kwargs.get('address',"1 Gateway Plaza")
		city = kwargs.get('city',"Los Angeles")
		state = kwargs.get('state',"CA")
		zipcode = kwargs.get('zipcode',"90012")
		lat = kwargs.get('lat',0.0)
		lon = kwargs.get('lon',0.0)
		self.stamp = set_stamp()
		self.pub_date = datetime.now()
		if (self.lat == 0.0):
			self._geocode(address,city,state,zipcode)
		return super(Place, self).save(*args, **kwargs)

	@property
	def myfeatures(self):
		myfeatures = (PlaceFeatures
			.select(Feature)
			.join(Feature)
			.switch(PlaceFeatures)
			.join(Place))
		return json.dumps(myfeatures)
		
	def __repr__(self):
		return '<Place %r>' % (self.name)

	def __unicode__(self):
		return self.name

	def __dict__(self):
		return {
			'name':self.name,
			'description':self.description,
			'active':self.active,
			'address':self.address,
			'city':self.city,
			'state':self.state,
			'lat':self.lat,
			'lon':self.lon,
			'lon':self.lon,
			# 'features':self.myfeatures,
			'category':self.category.__dict__(),
		}

@swagger.model
class PlaceFeatures(BaseModel):
	# Because peewee does not come with built-in many-to-many
	# relationships, we need this intermediary class to link
	# user to roles.
	place = ForeignKeyField(Place, related_name='placefeatures')
	feature = ForeignKeyField(Feature, related_name='features')
	name = property(lambda self: self.feature.name)
	description = property(lambda self: self.feature.description)
	
	class Meta:
		indexes = (
			# Specify a unique multi-column index on from/to-user.
			(('place', 'feature'), True),
		)

	resource_fields = {
		# for swagger
		'name': fields.String(),
		'description': fields.String(),
		'place': fields.Integer(),
		'feature': fields.Integer(),
	}

	def __repr__(self):
		return '<Place %r, Feature %r>' % (self.place.name, self.feature.name)

	def __unicode__(self):
		return '(%r,%r)' % (self.place.name, self.feature.name)

# class Tag(BaseModel):
# 	tag = CharField()
#
# 	def __repr__(self):
# 		return '<Tag %r>' % (self.tag)
#
# 	def __unicode__(self):
# 		return self.tag
#
# class TagRelationship(BaseModel):
# 	relPlace = ForeignKeyField(Place)
# 	relTag   = ForeignKeyField(Tag)
#
