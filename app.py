from flask import Flask, render_template, url_for
from flask_jwt import JWT
from flask.ext.admin import Admin
from flask.ext.principal import Principal
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.restplus import Api

from config import config
from models import (
	User, 
	Role, 
	)
from places.models import (
	Category, 
	Feature, 
	Place,
	)
from admin import (
	AdminModelView, 
	UserModelView, 
	LogoutView, 
	LoginView,
	PlaceAdmin,
	CategoryAdmin,
	FeatureAdmin,
	)
from places.api import (
	JsonResource,
	get_metas,
	)

db = SQLAlchemy()
principal = Principal()
security = Security()
jwt = JWT()
admin = Admin(name='Metro Places')
api = Api(
	contact='Douglas Goodwin <goodwind@metro.net>',
	license='',
	version='0.1',
	title='Metro Places API',
	description='The Metro Places webservice describes all Metro properties with a physical address',
	)

from config import config

def has_no_empty_params(rule):
	defaults = rule.defaults if rule.defaults is not None else ()
	arguments = rule.arguments if rule.arguments is not None else ()
	return len(defaults) >= len(arguments)
	
# API routes
# can we move these please?

# PlaceList | shows a list of all Places
@api.route('/api/place', endpoint='PlaceList')
@api.doc(params={})
class PlaceList(JsonResource):
	paginate_by=1000
	allowed_methods=['GET']

	def get(self):
		metas = get_metas(Place)
		mps = Place.query.filter(Place.active==True).all()
		placelist = [p.mydict() for p in mps]
		return { "meta": metas,"objects": placelist }

@api.route('/api/place/meta','/place/meta/')
@api.doc(params={})
class PlaceMeta(JsonResource):
	paginate_by=1000
	allowed_methods=['GET']

	def get(self):
		metas = get_metas(Place)
		return { "meta": metas }

# CategoryList | shows a list of all Place categories
@api.route('/api/category','/category/', endpoint='CategoryList')
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
@api.route('/api/category/<string:cat_name>','/category/<string:cat_name>/', endpoint='CatPlaces')
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


@api.route('/api/category/<string:cat_name>/meta/','/category/<string:cat_name>/meta', endpoint='CategoryMeta')
@api.doc(params={'cat_name': 'Place Category name'})
class CategoryMeta(JsonResource):
	paginate_by=1000
	allowed_methods=['GET']

	def get(self,cat_name):
		return get_metas(Place)

# Place | single place: edit, delete
@api.route('/api/place/<int:place_id>','/place/<int:place_id>/', endpoint='APlace')
@api.doc(params={'place_id': 'Metro places Place ID'})
class APlace(JsonResource):
	paginate_by=1000
	allowed_methods=['GET']

	def get(self, place_id):
		p = abort_if_place_doesnt_exist(place_id)
		return p.mydict()




def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	user_datastore = SQLAlchemyUserDatastore(db, User, Role)
	
	db.init_app(app)
	security.init_app(app,user_datastore)
	principal.init_app(app)
	jwt.init_app(app)
	api.init_app(app)
	admin.init_app(app)

	# attach routes and custom error pages here
	admin.add_view(UserModelView(User, db.session, category='Auth'))
	admin.add_view(AdminModelView(Role, db.session, category='Auth'))
	admin.add_view(PlaceAdmin(Place, db.session))
	admin.add_view(CategoryAdmin(Category, db.session))
	admin.add_view(FeatureAdmin(Feature, db.session))
	admin.add_view(LogoutView(name='Logout', endpoint='logout'))
	admin.add_view(LoginView(name='Login', endpoint='login'))

	@app.route("/site-map")
	def site_map():
		links = []
		for rule in app.url_map.iter_rules():
			# Filter out rules we can't navigate to in a browser
			# and rules that require parameters
			if "GET" in rule.methods and has_no_empty_params(rule):
				url = url_for(rule.endpoint)
				links.append((url, rule.endpoint))
		return render_template('site-map.html',links=links)


	return app

