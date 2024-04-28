#!/usr/bin/python3
"""app module"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_flask(exception):
    """end event listener"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """Handles the 404 error"""
    return jsonify(error='Not found'), 404


if __name__ == "__main__":
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=app_host, port=app_port, threaded=True)
