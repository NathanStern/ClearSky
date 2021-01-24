from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask.signals import request_started
import requests
import json

bp = Blueprint('weather-data', __name__, url_prefix='/weather_data')

url_format = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=minutely,daily,alerts&appid=536159a5b4c02240e63a25443055734b&units=imperial"

@bp.route('/')
def test():
    return "Testing"

@bp.route('/lat=<float(signed=true):lat>/lon=<float(signed=true):lon>', methods=('GET', 'POST'))
def display_data(lat, lon):
    r = requests.get(url_format.format(lat, lon))
    return render_template('weatherpage/weather_data.html', lat = lat, lon = lon, json = r.text, url="http://slowe.github.io/VirtualSky/embed?longitude={}&latitude={}&projection=stereo&constellations=true&constellationlabels=true&showstarlabels=true".format(lon, lat))
  
