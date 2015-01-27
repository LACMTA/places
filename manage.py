import os, sys, csv
sys.path.append('/var/www/envs/places')
from flask.ext.script import Manager, Server, Shell
from flask_security.utils import encrypt_password

from app import create_app
from database import db
from places.models import (
	Category,
	Place,
	Feature,
	# Tag,
	# TagRelationship,
)
from models import (
	User, 
	Role, 
	)

# application = create_app('development')
application = create_app('production')

manager = Manager(application)
# manager.add_command("migrate", ManageMigrations())
manager.add_command("runserver", Server(host='0.0.0.0', port=5000))
manager.add_command("shell", Shell())

# Bootstrap  ==================================================================
@manager.command
def init_app():
	db.init_app(application)
	db.create_all()

@manager.command
def add_stations():
	"""
		Add the station features, categories, 
		then add the stations
	"""
	rails= Category(name='railstations',description='Rail Stations')
	db.session.add(rails)
	locker_f= Feature(name='bikelockers',description='Bike Lockers')
	db.session.add(locker_f)
	stations=csv.DictReader(open('data/railstations.csv','rU'), delimiter=",")
	"""['stop_id',
		 'stop_code',
		 'stop_name',
		 'stop_desc',
		 'stop_lat',
		 'stop_lon',
		 'stop_url',
		 'location_type',
		 'parent_station',
		 'tpis_name']"""
	for row in stations:
		try:
			myfeatures = [locker_f]
			comment = "parent_station:%s" %(row['parent_station'])
			vndr=Place(name=row['stop_name'],
				lat=row['stop_lat'],
				lon=row['stop_lon'],
				features=myfeatures,
				categories=[rails],
				comment=comment,
				)
			vndr._reversegeocode(row['stop_lat'],row['stop_lon'])
			print vndr.name
			db.session.add(vndr)
		except Exception as e:
			print "blargh! %s" %(e)
	# Now, COMMIT!
	db.session.commit()

@manager.command
def add_places():
	"""
		Add the vendor features, categories, 
		then add the vendors
	"""
	# categories
	tapv= Category(name='tapvendors',description='TAP Vendors')
	db.session.add(tapv)
	# features
	avta_passes= Feature(name='avta_passes',description='AVTA Passes')
	ctc_coupons= Feature(name='ctc_coupons',description='CTC Coupons')
	ez_passes= Feature(name='ez_passes',description='EZ Passes')
	foothilltransit_passes= Feature(name='foothilltransit_passes',description='Foothill Transit Passes')
	ladot_passes= Feature(name='ladot_passes',description='LADOT Passes')
	longbeachtransit_passes= Feature(name='longbeachtransit_passes',description='Long Beach Transit Passes')
	metro_passes= Feature(name='metro_passes',description='Metro Passes')
	metrolink_passes= Feature(name='metrolink_passes',description='Metrolink Passes')
	montebello_passes= Feature(name='montebello_passes',description='Montebello Passes')
	rrtp_coupons= Feature(name='rrtp_coupons',description='Rider Relief Coupons')
	santaclaritatransit_passes= Feature(name='santaclaritatransit_passes',description='Santa Clarita Transit Passes')
	# add 'em to the db session
	db.session.add(avta_passes)
	db.session.add(ctc_coupons)
	db.session.add(ez_passes)
	db.session.add(foothilltransit_passes)
	db.session.add(ladot_passes)
	db.session.add(longbeachtransit_passes)
	db.session.add(metro_passes)
	db.session.add(metrolink_passes)
	db.session.add(montebello_passes)
	db.session.add(rrtp_coupons)
	db.session.add(santaclaritatransit_passes)
	# get the vendors from a csv
	tapvendors_csv = csv.reader(open("data/tapvendors.csv"), delimiter=",")
	# loop over 'em and add them to the db session
	for name,street,city,zipcode,phone,features,comments in tapvendors_csv:
		try:
			fl=features[1:-1].split(',')
			myfeatures = [eval(x) for x in fl]
			vndr=Place(name=name,
				address=street,
				city=city,
				zipcode=zipcode,
				phone=phone,
				features=myfeatures,
				categories=[tapv],
				comment=comments,
				)
			vndr._geocode(street,city,'CA',zipcode)
			print vndr.name
			db.session.add(vndr)
		except Exception as e:
			print "blargh! %s" %(e)
	# Now, COMMIT!
	db.session.commit()

"""
	name = db.Column(db.String(50))
	description = db.Column(db.String(255))
	address = db.Column(db.String(128))
	city = db.Column(db.String(40),default='Los Angeles')
	state = db.Column(db.String(2),default='CA')
	lat = db.Column(db.Float(10,6),default=0.0)
	lon = db.Column(db.Float(10,6),default=0.0)
	zipcode = db.Column(db.String(10),default='90012')
	phone = db.Column(db.String(16),default='2135551212')
	active =  db.Column(db.Boolean())
	comment = db.Column(db.String(255))
"""


@manager.command
def add_admin(email='test@email.com',firstname='Testy',lastname='Test',password='test'):
	"""Add an admin user to your database_string"""
	# add_admin --email=goodwind@metro.net --firstname=Doug --lastname=Goodwin --password=
	print "got email=%s,firstname=%s,lastname=%s,password=%s" %(email,firstname,lastname,password)
	epass = encrypt_password(email)
	print "pass set to: %s" %(epass)

	# set up the admin role if necessary
	try:
		admin_role = Role.query.filter(Role.name=='admin').first()
	except:
		admin_role = Role(name='admin',description='Administrator')
		db.session.add(admin_role)
		db.session.commit()
		
	# add this user unless s/he already exists
	try:
		admin = User(email=email,
			firstname=firstname,
			lastname=lastname,
			password=epass,
			active=True,
			roles=[admin_role],
			)
		db.session.add(admin)
		db.session.commit()
	except:
		admin = User.query.filter(User.email==email).first()
	

	print "Created admin user: %s" % (admin, )

@manager.command
def add_tapadmin(email='test@email.com',firstname='Testy',lastname='Test',password='test'):
	"""Add a TAP admin user to your database_string"""
	# add_tapadmin --email=goodwind@metro.net --firstname=Doug --lastname=Goodwin --password=
	print "got email=%s,firstname=%s,lastname=%s,password=%s" %(email,firstname,lastname,password)
	epass = encrypt_password(email)
	print "pass set to: %s" %(epass)

	# set up the tapadmin role if necessary
	try:
		tapadmin_role = Role(name='tapadmin',description='TAP Administrator')
		db.session.add(tapadmin_role)
		db.session.commit()
	except:
		tapadmin_role = Role.query.filter(name=='tapadmin').first()
		
	# add this user unless s/he already exists
	try:
		tapadmin = User(email=email,
			firstname=firstname,
			lastname=lastname,
			password=epass,
			active=True,
			roles=[tapadmin_role],
			)
		db.session.add(tapadmin)
		db.session.commit()
	except:
		tapadmin = User.query.filter(email==email).first()
		# need to merge() in the tapadmin_role here!



if __name__ == "__main__":
	import logging
	logging.basicConfig()
	logging.getLogger().setLevel(logging.DEBUG)

	manager.run()



"""
import csv
import os, sys
sys.path.append('/var/www/envs/places')
from flask.ext.script import Manager, Server, Shell
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from app import create_app
# application = create_app('development')
application = create_app('production')

from flask import Flask, render_template, request, url_for, redirect
from models import (
	User, 
	Role, 
	SomeStuff, 
	user_datastore,
	)
from places.models import (
	Category, 
	Feature, 
	Place,
	)

from database import db


def init_app():
	db.init_app(application)
	db.create_all()

with application.app_context():
	init_app()
"""
