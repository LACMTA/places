import os
from places import app

if __name__ == "__main__":
    port = int(os.environ.get(80))
    app.run(host='0.0.0.0', port=port)
