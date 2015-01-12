import os, sys
sys.path.append('/var/www/envs/places')

from app import create_app
application = create_app('production')

# Start server  ===============================================================
if __name__ == '__main__':		
	application.run()
