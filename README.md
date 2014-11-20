# places.metro.net

This is a start on a PLACES service to the LACMTA. It uses Google's Places API as inspiration and includes friendly Admin pages and a map. 

These places are authorized vendors for TAP cards. The list was taken from an Excel spreadsheet, and the latitude/longitude was looked up using Google's Geocoding service.

	# load TAP vendor file
	import csv
	csvfile='tapvendors.csv'
	input_file = csv.DictReader(open(csvfile))
	# prepare geocoder
	from pygeocoder import Geocoder
	myg=Geocoder(api_key='akjshdjashdkjhasd')
	myg.set_proxy('mtaweb.metro.net:8123')
	for r in input_file:
	    streetzip = "%s,%s"    %(r['STREET'],r['ZIP'])
	    results = myg.geocode(streetzip)
	    lat,lon = results[0].coordinates[0],results[0].coordinates[1]
	    vdict = {'address' : r['STREET'],
	        'city' : r['CITY'],
	        'comment' : r['RESTRICTIONS'],
	        'department' : department_tap,
	        'lat' : lat,
	        'lon' : lon,
	        'name' :r['VENDOR_NAME'],
	        'phone' :r['PHONE'],
	        'product' : product_pass,
	        'service' : service_sales,
	        'state' :r['STATE'],
	        'zipcode' :r['ZIP']}
	    Place.insert(**vdict).execute()


## Demo

Set up the environment and load the fixture data:

	cd places
	virtualenv .
	. bin/activate
	pip install -r requirements.txt
	sudo npm install less -g
	python manage.py add_admin admin@metro.net 4DM1N ; python manage.py add_places
	python manage.py runserver	

### Now you can access the frontpage:

[places homepage](http://127.0.0.1:5000/)

### The admin pages are here:

[places admin](http://127.0.0.1:5000/admin/)
	username: admin@metro.net
	pass: 4DM1N


### The API is here:

[places API](http://127.0.0.1:5000/api/place/)

## Docker

Nevermind: we abandoned Docker for Chef. 

-Follow steps one and two on instructions for installing Dokku on Digital Ocean slice: [Use the Dokku One-Click DigitalOcean Image to Deploy a Python/Flask App](https://www.digitalocean.com/community/tutorials/how-to-use-the-dokku-one-click-digitalocean-image-to-deploy-a-python-flask-app)-

-Then cd into your sourcecode and push the app to DO:-

	git remote add places dokku@107.170.234.105:places
	git push places master

## API

Quick documentation:

The structure of the JSON goes like this: 

	{
		meta: {
			version: 1409359669640,
			model: "place",
			previous: "",
			page: 1,
			count: 384,
			next: ""
		},
		objects: []
	}

meta.version is an integer derived from the timestamp of the last updated place. It will increase every time an entry has changed and when one is added. . 
meta.count is an integer that tell you the total number of vendors.

note that meta.version will not change when a vendor is removed. you will need to check meta.count in that case.  

objects is a list of place objects:

	{
		active: true,
		address: "11151 Avalon Blvd. Suite #108",
		category: {
			active: true,
			description: "TAP Vendors",
			name: "tapvendors"
		},
		city: "Los Angeles",
		comment: "No EZ Passes",
		department: 2,
		description: null,
		features: [
			{
				description: "EZ Passes",
				name: "ezpasses"
			},
			{
				description: "Senior Passes",
				name: "seniorpasses"
			}
		],
		id: 1,
		lat: 33.933915,
		lon: -118.265179,
		name: "1% Check Cashing",
		phone: "3237772067",
		product: 1,
		pub_date: "2014-11-20 11:15:07.013884",
		service: 1,
		stamp: 1416510907138,
		state: "CA",
		uid: 1416510907138,
		zipcode: "90012"
	}

Most of the keys will be familiar. department, product and service are internal keys: they will change. 
