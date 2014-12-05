from metroplaces.app import app
from metroplaces.models import (
	User,
	Role,
	UserRoles,
	Category,
	Place,
	PlaceFeatures,
	Feature,
	# Tag,
	# TagRelationship,
)
from flask.ext.admin import (
	Admin, 
	AdminIndexView,
	)
from flask.ext.admin.contrib.peewee import ModelView

class UserAdmin(ModelView):
	# Visible columns in the list view
	column_exclude_list = ['password']

class PlaceAdmin(ModelView):
	# Visible columns in the list view
	foreign_key_lookups = {
		'feature': 'name',
		'category': 'name',
	}
	column_searchable_list = ( Place.name, Place.city )
	# place_category = relationship("w_accounts", backref=db.backref('categories', lazy='dynamic'))
	# column_select_related_list = ('place_category',)


admin = Admin(app, name='Metro Places')
admin.add_view(UserAdmin(User))
admin.add_view(ModelView(Role))
admin.add_view(ModelView(UserRoles))
admin.add_view(PlaceAdmin(Place))
admin.add_view(ModelView(Feature))
admin.add_view(ModelView(Category))
admin.add_view(ModelView(PlaceFeatures))
# admin.add_view(ModelView(Tag))
# admin.add_view(ModelView(TagRelationship))

def create_tables(mdb):
	# Create table for each model if it does not exist.
	# Use the underlying peewee database object instead of the
	# flask-peewee database wrapper:
	mdb.create_tables([User, Role, UserRoles, Category, Place, Feature, PlaceFeatures], safe=True)

