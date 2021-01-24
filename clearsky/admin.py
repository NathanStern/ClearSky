import functools
from os import sysconf_names

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask.signals import request_started

from werkzeug.security import check_password_hash, generate_password_hash

import json

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Creates a new view that wraps the original.
# If a user is not logged in, the user is redirected.
# If they are, the original view is shown


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('admin.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/login', methods=('GET', 'POST'))
def login():
    session['user_id'] = 0
    return redirect(url_for('admin.admin_home'))


@bp.route('/', methods=('GET', 'POST'))
@login_required
def admin_home():
    if request.method == "POST":
        if 'url-openweather' in request.form:
            data = None
            with open("config.json", 'r') as json_file:
                data = json.load(json_file)

            data["OpenWeather-url"] = request.form["url-openweather"]
            data["OpenWeather-key"] = request.form["key-openweather"]

            with open("config.json", "w") as json_file:
                json.dump(data)
        elif 'url-radario' in request.form:
            pass

    return render_template('admin/admin.html')


@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return redirect('/hello')

# Loads the logged in user before any views are loaded
# influences the page view that is loaded and shown to the user


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None

    else:
        # g.user = get_db().execute(
        #     'SELECT * FROM user WHERE id = ?', (user_id,)
        # ).fetchone()
        g.user = "Testing"
