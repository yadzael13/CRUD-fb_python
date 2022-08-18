__author__ = "Hiram Yadzael Vargas Chalico"
__copyright__ = "yadza_dev"
__version__ = "1"
__maintainer__ = "Hiram Yadzael Vargas Chalico"
__github__ = "yadzael13"
__status__ = "dev"

# standard library
from datetime import datetime
import pytz
import os
# flask library
from flask_cors import CORS
from flask import Flask
# blueprints routes
from services.routes.v1.paths import v1
# flask app
app = Flask(__name__)
CORS(app)

app.register_blueprint(v1, url_prefix="/v1")

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    utc_now = datetime.utcnow()
    utc_now = utc_now.astimezone(pytz.timezone('America/Mexico_City'))
    print(utc_now)
    #app.run(threaded=True, host='0.0.0.0', port=port, debug=True)
    app.run(debug=True, host='0.0.0.0', port=port)
