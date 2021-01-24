from . import db
from flask import Flask, current_app
from . import create_app
import os

from . import db

app = create_app()

with app.app_context():
    if not os.path.exists(current_app.instance_path.join('clearsky.sqlite')):
        print("Initializing database for first-time use")
        db.init_db()
