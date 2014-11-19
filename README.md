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

	cd places
	virtualenv .
	. bin/activate
	pip install -r requirements.txt
	sudo npm install less -g
	python manage.py runserver	

### Now you can access the frontpage:

[places homepage](http://127.0.0.1:5000/)

### The admin pages are here:

[places admin](http://127.0.0.1:5000/admin/)

### The API is here:

[places API](http://127.0.0.1:5000/api/place/)

## Docker

Follow steps one and two on instructions for installing Dokku on Digital Ocean slice: [Use the Dokku One-Click DigitalOcean Image to Deploy a Python/Flask App](https://www.digitalocean.com/community/tutorials/how-to-use-the-dokku-one-click-digitalocean-image-to-deploy-a-python-flask-app)

Then cd into your sourcecode and push the app to DO:

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
		state: "CA ",
		phone: "6269622625",
		active: true,
		address: "4100 Baldwin Park Blvd",
		uid: 1408040831273,
		lat: 34.085845,
		department: 1,
		id: 44,
		pub_date: "2014-08-14 11:27:09",
		product: 1,
		city: "Baldwin Park",
		comment: "",
		service: 1,
		name: "City of Baldwin Park",
		stamp: 1408040831273,
		zipcode: "91706",
		lon: -117.964368
	}

Most of the keys will be familiar. department, product and service are internal keys: they will change. 
