from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask.signals import request_started

bp = Blueprint('weather-data', __name__, url_prefix='/weather_data')

@bp.route('/')
def test():
    return "Testing"

@bp.route('/lat=<float(signed=true):lat>/lon=<float(signed=true):lon>', methods=('GET', 'POST'))
def display_data(lat, lon):
    return "lat = {}, lon = {}".format(lat, lon)
