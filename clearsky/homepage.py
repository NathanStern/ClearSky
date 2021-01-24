from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask.signals import request_started

import requests
import json

from clearsky.db import get_db

bp = Blueprint('home', __name__)

url_format = ""
headers = "{}"


@bp.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        address = request.form['address']
        address = address.replace(', ', '+')
        address = address.replace(',', '+')
        address = address.replace(' ', '+')

        with open('clearsky/config.json') as json_config:
            data = json.load(json_config)

            url_format = data['Radar.io-url']
            headers = {'Authorization': data['Radar.io-key']}

        r = requests.get(url_format.format(address), headers=headers)
        return_coords = r.json()

        lat = (return_coords["addresses"][0]["latitude"])
        lon = (return_coords["addresses"][0]["longitude"])

        return redirect(url_for('weather-data.display_data', lat=lat, lon=lon))

    db = get_db()

    posts = db.execute(
        'SELECT * FROM post'
    ).fetchall()

    return render_template('homepage/home.html', posts=posts)
