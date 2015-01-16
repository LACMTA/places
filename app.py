from flask import Flask, render_template, url_for
from flask.ext.admin import Admin
from flask.ext.principal import Principal
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask_security.utils import encrypt_password
from flask.ext import assets as webassets

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
from places.views import (
	Sitemap,
	Placemap,
	Railmap,
	TAPVendorsCSV,
	RailStationsCSV,
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
	api,
	)
from places.mpassets import (
	css_all,
	js_vendor,
	# js_main,
	)
from database import db

principal = Principal()
security = Security()
# jwt = JWT()
admin = Admin(name='Metro Places')
assets = webassets.Environment()

from config import config
	
def create_app(config_name):
	from models import (
		User, 
		Role, 
		)
	from places.models import (
		Category, 
		Feature, 
		Place,
		)

	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	user_datastore = SQLAlchemyUserDatastore(db, User, Role)

	security.init_app(app,user_datastore)
	principal.init_app(app)
	# jwt.init_app(app)
	api.init_app(app)
	admin.init_app(app)
	assets.init_app(app)
	assets.register('css_all', css_all)
	assets.register('js_vendor', js_vendor)

	with app.app_context():
		db.init_app(app)
		db.create_all()

		if not Role.query.first():
			admin_role = Role(name='admin',description='Administrator')
			db.session.add(admin_role)
			db.session.commit()
		else:
			admin_role = Role.query.filter(Role.name=='admin').first()

		if not User.query.first():
			user_datastore.create_user(
				email='goodwind@metro.net',
				password=encrypt_password('Haukola'),
				roles=[admin_role]
				)
			db.session.commit()

	# attach routes and custom error pages here
	admin.add_view(UserModelView(User, db.session, category='Auth'))
	admin.add_view(AdminModelView(Role, db.session, category='Auth'))
	admin.add_view(PlaceAdmin(Place, db.session))
	admin.add_view(CategoryAdmin(Category, db.session))
	admin.add_view(FeatureAdmin(Feature, db.session))
	admin.add_view(LogoutView(name='Logout', endpoint='logout'))
	admin.add_view(LoginView(name='Login', endpoint='login'))

	sitemap_view = Sitemap.as_view('sitemap')
	app.add_url_rule('/sitemap', view_func=sitemap_view)
	
	tapvendors_csv_view = TAPVendorsCSV.as_view('tapvendors_csv')
	app.add_url_rule('/csv/tapvendors', view_func=tapvendors_csv_view)
	railstations_csv_view = RailStationsCSV.as_view('railstations_csv')
	app.add_url_rule('/csv/railstations', view_func=railstations_csv_view)

	placemap_view = Placemap.as_view('placemap')
	app.add_url_rule('/placemap/', 
		view_func=placemap_view,
		methods=['GET'],
		)
	placemaptapvendors_view = Placemap.as_view('placemaptapvendors')
	app.add_url_rule('/placemap/tapvendors', 
		view_func=placemaptapvendors_view,
		methods=['GET'],
		)
	placemaprailstations_view = Railmap.as_view('placemaprailstations')
	app.add_url_rule('/placemap/railstations', 
		view_func=placemaprailstations_view,
		methods=['GET'],
		)

	return app

