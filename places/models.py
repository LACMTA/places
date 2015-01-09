import pytz
import time
from datetime import datetime
import simplejson as json
import geopy
from geopy.geocoders import GoogleV3
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

from database import db

def set_stamp():
	d = datetime.now()
	stamp = (int(time.mktime(d.timetuple())) *1000) +(d.microsecond/100)
	print "set the stamp to %s" %(stamp)
	return int( stamp )

class Category(db.Model):
	"""Categories are groups of places."""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	description = db.Column(db.String(255))
	stamp = db.Column(db.Integer, default=set_stamp() ) # 1417737461016
	active =  db.Column(db.Boolean(), default=True)

	resource_fields = {
		# for swagger
		'name': fields.String(),
		'description': fields.String(),
		'stamp': fields.Integer(),
		'active': fields.Boolean(),
	}

	def save(self, *args, **kwargs):
		# save() method never gets called -- sqlalchemy?
		self.stamp = set_stamp()
		return super(Category, self).save(*args, **kwargs)

	def __repr__(self):
		return '<Category %r>' % (self.name)

	def __unicode__(self):
		return self.name

	def mydict(self):
		return {
			'name':self.name,
			'description':self.description,
		}

"""
id = db.Column(db.Integer, primary_key=True)
email = db.Column(db.String(50))
name = db.Column(db.String(50))
addresses = db.relationship(
	'Address', 
	backref='person',
	lazy='dynamic',
	)
"""

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
	name = db.Column(db.String(50))
	description = db.Column(db.String(255))
	stamp = db.Column(db.Integer, default=set_stamp() ) # 1417737461016
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
	stamp = db.Column(db.Integer, default=set_stamp() ) # 1417737461016
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
		geolocator = GoogleV3()
		addrstr = "%s %s, %s %s" %(address,city, state, zipcode)		
		try:
			print "{{{{{{{{{{{{{ _geocode() }}}}}}}}}}}}}"
			loc = geolocator.geocode(addrstr)
			print loc
			self.lat = loc.latitude
			self.lon = loc.longitude
			db.session.commit()
			return loc.latitude,loc.longitude
		except Exception, e:
			print "GEOCODER FAIL: %s. Maybe try setting the proxy?" %(e)
			myg.set_proxy('mtaweb.metro.net:8118')
			loc = geolocator.geocode(addrstr)
			return 0.0,0.0

	# def save(self, *args, **kwargs):
	# 	print "LET'S SAVE!"
	# 	address = kwargs.get('address',"1 Gateway Plaza")
	# 	city = kwargs.get('city',"Los Angeles")
	# 	state = kwargs.get('state',"CA")
	# 	zipcode = kwargs.get('zipcode',"90012")
	# 	lat = kwargs.get('lat',0.0)
	# 	lon = kwargs.get('lon',0.0)
	# 	self.stamp = set_stamp()
	# 	if (lat==0.0):
	# 		self._geocode(address,city,state,zipcode)
	# 	return super(Place, self).save(*args, **kwargs)

	
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
	
	@property
	def myCategory(self):
		# legacy feature
		maincat = self.categories[0]
		return {
			'name':maincat.name,
			'description':maincat.description,
		}


	# @property
	# def myfeatures(self):
	# 	# myp=Place.get(Place.id==1)
	# 	# SELECT feature.name, feature.description FROM feature,placefeatures,place
	# 	# WHERE ((placefeatures.feature_id = feature.id) AND (place.id = 1));
	# 	q=(Feature
	# 		.select()
	# 		.join(PlaceFeatures, on=PlaceFeatures.feature)
	# 		.where(PlaceFeatures.place==self))
	# 	return [ feat.__dict__() for feat in q ]
	#
	#
	# def __repr__(self):
	# 	return '<Place %r>' % (self.name)
	#
	# def __unicode__(self):
	# 	return self.name

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

