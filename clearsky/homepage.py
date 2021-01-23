from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask.signals import request_started

bp = Blueprint( 'home', __name__)

@bp.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        address = request.form['address']
        address.replace(', ', '+')
        address.replace(',', '+')
        address.replace(' ', '+')
        return redirect(url_for('weather-data.display_data', lat, lon))
    return render_template('homepage/home.html')
