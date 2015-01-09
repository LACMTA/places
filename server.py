# this works but you don't reall need it!
#
# use: uwsgi --ini uwsgi-dev.ini (uwsgi serves http on 127.0.0.1:5000)
# or
# python manage.py runserver

# import os, sys
# sys.path.append('/var/www/envs/places')
# from flask.ext.script import Manager, Server, Shell
# from flask_jwt import JWT
# from flask.ext.security import (
# 	SQLAlchemyUserDatastore,
# 	Security,
# 	login_required,
# 	current_user,
# 	logout_user,
# 	)
# from flask.ext.security.utils import encrypt_password, verify_password
#
# from app import create_app
# application = create_app('development')
#
# # database  ===================================================
# from database import db
#
# # JWT Token authentication  ===================================================
# jwt = JWT()
# @jwt.authentication_handler
# def authenticate(username, password):
# 	user = user_datastore.find_user(email=username)
# 	if username == user.email and verify_password(password, user.password):
# 		return user
# 	return None
#
# @jwt.user_handler
# def load_user(payload):
# 	user = user_datastore.find_user(id=payload['user_id'])
# 	return user
#
# # Views  ======================================================================
# @application.route('/')
# def home():
# 	return render_template('index.html')
#
# @application.route('/mypage')
# @login_required
# def mypage():
# 	return render_template('mypage.html')
#
# @application.route('/logout')
# def log_out():
# 	logout_user()
# 	return redirect(request.args.get('next') or '/')
#
# # Bootstrap  ==================================================================
# def init_app():
# 	db.init_app(application)
# 	db.create_all()
#
# # def create_test_models():
# # 	user_datastore.create_user(email='test', password=encrypt_password('test'))
# # 	user_datastore.create_user(email='test2', password=encrypt_password('test2'))
# # 	db.session.commit()
# #
# # @app.before_first_request
# # def bootstrap_app():
# # 	if not app.config['TESTING']:
# # 		if db.session.query(User).count() == 0:
# # 			create_test_models();
#
# # Start server  ===============================================================
# if __name__ == '__main__':
# 	with application.app_context():
# 		init_app()
# 	application.run()
