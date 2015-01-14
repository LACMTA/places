import cStringIO, csv
from flask import Flask, current_app, url_for, render_template, send_file
from flask.views import View
from flask.ext.restplus import (
	Resource,
	)

from places.api import (
	JsonResource,
	api,
	get_metas,
	abort_if_category_doesnt_exist,
	abort_if_place_doesnt_exist,
	)

from places.models import (
	Category,
	Place,
	Feature,
	# Tag,
	# TagRelationship,
)

def has_no_empty_params(rule):
	defaults = rule.defaults if rule.defaults is not None else ()
	arguments = rule.arguments if rule.arguments is not None else ()
	return len(defaults) >= len(arguments)


class Placemap(View):
	def dispatch_request(self,category='tapvendors'):
		mycat = abort_if_category_doesnt_exist(category)
		# mycat = Category.query.filter(Category.name==cat_name).filter(Category.active==True).count()
		mps = mycat.placecategories.all()
		placelist = [p for p in mps]
		return render_template('map.html', places=placelist, category=category)

class Sitemap(View):
	# like a class-based view
	def dispatch_request(self):
		links = []
		for rule in current_app.url_map.iter_rules():
			# Filter out rules we can't navigate to in a browser
			# and rules that require parameters
			if "GET" in rule.methods and has_no_empty_params(rule):
				url = url_for(rule.endpoint)
				links.append((url, rule.endpoint))
		return render_template('sitemap.html',links=links)

# API routes

# PlaceList | shows a list of all Places
@api.route('/api/place','/api/place/', endpoint='PlaceList')
@api.doc(params={})
class PlaceList(JsonResource):
	paginate_by=1000
	allowed_methods=['GET']

	def get(self):
		metas = get_metas(Place)
		mps = Place.query.filter(Place.active==True).all()
		placelist = [p.mydict() for p in mps]
		return { "meta": metas,"objects": placelist }

@api.route('/api/place/meta','/api/place/meta/', endpoint='PlaceMeta')
@api.doc(params={})
class PlaceMeta(JsonResource):
	paginate_by=1000
	allowed_methods=['GET']

	def get(self):
		metas = get_metas(Place)
		return { "meta": metas }

# CategoryList | shows a list of all Place categories
@api.route('/api/category','/api/category/', endpoint='CategoryList')
@api.doc(params={})
class CategoryList(JsonResource):
	paginate_by=1000
	allowed_methods=['GET']

	def get(self):
		metas = get_metas(Category)
		mps = Category.query.all()
		catlist = [
			{
				'name': p.name,
				'description': p.description,
			}
			for p in mps]
		return { "meta": metas,"objects": catlist }

# CatPlaces | shows a list of all Places in a specific category
@api.route('/api/category/<string:cat_name>','/api/category/<string:cat_name>/', endpoint='CatPlaces')
@api.doc(params={'cat_name': 'Place Category name'})
class CatPlaces(JsonResource):
	paginate_by=1000
	allowed_methods=['GET']

	def get(self,cat_name):
		mycat = abort_if_category_doesnt_exist(cat_name)
		metas = get_metas(Place)
		mps = mycat.placecategories.all()

		placelist = [p.mydict() for p in mps]
		return { "meta": metas,"objects": placelist }


class TAPVendorsCSV(View):
	# like a class-based view
	def dispatch_request(self,cat_name='tapvendors'):
		outfile = "%s.csv" %(cat_name)
		mycat = abort_if_category_doesnt_exist(cat_name)
		metas = get_metas(Place)
		mps = mycat.placecategories.all()

		placelist = [p.get_serial() for p in mps]
		dest = cStringIO.StringIO()
		writer = csv.writer(dest)
		for row in placelist:
			writer.writerow(row)

		dest.seek(0)
		return send_file(dest,
			attachment_filename=outfile,
			as_attachment=True)

@api.route('/api/category/<string:cat_name>/meta/','/api/category/<string:cat_name>/meta', endpoint='CategoryMeta')
@api.doc(params={'cat_name': 'Place Category name'})
class CategoryMeta(JsonResource):
	paginate_by=1000
	allowed_methods=['GET']

	def get(self,cat_name):
		return get_metas(Place)

# Place | single place: edit, delete
@api.route('/api/place/<int:place_id>','/api/place/<int:place_id>/', endpoint='APlace')
@api.doc(params={'place_id': 'Metro places Place ID'})
class APlace(JsonResource):
	paginate_by=1000
	allowed_methods=['GET']

	def get(self, place_id):
		p = abort_if_place_doesnt_exist(place_id)
		return p.mydict()
