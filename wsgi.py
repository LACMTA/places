import os
from metroplaces.app import (
	app,
	)
from metroplaces.admin import (
	admin,
	create_tables,
	UserAdmin,
	PlaceAdmin,
	)

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
