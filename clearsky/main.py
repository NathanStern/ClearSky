from . import db
from flask import Flask, current_app
from . import create_app
import os

from . import db

app = create_app()

with app.app_context():
    if os.path.exists("clearsky/config.json"):
        pass
    else:
        with open('clearsky/config.json', 'w') as configuration:
            print("Opened config file")
            configuration.write("""
{
    "OpenWeather-url": "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=minutely,daily,alerts&appid={}&units=imperial",
    "OpenWeather-key": "536159a5b4c02240e63a25443055734b",
    "Radar.io-url": "https://api.radar.io/v1/geocode/forward?query={}",
    "Radar.io-key": "prj_test_sk_47928039de151f97a0ec5e38c8b9e085a4d45efb"
}
            """)

    if not os.path.exists(current_app.instance_path + "/" + ('clearsky.sqlite')):
        print("Initializing database for first-time use")
        db.init_db()
