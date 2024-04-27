#!/usr/bin/python3
"""A module that contains the index view"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def get_status():
    """get the status of the API"""
    return jsonify(status='OK')
