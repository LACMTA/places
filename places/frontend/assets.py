from flask_assets import Environment, Bundle


#: application css bundle
css_places = Bundle("less/places.less",
                       filters="less", output="css/places.css",
                       debug=False)

#: consolidated css bundle
css_all = Bundle("css/bootstrap.min.css", css_places,
                 "css/bootstrap-theme.min.css",
                 "css/leaflet.css",
                 filters="cssmin", output="css/places.min.css")

#: vendor js bundle
js_vendor = Bundle("js/jquery-1.11.1.min.js",
                   "js/bootstrap.min.js",
                   "js/underscore-min.js",
                   "js/leaflet.js",
                   filters="jsmin", output="js/vendor.min.js")

#: application js bundle
# js_main = Bundle("coffee/*.coffee", filters="coffeescript", output="js/main.js")


def init_app(app):
    webassets = Environment(app)
    webassets.register('css_all', css_all)
    webassets.register('js_vendor', js_vendor)
    # webassets.register('js_main', js_main)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug

