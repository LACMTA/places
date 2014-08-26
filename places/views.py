import os,re,csv,datetime, time
import simplejson as json

from flask import Flask,request,render_template,jsonify,redirect,url_for,send_from_directory

from places import app, api, auth, admin
from places.models import Place

def get_places():
    places = Place.select().where(Place.active == True)
    return places

@app.route("/")
def index():
    places = get_places()
    return render_template('index.html', places=places)

# /<department>/<product>/<service>/


