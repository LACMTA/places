from places import app

if __name__ == "__main__":
	app.run()
	
"""
ini file: 

command=uwsgi
  --socket /tmp/rodney.sock
  --logto /var/www/envs/stage/mullen/rodney/rodney/log/application.log
  --home /var/www/envs/stage/mullen/rodney/rodney/venv
  --pythonpath /var/www/envs/stage/mullen/rodney/rodney/src
  --wsgi-file /var/www/envs/stage/mullen/rodney/rodney/src/wsgi.py
  --callable wsgi
  --max-requests 1000
  --master
  --processes 1
  --chmod
directory=/Users/admin/code/places
autostart=true
autorestart=true
"""