import os
from flask import Flask, render_template

from places.frontend import assets

# flask-peewee
from flask_peewee.auth import Auth
from flask_peewee.rest import RestAPI, UserAuthentication
from flask_peewee.db import Database
from flask_peewee.admin import Admin

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'static')

app = Flask(__name__, template_folder=tmpl_dir, static_folder=static_dir, static_url_path='/static')
assets.init_app(app)

app.config.from_object('config.ProductionConfig')
db = Database(app)

# needed for authentication
auth = Auth(app, db)
api_auth = UserAuthentication(auth, protected_methods=['PUT', 'DELETE'])

api = RestAPI(app, default_auth=api_auth)
admin = Admin(app, auth)

# from places import models, views

from places.models import Place
myplaces = Place.select()
placelist=[]
for p in myplaces:
    placelist.append([p.name,p.lat,p.lon])

@app.route('/')
def hello():
    return render_template('index.html', places=myplaces, placelist=placelist)
