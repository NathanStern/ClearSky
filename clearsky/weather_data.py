from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask.signals import request_started
import requests
import json

bp = Blueprint('weather-data', __name__, url_prefix='/weather_data')

# url_format = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=minutely,daily,alerts&appid={}&units=imperial"
# api_key = "536159a5b4c02240e63a25443055734b"
url_format = ""
api_key = ""


@bp.route('/')
def test():
    return "You need to enter geographical coordinates!"


@bp.route('/lat=<float(signed=true):lat>/lon=<float(signed=true):lon>', methods=('GET', 'POST'))
def display_data(lat, lon):
    with open('clearsky/config.json') as json_file:
        data = json.load(json_file)

        url_format = data['OpenWeather-url']
        api_key = data['OpenWeather-key']

    r = requests.get(url_format.format(lat, lon, api_key))
    return render_template('weatherpage/weather_data.html', lat=lat, lon=lon, json=r.text, url="http://slowe.github.io/VirtualSky/embed?longitude={}&latitude={}&projection=stereo&constellations=true&constellationlabels=true&showstarlabels=true".format(lon, lat))
