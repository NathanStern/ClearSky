#!/usr/bin/python3
from . import admin
import os

from flask import Flask
from flask import render_template
import json


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'clearsky.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

    else:
        # load the test config if it is passed
        app.config.from_pyfile(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def test_home():
        return render_template('base.html')

    from . import homepage
    app.register_blueprint(homepage.bp)

    from . import weather_data
    app.register_blueprint(weather_data.bp)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    if os.path.exists("clearsky/config.json"):
        pass
    else:
        with open('clearsky/config.json', 'w') as configuration:
            print("Opened config file")
            configuration.write("""
{
    "OpenWeather-url": " ",
    "OpenWeather-key": " ",
    "Radar.io-url": "https://api.radar.io/v1/geocode/forward?query={}",
    "Radar.io-key": " "
}
            """)

    # a simple page that just says hello

    @app.route('/hello')
    def hello():
        return "Hello, World!"

    from . import admin
    app.register_blueprint(admin.bp)

    return app
