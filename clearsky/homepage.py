from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask.signals import request_started

import requests
import json

bp = Blueprint( 'home', __name__)

url_format = "https://api.radar.io/v1/geocode/forward?query={}"
headers = {'Authorization': 'prj_test_sk_47928039de151f97a0ec5e38c8b9e085a4d45efb'}

@bp.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        address = request.form['address']
        address = address.replace(', ', '+')
        address = address.replace(',', '+')
        address = address.replace(' ', '+')

        r = requests.get(url_format.format(address), headers=headers)
        return_coords = r.json()

        lat = (return_coords["addresses"][0]["latitude"])
        lon = (return_coords["addresses"][0]["longitude"])
                
        return redirect(url_for('weather-data.display_data', lat=lat, lon=lon))
    return render_template('homepage/home.html')
