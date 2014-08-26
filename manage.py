from flask.ext.script import Manager

from places import app, auth
from places.models import Place, Department, Product, Service

manager = Manager(app)

@manager.command
def hello():
    print "hello"

@manager.command
def runserver():
    app.run()

@manager.command
def initdb():
    from variables import vendorlist,department_tap,product_pass,service_sales
    auth.User.create_table(fail_silently=True)
    # create the admin user
    try:
        adminu = auth.User.get_or_create(username='admin', password='admin', email='', admin=True, active=True)
        adminu.set_password('admin')
        adminu.save()
    except:
        adminu = auth.User.get_or_create(username='admin')
        adminu.set_password('admin')
        print "admin user exists: %s" %(adminu.username)
        
    Department.create_table(fail_silently=True)
    Product.create_table(fail_silently=True)
    Service.create_table(fail_silently=True)
    Place.create_table(fail_silently=True)
    
    for vendor in vendorlist:
        print "INSERT: %s" %(vendor)
        Place.insert(**vendor).execute()






if __name__ == "__main__":
    manager.run()