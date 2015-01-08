from flask import Flask, render_template, request, url_for, redirect
from flask.ext.security import (
	SQLAlchemyUserDatastore, 
	Security, 
	login_required, 
	current_user, 
	logout_user,
	)
from flask.ext.security.utils import encrypt_password, verify_password
from flask.ext.login import user_logged_in
from flask.ext.admin import (
	BaseView, 
	expose, 
	Admin,
	)
from flask_jwt import JWT, jwt_required
from flask.ext.principal import Principal, Permission, RoleNeed
from flask_restful_swagger import swagger

from database import db
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
from places.api import (
	Api, 
	JsonResource,
	PlaceList,
	PlaceMeta,
	CategoryList,
	CatPlaces,
	CategoryMeta,
	APlace,
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

# Configuration  ==============================================================
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Setup Flask-Principal  =======================================================
# load the extension
principals = Principal(app)
# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))
tapadmin_permission = Permission(RoleNeed('tapadmin'))

# Setup Flask-Security  =======================================================
security = Security(app, user_datastore)

# JWT Token authentication  ===================================================
jwt = JWT(app)
@jwt.authentication_handler
def authenticate(username, password):
	user = user_datastore.find_user(email=username)
	if username == user.email and verify_password(password, user.password):
		return user
	return None

@jwt.user_handler
def load_user(payload):
	user = user_datastore.find_user(id=payload['user_id'])
	return user

# Views  ======================================================================
@app.route('/')
def home():
	return render_template('index.html')

@app.route('/mypage')
@login_required
def mypage():
	return render_template('mypage.html')

@app.route('/logout')
def log_out():
	logout_user()
	return redirect(request.args.get('next') or '/')

# api = Api(app)
###################################
# This is important for Swagger
api = swagger.docs(Api(app),
	apiVersion='0.1',
	api_spec_url='/api/spec',
	description='Metro Places API',
	# basePath='http://localhost:5000/api/v1',
	# resourcePath='/',
	produces=["application/json", "text/html"],
	)
###################################

# API routes
api.add_resource(PlaceList, 
	'/api/place',
	'/api/place/',
	)
api.add_resource(APlace, 
	'/api/place/<int:place_id>',
	'/api/place/<int:place_id>/',
	)
api.add_resource(CategoryMeta, 
	'/api/category/<string:cat_name>/meta',
	'/api/category/<string:cat_name>/meta/',
	)
api.add_resource(PlaceMeta, 
	'/api/place/meta',
	'/api/place/meta/',
	)
api.add_resource(CategoryList, 
	'/api/category',
	'/api/category/',
	)
api.add_resource(CatPlaces, 
	'/api/category/<string:cat_name>',
	'/api/category/<string:cat_name>/',
	)

# Flask-Admin  ================================================================
admin = Admin(app,name='Metro Places')

admin.add_view(UserModelView(User, db.session, category='Auth'))
admin.add_view(AdminModelView(Role, db.session, category='Auth'))
admin.add_view(PlaceAdmin(Place, db.session))
admin.add_view(CategoryAdmin(Category, db.session))
admin.add_view(FeatureAdmin(Feature, db.session))
admin.add_view(LogoutView(name='Logout', endpoint='logout'))
admin.add_view(LoginView(name='Login', endpoint='login'))

# Bootstrap  ==================================================================
def init_app():
	db.init_app(app)
	db.create_all()

def create_test_models():
	user_datastore.create_user(email='test', password=encrypt_password('test'))
	user_datastore.create_user(email='test2', password=encrypt_password('test2'))
	db.session.commit()

@app.before_first_request
def bootstrap_app():
	if not app.config['TESTING']:
		if db.session.query(User).count() == 0:
			create_test_models();

# Start server  ===============================================================
if __name__ == '__main__':		
	with app.app_context():
		init_app()
	app.run()
