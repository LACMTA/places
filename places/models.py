import pytz
from random import randrange
import time
from datetime import datetime
import simplejson as json
import geopy
from geopy.geocoders import GoogleV3, Nominatim
from flask.ext.security import (
	Security,
	# SQLAlchemyUserDatastore,
	# UserMixin,
	# RoleMixin,
	login_required,
	)
from flask.ext.restplus import (
	fields,
	)
from flask.ext.sqlalchemy import models_committed
from flask import current_app

from database import db

# everythign here is for updating timestamps on update
def set_stamp():
	d = datetime.now()
	# careful -- this may require a BigInteger
	stamp = (int(time.mktime(d.timetuple())) *10) +int( randrange(0, 10) )
	return int( stamp )

def update_instance(obj):
	obj.stamp = set_stamp()

def on_models_committed(sender, changes):
	 for model, change in changes:
		 update_instance(model)

models_committed.connect(on_models_committed, sender=current_app)
# END updating timestamps on update

class Category(db.Model):
	"""Categories are groups of places."""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50),unique=True)
	description = db.Column(db.String(255))
	stamp = db.Column(db.BigInteger, default=set_stamp() ) # 1417737461016
	active =  db.Column(db.Boolean(), default=True)

	resource_fields = {
		# for swagger
		'name': fields.String(),
		'description': fields.String(),
		'stamp': fields.Integer(),
		'active': fields.Boolean(),
	}

	def __repr__(self):
		return '<Category %r>' % (self.name)

	def __unicode__(self):
		return self.name

	def mydict(self):
		return {
			'name':self.name,
			'description':self.description,
		}

placefeatures = db.Table('placefeatures',
	db.Column('feature_id', db.Integer, db.ForeignKey('feature.id')),
	db.Column('place_id', db.Integer, db.ForeignKey('place.id'))
)
placecategories = db.Table('placecategories',
	db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
	db.Column('place_id', db.Integer, db.ForeignKey('place.id'))
)

class Feature(db.Model):
	"""Places have Features"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50),unique=True)
	description = db.Column(db.String(255))
	stamp = db.Column(db.BigInteger, default=set_stamp() ) # 1417737461016
	active =  db.Column(db.Boolean(), default=True)

	resource_fields = {
		# for swagger
		'name': fields.String(),
		'description': fields.String(),
		'stamp': fields.Integer(),
		'active': fields.Boolean(),
	}

	def __repr__(self):
		return '<Feature %r>' % (self.name)

	def __unicode__(self):
		return self.name

	def mydict(self):
		return {
			'name':self.name,
			'description':self.description,
		}

class Place(db.Model):
	"""Places are stable locations describable by addresses and lat/lon points"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	description = db.Column(db.String(255))
	stamp = db.Column(db.BigInteger, default=set_stamp() ) # 1417737461016
	active =  db.Column(db.Boolean(), default=True)
	#
	pub_date = db.Column(db.DateTime(), default=datetime.now() )
	address = db.Column(db.String(128))
	city = db.Column(db.String(40),default='Los Angeles')
	state = db.Column(db.String(2),default='CA')
	lat = db.Column(db.Float(10,6),default=0.0)
	lon = db.Column(db.Float(10,6),default=0.0)
	zipcode = db.Column(db.String(10),default='90012')
	phone = db.Column(db.String(16),default='2135551212')
	comment = db.Column(db.String(255))
	url = db.Column(db.String(255))

	def _geocode(self, address,city,state,zipcode):
		print "LET'S GEOCODE!"
		proxies = {"https":"mtaweb.metro.net:8118"}
		api_key="AIzaSyAJmxEb1O6GJMxP9QuhCc4-HV2aae2FolA"
		geolocator = GoogleV3(api_key=api_key)
		addrstr = "%s %s, %s %s" %(address,city, state, zipcode)		
		try:
			print "{{{{{{{{{{{{{ _geocode() }}}}}}}}}}}}}"
			loc = geolocator.geocode(addrstr)
			print loc
			self.lat = loc.latitude
			self.lon = loc.longitude
			self.stamp = set_stamp()
			db.session.commit()
			return loc.latitude,loc.longitude
		except Exception, e:
			proxies = {"http":"mtaweb.metro.net:8118"}
			geolocator = Nominatim()
			loc = geolocator.geocode(addrstr)
			print loc
			self.lat = loc.latitude
			self.lon = loc.longitude
			self.stamp = set_stamp()
			db.session.commit()
			return loc.latitude,loc.longitude

	
	def _reversegeocode(self, lat,lon):
		print "LET'S REVERSE GEOCODE!"
		proxies = {"https":"mtaweb.metro.net:8118"}
		api_key="AIzaSyAJmxEb1O6GJMxP9QuhCc4-HV2aae2FolA"
		geolocator = GoogleV3(api_key=api_key)
		latlonstr = "%s,%s" %(lat,lon)
		try:
			print "{{{{{{{{{{{{{ _reverse() }}}}}}}}}}}}}"
			loc = geolocator.reverse(latlonstr,exactly_one=True)
			print loc
			formatted = loc.raw['formatted_address'].split(',')
			# [u'127-191 West 1st Street', u' San Pedro', u' CA 90731', u' USA']
			self.address=formatted[0].strip()
			self.city=formatted[-3].strip()
			self.state='CA' 	# yucky
			self.zipcode=formatted[-2].strip().split(' ')[1] # ditto
			self.stamp = set_stamp()
			db.session.commit()
			return loc.raw['formatted_address']
		except Exception, e:
			print "GoogleV3 REVERSE GEOCODER FAIL: %s." %(e)
			try:
				proxies = {"http":"mtaweb.metro.net:8118"} # no SSL for Nominatim
				geolocator = Nominatim()
				location = geolocator.reverse(latlonstr,exactly_one=True)
				print location
				formatted = location.address.split(',')
				self.address="%s %s" %(formatted[1].strip(),formatted[2].strip())
				self.city=formatted[-4].strip()
				self.state='CA'
				self.zipcode=formatted[-2].strip()
				self.stamp = set_stamp()
				db.session.commit()
				return location.address
			except Exception, e:
				print "REVERSE GEOCODER FINAL FAIL: %s." %(e)
				return "1 Gateway Plaza, Los Angeles, CA"

	# FKs
	features = db.relationship('Feature', secondary=placefeatures, 
		backref=db.backref('placefeatures', lazy='dynamic'))
	categories = db.relationship('Category', secondary=placecategories, 
		backref=db.backref('placecategories', lazy='dynamic'))

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
	
	def get_featurelist(self):
		return ', '.join( [p.description for p in self.features] )
	
	def get_catlist(self):
		return ', '.join( [p.description for p in self.categories] )
	
	def get_serial(self):
		ser = ( self.name,self.address,self.city,self.state,self.zipcode,self.get_featurelist(),self.get_catlist() )
		return ser
	
	@property
	def myCategory(self):
		# legacy feature
		maincat = self.categories[0]
		return {
			'name':maincat.name,
			'description':maincat.description,
		}

	def mydict(self):
		return {
			'name':self.name,
			'id':self.id,
			'description':self.description,
			'active':self.active,
			'address':self.address,
			'city':self.city,
			'state':self.state,
			'zipcode':self.zipcode,
			'phone':self.phone,
			'lat':float(self.lat),
			'lon':float(self.lon),
			'stamp':self.stamp,
			'pub_date':str(self.pub_date),
			'comment':self.comment,
			'active':self.active,
			'features':[p.mydict() for p in self.features],
			'categories':[c.mydict() for c in self.categories],
			'category':self.myCategory,	# legacy
			# for backwards compatibility
		}

	def csvdict(self):
		return {
			'name':self.name,
			'id':self.id,
			'description':self.description,
			'active':self.active,
			'address':self.address,
			'city':self.city,
			'state':self.state,
			'zipcode':self.zipcode,
			'phone':self.phone,
			'lat':float(self.lat),
			'lon':float(self.lon),
			'stamp':self.stamp,
			'pub_date':str(self.pub_date),
			'comment':self.comment,
			'active':self.active,
			# 'features':[p.mydict() for p in self.features],
			# 'categories':[c.mydict() for c in self.categories],
			'categories':self.get_catlist(),
			'features':self.get_featurelist(),
			'category':self.myCategory['name'],	# legacy
			# for backwards compatibility
		}

