import functools
from os import sysconf_names

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from flask.signals import request_started

from werkzeug.security import check_password_hash, generate_password_hash

import json

from clearsky.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


# Creates a new view that wraps the original.
# If a user is not logged in, the user is redirected.
# If they are, the original view is shown


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session['admin'] != 1:
            return redirect(url_for('admin.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = 'admin'
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM administrator WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['admin'] = 1
            flash(session['admin'])
            return redirect(url_for('admin.admin_home'))

        flash(session['admin'])

    return render_template('admin/login.html')


@bp.route('/', methods=('GET', 'POST'))
@login_required
def admin_home():
    if request.method == "POST":
        if 'passold' in request.form:
            old_password = request.form['passold']
            new_password = request.form['passnew']
            confirm_password = request.form['confirm']

            error = None

            db = get_db()

            if old_password == new_password:
                error = "Old password cannot equal new password"
            elif new_password != confirm_password:
                error = "Passwords do not match"
            elif not check_password_hash(db.execute('SELECT password FROM administrator WHERE username = ?', ('admin',)).fetchone()['password'], old_password):
                error = "Old password incorrect"
            else:
                pass

            if error is None:
                db.execute(
                    'UPDATE administrator SET password = ? WHERE username = ?', (generate_password_hash(
                        new_password), 'admin')
                )
                return redirect(url_for('admin.admin_home'))
            flash(error)

        if 'url-openweather' in request.form:
            data = None
            with open('clearsky/config.json', 'r') as json_file:
                data = json.load(json_file)
                json_file.close()

            data["OpenWeather-url"] = request.form["url-openweather"]
            data["OpenWeather-key"] = request.form["key-openweather"]

            with open('clearsky/config.json', "w") as json_file:
                json_output = json.dumps(data, sort_keys=True, indent=4)
                json_file.write(json_output)

                json_file.close()
        elif 'url-radario' in request.form:
            data = None
            with open('clearsky/config.json', 'r') as json_file:
                data = json.load(json_file)
                json_file.close()

            data["Radar.io-url"] = request.form["url-radario"]
            data["Radar.io-key"] = request.form["key-radario"]

            with open('clearsky/config.json', "w") as json_file:
                json_output = json.dumps(data, sort_keys=True, indent=4)
                json_file.write(json_output)

                json_file.close()

    db = get_db()

    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    users = db.execute(
        'SELECT * FROM user ORDER BY id DESC'
    ).fetchall()

    return render_template('admin/admin.html', users=users, posts=posts, config=json.load(open('clearsky/config.json', 'r')))


def get_post(id, check_author=False):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return post


@bp.route('/<int:id>/delete', methods=('POST', 'GET'))
@login_required
def delete(id):
    # get_post(id)
    db = get_db()
    db.execute(
        'DELETE FROM post WHERE id = ?', (id,)
    )
    db.commit()
    return redirect(url_for('admin.admin_home'))


@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return redirect(url_for('home.home'))

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
