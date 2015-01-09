from flask.ext.admin.form import rules
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.security import current_user
from flask import redirect
from flask.ext.security import logout_user
from flask.ext.admin import (
	BaseView, 
	expose, 
	)

from database import db
from models import (
	User, 
	Role, 
	user_datastore,
	)
from places.models import (
	Category, 
	Feature, 
	Place,
	set_stamp
	)

class MyBase(BaseView):
	def __init__(self, def_view, *args, **kwargs):
		self._default_view = def_view
		super(MyBase, self).__init__(*args, **kwargs)

class LogoutView(BaseView):
	@expose('/')
	def index(self):
		logout_user()
		return redirect('/admin/')

	def is_visible(self):
		return current_user.is_authenticated()

class LoginView(BaseView):
	@expose('/')
	def index(self):
		logout_user()
		return redirect('/login?next=/admin/')

	def is_visible(self):
		return not current_user.is_authenticated()

class AdminModelView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated()

class UserModelView(AdminModelView):
	column_list = ('email', 'active', 'last_login_at', 'roles', )

class PlaceAdmin(AdminModelView):
	# Visible columns in the list view
	foreign_key_lookups = {
		'feature': 'name',
		'category': 'name',
	}
	column_searchable_list = ( Place.name, Place.city )
	form_rules = [
		rules.FieldSet(('name', 'address', 'city', 'state','zipcode','phone'), 'Place Location (lat/lng will be determined from the address)'),
		rules.FieldSet(('features','categories','active'), 'add features, set the category and status'),
		rules.FieldSet(('description','comment','url'), 'optional information'),
		]
	def after_model_change(self, form, model,is_created):
		model.stamp = set_stamp()
		if is_created:
			# set the lat and lon
			print "get the lat and lng!"
			print form.address.data
			address=form.address.data
			city=form.city.data
			state=form.state.data
			zipcode=form.zipcode.data
			model.lat, model.lon = model._geocode(address,city,state,zipcode)
		else:
			# just update the stamp (above)
			pass
		db.session.commit()


class CategoryAdmin(AdminModelView):
	# Visible columns in the list view
	# form_create_rules = ('name', 'description','active')
	# form_edit_rules = ('name', 'description','active')
	column_searchable_list = ( Category.name, Category.description )
	column_exclude_list = ['stamp']
	form_rules = [
		# Define field set with header text and three fields
		rules.FieldSet(('name', 'description','active'), 'Place Category'),
		# ... and it is just shortcut for:
		# rules.Header('User'),
		# rules.Field('first_name'),
		# rules.Field('last_name'),
		# ...
		# It is possible to create custom rule blocks:
		#MyBlock('Hello World'),
		# It is possible to call macros from current context
		# rules.Macro('my_macro', foobar='baz')
		]

	def after_model_change(self, form, model,is_created):
		model.stamp = set_stamp()
		db.session.commit()

class FeatureAdmin(AdminModelView):
	# Visible columns in the list view
	# form_create_rules = ('name', 'description')
	# form_edit_rules = ('name', 'description')
	column_searchable_list = ( Feature.name, Feature.description )
	column_exclude_list = ['stamp']
	form_rules = [
		# Define field set with header text and three fields
		rules.FieldSet(('name', 'description'), 'Place Feature'),
		]

	def after_model_change(self, form, model,is_created):
		model.stamp = set_stamp()
		db.session.commit()

